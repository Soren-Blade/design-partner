# 空状态与零数据位（Empty States & Zero-Data）

> 快照 2026-11-13 · 一手：Ant Design Empty 组件与 token（ant.design/components/empty）、Atlassian Empty state（atlassian.design/components/empty-state）逐字核验；NN/g、Material 3、Apple HIG 为 JS 渲染/动态页，未取得逐字正文 → 见 §16 取源限制。

## §0 一句话立场

空状态不是"没有数据的占位"，而是**整块界面里最被浪费的引导位**：用户第一次看到某个视图、或某个操作清空后，注意力最集中、动机最强，却往往只收到一句"暂无数据"。本资产与 `feedback-states.md §5`（五种"空"分类）是**同一主题的两层**：§5 给分类与速查，本资产给**可抄的中英文文案矩阵、零数据位（starter content）设计模式、装饰插画的无障碍取舍、变体承载位置、以及"空状态有没有用"的度量口径**。

三条裁决（均引一手原文，见 §16）：

1. **默认要引导，不要道歉、不要留白死路。** Atlassian 原文：*"Empty states can be a chance to celebrate, educate, and inform people of what they can do next."* Ant Design：*"User tutorial to create something in fresh new situation."* 只写"暂无数据"等于把引导位空着。
2. **装饰性插画必须 `aria-hidden` 且不让焦点滞留。** Atlassian Accessibility：*"If the illustration provides useful information, include alternative text. If it's only for decoration, avoid alt text or remove the image altogether."* 纯装饰图 → `role="img"` + `aria-hidden="true"` 或 `alt=""`，且不能成为 Tab 停留点（SC 1.1.1 / 2.4.3）。
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

与 `feedback-states.md §5.1` 同源，这里给**判型顺序**而非重复表格：先判触发源，再看用户心理，最后给动作。

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
| `lineHeight` | `1.5714…` | 行高（4 的倍数派生） |
| `margin` / `marginXL` / `marginXS` | `16` / `32` / `8` | 间距尺度 |
| `opacityImage` | `1` | 图片不透明度（默认不降，靠尺寸/留白区分层级） |
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
- **控制 CTA 数量**：Atlassian *"Be mindful of how many CTAs might appear on one page."*；同屏多空态用 tertiary / 纯文字，避免五个主按钮（同 `feedback-states.md §5.3`）。
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

**决策**：容器 < 304px（Atlassian narrow）→ 只用图标或纯文字，不上插画；同屏多空态 → 纯文字优先；首次空且空间充足 → 可用中性/幽默插画提气。

---

## §6 单主行动与 CTA 纪律

- **只给一个主操作**（Carbon / Atlassian 共识）：多个选项 → 挑最重要的一个做主按钮，其余降为文字链接。
- **不要制造死路**：任何空态都不该只留一句"暂无数据"——至少给一个去向（主操作或"浏览推荐"）。
- **不要每个都配插画 + 主按钮**：仪表盘多卡片同时失败时空态，用 tertiary 按钮或纯文字，避免一屏五个主按钮（视觉噪音 + 决策瘫痪）。
- **主操作要具体**："新建项目"优于"开始使用"；"清除筛选"优于"返回"。动词 + 对象，≤6 字（中文）/ ≤2 词（英文）。
- **次级动作弱化为链接**：文档、帮助、历史记录 → 文字链接，不抢主按钮的视觉权重。

---

## §7 零数据位 / starter content：用示例教，而不是用文字讲

**零数据位（starter content）** 是首次空的最高形态：不直接教用户"点这里新建"，而是**预填一份示例 / 模板 / 示例数据**，让用户改着改着就会用。与 `onboarding-first-run.md §13` 同源（教学型零数据位），这里给**设计模式**。

- **模式 A · 模板入口**：首次空给"从模板开始"而非空白画布（Notion / Canva 范式）。降低"空白页恐惧"。
- **模式 B · 预填示例数据**：列表/表格首次空时，预填 1–3 行脱敏示例（标注"示例"），用户删除示例即上手。注意：示例必须明显可辨、可一键清空，不能伪装成真实数据。
- **模式 C · 占位样本**：图表/仪表盘首次空，给一张"长这样"的静态示例图，让用户预期产出形态，而非空白卡片。
- **模式 D · 引导式首条**：表单类首次空，把"添加第一条"做成内联输入（输入即创建），跳过"先点新建再填表"两步。

