#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
design-partner 记忆树生成器

扫描 SKILL.md / references/*.md / memory/*.md，产出两样东西：
  1) memory/index.json —— 机器索引（文件 → 章节 → 摘要 + 行号），供 dp_search.py 检索
  2) memory/tree.md     —— 人/agent 可读的知识树 + 主题索引 + 接线体检（路由见 SKILL.md §4）

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
# v52：意图路由只在 SKILL.md 第 4 节维护；本脚本不再硬编码意图表，避免两处漂移。


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
        "## 一、意图 → 位置（唯一路由源在 SKILL.md 第 4 节）",
        "",
        "> 路由只有一份真相：`SKILL.md` 第 4 节「执行：按需读 1–3 份资产」。",
        "> 本树不再复制路由表，避免两处漂移；要加路由，改 SKILL.md。",
        "",
    ]

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
    # 检索索引只剔除历史日志：design-log 归档是流水账，关键词密度高，
    # 会让「表单」「表格」这类查询的前 3 条全是日志而不是知识章节。
    # SKILL.md 现在是 277 行的判断流程 + 路由，必须进索引（v52 修正：
    # 旧版把 SKILL 整份排除，导致「检索不到技能本身」）。
    NOT_SEARCHABLE = {"memory/design-log.md", "memory/archive/design-log-v51.md"}
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
