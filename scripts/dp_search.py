#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
design-partner 快捷检索（记忆树的查询入口）

先用一句话定位到「文件 §章节」，再只读那一段——避免把 11 份参考整份塞进上下文。

用法:
    python scripts/dp_search.py "缓动曲线"            # 检索（默认前 8 条）
    python scripts/dp_search.py "抽屉 时长" -n 5       # 多关键词（空格分隔，命中任一即计分）
    python scripts/dp_search.py "token" --file tokens # 限定文件（路径模糊匹配）
    python scripts/dp_search.py --topic              # 主题总览：所有二级标题
    python scripts/dp_search.py "动效" --json         # 机器可读输出
    python scripts/dp_search.py --rebuild            # 先重建索引再检索

打分: 标题命中 ×10 · 摘要命中 ×4 · 正文出现次数 ×1（同一词只算一次标题/摘要）
"""
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
MEM = ROOT / "memory"
INDEX = MEM / "index.json"
FENCE = re.compile(r"```.*?```", re.S)


def terms_of(query: str) -> list:
    """英文按词切；中文补二元组（中文无空格，整串匹配会漏）。"""
    q = query.strip()
    out = set()
    for w in re.findall(r"[A-Za-z][A-Za-z0-9+#.\-]*", q):
        if len(w) >= 2:
            out.add(w.lower())
    for run in re.findall(r"[\u4e00-\u9fff]+", q):
        out.add(run)
        if len(run) > 2:
            for i in range(len(run) - 1):
                out.add(run[i:i + 2])
    return sorted(out, key=len, reverse=True)


def need_rebuild() -> bool:
    if not INDEX.exists():
        return True
    idx_mtime = INDEX.stat().st_mtime
    newest = max(
        [p.stat().st_mtime for p in (ROOT / "references").glob("*.md")]
        + [p.stat().st_mtime for p in (ROOT / "memory").glob("*.md") if p.name != "tree.md"]
        + [(ROOT / "SKILL.md").stat().st_mtime]
    )
    return newest > idx_mtime


def rebuild():
    subprocess.run([sys.executable, str(ROOT / "scripts" / "mindmap.py")], check=True)


def load_index():
    if need_rebuild():
        rebuild()
    return json.loads(INDEX.read_text(encoding="utf-8"))


def section_body(text: str, start_line: int, end_line: int) -> str:
    lines = text.splitlines()
    return "\n".join(lines[start_line - 1: end_line - 1])


def snippet(body: str, terms: list, width: int = 46) -> str:
    flat = re.sub(r"\s+", " ", FENCE.sub(" ", body))
    low = flat.lower()
    pos = -1
    for t in terms:
        p = low.find(t.lower())
        if p >= 0 and (pos < 0 or p < pos):
            pos = p
    if pos < 0:
        return flat[: width * 2].strip()
    a = max(0, pos - width)
    b = min(len(flat), pos + width)
    return ("…" if a else "") + flat[a:b].strip() + ("…" if b < len(flat) else "")


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return

    if "--rebuild" in argv:
        rebuild()
        argv = [a for a in argv if a != "--rebuild"]

    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    top_n = 8
    if "-n" in argv:
        i = argv.index("-n")
        top_n = int(argv[i + 1])
        del argv[i:i + 2]
    only = None
    if "--file" in argv:
        i = argv.index("--file")
        only = argv[i + 1].lower()
        del argv[i:i + 2]

    index = load_index()

    if "--topic" in argv:
        for f in index["files"]:
            print(f"\n{f['path']}  ·  {f['title']}  ({f['lines']} 行, 快照 {f['snapshot']})")
            for s in f["sections"]:
                if s["level"] == 2:
                    print(f"  L{s['line']:<5} {s['title']}  —  {s['summary'][:70]}")
        return

    query = " ".join(a for a in argv if not a.startswith("-")).strip()
    if not query:
        print(__doc__)
        return
    terms = terms_of(query)

    cache, hits = {}, []
    for f in index["files"]:
        if only and only not in f["path"].lower():
            continue
        secs = f["sections"]
        text = None
        for i, s in enumerate(secs):
            end = secs[i + 1]["line"] if i + 1 < len(secs) else f["lines"] + 1
            if text is None:
                p = ROOT / f["path"]
                text = p.read_text(encoding="utf-8") if p.exists() else ""
            body = section_body(text, s["line"] + 1, end)  # 跳过标题行本身
            low_title = s["title"].lower()
            low_sum = s["summary"].lower()
            low_body = body.lower()
            score = 0
            for t in terms:
                tl = t.lower()
                if tl in low_title:
                    score += 10
                if tl in low_sum:
                    score += 4
                c = low_body.count(tl)
                if c:
                    score += min(c, 8)
            if score:
                hits.append({
                    "file": f["path"], "title": f["title"], "section": s["title"],
                    "line": s["line"], "score": score, "snippet": snippet(body, terms),
                })

    hits.sort(key=lambda h: -h["score"])
    hits = hits[:top_n]

    if as_json:
        print(json.dumps({"query": query, "terms": terms, "hits": hits},
                         ensure_ascii=False, indent=1))
        return

    if not hits:
        print(f"未命中「{query}」。试试更短的关键词，或先 --topic 看全部主题。")
        return

    print(f"查询「{query}」 · 拆词 {len(terms)} 个 · 命中 {len(hits)} 条\n")
    for h in hits:
        print(f"[{h['score']:>3}] {h['file']}  §{h['section']}  (L{h['line']})")
        print(f"      {h['snippet']}")
        print()


if __name__ == "__main__":
    main()