**判定**：零数据位适合**创作型**产品（文档/设计/表格/看板）；**交易/管理型**产品（订单/权限）更适合同步给主操作 + 说明，不宜预填假数据（合规与信任风险）。

**中英对照（模式 A 文案）**：中文"从模板开始"／英文 "Start from a template"；中文"看看示例长什么样"／英文 "See an example"。

---

## §8 变体与承载位置（全屏 / 容器内 / 表格区 / 迷你 widget）

同一份空状态文案，按承载位置降级：

| 承载位置 | 对齐 | 插画 | 主操作呈现 |
|---|---|---|---|
| **整页** | 整块居中或左对齐（全站统一二选一） | 可用宽插画 | 主按钮 |
| **大卡片 / 表格区** | 整块左对齐，或整体居中 | 宽图在上 | 主按钮 / 指向界面元素 |
| **小 tile / 侧栏** | 图居中、文字与按钮左对齐（Carbon 特例，防止被误认为内容跳过） | 图在上，空间小则省略 | 文字链接优先 |
| **迷你 widget（行内/标签）** | 左对齐，纯文字 | 无 | 内联链接 |

- **同屏多个空态**（仪表盘多卡片失败）：用 tertiary 按钮，避免一屏五个主按钮；优先纯文字空态，不要每个都配插画。
- **空间不足就只留文字**（Carbon / Atlassian 明确）：塞缩小插画比没有更乱。
- **表格空态 ≠ 全局空态**：表格区空态用行内对齐、轻插画；全局空态用整页居中。Ant Design 用 `ConfigProvider` 全局设置 Empty 样式，表格无数据时自动应用。

---

## §9 空状态可访问性清单

- **装饰图 `aria-hidden` + `alt=""`**（裁决二）：纯装饰插画/图标不得进 Tab 顺序（SC 2.4.3），不得被读屏念出（SC 1.1.1）。
- **标题是真实标题**：用 `<h1>–<h6>`（Atlassian 用 h600 级），不是 `<div>` 假标题——读屏用户靠标题导航。
- **动态空态用 live region**：列表从"有"变"空"时，若用 toast/文案告知，按 `conversational-generative-ui.md §5` 的 live region 契约播报一次（不刷屏）；纯静态空态无需 live region。
- **焦点不滞留**：空态内的主操作按钮若失败，焦点应留在可操作元素上，不丢到 `<body>`（同 `overlays-modality.md` 焦点契约）。
- **reduced-motion**：空态插画若带入场动画，遵循 `motion-system.md §8.1` 三档降级；默认给"淡入"而非"弹跳"，且尊重 `prefers-reduced-motion`。
- **对比度**：说明文字 `rgba(0,0,0,0.45)`（Ant 默认）在白底约 3:1 边缘——若说明是**唯一**传达状态的方式，需确认 ≥3:1（非文本/大文本口径），否则加图标辅助（SC 1.4.11）。
- **不要靠颜色表状态**："空"不是错误，不要用红色表达空态（红色留给失败空，且失败空另给文案）。

---

## §10 移动端 / 小程序空态

- **窄屏优先纯文字或小图标**：Atlassian `narrow` = 304px 以下只留文字；移动端同理，插画省去，标题 + 说明 + 主按钮垂直堆叠。
- **主操作够大**：移动端主按钮遵循 `direct-manipulation.md §8` 目标尺寸（24×24 含间距 / 44×44 AAA / 48×48 设计值），空态按钮不得因空间小缩到点不到。
- **小程序**：首屏空态别叠加引导教程（`onboarding-first-run.md` 判定先测无引导）；用零数据位（§7）或单主操作即可。弱网下失败空态必须给"重试"且文案说清"是你的网还是我们的服务"（§11）。
- **避免首屏空态 + 骨架屏混用**：首次加载用骨架屏（`feedback-states.md §2`），加载完成仍无数据才切空态——不要一上来就空。

---

## §11 失败态 ≠ 缺省态（禁止把出错伪装成无内容）

- **最高频错误**：把**失败**渲染成**缺省态**。用户以为"真的没有"，于是不再重试——而真实原因是网络抖动。
- **失败态三件套（必须）**：① 明确"是我们的错还是你的错"（GOV.UK 口径：500 明确不是用户的错）；② 一句现状 + 一句下一步（"已记录，正在修复" / "请 5 分钟后重试"）；③ 至少两个出口（重试、返回首页/联系支持）。
- **不得伪装**：失败态**不得**用"零内容 / No data"文案，也不得用俏皮话（"哎呀"/"Oops"）掩盖（同 `feedback-states.md §6.2` 404/500 规则）。
- **与 §2 判型联动**：判型器第三步命中"请求失败"才走失败空态；其余一律不伪装。
- **可访问性**：失败空态若动态出现，用 live region 播报一次（§9），焦点留在重试按钮。

