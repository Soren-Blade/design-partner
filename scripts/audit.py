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
    python scripts/audit.py --json       # 机器可读（checks 数组 + summary）
    python scripts/audit.py --only A4,A5 # 只跑指定门禁（A1–A8）

退出码：0 = 无 FAIL；1 = 有 FAIL（WARN 不影响退出码）。
"""
from __future__ import annotations

import argparse
import ast
import fnmatch
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
quiet = False
_results = []


def line(text: str) -> None:
    if not quiet:
        print(text)


def check(name: str, passed: bool, detail: str = "", soft: bool = False,
          cid: str = "") -> bool:
    """cid：门禁编号（A1–A8），供 --json / --only 使用；旧检查留空。"""
    global ok_count
    if passed:
        ok_count += 1
        _results.append({"id": cid, "name": name, "status": "PASS", "detail": detail})
        if verbose and not quiet:
            print("  PASS  %s%s" % (name, (" — " + detail) if detail else ""))
    elif soft:
        warn.append((name, detail))
        _results.append({"id": cid, "name": name, "status": "WARN", "detail": detail})
        if not quiet:
            print("  WARN  %s — %s" % (name, detail))
    else:
        fail.append((name, detail))
        _results.append({"id": cid, "name": name, "status": "FAIL", "detail": detail})
        if not quiet:
            print("  FAIL  %s — %s" % (name, detail))
    return passed


def read(p: Path, newline: str = "") -> str:
    return io.open(p, encoding="utf-8", newline=newline).read()


# ── 1. 换行与编码 ────────────────────────────────────────────────────────────
def audit_newlines() -> None:
    print("\n[1] 换行与编码")
    targets = [SKILL, README, SITES, KMAP, ALIASES]
    targets += sorted(REFS.glob("*.md"))
    targets += sorted((ROOT / "scripts").glob("*.py"))
    targets = [p for p in targets if p.exists()]
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


# ── 2. 数字声明一致性 ────────────────────────────────────────────────────────
def audit_counts() -> None:
    print("\n[2] 路由覆盖与版本声明")
    skill = read(SKILL)
    refs = sorted(REFS.glob("*.md"))
    cited = set(re.findall(r"([a-z0-9\-]+\.md)", skill))
    missing = [p.name for p in refs if p.name not in cited]
    check("SKILL 路由表列全 %d 份参考" % len(refs), not missing, ",".join(missing[:6]))
    m = re.search(r"当前版本\s*v(\d+)\s*·\s*(\d{4}-\d{2}-\d{2})", skill)
    check("SKILL 首部有「当前版本 vNN · YYYY-MM-DD」", bool(m),
          "缺版本行" if not m else "v%s · %s" % m.groups())

    km = read(KMAP)
    m2 = re.search(r"## 能力自测（(\d+) 条", km)
    actual = len(re.findall(r"^- \[ \] ", km, re.M))
    check("知识地图自测标题 = 实测 %d" % actual, bool(m2) and int(m2.group(1)) == actual,
          "标题 %s" % (m2.group(1) if m2 else "缺"))
    branches = len(re.findall(r"^### 支线 ", km, re.M))
    check("知识地图支线 ≥ 30", branches >= 30, "实测 %d" % branches)


# ── 3. 资产覆盖关系 ──────────────────────────────────────────────────────────
def audit_coverage() -> None:
    print("\n[3] 资产覆盖关系")
    refs = {p.name for p in REFS.glob("*.md")}
    skill = read(SKILL)
    missing_in_skill = sorted(n for n in refs if n not in skill)
    check("每份参考都被 SKILL.md 引用", not missing_in_skill, ",".join(missing_in_skill[:6]))
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


# ── 7. 门禁与评估（A1–A8，2026-11-19 审计整改新增）─────────────────────────
# 原来的自检只证明「声明与实测一致」，证明不了「文档真的变好了」；这一节把
# 审计里点名的四类漏洞（章节号悬挂、生成物过期、画像空转、重复段落）固化，
# 并补上结构预算、别名卫生、派生索引、立场接线。规则宁严勿松：整改中途
# FAIL/WARN 是事实，不是脚本坏了。
CN_DIGITS = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
             "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
HEAD_RE = re.compile(r"^#{2,3}\s*§?\s*(\d+(?:\.\d+)*)", re.M)
CN_HEAD_RE = re.compile(r"^##\s*([一二三四五六七八九十]+)、", re.M)
SEC_RE = re.compile(r"§\s*(\d+(?:\.\d+)*)")
REF_PATH_RE = re.compile(r"references/([A-Za-z0-9\-]+)\.md")
MD_NAME_RE = re.compile(r"([A-Za-z][A-Za-z0-9\-]*)\.md")
LEGAL_RE = re.compile(r"(U\.S\.C\.|CFR|UStG|PAngV|BGB|EuGH|DSGVO|GDPR|CCPA|CPPA)\s*$")
SELF_WORDS = ("本资产", "本文件", "本份", "本页", "自身")
SKILL_BUDGET_LINES = 500
SKILL_BUDGET_CHARS = 30000


def _cn_num(s: str) -> int:
    if s == "十":
        return 10
    if "十" in s:
        a, b = s.split("十", 1)
        return CN_DIGITS.get(a, 1) * 10 + (CN_DIGITS.get(b, 0) if b else 0)
    return CN_DIGITS.get(s, 0)


def strip_fences(text: str) -> str:
    """屏蔽 ``` 代码块（保留行号），避免把示例里的 ## 标题当成真标题。"""
    out, fenced = [], False
    for ln in text.splitlines():
        if ln.startswith("```"):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else ln)
    return "\n".join(out)


