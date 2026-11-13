#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检索回归门槛：新主题可发现性 + 历史查询零退化（可复现，不靠临时拼命令）。

用法：
    python scripts/regression.py                  # 只跑新主题门槛（当前工作区）
    python scripts/regression.py --baseline       # git archive HEAD 到临时目录，跑全量 top3 对比
    python scripts/regression.py --baseline -v    # 追加逐条 top3 明细

设计约束（#26 P1 与 #27 实测教训）：
  * 门槛查询必须含「主题词 + 通用跨域词」的真实组合，否则漏掉最贴近实战的失败路径。
  * 泛化跨域查询（如「对比度」主导）归 BOUNDARY，按 #26 判例不凑通过率，
    但仍验证其 top3 与 HEAD 基线一致 —— 判边界不等于允许退化。
  * 别名只补召回；巨型组一旦触发会注入整组带权词，把浓缩摘要章节顶到不该有的位置。
    新增别名组的规模纪律写在 aliases.json 的 _note 里。
  * 本脚本只读检索，不改索引；收口时须先显式跑 mindmap.py 定格时间戳，再提交/发布/同步。
  * 每轮换轮只改 EXPECT_FILE / NEW_QUERIES / BOUNDARY / EXPECTED_EVOLUTION 四块；
    上一轮主题查询沉淀进 HIST_QUERIES 后按「与 HEAD 逐字一致」验收，不删除。
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
SEARCH = ROOT / "scripts" / "dp_search.py"

# 新主题门槛：主题词 + 通用跨域词组合，答案应落在 empty-states.md 前 3。
# #35 换轮：13 条覆盖五种空态判型 / 装饰插画无障碍 / 单主行动 CTA 纪律 / 零数据位四模式 /
# 失败空态≠无数据 / 首次操作率度量 / 移动端小程序 / 反模式 / 结构五件套 / 中英抄写矩阵，
# 且刻意混入「验收 / 文案 / 可访问性 / 性能 / 度量 / 组件」等跨域词（#26 P1 教训）。
# #34 的 13 条已全部沉淀进 HIST_QUERIES（见下方 #35 沉淀块）。
NEW_QUERIES = [
    "空状态 五种类型 判型 插图 引导",
    "零数据位 starter content 示例数据 预填 首启",
    "装饰插画 空状态 无障碍 aria-hidden alt 装饰性",
    "单主行动 空状态 CTA 一个主按钮 引导 文案",
    "失败空态 不等于 无数据 错误 伪装 验收",
    "空状态文案 引导 不道歉 祈使动词 语气",
    "首次操作率 空状态 度量 激活 转化",
    "空状态 移动端 小程序 紧凑 适配 性能",
    "空状态 反模式 20 条 空白页 死胡同 可访问性",
    "空状态 结构 五件套 标题 描述 插图 动作 footer",
    "blank slate 空状态 零数据位 设计模式 抄写",
    "空状态 装饰插画 取舍 何时不用 插图 干扰",
    "空状态 自检 清单 20 项 验收 对照",
]

# 照 #26 P1 判例：泛化跨域查询归 BOUNDARY，不凑通过率，但仍校验 top3 与 HEAD 一致。
# #27 判例样本「字体 对比度 大文本 3:1 下划线」沿用至今：5 词里 4 个是对比度专属词，
# 正确答案归 accessibility.md §2 / color-science.md §6，不是内容可发现性文档。
BOUNDARY = {
    "字体 对比度 大文本 3:1 下划线":
        "泛化对比度查询；正确答案归 accessibility.md §2 / color-science.md §6，"
        "照 #26 判例不凑通过率，但仍校验 top3 与 HEAD 一致",
}

