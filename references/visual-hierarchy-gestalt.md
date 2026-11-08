# 视觉层级与格式塔组织律（Visual Hierarchy & Gestalt / Attention & Cognitive Load）

> 快照 2026-11-08 · 24 节 · 12 场景 · 20 反模式 · 20 自检 · 5 段可抄代码（3 段 Python 已实跑）

把「标题放大加粗、主色块放在上面、内容分个组」变成**有原文依据、有顺序契约、能验收的注意力分配决策**。本文件不替代 `editorial-layout.md §8`（版面的 Z/F 路径与视觉重量表）/`typography-system.md`（字号与行高的可访问性契约）/`color-science.md`（对比度计算）/`accessibility.md`（WCAG 全档阈值）/`navigation-ia.md`（信息架构与项数）/`shape-elevation.md`（形与层的几何）/`design-ethics-inclusion.md`（dark pattern）/`iconography.md`（图标语义），而是补上它们都在**用**、却没人讲清楚底层机制的第四根基础支柱：**人怎么把元素看成一组（组织）、目光按什么顺序走（引导）、这套顺序要花多少心智（负荷），以及视觉顺序与代码顺序不一致时会伤到谁**。

**一句话立场**：视觉层级不是「把重要的东西放大」，是**注意力的分配契约**——格式塔决定用户**先看到什么被归为一组**，扫描模式决定用户**接下来往哪走**，认知负荷决定用户**走不走得完**；而前三者必须同时兑现为 DOM 阅读顺序、键盘焦点顺序与标题结构，否则视觉上的「清楚」对读屏与键盘用户是**结构性失真**，不是品味差异。

**本轮三条最重要裁决**（后文逐条给官方原文、公式与验收动作）：

1. **F 型不是设计目标，是缺少强引导时的默认最低成本扫描**。NN/g 原文：*"The F-pattern is the default pattern when there are no strong cues to attract the eyes towards meaningful information."* 以及 *"In the absence of any signals to guide the eye, they will choose the path of minimum effort and will spend most of their fixations close to where they start reading"*。把 F 型当版式模板去「设计」是本末倒置；要做的是给足引导信号（标题、分组、留白、单一起点），让目光不必用最低成本路径兜底。原文同时列出 F 之外的多种扫描模式，F 只是其中之一。
2. **视觉层级必须同时落在三条顺序上，视觉呈现本身不构成结构**。W3C WCAG 2.2：SC 1.3.2（Level A）要求 *"a correct reading sequence can be programmatically determined"*，充分技术含 **C27: Making the DOM order match the visual order**，失败例 **F1** 是 *"changing the meaning of content by positioning information with CSS"*；SC 2.4.3（Level A）要求 *"focusable components receive focus in an order that preserves meaning and operability"*；SC 2.4.10（Level AAA）Intent 逐字写明 *"visual presentation is not sufficient to identify document sections"*，另有 SC 2.4.6（Headings and Labels，Level AA）要求 *"Headings and labels describe topic or purpose"*。所以「大标题 + 卡片分区」只是视觉层，**没有 `<h2>`、没有 DOM 顺序、没有焦点顺序就没有层级**。
3. **7±2 不是导航项数上限，认知负荷要拆三类分别处理**。Laws of UX Miller's Law 的第一条 Takeaways 逐字是 *"Don't use the 'magical number seven' to justify unnecessary design limitations."*；认知负荷理论（Sweller，1988 论文 *"Cognitive Load Theory, Learning Difficulty, and Instructional Design"*）把负荷分为 intrinsic / extraneous / germane。同理，Hick–Hyman `RT = a + b·log₂(n+1)` 的 `log₂` 隐含**用户能按分类树逐层排除**；随机无序菜单需要线性扫描，此时公式不适用，别拿「对数增长所以多放几项没关系」当挡箭牌。

**边界声明**：本文件管「分组、顺序、注意力、决策成本」的机制与验收；具体字号数值归 `typography-system.md`；颜色与 3:1 / 4.5:1 计算归 `color-science.md §6` 与 `accessibility.md §2`；版式网格与视觉重量排序归 `editorial-layout.md §8`；导航项数与深度广度归 `navigation-ia.md`；圆角阴影归 `shape-elevation.md`；诱导性设计归 `design-ethics-inclusion.md`。**本文件不生产新的「XX px / XX 项」魔法数**，只生产可复现的判断规则与一致性检查。

---

## 1 · 为什么单列视觉层级与格式塔

圆角、阴影、字号、色彩都已有独立资产，唯独「用户先看哪、看完往哪走、走完累不累」始终散在边角。缺口用 `dp_search.py` 与全域词频统计判定为**结构性空白**而非覆盖不足。

**缺口实测**（本轮 `python scripts/dp_search.py "格式塔 完形 组织律"` / `"视觉层级 视觉动线 F 模式 Z 模式 眼动"` / `"认知负荷 注意力 希克定律 米勒定律"` + `grep -ril` 全域统计）：`格式塔=0`、`Gestalt=0`、`邻近性=0`、`闭合性=0`、`希克定律=0`、`Fitts=0`、`菲茨=0`、`视觉层次=0`，`视觉层级=1`（且仅出现在 `shape-elevation.md §1` 的「下轮候选缺口」自述里）。三条查询的命中集中在四类边角：`editorial-layout.md §8`（Z 型 / F 型 / 单点式三行路径 + 视觉重量排序）、`navigation-ia.md`（项数铁律里引用米勒 7±2）、`design-ethics-inclusion.md`（"情境性认知负荷正是 dark pattern 的作用面" 一句）、`iconography.md`（"图标 + 文字降低认知负荷" 一行）。

上游文件都在**用**层级，没人讲**它为什么成立、什么时候失效、怎么与代码顺序对齐、怎么用公式估决策成本**。缺了这一层，「主标题再大一点」就永远是一条没有理由的口诀——放大到所有元素都"重要"等于没有层级；用 CSS `order` 把主内容挪到上面，读屏用户却仍从侧栏开始读；用 7±2 论证导航只能放 7 项，而 Miller 1956 讲的是即时记忆广度不是菜单容量。

**与前三根支柱的对照**：色彩有 OKLCH 这套可计算坐标，排印有一组不可协商的边界，形状与深度有一组几何硬约束；层级同样没有"唯一正确的 1.5 倍字号"，但有**一组组织律 + 一组顺序契约 + 一组决策成本公式**。越界是缺陷，不是审美分歧。

---

## 2 · 三层模型：先判层，再谈放大加粗

任何「重点不突出 / 信息太乱 / 用户找不到」的问题，先判落在哪一层，不要一上来就改字号。

| 层 | 回答的问题 | 机制 | 典型失效 | 主武器 | 本文件 |
|---|---|---|---|---|---|
| **L1 组织** | 用户把哪些元素看成**一组**？ | 格式塔组织律、前注意特征 | 该分组的没分组、不该分组的被框在一起 | 间距比 / 共同区域 / 相似 token / 对齐轴 | §7 §8 §9 |
| **L2 引导** | 目光**按什么顺序**走？ | 扫描模式、视觉重量、顺序契约 | 没有唯一起点、DOM/焦点/视觉三顺序打架 | 标题结构、单一焦点、DOM 顺序、焦点顺序 | §3 §4 §5 §6 §17 |
| **L3 负荷** | 用户**走不走得完**？ | 认知负荷、决策时间、工作记忆 | 选项过载、目标太小、信息一次给完 | 分块、渐进披露、目标尺寸、减少外在负荷 | §11–§16 |

**判层口诀**：先问「是不是分组错了」（眯眼看有哪些团块）→ 再问「是不是顺序错了」（第一眼落在哪、Tab 键落到哪）→ 最后才问「是不是太费脑」（选项数、目标尺寸、一次要记几件事）。**L1 错了改间距与容器，L2 错了改结构与顺序，L3 错了改选项与目标**；三层都用"加大字号"处理，必然把 L1/L3 的问题推给 L2，越改越乱。

---

## 3 · 裁决一：F 型是默认行为，不是设计目标

**来源**：NN/g *F-Shaped Pattern of Reading on the Web: Misunderstood, But Still Relevant (Even on Mobile)*，Kara Pernice，2017-11-12（最后审阅 2026-08-19）；原始 2006 研究 *F-Shaped Pattern For Reading Web Content*。原文：*"Among NN/G's contributions to the world of UX, perhaps one of the most cited is the F-shaped reading pattern for web content, which we identified in 2006."*、*"Eleven years after discovering this pattern, we revisit what it means today."*