def md_files() -> list[Path]:
    fs = [SKILL, README]
    fs += sorted(REFS.glob("*.md"))
    fs += sorted((ROOT / "memory").glob("*.md"))
    if (ROOT / "tests").exists():
        fs += sorted((ROOT / "tests").rglob("*.md"))
    return [p for p in fs if p.exists()]


def section_ids(p: Path) -> set[str]:
    """章节号集合：`## §1` / `## 1` / `### 2.1`，以及中文序号 `## 一、`。"""
    t = strip_fences(read(p))
    ids = set(HEAD_RE.findall(t))
    for m in CN_HEAD_RE.finditer(t):
        n = _cn_num(m.group(1))
        if n:
            ids.add(str(n))
    return ids


def _resolve_target(pre: str, cur: Path, refs: dict[str, Path],
                    heads: dict[str, set[str]]):
    """把 §N 归到同一行最近的前置文件；「本资产」优先于更早的文件名。"""
    last_file, last_pos = None, -1
    for m in REF_PATH_RE.finditer(pre):
        last_file, last_pos = m.group(1) + ".md", m.end()
    for m in MD_NAME_RE.finditer(pre):
        cand = m.group(1) + ".md"
        if cand in refs and m.end() > last_pos:
            last_file, last_pos = cand, m.end()
    self_pos = max([pre.rfind(w) for w in SELF_WORDS] + [-1])
    if self_pos > last_pos:
        return cur.name if cur.name in refs else None
    if last_file:
        return last_file
    m = re.search(r"`([a-z][a-z0-9\-]*)`\s*$", pre)
    if m and m.group(1) + ".md" in refs:
        return m.group(1) + ".md"
    m = re.search(r"([a-z][a-z0-9\-]{2,})\s+$", pre)
    if m and m.group(1) + ".md" in refs:
        return m.group(1) + ".md"
    if cur.name in refs and heads.get(cur.name):
        return cur.name
    return None


def audit_structure() -> None:
    line("\n  [A1] 结构预算（SKILL.md ≤500 行 / ≤30,000 字符）")
    skill = read(SKILL)
    n_lines = len(skill.splitlines())
    n_chars = len(skill)
    line("       实测 %d 行 / %d 字符" % (n_lines, n_chars))
    check("A1 SKILL.md 行数 ≤ %d" % SKILL_BUDGET_LINES, n_lines <= SKILL_BUDGET_LINES,
          "实测 %d 行" % n_lines, cid="A1")
    check("A1 SKILL.md 字符数 ≤ %d" % SKILL_BUDGET_CHARS, n_chars <= SKILL_BUDGET_CHARS,
          "实测 %d 字符" % n_chars, cid="A1")