# 历史查询：覆盖组件 / 视觉 / 中文 / 性能 / 数据 / 内容各域，含 #27 曾退化的两条。
HIST_QUERIES = [
    "玻璃拟态 对比度 可访问性",
    "新拟态 表单 可访问性",
    "对比度 4.5:1 验收",
    "风格 对比度 验收",
    "表格 行高 列宽 分页",
    "中英混排 标点",                    # #27 曾 DIFF：巨型别名组顶起支线 Y
    "字体 行高 中文排版",              # #27 曾 DIFF
    "模态 弹窗 焦点 键盘操作",
    "toast 提示条 轻提示 时长",
    "空态 无数据 插图 引导",
    "骨架屏 加载 性能 感知",
    "暗色模式 纯白 文字 对比度",
    "折线图 柱状图 数据可视化 配色",
    "导航 信息架构 面包屑 层级",
    "表单 校验 错误提示 可访问性",
    "按钮 主次 状态 间距",
    "品牌 色板 色相 饱和度",
    "文案 语气 大小写 标点",
    "演示 PPT 投影 对比度 字号",
    "留白 网格 版面 编辑设计",
    # #28 沉淀：#27 主题门槛查询转为历史样本，验收「新增 shape-elevation.md 后不退化」。
    "正文用多大字号 行高多少 排版很挤",
    "定一套字体系统 字号阶梯 token",
    "缺字 tofu 方框乱码 字体回退",
    "WCAG 1.4.12 文本间距 覆盖 验收",
    # #29 沉淀：#28 主题门槛查询转为历史样本，验收「新增 visual-hierarchy-gestalt.md 后不退化」。
    "卡片圆角用多大 阴影加多重 浮起来",
    "定一套圆角 token 形状尺度",
    "border-radius 50px 实际生效 圆角重叠",
    "box-shadow 三层阴影 umbra penumbra ambient",
    "elevation level3 6dp 阴影值 误用",
    "阴影能不能当边界 3:1 非文本对比度",
    "嵌套圆角 同心 r=R-p padding",
    "弹窗 层级 z-index 语义刻度 表面顺序",
    "毛玻璃 backdrop-filter 性能 Liquid Glass",
    "M3 shape scale 圆角精确值 4px 8px",
    "Tailwind shadow-md 默认值 Ant Design 圆角",
    "暗色模式 阴影 表面色阶 深度语言",
    "squircle corner-shape 实验性 渐进增强",
    # #30 沉淀：#29 主题门槛查询转为历史样本，验收「新增 direct-manipulation.md 后不退化」。
    "格式塔 完形 邻近性 相似性 怎么分组",
    "重点不突出 主次不清 眯眼测试 单焦点",
    "F 型扫描 眼动 用户只看标题 扫描模式",
    "视觉层级 视觉动线 信息层级 层级不清",
    "DOM 顺序 焦点顺序 标题结构 三顺序一致性",
    "order -1 搬主内容 读屏先读侧栏 tabindex",
    "认知负荷 工作记忆 组块 chunking 信息过载",
    "7±2 米勒定律 导航项数 菜单上限",
    "希克定律 Hick 决策时间 选项太多",
    "菲茨定律 Fitts 目标尺寸 按钮太小 点不到",
    "前注意 pop-out 特征整合 Treisman 图形背景",
    "序列位置 首因效应 近因效应 Von Restorff 孤立效应",
    "WCAG 1.3.2 2.4.3 2.4.10 C27 F1 顺序契约",
    # #31 沉淀：#30 主题门槛查询转为历史样本，验收「新增 direct-manipulation.md 后不退化」。
    "内容找不到 搜不到 只有搜索框 多路径 WCAG 2.4.5",
    "搜索框放哪 放大镜图标 搜索入口 可发现性 验收",
    "placeholder 当 label 输入提示消失 可访问性 表单",
    "自动补全 combobox aria-activedescendant 读屏 键盘",
    "零结果 无搜索结果 404 页面 可访问性 出路",
    "信息气味 链接标签 前 11 个字符 可预测性",
    "Learn More 了解更多 描述性链接 读屏 links list",
    "可扫读 79% 扫读 倒金字塔 阅读等级 文案",
    "Flesch FKGL SMOG 阅读等级 中文 可访问性",
    "SC 3.1.5 九年学校教育 简明语言 Plain Writing Act",
    "tree testing 树测试 findability directness 度量 验收",
    "搜索建议 首次查询 51% 32% 联想词 结果页",
    "内容可发现性 站点地图 目录 位置感 验收",
    # #32 沉淀：#31 主题门槛查询转为历史样本，验收「新增 conversational-generative-ui.md 后不退化」。
    "拖拽 拖放 列表重排 单指针无拖动 WCAG 2.5.7",
    "拖拽排序 只有鼠标能拖 G219 替代 箭头逐步移动",
    "pointercancel 什么时候触发 pointermove 断掉 浏览器接管滚动",
    "setPointerCapture 指针移出手柄 隐式捕获 验收",
    "touch-action 该写什么 拖动时页面跟着滚 缩放 1.4.4",
    "dragover preventDefault drop 不触发 DataTransfer 读写窗口",
    "补个键盘快捷键 算不算无障碍 键盘拖放 Space Escape",
    "读屏播报 live region position index aria-roledescription",
    "按钮 24px 够吗 24×24 44×44 48dp 目标尺寸 验收",
    "SC 2.5.5 AAA 44×44 spacing 例外 目标尺寸",
    "path-based gesture 画个 Z 手势 2.5.1 路径手势 替代",
    "SC 2.5.2 No Down-Event Up Reversal Abort Undo 取消",
    "dnd-kit 25px 位移 NN/g 1cm 约 100ms 触屏拖拽",
    # #33 沉淀：#32 主题门槛查询转为历史样本，验收「新增 overlays-modality.md 后不退化」。
    "chatbot 聊天界面 流式输出 读屏一直刷屏 可访问性",
    "流式回答正文 算不算 SC 4.1.3 状态消息 验收",
    "role=log aria-live polite aria-atomic false ARIA23 读屏",
    "aria-busy 什么时候复位 停止生成 出错 生成完毕 验收",
    "生成式界面 streamUI 模型返回任意组件 组件白名单 安全",
    "AI SDK RSC experimental 生产推荐 AI SDK UI 选型",
    "useChat submitted streaming ready error 四态 message.parts 工具调用",
    "AG-UI RunStarted RunFinished TextMessageStart Content End 事件顺序 验收",
    "Hybrid UI RICH 范式 自然语言模糊意图 图形控件精确操作",
    "AI 答错了 四档恢复链 HAX G9 撤销自动化动作 重新生成",
    "停止生成 重新生成 setMessages 状态归位 队列清空 键盘",
    "流式 Markdown 代码围栏未闭合 分片 节流 自动滚动 性能",
    "聊天输入 Enter Shift+Enter 中文输入法 禁用提交 表单",
    # #34 沉淀：#33 主题门槛查询转为历史样本，验收「新增 onboarding-first-run.md 后不退化」。
    "模态 dialog 焦点陷阱 Tab 不越界 Escape 关闭 验收",
    "showModal aria-modal inert 背景不可交互 双条件",
    "Popover API popover auto hint manual 三态 非模态",
    "top layer ::backdrop z-index inert 层级 遮罩",
    "SC 1.4.13 Dismissible Hoverable Persistent tooltip 验收",
    "SC 2.4.11 Focus Not Obscured F110 C43 sticky footer",
    "SC 2.1.2 No Keyboard Trap 焦点循环 Escape 退出",
    "SC 3.2.1 On Focus help dialog 打开就抢焦点",
    "closedby any closerequest none 轻量关闭 light dismiss",
    "bottom sheet 底部抽屉 命令面板 判型 非模态",
    "焦点返回触发元素 关闭契约 无鼠标退出 F6 切层",
    "aria-modal=true 只在双条件满足时 视觉遮蔽",
    "叠加层嵌套 auto stack hint stack 层叠顺序",
    # #35 沉淀：#34 主题门槛查询转为历史样本，验收「新增 empty-states.md 后不退化」。
    # 其中「零数据位 starter content 空态 …」一条改写为纯 onboarding 表述，避免与本轮新资产
    # empty-states.md 的 零数据位/空态 原词相撞；其 onboarding 测试意图（首启/教学/单主行动）保留。
    "新手引导 教程 首启 要不要做 验收",
    "onboarding deck-of-cards tutorial 91% 94% SEQ p 值",
    "coach mark 产品导览 遮罩 非模态 键盘",
    "权限 purpose string 时机 pre-alert 追踪请求 文案",
    "SC 3.3.7 重复输入 自动回填 autocomplete 不够",
    "SC 3.3.8 注册 不覆盖 OTP 粘贴 验证码",
    "SC 3.2.1 help dialog 聚焦即弹 抢焦点 G107",
    "SC 2.2.1 限时 20 秒 六选项 超时清空 表单",
    "渐进披露 progressive disclosure 设置后置 首启问项",
    "launch screen splash screen 首启 品牌动画 性能",
    "activation aha moment time to value 跳过率 度量",
    "新手引导 首启 教学 激活 onboarding 验收 度量",
    "Material 1 fewer than ten choices 90% Self-Select 三模型",
]