**两条必须逐字记住的原文**：

> "The F-pattern is the default pattern when there are no strong cues to attract the eyes towards meaningful information."

> "In the absence of any signals to guide the eye, they will choose the path of minimum effort and will spend most of their fixations close to where they start reading (which is usually the top left most word on a page of text)."

**推论（可直接写进评审意见）**：

- F 型是**缺引导时用户自己选的省力路径**，不是设计稿要主动复刻的 Z/F 骨架。把「我们是 F 型布局」当设计理由，等于承认页面没有强引导信号。
- 想让用户读到第三屏，靠的是**每段开头的可扫读信号**（描述性标题、首句承载结论、列表项同构、加粗只给关键词），不是把左边一栏做得更宽。
- "F 型已死"也是误读。原文：*"Our recent eyetracking research shows that the F-shaped scanning pattern is alive and well in today's world — both on desktop and on mobile."* 并给出移动端 F 型实例（横向滑动读宽栏时仍成立）。
- **RTL 要翻转，不要镜像复用**：*"in right-to-left languages such as Arabic, people read in a flipped F-shaped pattern"* / *"The F-pattern is mirrored in right-to-left languages"*。阿拉伯语等 RTL 版面的起点在右上，左侧竖扫变成右侧竖扫；`dir="rtl"` 不止是文字方向，**视觉动线也要跟着换**。
- 原文另提到用户扫到更深处时会 *"so the pattern comes to resemble an E"*——注意文章**只说"像 E"，没有正式命名 E-pattern**，也没有使用 zigzag 一词，别在文档里造名词。

**与 `editorial-layout.md §8` 的分工**：那一节给的是**平面设计/版式**里 Z 型、F 型、单点式三种路径的适用面（少内容落地页 / 内容型页面 / 海报），是构图选择；本节的 F 型是**眼动实证里的默认行为**，是诊断结论。前者回答"我想让目光怎么走"，后者回答"没引导时目光实际怎么走"。两者不冲突，但不能互相顶替。

---

## 4 · 扫描模式全表：F 只是其中一种

NN/g 2017 原文命名/描述的模式（逐项核对，未标"命名"的是描述性表述）：

| 模式 | 原文措辞 | 行为 | 设计含义 |
|---|---|---|---|
| **F-shaped pattern** | `F-shaped pattern` / `F-pattern` | 顶部横扫 → 左侧竖扫 → 局部横扫 | 无强引导时的默认省力路径；不是目标 |
| **E 形变体** | *"so the pattern comes to resemble an E"* | 用户扫得更深，底部又出现一次横扫 | **文章未正式命名 E-pattern**，只作描述 |
| **Layer-cake pattern** | `Layer-cake pattern` | 逐层只看标题行，跳过正文 | 标题必须能独立承载信息，否则整层被跳过 |
| **Spotted pattern** | `Spotted pattern` | 目光在页面上跳着找特定词/锚点 | 需要一致的可扫读锚点（图标、加粗关键词、稳定位置） |
| **Marking pattern** | `Marking pattern` | 目光沿固定位置反复回到同一区域 | 关键控件位置要稳定，别随滚动/断点乱跳 |
| **Bypassing pattern** | `Bypassing pattern` | 整块跳过某类内容（常见广告/侧栏） | 被跳过的区域不要放主操作或必读信息 |
| **Commitment pattern** | `Commitment pattern` | 用户决定读下去后几乎逐字读 | 长文正文要保证行宽与行高，别只为扫描优化 |
| **RTL flipped F** | `flipped F-shaped pattern` / *"mirrored in right-to-left languages"* | 阿拉伯语等 RTL 下左右镜像 | `dir="rtl"` 时重排视觉起点与竖扫侧 |
| **移动端 F** | `F-pattern on mobile` | 宽栏横向滑动时仍呈 F | 不是独立新命名模式，是 F 在窄屏的实例 |

**用法**：这张表是**诊断表**不是模板库。评审时先问「用户实际会落在哪种模式」，再问「这种模式被跳过的区块里有没有必读内容」。若答案是"有"，改的是结构（标题、分组、顺序），不是把字号再放大一档。

---

## 5 · 裁决二：四条 WCAG 准则构成的顺序契约

视觉层级若只存在于渲染结果里，对读屏与键盘用户就不存在。以下四条均取自 W3C WAI《Understanding WCAG 2.2》原文。

### 5.1 SC 1.3.2 Meaningful Sequence（Level A）

> "When the sequence in which content is presented affects its meaning, a correct reading sequence can be programmatically determined."

Intent 关键句：*"A sequence is meaningful if the order of content in the sequence cannot be changed without affecting its meaning."*；*"There may be more than one order that is 'correct'"*；*"Only one correct order needs to be provided."* 另明确：HTML 中 **text 永远是 meaningful sequence，tables 与 ordered lists 是，unordered lists 不是**；主内容区与导航区的相对顺序**不影响意义**，所以二者谁先谁后都能达标。

- 充分技术：**G57**（按有意义顺序排列内容）、**C27: Making the DOM order match the visual order**、**C6**（基于结构标记定位）、H34/H56（双向文字）、PDF3。
- 失败例：**F1**（用 CSS 定位改变内容含义）、F49（线性化后无意义的布局表格）、F32/F33/F34（用空格字符排版）。
- 原文 Example 2 特别给出**可通过**的情形：用 CSS 定位导航/主文/侧栏，视觉顺序与程序顺序不一致，**但页面意义不依赖区块顺序**。所以 1.3.2 不是"视觉顺序必须等于 DOM"，而是"**意义依赖顺序时，必须有一条可被程序读出的正确顺序**"。

### 5.2 SC 2.4.3 Focus Order（Level A）

> "If a web page can be navigated sequentially and the navigation sequences affect meaning or operation, focusable components receive focus in an order that preserves meaning and operability."

Intent 关键句：*"Focus order does not necessarily need to follow the visual layout of the web page, as long as the order in which elements receive focus is logical, and the hierarchy and relationship of content implied by the visual presentation is preserved."*；*"The focus order may not be identical to the programmatically determined reading order (see Success Criterion 1.3.2 Meaningful Sequence) as long as the user can still understand and operate the web page."*；*"Care should be taken so that the focus order makes sense to both of these sets of users and does not appear to either of them to jump around randomly."*（两类用户：screen reader user 与 sighted keyboard user）

- 原文点明：*"If no scripting or `tabindex` attributes are used, the navigation order is the order that components appear in the content stream."* —— **DOM 顺序天然就是焦点顺序**，这是最省事的正确做法。
- 充分技术：G59、**C27**、SCR26（动态内容插到触发元素之后）、SCR27（用 DOM 重排区块）、PDF3。
- 该准则**不规定谁该获得焦点**，只评顺序；但原文仍建议避免把不可操作元素做成可聚焦项（*"likely to make operation tedious for keyboard users"*）。

### 5.3 SC 2.4.6 Headings and Labels（Level AA）

> "Headings and labels describe topic or purpose."

Intent：描述性标题/标签帮助用户理解信息与其组织、各部分关系、组件用途。**该准则不要求必须提供标题或标签**：正确标记由 1.3.1 覆盖，输入标签由 3.3.2 覆盖，可访问名称由 4.1.2 覆盖。也就是说——**有了 `<h2>` 还得写得出它讲什么**，"章节一 / 更多信息"不达标。

### 5.4 SC 2.4.10 Section Headings（Level AAA）

> "Section headings are used to organize the content."

Note 1：*"'Heading' is used in its general sense and includes titles and other ways to add a heading to different types of content."*；Note 2：覆盖**文字内容里的分节**，UI 组件归 4.1.2。Intent 逐字：*"Other page elements may complement headings to improve presentation (e.g., horizontal rules and boxes), but visual presentation is not sufficient to identify document sections."* —— 这是「卡片 + 分隔线 ≠ 层级结构」的直接规范依据。列 AAA 的原因是**不能适用于所有内容**（如转载既有文档、长信件），不是因为它不重要。充分技术：G141、H69。

### 5.5 四条准则的分工表

