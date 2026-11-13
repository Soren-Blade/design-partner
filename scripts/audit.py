#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""audit.py —— design-partner 常驻自检（#37 维护轮新建）

为什么有这个脚本：此前每一轮升级的「统计一致性」靠临时脚本手写（.tmp_audit*.py），
用完即删，下一轮又从零开始；而 v40 暴露的三类问题恰恰都是**可以自动判定**的：
README 声明数与实测数漂移、别名组重复建组导致撞词、regression 在提交之后才失效。
本脚本把这些判定固化下来，成为每日升级协议的最后一关。

用法：
    python scripts/audit.py              # 全量（含检索抽检，约 20–40s）
    python scripts/audit.py --no-retrieval
    python scripts/audit.py -v           # 打印每条通过项

退出码：0 = 无 FAIL；1 = 有 FAIL（WARN 不影响退出码）。
"""
from __future__ import annotations

import argparse
import ast
import io
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
README = ROOT / "README.md"
SITES = ROOT / "Design-related websites.txt"
ALIASES = ROOT / "memory" / "aliases.json"
KMAP = ROOT / "references" / "knowledge-map.md"
REFS = ROOT / "references"

# 别名组粒度纪律：新建组 ≤12 词；历史组容忍到 16；>16 必须拆（#27 巨型组教训）
ALIAS_HARD_MAX = 16

# 检索抽检样本：(查询, 期望资产)。期望值是「这个查询最小够用的那一份」，
# 不要求排第一，但要求进前三——排第一常见是三万字的 knowledge-map 在当导航。
SAMPLE = [
    ("toast 停留时长 几秒", "feedback-states.md"),
    ("暗色模式 表面层级 三级", "dark-mode.md"),
    ("中文 行长 多少字", "chinese-design.md"),
    ("对比度 4.5 AA 大字 3:1", "accessibility.md"),
    ("空状态 文案 怎么写", "empty-states.md"),
    ("结账 复核页 Change 预填", "pricing-checkout.md"),
    ("月年切换 定价 折扣", "pricing-checkout.md"),
    ("缓动曲线 cubic-bezier 时长", "motion-system.md"),
    ("表单 标签 对齐 左对齐 顶对齐", "form-table.md"),
    ("图表 选型 九类关系", "dataviz.md"),
    ("行高 字号 比例 1.5", "typography-system.md"),
    ("图标 24dp 网格 对齐", "iconography.md"),
    ("信息架构 卡片分类", "navigation-ia.md"),
    ("自动续费 取消订阅 显著告知", "design-ethics-inclusion.md"),
    ("受控组件 非受控组件 切换", "component-api-design.md"),
    ("设计 token 命名 语义层", "design-tokens.md"),
    ("SUS 样本量 多少人才有效", "design-measurement-research.md"),
    ("RTL 镜像 阿语 布局", "i18n-localization.md"),
    ("骨架屏 加载 占位", "feedback-states.md"),
    ("三层阴影 高度 elevation", "shape-elevation.md"),
    ("拖拽 键盘 拖放 替代", "direct-manipulation.md"),
    ("流式输出 读屏 播报", "conversational-generative-ui.md"),
    ("模态 焦点陷阱 inert 返回", "overlays-modality.md"),
    ("首次启动 引导 要不要做", "onboarding-first-run.md"),
    ("海报 出血 安全区 mm", "editorial-layout.md"),
    ("品牌色 色阶 生成 对比度护栏", "multi-brand-theming.md"),
    ("设计评审 走查 议程 怎么开", "design-critique.md"),
    ("WCAG 2.2 新增 条款 清单", "accessibility.md"),
]

ok_count = 0
fail = []
warn = []
verbose = False


def line(text: str) -> None:
    print(text)


def check(name: str, passed: bool, detail: str = "", soft: bool = False) -> bool:
    global ok_count
    if passed:
        ok_count += 1
        if verbose:
            print("  PASS  %s%s" % (name, (" — " + detail) if detail else ""))
    elif soft:
        warn.append((name, detail))
        print("  WARN  %s — %s" % (name, detail))
    else:
        fail.append((name, detail))
        print("  FAIL  %s — %s" % (name, detail))
    return passed


def read(p: Path, newline: str = "") -> str:
    return io.open(p, encoding="utf-8", newline=newline).read()


# ── 1. 换行与编码 ────────────────────────────────────────────────────────────
def audit_newlines() -> None:
    print("\n[1] 换行与编码")
    targets = [SKILL, README, SITES, KMAP, ALIASES, ROOT / "memory" / "design-log.md"]
    targets += sorted(REFS.glob("*.md"))
    targets += sorted((ROOT / "scripts").glob("*.py"))
    bad_double, mixed, bad_utf8 = [], [], []
    for p in targets:
        try:
            raw = io.open(p, encoding="utf-8", newline="").read()
        except UnicodeDecodeError:
            bad_utf8.append(p.name)
            continue
        if "\r\r" in raw:
            bad_double.append(p.name)
        crlf, lone = raw.count("\r\n"), raw.count("\n") - raw.count("\r\n")
        if crlf and lone:
            mixed.append("%s(CRLF %d / LF %d)" % (p.name, crlf, lone))
    check("无双重换行 \\r\\r\\n", not bad_double, ",".join(bad_double))
    check("单文件内不混用换行", not mixed, ",".join(mixed[:4]))
    check("全部 UTF-8 可解码", not bad_utf8, ",".join(bad_utf8))
    # 本仓库的换行现状是「核心四件套 CRLF、多数参考资产 LF」，并非全仓统一 CRLF；
    # 因此只把「核心文件必须 CRLF」当硬规则，混用由上面的硬校验兜住。
    bad_core = [p.name for p in (SKILL, README, SITES, KMAP) if read(p).count("\r\n") == 0]
    check("核心四件套保持 CRLF（SKILL / README / 源清单 / 知识地图）",
          not bad_core, ",".join(bad_core))


# ── 2. 数字声明一致性 ────────────────────────────────────────────────────────
def audit_counts() -> None:
    print("\n[2] 数字声明一致性")
    skill = read(SKILL)
    refs = sorted(REFS.glob("*.md"))
    total_chars = sum(len(read(p)) for p in refs)

    m = re.search(r"资产已 (\d+) 份参考、约 (\d+) 万字符", skill)
    check("SKILL.md 有「资产已 N 份参考」声明", bool(m))
    if m:
        check("参考份数声明 = 实测 %d" % len(refs), int(m.group(1)) == len(refs),
              "声明 %s" % m.group(1))
        claimed = int(m.group(2)) * 10000
        check("字符量声明 ≈ 实测 %.2f 万" % (total_chars / 10000.0),
              abs(claimed - total_chars) <= 20000,
              "声明 %d / 实测 %d" % (claimed, total_chars))

    rmap = re.findall(r"version-v(\d+)", read(README))
    vskill = re.search(r"当前版本 v(\d+)", skill)
    if rmap and vskill:
        check("README 版本徽标 = SKILL.md 版本", rmap[0] == vskill.group(1),
              "README v%s / SKILL v%s" % (rmap[0], vskill.group(1)))
    fam = re.findall(r"reference_files-(\d+)", read(README))
    if fam:
        check("README 参考份数徽标 = 实测 %d" % len(refs), int(fam[0]) == len(refs),
              "徽标 %s" % fam[0])

    # 第 0 步份数已校验；再看自检条数与路由条数（README 声明 vs 实测）
    # 注意：必须限制在对应章节内，否则会把协议步骤、其它编号列表一起算进来
    def section(text: str, start: str, end: str) -> str:
        i = text.find(start)
        j = text.find(end, i + 1)
        return text[i:j] if i >= 0 and j > i else ""

    step6 = section(skill, "### 第 6 步", "## 自我成长机制")
    step1 = section(skill, "### 第 1 步", "### 第 2 步")
    checks = len(re.findall(r"^\d+\. ", step6, re.M))
    # 路由数 = 意图路由表的数据行数（表头 `| 意图 |` 不计；少数行只写「走哪些步」不点名文件）
    routing = len([ln for ln in step1.split("\n")
                   if ln.startswith("| ") and not ln.startswith("| 意图 |")])
    rc = re.findall(r"(\d+) 项自检", read(README))
    rr = re.findall(r"(\d+) 类意图路由", read(README))
    if rc:
        check("README 自检项数 = 实测 %d" % checks, int(rc[0]) == checks, "README %s" % rc[0])
    if rr:
        check("README 路由数 = 实测 %d" % routing, int(rr[0]) == routing, "README %s" % rr[0])

    # 知识地图：标题里的条数 / 支线数
    km = read(KMAP)
    m2 = re.search(r"## 能力自测（(\d+) 条", km)
    actual = len(re.findall(r"^- \[ \] ", km, re.M))
    check("知识地图自测标题 = 实测 %d" % actual, bool(m2) and int(m2.group(1)) == actual,
          "标题 %s" % (m2.group(1) if m2 else "缺"))
    branches = len(re.findall(r"^### 支线 ", km, re.M))
    check("知识地图支线 ≥ 30", branches >= 30, "实测 %d" % branches, soft=branches >= 30)


# ── 3. 资产覆盖关系 ──────────────────────────────────────────────────────────
def audit_coverage() -> None:
    print("\n[3] 资产覆盖关系")
    refs = {p.name for p in REFS.glob("*.md")}
    skill = read(SKILL)
    build = (ROOT / "scripts" / "build_readme.py")
    src = read(build)
    assets = set(re.findall(r'"([a-z0-9\-]+\.md)"', src))
    missing_in_skill = sorted(n for n in refs if n not in skill)
    check("每份参考都被 SKILL.md 引用", not missing_in_skill, ",".join(missing_in_skill[:6]))
    missing_in_build = sorted(n for n in refs if n not in assets)
    check("每份参考都在 build_readme ASSETS 里", not missing_in_build,
          ",".join(missing_in_build[:6]))
    ghost = sorted(n for n in set(re.findall(r"references/([a-z0-9\-]+\.md)", skill))
                   if n not in refs)
    check("SKILL.md 没引用不存在的文件", not ghost, ",".join(ghost[:6]))


# ── 4. 别名层健康 ────────────────────────────────────────────────────────────
def audit_aliases() -> None:
    print("\n[4] 别名层健康")
    data = json.loads(read(ALIASES))
    groups = data["groups"]
    words = [w.strip().lower() for g in groups for w in g["aliases"]]
    dup = sorted({w for w in words if words.count(w) > 1})
    canon = [g["canonical"] for g in groups]
    dupc = sorted({c for c in canon if canon.count(c) > 1})
    empty = [g["canonical"] for g in groups if not g["aliases"]]
    pairs = sorted(((len(g["aliases"]), g["canonical"]) for g in groups), reverse=True)
    big = [(n, c) for n, c in pairs if n > ALIAS_HARD_MAX]
    over12 = [(n, c) for n, c in pairs if 12 < n <= ALIAS_HARD_MAX]

    check("别名组数 ≥ 200", len(groups) >= 200, "实测 %d 组 / %d 词" % (len(groups), len(words)))
    check("无跨组撞词", not dup, "%d 个：%s" % (len(dup), ",".join(dup[:6])))
    check("无重名 canonical 组", not dupc, ",".join(dupc[:6]))
    check("无空组", not empty, ",".join(empty[:6]))
    check("无 >%d 词的组" % ALIAS_HARD_MAX, not big,
          ",".join("%s(%d)" % (c, n) for n, c in big))
    check("13–%d 词容忍带" % ALIAS_HARD_MAX, not over12,
          "%d 组：%s" % (len(over12), ",".join("%s(%d)" % (c, n) for n, c in over12[:6])),
          soft=True)
    check("_weight 保持 0.45", float(data.get("_weight", 0)) == 0.45,
          str(data.get("_weight")))


# ── 5. 脚本与 JSON 可解析 ────────────────────────────────────────────────────
def audit_parse() -> None:
    print("\n[5] 脚本与 JSON 可解析")
    bad = []
    for p in sorted((ROOT / "scripts").glob("*.py")):
        try:
            ast.parse(read(p))
        except SyntaxError as e:
            bad.append("%s:%s" % (p.name, e.lineno))
    check("scripts/*.py 全部 ast.parse", not bad, ",".join(bad))
    jbad = []
    for p in sorted((ROOT / "memory").glob("*.json")):
        try:
            json.loads(read(p))
        except Exception as e:  # noqa: BLE001
            jbad.append("%s:%s" % (p.name, type(e).__name__))
    check("memory/*.json 全部可解析", not jbad, ",".join(jbad))


# ── 6. 检索抽检 ──────────────────────────────────────────────────────────────
def audit_retrieval() -> None:
    print("\n[6] 检索抽检（%d 条）" % len(SAMPLE))
    search = ROOT / "scripts" / "dp_search.py"
    top1 = top3 = 0
    misses = []
    for q, want in SAMPLE:
        out = subprocess.run([sys.executable, "-X", "utf8", str(search), q, "-n", "3"],
                             capture_output=True, text=True, encoding="utf-8",
                             cwd=str(ROOT)).stdout
        hits = re.findall(r"\]\s+references/([a-z0-9\-]+\.md)", out)
        if hits and hits[0] == want:
            top1 += 1
        if want in hits:
            top3 += 1
        else:
            misses.append("%s → %s" % (q, hits[:3] or "无命中"))
    n = len(SAMPLE)
    check("检索 top3 ≥ 85%%（实测 %d/%d）" % (top3, n), top3 >= n * 0.85,
          "; ".join(misses[:3]))
    check("检索 top1 ≥ 60%%（实测 %d/%d）" % (top1, n), top1 >= n * 0.6,
          "参考值，不是硬指标", soft=True)


def main() -> int:
    global verbose
    ap = argparse.ArgumentParser(description="design-partner 常驻自检")
    ap.add_argument("--no-retrieval", action="store_true", help="跳过检索抽检")
    ap.add_argument("-v", "--verbose", action="store_true", help="打印每条通过项")
    args = ap.parse_args()
    verbose = args.verbose

    print("design-partner 自检 · %s" % ROOT)
    audit_newlines()
    audit_counts()
    audit_coverage()
    audit_aliases()
    audit_parse()
    if not args.no_retrieval:
        audit_retrieval()

    print("\n结果：PASS %d · WARN %d · FAIL %d" % (ok_count, len(warn), len(fail)))
    for name, detail in warn:
        print("  WARN  %s — %s" % (name, detail))
    for name, detail in fail:
        print("  FAIL  %s — %s" % (name, detail))
    if not fail:
        print("自检通过：统计口径、覆盖关系、别名健康、可解析性%s全部一致。"
              % ("、检索可达性" if not args.no_retrieval else ""))
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