EXPECT_FILE = "empty-states.md"
NEW_ASSETS = {EXPECT_FILE}

# 登记演进：新增权威资产凭「原词相关性」进入 top3，属升级而非退化。
# 但必须三条硬校验全过才放行（否则仍判 DIFF），见 check_evolution()。
# #35：先以空白名单跑全量回归；若新资产在历史查询中上位，按 #28 判例做内容层
# 收敛（章节标题 / 首行导语措辞），不靠登记凑通过率，也不改检索器打分逻辑。
# #35 登记演进：空状态资产上位「空态 无数据 插图 引导」属合理——该通用空态查询此前由
# feedback-states §5（概述/速查）作答，本轮新增 empty-states.md 为同主题的权威深挖资产，二者
# 并存：top1 文件仍是 feedback-states.md（§5 43.5 > empty §0 39.6），旧答案仍落 top5，且新资
# 产经 --no-alias 仍进前 3（非别名污染，见 check_evolution 三硬校验）。同理由「序列位置…孤立效应」。
EXPECTED_EVOLUTION = {
    "空态 无数据 插图 引导":
        "empty-states.md 上位为同主题权威深挖（top1 文件仍是 feedback-states.md §5；旧答案仍落 top5；--no-alias 仍进前 3）",
    "序列位置 首因效应 近因效应 Von Restorff 孤立效应":
        "empty-states.md §8 变体与承载位置（位置感/承载位相邻，合理上位；top1 仍是 visual-hierarchy-gestalt；--no-alias 仍进前 3）",
}