| 准则 | 级别 | 管什么 | 不管什么 | 视觉层级的落点 |
|---|---|---|---|---|
| 1.3.2 Meaningful Sequence | A | 意义依赖顺序时有一条可程序判定的正确阅读顺序 | 与视觉顺序是否逐像素一致 | DOM 顺序 / 线性化后仍读得通 |
| 2.4.3 Focus Order | A | 可聚焦组件的焦点顺序保意义与可操作性 | 哪些元素该可聚焦 | 不用正 `tabindex`、不用 JS 乱跳焦点 |
| 2.4.6 Headings and Labels | AA | 标题/标签描述主题或用途 | 是否必须存在标题/标签 | 标题文案本身要可扫读 |
| 2.4.10 Section Headings | AAA | 分节要有标题来组织内容 | UI 组件（归 4.1.2）、不适用所有内容类型 | `<h2>/<h3>` 层级树与视觉分区一一对应 |

---

## 6 · 三顺序一致性验收：DOM / 焦点 / 标题树

**核心检查**：同一个页面，把三份「顺序」分别导出，看是否指向同一个故事。

| 顺序 | 怎么导出 | 典型破坏手法 | 判定 |
|---|---|---|---|
| **DOM 阅读顺序** | 禁用 CSS（或读屏器线性模式）后从上到下读 | `order: -1`、`flex-direction: row-reverse`、`position: absolute` 搬移、表格布局 | 与视觉顺序不一致且**意义依赖顺序** → F1 / 1.3.2 失败 |
| **键盘焦点顺序** | 从头按 Tab，记录落点 | `tabindex="5"` 等正值、JS 强制 `focus()` 跳走、视觉上在左但 DOM 在右 | 出现"随机跳" → 2.4.3 失败 |
| **标题结构顺序** | 抽取 `h1→h2→h3` 大纲 | 用 `<div class="title">` 冒充标题、`h1→h3` 跳级、一页多个 `h1` | 视觉分区在标题树里找不到 → 2.4.10 不成立 |

**四条可执行规则**：

1. **优先让 DOM 顺序 = 视觉顺序**（C27）。想让主内容在视觉上先出现，就在 HTML 里先写主内容，再用 CSS 把侧栏放到右边；不要反过来先写侧栏再用 `order: -1` 搬主内容。
2. **禁止正 `tabindex`**。原文在无脚本无 `tabindex` 时焦点顺序 = content stream 顺序，这是唯一不需要维护的正确答案；`tabindex="-1"` 只用于程序化聚焦，`tabindex="0"` 只用于让自定义控件进入自然顺序。
3. **标题树不许跳级**，且视觉上每个"分区块"都能在标题树里找到对应节点。分隔线、卡片、色块只能**补充**标题（2.4.10 Intent 逐字），不能替代。
4. **RTL 与响应式各验一遍**：`dir="rtl"` 时起点翻转（§3），断点重排后 DOM 顺序不变但视觉顺序变了，必须重新确认"C27 是否仍成立"。

**反例（F1 的典型形态）**：视觉上是「主操作 → 说明 → 次要链接」，HTML 写成「次要链接 → 主操作 → 说明」再用 Grid `order` 搬位；关闭 CSS 后读屏先读次要链接，且流程性内容被拆散 → 意义依赖顺序，1.3.2 失败。修法是改 HTML 顺序，不是加 `aria-*` 打补丁。

---

## 7 · 格式塔 12 条组织律全表（IxDF 逐条核对）

**来源**：Interaction Design Foundation《The Gestalt Principles》（页面标注 updated 2026）。原文：*"Gestalt" is German for "unified whole"*；由 Max Wertheimer、Kurt Koffka、Wolfgang Köhler 在 **1920s** 创立；*"There are more than ten overlapping principles."*；Koffka 名言是 *"The whole is other than the sum of the parts."*（**不是** "greater than"，原文特意区分：整体与部分**不同**、甚至可能完全无关）。

| # | 原则 | IxDF 定义要点（原文摘译） | 界面落点 | 失效信号 |
|---|---|---|---|---|
| 1 | **Emergence** | 从一堆斑点里直接认出斑点狗；整体先于局部涌现 | 首屏用一个可整体识别的构型（品牌符号、主视觉），不要先堆零件 | 用户说"看不出这是什么" |
| 2 | **Closure / Reification** | *"We prefer complete shapes, so we automatically fill the gaps"*；IBM 条纹、WWF 熊猫 | 图标/进度/裁切图形可留缺口，但**缺口不能落在需要精确辨识的语义上** | 闭合补出的形状与真实状态不符 |
| 3 | **Common Region** | *"We perceive elements that are in the same closed region as one group"*；Facebook 帖子的赞/评在同一边界内 | **最强的分组信号**：卡片、描边、底色块；一个区域内只放一组 | 卡片里塞了两组无关信息 |
| 4 | **Continuity / Continuation** | 目光沿连续路径走，*"even if an obstacle hides it"* | 对齐轴、列表分隔线、进度条；中间被遮挡也要保持方向 | 对齐轴频繁错位，目光被打断 |
| 5 | **Proximity** | *"We group closer-together elements, separating them from those farther apart"* | 组内间距 < 组间间距（§8 给可验收比值） | 标签离了输入框、标题贴到上一组 |
| 6 | **Multistability** | Necker 立方、"我的妻子与岳母"：两种解释来回切换，*"We cannot see the multiple versions simultaneously"* | **禁止**把关键状态做成歧义图（同形状既可点又不可点） | 用户来回改口"这到底是…" |
| 7 | **Figure/Ground** | Rubin's Vase；*"we see its foreground first"*；明暗主题反转后仍能识别 | 前景/背景要有稳定对比，弹窗遮罩是典型 figure/ground | 卡片与背景对比太弱，边界消失 |
| 8 | **Invariance** | 旋转、位移、缩放、拉伸、光照变化下仍认得同一形状 | 图标在不同尺寸/主题下保持同一骨架，别换造型 | 小尺寸换成另一套图标 |
| 9 | **Prägnanz** | *"the human tendency to simplify complexity"*；看到奥运五环是五个圆而不是 C 形与透镜 | 用矩形/圆等简单形；元素数量与形状种类都要收敛 | 装饰形状比信息形状还复杂 |
| 10 | **Similarity** | 共享表面特征即被视为一组；所有按钮同款、所有链接同款 | 同一语义用同一 token，别靠位置猜"这也是按钮" | 同类控件长得不一样 |
| 11 | **Symmetry and Order** | 对称排列更易被看成一组；*"Grid systems that evenly divide the space"* | 网格与居中对齐；但**对称不等于层级**，需另给主次 | 全页对称导致没有起点 |
| 12 | **Common Fate** | 同方向/同步运动的元素被归为一组；*"Visuals need not be moving"*，箭头与旋转角也可指示 | 手风琴同向箭头、同步展开/折叠、同向动画 | 一组元素各自乱动、方向不一致 |

IxDF 的结论句可直接作为评审口径：*"When you design interfaces, users must be able to understand what they see—and find what they want—at a glance."* 以及 *"you should never confuse or delay users"*。

**Laws of UX 侧的同源条目**（站点首页逐字）：Law of Proximity *"Objects that are near, or proximate to each other, tend to be grouped together."*；Law of Similarity *"The human eye tends to perceive similar elements as a complete picture, shape, or group, even if those elements are separated."*；Law of Common Region *"Elements tend to be perceived into groups if they are sharing an area with a clearly defined boundary."*；Law of Prägnanz *"People will perceive and interpret ambiguous or complex images as the simplest form possible, because it is the interpretation that requires the least cognitive effort of us."*；Law of Uniform Connectedness *"Elements that are visually connected are perceived as more related than elements with no connection."*。两套命名不完全重合，别当成同一张清单互相补全。

---

## 8 · 组织律里可验收的四个部分

格式塔常被讲成"看图说话"，但其中四条能落成**可检查的构型规则**。以下比值是**本知识库的工程约定**（便于评审时有一致口径），**不是实验测得的感知常数**，不要当研究结论引用。

| 组织律 | 可检查的构型 | 工程约定（自定，非实验值） | 检查方式 |
|---|---|---|---|
| Proximity | 组内间距 `g_in`、组间间距 `g_out` | `g_in × 1.5 ≤ g_out` | 量设计稿/Computed CSS 的相邻 margin/padding |
| Common Region | 同一闭合边界内的元素集合 | 一个边界内只承载**一组**语义；跨组必须换边界或换底色 | 数每个卡片里的语义组数 |
| Similarity | 同一语义 token 复用率 | 同语义控件共用同一组 type/color/shape token，零"长得像但不是" | 扫组件库 variant 表 |
| Continuity | 对齐轴数量 | 一个视图主对齐轴 ≤2（主内容轴 + 辅助轴） | 截图叠辅助线数轴 |

