#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
design-partner README 自动生成器

从技能目录的真实文件统计条目数、快照日期、升级记录，重建 README.md。
目的：每次知识库迭代后 README 数据自动对齐，避免手写数字过期。

用法:
    python scripts/build_readme.py            # 写入 README.md
    python scripts/build_readme.py --dry-run  # 只打印不写盘
"""
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

# (文件名, 中文名, 定位说明)
ASSETS = [
    ("knowledge-map.md", "知识路线图", "L0→L4 分级目标 / 必读 / 练习 / 验收 + 20 条自测"),
    ("patterns.md", "元素设计模式", "12 类高频元素的构型谱系、参数区间、速配规则"),
    ("design-tokens.md", "设计 Token 体系", "三层架构 / Ant Design 数值全量 / 三大体系对比 / 中文设计系统矩阵"),
    ("design-md-format.md", "DESIGN.md 规范", "九章骨架 + 54 品牌 DNA 速查 + 项目类型选型"),
    ("chinese-design.md", "中文设计场景", "中文排版规范 + 中文设计生态地图 + 产品形态特征"),
    ("inspiration.md", "灵感与阅读", "策展画廊与设计阅读"),
    ("resources.md", "设计资源", "组件 / 图标 / 动效 3D / 字体配色"),
    ("component-libraries.md", "组件库地图", "14 库元素覆盖矩阵（GitHub API 验证）"),
    ("tools.md", "制作工具", "开发 / AI / 截取 / 效率工具"),
    ("portfolios.md", "作品集", "一线从业者站点，用于审美校准"),
]

ENTRY_RE = re.compile(r"^- \*\*\[(.+?)\]", re.M)
SNAPSHOT_RE = re.compile(r"快照\s*(\d{4}-\d{2}-\d{2})")
VERIFY_RE = re.compile(r"(\d{4}-\d{2}-\d{2})\s*经?\s*GitHub\s*API")


def count_entries(path: Path) -> int:
    if not path.exists():
        return 0
    return len(ENTRY_RE.findall(path.read_text(encoding="utf-8")))


def snapshot(path: Path) -> str:
    if not path.exists():
        return "—"
    text = path.read_text(encoding="utf-8")[:1500]
    for rx in (SNAPSHOT_RE, VERIFY_RE):
        m = rx.search(text)
        if m:
            return m.group(1)
    return "—"


def changelog() -> list:
    """从 design-log.md 提取 `## YYYY-MM-DD · 标题` 作为升级记录。"""
    p = MEM / "design-log.md"
    if not p.exists():
        return []
    rows = []
    for line in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (\d{4}-\d{2}-\d{2}) · (.+)$", line.strip())
        if m:
            rows.append((m.group(1), m.group(2)))
    return rows[-8:][::-1]


def build() -> str:
    rows, total_entries, total_files = [], 0, 0
    for fname, name, desc in ASSETS:
        p = REF / fname
        n = count_entries(p)
        snap = snapshot(p)
        total_files += 1 if p.exists() else 0
        total_entries += n
        rows.append(f"| [{name}](references/{fname}) | {desc} | {n if n else '规则型'} | {snap} |")

    log = changelog()
    log_md = "\n".join(f"| {d} | {t} |" for d, t in log) or "| — | 尚无记录 |"
    today = time.strftime("%Y-%m-%d")

    return f"""# Design Partner · 设计伙伴

> 一个会**自我进化**的设计 Skill：把模糊的想法变成有品味的设计决策，并在每次使用与每日迭代中变得更准。