def audit_section_refs() -> None:
    line("\n  [A2] 显式章节引用（`名字.md §N`，裸 §N 不猜）")
    refs = {p.name: p for p in sorted(REFS.glob("*.md"))}
    heads = {name: section_ids(p) for name, p in refs.items()}
    missing, weak, bare = [], [], 0
    pat = re.compile(r"(?:references/)?([a-z][a-z0-9\-]*\.md)\s*§\s*(\d+(?:\.\d+)*)")
    for p in md_files():
        for ln, raw in enumerate(strip_fences(read(p)).splitlines(), 1):
            for m in pat.finditer(raw):
                name, num = m.group(1), m.group(2)
                if name not in refs:
                    continue  # 外部文件/法条，不是本库资产
                if not heads[name]:
                    continue  # 目标没有数字标题，无法判定
                if num in heads[name]:
                    continue
                anc = ".".join(num.split(".")[:-1])
                if anc and anc in heads[name]:
                    weak.append("%s:%d → %s §%s（仅到 §%s）"
                                % (p.relative_to(ROOT), ln, name, num, anc))
                else:
                    missing.append("%s:%d → %s §%s"
                                   % (p.relative_to(ROOT), ln, name, num))
            bare += len(re.findall(r"(?<![\w.])§\s*\d", pat.sub("", raw)))
    detail = "；".join(missing[:20])
    if len(missing) > 20:
        detail += "；…（共 %d 条，此处仅列前 20）" % len(missing)
    check("A2 显式 §章节引用均可解析", not missing, detail,
          cid="A2")
    check("A2 精确到子节（祖先节存在即容忍）", not weak,
          ("%d 条只到祖先节：%s" % (len(weak), "；".join(weak[:6]))) if weak else "0",
          soft=True, cid="A2")
    if not quiet:
        print("  （裸 §N %d 处不参与判定；改为显式 `名字.md §N` 才检查）" % bare)


def audit_freshness() -> None:
    line("\n  [A3] 生成物新鲜度（README 与 SKILL / 生成器一致）")
    skill = read(SKILL)
    m = re.search(r"当前版本\s*v(\d+)\s*·\s*(\d{4}-\d{2}-\d{2})", skill)
    if not m:
        check("A3 SKILL.md 首部有「当前版本 vNN · YYYY-MM-DD」", False,
              "未找到版本行", cid="A3")
        return
    sv, sd = m.group(1), m.group(2)
    head = "\n".join(read(README).splitlines()[:40])
    rv = re.search(r"当前版本\s*v(\d+)", head)
    rd = re.search(r"生成于\s*(\d{4}-\d{2}-\d{2})", head)
    check("A3 README 版本 = SKILL v%s" % sv,
          bool(rv) and rv.group(1) == sv,
          ("README v%s" % rv.group(1)) if rv else "README 首部缺「当前版本 vNN」",
          cid="A3")
    check("A3 README 日期 = SKILL %s" % sd,
          bool(rd) and rd.group(1) == sd,
          ("README %s" % rd.group(1)) if rd else "README 首部缺「生成于 YYYY-MM-DD」",
          cid="A3")
    proc = subprocess.run([sys.executable, "-X", "utf8",
                           str(ROOT / "scripts" / "build_readme.py"), "--check"],
                          capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT))
    check("A3 build_readme.py --check 通过", proc.returncode == 0,
          (proc.stdout or proc.stderr).strip()[:300], cid="A3")


def audit_profile() -> None:
    line("\n  [A4] 画像非空（高信号 ≥10 条时 profile.md 必须有规则）")
    journal = ROOT / "memory" / "journal.jsonl"
    profile = ROOT / "memory" / "profile.md"
    if not journal.exists():
        check("A4 画像非空（信号不足时不触发）", True, "无 journal.jsonl，跳过", cid="A4")
        return
    signals = 0
    for raw in read(journal).splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except Exception:  # noqa: BLE001
            continue
        if str(rec.get("signal_type", "")) in ("explicit_preference", "correction"):
            signals += 1
    if signals < 10:
        check("A4 画像非空（信号不足时不触发）", True,
              "explicit_preference/correction 共 %d 条 < 10" % signals, cid="A4")
        return
    rules = 0
    if profile.exists():
        rules = len(re.findall(r"^\s*(?:[-*+]|\d+\.)\s+\S", read(profile), re.M))
    check("A4 高信号 %d 条时 profile.md 有规则" % signals, rules >= 1,
          "规则条目 %d" % rules, cid="A4")