**三条可复现的验收动作**：

1. **间距比检查**：导出一组列表项的 `margin-bottom` 与组与组之间的 `margin-top`，若组间没有明显大于组内（约定 1.5×），分组就只存在于设计稿标注里，用户看不到。用 §23.5 的脚本跑。
2. **眯眼测试**：把界面模糊/缩到 25%，只看还剩几个"团块"和哪一块最重。若团块数与预期分组数不一致，问题在 L1，改字号没用。IxDF 的 Emergence 与 Figure/Ground 都支持这一点；`editorial-layout.md §8` 的视觉重量排序（人脸/眼睛 > 高对比色块 > 大字号 > 深色块 > 图形 > 细线 > 留白）可用于解释「为什么这一块最重」。
3. **单焦点检查**：`editorial-layout.md §8` 的硬规则是"一张图只允许一个最重元素"。本文件补一条：**一个视图只允许一个主操作承载"最重"**，其余按钮用次级样式；两个并排同款主按钮会触发 Multistability 式的来回选择，属于 L1 缺陷。

**边界**：这里讲的是**构型**，不是圆角或阴影值（归 `shape-elevation.md`），也不是色值（归 `color-science.md`）。Common Region 的"边界"若需要满足 3:1 非文本对比，按 `accessibility.md §2` / `shape-elevation.md §5 §6` 处理——**阴影不能当边界**。

---

## 9 · 前注意属性：为什么"单特征差异"才会 pop-out

**来源**：Wikipedia《Feature integration theory》，Anne Treisman 与 Garry Gelade **1980**，原始论文 *"A feature-integration theory of attention"*, Cognitive Psychology **12**(1), 97–136。原文定义：特征 *"registered early, automatically, and in parallel, while objects are identified separately"* 并在稍后阶段处理。

- **前注意阶段**（原文 *"According to Treisman, the first stage of the feature integration theory is the preattentive stage."*）：*"During this stage, different parts of the brain automatically gather information about basic features (colors, shape, movement, size) that are found in the visual field."* 该过程发生在意识到对象之前：*"we are not aware of this process because it occurs early in perceptual processing"*。feature maps 里还列出 *"color, shape, orientation, sound, and movement"*。
- **聚焦注意阶段**：*"The second stage of feature integration theory is the focused attention stage, where a subject combines individual features of an object to perceive the whole object."*；*"Combining individual features of an object requires attention"*；选中的位置来自 "master map of locations"，绑定后存入 "object files"。
- **两类搜索**（设计上最关键的一条）：*"Feature searches can be performed fast and pre-attentively for targets defined by only one feature, such as color, shape, perceived direction of lighting, movement, or orientation."* / *"Features should 'pop out' during search"*；而 *"conjunction searches occur with the combination of two or more features and are identified serially"*、*"Conjunction search is much slower than feature search and requires conscious attention and effort."* Treisman 在多项实验中确认 **color、orientation、intensity** 可用于 feature search。
- **实验证据**（逐字数据，避免外推）：Treisman & Schmidt 1982 用 1/5 秒呈现 + 随机点掩蔽，**18%** 试次报告看到由两个不同刺激特征拼成的形状（illusory conjunctions）；Bálint 综合征患者 R.M. 即使观看长达 **10 秒**，仍在 **23%** 试次把 "blue O / red T" 报成 "red O / blue T"；Treisman & Souther 1986 给形状加上熟悉语义标签（carrot、lake、tire）后，错误组合消失，说明 prior knowledge / top-down processing 参与绑定。页面另有 **binding congruency effect**：绑定不一致特征（小数字却用大物理尺寸、颜色词用冲突字色）错误显著更多。

**四条设计推论**：

1. **要让某个元素"跳出来"，只改一个特征维度**。同时改颜色 + 大小 + 形状 + 位置，就把它从 feature search 推成 conjunction search，用户反而要串行找。
2. **颜色/朝向/强度是最省的前注意通道**；但颜色不能单独承载语义（色觉与对比度约束归 `color-science.md` / `accessibility.md`）。
3. **"不一致"本身有代价**：binding congruency effect 与 Stroop 式的冲突字色都说明，视觉信号互相矛盾时错误率上升，别把"醒目"做成信号打架。
4. **熟悉构型能抵错误绑定**：给形状配上用户已有的语义标签（图标 + 文字）比纯抽象图形稳，这与 `iconography.md` 的"图标 + 文字降低认知负荷"是同一条机制。

**取源纪律**：Wikipedia 并无 `Preattentive_processing` 条目（本轮实测返回"Wikipedia does not have an article with this exact name"），因此改用 FIT 1980 作为前注意机制的权威源；FIT 页面**没有**给出 visual search slopes 的具体数值（ms/item、set-size × RT 斜率），只能引用 feature/conjunction 的定性快慢差异，**不得编造斜率常数**。

---

## 10 · 图形/背景与多稳态：不要做歧义层级

IxDF 把 Figure/Ground 与 Multistability 分列，并明确指出二者常被混淆：*"In most cases, background and foreground are stable, but in some cases, such as the optical illusion of Rubin's vase, it can contribute to multistability."*

- **Figure/Ground 是层级的地基**：*"we look for solid, stable items"*、*"we see its foreground first"*。明暗主题反转（黑字白底 → 白字黑底）后用户仍能识别，靠的是稳定的前景/背景关系，而不是具体色值。
- **Multistability 是缺陷信号，不是趣味效果**：*"When images are ambiguous and present two or more meaningful interpretations, we experience the sensation of switching between them. We cannot see the multiple versions simultaneously."* 界面里出现"这个卡片到底能不能点""这块到底是背景还是可操作区""这两个按钮哪个是默认"，用户就无法同时持有两种解释，只能来回切换——这是**认知负荷的直接来源**。
- **验收口径**：任意一个可交互状态，必须能用一句话说清"它是 figure 还是 ground、是不是当前唯一最重元素"；说不清就回到 §2 判层，别用动效或说明文字去补。

---

## 11 · 裁决三：认知负荷分三类，7±2 不是菜单上限

**来源**：Laws of UX《Cognitive Load》与《Miller's Law》逐字页 + Wikipedia《Cognitive_load》。

- 定义（Laws of UX 逐字）：*"The amount of mental resources needed to understand and interact with an interface."*
- 起源（Laws of UX 逐字）：*"Cognitive load theory was developed in the late 1980s by John Sweller out of a study of problem solving"*， culminated in his **1988** publication *"Cognitive Load Theory, Learning Difficulty, and Instructional Design"*，是对 George Miller 信息处理理论的扩展。
- **三类负荷**：Wikipedia《Cognitive_load》给出 intrinsic / extraneous / germane 三分（Sweller 1988）。Laws of UX 的 Takeaways 逐字覆盖前两类：
  - *"Intrinsic cognitive load refers to the effort required by users to carry around information relevant to their goal, absorb new information and keep track of their goals."*
  - *"Extraneous cognitive load refers to the mental processing that takes up resources but doesn't help users understand the content of an interface (e.g. distracting or unnecessary design elements)."*
  - **germane**（用于图式建构/学习的投入）不在该页 Takeaways 里，来自 Wikipedia 的三分，引用时标注来源，别混成同一页原文。
- **超载的可观察信号**（Laws of UX Takeaway 1 逐字）：*"When the amount of information coming in exceeds the space we have available, we struggle mentally to keep up — tasks become more difficult, details are missed, and we begin to feel overwhelmed."*

**7±2 的正确与错误用法**：