![version](https://img.shields.io/badge/version-v4-1677ff)
![assets](https://img.shields.io/badge/reference_files-{total_files}-2ea44f)
![entries](https://img.shields.io/badge/curated_entries-{total_entries}-e60023)
![updated](https://img.shields.io/badge/updated-{today}-6e7781)

---

## 它解决什么问题

| 问题 | 表现 | 本 Skill 的解法 |
|---|---|---|
| **需求不清** | "做个好看点的页面" | 第 2 步：设计 brief 澄清（给选项，不问开放题） |
| **不知可行与否** | 做完才发现做不出来 | 第 3 步：可行性 × 美观性预判，执行前先给评审 |
| **没有参照** | 只会一种做法，遇到新场景就硬套 | 第 4 步：三级精准匹配（元素级 / 风格级 / 实现级） |
| **系统不统一** | 第 5 个页面和第 1 个不像同一产品 | 三层 token + DESIGN.md 契约 |
| **中文场景翻车** | 直接套英文规范，字号小、行距挤、标点乱 | `chinese-design.md` 中文排版修正 |
| **产出平庸** | 说不上哪不好，但就是不对 | 第 5 步原则执行 + 第 6 步 8 项自检 |
| **不记得用户偏好** | 每次都从零猜 | `memory/design-log.md` 持续蒸馏偏好画像 |

---

## 知识资产（自动统计，随迭代更新）

| 资产 | 内容 | 条目 | 快照 |
|---|---|---|---|
{chr(10).join(rows)}

> 条目数与快照日期由 `scripts/build_readme.py` 从文件实时统计，不手写。
> 快照 > 30 天时执行 `python scripts/refresh_catalog.py` 自动重抓。

---

## 六步工作流

```
第 1 步  识别设计意图  →  10 类意图路由（做新 / 改旧 / 要灵感 / 审美判断 / 评估需求 / 要规范 / 对标品牌 / 中文项目 / 找资产 / 想提升）
第 2 步  完善需求      →  brief 澄清，最多 3 个问题，给选项不给开放题；主动提示盲区
第 3 步  可行性×美观性 →  技术/范围/资源/性能 四查 + 审美风险预判，给明确立场
第 4 步  匹配灵感      →  L1 元素级（出可视化设计板）/ L2 风格级（品牌 DNA）/ L3 实现级（组件库）
第 5 步  按原则执行    →  层级 / 排版 / 色彩 / 间距 / 动效 / 一致性 / 系统化 / 中文修正
第 6 步  自检与交付    →  8 项自检（含中文关、系统关）+ 交付说明三段式
```

**核心主张：给立场，不和稀泥。** 评审先给结论再列备选；⚠️ 时给"满足什么条件就可行"，❌ 时给最接近意图的替代方案。

---

## 知识路线图 L0→L4

| 级别 | 目标 | 可交付物 |
|---|---|---|
| **L0** 视觉感知 | 能**看出**两个设计的高低 | 一份"好在哪/差在哪"的书面判断 |
| **L1** 界面语汇 | 知道每个元素**有几种做法** | 元素级设计板（4–6 变体） |
| **L2** 系统秩序 | 用**一套 token** 统管全站 | token 表 + DESIGN.md |
| **L3** 工程落地 | 把设计**变成可运行代码** | 组件代码 / 可交互页面 |
| **L4** 判断与品味 | 在**冲突约束**下做取舍 | 设计评审报告、方案对比结论 |

含三条专题支线（中文场景 / 数据可视化 / 动效）、学习节奏表、20 条能力自测 → 见 [`references/knowledge-map.md`](references/knowledge-map.md)

---

## 自我进化机制

```
每日  ┌─ 取源：Design-related websites.txt + 上轮待挖项 + 知识缺口
      ├─ 验证：GitHub API 实测 star/许可；规范数值读官方原文
      ├─ 蒸馏：产出可执行判断规则（数值/构型/验收），不是链接清单
      ├─ 接线：更新 SKILL.md 路由，让新知识在对的时机被读到
      └─ 归档：design-log 追加 → build_readme 重算 → git push
```

**质量门槛**：一轮升级至少要让某类问题**不再含糊**（能给具体数值或明确立场）。只多了几条链接 = 无效升级，重做。

**记忆协议**：偏好信号出现 ≥2 次即升级为画像规则；画像优先于通用推荐；记录只增不改，保持可审计。

---

## 升级记录

| 日期 | 内容 |
|---|---|
{log_md}

---

## 数据来源

- [designeer.xyz](https://designeer.xyz/) — 按 craft / utility / clarity / relevance 人工策展的 657 条资源
- [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — 54 个真实产品 DESIGN.md
- [Ant Design 设计规范](https://ant.design/docs/spec/introduce-cn) — 价值观 / 色彩 / 字体 / 布局原文
- [W3C clreq](https://www.w3.org/TR/clreq/) — 中文排版需求
- [Material Design 3](https://m3.material.io/) · [Apple HIG](https://developer.apple.com/design/human-interface-guidelines)

## 目录结构

```
design-partner/
├── SKILL.md                  # 主文件：六步工作流 + 资产索引 + 进化协议
├── README.md                 # 本文件（自动生成）
├── references/               # 知识库（10 份，见上表）
├── memory/design-log.md      # 偏好画像 + 匹配日志（只增不改）
└── scripts/
    ├── refresh_catalog.py    # 重抓目录 API，重建 references
    ├── build_readme.py       # 统计并重建 README
    └── publish_github.py     # REST API 发布（git push 被网络策略拦截时用）
```

## License

MIT
"""


def main():
    text = build()
    if "--dry-run" in sys.argv:
        print(text)
        return
    (ROOT / "README.md").write_text(text, encoding="utf-8")
    print(f"README.md 已生成 · {len(text.splitlines())} 行")


if __name__ == "__main__":
    main()