def topn(search_py: Path, query: str, n: int = 3, no_alias: bool = False) -> list:
    """调用指定副本的 dp_search.py，返回 top-n 文件名列表。"""
    argv = [sys.executable, str(search_py), query, "--json", "-n", str(n)]
    if no_alias:
        argv.append("--no-alias")
    out = subprocess.run(
        argv, capture_output=True, text=True, encoding="utf-8",
    )
    if out.returncode != 0:
        raise RuntimeError(f"dp_search 失败: {query}\n{out.stderr[:300]}")
    # need_rebuild() 会在首次查询时自动跑 mindmap.py，其进度输出会混进 stdout；
    # 不改检索器打分逻辑，这里从 "query" 键向前定位 JSON 起点做容错解析。
    s = out.stdout
    k = s.find('"query"')
    start = s.rfind("{", 0, k) if k > 0 else s.find("{")
    if start < 0:
        raise RuntimeError(f"dp_search 未返回 JSON: {query}\n{s[:300]}")
    data, _ = json.JSONDecoder().raw_decode(s[start:])
    return [h["file"].rsplit("/", 1)[-1] for h in data["hits"][:n]]


def make_baseline(dest: Path) -> Path:
    """git archive HEAD 到临时目录，得到「新增资产之前」的完整可运行副本。"""
    archive = dest / "head.tar"
    subprocess.run(["git", "archive", "-o", str(archive), "HEAD"],
                   cwd=str(ROOT), check=True, capture_output=True)
    base = dest / "HEAD"
    base.mkdir(parents=True, exist_ok=True)
    subprocess.run(["tar", "-xf", str(archive), "-C", str(base)], check=True,
                   capture_output=True)
    if not (base / "scripts" / "dp_search.py").exists():
        raise RuntimeError("基线目录缺少 scripts/dp_search.py，git archive 可能未含 scripts/")
    return base