- Miller 1956 讲的是**即时记忆广度与绝对判断**的容量（Laws of UX Origins 逐字：*"the span of immediate memory and absolute judgment were both limited to around 7 pieces of information"*），信息单位是 **bit**——*"the amount of data necessary to make a choice between two equally likely alternatives"*，4 bits 对应 16 个二选一（4 次连续二元判断），混淆点称 channel capacity。
- Laws of UX 三条 Takeaways 逐字：① *"Don't use the 'magical number seven' to justify unnecessary design limitations."* ② *"Organize content into smaller chunks to help users process, understand, and memorize easily."* ③ *"Remember that short-term memory capacity will vary per individual, based on their prior knowledge and situational context."*
- **所以**：不能用 7±2 论证"导航最多 7 项""表单最多 7 个字段"。`navigation-ia.md` 里的项数铁律（全局 5–9 / 底部 ≤5）是**导航形态与移动端约束的工程约定**，不是 Miller 定律的推论；两者不要互相背书。真正可用的是 **chunking**（Laws of UX 定义：*"A process by which individual pieces of an information set are broken down and then grouped together in a meaningful whole."*）——把信息按语义分块，而不是砍数量。

---

## 12 · Hick–Hyman Law：决策时间的公式与失效条件

**定义**（Laws of UX 逐字）：*"The time it takes to make a decision increases with the number and complexity of choices."* **起源**：William Edmund Hick 与 Ray Hyman，**1952** 年研究刺激数量与反应时的关系。

**通式**（Wikipedia《Hick's law》口径）：

```
RT = a + b · log₂(n + 1)
```

- `n` 为等概率选项数；`a`、`b` 为经验常数（含编码、运动等基线开销）。
- `log₂` 对应**二分/选择树**：用户每做一次判断约排除一半剩余选项，所以耗时随选项数**对数**增长而非线性。
- `+1` 表示"是否要响应"这一额外不确定性（即存在"不选项"）。

**五条 Takeaways**（Laws of UX 逐字）：① *"Minimize choices when response times are critical to decrease decision time."* ② *"Break complex tasks into smaller steps in order to decrease cognitive load."* ③ *"Avoid overwhelming users by highlighting recommended options."* ④ *"Use progressive onboarding to minimize cognitive load for new users."* ⑤ *"Be careful not to simplify to the point of abstraction."*

**失效条件（最容易误用的一点）**：`log₂` 成立的前提是选项**可分类、可被逐层排除**（按字母排序的列表、有层级结构的菜单、用户已有心智模型）。若选项是**随机无序、必须逐项读完才能判断**的菜单，用户做的是线性扫描，耗时随 `n` 近似线性增长，Hick 公式不适用。此时正确动作是**先排序/分组/给默认推荐**（把线性扫描改造成选择树），而不是套公式说"反正对数增长，多放几项无所谓"。

**与 Fitts 的分工**：Hick 管"选哪个"（决策），Fitts 管"点得到"（运动）。一个按钮既难找又难点，两个成本相加，不能只优化其中之一。

---

## 13 · Fitts's Law：目标尺寸与距离的三种写法

**定义**（Laws of UX 逐字）：*"The time to acquire a target is a function of the distance to and size of the target."* **起源**：Paul Fitts **1954** 年研究人类运动系统，*"the time required to move to a target depends on the distance to it, yet relates inversely to its size"*，并指出 speed-accuracy trade-off：*"fast movements and small targets result in greater error rates"*。

**三种形式要分清**（Wikipedia《Fitts's law》口径）：

```
原始形式：        ID = log₂(2D / W)             MT = a + b·log₂(2D / W)
Shannon/MacKenzie：ID = log₂(D / W + 1)         MT = a + b·log₂(D / W + 1)
吞吐量：          TP = ID_e / MT                （ID_e 为有效难度指数）
```

- `D`：从起点到**目标中心**的距离；`W`：**沿运动轴方向**的目标宽度（不是视觉上的最大边，斜向移动要用投影宽度）。
- `MT` 为 movement time，`a`/`b` 为经验常数。`MT = a + b·log₂(2D/W)` **不是**严格意义的 Shannon formulation，写文档时别混称。
- `TP`（throughput，bits/s）用于跨设备/跨输入方式比较，不是"越大越好看"的审美指标。

**三条 Takeaways**（Laws of UX 逐字）：① *"Touch targets should be large enough for users to accurately select them."* ② *"Touch targets should have ample spacing between them."* ③ *"Touch targets should be placed in areas of an interface that allow them to be easily acquired."*

**可推导的布局结论**：把高频目标做大（增大 `W`）、放在当前注意力区域附近（减小 `D`）、相邻危险操作之间留足间距（降低误触代价）；屏幕边缘与角落因指针被边界"钉住"而相当于拥有更大的有效宽度（edge/corner 与 prime pixel 的概念），适合放高频全局操作，但**不要**因此把破坏性操作放角落当作防误触手段。具体触控尺寸阈值以对应平台规范为准，本文件不臆造统一 px 数；组件库实测值见 `component-libraries.md`。

---

## 14 · 工作记忆、chunking 与渐进披露

- **工作记忆**（Laws of UX 逐字）：*"A cognitive system that temporarily holds and manipulates information needed to complete tasks."*；**Chunking**（逐字）：*"A process by which individual pieces of an information set are broken down and then grouped together in a meaningful whole."*
- **可直接照抄的做法**：把长表单按语义分块、每块给描述性标题（同时满足 §5 的 2.4.6 / 2.4.10）；跨步骤保留用户已填信息的可见回执，别要求"记住上一页"；把复杂任务拆成小步（Hick Takeaway 2）并给推荐项（Hick Takeaway 3）。
- **渐进披露**（Hick Takeaway 4，Laws of UX 的 Slack 例子逐字）：*"Instead of dropping users into a fully featured app after enduring a few onboarding slides, Slack uses a bot to engage users"*，*"To prevent new users from feeling overwhelmed, Slack hides all features except for the messaging input."* 关键是**按当前任务披露**，不是永久隐藏；隐藏带来的下一步寻找成本要计入 L3。
- **反例**：把"7±2"当成一屏最多 7 个字段、把 chunking 做成把 20 项硬切成 3 组却不加组标题——后者没有形成 "meaningful whole"，只是多了两道分隔线。

---

## 15 · 序列位置效应与 Von Restorff：位置与差异如何改变记忆

**来源**：Wikipedia《Serial_position_effect》《Von_Restorff_effect》+ Laws of UX 同名条目。

- **序列位置效应**（逐字）：*"Serial-position effect is the tendency of a person to recall the first and last items in a series best, and the middle items worst."* 前段优势为 **primacy effect**，末段优势为 **recency effect**。
- **可复现的实验细节**：干扰任务 **15–30 秒**可抵消 recency effect；另有 10–30 秒心算干扰削弱 recency 的记载；相关经典工作含 Ebbinghaus 与 Murdock 1962。Laws of UX 的界面化表述（逐字）：*"Users have a propensity to best remember the first and last items in a series."*
- **设计落点**：导航/步骤条/列表的**首项与末项**是记忆优势位——把最关键的入口放首项、把最重要的收尾动作（提交/完成）放末项；中间项不要放唯一必读信息。注意这是**回忆优势**不是"注意力必然覆盖"，不能替代 §3 的引导信号。
- **Von Restorff effect / isolation effect**（逐字）：*"The von Restorff effect, also known as the isolation effect, predicts that when multiple homogeneous stimuli are presented, the stimulus that differs from the rest is more likely to be remembered."* Hedwig von Restorff **1933**；制造差异的手段包括 **size / shape / color / spacing / underlining**。Laws of UX 逐字：*"when multiple similar objects are present, the one that differs from the rest is most likely to be remembered."*
- **关键限定**：差异是**相对的**。全页每个模块都"突出"就等于没有孤立项——这正是 §8"单焦点"与 `editorial-layout.md §8`"一张图只允许一个最重元素"的实验心理学依据。另注意 Wikipedia 提醒该效应主要来自实验室短词表范式，向真实界面外推要谨慎，别据此宣称具体提升百分比。

---

## 16 · Laws of UX 中注意力/负荷相关的 12 条速查

站点首页共列 31 条。以下 12 条与 L2/L3 直接相关，定义均为首页逐字，未做二次演绎；**未在本轮逐页核验的条目只收录首页那一句定义**，不补造出处与年份。

