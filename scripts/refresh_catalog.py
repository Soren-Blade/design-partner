#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
design-partner 知识库自动刷新脚本（自我进化机制）
- 重新抓取 designeer.xyz 目录 API（4 个集合，游标翻页）
- 重建 references/*.md（保留 memory/ 记忆）
- 与另一份安装副本双向同步（master <-> global），memory 按行合并
- 输出变更摘要（各集合条数、新增、移除）

用法: python refresh_catalog.py [--dry-run]
"""
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from collections import OrderedDict
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL_ROOT = Path(__file__).resolve().parent.parent          # design-partner/
REF_DIR = SKILL_ROOT / "references"
MEM_DIR = SKILL_ROOT / "memory"
API = "https://designeer.xyz/api/catalog"
COLLECTIONS = ["inspiration", "resources", "tools", "portfolios"]
PRICING_CN = {"free": "免费", "freemium": "免费+付费", "paid": "付费"}
# 另一份副本：脚本在哪个安装里运行，就同步到另一个
SIBLINGS = [
    Path(r"D:\My Skills\design-partner"),
    Path.home() / ".agents" / "skills" / "design-partner",
]

HEADER = {
    "inspiration": "# 灵感与阅读 — Inspiration\n\n> 蒸馏自 designeer.xyz/inspiration（{n} 条，人工策展，快照 {date}）。画廊用于视觉调研与风格定位；阅读材料用于深化设计判断力。\n\n## 用法\n按需求关键词定位：做 **Web/UI 视觉调研** 找 Galleries 里对应领域的站点；想 **系统提升审美与方法论** 读 Reading 里的小节。\n",
    "resources": "# 设计资源 — Resources\n\n> 蒸馏自 designeer.xyz/resources（{n} 条，人工策展，快照 {date}）。组件库、图标、动效/3D 资产、字体与配色，全部面向数字产品界面。\n\n## 用法\n- **Components**：找可复用 UI 组件库与设计系统参考\n- **Icons**：图标库\n- **Motion & 3D**：动效与三维资产\n- **Type & Colour**：字体排印与配色工具\n\n标注（免费）/（免费+付费）/（付费）为官方定价信息。\n",
    "tools": "# 制作工具 — Tools\n\n> 蒸馏自 designeer.xyz/tools（{n} 条，人工策展，快照 {date}）。开发、AI、设计画布、截取媒体、生产力工具。\n\n## 用法\n- **Development**：前端/开发工具\n- **AI & Agents**：AI 辅助设计与生成\n- **Design & Canvas**：设计画布类工具\n- **Capture & Media**：截图、录屏、媒体处理\n- **Productivity & Desktop**：效率与桌面工具\n",
    "portfolios": "# 作品集 — Portfolios\n\n> 蒸馏自 designeer.xyz/portfolios（{n} 条，人工策展，快照 {date}）。设计工程师、设计师、开发者、创作者与工作室的个人站点，代表当前 Web 界面 craft 的一线水准。\n\n## 用法\n这是**审美校准**素材：当 agent 需要判断「什么是好的界面」时，参考这些一线从业者的作品构成方式；也用于给用户推荐可对标的作品集风格。\n",
}


def fetch_json(url):
    """urllib 优先，SSL 被代理干扰时回退 curl。"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        return json.load(urllib.request.urlopen(req, timeout=60))
    except Exception:
        for _ in range(3):
            r = subprocess.run(
                ["curl", "-sL", "--max-time", "90", url],
                capture_output=True, text=True, encoding="utf-8",
            )
            try:
                return json.loads(r.stdout)
            except Exception:
                time.sleep(1.5)
        raise RuntimeError("fetch failed: " + url)


def fetch_collection(name):
    items, cursor, page = [], None, 0
    while True:
        url = f"{API}?collection={name}"
        if cursor:
            url += "&cursor=" + urllib.parse.quote(cursor)
        d = fetch_json(url)
        items += d.get("items", [])
        cursor = d.get("nextCursor")
        page += 1
        if not cursor or page > 30:
            break
        time.sleep(0.4)
    return items


def render_md(coll, items, date_str):
    header = HEADER[coll].format(n=len(items), date=date_str)
    groups = OrderedDict()
    for it in items:
        cat = (it.get("category") or {}).get("name", "Other")
        groups.setdefault(cat, []).append(it)
    lines = [header, ""]
    for cat, its in groups.items():
        lines.append(f"## {cat} ({len(its)})\n")
        for it in its:
            price = PRICING_CN.get(it.get("pricing"), "")
            tag = f"（{price}）" if price else ""
            lines.append(f"- **[{it['name']}]({it['url']})**{tag} — {it['tagline'].strip()}")
        lines.append("")
    return "\n".join(lines)


def names_from_md(path):
    """从现有 md 提取条目名集合，用于变更统计。"""
    if not path.exists():
        return set()
    import re
    return set(re.findall(r"^- \*\*\[(.+?)\]", path.read_text(encoding="utf-8"), re.M))


def merge_memory(other: Path):
    """append-only 日志按行并集合并，两个方向都写。"""
    changed = False
    for a, b in [(MEM_DIR, other / "memory"), (other / "memory", MEM_DIR)]:
        if not b.exists():
            continue
        for f in b.glob("*.md"):
            if f.name == "design-log.md":
                continue  # 日志文件单独处理
            target = a / f.name
            src_lines = f.read_text(encoding="utf-8").splitlines()
            if not target.exists():
                a.mkdir(parents=True, exist_ok=True)
                target.write_text("\n".join(src_lines) + "\n", encoding="utf-8")
                changed = True
                continue
            existing = target.read_text(encoding="utf-8").splitlines()
            add = [l for l in src_lines if l.strip() and l not in existing]
            if add:
                target.write_text("\n".join(existing + add) + "\n", encoding="utf-8")
                changed = True
    # design-log.md：按日期小节合并
    for side_a, side_b in [(MEM_DIR, other / "memory"), (other / "memory", MEM_DIR)]:
        fa, fb = side_a / "design-log.md", side_b / "design-log.md"
        if not (fa.exists() and fb.exists()):
            continue
        la = fa.read_text(encoding="utf-8").splitlines()
        lb = fb.read_text(encoding="utf-8").splitlines()
        add = [l for l in lb if l.strip() and l not in la]
        if add:
            fa.write_text("\n".join(la + add) + "\n", encoding="utf-8")


def sync_sibling(other: Path, summary):
    if other.resolve() == SKILL_ROOT or not (other / "SKILL.md").exists():
        return
    import shutil
    for sub in ["references", "scripts"]:
        src, dst = SKILL_ROOT / sub, other / sub
        if src.exists():
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst)
    shutil.copy2(SKILL_ROOT / "SKILL.md", other / "SKILL.md")
    merge_memory(other)
    summary.append(f"已同步副本: {other}")


def main():
    dry = "--dry-run" in sys.argv
    date_str = time.strftime("%Y-%m-%d")
    summary, report = [], []

    for coll in COLLECTIONS:
        try:
            items = fetch_collection(coll)
        except Exception as e:
            report.append(f"[{coll}] 抓取失败: {e}")
            continue
        target = REF_DIR / f"{coll}.md"
        old = names_from_md(target)
        new = {it["name"] for it in items}
        added, removed = new - old, old - new
        text = render_md(coll, items, date_str)
        if not dry:
            REF_DIR.mkdir(exist_ok=True)
            target.write_text(text, encoding="utf-8")
        report.append(
            f"[{coll}] {len(old)} -> {len(items)} 条"
            + (f"，新增 {len(added)}: {', '.join(sorted(added)[:5])}{'…' if len(added) > 5 else ''}" if added else "")
            + (f"，移除 {len(removed)}" if removed else "")
        )
        time.sleep(0.3)

    if not dry:
        for sib in SIBLINGS:
            sync_sibling(sib, summary)

    print(f"=== design-partner 知识库刷新 {'(dry-run)' if dry else '完成'} · {date_str} ===")
    for line in report + summary:
        print(line)


if __name__ == "__main__":
    main()
