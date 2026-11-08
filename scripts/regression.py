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

# 新主题门槛：主题词 + 通用跨域词组合，答案应落在 shape-elevation.md 前 3。
NEW_QUERIES = [
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
]

# 照 #26 P1 判例：「风格 对比度 验收」判为泛化对比度查询的正确路由边界，不凑 11/11。
# 这条 5 个词里 4 个是对比度专属词，正确答案归 accessibility.md / color-science.md 系，
# 不是字体文档；要求 typography-system.md 进 top3 属于测试集标签错误。
BOUNDARY = {
    # #27 判例样本，本轮继续作为历史路由边界校验（strict 比对 top3 与 HEAD 一致）。
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
]

EXPECT_FILE = "shape-elevation.md"
NEW_ASSETS = {EXPECT_FILE}

# 登记演进：新增权威资产凭「原词相关性」进入 top3，属升级而非退化。
# 但必须三条硬校验全过才放行（否则仍判 DIFF），见 check_evolution()。
EXPECTED_EVOLUTION = {
    # #27 的「字体 行高 中文排版」演进已被 HEAD 吸收，本轮正式归档为普通历史查询：
    # HEAD 基线本身已含 typography-system.md，NOW 与 HEAD 应逐字一致。
    "玻璃拟态 对比度 可访问性":
        "#28 登记演进：shape-elevation.md §17「玻璃拟态的合成开销与降级顺序」凭原词标题命中上位，"
        "属新权威资产在跨域查询里可见（#26 P1 曾专门修这条的可发现性），非别名污染；"
        "HEAD top1 visual-style-taxonomy.md 不变、HEAD top3 三个文件全在 NOW top5、"
        "--no-alias 下新资产仍排 #2。三条硬校验见 check_evolution()。",
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