| 条目 | 首页定义（逐字） | 本文件用法 |
|---|---|---|
| **Cognitive Load** | *"The amount of mental resources needed to understand and interact with an interface."* | §11 三分 |
| **Hick's Law** | *"The time it takes to make a decision increases with the number and complexity of choices."* | §12 公式与失效条件 |
| **Fitts's Law** | *"The time to acquire a target is a function of the distance to and size of the target."* | §13 三种写法 |
| **Miller's Law** | *"The average person can only keep 7 (plus or minus 2) items in their working memory."* | §11 **不可**当菜单上限 |
| **Chunking** | *"A process by which individual pieces of an information set are broken down and then grouped together in a meaningful whole."* | §14 |
| **Working Memory** | *"A cognitive system that temporarily holds and manipulates information needed to complete tasks."* | §14 |
| **Selective Attention** | *"The process of focusing our attention only to a subset of stimuli in an environment — usually those related to our goals."* | §9 与目标的绑定 |
| **Serial Position Effect** | *"Users have a propensity to best remember the first and last items in a series."* | §15 |
| **Von Restorff Effect** | *"when multiple similar objects are present, the one that differs from the rest is most likely to be remembered."* | §15 单焦点 |
| **Choice Overload** | *"The tendency for people to get overwhelmed when they are presented with a large number of options, often used interchangeably with the term paradox of choice."* | §12 与 Hick 的区别：这里是**主观压倒感**，不是反应时公式 |
| **Doherty Threshold** | *"Productivity soars when a computer and its users interact at a pace (<400ms) that ensures that neither has to wait on the other."* | 交互节奏；注意 <400ms 是站点表述，性能预算归 `performance-design.md` |
| **Jakob's Law** | *"Users spend most of their time on other sites. This means that users prefer your site to work the same way as all the other sites they already know."* | 用既有心智模型降低 intrinsic load |

**NN/g 10 Usability Heuristics**（Jakob Nielsen；原文说明启发式 **1990** 年开发，本文 **1994-04-24** 发布且 *"unchanged since 1994"*，**2020** 年更新，**2024-01-30** 最后审阅）：① Visibility of System Status ② Match Between the System and the Real World ③ User Control and Freedom ④ Consistency and Standards ⑤ Error Prevention ⑥ Recognition Rather than Recall ⑦ Flexibility and Efficiency of Use ⑧ Aesthetic and Minimalist Design ⑨ Help Users Recognize, Diagnose, and Recover from Errors ⑩ Help and Documentation。与 L3 最相关的是 **⑥ Recognition Rather than Recall**（别让用户记状态）与 **⑧ Aesthetic and Minimalist Design**（减少外在负荷）。

---

## 17 · 从内容到视觉的六步构建流程

顺序不可颠倒——多数"层级乱"是跳过了前 3 步直接做第 4 步。

1. **写内容大纲**：先有 `h1 → h2 → h3` 的语义树，标题文案要能独立描述主题或用途（SC 2.4.6）。没有大纲就不要开画。
2. **定 DOM 顺序**：按大纲写 HTML，让代码顺序就是阅读顺序（C27 / SC 1.3.2）。此时**不写任何 `order` / 正值 `tabindex`**。
3. **分组**：用间距、闭合区域、相似 token、对齐轴把内容落成团块（§7 §8）。眯眼测试确认团块数 = 大纲分组数。
4. **定单一焦点**：选出一个"最重"元素与一个主操作；其余降为次级（§8 §10 §15）。新增的强调维度**只改一个**（§9）。
5. **才做视觉表达**：字号/字重/颜色/留白按已有的分组与顺序去表达，不反过来用字号创造结构（数值契约分别归 `typography-system.md`、`color-science.md`）。
6. **三顺序回归**：禁用 CSS 读一遍、Tab 走一遍、抽取标题树一遍（§6），三类结果讲同一个故事才算完成；RTL / 断点再各走一遍。

**输出物清单**：标题树、DOM 顺序说明、分组间距 token、单一焦点说明、三顺序检查记录。缺任何一项，"层级"就仍然只是截图里的观感。

---

## 18 · 三关度量与验收

不生产玄学评分，只做三道可复现的检查；任何一道不过，回到 §2 对应层修。

| 关 | 检查对象 | 具体动作 | 通过标准 |
|---|---|---|---|
| **组织关（L1）** | 团块、单焦点、间距比 | 眯眼/25% 缩放截图；量 `g_in` / `g_out`；数主操作数 | 团块数 = 大纲分组数；`g_in ×1.5 ≤ g_out`；主操作 = 1 |
| **顺序关（L2）** | DOM / 焦点 / 标题树 | 禁 CSS 线性读、Tab 全程走、`h1→h2→h3` 大纲导出；RTL 与断点各一遍 | 三者同故事；无正 `tabindex`；无跳级；无意义依赖顺序的 CSS 搬移 |
| **负荷关（L3）** | 决策与目标 | 数每屏选项是否可分类（Hick 前提）；量高频目标 `D`/`W`；逐项标 intrinsic / extraneous | 无序选项先排序/分组/给默认；高频目标 `W` 与间距按 §13 复核；能指出至少一处被删掉的外在负荷 |

**可用工具**：`scripts/dp_search.py "格式塔 分组 邻近性"` 定位本章；§23.2 的静态扫描器跑 DOM/焦点/标题树；§23.1 的计算器给 Hick/Fitts 的相对变化量（**只用于比较方案 A/B，不用于预测真实秒数**，因为 `a`/`b` 需实测标定）。

---

## 19 · 与既有资产的边界矩阵

| 用户问题 | 归谁 | 本文件只补什么 |
|---|---|---|
| 正文多大字号、行高多少、200% 缩放 | `typography-system.md` | 层级是**顺序**不是字号；字号只是表达手段之一 |
| 对比度 3:1 / 4.5:1 怎么算 | `color-science.md §6` / `accessibility.md §2` | 前注意颜色通道不可单独承载语义 |
| 版面 Z 型 / F 型构图、视觉重量排序 | `editorial-layout.md §8` | F 型的**眼动实证**与"非设计目标"裁决 |
| 导航放几项、深度还是广度 | `navigation-ia.md` | 7±2 **不能**用来论证项数上限 |
| 圆角、阴影、卡片浮起、z-index | `shape-elevation.md` | 卡片是 Common Region 的**容器**，但边界值不由本文件给 |
| 图标要不要配文字 | `iconography.md` | 熟悉语义标签降低绑定错误（§9） |
| 诱导、默认勾选、取消订阅难 | `design-ethics-inclusion.md` | 情境性认知负荷是 dark pattern 的作用面，本文件只讲机制 |
| 首屏加载、交互 <400ms | `performance-design.md` | Doherty Threshold 是站点表述，性能预算不在此定 |
| 动效顺序、共同命运动画 | `motion-design.md` / `interaction-states.md` | Common Fate 是分组机制，曲线与状态归它们 |

---

## 20 · 场景速查（12）

| 场景 | 判层 | 第一动作 | 依据 |
|---|---|---|---|
| 用户说"页面很乱、找不到重点" | L1 | 眯眼测团块数；数主操作是否 >1 | §8 §10 §15 |
| 卡片里塞了两组无关内容 | L1 | 拆成两个闭合区域（Common Region） | §7 #3 |
| 标签离输入框太远、看起来像上一组的 | L1 | 调组内/组间间距比 | §7 #5 §8 |
| 主内容视觉在上、读屏却先读侧栏 | L2 | 改 HTML 顺序，去掉 `order: -1` | §5.1 §6 |
| Tab 键乱跳、焦点突然回顶部 | L2 | 删正 `tabindex` 与强制 `focus()` | §5.2 §6 |
| 视觉有分区但没有 `<h2>` | L2 | 补标题树与描述性标题文案 | §5.3 §5.4 |
| 长文用户只看标题行 | L2 | 让每个标题独立承载结论（Layer-cake） | §4 |
| 用户跳过了放主操作的侧栏 | L2 | 主操作移进必读区（Bypassing） | §4 |
| 菜单 20 项，用户选得很慢 | L3 | 先排序/分组/给推荐，再谈删减 | §12 |
| 按钮太小、总点错相邻项 | L3 | 增大 `W`、加间距、缩短 `D` | §13 |
| 表单一屏 20 个字段 | L3 | 分块 + 每块描述性标题 + 渐进披露 | §11 §14 |
| 阿拉伯语版沿用中文版视觉动线 | L2 | 翻转起点与竖扫侧，`dir="rtl"` 全量复核 | §3 §6 |

---

## 21 · 反模式（20）