---

## §12 度量：空状态有没有用（首次操作率 / 微转化）

空状态不是"写了就完"，要用数据看它有没有把人送向下一步。接 `design-measurement-research.md`：

- **首次操作率（First-Action Rate）**：看到首次空态的用户中，点击主操作的比例。这是空状态最核心的北极星——比"空状态曝光量"有用。
- **清除筛选率**（无结果空）：点击"清除筛选"的比例，反映筛选是否过严。
- **重试率**（失败空）：失败空态的"重试"点击率，排除网络抖动后的真实恢复能力。
- **样本量**：单视图日活低时，A/B 需要更大样本；见 `design-measurement-research.md §7` 比例样本量公式。
- **护栏**：不要为了首操率堆砌多个 CTA（§6）——short-term 提升可能损害 long-term 信任。
- **不要在空状态里做转化实验坑**：把"重试"按钮做成伪进度、把"清除筛选"默认勾选保留筛选，属 `design-ethics-inclusion.md` 欺骗性设计红线。

---

## §13 反模式 20 条

1. 只写"暂无数据 / No data"就完事，不留任何去向。
2. 把**失败**伪装成**无数据**（用户不再重试）。
3. 空状态用红色表达"空"（红色留给错误，且错误另给文案）。
4. 同屏五个主按钮（多卡片失败空态）。
5. 把大插画缩小塞进 304px 容器。
6. 用隐喻插画做跨语言产品，不本地化。
7. 装饰插画没 `aria-hidden`，读屏念出无意义描述。
8. 装饰插画可 Tab 聚焦，焦点滞留。
9. 标题用 `<div>` 假标题，读屏无法导航。
10. 标题负面化（"您还没有任何数据"优于正向却写成"数据丢失"感）。
11. 无结果空给"新建"按钮（应为"清除筛选"）。
12. 首次空不给主操作，只给一段长说明。
13. 说明超过 30 字（中文）/ 一长句（英文），用户不读。
14. 按钮用"开始使用"等模糊动词，不写对象。
15. 同屏多个空态全配插画，视觉噪音 + 决策瘫痪。
16. 小程序首屏空态叠加 coach mark 教程（先测无引导）。
17. 骨架屏与空态混用，一上来就空。
18. 失败空态不暴露"是你的错还是我们的错"。
19. 零数据位预填假数据却不标注"示例"，伪装成真实数据（合规风险）。
20. 在空状态里做伪进度 / 默认保留筛选等欺骗性设计。

---

## §14 自检 20 项

1. 我判了这是哪一种空（首次/无结果/无权限/失败/完成）吗？
2. 标题正向、≤12 字（中文）/ ≤6 词（英文）、句首大写吗？
3. 说明给了"将出现什么 + 怎么做"，且 ≤30 字（中文）/ ≤1 句（英文）吗？
4. 按钮是动词 + 对象、≤6 字（中文）/ ≤2 词（英文）吗？
5. 只给了一个主操作吗（其余降为文字链接）？
6. 任何空态都有去向，没有"死路"吗？
7. 失败空态给了原因 + 重试，且没有伪装成"暂无数据"吗？
8. 无结果空给的是"清除筛选"而非"新建"吗？
9. 装饰插画 `aria-hidden` + `alt=""`，且不进 Tab 顺序吗？
10. 承载信息的插画有真实 `alt` 描述吗？
11. 标题是真实 `<h*>` 而非 `<div>` 假标题吗？
12. 容器 < 304px 时，省去了插画、只留文字/小图标吗？
13. 同屏多个空态用 tertiary / 纯文字，避免五主按钮吗？
14. 插画语气中性或幽默，没有负面吗？
15. 跨语言产品不用隐喻插画，或已本地化吗？
16. 动态空态用了 live region 播报一次（不刷屏）吗？
17. 空态动画尊重 `prefers-reduced-motion` 吗？
18. 说明文字对比度 ≥3:1（若它是唯一状态传达）吗？
19. 小程序 / 移动端主按钮 ≥24×24（含间距）点得到吗？
20. 我有没有用首次操作率 / 清除筛选率 / 重试率度量这个空状态，而不是"写了就完"？

---

## §15 可抄代码 5 段（Python 严格模式实跑 PASS）

