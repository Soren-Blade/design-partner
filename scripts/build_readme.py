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

# (文件名, 中文名, 定位说明)
ASSETS = [
    ("knowledge-map.md", "知识路线图", "L0→L4 分级目标 / 必读 / 练习 / 验收 + {selftests} 条自测"),
    ("patterns.md", "元素设计模式", "12 类高频元素的构型谱系、参数区间、速配规则"),
    ("design-tokens.md", "设计 Token 体系", "三层架构 / Ant Design 数值全量 / 三大体系对比 / 中文设计系统矩阵"),
    ("motion-system.md", "动效与微交互系统", "曲线语义表（M3/Carbon/Ant 精确值）/ 时长刻度 / 20 场景速查 / 转场代码 / 降级与验收"),
    ("dataviz.md", "数据可视化规范", "FT 九类关系选型 / Carbon·AntV 精确色板 / 坐标轴与图例数值 / 仪表盘布局 / 12 条反模式"),
    ("form-table.md", "表单与表格规范", "标签对齐决策 / 字段定宽 / 校验三档与 12 条错误文案模板 / 行高三档 / 列对齐 / 分页·批量·空态 / 18 条反模式"),
    ("accessibility.md", "可访问性实操", "WCAG 2.2 四档阈值 / 焦点三层标准与可抄样式 / 24px 圆间距例外 / ARIA 纪律 / aria-live / 读屏实测 / GB/T 37668 与适老化 / 25 条自检"),
    ("feedback-states.md", "反馈与状态设计", "五层反馈决策树 / 0.1·1·10s 阈值 / 四体系 toast 时长与宽度 / 加载三形态 / 进度六铁律 / 五种空态 / 五级错误 / 确认框八条 / 五态模型 / WCAG 4.1.3 / 15 项自检"),
    ("responsive-layout.md", "响应式与断点体系", "六体系断点精确值对照 / 断点按内容定 / 跨断点五动词 / gutter 固定 column 流体 / 版心阶梯 / 容器查询 / clamp 无障碍公式 / 视口单位陷阱 / 窄屏表格四策略 / 中后台 1440 适配 / 20 条反模式"),
    ("editorial-layout.md", "版式与网格（Editorial）", "五类载体决策 / 网格五型 / 12 栏与基线 / Van de Graaf 页边距 2:3:4:6 / 模数阶梯七档 / 行长 45–90 字符与行距 120–145% / 孤寡行与断行 / 海报出血 3mm 与安全区 / 长图字号换算 / 九平台社媒尺寸 / 印刷 CMYK 与总墨量 300% / 竖排与避头尾 / 18 项自检"),
    ("brand-identity.md", "品牌视觉与 Logo 逻辑", "四层结构 / 三词定位与六维翻译 / 七型标志决策树 / 24dp 网格与四基形 / 光学修正四条 / 清space 三口径 / 最小尺寸 40px·10mm / 响应式标志四档 / 种子色四问 / 三条色阶路线（HCT·Radix 12 步·对比度优先）/ M3 亮暗 tone 全表 / 图标网格两体系 / 插画五参数 / 品牌语气四维 / 资产交付清单 / 商标与授权合规 / 18 项自检"),
    ("performance-design.md", "性能与设计的关系", "CWV 七指标阈值与 p75 口径 / Lighthouse 10 权重 / LCP 四分解 40·10·40·10 / INP 三阶段与长任务 50ms / CLS 公式与 500ms 免责窗口 / 关键路径 170KB 与六类页面预算 / 图片格式矩阵与 25 倍像素浪费 / font-display 五档与中文字集化 / 视觉手法性能价格表 / 帧预算 16.67ms 与图层内存算术 / 三档决策分级 / 弱网三层降级 / 小程序单包 2MB / 18 项自检"),
    ("dark-mode.md", "暗色模式体系", "该不该做的 NN/g 证据链 / 三态切换决策树 / 表面层级三套精确值（M3 tone 4·6·10·12·17·22 / Ant lighten 0·8·12·26 / Carbon g100 阶梯）/ 实测对比度陷阱（45% 白仅 4.43、边框仅 2.09:1）/ 不用纯白的四体系共识 / 阴影两派与合成方案 / 品牌色 tone 重映射 / 涨跌色双套 / 图像四死法 / 四端实现与防闪白 / 暗色专属八陷阱 / 22 项自检"),
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


def alias_count() -> int:
    """从 memory/aliases.json 实时统计别名组数，避免手写数字过期。"""
    p = MEM / "aliases.json"
    if not p.exists():
        return 0
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return len(data.get("groups", []))
    except Exception:
        return 0


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


def skill_facts() -> dict:
    """从 SKILL.md 与 references/ 实时推导版本号、路由数、自检数、字数。

    README 里的数字一律不手写——上一轮就出现过「11 份参考」「12 类意图路由」
    这类硬编码过期的问题。全部改为从真实文件统计。
    """
    facts = {"version": "?", "routes": 0, "checks": 0, "refs": 0, "chars": 0, "selftests": 0, "branches": []}
    refs = sorted(REF.glob("*.md"))
    facts["refs"] = len(refs)
    facts["chars"] = sum(len(p.read_text(encoding="utf-8")) for p in refs)

    km = REF / "knowledge-map.md"
    if km.exists():
        kt = km.read_text(encoding="utf-8")
        facts["selftests"] = len(re.findall(r"^- \[ \]", kt, re.M))
        # 专题支线：`### 支线 X · 名称（…）` → 只取名称部分
        facts["branches"] = [re.sub(r"（.*$", "", b).strip()
                             for b in re.findall(r"^### 支线 [A-Z] · (.+)$", kt, re.M)]

    sk = ROOT / "SKILL.md"
    if not sk.exists():
        return facts
    text = sk.read_text(encoding="utf-8")

    m = re.search(r"当前版本\s*v(\d+)", text)
    if m:
        facts["version"] = m.group(1)

    # 意图路由：第 1 步表格中以 `| **` 开头的行
    seg = re.search(r"### 第 1 步.*?(?=### 第 2 步)", text, re.S)
    if seg:
        facts["routes"] = len(re.findall(r"^\|\s*\*\*", seg.group(0), re.M))

    # 自检项：第 6 步中以 `N. **` 开头的行
    seg = re.search(r"### 第 6 步.*?(?=\n---)", text, re.S)
    if seg:
        facts["checks"] = len(re.findall(r"^\d+\.\s*\*\*", seg.group(0), re.M))

    return facts


def build() -> str:
    f = skill_facts()
    rows, total_entries, total_files = [], 0, 0
    for fname, name, desc in ASSETS:
        desc = desc.replace("{selftests}", str(f["selftests"]))
        p = REF / fname
        n = count_entries(p)
        snap = snapshot(p)
        total_files += 1 if p.exists() else 0
        total_entries += n
        rows.append(f"| [{name}](references/{fname}) | {desc} | {n if n else '规则型'} | {snap} |")

    log = changelog()
    log_md = "\n".join(f"| {d} | {t} |" for d, t in log) or "| — | 尚无记录 |"
    today = time.strftime("%Y-%m-%d")
    wan = f"{f['chars'] / 10000:.0f}"

    return f"""# Design Partner · 设计伙伴

> 一个会**自我进化**的设计 Skill：把模糊的想法变成有品味的设计决策，并在每次使用与每日迭代中变得更准。

![version](https://img.shields.io/badge/version-v{f['version']}-1677ff)
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
| **动效凭感觉** | 时长随手写 500ms、入场出场一样慢 | `motion-system.md` 语义曲线 + 时长刻度 + 场景表 |
| **图表不像专业出品** | 饼图切 8 片、柱状图截断轴、配色靠感觉 | `dataviz.md` 九类关系选型 + 精确色板 + 坐标轴铁律 |
| **表单难填、表格难读** | 一进来就全红、错误只说"格式不正确"、表格全列居中 | `form-table.md` 校验三档 + 错误文案模板 + 行高与列对齐铁律 |
| **无障碍过不了验收** | 焦点框被 `outline:none` 杀掉、只靠颜色表状态、读屏念不出、适老化尺寸不够 | `accessibility.md` 四档阈值 + 焦点三层 + 24/44/60 三档 + 25 条自检 |
| **反馈要么吵要么没** | 保存成功弹一堆 toast、严重错误 3 秒就消失、加载转圈 15 秒没进度、空态只放插画 | `feedback-states.md` 五层决策树 + toast 精确时长 + 五种空态 + 五级错误 |
| **多端就散架** | 手机上横向滚动、`100vh` 被地址栏挡住、8 列表格硬变卡片、大屏只是把手机版放大 | `responsive-layout.md` 六体系断点对照 + 五动词降级 + 窄屏表格四策略 + 版心阶梯 |
| **版式全靠感觉** | 一行 130 字读不下去、海报裁切露白边、长图字小到看不清、印出来颜色发暗 | `editorial-layout.md` 行长行距联动表 + 出血与安全区 + 长图字号换算 + 印刷五查 |
| **品牌立不住** | logo 好看但说不清为什么、缩小就糊、品牌色一进暗色模式就脏、交付缺图标尺寸、没注册商标 | `brand-identity.md` 三词定位 + 七型决策树 + 24 网格构造 + 清space 与最小尺寸 + 色阶三路线 + tone 映射 + 交付清单 + 商标合规 |
| **暗色模式一开就脏** | 把亮色反一下就当暗色、纯白字刺眼、卡片和背景分不开、切换闪白、辅助文字看不清 | `dark-mode.md` 该不该做的证据链 + 三套表面层级精确值 + 不用纯白 + 实测对比度陷阱 + 四端实现与防闪白 |
| **中文场景翻车** | 直接套英文规范，字号小、行距挤、标点乱 | `chinese-design.md` 中文排版修正 |
| **产出平庸** | 说不上哪不好，但就是不对 | 第 5 步原则执行 + 第 6 步 {f['checks']} 项自检 |
| **知识找不到** | {f['refs']} 份参考、{wan} 万字符，不知读哪节 | `memory/tree.md` 记忆树 + `dp_search.py` 章节级检索 |
| **不记得用户偏好** | 每次都从零猜 | `memory/design-log.md` 持续蒸馏偏好画像 |

---

## 知识资产（自动统计，随迭代更新）

| 资产 | 内容 | 条目 | 快照 |
|---|---|---|---|
{chr(10).join(rows)}

> 条目数与快照日期由 `scripts/build_readme.py` 从文件实时统计，不手写。
> 快照 > 30 天时执行 `python scripts/refresh_catalog.py` 自动重抓。

---

## 七步工作流

```
第 0 步  先检索        →  dp_search.py 定位到「文件 §章节」，只读那一段
第 1 步  识别设计意图  →  {f['routes']} 类意图路由（全表见 SKILL.md 第 1 步）
第 2 步  完善需求      →  brief 澄清，最多 3 个问题，给选项不给开放题；主动提示盲区
第 3 步  可行性×美观性 →  技术/范围/资源/性能 四查 + 审美风险预判，给明确立场
第 4 步  匹配灵感      →  L1 元素级（出可视化设计板）/ L2 风格级（品牌 DNA）/ L3 实现级（组件库）
第 5 步  按原则执行    →  层级 / 排版 / 色彩 / 间距 / 动效 / 图表 / 表单 / 表格 / 反馈与状态 / 响应式 / 版式与网格 / 一致性 / 系统化 / 中文修正
第 6 步  自检与交付    →  {f['checks']} 项自检（含中文关、系统关、动效关、图表关、表单关、表格关、无障碍关、反馈关、响应式关、版式关、品牌关、暗色关、性能关）+ 交付说明三段式
```

**核心主张：给立场，不和稀泥。** 评审先给结论再列备选；⚠️ 时给"满足什么条件就可行"，❌ 时给最接近意图的替代方案。

---

## 记忆树与快捷检索

资产过千行后，"知识在哪"本身成了问题。本技能自带一层索引：

```bash
python scripts/dp_search.py "缓动曲线"    # → references/motion-system.md §2 (L30) + 摘要
python scripts/dp_search.py --topic       # 全部主题总览
python scripts/mindmap.py                 # 重建 memory/tree.md + index.json，并做接线体检
```

| 文件 | 作用 |
|---|---|
| [`memory/tree.md`](memory/tree.md) | 意图→位置路由表 + 别名映射 + 全资产章节树 + 接线体检（谁写了但没被路由） |
| `memory/index.json` | 机器索引：文件 → 章节 → 行号 → 摘要（检索数据源） |
| `memory/aliases.json` | **检索层别名映射**：{alias_count()} 组口语/术语/中英对应，只提升召回、不改路由优先级 |
| `scripts/dp_search.py` | 中文按二元组拆词、英文按词拆，标题/摘要/正文加权打分；别名以 0.45 权重补充召回 |
| `scripts/mindmap.py` | 扫描全部 Markdown 重建索引；`--check` 只跑体检 |

**接线体检**是自我进化的自检项：新增参考文件却忘了在 `SKILL.md` 加路由时，`mindmap.py` 会直接报「未接线」——避免"写了等于没写"。

---

## 知识路线图 L0→L4

| 级别 | 目标 | 可交付物 |
|---|---|---|
| **L0** 视觉感知 | 能**看出**两个设计的高低 | 一份"好在哪/差在哪"的书面判断 |
| **L1** 界面语汇 | 知道每个元素**有几种做法** | 元素级设计板（4–6 变体） |
| **L2** 系统秩序 | 用**一套 token** 统管全站 | token 表 + DESIGN.md |
| **L3** 工程落地 | 把设计**变成可运行代码** | 组件代码 / 可交互页面 |
| **L4** 判断与品味 | 在**冲突约束**下做取舍 | 设计评审报告、方案对比结论 |

含{len(f['branches'])}条专题支线（{' / '.join(f['branches'])}）、学习节奏表、{f['selftests']} 条能力自测 → 见 [`references/knowledge-map.md`](references/knowledge-map.md)

---

## 自我进化机制

```
每日  ┌─ 取源：Design-related websites.txt + 上轮待挖项 + 知识缺口
      ├─ 验证：GitHub API 实测 star/许可；规范数值读官方原文
      ├─ 蒸馏：产出可执行判断规则（数值/构型/验收），不是链接清单
      ├─ 接线：更新 SKILL.md 路由 + 补 memory/aliases.json 别名 + mindmap 重建记忆树（含接线体检）
      └─ 归档：design-log 追加 → build_readme 重算 → git commit → REST API 推送
```

**质量门槛**：一轮升级至少要让某类问题**不再含糊**（能给具体数值或明确立场）。只多了几条链接 = 无效升级，重做。

**检索门槛**：新知识必须能被 `dp_search.py "关键词"` 命中前 3 条，否则说明标题不像索引。

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
- [Ant Design 设计规范](https://ant.design/docs/spec/introduce-cn) — 价值观 / 色彩 / 字体 / 布局 / 动效原文
- [Material 3 · Easing & duration tokens](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs) — 曲线与时长 token 全表
- [Carbon Design System · Motion](https://www.carbondesignsystem.com/elements/motion/overview/) — productive/expressive 二分与评估清单
- [Fluent 2 · Motion](https://fluent2.microsoft.design/motion) — 四种转场模式与编排原则
- [MDN](https://developer.mozilla.org/) — View Transition API / scroll-driven animations / prefers-reduced-motion
- [FT Visual Vocabulary](https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary) — 九类数据关系与图形选型（含简体中文版）
- [IBM Carbon · Data visualization color palettes](https://carbondesignsystem.com/data-visualization/color-palettes/) — 分类/顺序/发散色板精确 hex 与取用顺序
- [AntV G2](https://github.com/antvis/G2) — 色板、坐标轴、图例、Tooltip 默认值（源码实测）
- [W3C WCAG 2.2 SC 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) — 图形对象 3:1 非文本对比度
- [Datawrapper](https://www.datawrapper.de/blog/dual-axis-charts-guide) — 双轴图的适用条件与误导机制
- [W3C clreq](https://www.w3.org/TR/clreq/) — 中文排版需求
- [Apple HIG](https://developer.apple.com/design/human-interface-guidelines)

## 目录结构

```
design-partner/
├── SKILL.md                  # 主文件：七步工作流 + 资产索引 + 进化协议
├── README.md                 # 本文件（自动生成）
├── references/               # 知识库（{total_files} 份，见上表）
├── memory/
│   ├── tree.md               # 记忆树（自动生成）
│   ├── index.json            # 检索索引（自动生成）
│   ├── aliases.json          # 检索层别名映射（手维护）
│   └── design-log.md         # 偏好画像 + 匹配日志（只增不改）
└── scripts/
    ├── dp_search.py          # 章节级快捷检索
    ├── mindmap.py            # 重建记忆树 + 接线体检
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