1. 把 F 型当版式模板主动"设计"，而不是当作缺引导的诊断信号。
2. 用「我们是 F 型布局」解释为什么第三屏没人看。
3. 宣称"F 型已死/移动端不适用"，与 NN/g 2017 的桌面与移动眼动结论相悖。
4. RTL 只改文字方向，不翻转视觉起点与竖扫侧。
5. 给 NN/g 文章里只作描述的 "像 E" 造一个 "E-pattern" 名词并当成已命名模式。
6. 用 `order: -1` / `row-reverse` 把主内容搬到视觉上方，DOM 里却排在侧栏之后。
7. 用正 `tabindex` 手工"修"焦点顺序，导致每次改版都要重排一套数字。
8. 用 `<div class="title">` + 大字号冒充标题树，`<h1>` 后直接跳 `<h3>`。
9. 用卡片/分隔线/色块代替 `<h2>`，理由是"视觉上已经分好了"。
10. 标题写成"章节一 / 更多信息 / 相关"，不描述主题或用途。
11. 用 7±2 论证"导航最多 7 项""表单最多 7 个字段"。
12. 把 chunking 做成硬切分组却不加组标题，没有形成 meaningful whole。
13. 拿 Hick 的 `log₂` 为随机无序菜单的无限增项背书。
14. 同时改颜色+大小+形状+位置来"强调"，把 feature search 推成 conjunction search。
15. 全页每个模块都加粗/加色/加角标，等于取消唯一的孤立项。
16. 把破坏性操作放到屏幕角落，理由是"角落难点到"（edge/corner 恰恰更易命中）。
17. 用阴影充当分组边界，或让前景/背景对比弱到出现 figure/ground 歧义。
18. 把关键状态做成两种解释都可的图形（Multistability），再用 tooltip 打补丁。
19. 渐进披露变成永久隐藏，用户为找下一步付出的成本高于披露前的负荷。
20. 把本文件的间距比、单焦点、团块数等工程约定写成"研究证明的最佳数值"。

---

## 22 · 自检（20）

1. 说过"F 型是默认扫描而非设计目标"，并能引用 NN/g 那句 default pattern 原文？
2. 能列出 F 之外的至少 5 种 NN/g 扫描模式，并说明 layer-cake 对标题文案的要求？
3. 知道 RTL 下 F 型翻转、移动端仍有 F 型，且"像 E"不是正式命名模式？
4. 能逐字说出 SC 1.3.2 与 SC 2.4.3 的规范条文及各自级别（均为 A）？
5. 能说清 1.3.2 **不要求**视觉顺序等于 DOM 顺序，但要求意义依赖顺序时存在可程序判定的正确顺序？
6. 能说出 C27、F1、G57、G59 各自管什么？
7. 能引用 2.4.10 Intent 里 "visual presentation is not sufficient to identify document sections" 这一句？
8. 知道 2.4.6 不要求必须提供标题/标签，正确标记归 1.3.1、标签归 3.3.2、可访问名称归 4.1.2？
9. 三顺序（DOM/焦点/标题树）各导出过一次且讲同一个故事？
10. 全站没有正 `tabindex`，且无脚本时焦点顺序 = content stream 顺序？
11. 眯眼测试里团块数与大纲分组数一致、主操作数 = 1？
12. 能量化 `g_in`/`g_out` 并说明 1.5× 是工程约定而非实验常数？
13. 能列全 IxDF 的 12 条格式塔原则，并区分 Figure/Ground 与 Multistability？
14. 知道 Koffka 原话是 "other than the sum of the parts" 而不是 "greater than"？
15. 能解释 feature search 与 conjunction search 的差别，以及为什么"只改一个特征维度"才能 pop-out？
16. 能说出 Treisman & Gelade 1980、18% / 23% 两个实验数据分别来自哪个实验，并声明 FIT 页面没有视觉搜索斜率数值？
17. 能把认知负荷拆成 intrinsic / extraneous / germane，并说清哪一类的来源页是 Wikipedia 而非 Laws of UX Takeaways？
18. 能写出 `RT = a + b·log₂(n+1)` 并说明 `+1` 与"随机无序菜单不适用"的原因？
19. 能写出 Fitts 的 Shannon 形式 `ID = log₂(D/W+1)`，说清 `W` 是沿运动轴宽度、`MT = a + b·log₂(2D/W)` 不是 Shannon formulation？
20. 知道序列位置的 primacy/recency、15–30 秒干扰抵消 recency、Von Restorff 的"相对差异"限定，并把外推限制写进交付说明？

---

## 23 · 可抄代码（5 段，3 段 Python 已实跑）

### 23.1 Python · Hick / Fitts 相对成本计算器（实跑 PASS）

只用于**方案 A/B 的相对比较**；`a`、`b` 是占位常数，真实秒数需实测标定。

```python
import math


def hick_rt(n: int, a: float = 0.0, b: float = 0.155) -> float:
    """RT = a + b*log2(n+1)；+1 为「是否响应」的不确定性。"""
    return a + b * math.log2(n + 1)


def fitts_id(d: float, w: float, form: str = "shannon") -> float:
    """Shannon/MacKenzie: log2(D/W+1)；original: log2(2D/W)。"""
    if w <= 0 or d <= 0:
        raise ValueError("D 与 W 必须为正")
    if form == "original":
        return math.log2(2 * d / w)
    return math.log2(d / w + 1)


def fitts_mt(d: float, w: float, a: float = 0.0, b: float = 0.1,
             form: str = "shannon") -> float:
    return a + b * fitts_id(d, w, form)


if __name__ == "__main__":
    print("Hick  RT(n) 与相对 n=2 的增量")
    for n in (2, 4, 8, 16):
        print(f"  n={n:>2}  RT={hick_rt(n):.4f}s  delta={hick_rt(n)-hick_rt(2):+.4f}s")
    print("Fitts  Shannon ID 与 MT")
    for d, w in ((200, 40), (200, 80), (400, 40)):
        print(f"  D={d} W={w}  ID={fitts_id(d, w):.4f}  MT={fitts_mt(d, w):.4f}s")
    assert fitts_id(200, 40) > fitts_id(200, 80) > 0
    assert hick_rt(16) > hick_rt(2)
    print("PASS")
```

### 23.2 Python · 三顺序静态扫描器（实跑 PASS）

对一段 HTML 检查标题跳级、正 `tabindex`、CSS `order` / `row-reverse` / `position: absolute` 造成的视觉顺序搬移，输出可直接贴进评审记录。

```python
from html.parser import HTMLParser
import re

HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings = []
        self.focus = []
        self.reorders = []
        self._cur = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in HEADINGS:
            self.headings.append(int(tag[1]))
            self._cur = tag
        ti = d.get("tabindex")
        if ti is not None:
            self.focus.append((tag, ti))
        style = (d.get("style") or "").lower()
        if re.search(r"order\s*:\s*-?\d", style) or "row-reverse" in style \
                or "column-reverse" in style or re.search(r"position\s*:\s*absolute", style):
            self.reorders.append((tag, style.strip()))


def audit(html: str) -> dict:
    p = Audit()
    p.feed(html)
    skips = [(a, b) for a, b in zip(p.headings, p.headings[1:]) if b - a > 1]
    positive = [(t, v) for t, v in p.focus if v.lstrip("+").isdigit()
                and int(v) > 0]
    return {
        "heading_outline": p.headings,
        "heading_skips": skips,
        "positive_tabindex": positive,
        "visual_reorders": p.reorders,
        "pass": not skips and not positive and not p.reorders,
    }


BAD = """<h1>结算</h1>
<div style="order:-1">主操作</div>
<h3>次要信息</h3>
<button tabindex="5">提交</button>"""

GOOD = """<h1>结算</h1>
<h2>收货信息</h2>
<h2>支付方式</h2>
<button>提交</button>"""

if __name__ == "__main__":
    for name, sample in (("BAD", BAD), ("GOOD", GOOD)):
        r = audit(sample)
        print(name, "outline=", r["heading_outline"],
              "skips=", r["heading_skips"],
              "positive_tabindex=", r["positive_tabindex"],
              "reorders=", len(r["visual_reorders"]),
              "PASS" if r["pass"] else "FAIL")
    assert audit(BAD)["pass"] is False
    assert audit(GOOD)["pass"] is True
    print("PASS")
```

### 23.3 Python · 邻近性间距比校验器（实跑 PASS）

`1.5` 是 §8 声明的**工程约定**，改成一个常量便于团队按自己设计系统调整，不伪装成感知实验结论。

