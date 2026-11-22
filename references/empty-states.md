# 空状态与零数据位（Empty States & Zero-Data）

> 快照 2026-11-20 · 一手：Carbon empty-states pattern 仓库源码（2026-11-20 取全文）、Ant Design Empty 组件与 token、Atlassian Empty state（后两者 2026-11-13 逐字核验，2026-11-20 复取失败）；NN/g、Material 3、Apple HIG 未取得逐字正文 → 见 §15 取源限制。

## §0 一句话立场

空状态不是"没有数据的占位"，而是**整块界面里最被浪费的引导位**：用户第一次看到某个视图、或某个操作清空后，注意力最集中、动机最强，却往往只收到一句"暂无数据"。本资产与 `feedback-states.md §5`（五种"空"分类）是**同一主题的两层**：§5 给分类与速查，本资产给**可抄的中英文文案矩阵、零数据位（starter content）设计模式、装饰插画的无障碍取舍、变体承载位置、以及"空状态有没有用"的度量口径**。

三条裁决（均引一手原文，见 §15）：

1. **默认要引导，不要道歉、不要留白死路。** Atlassian 原文：*"Empty states can be a chance to celebrate, educate, and inform people of what they can do next."* Ant Design：*"User tutorial to create something in fresh new situation."* 只写"暂无数据"等于把引导位空着。
2. **装饰性插画必须被读屏跳过，且不让焦点滞留。** Atlassian Accessibility：*"If the illustration provides useful information, include alternative text. If it's only for decoration, avoid alt text or remove the image altogether."* Carbon 补了口径：*"an empty alt tag is more widely supported… avoid assigning role to presentation until support is more ubiquitous."* → 纯装饰图**首选 `alt=""`**，`role="presentation"` 不作首选，`role="img" aria-hidden="true"` 只在上下文仍需隐藏时叠用；且不能成为 Tab 停留点（SC 1.1.1 / 2.4.3）。
3. **失败空态 ≠ 无数据空态，禁止伪装。** 错误空态必须给"为什么失败 + 重试"；把它渲染成"暂无数据"会让用户以为真的没有，于是不再重试（见 §11）。

---

## §1 为什么空状态是被浪费的引导位

- **注意力窗口**：用户看到空视图的瞬间，是在问"这是什么、我现在该做什么"。这个窗口不填，下次就不会再回来问。
- **动机最强**：首启 / 清空后，用户刚完成一个动作（建项目、清空收件箱），正处于"想继续"的状态，比随机落地页转化意愿高。
- **最便宜的引导**：不占导航、不打断流程，是**渐进披露**（`onboarding-first-run.md §5`）最轻的一档——不需要教程、不需要 coach mark，一句话 + 一个按钮就够。
- **最常被浪费**：团队把精力放在"有数据时多好看"，空状态交给后端默认文案"暂无数据 / No data"，等于把引导位清空。
- **判定起点**：先回答"这是哪一种空"（§2），再决定给什么。把失败渲染成无数据，是最高频也最贵的错误。

---

## §2 五种空状态分类与判型（判型器）

与 `feedback-states.md §5.1` 同源，本文件给**判型顺序**，不重复那张分类速度表。

| 触发 | 用户心理 | 该给什么（不重复 §5 表格，给判型信号） |
|---|---|---|
| **首次空**（新账号/新项目） | "这东西怎么用？" | 说明将出现什么 + **一个主操作**；可用零数据位（§7）直接示范 |
| **无结果空**（搜索/筛选为 0） | "是不是我筛错了？" | 说明筛选条件 + **清除筛选**；**不要**给"新建" |
| **无权限空**（有数据不可见） | "为什么我看不到？" | 说明原因 + **申请权限 / 切换账号** |
| **失败空**（请求失败） | "是不是坏了？" | 说清失败原因 + **重试**；**不得伪装成"暂无数据"** |
| **完成空**（待办清空） | 正向情绪 | 一句肯定 + 可选下一步；**不要塞广告** |

