# -*- coding: utf-8 -*-
"""README 单源生成器。

README.md 不再手写成第二本 SKILL：本脚本从
  - CHANGELOG.md 的「当前版本 vNN」
  - references/*.md 的真实标题 / 行数 / 章节数
  - memory/journal.jsonl 的真实条数
填充 `scripts/readme_template.md`，产出 README.md。

用法:
  python scripts/build_readme.py          # 生成
  python scripts/build_readme.py --check  # 只检查是否过期（过期 exit 1）
"""
import io
import json
import re
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "scripts" / "readme_template.md"
README = ROOT / "README.md"

GROUPS = [
    ("判断与品味", ["taste-criteria", "comparison-protocol", "before-after", "user-modeling",
                    "numeric-truth", "design-critique"]),
    ("视觉基础", ["typography-system", "color-science", "visual-hierarchy-gestalt", "shape-elevation",
                  "iconography", "visual-style-taxonomy", "chinese-design", "design-tokens",
                  "brand-identity"]),
    ("版式与系统", ["editorial-layout", "responsive-layout", "dark-mode", "motion-system", "dataviz",
                    "performance-design", "multi-brand-theming"]),
    ("界面与交互", ["component-api-design", "form-table", "feedback-states", "empty-states",
                    "navigation-ia", "overlays-modality", "content-findability", "direct-manipulation",
                    "keyboard-shortcuts-command-palette", "onboarding-first-run", "sound-haptics-feedback",
                    "conversational-generative-ui", "realtime-collaboration", "video-player-captions"]),
    ("领域与商业", ["presentation-design", "email-design", "pricing-checkout", "pricing-localization",
                    "quote-invoice-documents", "auth-account-ux", "notifications-messaging",
                    "file-upload-media-input", "handoff-collaboration", "design-measurement-research",
                    "ux-writing"]),
    ("合规与工具链", ["accessibility", "i18n-localization", "design-ethics-inclusion",
                      "ai-design-toolchain", "design-system-docs", "component-libraries"]),
    ("索引与资源", ["knowledge-map", "patterns", "portfolios", "resources", "tools", "inspiration",
                    "design-md-format"]),
]


def version() -> str:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"当前版本\s*(v\d+)", skill)
    if m:
        return m.group(1)
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    m = re.search(r"当前版本\s*(v\d+)", text) or re.search(r"v(\d+)", text)
    return m.group(1) if m else "v0"


def refs() -> list:
    out = []
    for p in sorted((ROOT / "references").glob("*.md")):
        text = p.read_text(encoding="utf-8")
        first = next((l for l in text.splitlines() if l.startswith("# ")), "")
        title = re.sub(r"^#\s*", "", first).strip()
        out.append({
            "stem": p.stem,
            "title": title,
            "lines": text.count("\n") + 1,
            "sections": sum(1 for l in text.splitlines() if l.startswith("## ")),
            "chars": len(text),
        })
    return out


def asset_table(items: list) -> str:
    known = {s for _, stems in GROUPS for s in stems}
    grouped = []
    for name, stems in GROUPS:
        rows = [i for s in stems for i in items if i["stem"] == s]
        if rows:
            grouped.append((name, rows))
    rest = [i for i in items if i["stem"] not in known]
    if rest:
        grouped.append(("未归组（请补 GROUPS）", rest))

    lines = ["| 组 | 资产 | 行 | 节 |", "|---|---|---:|---:|"]
    for name, rows in grouped:
        for r in rows:
            title = r["title"][:70].replace("|", "／")
            lines.append(f"| {name} | [`{r['stem']}.md`](references/{r['stem']}.md) · {title} "
                         f"| {r['lines']} | {r['sections']} |")
    return "\n".join(lines)


def memory_stats() -> dict:
    rows = real = 0
    path = ROOT / "memory" / "journal.jsonl"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            rows += 1
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("user_quote") or (rec.get("signal_type") not in (None, "none")):
                real += 1
    profile = ROOT / "memory" / "profile.md"
    state = "尚未建立"
    if profile.exists():
        text = profile.read_text(encoding="utf-8")
        state = f"{text.count(chr(10)) + 1} 行"
    return {"rows": rows, "real": real, "profile": state}


def render() -> str:
    items = refs()
    stats = memory_stats()
    tpl = TEMPLATE.read_text(encoding="utf-8")
    return (tpl
            .replace("{{VERSION}}", version())
            .replace("{{DATE}}", time.strftime("%Y-%m-%d"))
            .replace("{{REF_COUNT}}", str(len(items)))
            .replace("{{ASSET_TABLE}}", asset_table(items))
            .replace("{{JOURNAL_ROWS}}", str(stats["rows"]))
            .replace("{{JOURNAL_REAL}}", str(stats["real"]))
            .replace("{{PROFILE_STATE}}", stats["profile"]))


def main() -> int:
    text = render()
    old = README.read_text(encoding="utf-8") if README.exists() else ""
    if "--check" in sys.argv:
        if old != text:
            print("[过期] README.md 与源文件不一致，运行 python scripts/build_readme.py")
            return 1
        print("[新鲜] README.md 与源文件一致")
        return 0
    README.write_text(text, encoding="utf-8", newline="\n")
    print(f"[完成] README.md {len(text):,} 字符 / {text.count(chr(10)) + 1} 行 / {len(text.encode()):,} 字节")
    return 0


if __name__ == "__main__":
    sys.exit(main())
