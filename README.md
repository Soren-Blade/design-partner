# Design Partner · 设计伙伴

> 一个会**自我进化**的设计 Skill：把模糊的想法变成有品味的设计决策，并在每次使用与每日迭代中变得更准。

![version](https://img.shields.io/badge/version-v5-1677ff)
![assets](https://img.shields.io/badge/reference_files-11-2ea44f)
![entries](https://img.shields.io/badge/curated_entries-657-e60023)
![updated](https://img.shields.io/badge/updated-2026-10-30-6e7781)

---

## 它解决什么问题

| 问题 | 表现 | 本 Skill 的解法 |
|---|---|---|
| **需求不清** | "做个好看点的页面" | 第 2 步：设计 brief 澄清（给选项，不问开放题） |
| **不知可行与否** | 做完才发现做不出来 | 第 3 步：可行性 × 美观性预判，执行前先给评审 |
| **没有参照** | 只会一种做法，遇到新场景就硬套 | 第 4 步：三级精准匹配（元素级 / 风格级 / 实现级） |
| **系统不统一** | 第 5 个页面和第 1 个不像同一产品 | 三层 token + DESIGN.md 契约 |
| **动效凭感觉** | 时长随手写 500ms、入场出场一样慢 | `motion-system.md` 语义曲线 + 时长刻度 + 场景表 |
| **中文场景翻车** | 直接套英文规范，字号小、行距挤、标点乱 | `chinese-design.md` 中文排版修正 |
| **产出平庸** | 说不上哪不好，但就是不对 | 第 5 步原则执行 + 第 6 步 9 项自检 |
| **知识找不到** | 12 份参考、12 万字符，不知读哪节 | `memory/tree.md` 记忆树 + `dp_search.py` 章节级检索 |
| **不记得用户偏好** | 每次都从零猜 | `memory/design-log.md` 持续蒸馏偏好画像 |

---

## 知识资产（自动统计，随迭代更新）

| 资产 | 内容 | 条目 | 快照 |
|---|---|---|---|
| [知识路线图](references/knowledge-map.md) | L0→L4 分级目标 / 必读 / 练习 / 验收 + 20 条自测 | 规则型 | 2026-10-29 |
| [元素设计模式](references/patterns.md) | 12 类高频元素的构型谱系、参数区间、速配规则 | 规则型 | 2026-10-29 |
| [设计 Token 体系](references/design-tokens.md) | 三层架构 / Ant Design 数值全量 / 三大体系对比 / 中文设计系统矩阵 | 规则型 | 2026-10-29 |
| [动效与微交互系统](references/motion-system.md) | 曲线语义表（M3/Carbon/Ant 精确值）/ 时长刻度 / 20 场景速查 / 转场代码 / 降级与验收 | 规则型 | 2026-10-30 |
| [DESIGN.md 规范](references/design-md-format.md) | 九章骨架 + 54 品牌 DNA 速查 + 项目类型选型 | 规则型 | 2026-10-29 |
| [中文设计场景](references/chinese-design.md) | 中文排版规范 + 中文设计生态地图 + 产品形态特征 | 规则型 | 2026-10-29 |
| [灵感与阅读](references/inspiration.md) | 策展画廊与设计阅读 | 137 | 2026-10-29 |
| [设计资源](references/resources.md) | 组件 / 图标 / 动效 3D / 字体配色 | 201 | 2026-10-29 |
| [组件库地图](references/component-libraries.md) | 14 库元素覆盖矩阵（GitHub API 验证） | 规则型 | 2026-10-29 |
| [制作工具](references/tools.md) | 开发 / AI / 截取 / 效率工具 | 153 | 2026-10-29 |
| [作品集](references/portfolios.md) | 一线从业者站点，用于审美校准 | 166 | 2026-10-29 |

> 条目数与快照日期由 `scripts/build_readme.py` 从文件实时统计，不手写。
> 快照 > 30 天时执行 `python scripts/refresh_catalog.py` 自动重抓。

---

## 七步工作流

```
第 0 步  先检索        →  dp_search.py 定位到「文件 §章节」，只读那一段
第 1 步  识别设计意图  →  12 类意图路由（做新 / 改旧 / 要灵感 / 审美判断 / 评估需求 / 要规范 / 对标品牌 / 中文项目 / 动效 / 转场 / 找资产 / 想提升）
第 2 步  完善需求      →  brief 澄清，最多 3 个问题，给选项不给开放题；主动提示盲区
第 3 步  可行性×美观性 →  技术/范围/资源/性能 四查 + 审美风险预判，给明确立场
第 4 步  匹配灵感      →  L1 元素级（出可视化设计板）/ L2 风格级（品牌 DNA）/ L3 实现级（组件库）
第 5 步  按原则执行    →  层级 / 排版 / 色彩 / 间距 / 动效 / 一致性 / 系统化 / 中文修正
第 6 步  自检与交付    →  9 项自检（含中文关、系统关、动效关）+ 交付说明三段式
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
| [`memory/tree.md`](memory/tree.md) | 意图→位置路由表 + 全资产章节树 + 接线体检（谁写了但没被路由） |
| `memory/index.json` | 机器索引：文件 → 章节 → 行号 → 摘要（检索数据源） |
| `scripts/dp_search.py` | 中文按二元组拆词、英文按词拆，标题/摘要/正文加权打分 |
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

含三条专题支线（中文场景 / 数据可视化 / 动效）、学习节奏表、20 条能力自测 → 见 [`references/knowledge-map.md`](references/knowledge-map.md)

---

## 自我进化机制

```
每日  ┌─ 取源：Design-related websites.txt + 上轮待挖项 + 知识缺口
      ├─ 验证：GitHub API 实测 star/许可；规范数值读官方原文
      ├─ 蒸馏：产出可执行判断规则（数值/构型/验收），不是链接清单
      ├─ 接线：更新 SKILL.md 路由 + mindmap.py 重建记忆树（含接线体检）
      └─ 归档：design-log 追加 → build_readme 重算 → git commit → REST API 推送
```

**质量门槛**：一轮升级至少要让某类问题**不再含糊**（能给具体数值或明确立场）。只多了几条链接 = 无效升级，重做。

**检索门槛**：新知识必须能被 `dp_search.py "关键词"` 命中前 3 条，否则说明标题不像索引。

**记忆协议**：偏好信号出现 ≥2 次即升级为画像规则；画像优先于通用推荐；记录只增不改，保持可审计。

---

## 升级记录

| 日期 | 内容 |
|---|---|
| 2026-10-30 | 动效系统 + 记忆树与检索（每日升级 #2） |
| 2026-10-29 | v4 系统化与中文场景补齐（每日升级 #1） |
| 2026-10-29 | 元素级精准匹配升级（v3） |
| 2026-10-28 | 开发者工具深色落地页（自测） |

---

## 数据来源

- [designeer.xyz](https://designeer.xyz/) — 按 craft / utility / clarity / relevance 人工策展的 657 条资源
- [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — 54 个真实产品 DESIGN.md
- [Ant Design 设计规范](https://ant.design/docs/spec/introduce-cn) — 价值观 / 色彩 / 字体 / 布局 / 动效原文
- [Material 3 · Easing & duration tokens](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs) — 曲线与时长 token 全表
- [Carbon Design System · Motion](https://www.carbondesignsystem.com/elements/motion/overview/) — productive/expressive 二分与评估清单
- [Fluent 2 · Motion](https://fluent2.microsoft.design/motion) — 四种转场模式与编排原则
- [MDN](https://developer.mozilla.org/) — View Transition API / scroll-driven animations / prefers-reduced-motion
- [W3C clreq](https://www.w3.org/TR/clreq/) — 中文排版需求
- [Apple HIG](https://developer.apple.com/design/human-interface-guidelines)

## 目录结构

```
design-partner/
├── SKILL.md                  # 主文件：七步工作流 + 资产索引 + 进化协议
├── README.md                 # 本文件（自动生成）
├── references/               # 知识库（11 份，见上表）
├── memory/
│   ├── tree.md               # 记忆树（自动生成）
│   ├── index.json            # 检索索引（自动生成）
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