**判型器（按此顺序，三问定类）**：

1. 刚才那个动作是"成功清空/完成"吗？→ 完成空（正向语气）。
2. 是用户主动搜/筛后为零吗？→ 无结果空（给清除，不给新建）。
3. 是数据请求失败吗？→ 失败空（给原因+重试，绝不伪装）。
4. 是权限导致不可见吗？→ 无权限空（给申请/切换）。
5. 以上都不是、且视图从未有过数据？→ 首次空（给主操作 + 可示范）。

> 判型错了比不判更糟：把失败当无数据，用户不再重试；把无结果当首次空给"新建"，用户会更困惑。

**一条硬线：版式可复用，状态不共用（Carbon 一手）**。Carbon 把权限、系统故障、缺配置、操作不支持都归进 empty state 的**版式**——原文 *"These are empty states that occur when data exists but cannot be surfaced for some reason"*——所以四类状态在数据层互斥：`loading | empty | error | forbidden`，只有 `200 + 空集合` 才是 empty，`length === 0` 只说明"没有可视行"。反例 `if (!rows.length) return <Empty description="暂无数据" />` 用一个分支接住四种原因，等于把"重试"这条唯一出路删掉（判据见 `before-after.md §0` J10）。**表格空态必须替换表头与表尾**：Carbon 原文 *"an empty state for a table would replace the table and the column headers and footer should not be present. This practice avoids having a screen reader read the entire table before getting to the message that there is no content in the table."*

---

## §3 空状态的结构五件套（Ant Design / Atlassian 一手解剖）

Atlassian 把空状态拆成四部分（Anatomy），Ant Design 的 Empty 组件给了 token 级的精确值。两者合并成**五件套**：

1. **插画 / 图标（可选）**：Atlassian *"Illustration (optional): A spot illustration that relates to the message literally or as a metaphor."* 空间小就省略，只留文字（Carbon 同口径）。
2. **标题（必填）**：Atlassian *"The only required part of the empty state component is the heading."* 用 h600 级标题；**正向表述**。
3. **说明（可选）**：一句"这里将出现什么 + 为什么现在是空的 + 做这一步的好处"。
4. **主操作（可选）**：按钮 / 正文内链接 / 指向界面元素（"点击右上角 + 新建"）。
5. **次操作（可选）**：文档链接等，弱化为文字链接。

**Ant Design Empty 一手 token（components/empty，5.23+）**：

| Token | 默认值 | 含义 |
|---|---|---|
| `colorTextDescription` | `rgba(0,0,0,0.45)` | 描述文字颜色（次级，不抢标题） |
| `controlHeightLG` | `40` | LG 按钮高度 |
| `fontSize` | `14` | 基础字号 |
| `margin` / `marginXL` / `marginXS` | `16` / `32` / `8` | 间距尺度 |
| 内置图 | `PRESENTED_IMAGE_SIMPLE` / `PRESENTED_IMAGE_DEFAULT` | 两档内置插画，无需自备资源 |

**Atlassian 宽度两档**：默认 `wide` = 464px（cozy 网格 6 列），`narrow` = 304px（4 列，用于小于默认宽度的容器）。标题用 h600；容器小于默认宽度时改用 `narrow`。

---

## §4 空状态文案公式与中英抄写矩阵（核心交付）

**公式（中文）**：`标题（正向，≤12 字）` + `说明（这里会出现什么 + 怎么做，≤30 字）` + `按钮（动词，≤6 字）`。
**公式（英文）**：`Headline (imperative or state, ≤6 words)` + `Description (what will appear + why empty + benefit, ≤1 sentence)` + `Button (verb, ≤2 words)`。

**中英抄写矩阵（可直接抄，按类型对齐）**：