def audit_alias_hygiene() -> None:
    line("\n  [A5] 别名卫生（≤12 词 / canonical 不进自身 / 全库唯一）")
    groups = json.loads(read(ALIASES))["groups"]
    too_big = [(len(g["aliases"]), g["canonical"]) for g in groups
               if len(g["aliases"]) > 12]
    self_canon = [g["canonical"] for g in groups
                  if g["canonical"].strip().lower()
                  in [w.strip().lower() for w in g["aliases"]]]
    owners, dup = {}, []
    for g in groups:
        for w in g["aliases"]:
            k = w.strip().lower()
            if k in owners:
                dup.append(k)
            owners[k] = g["canonical"]
    canon_as_alias = sorted({g["canonical"] for g in groups
                             if g["canonical"].strip().lower() in owners
                             and owners[g["canonical"].strip().lower()] != g["canonical"]})
    check("A5 每组别名 ≤ 12", not too_big,
          ",".join("%s(%d)" % (c, n) for n, c in sorted(too_big, reverse=True)[:8]),
          cid="A5")
    check("A5 canonical 不出现自身 aliases", not self_canon,
          ",".join(self_canon[:8]), cid="A5")
    check("A5 任意词全库唯一", not dup and not canon_as_alias,
          "重复词：%s；canonical 被占用：%s"
          % (",".join(sorted(set(dup))[:8]) or "无",
             ",".join(canon_as_alias[:8]) or "无"),
          cid="A5")


def _gitignore_covers(rel: str, name: str) -> bool:
    gi = ROOT / ".gitignore"
    if not gi.exists():
        return False
    for raw in read(gi).splitlines():
        pat = raw.strip()
        if not pat or pat.startswith("#"):
            continue
        if pat.startswith("/"):
            pat = pat[1:]
        d = pat.rstrip("/")
        if pat.endswith("/"):
            if rel == d or rel.startswith(d + "/"):
                return True
        elif fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(name, pat):
            return True
    return False


def audit_derived_index() -> None:
    line("\n  [A6] 派生索引未入库（tree.md / index.json 应本地生成）")
    leaked = [rel for rel in ("memory/tree.md", "memory/index.json")
              if (ROOT / rel).exists() and not _gitignore_covers(rel, (ROOT / rel).name)]
    check("A6 tree.md / index.json 为本地生成物", not leaked,
          ("未被 .gitignore 覆盖：%s（应为本地生成物，不应入库）" % ",".join(leaked))
          if leaked else "", soft=True, cid="A6")


def _paragraphs(text: str, min_chars: int = 300) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text)
            if len(re.sub(r"\s+", "", p)) >= min_chars]


def _shingles(p: str, n: int = 8) -> set[int]:
    s = re.sub(r"\s+", "", p)
    return {hash(s[i:i + n]) for i in range(len(s) - n + 1)}


def audit_duplicate_paragraphs() -> None:
    line("\n  [A7] 重复段落（≥300 字符、8-gram 相同）")
    items = []
    for p in sorted(REFS.glob("*.md")):
        for idx, para in enumerate(_paragraphs(read(p))):
            items.append((p.name, idx, para, _shingles(para)))
    index = {}
    for k, (_, _, _, sh) in enumerate(items):
        for h in sh:
            index.setdefault(h, []).append(k)
    shared = {}
    for h, ks in index.items():
        if 2 <= len(ks) <= 400:
            for a in range(len(ks)):
                for b in range(a + 1, len(ks)):
                    pa, pb = min(ks[a], ks[b]), max(ks[a], ks[b])
                    shared[(pa, pb)] = shared.get((pa, pb), 0) + 1
    dups = []
    for (a, b), cnt in shared.items():
        if items[a][0] == items[b][0]:
            continue
        small = min(len(items[a][3]), len(items[b][3]))
        ratio = cnt / small if small else 0
        if ratio >= 0.5:
            dups.append((ratio, items[a][0], items[b][0],
                         len(items[a][2]), len(items[b][2])))
    dups.sort(reverse=True)
    check("A7 references 之间无重复段落", not dups,
          "；".join("%s ↔ %s（相似度 %.2f，%d/%d 字符）"
                   % (a, b, r, la, lb) for r, a, b, la, lb in dups[:5]),
          soft=True, cid="A7")
    ss = [_shingles(p) for p in _paragraphs(read(SKILL))]
    rr = [_shingles(p) for p in _paragraphs(read(README))]
    cross = []
    for i, sa in enumerate(ss):
        for j, sb in enumerate(rr):
            small = min(len(sa), len(sb))
            if small and len(sa & sb) / small >= 0.5:
                cross.append((len(sa & sb) / small, i, j))
    cross.sort(reverse=True)
    check("A7 SKILL.md 与 README.md 之间无重复段落", not cross,
          "；".join("SKILL 段 %d ↔ README 段 %d（相似度 %.2f）" % (i, j, r)
                   for r, i, j in cross[:5]),
          cid="A7")


