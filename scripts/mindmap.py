#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
design-partner 记忆树生成器

扫描 SKILL.md / references/*.md / memory/*.md，产出两样东西：
  1) memory/index.json —— 机器索引（文件 → 章节 → 摘要 + 行号），供 dp_search.py 检索
  2) memory/tree.md     —— 人/agent 可读的知识树 + 意图路由 + 主题索引 + 接线体检

为什么需要它：
    技能资产到 11 份、上千行后，"知识在哪个文件哪一节"本身成了问题。
    没有索引时 agent 只能整份读，浪费上下文；有了索引可以先定位再精读。

用法:
    python scripts/mindmap.py              # 重建索引与树
    python scripts/mindmap.py --check      # 只做接线体检（SKILL.md 是否收录所有资产）
"""
import json
import re
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "references"
MEM = ROOT / "memory"
SKILL = ROOT / "SKILL.md"

H2 = re.compile(r"^(#{2,3})\s+(.+?)\s*$", re.M)
FENCE = re.compile(r"```.*?```", re.S)
LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
EMPH = re.compile(r"[*_`>|]")

# 意图 → 该去哪儿（保持与 SKILL.md 第 1 步的路由一致，树里做快捷方式）
INTENTS = [
    ("从零做视觉", "第 5 步原则 + patterns.md 取构型 + design-tokens.md 取数值"),
    ("改进现有设计", "按第 5 步逐条诊断；动效问题查 motion-system.md §10 验收清单"),
    ("要灵感 / 参考", "patterns.md（元素级）→ inspiration.md（风格级）→ portfolios.md（校准）"),
    ("要设计规范 / 系统", "design-tokens.md（三层 token）→ design-md-format.md（九章骨架）"),
    ("对标某品牌", "design-md-format.md §3 品牌 DNA + design-tokens.md 取精确值"),
    ("中文项目", "chinese-design.md（排版/生态）→ motion-system.md §9（小程序）"),
    ("动效 / 微交互 / 动画", "motion-system.md：§2 曲线 · §3 时长 · §4 场景表 · §7 代码 · §10 验收"),
    ("滚动动画 / 页面转场", "motion-system.md §7.3 View Transitions · §7.4 scroll-driven"),
    ("无障碍 / reduced-motion", "motion-system.md §8.1 三档降级"),
    ("提示 / toast / 弹窗 / 确认", "feedback-states.md：§1 层级决策 · §3 toast 数值 · §7 确认与破坏性操作"),
    ("加载 / 骨架屏 / 进度", "feedback-states.md：§2 时间阈值 · §4 加载与进度 · §14.2 骨架代码"),
    ("空状态 / 无数据 / 失败空", "feedback-states.md §5（五种空 + 五件套结构 + 文案公式）"),
    ("错误页 / 报错文案 / 重试", "feedback-states.md §6（五级错误 + 404/500 规则 + 三段式文案）"),
    ("找工具 / 资产", "tools.md（工具）· resources.md（图标/字体/3D）· component-libraries.md（代码）"),
    ("想提升自己 / 学习路径", "knowledge-map.md L0→L4 + 20 条自测"),
    ("AI 生成设计 / AIGC 工作流", "ai-design-toolchain.md §1 五层人工闸门 · §9 八步工作流 · §13 选型三问"),
    ("AI 内容标识 / 合规 / 版权 / 提示词 / AI 味验收", "ai-design-toolchain.md §2 标识 · §4 USCO 裁决 · §8 提示词 · §11 AI Slop Test · §20 自检"),
    ("设计伦理 / 欺骗性设计 / 隐私同意 / 自动续费 / 一键关闭", "design-ethics-inclusion.md §1 三条立场 · §2 现行 18 类 · §4 对称选择 · §8 一键关闭 · §9 反陈旧裁决 · §21 脚本"),
    ("包容性设计 / 认知无障碍 / 未成年人 / 成瘾设计", "design-ethics-inclusion.md §11 令第 766 号 · §12 成瘾四红线 · §14 三原则 · §15 七原则 · §16 COGA 八目标 · §17 四象限"),
    ("组件 API / props 契约 / 受控非受控 / 组合 / 插槽 / asChild / 换元素", "component-api-design.md §1 三份所有权 · §2 受控契约 · §5 五种换元素 API · §7 合并优先级 · §8 compound components"),
    ("ref 转发 / React 19 forwardRef / 复合组件键盘 / roving tabindex / 组件发版 SemVer / argTypes", "component-api-design.md §9 反陈旧裁决 · §12 APG 键盘契约 · §14 API SemVer 六冻结面 · §15 Storybook argTypes · §20 脚本"),
    ("设计度量 / 用户研究 / 可用性测试 / SUS / 样本量 / HEART / A-B 测试", "design-measurement-research.md §0 分层导语 · §1 度量三步法 · §3 任务级指标 · §4 SUS/UMUX · §5 问卷量表 · §7 样本量 · §11 A/B 统计"),
    ("满意度怎么量化 / 改版有没有效 / 要不要上线 A-B / 该做多少人的研究", "design-measurement-research.md §21 四段可抄代码（问题暴露率·比例样本量·SUS 计分·A/B z 检验）· §23 接线与其他资产"),
    ("导航 / 导航栏 / 菜单 / 信息架构", "navigation-ia.md §1 四类职责 → §2 形态决策 → §3 项数铁律 → §7 移动端降级"),
    ("信息架构 / 网站结构 / 菜单组织", "navigation-ia.md §4（深度 vs 广度 / 3-click 迷思 / 信息气味 / 卡片分类·树测试）"),
    ("面包屑 / 当前位置", "navigation-ia.md §5（位置型/属性型/路径型 + 末级非链接 + aria-current）"),
    ("标签页 Tabs", "navigation-ia.md §6（APG tabs 键盘契约 + tabpanel + 何时用 tabs vs 侧栏）"),
    ("底部 Tab / 移动端导航 / 汉堡", "navigation-ia.md §7（Apple ≤5 项 / Material bar·rail·drawer / NN/g 可发现性）+ responsive-layout §9 降级路径"),
    ("当前位置指示 / 激活态 / you are here", "navigation-ia.md §8（≥2 信号 + aria-current + 聚焦态独立）"),
    ("导航可访问性 / skip link / 地标", "navigation-ia.md §9（2.4.1 skip link / 1.3.1 landmark / 2.4.5 multiple ways / 2.4.7 焦点）+ accessibility §3"),
    ("搜索与导航", "navigation-ia.md §10（搜索是导航备份 + 占位符写示例 + 零结果三件套）"),
    ("设计评审 / critique / 设计走查", "references/design-critique.md §1 两种评审分清 + §2 三前提 + §5 RACI/远程异步"),
    ("给反馈 / 反馈话术 / I like I wish I wonder / 2 正 1 改", "references/design-critique.md §3 给反馈七铁律"),
    ("接收反馈 / 怎么不辩护 / 别人挑刺怎么应对", "references/design-critique.md §4 接收反馈四步"),
    ("设计 by committee / HiPPO / 谁说了算 / 委员会改稿", "references/design-critique.md §5 Decider + §7 反模式"),
    ("决策留痕 / ADR / 评审结论去哪了", "references/design-critique.md §8 ADR / critique notes 模板"),
    ("评判框架 / 严重度 0–4 / NN/g 10 启发式", "references/design-critique.md §6 评判框架"),
    ("视觉风格 / 风格匹配 / 做成 XX 那种感觉 / 高级感 / 视觉调性", "references/visual-style-taxonomy.md §2 四维信号 → §4 匹配决策（参考站四步 / 形容词先确认语境）"),
    ("风格谱系 / 设计运动 / 玻璃拟态 / 新拟态 / 野兽派 / Y2K / Bento", "references/visual-style-taxonomy.md §3 编年谱系 + §5 混搭纪律 + §6 趋势生命周期"),
    ("风格诊断 / 风格不一致 / 潮流该不该跟", "references/visual-style-taxonomy.md §10 反模式 20 条 + §11 自检 20 项 + §6 生命周期"),
    ("字体排印 / 字号 / 行高 / 行距 / 定一套字体系统 / 排版很挤", "references/typography-system.md §2 六层模型判层 → §4 rem 阶梯（px 不可访问）→ §5 行高两档与行长 → §17 M3 五角色×三尺寸落 token"),
    ("文本间距 / WCAG 1.4.12 / 200% 缩放 / 放大就裁切 / 表单 label 重叠 / 可访问性验收", "references/typography-system.md §6 三关硬数值 + §7 注入验收五步（§23.3 书签）+ §8 两种缩放与容器弹性 + §23.5 静态扫描"),
    ("中文排版 / 中英混排 / 缺字 tofu / 字体回退 / 全角半角 / 字素丛", "references/typography-system.md §16 W3C clreq（1/4 汉字宽·1:1 正方形·全角 ASCII·UAX #29）+ §12 逐字符回退 + §13 unicode-range 分片"),
    ("数字抖动 / tabular-nums / 可变字体 / 字体加载闪烁 / CLS / 字体商用授权", "references/typography-system.md §10 OpenType 数字特性 + §9 五注册轴 + §14 font-display 五档 + §15 size-adjust + §18 OFL 1.1 五条件 + §19 仓库实测"),
    ("不确定知识在哪", "python scripts/dp_search.py \"关键词\""),
    ("圆角 / 形状 / 半径", "shape-elevation.md §10 语法 · §11 corner overlap · §12 同心 r=R−p · §13 七体系精确值"),
    ("阴影 / 投影 / 三层阴影", "shape-elevation.md §7 box-shadow 语法 · §8 七体系对照 · §9 物理分解 · §23.1 token"),
    ("高度层级 / elevation / 表面浮起", "shape-elevation.md §3 语义裁决 · §4 六级 dp · §15 Carbon Layering · §19 深度语言"),
    ("边界看不见 / 阴影当 3:1", "shape-elevation.md §5 实跑对比度 · §6 非文本 3:1 正确落点 · accessibility.md §2"),
    ("材质 / 毛玻璃 / z-index", "shape-elevation.md §16 Apple Materials · §17 性能红线 · §18 语义 z-index · §23.6 渐进增强"),
    ("格式塔 / 完形 / 组织律 / 邻近性 / 分组", "visual-hierarchy-gestalt.md §7 IxDF 12 条全表 · §8 可验收四规则 · §9 前注意 pop-out"),
    ("视觉层级 / 重点不突出 / 主次不清 / 眯眼测试 / 单焦点", "visual-hierarchy-gestalt.md §2 三层模型判层 · §3 F 型非目标 · §10 图形背景与多稳态 · §15 Von Restorff"),
    ("眼动 / F 型 / 扫描模式 / RTL 动线 / 用户只看标题", "visual-hierarchy-gestalt.md §3 NN/g 逐字裁决 · §4 八种扫描模式诊断表 · §6 RTL 与断点复核"),
    ("认知负荷 / 7±2 / 选项太多 / 希克定律 / 菲茨定律 / 组块", "visual-hierarchy-gestalt.md §11 三分与 7±2 误用 · §12 Hick 公式与失效条件 · §13 Fitts 三形式 · §14 chunking"),
    ("DOM 顺序 / 焦点顺序 / 标题结构 / tabindex / 三顺序一致性", "visual-hierarchy-gestalt.md §5 四条 WCAG 准则逐字原文 · §6 一致性验收 · §23.2 静态扫描器 · §23.5 C27 正例"),
    ("内容找不到 / 搜不到 / 可发现性 / 多路径 / 站点地图", "content-findability.md §2 四层链路判层 → §3 SC 2.4.5 至少两条路 → §4 搜索入口 → §19 位置感清单"),
    ("链接文案 / Learn More / 信息气味 / 前 11 个字符", "content-findability.md §10 SC 2.4.4 A · 2.4.9 AAA · 3.2.4 AA → §9 信息气味 → §12 nano-content → §13 三种改法 → §26.2 扫描器"),
    ("可扫读 / 阅读等级 / 简明语言 / Flesch / 中文", "content-findability.md §11 NN/g 79%/16% → §14 SC 3.1.5 九年门槛 → §15 三公式不可换算 → §16 中文代理指标 → §17 Plain Writing Act → §26.1 计算器"),
    ("零结果 / 404 / 自动补全 combobox / placeholder 不是 label", "content-findability.md §5 SC 3.3.2 → §6 APG combobox 契约 → §18 零结果与 GOV.UK 404 四条禁令 → §26.3 契约检查器"),
    ("树测试 / findability / directness / 卡片分类", "content-findability.md §20 度量口径（定性结果不可冒充百分比）→ §21 六步构建流程"),
    ("拖拽 / 拖放 / 列表重排 / 排序 / 直接操纵", "direct-manipulation.md §2 四段链路判层 → §3 SC 2.5.7 单指针无拖动 → §4 G219 四类替代 → §7 完整状态机"),
    ("指针事件 / pointercancel / setPointerCapture / touch-action", "direct-manipulation.md §9 PE3 规范性抑制链 → §10 MDN 工程契约 → §11 touch-action 全值表 → §12 HTML DnD 七事件"),
    ("拖动无障碍 / 键盘拖放 / 读屏播报 / Escape 取消", "direct-manipulation.md §5 SC 2.5.1 交叉约束 → §6 SC 2.5.2 与 G210 → §13 dnd-kit 键盘默认 → §14 live region"),
    ("目标尺寸 / 点击区 / 触控目标 / 24×24 / 44×44 / 48dp", "direct-manipulation.md §8 三口径裁决表 → §17 阈值与时序决策表 → §25.1 目标尺寸判定器"),
    ("手势 / 路径手势 / 长按 / 触屏拖动 / 磁吸", "direct-manipulation.md §5 SC 2.5.1 路径手势 → §15 NN/g signifier → §16 1cm×1cm 与约 100ms → §19 替代路径矩阵 → §20 库生态选型"),
    ("对话式界面 / 聊天 UI / chatbot / 流式输出 / 打字机效果", "conversational-generative-ui.md §2 五段链路判层 → §3 SC 4.1.3 裁决一 → §4 ARIA23 role=log → §5 live region 契约 → §12 状态边界播报一次"),
    ("生成式界面 / GenUI / streamUI / 组件白名单 / 动态组件", "conversational-generative-ui.md §6 裁决二 → §7 RSC experimental 与生产路径 → §8 message.parts → §20 代码 4 白名单分派"),
    ("对话状态机 / useChat / message.parts / AG-UI 事件", "conversational-generative-ui.md §8 四态逐字 → §9 AG-UI 三模式与生命周期边界 → §13 状态归位表 → §20 代码 1 事件流校验器"),
    ("AI 答错了 / 停止生成 / 重新生成 / 纠错 / 撤销自动化动作", "先读 conversational-generative-ui.md §11 HAX G9 四档恢复链 → §12 → §13；HAX 原则层 18 条归 ai-design-toolchain.md §10"),
    ("混合界面 / Hybrid UI / RICH 范式 / 读屏刷屏 / aria-busy", "conversational-generative-ui.md §10 RICH 四要素与 WIMP 判型 → §5 aria-busy 三出口 → §16 来源与引用 → §17 场景 7/8"),
    ("模态判型 / 焦点陷阱 / inert / aria-modal / 四问判型", "overlays-modality.md §1 四问判型 → §3 APG 焦点契约 → §4 aria-modal 双条件 → §20.1 判型器"),
    ("原生 dialog / showModal / closedby / ::backdrop / returnValue", "overlays-modality.md §5 showModal 与 top layer → §7 ::backdrop 与 z-index 分界 → §13 关闭契约 → §20.4 原生骨架"),
    ("Popover API / popover 三态 / auto hint manual / 顶层栈", "overlays-modality.md §6 always non-modal 与双栈六规则 → §7 top layer → §14 层叠嵌套 → §15 组件族谱"),
    ("hover 浮层 / tooltip / SC 1.4.13 / Dismissible Hoverable Persistent", "overlays-modality.md §9 三条件 → §12 SC 3.2.1 help dialog 失败例 → §20.2 校验器"),
    ("浮层遮挡 / SC 2.4.11 / F110 / C43 / 退出契约", "overlays-modality.md §10 modal always pass 与 Note 2 三出路 → §11 SC 2.1.2 → §13 关闭契约 → §20.3 遮挡裁决器"),
    ("首次体验 / onboarding / 新手引导 / 要不要做教程", "onboarding-first-run.md §0 一句话立场 → §3 六问判型（Q4 先测无引导是闸门）→ §7 NN/g 实证全表与四条限制 → §20.1 判型器"),
    ("教程 / coach mark / 产品导览 / 首启轮播 / 跳过后又弹", "onboarding-first-run.md §4 六类形态矩阵 → §9 Apple tips 阈值 → §12 Tour 精确 props 与叠加层契约 → §18 反模式"),
    ("权限时机 / purpose string / pre-alert / 追踪弹窗 / 授权文案", "onboarding-first-run.md §2 裁决二 → §10 时机矩阵与 purpose string 三行正反例 + pre-alert 作用域警告 → §20.2 验收器"),
    ("注册向导 / 重复输入 / 验证码 / 超时 / SC 3.3.7 3.3.8 3.2.1 2.2.1", "onboarding-first-run.md §2 裁决三 → §11 四条款合取表 → §20.3 检查器；条款明细归 form-table.md / accessibility.md"),
    ("激活 / aha moment / time to value / 跳过率 / 零数据位", "onboarding-first-run.md §14 口径与跳过率陷阱 → §13 教学型零数据位 → §5 设置后置；统计方法归 design-measurement-research.md"),
    ("渐进披露 / splash / launch screen / 首启性能 / 设置后置", "onboarding-first-run.md §5 四类可延后清单 → §6 三分界 → §8 Material 1 归档数值；LCP 与首包归 performance-design.md"),
    ("空状态 / 零数据位 / 装饰插画 / starter content / 空状态文案矩阵", "empty-states.md §4 中英抄写矩阵 → §3 结构五件套 → §7 零数据位 → §5 装饰插画 → §8 变体 → §9 无障碍 → §12 度量"),
    ("定价页 / 三档套餐 / 月年切换 / 推荐档 / 价格数字排版", "pricing-checkout.md §2 四种构型 → §3 价格数字表 → §6 月年切换器 → §5 对比表与 CTA"),
    ("结账流程 / checkout / 结算页 / 复核页 / 承诺闸门", "pricing-checkout.md §7 结账三型 → GOV.UK check answers 七条 → §11 SC 3.3.4 三选一（AA）→ §16 自检"),
    ("划线价 / 原价折扣 / 运费税费 / 总价披露 / 隐藏费用", "pricing-checkout.md §4 FTC 464 total price → §10 费用三级披露 → §17.2 validate_was_price → §18 取源限制"),
]


def clean(text: str) -> str:
    text = FENCE.sub(" ", text)
    text = LINK.sub(r"\1", text)
    text = EMPH.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slug(title: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", title).strip("-")
    return s.lower() or "section"


def load_aliases() -> list:
    """读 memory/aliases.json → [(规范词, [别名...])]，供树中展示与检索扩展。"""
    p = MEM / "aliases.json"
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []
    rows = []
    for g in data.get("groups", []):
        c, a = g.get("canonical"), g.get("aliases", [])
        if c:
            rows.append((c, a))
    return rows


def snapshot(text: str) -> str:
    m = re.search(r"快照\s*(\d{4}-\d{2}-\d{2})", text[:2000])
    if m:
        return m.group(1)
    m = re.search(r"(\d{4}-\d{2}-\d{2})\s*经?\s*GitHub\s*API", text[:2000])
    return m.group(1) if m else "—"


def mask_fences(text: str) -> str:
    """把 ``` 代码块里的内容抹成空格（保留换行与字符位置）。

    否则代码块里的 `## 标题` 会被当成真章节：例如变更日志模板里的
    `## [2.0.0] - 2026-11-01` 会变成一条假章节，污染索引与检索排序。
    抹成等长空格是为了让 match 的 start/end 仍能直接索引原文。
    """
    def repl(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    return FENCE.sub(repl, text)


def parse_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = path.stem
    for line in lines[:15]:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    sections = []
    # 标题只在代码块之外识别；正文仍从原文切，行号与内容都不受影响
    matches = list(H2.finditer(mask_fences(text)))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        # 若本节下面紧接子标题（body 只有空行），摘要要往下找：
        # 否则 §3 这类"只有子节、没有导语"的章节在索引里摘要为空，检索命中后片段也是空白。
        level = len(m.group(1))
        eff_end = end
        if not body.strip():
            for j in range(i + 1, len(matches)):
                if len(matches[j].group(1)) <= level:
                    eff_end = matches[j].start()
                    break
            else:
                eff_end = len(text)
        summary = ""
        for raw in text[start:eff_end].splitlines():
            s = raw.strip()
            if not s or s.startswith("|") or s.startswith("<!--") or s.startswith("#"):
                continue
            summary = clean(s)[:120]
            if summary:
                break
        line_no = text[: m.start()].count("\n") + 1
        sections.append({
            "id": slug(m.group(2)),
            "level": level,
            "title": clean(m.group(2)),
            "summary": summary,
            "line": line_no,
            "chars": len(body),
        })

    rel = path.relative_to(ROOT).as_posix()
    return {
        "path": rel,
        "title": clean(title),
        "snapshot": snapshot(text),
        "lines": len(lines),
        "chars": len(text),
        "sections": sections,
    }


def collect() -> list:
    files = []
    targets = [SKILL] + sorted(REF.glob("*.md")) + sorted(MEM.glob("*.md"))
    for p in targets:
        if p.exists() and p.name != "tree.md":
            files.append(parse_file(p))
    return files


def wiring_check(files: list) -> dict:
    """接线体检：SKILL.md 是否引用了每个资产；磁盘上是否有 SKILL.md 提到但不存在的文件。"""
    skill_text = SKILL.read_text(encoding="utf-8") if SKILL.exists() else ""
    referenced = set(re.findall(r"references/([\w\-.]+\.md)", skill_text))
    on_disk = {p.name for p in REF.glob("*.md")}
    return {
        "未接线": sorted(on_disk - referenced),      # 写了但没在 SKILL.md 里路由 → 等于没写
        "已失联": sorted(referenced - on_disk),      # SKILL.md 指向不存在的文件
    }


def build_tree(files: list, check: dict) -> str:
    today = time.strftime("%Y-%m-%d %H:%M")
    total_sections = sum(len(f["sections"]) for f in files)
    total_chars = sum(f["chars"] for f in files)

    out = [
        "# 记忆树 · Knowledge Tree",
        "",
        f"> 自动生成于 {today} ｜ {len(files)} 个文件 · {total_sections} 个章节 · {total_chars:,} 字符",
        "> 由 `scripts/mindmap.py` 重建，**不要手改**（手改会被下次覆盖；要改就改源文件或脚本）。",
        "",
        "## 怎么用（三条命令）",
        "",
        "```bash",
        "python scripts/dp_search.py \"缓动曲线\"      # 关键词检索：命中章节 + 行号 + 摘要",
        "python scripts/dp_search.py --topic          # 列出所有主题（章节标题一览）",
        "python scripts/mindmap.py                    # 资产变更后重建本树与 index.json",
        "```",
        "",
        "**检索纪律**：先用 `dp_search` 定位到「文件 §章节」，再只读那一段。不要整份读 references——十几份文件全读一遍会吃掉大量上下文，而命中往往只在一节。",
        "",
        "## 一、意图 → 位置（快捷路由）",
        "",
        "| 用户这么说 | 去哪儿 |",
        "|---|---|",
    ]
    for intent, where in INTENTS:
        out.append(f"| {intent} | {where} |")

    # 别名映射：检索层专用，只提升召回，不改上面的路由优先级
    alias_rows = load_aliases()
    if alias_rows:
        out += [
            "",
            "## 一·B、别名映射（检索层，不改路由优先级）",
            "",
            "> 用户在说法上不会统一：说「弹窗」还是 dialog、说「转圈」还是 loading。"
            "`memory/aliases.json` 把这些说法归到同一个规范词，`dp_search.py` 检索时以 **0.45 权重**追加召回——"
            "**只影响召回，不影响上表的意图路由顺序**。",
            "",
            "| 规范词 | 别名 / 俗称 / 中英对应 |",
            "|---|---|",
        ]
        for canonical, aliases in alias_rows:
            out.append(f"| **{canonical}** | {' · '.join(aliases)} |")
        out.append("")
        out.append("新增别名改 `memory/aliases.json`；`dp_search.py \"词\" --no-alias` 可关闭扩展做对比。")

    out += ["", "## 二、知识树（按文件）", ""]
    for f in files:
        out.append(f"### `{f['path']}` · {f['title']}")
        out.append(f"_{f['lines']} 行 · 快照 {f['snapshot']} · {len(f['sections'])} 节_")
        out.append("")
        for s in f["sections"]:
            indent = "  " * (s["level"] - 2)
            summary = f" — {s['summary']}" if s["summary"] else ""
            out.append(f"{indent}- **{s['title']}** `L{s['line']}`{summary}")
        out.append("")

    out += ["## 三、主题索引（章节标题 → 位置）", ""]
    idx = {}
    for f in files:
        for s in f["sections"]:
            if s["level"] == 2:
                idx.setdefault(s["title"], []).append(f"`{f['path']}` L{s['line']}")
    for title in sorted(idx):
        out.append(f"- **{title}** → {' · '.join(idx[title])}")

    out += ["", "## 四、接线体检（自我进化的自检项）", ""]
    if check["未接线"]:
        out.append("⚠️ **未接线**（在 references 里但 SKILL.md 没路由 → agent 不会在正确时机读到）：")
        for n in check["未接线"]:
            out.append(f"- `references/{n}`")
    else:
        out.append("✅ 所有 references 均已在 SKILL.md 接线。")
    if check["已失联"]:
        out.append("")
        out.append("❌ **已失联**（SKILL.md 指向但文件不存在）：")
        for n in check["已失联"]:
            out.append(f"- `references/{n}`")
    out += [
        "",
        "> 每次升级新增参考文件后，必须同步在 SKILL.md 资产表 + 意图路由里加一行，否则等于没写。",
        "",
    ]
    return "\n".join(out)


def main():
    files = collect()
    check = wiring_check(files)
    # 检索索引剔除变更日志：design-log.md 是流水账，关键词密度极高，
    # 会让「表单」「表格」这类查询的前 3 条全是日志而不是知识章节。
    # 树里仍保留它（人可读），只是不参与 dp_search 排序。
    # SKILL.md 常驻上下文（技能激活即全量可见），而它的「工作流」是 500+ 行的巨型章节，
    # 放进索引会吞掉任何多词查询（例：查「商标注册」时 §工作流 因正文词频高排第一，
    # 真正的 §17 反而被压到第二）。检索层的职责是定位 references/ 与 memory/ 里的知识，
    # 所以这两类不进索引——树里仍保留，方便人看。
    NOT_SEARCHABLE = {"memory/design-log.md", "SKILL.md"}
    searchable = [
        {**f, "sections": []} if f["path"] in NOT_SEARCHABLE else f for f in files
    ]
    index = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "files": searchable,
        "wiring": check,
    }
    MEM.mkdir(parents=True, exist_ok=True)
    (MEM / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    if "--check" in sys.argv:
        print(f"文件 {len(files)} · 章节 {sum(len(f['sections']) for f in files)}")
        print("未接线:", check["未接线"] or "无")
        print("已失联:", check["已失联"] or "无")
        return

    (MEM / "tree.md").write_text(build_tree(files, check), encoding="utf-8")
    print(f"[完成] {len(files)} 文件 / {sum(len(f['sections']) for f in files)} 章节")
    print("  memory/index.json")
    print("  memory/tree.md")
    if check["未接线"]:
        print("  ⚠️ 未接线:", ", ".join(check["未接线"]))


if __name__ == "__main__":
    main()