| 类型 | 中文标题 | 中文说明 | 中文按钮 | English Headline | English Description | Button |
|---|---|---|---|---|---|---|
| 首次空 | 创建第一个项目 | 项目用来归类素材与成员，创建后即可协作 | 新建项目 | Create your first project | Projects keep your assets and teammates organized—start one to invite others. | Create |
| 首次空（清单） | 还没有任务 | 把今天要做的事加进来，完成后打勾即可 | 添加任务 | No tasks yet | Add what you need to do today, then check them off as you go. | Add task |
| 无结果空 | 没有匹配的结果 | 试试减少筛选条件，或换个关键词 | 清除筛选 | No results found | Try removing a filter or using a different keyword. | Clear filters |
| 无权限空 | 你没有查看权限 | 该看板属于「增长组」，可向管理员申请 | 申请权限 | You don't have access | This board belongs to the Growth team—request access to view it. | Request |
| 失败空 | 内容加载失败 | 网络似乎不稳定，请稍后重试 | 重新加载 | Couldn't load content | Your connection dropped—retry and we'll pick up where we left off. | Retry |
| 完成空 | 今天的任务都完成了 | 新任务分配后会出现在这里 | 查看历史 | All done for today | New tasks will show up here when they're assigned. | View history |
| 搜索空（全局） | 没找到相关内容 | 换个说法，或浏览下方的推荐 | 浏览推荐 | Nothing matched your search | Rephrase your query, or explore the suggestions below. | Browse |
| 空购物车 | 购物车还是空的 | 挑几件喜欢的，结算时一起优惠 | 去逛逛 | Your cart is empty | Add items you love—we'll apply discounts at checkout. | Shop now |

**文案纪律（来自 Atlassian Content guidelines + NN/g 共识）**：

- **正向优先**：Atlassian *"Always use sentence case for titles and headings."*；标题用"添加第一个数据源"优于"您还没有数据源"（Carbon 同口径）。
- **动词开头按钮**：Atlassian *"use imperative verbs such as Try, Remove, or Create."* 中文对应"新建 / 添加 / 重试 / 申请"。
- **控制长度**：Atlassian *"Try to limit the number of words… most people scan text instead of reading everything."* 说明 ≤30 字（中文）/ ≤1 句（英文）。
- **控制 CTA 数量**：Atlassian *"Be mindful of how many CTAs might appear on one page."*；同屏多空态用 tertiary / 纯文字，避免五个主按钮（同 `feedback-states.md §5.2` 纪律一）。
- **语气随场景（Atlassian 一手）**：首次空 → 启发/教育；完成空 → 庆祝；无结果 → 中性但给下一步。

---

## §5 装饰插画与图标：何时用、何时省、无障碍

Atlassian 对插画给了明确的可选性与禁忌：

- **可选，不是必须**：*"Illustrations are optional. Consider leaving out the illustration if there are other visuals competing on one screen, or if the space is too small."*
- **尺寸纪律**：*"Don't resize spot heroes or other larger illustrations to fit a smaller space."* 缩一张大图塞进小空态，比没有更乱。
- **语气**：*"Choose an image that has a neutral or humorous tone (never negative)."* 空状态插画**永远不要负面**（别用"出错/警告"感的图）。
- **国际化陷阱**：*"Using an image as a metaphor may not translate to all cultures and languages."* 隐喻图在跨语言时可能失灵——出海项目优先用抽象/通用图形，或本地化插画。
- **无障碍（裁决二落地）**：
  - 插画**承载信息**（如图示"这里能上传文件"）→ 必须 `alt` 描述其含义。
  - 插画**纯装饰** → `alt=""` 或 `role="img" aria-hidden="true"`，且**不能成为 Tab 焦点**（装饰图不应进焦点顺序，SC 2.4.3）。
  - 图标同理：纯装饰图标用 `aria-hidden="true"`；若图标即动作（如"上传"按钮内的图标），无障碍由按钮的 `aria-label` 承担，图标仍 `aria-hidden`。

**决策**：容器 < 304px（Atlassian narrow）→ 只留文字；同屏多空态 → 纯文字优先；首次空且空间充足 → 可用中性/幽默插画（承载位置见 §8）。