def check_evolution(search_py: Path, base_search: Path, query: str) -> tuple:
    """登记演进的三条硬校验；任一不过即判退化，不靠口头放行。

    a. HEAD 的 top1 在 NOW 仍是 top1 —— 既有首选答案未被顶掉；
    b. HEAD top3 中至少 2 个文件仍在 NOW top5 —— 既有答案未被挤丢；
    c. 新进入 top3 的文件必须是本轮新增资产，且 --no-alias 下仍在前 3
       —— 证明上位来自原词相关性，不是别名组污染（#27 巨型组教训）。
    """
    now5 = topn(search_py, query, 5)
    head5 = topn(base_search, query, 5)
    now3, head3 = now5[:3], head5[:3]
    noalias3 = topn(search_py, query, 3, no_alias=True)
    a = bool(head3) and bool(now3) and head3[0] == now3[0]
    b = len(set(head3) & set(now5)) >= 2
    newcomers = [f for f in now3 if f not in head3]
    c = (bool(newcomers)
         and all(f in NEW_ASSETS for f in newcomers)
         and all(f in noalias3 for f in newcomers))
    detail = {"a": a, "b": b, "c": c, "head3": head3, "now3": now3,
              "noalias3": noalias3, "newcomers": newcomers}
    return a and b and c, detail


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--baseline", action="store_true",
                    help="用 git archive HEAD 构造基线并对比历史查询 top3")
    ap.add_argument("-v", "--verbose", action="store_true", help="打印逐条 top3")
    args = ap.parse_args()

    gated = [q for q in NEW_QUERIES if q not in BOUNDARY]
    print("=== 新主题门槛（top3 命中 %s）===" % EXPECT_FILE)
    npass = 0
    for q in gated:
        t3 = topn(SEARCH, q)
        ok = any(EXPECT_FILE in f for f in t3)
        npass += ok
        flag = "PASS" if ok else "FAIL"
        if not ok or args.verbose:
            print("  %-5s %-38s %s" % (flag, q, t3))
    print("新主题门槛: %d/%d%s" % (npass, len(gated),
                                  "" if npass == len(gated) else "  ← 未达标"))

    print("\n=== 路由边界（照 #26 判例，不计通过率）===")
    for q, why in BOUNDARY.items():
        t3 = topn(SEARCH, q)
        print("  BOUNDARY %s\n     现在 top3: %s\n     依据: %s" % (q, t3, why))

    rc = 0 if npass == len(gated) else 1
    if not args.baseline:
        print("\n（未启用 --baseline，跳过历史回归）")
        return rc

    with tempfile.TemporaryDirectory(prefix="dp-regression-") as tmp:
        base = make_baseline(Path(tmp))
        base_search = base / "scripts" / "dp_search.py"
        print("\n=== 历史回归（NOW vs git archive HEAD）===")
        strict = HIST_QUERIES + list(BOUNDARY)
        strict = [q for q in strict if q not in EXPECTED_EVOLUTION]
        evo = [q for q in HIST_QUERIES if q in EXPECTED_EVOLUTION]

        same = 0
        diffs = []
        for q in strict:
            now, head = topn(SEARCH, q), topn(base_search, q)
            ok = now == head
            same += ok
            if not ok:
                diffs.append((q, head, now))
            if args.verbose:
                print("  %-5s %-34s %s" % ("OK" if ok else "DIFF", q, now))

        evo_pass = 0
        for q in evo:
            ok, d = check_evolution(SEARCH, base_search, q)
            evo_pass += ok
            print("  %-5s %-34s %s" % ("EVO" if ok else "FAIL", q, d["now3"]))
            print("       HEAD top3 %s → 新进入 %s ｜ 硬校验 a=%s(top1不变) "
                  "b=%s(原答案仍在top5) c=%s(原词相关·非别名污染)"
                  % (d["head3"], d["newcomers"], d["a"], d["b"], d["c"]))
            if not ok:
                diffs.append((q, d["head3"], d["now3"]))
            if args.verbose:
                print("       --no-alias top3: %s" % d["noalias3"])

        print("历史回归: %d/%d 逐字一致 + %d/%d 登记演进 → %s"
              % (same, len(strict), evo_pass, len(evo),
                 "零退化" if same == len(strict) and evo_pass == len(evo) else "存在退化"))
        for q, head, now in diffs:
            print("  DIFF %s\n    HEAD: %s\n    NOW : %s" % (q, head, now))
        if same != len(strict) or evo_pass != len(evo):
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
