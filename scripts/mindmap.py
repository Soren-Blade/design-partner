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
    ("找工具 / 资产", "tools.md（工具）· resources.md（图标/字体/3D）· component-libraries.md（代码）"),
    ("想提升自己 / 学习路径", "knowledge-map.md L0→L4 + 20 条自测"),
    ("不确定知识在哪", "python scripts/dp_search.py \"关键词\""),
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


def snapshot(text: str) -> str:
    m = re.search(r"快照\s*(\d{4}-\d{2}-\d{2})", text[:2000])
    if m:
        return m.group(1)
    m = re.search(r"(\d{4}-\d{2}-\d{2})\s*经?\s*GitHub\s*API", text[:2000])
    return m.group(1) if m else "—"


def parse_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = path.stem
    for line in lines[:15]:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    sections = []
    matches = list(H2.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        summary = ""
        for raw in body.splitlines():
            s = raw.strip()
            if not s or s.startswith("|") or s.startswith("<!--"):
                continue
            summary = clean(s)[:120]
            if summary:
                break
        line_no = text[: m.start()].count("\n") + 1
        sections.append({
            "id": slug(m.group(2)),
            "level": len(m.group(1)),
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
    NOT_SEARCHABLE = {"memory/design-log.md"}
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