---

## §6 单主行动与 CTA 纪律

- **只给一个主操作**（Carbon / Atlassian 共识）：挑最重要的一个做主按钮，其余降为文字链接；仪表盘多卡片同屏失败时用 tertiary 或纯文字，避免五个主按钮。
- **不要制造死路**：任何空态都不该只留一句"暂无数据"——至少给一个去向（主操作或"浏览推荐"）。
- **主操作要具体**："新建项目"优于"开始使用"，"清除筛选"优于"返回"；动词 + 对象，≤6 字（中文）/ ≤2 词（英文）。

---

## §7 零数据位 / starter content：用示例教，而不是用文字讲

**零数据位（starter content）** 是首次空的最高形态：不直接教用户"点这里新建"，而是**预填一份示例 / 模板 / 示例数据**，让用户改着改着就会用。与 `onboarding-first-run.md §13` 同源（教学型零数据位），这里给**设计模式**。

- **模式 A · 模板入口**：首次空给"从模板开始"而非空白画布（Notion / Canva 范式），降低空白页恐惧。
- **模式 B · 预填示例 / 占位样本**：列表预填 1–3 行脱敏示例、图表给"长这样"的静态示例图；示例必须明显可辨、可一键清空，不伪装成真实数据。
- **模式 C · 引导式首条**：表单类把"添加第一条"做成内联输入（输入即创建），跳过"先点新建再填表"。

**判定**：零数据位适合**创作型**产品（文档/设计/表格/看板）；**交易/管理型**产品（订单/权限）更适合同步给主操作 + 说明，不宜预填假数据（合规与信任风险）。

---

## §8 变体与承载位置（全屏 / 容器内 / 表格区 / 迷你 widget）

同一份空状态文案，按承载位置降级：

| 承载位置 | 对齐 | 插画 | 主操作呈现 |
|---|---|---|---|
| **整页** | 整块居中或左对齐（全站统一二选一） | 可用宽插画 | 主按钮 |
| **大卡片 / 表格区** | 整块左对齐，或整体居中 | 宽图在上 | 主按钮 / 指向界面元素 |
| **小 tile / 侧栏** | 图居中、文字与按钮左对齐（Carbon 特例，防止被误认为内容跳过） | 图在上，空间小则省略 | 文字链接优先 |
| **迷你 widget（行内/标签）** | 左对齐，纯文字 | 无 | 内联链接 |

- 同屏多个空态用 **tertiary 或纯文字**（§6），空间不足只留文字（§5）；**表格空态 ≠ 全局空态**——表格区用行内对齐 + 轻插画，全局用整页居中（Ant Design 用 `ConfigProvider` 全局设置 Empty）。

---

## §9 空状态可访问性清单

- **装饰图 `alt=""`**（裁决二）：纯装饰插画/图标不进 Tab 顺序（SC 2.4.3），也不被读屏念出（SC 1.1.1）；标题用真实 `<h1>–<h6>`（Atlassian h600 级），不用 `<div>` 假标题。
- **动态与焦点**：列表从"有"变"空"时按 `conversational-generative-ui.md §5` 的 live region 契约播报一次（纯静态空态不用）；主操作失败后焦点留在可操作元素上，不丢到 `<body>`（`overlays-modality.md` 焦点契约）。
- **动效与颜色**：插画入场动画遵循 `motion-system.md §8.1` 三档降级（默认淡入，尊重 `prefers-reduced-motion`）；"空"不是错误，不用红色表达空态——红色只留给失败态，且失败态另给文案。

---

## §10 移动端 / 小程序空态

- **窄屏只留文字或小图标**：Atlassian `narrow` = 304px 以下只留文字（§5 同一决策），标题 + 说明 + 主按钮垂直堆叠；主按钮按 `direct-manipulation.md §8` 保持 24×24 含间距 / 44×44 AAA，不因空间小缩到点不到。
- **小程序**：首屏空态不叠 coach mark（`onboarding-first-run.md` 先测无引导），用零数据位（§7）或单主操作；弱网失败态必须给"重试"并说清是你的网还是我们的服务（§11）。