def audit_stance_wiring() -> None:
    line("\n  [A8] 判断层接线（五件套 / 互引 / 数值口径）")
    skill = read(SKILL)
    judge = ["taste-criteria.md", "comparison-protocol.md", "before-after.md",
             "numeric-truth.md", "user-modeling.md"]
    missing = [n for n in judge if n not in skill]
    check("A8 判断层五件套均被 SKILL.md 引用", not missing, ",".join(missing))

    texts = {p.name: read(p) for p in REFS.glob("*.md")}
    tri = ["taste-criteria.md", "comparison-protocol.md", "before-after.md"]
    weak = [a + "→" + b for a in tri for b in tri if a != b and b not in texts.get(a, "")]
    check("A8 品味 / 比较 / 改稿三文件互相引用", not weak, ",".join(weak))

    users = [n for n in ("comparison-protocol.md", "before-after.md", "taste-criteria.md")
             if "user-modeling.md" in texts.get(n, "")]
    check("A8 受众模型被判断层引用", len(users) >= 2, "仅 %s" % ("," .join(users) or "无"))

    cnt = sum(1 for n, t in texts.items() if n != "numeric-truth.md" and "numeric-truth.md" in t)
    check("A8 数值口径被 ≥5 份正文引用", cnt >= 5, "实测 %d 份" % cnt)


GATES = [
    ("A1", audit_structure),
    ("A2", audit_section_refs),
    ("A3", audit_freshness),
    ("A4", audit_profile),
    ("A5", audit_alias_hygiene),
    ("A6", audit_derived_index),
    ("A7", audit_duplicate_paragraphs),
    ("A8", audit_stance_wiring),
]


def main() -> int:
    global verbose, quiet
    ap = argparse.ArgumentParser(description="design-partner 常驻自检")
    ap.add_argument("--no-retrieval", action="store_true", help="跳过检索抽检")
    ap.add_argument("-v", "--verbose", action="store_true", help="打印每条通过项")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出全部结果")
    ap.add_argument("--only", default="", help="只跑指定门禁，如 A4,A5")
    args = ap.parse_args()
    verbose = args.verbose
    quiet = args.json
    only = [x.strip().upper() for x in args.only.split(",") if x.strip()]
    gate_names = dict(GATES)
    if only:
        bad = [x for x in only if x not in gate_names]
        if bad:
            print("未知检查项：%s（可选 %s）"
                  % (",".join(bad), ",".join(cid for cid, _ in GATES)),
                  file=sys.stderr)
            return 2
        real_stdout = sys.stdout
        if args.json:
            sys.stdout = io.StringIO()
        try:
            line("design-partner 自检 · %s（only %s）" % (ROOT, ",".join(only)))
            for cid, fn in GATES:
                if cid in only:
                    fn()
        finally:
            sys.stdout = real_stdout
    else:
        real_stdout = sys.stdout
        if args.json:
            sys.stdout = io.StringIO()
        try:
            line("design-partner 自检 · %s" % ROOT)
            audit_newlines()
            audit_counts()
            audit_coverage()
            audit_aliases()
            audit_parse()
            if not args.no_retrieval:
                audit_retrieval()
            line("\n[7] 门禁与评估（A1–A8）")
            for _, fn in GATES:
                fn()
        finally:
            sys.stdout = real_stdout

    if args.json:
        print(json.dumps({
            "root": str(ROOT),
            "only": only or None,
            "checks": _results,
            "summary": {"pass": ok_count, "warn": len(warn), "fail": len(fail)},
        }, ensure_ascii=False, indent=2))
    else:
        print("\n结果：PASS %d · WARN %d · FAIL %d" % (ok_count, len(warn), len(fail)))
        for name, detail in warn:
            print("  WARN  %s — %s" % (name, detail))
        for name, detail in fail:
            print("  FAIL  %s — %s" % (name, detail))
        if not fail:
            print("自检通过：统计口径、覆盖关系、别名健康、可解析性%s、8 项门禁全部通过。"
                  % ("、检索可达性" if not args.no_retrieval else ""))
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