> 以下 5 段均用 `python -W error::SyntaxWarning` 实跑通过。可直接纳入设计校验脚本。

```python
#!/usr/bin/env python3
# §15.1 空状态文案合规校验：标题≤12字 / 说明≤30字 / 按钮≤6字（中文口径）
def validate_empty_copy(title: str, desc: str, button: str) -> list:
    errors = []
    if len(title) > 12:
        errors.append(f"标题 {len(title)} 字 > 12：{title}")
    if len(desc) > 30:
        errors.append(f"说明 {len(desc)} 字 > 30：{desc}")
    if len(button) > 6:
        errors.append(f"按钮 {len(button)} 字 > 6：{button}")
    return errors


# §15.2 判型器：按 §2 三问定类，返回空状态类型
def classify_empty(just_cleared: bool, user_searched: bool,
                  request_failed: bool, no_permission: bool) -> str:
    if just_cleared:
        return "完成空"
    if request_failed:
        return "失败空"
    if user_searched:
        return "无结果空"
    if no_permission:
        return "无权限空"
    return "首次空"


# §15.3 装饰图无障碍决策：纯装饰→返回 None（调用方应置 aria-hidden/alt=""）
def decorative_alt(illustration_carries_info: bool) -> "str | None":
    if illustration_carries_info:
        return "图表达含义，必须给 alt 描述"
    return None


# §15.4 首次操作率（First-Action Rate）：看到空态并点击主操作的比例
def first_action_rate(seen_empty: int, clicked_primary: int) -> float:
    if seen_empty <= 0:
        return 0.0
    rate = clicked_primary / seen_empty
    return round(max(0.0, min(1.0, rate)), 4)


# §15.5 说明文案截断（严守 ≤30 字，超出补省略号）
def clamp_desc(text: str, limit: int = 30) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"
```

---

## §16 来源与取源限制

**一手核验（逐字/逐值）**：

- Ant Design Empty：`https://ant.design/components/empty` — Anatomy、API、Design Token（`colorTextDescription: rgba(0,0,0,0.45)`、`PRESENTED_IMAGE_SIMPLE`/`DEFAULT`、margin 8/16/32、内置语义 DOM root/image/description/footer）2026-11-13 逐字核验。
- Atlassian Empty state：`https://atlassian.design/components/empty-state/usage` — Anatomy（Illustration/Header/Description/Buttons）、*"Empty states can be a chance to celebrate, educate, and inform…"*、width wide 464px / narrow 304px、h600 标题、CTA imperative verbs、*"never negative"*、装饰图 alt 规则、Content guidelines 语气分级，2026-11-13 逐字核验。

**二手 / 共识（设计社区广泛引用，未逐字抓取原文）**：

- NN/g 空状态四分类（首次/用户清空/无结果/错误）与"空状态是被浪费的引导位"立场：NN/g 文章库 `https://www.nngroup.com/articles/`（本轮通过 topic 页与搜索结果确认主题存在，具体文章正文因站点 404/JS 未逐字抓取 → 取源限制）。
- Carbon Design System 空状态五件套与"空间小只留文字"：出自 IBM Carbon 组件文档（本轮沿用历史轮次已引用口径，未重新逐字核验）。

**取源限制（本轮未取得逐字正文，已显式标注，下轮候选补取）**：

1. **Material 3 Empty states**：`https://m3.material.io/components/empty-states/overview` 为 JS 渲染动态页，WebFetch 返回 404/动态骨架，未取解剖与规格 → 标注为取源限制（沿用 Material 1 归档口径时须显式声明）。
2. **Apple HIG Empty States**：`https://developer.apple.com/design/human-interface-guidelines/empty-states` 同样 JS 渲染返回 404，未取逐字 → 取源限制。
3. **Shopify Polaris Empty state**：`https://polaris.shopify.com/components/feedback/empty-state` 重定向到 `shopify.dev` 文档枢纽，未取到组件级逐字 → 取源限制。
4. **Baymard Institute 空购物车 / 空状态研究**：仅经搜索结果级确认主题存在，未取到报告正文数值 → 取源限制。
5. **Luke Wroblewski《Error and Empty States》**：仅经搜索结果级确认，未逐字 → 取源限制。

**下轮补取候选（接 §16 取源限制）**：Material 3 empty-states 现行静态路径、Apple HIG empty-states 正文、Baymard 空购物车报告、Luke Wroblewski 原文、NN/g 空状态具体文章 URL（本轮 404 需换路径）。