```python
RATIO = 1.5  # 工程约定：组间间距至少为组内间距的 1.5 倍；非实验常数


def proximity_ok(gaps_within, gaps_between, ratio=RATIO):
    """两个列表按位置一一对应：每个分组的内部间距 vs 该组与下一组之间的间距。"""
    bad = [(i, a, b) for i, (a, b) in enumerate(zip(gaps_within, gaps_between))
           if b < a * ratio]
    return {"bad": bad, "pass": not bad}


if __name__ == "__main__":
    ok = proximity_ok([8, 8, 8], [24, 24, 24])
    bad = proximity_ok([8, 16, 8], [24, 16, 24])
    print("均匀分组", ok)
    print("第二组过挤", bad)
    assert ok["pass"] is True and bad["pass"] is False
    assert bad["bad"] == [(1, 16, 16)]
    print("PASS")
```

### 23.4 CSS · 层级信号 token（不靠"一路放大加粗"）

```css
:root {
  /* 表达层：复用 typography-system.md / color-science.md 的既有 token，不另造字号色值 */
  --hierarchy-gap-in: var(--space-2);      /* 组内 */
  --hierarchy-gap-out: var(--space-5);     /* 组间，按 §8 约定 >= 1.5 * gap-in */
  --hierarchy-region-border: var(--border-subtle);
}

.hierarchy-region {                        /* Common Region：一个闭合区域只承载一组 */
  border: 1px solid var(--hierarchy-region-border);
  padding: var(--hierarchy-gap-in);
  margin-block-end: var(--hierarchy-gap-out);
}
.hierarchy-region > * + * {
  margin-block-start: var(--hierarchy-gap-in);
}
.hierarchy-primary {                       /* 单一焦点：一个视图只允许一处 */
  font-weight: var(--weight-bold);
}
/* Continuity：同一视图主对齐轴 <= 2，别用 order/row-reverse 搬主内容 */
.hierarchy-layout { display: grid; grid-template-columns: 1fr; }
@media (min-width: 60rem) {
  .hierarchy-layout { grid-template-columns: minmax(0, 1fr) 18rem; }
}
/* RTL：起点与竖扫侧翻转，方向交给逻辑属性而不是 left/right */
.hierarchy-region { padding-inline-start: var(--hierarchy-gap-in); }
```

### 23.5 HTML · C27 正例与 F1 反例对照

```html
<!-- 正例：DOM 顺序 = 阅读顺序 = 焦点顺序；标题树可导出 -->
<main>
  <h1>结算</h1>
  <section aria-labelledby="ship">
    <h2 id="ship">收货信息</h2>
    <!-- 表单字段 -->
  </section>
  <aside aria-labelledby="help">
    <h2 id="help">帮助</h2>
    <!-- 侧栏在 DOM 里排在后面，用 CSS 放到右边 -->
  </aside>
  <button type="submit">提交订单</button>
</main>

<!-- 反例：视觉靠 order 搬位，读屏先读帮助；h1 直接跳 h3；正 tabindex -->
<main style="display:flex">
  <aside style="order:0"><h3>帮助</h3></aside>
  <section style="order:-1"><h1>结算</h1></section>
  <button tabindex="5">提交订单</button>
</main>
```

---

## 24 · 取源与限制（公开记录）

**本轮深蒸馏的官方/权威原文**（逐字引用均已在前文标注出处）：

- W3C WAI《Understanding WCAG 2.2》：`meaningful-sequence.html`（SC 1.3.2, A）、`focus-order.html`（SC 2.4.3, A）、`headings-and-labels.html`（SC 2.4.6, AA）、`section-headings.html`（SC 2.4.10, AAA）。
- NN/g：`/articles/f-shaped-pattern-reading-web-content/`（Kara Pernice, 2017-11-12, last reviewed 2026-08-19）与其中链接的 2006 原始研究 `/articles/f-shaped-pattern-reading-web-content-discovered/`；`/articles/ten-usability-heuristics/`（Jakob Nielsen，1990 开发 / 1994-04-24 发布 / 2020 更新 / 2024-01-30 最后审阅）。
- IxDF：`interaction-design.org/literature/topics/gestalt-principles`（页面标注 updated 2026）12 条原则与 Koffka 原话。
- Laws of UX 首页 31 条定义 + `hicks-law` / `fittss-law` / `millers-law` / `cognitive-load` 四个逐字页（Takeaways 与 Origins）。
- Wikipedia：`Cognitive_load`（Sweller 1988 与三分）、`Hick's_law`（通式与 `+1`）、`Fitts's_law`（三种形式与 `W` 定义）、`Serial_position_effect`、`Von_Restorff_effect`、`Feature_integration_theory`（Treisman & Gelade 1980 与 18% / 23%）。
- 中文侧（**仅搜索结果级、未逐字核验，故未作为本文件任何数值/引文的依据**）：`uisdc.com/gestalt-principle`、`uisdc.com/7-visual-principles-of-gestalt`、`zhuanlan.zhihu.com/p/337506743`、`hxsd.com/information/8071/`、`woshipm.com/open/5978930.html`。

**GitHub API 实测**（本轮 `GET /repos/{owner}/{repo}`，无鉴权公开端点；star / license 为实测值）：`pinterest/gestalt` **4,384★ / Apache-2.0**（设计系统名即取自格式塔）、`primer/primitives` **417★ / MIT**、`radix-ui/themes` **8,825★ / MIT**、`mui/material-ui` **99,301★ / MIT**、`tailwindlabs/tailwindcss` **98,646★ / MIT**。

**取源限制（不臆造、不外推）**：

- Wikipedia **没有** `Preattentive_processing` 条目，改用 FIT 1980；FIT 页面**未给出** visual search slopes 的具体数值，本文件只写 feature/conjunction 的定性差异。
- 猜测的 NN/g URL 全部 404：`/articles/visual-hierarchy/`、`/articles/scanning-patterns/`、`/articles/attention-span/`、`/articles/f-shaped-pattern-of-reading-on-the-web/`；正确路径经搜索确认为 `/articles/f-shaped-pattern-reading-web-content/`。**404 页面里的任何内容均未引用**。
- IxDF 的 `cognitive-load` 主题页**未包含** Sweller 三分与年份，故 CLT 权威源改为 Wikipedia `Cognitive_load` + Laws of UX `cognitive-load`；Wikipedia 该页亦未给出工作记忆时长的具体秒数，本文件不写"X 秒会忘"。
- Wikipedia 部分公式以图片/LaTeX 呈现，页面抓取时未渲染；本文公式按可见正文与标准表述整理，并明确区分 original / Shannon 两种形式，不把 `MT = a + b·log₂(2D/W)` 称作 Shannon formulation。
- `lawsofux/lawsofux.com`、`jonathantneal/laws-of-ux`、`victorpowerr/laws-of-ux`、`jonyablonski/laws-of-ux`、`lawsofux/laws-of-ux`、`nngroup/ux-research-cheat-sheet` 均返回 Not Found，故 Laws of UX **只记站点不记仓库**；无鉴权 `/search/repositories` 本轮触发 API rate limit，未据此补仓库。
- §8 的 `1.5×` 间距比、§18 的团块/单焦点规则均为**本知识库工程约定**，非实验常数；§23.1 的 `a`/`b` 为占位常数，不得用于预测真实反应时秒数。
- 发布通道备注：本轮实测 `~/.workbuddy-ai/secrets/github_token.txt` 首行的 PAT 返回 `Bad credentials`（已失效），而 `git credential fill` 取出的凭据 `GET /user` 返回 200；`publish_github.py` 的降级链会自动取用后者，不影响发布。

**下轮候选缺口**：① **信息气味与可扫读文案的量化验收**（`information scent`、链接标签可预测性、卡片分类/树测试实测口径，`navigation-ia.md` 只有定性）；② **眼动研究方法的工程化**（注视点/扫视/热区图的有效样本与常见误读，本轮只取了 NN/g 结论性原文）；③ **注意力与通知/中断**（选择性注意、变化盲视、中断恢复时间的权威原文，本轮未取）；④ **Laws of UX 余下 19 条逐页核验**（本轮只逐页核了 4 条 + 首页定义）；⑤ **中文侧逐字核验**（本轮 5 个中文源仅搜索结果级）；⑥ `radix-ui/themes` shape/elevation token 源码精确定位与 Fluent 2 depth 现行路径复核（沿用 #28 未结项）。