---

## §11 失败态 ≠ 缺省态（禁止把出错伪装成无内容）

- **失败态三件套（必须）**：① 明确"是我们的错还是你的错"（GOV.UK 口径：500 不是用户的错）；② 一句现状 + 一句下一步（"已记录，正在修复" / "请 5 分钟后重试"）；③ 至少两个出口（重试、返回首页/联系支持）。
- **不得伪装**：不用"零内容 / No data"文案，也不用"哎呀 / Oops"掩盖（`feedback-states.md §6.2` 404/500 规则）；判型命中"请求失败"才走此态。
- **可访问性**：动态出现时用 live region 播报一次（§9），焦点留在重试按钮。

---

## §12 度量：空状态有没有用（首次操作率 / 微转化）

空状态不是"写了就完"，要用数据看它有没有把人送向下一步。接 `design-measurement-research.md`：

- **首次操作率（First-Action Rate）**：看到首次空态后点击主操作的比例，是这块的北极星——比"空态曝光量"有用。
- **清除筛选率**（无结果空）与**重试率**（失败空）：分别反映筛选是否过严、排除网络抖动后的真实恢复能力。
- **样本量与护栏**：日活低时按 `design-measurement-research.md §8` 的样本量公式放大；不用多个 CTA 换首操率（§6），也不做伪进度、默认保留筛选这类 `design-ethics-inclusion.md` 红线设计。

---

## §13 自检 16 项（原「反模式 20 条」已并入此表）

1. 这个"空"是数据层给的 `200 + 空集合`，还是我用 `length===0` 猜的？403 / 5xx 有没有被我塞进空态？
2. 我判了这是哪一种空（首次/无结果/无权限/失败/完成）——去掉图标与颜色后还判得出吗？
3. 文案三项过关吗：标题正向 ≤12 字（≤6 词、句首大写）· 说明给出"将出现什么 + 怎么做"且 ≤30 字（≤1 句）· 按钮动词 + 对象 ≤6 字（≤2 词）？
4. 只给了一个主操作吗（其余降为文字链接）？
5. 任何空态都有去向，没有"死路"吗？
6. 失败空态给了原因 + 重试，且没有伪装成"暂无数据"、没有只换个红图标吗？
7. 无结果空给的是"清除筛选"而非"新建"吗？
8. 空态替换掉它该替换的元素了吗（表格连表头、表尾分页一起撤）？
9. 装饰插画首选 `alt=""`（不是 `role="presentation"`）、不进 Tab 顺序，承载信息的插画有真实 `alt` 描述吗？
10. 标题是真实 `<h*>` 而非 `<div>` 假标题吗？
11. 容器 < 304px 时省去了插画、只留文字/小图标；移动端主按钮 ≥24×24（含间距）点得到吗？
12. 同屏多个空态用 tertiary / 纯文字，避免五主按钮与五张插画吗？
13. 插画语气中性或幽默、没有负面；跨语言产品不用未本地化的隐喻吗？
14. 动态空态用 live region 播报一次（不刷屏）；骨架屏与空态不混用、加载完仍无数据才切空吗？
15. 空态动画尊重 `prefers-reduced-motion`；说明文字对比度 ≥3:1（若它是唯一状态传达）、没有用红色表达"空"吗？
16. 我有没有用首次操作率 / 清除筛选率 / 重试率度量这个空状态，而不是"写了就完"？

---

## §14 可抄代码 1 段（Python 严格模式实跑通过）

> `python -W error::SyntaxWarning` 实跑通过。只留"三态分发"这一件真会被写错的东西；文案限值见 §4 公式，度量口径见 §12。

```python
#!/usr/bin/env python3
# §14.1 三态分发：状态来自数据层，不用 length===0 猜（§2）
def empty_kind(status: str, total: int, filtered: bool) -> str:
    if status == "forbidden":
        return "无权限空"
    if status == "error":
        return "失败空"
    if status != "ok" or total:
        return "非空（照常渲染内容）"
    return "无结果空" if filtered else "首次空"

```

---

## §15 来源与取源限制

**一手核验（逐字/逐值）**：

- Ant Design Empty：`https://ant.design/components/empty` — Anatomy、API、Design Token（`colorTextDescription: rgba(0,0,0,0.45)`、`PRESENTED_IMAGE_SIMPLE`/`DEFAULT`、margin 8/16/32、内置语义 DOM root/image/description/footer）2026-11-13 逐字核验。
- Atlassian Empty state：`https://atlassian.design/components/empty-state/usage` — Anatomy（Illustration/Header/Description/Buttons）、*"Empty states can be a chance to celebrate, educate, and inform…"*、width wide 464px / narrow 304px、h600 标题、CTA imperative verbs、*"never negative"*、装饰图 alt 规则、Content guidelines 语气分级，2026-11-13 逐字核验。
- Carbon empty-states pattern（仓库源码，§2 与 J10 全部引文）：`https://raw.githubusercontent.com/carbon-design-system/carbon-website/main/src/pages/patterns/empty-states-pattern/index.mdx` — 2026-11-20 取到全文：三类划分（No data / User action / Error management + 四个 error 用例）、*"an empty state for a table would replace the table and the column headers and footer should not be present…"*、同屏多空态用 tertiary button、装饰图空 alt（*"avoid assigning role to presentation…"*）。站点渲染页 `carbondesignsystem.com/patterns/empty-states-pattern/` 30s 超时未取到，故以仓库源码为准。

**二手 / 共识（设计社区广泛引用，未逐字抓取原文）**：

- NN/g 空状态四分类（首次/用户清空/无结果/错误）与"空状态是被浪费的引导位"立场：NN/g 文章库 `https://www.nngroup.com/articles/`（本轮通过 topic 页与搜索结果确认主题存在，具体文章正文因站点 404/JS 未逐字抓取 → 取源限制）。

**取源限制（本轮未取得逐字正文，已显式标注，下轮候选补取）**：

1. **Atlassian 复取失败**：2026-11-20 重取 `atlassian.design/components/empty-state/usage` 返回 200 但正文被截断只剩导航，本轮未取到新逐字，§3/§5 的 Atlassian 引文仍以 2026-11-13 那次核验为准。
2. **Ant Design 复取失败**：2026-11-20 重取 `ant.design/components/empty` 返回 200 但正文为空（JS 渲染），token 值沿用 2026-11-13 核验。
3. **Material 3 Empty states**：`https://m3.material.io/components/empty-states/overview` 为 JS 渲染动态页，WebFetch 返回 404/动态骨架，未取解剖与规格 → 标注为取源限制（沿用 Material 1 归档口径时须显式声明）。
4. **Apple HIG Empty States**：`https://developer.apple.com/design/human-interface-guidelines/empty-states` 同样 JS 渲染返回 404，未取逐字 → 取源限制。
5. **Shopify Polaris Empty state**：`https://polaris.shopify.com/components/feedback/empty-state` 重定向到 `shopify.dev` 文档枢纽，未取到组件级逐字 → 取源限制。
6. **Baymard Institute 空购物车 / 空状态研究**：仅经搜索结果级确认主题存在，未取到报告正文数值 → 取源限制。
7. **Luke Wroblewski《Error and Empty States》**：仅经搜索结果级确认，未逐字 → 取源限制。

**下轮补取候选（接 §15 取源限制）**：Material 3 empty-states 现行静态路径、Apple HIG empty-states 正文、Baymard 空购物车报告、Luke Wroblewski 原文、NN/g 空状态具体文章 URL（本轮 404 需换路径）。
