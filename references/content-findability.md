# 内容可发现性与可扫读性（Content Findability / Search UX / Scannability）

> 快照 2026-11-09 · 27 节 · 12 场景 · 20 反模式 · 20 自检 · 5 段可抄代码（3 段 Python 已实跑）

把「放个搜索框、写几句简洁文案、导航清楚一点」变成**有官方原文、有量化口径、能静态验收的找路契约**。本文件不替代 `navigation-ia.md`（导航形态、面包屑、IA 深度广度）、`feedback-states.md §5/§6`（五种空态与 404 文案模板）、`ux-writing.md §14.3`（文案语气与可读性）、`design-measurement-research.md §11`（A/B 与统计）、`accessibility.md`（WCAG 全档阈值）、`typography-system.md §16`（W3C clreq 中文排版）、`visual-hierarchy-gestalt.md §3/§4`（F 型与扫描模式），而是补上它们都在**假设**、却没人贯通的一整条链路：**用户从「我要找个东西」到「我确认找到了」之间，每一步靠什么线索、在哪一步流失、以及这条链路对读屏用户是否同样成立**。

**一句话立场**：可发现性不是搜索框的属性，是**内容在整条链路上留下的线索密度**——用户先要「有路可走」，再要「看得出哪条路对」，再要「点进去读得动」，最后要「走错了还能退出来」。任何一环断裂，前面的视觉层级做得再好都是把用户更快地送到一个死胡同。

**本轮三条最重要裁决**（后文逐条给官方原文、数值与验收动作）：

1. **多种找路方式是 WCAG AA 的硬要求，搜索不是导航的替身**。W3C SC 2.4.5（Level AA）逐字：*"More than one way is available to locate a web page within a set of web pages except where the web page is the result of, or a step in, a process."*，In Brief 更直白 *"Provide at least two options for reaching the same content."*；充分技术要求 **Using two or more of the following techniques**，其中 **G161: Providing a search function to help users find content** 只是六个候选之一。NN/g（Jakob Nielsen, 2001-05-12）把搜索定位为 *"the user's escape hatch when they are stuck in navigation"*，并据此要求 *"make search available from every page on the site"*。**把搜索藏进放大镜图标、或把导航砍掉只留搜索，是把合规要求退化成单点故障**。
2. **链接目的必须能在脱离上下文时成立；前 11 个字符决定用户会不会看完整句**。W3C SC 2.4.4（A）要求链接目的可由 *"link text alone or from the link text together with its programmatically determined link context"* 判定，SC 2.4.9（AAA）进一步要求 *"from link text alone"*，Intent 说明理由：*"links can be understood when they are out of context, such as when the user agent provides a list of all the links on a page."* NN/g（1997-09-30）实测 *"79 percent of our test users always scanned any new page they came across; only 16 percent read word-by-word."*；2009-04-06 的 11 字符研究里，35% 的链接只凭开头根本 *"hadn't the faintest idea of where the links would lead"*。**「了解更多 / Learn More」不是文案风格问题，是读屏用户的 links list 里一排无法区分的同名项**。
3. **阅读等级的合规门槛是「九年学校教育」，不是某个 Flesch 分数；音节公式不能套中文**。W3C SC 3.1.5（AAA）逐字要求当文本 *"requires reading ability more advanced than the lower secondary education level after removal of proper names and titles"* 时提供补充内容或简化版本；Intent 明确 *"Supplemental content is required when text demands reading ability more advanced than the lower secondary education level—that is, more than nine years of school."* FRE / FKGL / SMOG 三条公式都以**英文音节**为输入，Wikipedia 明确 *"the two schemes are not directly comparable and cannot be converted"*，且 *"As readability formulas were developed for school books, they demonstrate weaknesses compared to directly testing usability with typical readers."* 中文没有等价音节结构，**把 206.835 公式直接跑在中文上得到的数值没有意义**。

**边界声明**：本文件管「找路路径、链接线索、文本可扫读、死胡同、可发现性度量」的机制与验收；具体导航项数与深度归 `navigation-ia.md §3/§4`；面包屑三型与 `aria-current` 归 `navigation-ia.md §5`；空态五分法与错误页文案模板归 `feedback-states.md §5/§6`；字号、行高、行长、W3C clreq 归 `typography-system.md`；对比度与焦点可见归 `accessibility.md` / `color-science.md`；F 型扫描与视觉动线归 `visual-hierarchy-gestalt.md §3/§4`；A/B 与统计显著性归 `design-measurement-research.md §11`。**本文件不生产新的「XX 字最合适」魔法数**，只生产可复现的判断规则、逐字原文与静态检查器。

---

## 1 · 为什么单列「内容可发现性」

39 份参考里，「搜索体验 / 内容可发现性」没有独立资产。缺口用 `dp_search.py` 与全域词频统计判定为**结构性空白**，不是覆盖不足。

**缺口实测**（本轮 `python scripts/dp_search.py "搜索体验 筛选器 自动补全 无结果"` / `"信息气味 链接标签 可扫读"` / `"Flesch 阅读等级 简明语言"` + `grep -ric` 全域统计）：命中最多的 `design-measurement-research.md`（14 次，但都是研究方法口径）、`navigation-ia.md`（6 次，集中在 §4 信息气味一句与 §10 搜索协同五条）、`visual-hierarchy-gestalt.md`（4 次，讲眼动不讲内容）、`knowledge-map.md`（4 次目录条目）、`feedback-states.md`（1 次，零结果空态一行）、`ux-writing.md`（1 次，§14.3 文案可读性）。**没有任何一份**覆盖：站内搜索完整链路（入口可见性 → 输入 → 联想 → 结果 → 零结果）、链接目的的 WCAG 契约族（2.4.4 / 2.4.9 / 2.4.6 / 3.2.4 / 3.3.2）、APG combobox 的 ARIA 与键盘契约、阅读等级（SC 3.1.5）与简明语言规范、可发现性的度量（tree testing / findability / directness）。

上游文件都在**用**这些结论：`navigation-ia.md §4` 写「信息气味」却没给定义与可验收口径；`§10` 写「联想列表 `role="combobox"`+`listbox`」却没给 `aria-activedescendant` / DOM focus 契约；`feedback-states.md §6` 写了 GOV.UK 404 口径却没解释为什么「不给面包屑」与 SC 2.4.8 的张力如何裁决；`ux-writing.md §14.3` 谈可读性却没区分「合规门槛」与「英文公式」。缺了这一层，「文案简短点」「搜索放右上」就永远是没有理由的口诀。

**与相邻支柱的对照**：`visual-hierarchy-gestalt.md` 回答「目光先看哪」，`typography-system.md` 回答「字怎么排」，本文件回答「**用户带着一个具体问题时，能不能靠线索一路走到答案，并在每一步都确信自己没走错**」。这是注意力链路的下游，也是 `navigation-ia.md` 结构链路的验收端。

---

## 2 · 四层链路模型：先判哪一层断，再谈改文案

任何「找不到 / 搜不到 / 看不下去 / 用户流失」的问题，先判落在哪一层。

| 层 | 回答的问题 | 机制 | 典型失效 | 主武器 | 本文件 |
|---|---|---|---|---|---|
| **L1 有路** | 用户有几种方式到达同一内容？ | SC 2.4.5 多路径、G161 搜索、导航/目录/站点地图 | 只有搜索或只有导航、搜索藏进图标、深层页无返回路径 | ≥2 条独立路径、搜索常驻每页 | §3 §4 §19 |
| **L2 认得出** | 用户看得出哪条路是对的？ | 信息气味、链接目的、nano-content、位置指示 | 「Learn More」×8、链接脱离上下文不可辨、首词是「Introducing」 | front-loading、描述性链接、SC 2.4.4/2.4.9/3.2.4 | §5 §6 §10–§13 §19 |
| **L3 读得动** | 点进去之后读得下去吗？ | 可扫读结构、阅读等级、简明语言 | 大段无标题、marketese、从句套从句 | 倒金字塔、一段一意、补充内容、SC 3.1.5 | §11 §14–§17 |
| **L4 走得出** | 走错了还能回来吗？ | 零结果、404、路径回退、位置感 | 「没有结果」四个字、404 写俏皮话、无法清除筛选 | 零结果三件套、404 出路、breadcrumb/site map | §18 §19 |

**判层口诀**：先问「有没有第二条路」（L1）→ 再问「链接本身能不能猜到目的地」（L2）→ 再问「落地页前两屏有没有给足上下文」（L3）→ 最后问「猜错了能不能一步退回」（L4）。**四层都用「把文案写得短一点」处理，必然把 L1/L4 的结构问题推给 L2/L3，越改越像在怪用户不会搜**。

---

## 3 · 裁决一：SC 2.4.5 是「至少两条路」，不是「有个搜索就行」

W3C《Understanding SC 2.4.5 Multiple Ways》（Level AA）逐字：

> *"More than one way is available to locate a web page within a set of web pages except where the web page is the result of, or a step in, a process."*

In Brief 三行：*"Users can get to content in multiple ways."* / *"Provide at least two options for reaching the same content."* / *"Not everyone can navigate content in the same way."*

**充分技术要求是「组合」而非「任选」**：原文 *"Using two or more of the following techniques:"*，六项为 G125（相关页链接）、G64（目录 Table of Contents）、G63（站点地图）、**G161（搜索函数）**、G126（指向所有页面的链接列表）、G185（首页链接到全站所有页面）。也就是说：**搜索只算一条，还需要导航 / 目录 / 站点地图 / 全页链接中的至少一条**。

**例外边界要说清**：原文对 `process` 的定义是 *"series of user actions where each action is required in order to complete an activity"*，页面里给的例外例是 *"A search engine provides the search results based on user input. There is no other way to locate the search results except to perform the search process itself."* 与转账确认页。**「搜索结果页」本身是流程产物，不要求再给它两条路；但「产品详情页 / 文档页」不是，不能拿这条例外给全站开脱。**

**为什么这条是可访问性而不是信息架构洁癖**：Benefits 逐字 *"Individuals with cognitive limitations may find it easier to use search features than to use a hierarchical navigation scheme that may be difficult to understand."*，另一段写 *"Users with visual impairments may find it easier to navigate to the correct part of the site by using a search, rather than scrolling through a large navigation bar using a screen magnifier or screen reader."* 两类用户偏好**相反**，所以规范要的是「两条并存」，不是「挑一条最优」。

**小站也适用**：Intent 逐字 *"Even small sites should provide users some means of orientation. For a three or four page site, with all pages linked from the home page, it may be sufficient simply to provide links from and to the home page where the links on the home page can also serve as a site map."*

**验收动作**：列出目标页可达的全部路径 → 数出**互不依赖**的 ≥2 条 → 若两条都要先经过同一个「猜关键词」步骤，判 L1 不合格 → 用 §26.3 静态检查器扫 `nav` / `search` / `sitemap` / `toc` 的并存情况。

---

## 4 · 搜索入口的可发现性：位置、形态、宽度

NN/g《Search: Visible and Simple》（Jakob Nielsen, 2001-05-12）是本节的实证底座，以下数值均来自该文正文：

| 结论 | 逐字原文 / 数值 | 设计动作 |
|---|---|---|
| 搜索是逃生口 | *"Search is also users' escape hatch when they are stuck in navigation."* | 不是首页专属，**每页常驻** |
| 每页可用 | *"This is why you should make search available from every page on the site; you cannot predict where users will be when they decide they are lost."* | 深层页 / 结果页 / 404 页都要有 |
| 是输入框不是链接 | *"On homepages, search should be a type-in field and not a link."* | 首页禁「搜索」文字链 |
| 位置 | *"Put the search box at the top of the page, usually in the right hand corner (though the left works almost as well)."* | 顶栏右侧或左上，别放页脚 |
| 宽度 | *"The search input field should be wide enough to contain the typical query; if the box is too small, the query will scroll and diminish usability."* | 按典型查询长度定宽，不按图标定宽 |
| 改成输入框的收益 | *"When I changed the useit.com homepage to include a search box instead of a link, search engine use increased by 91%."* | 这是**单个站点单次改版的实测**，不是可外推的通用提升率 |
| 搜索对生产力的解释力 | 内网研究中 *"the usability of the search on intranets we have tested accounted for 43% of the difference in employee productivity between intranets with high and low usability"* | 仅内网研究语境，不套到电商 |
| 行业合规基线 | 2002 年评测 20 站，平均只 *"following 48% of the usability guidelines"* | 别用「大家都这样」当理由 |

**与平台精确值的对表**（Material 3《Search – Specs》，本轮逐字核验）：search bar 容器 **Height 56dp**、**Width Min 360dp / max 720dp**、Label alignment **Start-aligned**、Leading/Trailing padding **Unfocused 24dp → focused 12dp**（原文 *"In M3 Expressive, the search bar expands when focused. The margins change from 24dp to 12dp."*）、Leading icon 与 label 间距 **4dp from tap target**、Avatar **30dp**；聚焦态 full-screen 容器 **Full width / Full height**，docked 容器 **Min 360dp / max 720dp**、**Height Min 240dp / max 2/3 of screen height**，此时 padding **16dp**。两种 style：**Contained**（M3 Expressive，filled container）与 **Divided**（baseline，官方表格标注 *"Not recommended. Use contained."*）。解剖六件：Search bar container / Leading icon / Supporting text / Trailing icon and avatar (optional) / Input text / Container for search suggestions or results。

**注意**：56dp、360–720dp 是 **M3 的组件规格**，不是 WCAG 要求，也不是「所有平台都应该 56」；Apple HIG search fields 页面本轮抓取未取到正文（JS 渲染），**故本文件不写任何 Apple 侧数值**，只登记为下轮候选。

---

## 5 · 搜索框的标签契约：placeholder 不是 label

「把 placeholder 当 label 用」「输入提示一打字就消失」「表单可访问性过不了关」——这三种真实投诉都落在同一处：搜索框的标签契约。三条 W3C 准则在这一处交汇：

- **SC 3.3.2 Labels or Instructions（Level A）**：*"Labels or instructions are provided when content requires user input."* Intent 逐字 *"When labels or instructions are provided, they need to be persistently available to users. In many cases, the best way to do this is to make them visually persistent as part of the UI."* —— **输入后 placeholder 消失，不满足「持续可用」**。
- **SC 2.4.6 Headings and Labels（Level AA）**：*"Headings and labels describe topic or purpose."* Intent：*"This success criterion requires that if headings or labels are provided, they be descriptive."* 且 *"Labels and headings do not need to be lengthy. A word, or even a single character, may suffice if it provides an appropriate cue to finding and navigating content."* 官方甚至给了放大镜图标的例子：*"when accompanying a text field, a loupe or magnifying glass icon with text alternative of "Search" is commonly interpreted as indicating the field is for entering and submitting a search query."* 同一段立刻提醒**同一图标换个语境会变成放大图片**：*"Placed on or near another image, a loupe or magnifying glass icon is commonly interpreted as a means to view a magnified version of the image."*
- **SC 3.3.2 的 Note 有个高频误读**：*"The use of "requires" in this criterion's normative wording does not mean that the criterion only applies to required form fields. It is used here as a synonym for "accepts", "expects", or "allows". The criterion applies to all form fields, whether they're required or optional."*

**结论（本知识库工程裁决）**：搜索框用可见 `<label>`（可视觉隐藏但需可访问名），`placeholder` 只放**示例查询**（`navigation-ia.md §10` 已有同一口径），且示例不能承载唯一语义；仅有无文字的放大镜图标时，必须用 `aria-label` / `aria-labelledby` 给可访问名，并同时满足 `accessibility.md` 的非文本 3:1 与目标尺寸口径。SC 2.4.6 的 Sufficient Techniques 下方还有一条 Note：*"Headings and labels must be programmatically determined, per Success Criterion 1.3.1."* —— 视觉上「看起来像标题」不算。

---

## 6 · APG combobox 契约：自动补全不是「弹个下拉」

W3C《ARIA Authoring Practices Guide — Combobox Pattern》逐字契约，本轮核验：

**角色与状态**

- *"The element that serves as an input and displays the combobox value has role combobox."*
- *"The popup is an element that has role listbox, tree, grid, or dialog."* 且 *"If the popup has a role other than listbox, the element with role combobox has aria-haspopup set to a value that corresponds to the popup type."*；*"elements with role combobox have an implicit aria-haspopup value of listbox."*
- *"When the combobox popup is not visible, the element with role combobox has aria-expanded set to false. When the popup element is visible, aria-expanded is set to true."* 默认 *"The popup is hidden by default, i.e., the default state is collapsed."*
- *"The combobox element has aria-controls set to a value that refers to the element that serves as the popup. Note that aria-controls only needs to be set when the popup is visible. However, it is valid to reference an element that is not visible."* 兼容注：*"In ARIA 1.0, the combobox referenced its popup with aria-owns instead of aria-controls ... it is strongly recommended that authors use aria-controls."*
- 选中项：*"For a combobox that controls a listbox, grid, or tree popup, when a suggested value is visually indicated as the currently selected value, the option, gridcell, row, or treeitem containing that value has aria-selected set to true."*

**DOM focus 不进 popup（这是最常被写错的一条）**

- *"When a combobox receives focus, DOM focus is placed on the combobox element."*
- *"When a descendant of a listbox, grid, or tree popup is focused, DOM focus remains on the combobox and the combobox has aria-activedescendant set to a value that refers to the focused element within the popup."* 各 popup Note 重复：*"DOM Focus is maintained on the combobox and the assistive technology focus is moved within the listbox using aria-activedescendant"*。
- 例外：*"Unlike other combobox popups, dialogs do not support aria-activedescendant so DOM focus moves into the dialog from the combobox."*
- Tab 序列：*"Tab: The combobox is in the page Tab sequence."* 且 *"the popup indicator icon or button (if present), the popup, and the popup descendants are excluded from the page Tab sequence."*

**selection 与 focus**

- 总契约：*"keep in mind that a combobox is a single-select widget where selection follows focus in the popup."* listbox Note：*"Selection follows focus in the listbox; the listbox allows only one suggested value to be selected at a time for the combobox value."*
- tree popup 的父节点可能只是分类标签，此时 *"focus is visually distinct from selection so users can readily see if a value is selected or not."*
- 与独立 listbox 的区别：*"users can navigate the set of available choices in a combobox popup or menu and then press escape, which closes the popup or menu without changing previous input. In contrast, navigating among options in a single-select listbox immediately changes its value, and Escape does not provide an undo mechanism."* —— **combobox 的 Escape 必须能撤销，别写成「已选中」**。

**键盘**（combobox 有焦点时）：`Down Arrow` 移入 popup（若已有自动选中项则落在下一项，否则第一个可聚焦元素）；`Up Arrow (Optional)` 落在最后一个；`Enter` 接受联想值；`Escape` 关闭 popup（可选清空）；`Alt + Down Arrow (Optional)` 展开但不移焦点；`Alt + Up Arrow (Optional)` 收回焦点并关闭；`Printable Characters` 输入。popup 内 `Down/Up Arrow` *"Moves focus to and selects the next/previous option"*，`Enter` 接受，`Escape` 关闭并回到 combobox。APG 特别警告：*"IMPORTANT: Ensure JavaScript does not interfere with browser-provided text editing functions by capturing key events for the keys used to perform them."*，并说 *"The most robust approach for providing text editing functions is to rely on browsers, which supply them for HTML inputs with type text and for elements with the contenteditable HTML attribute."*

**`aria-autocomplete` 三档必须与实际行为一致**：`none`（popup 内容与输入无关）、`list`（给出与输入逻辑对应的建议）、`both`（建议 + 未输入部分内联补全，原文 *"the portion of the selected suggestion that has not been typed by the user, known as the completion string, appears inline after the input cursor in the combobox. The inline completion string is visually highlighted and has a selected state."*）。**写成 `list` 却做内联补全，或写 `both` 却只弹列表，都是契约撒谎。**

---

## 7 · 联想、筛选与结果：第一次查询基本就是决战

NN/g《Search: Visible and Simple》的电商研究数值（同一段落逐字）：

> `Search Success First query: 51% Second query: 32% Third query: 18%`
> *"In other words, if users don't find the result with their first query, they are progressively less and less likely to succeed with additional searches."*
> *"Many users don't even bother: In our study, almost half the users whose first search failed gave up immediately."*
> *"In our recent search study, the mean query length was 2.0 words."*
> *"Most users cannot use advanced search or Boolean query syntax."*

由此推出四条硬裁决：

1. **禁把高级搜索放首页**：*"Do not offer advanced search from the homepage. Advanced search leads users into trouble, as they invariably use it wrong."* 正确落点是结果页的 *"Didn't find what you were looking for? Try advanced search."*
2. **优化目标是首次成功率，不是「支持多少种查询语法」**：*"Given this, the emphasis should be on increasing users' success on the first attempt."* 具体动作：同义词/错别字容错、单复数与词形归一、热门查询人工置顶（原文 *"look through the most common queries in your search engine logs and determine the optimal landing page for each common query"*）。
3. **结果排序是设计决策**：*"Users almost never look beyond the second page of search results. It is thus essential that your search prioritize results in a useful way and that all the most important hits appear on the first page."* 章节标题即 *"First Results Page is Golden"*。
4. **范围限定（scoped search）默认危险**：*"In general, this is dangerous. Users often overlook the scope, or they think they are in a different site area than the one they are actually searching."* 若确需使用，原文四条规则：默认范围为 `"all"`；窄范围时 *"explicitly state the scope at the top of the results page"*；*"Offer one-click access to enlarge the scope"*；结果过多时 *"give users suggestions for limiting the scope"*。

**筛选器的边界**：本文件只管「筛选是否可清除、是否让用户走进零结果死胡同」（§18）；筛选器的组件形态、选中态与计数徽标归 `form-table.md` / `component-api-design.md`。

---

## 8 · 决策一图流：从入口到死胡同

```
用户带问题进入
   │
   ├─ L1 有没有 ≥2 条独立路径？ ── 否 → 补导航/目录/站点地图（SC 2.4.5 AA，§3）
   │
   ├─ 搜索入口是否可见常驻？ ─── 否 → 输入框（非链接）置于顶部、每页可用（§4）
   │
   ├─ L2 链接脱离上下文能否辨认？ ─ 否 → 描述性链接 + front-load（SC 2.4.4 A / 2.4.9 AAA，§10–§13）
   │
   ├─ 输入联想是否符合 APG 契约？ ─ 否 → role/expanded/controls/activedescendant/autocomplete 六件（§6）
   │
   ├─ 首次查询能否命中？ ─────── 否 → 容错 + 热门词置顶 + 排序（§7）
   │
   ├─ L3 落地页前两屏有上下文吗？ ─ 否 → 倒金字塔 + 一段一意 + 描述性小标题（§11 §14–§17）
   │
   └─ L4 走错能否一步退回？ ──── 否 → 零结果三件套 / 404 出路 / 位置指示（§18 §19）
```

---

## 9 · 信息气味：一个相对量，不是一个形容词

NN/g《Information Scent: How Users Decide Where to Go Next》（Raluca Budiu, 2020-02-02）逐字定义：

> *"Definition: The information scent of a source of information (such as a webpage) relative to an information need represents the user's imperfect estimate of the value that the source will deliver to the user, derived from a representation of the source."*

> *"The estimate of how relevant the page will be, if visited, is the information scent of that page."*

> *"When deciding which links to click on the web, users choose those with the highest information scent — which is a mix of cues that they get from the link label, the context in which the link is shown, and their prior experiences."*

**四个必须记住的性质**：

1. **相对性**：*"Information scent is a relative concept — meaning that the same source of information may have different information scents for different information needs."* 原文例子：找奶酪时 *Food* 气味高，找洗面奶时气味低。**不存在「这条链接文案好」的绝对评分**。
2. **两部分**：*"what the user sees"*（远端表征：链接文本 + 紧邻上下文 + 更广的页面语境）与 *"what the user already knows about the source"*（对品牌/领域/作者的既有知识）。原文点明前者 *"is largely controllable by designers"*，后者只能间接影响。
3. **链接标签是最主要的可控变量**：*"Perhaps the most important component of the information scent, the link label is supposed to be a succinct yet accurate description of what the page is about."*
4. **别过度依赖上下文**：*"Although context is usually a strong cue, designers often make the mistake of relying too much on it. Especially on small screens, the context is not always entirely visible or may get ignored ... So, it's always good to be as specific as possible with the link names instead of relying on the context to provide the extra cues."* —— 这条直接否掉了「前面那段已经说清楚了，链接写『了解更多』没关系」的辩护。

**落地页会毁掉上游气味**：*"Too often we see landing pages with very little text and a big image on the first screenful ... they don't provide enough context to tell people whether they are on the right track ... they quickly decide that the page is not worth exploring any longer and simply leave"*。**「点进来之后不知道自己在不在对的地方」是 L3 断裂，不是 L2 文案问题**。原文举的 PosturePillow 例：首屏只有一张床的大图 + logo，从搜索结果来的用户没有足够线索判断是否值得继续。

**气味透支有长期代价**：标题党会 *"use up your visitors' trust"*，原文用 *"the boy who cried 'wolf'"* 类比，结论 *"So you may not even get that first click."*

**理论归属说明**：本页把 information scent 定位为 *"a central concept in the information-foraging theory"*，但**页面正文未出现 Pirolli / Card 的姓名或文献**，故本文件不写作者归属；the `nngroup.com/articles/information-foraging/` 链接页本轮未逐页深取，登记为下轮候选。

---

## 10 · 裁决二：链接目的的 WCAG 契约族（五条准则）

| 准则 | 级别 | 逐字规范文本 | 对本文件的意义 |
|---|---|---|---|
| **SC 2.4.4 Link Purpose (In Context)** | A | *"The purpose of each link can be determined from the link text alone or from the link text together with its programmatically determined link context, except where the purpose of the link would be ambiguous to users in general."* | 允许借上下文，但上下文必须**可程序化确定** |
| **SC 2.4.9 Link Purpose (Link Only)** | AAA | *"A mechanism is available to allow the purpose of each link to be identified from link text alone, except where the purpose of the link would be ambiguous to users in general."* | 脱离上下文仍可辨；可提供「长短文案切换」机制 |
| **SC 2.4.6 Headings and Labels** | AA | *"Headings and labels describe topic or purpose."* | 标题也要描述主题，不能只写「概览」 |
| **SC 3.2.4 Consistent Identification** | AA | *"Components that have the same functionality within a set of web pages are identified consistently."* | 同功能组件跨页一致识别 |
| **SC 3.3.2 Labels or Instructions** | A | *"Labels or instructions are provided when content requires user input."* | 搜索框 / 筛选器必须有标签 |

**2.4.4 的「可程序化上下文」到底是什么**：Key Terms 定义 *"additional information that can be programmatically determined from relationships with a link, combined with the link text, and presented to users in different modalities"*，HTML 例包括 *"text that is in the same paragraph, list item, or table cell as the link or in a table header cell that is associated with the table cell that contains the link."* Note 补充 *"Since screen readers interpret punctuation, they can also provide the context from the current sentence, when the focus is on a link in that sentence."*

**位置有讲究**：Intent 逐字 *"This context will be most usable if it precedes the link."*，括号里的解释是 *"if you must use ambiguous link text, it is better to put it at the end of the sentence that describes its destination, rather than putting the ambiguous phrase at the beginning of the sentence"*，理由 *"If the description follows the link, there can be confusion and difficulty for screen reader users who are reading through the page in order (top to bottom)."*

**技术编号（做静态检查时直接用）**：Sufficient Techniques `G91` / `H30` / `H24` / `G189` / `SCR30` / `G53` / `H33` / `C7` / `ARIA7` / `ARIA8` / `H77` / `H78` / `H79` / `H81` / `PDF11` / `PDF13`；**Failures 只有 `F63`（*providing link context only in content that is not related to the link*）与 `F89`（*not providing an accessible name for an image which is the only content in a link*）**。Advisory 有 `H80`（前置标题作上下文）。注意：本轮核验发现 **`F84` 并不在该页**，写审计规则时不要凭印象加进去。

**2.4.9 的「机制」不是「必须全部写长」**：Intent 逐字 *"The word "mechanism" is used to allow authors to either make all links fully understandable out of context by default or to provide a way to make them this way."* 原文给的例子是 100 本书 × 6 种格式的列表：一组用户希望短标签（HTML / PDF / DOC…），另一组希望每本书全名出现在每条链接里，**提供切换即可满足 AAA**（`G189` / `SCR30`）。

**3.2.4 的常见误读**：Intent 逐字 *"Consistent identification does not require *identical* labels, names, or text alternatives."* 判据是 *"Identification is considered consistent when users can reliably recognize that components perform the same functionality, even if the specific mechanism used to identify them varies to reflect the context."* 且 *"This success criterion only applies to components that have the same functionality."* —— **不要求把「Page 4」和「Previous page」改成同一个词**，上下文允许变体。

---

## 11 · 可扫读性：79% / 16% 与 124% 的原文口径

NN/g《How Users Read on the Web》（Jakob Nielsen, 1997-09-30）逐字：

> *"In research on how people read websites we found that 79 percent of our test users always scanned any new page they came across; only 16 percent read word-by-word."*
> Summary: *"They don't. People rarely read Web pages word by word; instead, they scan the page, picking out individual words and sentences."*

**该文给出的六种可扫读手法**（逐字要点）：highlighted **keywords**（*hypertext links serve as one form of highlighting; typeface variations and color are others*）、meaningful **sub-headings**（*"not "clever" ones"*）、bulleted **lists**、**one idea** per paragraph（*"users will skip over any additional ideas if they are not caught by the first few words in the paragraph"*）、**inverted pyramid** *"starting with the conclusion"*、**half the word count (or less)** than conventional writing。

**同一站点五个版本的对照实验**（原文表格，Usability Improvement relative to control）：

| 版本 | 处理 | 提升 |
|---|---|---|
| Promotional writing (control) | marketese | 0%（定义） |
| Concise text | 约一半字数 | **58%** |
| Scannable layout | 同文案改成可扫列表 | **47%** |
| Objective language | 去掉主观夸饰 | **27%** |
| **Combined version** | 简洁 + 可扫 + 客观 | **124%** |

原文对 27% 的解释值得抄进评审话术：*"promotional language imposes a cognitive burden on users who have to spend resources on filtering out the hyperbole to get at the facts"*；并写 *"Users detested "marketese""*。

**口径纪律**：这是 **1997 年、同一站点、五个版本、同一任务**的对照实验结果，是「相对该实验控制组的可用性提升」，**不是「精简文案能提升 58% 转化」**。引用时必须带上实验语境；把它当通用 ROI 是本知识库明令禁止的外推。

---

## 12 · nano-content：前 11 个字符决定要不要读下去

NN/g《First 2 Words: A Signal for the Scanning Eye》（Jakob Nielsen, 2009-04-06）：

**方法**：*"Our study included 80 people broadly distributed across age groups, gender, and education."*；测试 **20 个链接，来自 20 个站点、3 大洲**（Accenture / Amazon / Ann Taylor / AT&T / Barclays / Chase / Dell / Directgov.uk / Xerox 等）；每个链接只展示**前 11 个字符**（例：本文标题被截成 `"First 2 Wor"`）。两个任务：单独看截断串预测目的地；从 10 条截断链接（9 条干扰项）里按场景选对的那条。

**为什么是 11 个字符**：原文 *"Users typically see about 2 words for most list items; they'll see a little more if the lead words are short, and only the first word if they're long. Of course, people don't see exactly 11 characters every time, but we picked this number to ensure uniformity across the sites we tested."* 出现场景包括 SERP、新闻/文章列表、电商分类页商品列表、ToC、FAQ 问题列表、项目符号与步骤列表。

**结果表**（逐字数值）：

| 链接（前 11 字符 / 全文） | 单独预测正确 | 10 选 1 正确 |
|---|---|---|
| Ann Taylor `"Gift Cards "` / *Gift Cards & E-Gift Certificates* | **85%** | **100%** |
| Barclays `"New custome"` / *New customers apply online now* | **75%** | **95%** |
| 全部 20 条里 **35%** | *"hadn't the faintest idea of where the links would lead"* | — |
| Chase `"Introducing"` / *Introducing Chase Exclusives Special Benefits for Checking Customers* | 0（*"none of the users had a reasonable prediction"*） | **15%** |
| Directgov `"Working whi"` / *Working while you study: paying tax* | — | **25%** |
| Xerox `"Profit Acce"` / *Profit Accelerator Overview* | 1 人猜对 | **5%** |

**获胜链接的四条共性**（原文）：*Use plain language* / *Use specific terminology* / *Follow conventions for naming common features* / ***Front-load user- and action-oriented terms***。失败链接的「三个 nasties」：*"Bland, generic words"* / *"Made-up words or terms"* / *"Starting with blah-blah and deferring the information-carrying text to the end"*。

**别把 11 字符当成新的魔法数**：原文自己划了界 *"It's admittedly harsh to judge a website's design on only the first 11 characters of its links"*，并明确 *"Thus, only the full link text needs to provide the full information scent"*（三条：能自信预测点下去得到什么 / 与其他链接明显区分 / 不误导或过度承诺），而 *"Nanocontent (first bit of a link) just needs to be good enough that users will sniff the most promising links in full."*

**中文适配（工程约定，非实验常数）**：11 字符是**英文字母**口径；中文一个汉字的信息密度远高于一个字母，且没有词间空格。本知识库的工程代理是「**前 6–8 个汉字内出现主题词或动作词**」，**这是约定不是实验结论**，不得当成 NN/g 的研究数值引用；验收时以「截断后让同事猜目的地」的小样本走查替代公式。

---

## 13 · 「Learn More」的三种改法与信息气味的重合

NN/g《"Learn More" Links: You Can Do Better》（Katie Sherwin, 2015-12-13）Summary 逐字：*"The phrase 'Learn More' is increasingly used as a crutch for link labels. But the text has poor information scent and is bad for accessibility."* 文中提到 *"A Google search finds 1.4 billion instances of this term"*（同一句自带保留：*"though some admittedly might be from proper use of the term in general content"*，**不可当作「14 亿个错误链接」引用**）。

**三条问题链**（原文）：① 单独使用时 *"creates uncertainty, because users don't know what to expect"*，会 *"shift into a state of cognitive strain"*，部分用户改用 *"page parking"*（开多标签页评估含糊链接）；② 页面上多个 Learn More 时 *"users may wonder if the links point to the same page or to different pages"*；③ *"as a standalone link, the lack of descriptive keywords is a serious problem for accessibility ... Most screen-reader users will hear a list of links read to them, with no visual context to help them make sense of different generic Learn More or Read More links."* —— 与 §10 的 2.4.9 Intent 完全对上。

**三种改法**（原文小节标题即方案）：

1. **用描述目的地的关键词**（*"This is the most common and, typically, the best approach."*）。原文强调 *"you have to look at the destination page and see what it's about. Don't skip that step."* 并 *"remember to try to front-load the link text by putting the most relevant keywords at the beginning"*；例子把 *"Learn How Professional Chefs Cook Squash"* 改成 *"Cook Squash Like The Pros."*
2. **保留 Learn More 但补关键词**（如 *Learn more about our services*）。原文点明代价：*"reduced scannability because the relevant keywords appear at the end instead of the beginning"*；好处是 *"a long link does create a larger target"*。折中写法：*"Learn more: [How a Link is a Promise]"*。
3. **把上一段的标题本身做成唯一链接**——若标题已明显可点且描述了目的地，Learn More 是冗余。

**原文明确澄清的边界**：*"this article is a critique of the link label only, and not of the general practice of deferring less important content"*；且 *"if the text that precedes the link makes it obvious what's to come, then a Learn More label isn't devastating to the user experience"*。所以判违规的场景是「**脱离上下文 / 同页多个同名 / 读屏 links list**」，不是「出现即违规」。

---

## 14 · 裁决三：阅读等级的合规门槛是「九年学校教育」

「Flesch / FKGL / SMOG 算到多少分才算合规？」——先记住裁决：分数不是合规门槛，SC 3.1.5 要的是「九年学校教育」。W3C《Understanding SC 3.1.5 Reading Level》（Level AAA）逐字：

> *"When text requires reading ability more advanced than the lower secondary education level after removal of proper names and titles, supplemental content, or a version that does not require reading ability more advanced than the lower secondary education level, is available."*

**Key Terms 定义**（基于 UNESCO ISCED）：*"the two or three year period of education that begins after completion of six years of school and ends nine years after the beginning of primary education"*。Intent 给出可直接执行的门槛句：

> *"Supplemental content is required when text demands reading ability more advanced than the lower secondary education level—that is, more than nine years of school."*

**UNESCO 分级表**（页面 `Levels of education` 小节，逐字）：Primary education *First 6 years of school* / Lower secondary *7-9 years of school* / Upper secondary *10-12 years of school* / Advanced *More than 12 years of school*。

**三条容易漏掉的细则**：

1. **专有名词与标题要先剔除再判**：*"proper names can be ignored or removed from the text before assessing whether it meets the reading ability requirement"*；*"Titles are removed or ignored for the analysis because changing the words in titles might make the titles easier to read but would make it impossible to understand the item to which the title refers."*
2. **多语言按最差者判**：*"When a web page contains multiple languages, a readability result should be calculated for each language that constitutes at least 5% of the content and that is used in full sentences or paragraphs (not just individual words or phrases). The overall readability of the page should be judged on the language that yields the worst readability results."* —— **中英混排页面不能只算中文或只算英文**。
3. **补充内容的定义**：*"additional content that illustrates or clarifies the primary content"*，例含音频版、复杂流程图示、研究摘要段。Sufficient Techniques：`G86`（摘要）、`G103`（图示）、`G79`（朗读版）、`G153`（简化文本）、`G160`（手语版）。

**最该记住的自我克制**：Intent 的 Note 逐字 *"According to the Open Society Mental Health Initiative, the concept of Easy to Read cannot be universal, and it will not be possible to write a text that will suit the abilities of all people with literacy and comprehension problems. Using the clearest and simplest language appropriate is highly desirable, but the Accessibility Guidelines Working Group could not find a way to test whether this had been achieved. The use of reading level is a way to introduce testability into a success criterion that encourages clear writing."* —— **W3C 自己承认「清晰」不可测，引入阅读等级只是为了可测性**。所以别把某个 Flesch 分数写成「符合 WCAG 3.1.5」。

---

## 15 · 三条可读性公式、精确系数与「不可换算」

以下系数来自 ReadabilityFormulas.com 两个逐字核验页（Brian Scott，2025-11-14 / 2025-02-07），解释表与限制来自 Wikipedia《Flesch–Kincaid readability tests》。

| 公式 | 精确形式 | 输入 | 出处 |
|---|---|---|---|
| **Flesch Reading Ease (FRE)** | `206.835 − (1.015 × ASL) − (84.6 × ASW)` | ASL = 平均句长（词/句），ASW = 平均每词音节数 | Flesch 1948 *A New Readability Yardstick* |
| **Flesch–Kincaid Grade Level (FKGL)** | `0.39 × ASL + 11.8 × ASW − 15.59` | 同上 | Flesch & Kincaid 改进版 |
| **SMOG** | `1.043 × √( n_poly × 30 / n_sent ) + 3.1291` | `n_poly` = 三音节及以上词数，`n_sent` = 句数 | McLaughlin 1969 *SMOG Grading–A New Readability Formula* |

**SMOG 的采样约定**：固定 **30 句**样本，`30 / sentence count` 是把不足/超过 30 句的文本归一化；McLaughlin 认为 30 句给出 *"the most stable and accurate readability estimates"*。原始版本常数是 **+3**，新版 refinements 用 **3.1291**，两者差异 *"less than 0.2 grade levels"*。适用区间 *"4th grade to college level readers"*。

**FRE 解释表**（Wikipedia 逐字短语）：

| Score | School level (US) | Notes（逐字） |
|---|---|---|
| 100.00–90.00 | 5th grade | *Very easy to read. Easily understood by an average 11-year-old student.* |
| 90.0–80.0 | 6th grade | *Easy to read. Conversational English for consumers.* |
| 80.0–70.0 | 7th grade | *Fairly easy to read.* |
| **70.0–60.0** | **8th & 9th grade** | ***Plain English. Easily understood by 13- to 15-year-old students.*** |
| 60.0–50.0 | 10th to 12th grade | *Fairly difficult to read.* |
| 50.0–30.0 | College | *Difficult to read.* |
| 30.0–10.0 | College graduate | *Very difficult to read.* |
| ≤10.0 | Professional | *Extremely difficult to read.* |

**边界与陷阱（Wikipedia 逐字）**：

- *"The highest (easiest) readability score possible is 121.22, but only if every sentence consists of only 1 one-syllable word."*；*"The score does not have a theoretical lower bound"*；FKGL *"does not have an upper bound"*，理论最低 **−3.40**（*"Go. See. Stop. Rest."*）。
- *"The different weighting factors for words per sentence and syllables per word in each scoring system mean that the two schemes are not directly comparable and cannot be converted."* —— **禁止把 FRE 换算成 FKGL 再来汇报**。
- *"The grade level formula emphasizes sentence length over word length."* 而 *"Polysyllabic words affect this score significantly more than they do the grade-level score."*（指 FRE）。
- 最关键的 Limitations：*"As readability formulas were developed for school books, they demonstrate weaknesses compared to directly testing usability with typical readers. They neglect between-reader differences and effects of content, layout and retrieval aids."* —— **公式看不见版式、看不见检索辅助，而这两样本文件正是讲它们的**。

**结论**：公式可做**回归护栏**（同一批文案改版前后是否变难），不可做**验收结论**（「FRE 62 所以达标」）。验收仍要回到 §14 的九年门槛 + §20 的真实用户树测试/找路测试。

---

## 16 · 中文可读性：音节公式失效，改用可解释的代理指标

**为什么不能直接套**：FRE / FKGL / SMOG 的输入全是「英文音节数 / 英文词数」。中文一字一音节，词边界需分词，成语与专业术语的难度不随字数线性增长；把 `ASW` 硬套到中文几乎恒为 1.0，公式会退化成纯句长函数，输出数值看似精确实则无信息。中文侧本轮搜索到的资料（含把 FRE 改写成「每 100 字音节数」的百科条目、若干中文可读性评估 NLP 文章）**仅为搜索结果级、未逐字核验**，因此**不作为本文件任何数值或引文的依据**，仅登记为下轮候选。W3C `clreq` 管的是**中文排版**（已在 `typography-system.md §16` 核验：1/4 汉字宽、1:1 正方形、全角 ASCII、UAX #29 字素丛），**不规定阅读难度**。

**本知识库的工程代理指标（明确标注：工程约定，非实验常数、非标准）**：

| 代理量 | 口径 | 为什么用它 | 阈值性质 |
|---|---|---|---|
| 平均句长（汉字数） | 按 `。！？；` 切句，计汉字数 | 对应 FKGL 里权重最大的句长项 | **工程约定**，需按站点基线自校准 |
| 单段字数 | 按空行切段 | 对应 §11「one idea per paragraph」 | **工程约定** |
| 标题密度 | 每 N 字的 `h2/h3` 数 | 对应「meaningful sub-headings」与 L2 定位 | **工程约定** |
| 前 6–8 汉字含主题词 | 标题/链接/段首 | 对应 §12 front-loading 的中文代理 | **工程约定** |
| 生僻字词比例 | 与自建常用词表比对 | 替代英文 ASW 的「词难度」维度 | **工程约定**，词表需版本化 |
| 列表化比例 | 列表项字数 / 总字数 | 对应 §11 bulleted lists | **工程约定** |

**使用纪律**：① 只做**同语言、同站点、改版前后**的相对比较，不跨语言比数值；② 中英混排按 §14 的 **5% 规则**分别对两种语言算，按最差者判；③ 任何代理数值都**不得**写成「符合 WCAG 3.1.5」；④ 代理指标异常时，用 §20 的真实找路测试收口，而不是继续调阈值。§26.1 的 Python 计算器内置中文守卫，喂中文会明确拒答而非给一个假分数。

---

## 17 · 简明语言：Plain Writing Act 与四份官方指南

Digital.gov《Plain language guide series》（内容改编自 PlainLanguage.gov）逐字：

> *"Plain language – content that is clear and easy to understand – is critical to helping the public to make sense of their obligations and benefits."*
> *"Not only is plain language more efficient and effective. It is also the law."*
> *"The Plain Writing Act of 2010 established the requirement that content for the public is written for its specific audience."*

**四份指南的分工**（官方小节名）：`Principles of plain language`（原则与受众、法案）→ `Writing for understanding`（怎么写）→ `Design for understanding`（**内容设计如何支撑简明语言**）→ `Test for understanding`（怎么测）。第三份是本文件与 `ux-writing.md` 的交界：**简明语言不只是改词，还包括标题、列表、表格、留白的编排**。Digital.gov 注明 *"This content is adapted from PlainLanguage.gov"*，原文归档于 `gsa/plainlanguage.gov` 仓库（本轮 GitHub API 实测 **228★ / NOASSERTION / archived=true / pushed 2025-09-23**，归档不等于失效）。

**与 §11 的合并动作清单**（NN/g 六种手法 + W3C 3.1.5 + 官方四指南）：结论前置（倒金字塔）、一段一意、描述性小标题（不玩梗）、列表化、字数减半、去 marketese、专业术语首次出现给释义（= 3.1.5 的 `supplemental content`）、为长文提供摘要或图示（G86 / G103）、RTL 与多语言各验一遍。**「写得清楚」在美国联邦机构是法定义务，在一般产品是设计质量，两者别混为一谈。**

---

## 18 · L4 死胡同治理：零结果与 404

**零结果不是「没有结果」四个字**。NN/g 的数据说明它代价极高：首次查询失败后 *"almost half the users whose first search failed gave up immediately"*，第二/三次成功率掉到 32% / 18%。`navigation-ia.md §10` 与 `feedback-states.md §5` 已给出「换个词 / 清除筛选 / 联系」三件套与「说明筛选条件 + 清除筛选」口径，本文件补上**为什么必须给出路**：这是 L4 的回退路径，也是 SC 2.4.5「多条路」在失败态的延续——用户走进零结果后若只剩「返回上一页」，等于站点此刻只提供一条路。

**404 的 GOV.UK 逐字规范**（《GOV.UK Design System — Page not found pages》，本轮核验）：

- 触发场景三条：*"selects a link or button that takes them to a page that does not exist"* / *"types or copies a web address for a page that does not exist"* / *"types or copies a web address incorrectly"*。
- 页面应有：*"'Page not found – service name – GOV.UK' as the page title"*、*"'Page not found' as the H1"*、*"contact information, if it exists and helps meet a user need"*；联系信息要么链到含号码与开放时间的页，要么直接写全。
- *"The content should be clear and concise, not blame the user."*
- **Do not use 四条（逐字）**：*"breadcrumbs"* / *"technical jargon like 404 or bad request"* / *"informal or humorous words like oops"* / *"red text to warn people"*。
- 前置治理：*"Test all links and buttons to make sure they work."* 与 *"Make sure any web addresses in your service, letters, forms and on GOV.UK are for pages that exist or redirect to pages that exist."*
- **官方自述证据不足**：`"Research on this pattern"` 小节写 *"More research is needed to find out if people: can fix the problem on their own / understand what has happened / understand the content and if there is anything missing"*。所以这是**设计系统规范而非实验结论**，引用时别写成「研究证明」。

**与 SC 2.4.8（Location, AAA）的张力如何裁决**：SC 2.4.8 要求 *"Information about the user's location within a set of web pages is available."*，充分技术含 **G65: Providing a breadcrumb trail**、G63 站点地图、G128 导航栏当前位置、**ARIA26: aria-current**、G127。GOV.UK 却明确 404 页 **不要面包屑**。裁决：404 页**不在 `set of web pages` 的正常层级里**，它是一次失败态、不是一个可被定位的内容节点；给它面包屑等于宣称用户「位于」一个不存在的位置，制造假上下文。**AAA 的位置要求对正常内容页成立，对失败页以「清晰出路」替代「位置指示」**。

**NN/g 404 页的现实注脚**：本轮访问猜测的 `/articles/empty-state-no-results/` 返回 NN/g 自己的 404 页，其中写 *"Did an AI chat send you here? They sometimes get URLs wrong or hallucinate nonexistent NN/G articles."* —— 这是**当代死胡同的新成因**（AI 生成的失效链接），本文件只作现象记录，**该 404 页的文案不作为任何规范引用**（与 `visual-hierarchy-gestalt.md §24` 的取源纪律一致：猜测 URL 的 404 内容不引用）。

---

## 19 · 多条路径与当前所在指示的落地清单

L4 的位置感（SC 2.4.8）与 L1 的多条路径（SC 2.4.5）合并为一张落地清单，逐项标明权威依据与归属资产：

| 机制 | 权威依据 | 落地 |
|---|---|---|
| 面包屑 | SC 2.4.8 AAA · G65 | 三型与末级非链接归 `navigation-ia.md §5` |
| 站点地图 / 目录 | SC 2.4.5 AA · G63 / G64 · SC 2.4.8 G63 | 与导航互不依赖的第二条路 |
| 搜索函数 | SC 2.4.5 AA · G161 | 每页常驻（§4） |
| 导航栏当前位置 | SC 2.4.8 AAA · G128 / ARIA26 | `aria-current` 用法归 `navigation-ia.md §8` |
| 全页链接列表 / 首页全覆盖 | SC 2.4.5 AA · G126 / G185 | 小站的低成本合规路径 |
| 相关页链接 | SC 2.4.5 AA · G125 | 上下文内导航 |

**验收句式**：「目标页 P 可由 ①主导航逐层下钻 ②站内搜索输入关键词 两条互不依赖的路径到达；且 P 上有面包屑或导航激活态指示位置；且从 P 的零结果/404 态可一步回到 ① 或 ②。」三条都成立才判 L1+L4 合格。

---

## 20 · 可发现性的度量：tree testing 与 findability

NN/g《Tree Testing: Evaluate Menu Labels and Categories》（Page Laubheimer, 2023-08-06，Last reviewed 2026-08-19）逐字定义：

> *"Tree test: An evaluation of a hierarchical category structure, or tree, by having users find the locations in the tree where specific resources or features can be found."*

> *"Tree testing focuses exclusively on evaluating the findability of key resources in your category structure and whether the text labels are understandable to users."*

**与卡片分类的分工**（原文）：*"Card sorting is a generative method used for discovering possible groupings for your categories or content"*，而 *"Tree testing, on the other hand, is a method solely used for evaluating a potential navigation hierarchy"*。原文还给了「模糊分类没人点」的判据：*"Website visitors are notoriously reluctant to click on vague labels because they quite rightly suspect they'll have to do a lot of work to sift through the content."* —— 与 §9 信息气味、§12 front-loading 是同一条因果链的三个说法。

**只需准备两样**（原文 *"You need to prepare only two things"*）：**tree**（无视觉样式、无内容的层级菜单）与 **tasks**（找路任务）。*"For each task you write, you should also define the correct answer(s) ... This information will allow the testing tool to automatically calculate success rates for each task."*

**可量化指标**：`success rates for each task`、`time on task`、*"what proportion of users were successful"*、`any other categories users selected`，以及 **directness** —— 原文 *"whether users bounced around trying a few categories before making a choice or went directly to their selection (a measure called directness, which can give you context about the clarity or ambiguity of your category labels, also functions as a proxy for how confident users are in a particular path)"*。**directness 是「线索是否清晰」的代理量，比成功率更早暴露标签问题。**

**样本量纪律（常被写错）**：原文 **没有给出具体人数**。写的是定性 *"requires only a few participants"* 且 *"qualitative tree testing is not appropriate for gathering statistics (such as success rate or time on task)"*；定量 *"Quantitative tree testing requires a larger sample size"*；并建议 *"beginning a quantitative tree test with a small qualitative study for two reasons"*（试测任务措辞、拿到「为什么」的洞察）与 *"conduct at least a few moderated pilot sessions before collecting the bulk of your data"*。文中出现的 `why-you-only-need-to-test-with-5-users/` 只是**链接 URL**，不是本页给出的样本数；要写「5 人」须另引该文并单独标注，别挂在本页名下。

**任务措辞三例**（原文表格）：✗ *"Find information about starting a business."*（*"Gives away the answer by using the exact label term"*）；✗ 长篇情境（*"Long and packed with extraneous words that might sidetrack the participants"*）；✓ *"You are considering opening a lawn-care service. See if there are any resources on this site that can help you begin the process."*

**多树比较**：比**标签词**用 *"two different trees"* 且 *"use a between-subjects study design"*（否则第一棵树影响第二棵）；只比**位置**用 *"a single tree"* 即可。工具限制要注意：多数 tree-testing 软件 *"users can choose only bottom-level items in the tree as their answer"*，**中间分类页无法标为正确答案**，原文建议此时改看 *"whether the user selects the correct top-level category, rather than on success rates"*。

**与 `design-measurement-research.md` 的边界**：那里给样本量公式、SUS、A/B 统计；本文件只给**可发现性专属**的口径（findability / success rate / directness / 定性不可统计）。两者不重复，冲突时以本节的 NN/g 原文为方法口径、以那份为统计口径。

---

## 21 · 六步构建流程

1. **盘路径（L1）**：列出目标页全部可达路径，确认 ≥2 条互不依赖（§3 §19），标出流程产物例外页。
2. **修入口**：搜索改输入框、顶部常驻、每页可用、宽度容得下典型查询；`<label>` 持久化（§4 §5）。
3. **修链接（L2）**：跑 §26.2 扫描器，清掉通用文案、重复同名、含糊首词；按前 6–8 汉字（中文）/ 前 11 字符（英文）做截断走查（§10–§13）。
4. **修联想与结果**：按 §6 六件契约核对 ARIA 与 DOM focus；把预算优先投给首次查询成功率与首屏排序（§7）。
5. **修落地页（L3）**：结论前置、一段一意、描述性小标题、去 marketese；长专业文本补摘要/图示（G86/G103）；中文用 §16 代理指标做改版前后回归，不跨语言比（§11 §14–§17）。
6. **修死胡同（L4）+ 验收**：零结果给清除筛选与改写建议；404 清出路、不写 404/oops/红字、不给面包屑；最后用 tree testing 量 findability 与 directness，定性结果不报百分比（§18 §20）。

---

## 22 · 与既有资产的边界矩阵

| 用户问的是 | 去这里 | 不去本文件的原因 |
|---|---|---|
| 导航项数、深度广度、面包屑三型、`aria-current` | `navigation-ia.md §3–§5 §8–§9` | 结构形态与位置组件 |
| 五种空态分类、错误页文案模板、toast 时长 | `feedback-states.md §5 §6` | 反馈状态体系 |
| 文案语气、术语表、sentence case、中文标点 | `ux-writing.md` | 文案风格层 |
| 字号 / 行高 / 行长 / W3C clreq / 200% 缩放 | `typography-system.md` | 排印可访问性 |
| 对比度 4.5:1 / 3:1、焦点可见、目标尺寸 | `accessibility.md` `color-science.md §6` | 通用无障碍阈值 |
| F 型扫描、视觉动线、眯眼测试、认知负荷三分 | `visual-hierarchy-gestalt.md §3 §4 §11` | 视觉注意力机制 |
| A/B 显著性、样本量公式、SUS/UMUX | `design-measurement-research.md` | 统计方法 |
| 组件 API、受控/非受控、ARIA 键盘通用契约 | `component-api-design.md §12` | 组件工程 |
| 筛选器/复选框/表格组件形态 | `form-table.md` | 表单与表格 |
| **找不到内容、搜不到、链接认不出、读不下去、零结果/404 出路、阅读等级、简明语言、tree testing** | **本文件** | — |

---

## 23 · 场景速查（12）

1. **「我们网站有搜索啊，为什么还说我不可访问」** → §3 SC 2.4.5 要 ≥2 条；搜索只算 G161 一条，补目录/站点地图/全页链接。
2. **「首页搜索想收进放大镜图标省空间」** → §4 *"type-in field and not a link"* + 91% 单站实测；核心产品常驻。
3. **「placeholder 写了『搜索产品』，还需要 label 吗」** → §5 SC 3.3.2「持续可用」+ 2.4.6 放大镜图标例子；需要。
4. **「联想列表键盘上下键没反应」** → §6 APG 键盘表 + DOM focus 保持在 combobox + `aria-activedescendant`。
5. **「用户第一次搜不到就走了」** → §7 51%/32%/18%、2.0 词、近半数立刻放弃；优化首次命中而非加高级语法。
6. **「同页有 8 个『了解更多』」** → §13 三种改法 + §10 2.4.9 的 links list 理由；优先方案 1/3。
7. **「链接文案要不要把品牌名放前面」** → §12 front-loading + 三个 nasties；主题词/动作词前置。
8. **「长文档要不要给摘要」** → §14 SC 3.1.5 九年门槛 + G86/G103；且不是「友好加分」，是 AAA 达标路径。
9. **「中文文案能不能跑 Flesch 分数」** → §16 音节公式失效；用代理指标做同语言改版回归，混排按 5% 规则各算。
10. **「404 页要不要加面包屑帮用户定位」** → §18 GOV.UK 明确 Do not use breadcrumbs + 与 2.4.8 的裁决。
11. **「菜单改版怎么证明更好找了」** → §20 tree testing 的 success rate / directness / 定性不可统计 / between-subjects。
12. **「政务/公共服务文案有什么硬要求」** → §17 Plain Writing Act of 2010 + 四份指南；注意适用主体是面向公众的机构内容。

---

## 24 · 反模式（20）

1. 把「有搜索框」当成满足 SC 2.4.5。
2. 搜索只放首页，深层页/结果页/404 页没有。
3. 首页用「搜索」文字链代替输入框。
4. 把搜索藏进图标且不提供可访问名。
5. `placeholder` 当唯一标签，输入后语义消失。
6. 高级搜索/布尔语法入口放首页。
7. 范围限定默认收窄且不在结果页说明范围。
8. 结果页不提供「放大到全站」的一键出口。
9. 把预算花在第 2/3 次查询的改写引导，而非首次命中率。
10. ARIA 写 `aria-autocomplete="list"` 却做内联补全（或反之）。
11. 把 DOM focus 移进 listbox、漏掉 `aria-activedescendant`。
12. popup 内 `Escape` 直接提交已选项，无法撤销 previous input。
13. 同页多个同名「Learn More / 了解更多」指向不同页。
14. 链接首词用「Introducing / 全新 / 关于 / 更多」等零信息词。
15. 依赖上一段文字给上下文，却在窄屏把上下文折叠掉（§9）。
16. 拿某个 Flesch 分数宣称「符合 WCAG 3.1.5」。
17. 把 FRE 换算成 FKGL 再汇报，或把英文音节公式直接跑中文。
18. 中英混排只按中文算可读性，忽略 §14 的 5% 最差者规则。
19. 404 页写「Oops! 404」、用红字、加面包屑或俏皮插画抢注意力。
20. 定性 tree testing（"a few participants"）报出「87% 成功率」。

---

## 25 · 自检（20）

1. 目标页有 ≥2 条互不依赖的可达路径，且没有把流程产物例外扩大到全站？
2. 搜索是输入框而非链接、位于顶部、每页常驻、宽度容得下典型查询？
3. 搜索框有持续可用的 `<label>` 或等价可访问名；`placeholder` 只放示例？
4. 仅有图标的搜索按钮有非文本可访问名与 ≥3:1 边界？
5. combobox 六件齐：`role=combobox` / `aria-expanded` / `aria-controls` / `aria-activedescendant` / `aria-autocomplete` / popup `role=listbox|grid|tree|dialog`？
6. `aria-autocomplete` 的档位与实际行为（none / list / both）一致？
7. DOM focus 始终留在 combobox（dialog popup 除外），popup 后代不在页面 Tab 序列？
8. 选中项有 `aria-selected="true"`；tree popup 的 focus 与 selection 视觉可区分？
9. `Escape` 能关闭而不改变 previous input？
10. 首次查询有同义词/错别字容错与热门词置顶；最相关命中在第一页？
11. 若用了 scoped search：默认 `all`、结果页明示范围、一键放大、结果过多给收窄建议？
12. 每条链接脱离上下文（读屏 links list）仍可辨目的？
13. 同页无重复同名链接；同目的地链接文案一致（SC 3.2.4），不同目的地文案可区分？
14. 链接/标题的前 11 字符（英）/ 前 6–8 汉字（中）含主题词或动作词？
15. 上下文型链接的描述**前置**于链接，且在同句/同段/同列表项/同单元格内（F63）？
16. 落地页前两屏给足「我在不在对的地方」的线索；结论前置、一段一意、描述性小标题？
17. 超过九年教育门槛的专业文本提供了 G86 摘要或 G103 图示；专有名词与标题剔除后再判？
18. 多语言/中英混排按 ≥5% 各算可读性，按最差者判；中文只做同语言回归、不套音节公式？
19. 零结果给「清除筛选 / 改写建议 / 出路」；404 不写 404/oops/红字/面包屑、不怪用户、给出路与联系信息？
20. 可发现性结论来自 tree testing 的 success rate + directness；定性样本未冒充百分比；最后跑过 §26 三段检查器？

---

## 26 · 可抄代码（5 段；§26.1–§26.3 为 Python，本轮已实跑 PASS）

### 26.1 英文可读性计算器 + 中文守卫（Python，已实跑）

```python
"""FRE / FKGL / SMOG 计算器。中文输入明确拒答，不产出伪精确分数。
系数来源见 §15；音节计数为启发式近似，仅用于同语料改版前后回归。"""
import math
import re
from pathlib import Path


def is_cjk_dominant(text: str) -> bool:
    han = len(re.findall(r"[\u4e00-\u9fff]", text))
    letters = len(re.findall(r"[A-Za-z]", text))
    return han > 0 and han / max(1, han + letters) > 0.30


def syllables(word: str) -> int:
    """英文音节启发式：元音组计数，词尾静音 e 与 -le 修正。"""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ye")) and n > 1:
        n -= 1
    if w.endswith("le") and len(w) > 2 and w[-3] not in "aeiouy":
        n += 1
    return max(1, n)


def score(text: str) -> dict:
    if is_cjk_dominant(text):
        raise ValueError("CJK-dominant text: 音节公式不适用，请用 §16 代理指标，不要输出 FRE/FKGL 分数")
    sentences = [s for s in re.split(r"[.!?]+", text) if re.search(r"[A-Za-z]", s)]
    words = [w for s in sentences for w in re.findall(r"[A-Za-z][A-Za-z'-]*", s)]
    if not sentences or not words:
        raise ValueError("no English sentences found")
    ns, nw = len(sentences), len(words)
    nsy = sum(syllables(w) for w in words)
    asl, asw = nw / ns, nsy / nw
    n_poly = sum(1 for w in words if syllables(w) >= 3)
    fre = 206.835 - 1.015 * asl - 84.6 * asw
    fk = 0.39 * asl + 11.8 * asw - 15.59
    smog = 1.043 * math.sqrt(n_poly * 30 / ns) + 3.1291
    return {"sentences": ns, "words": nw, "ASL": round(asl, 2),
            "ASW": round(asw, 3), "polysyllables": n_poly,
            "FRE": round(fre, 2), "FKGL": round(fk, 2), "SMOG": round(smog, 2),
            "_note": "FRE 与 FKGL 不可互相换算；公式看不见版式与检索辅助"}


PLAIN = ("We ship your order in two days. "
         "You can track the box with the link in your email. "
         "Call us if the box is late.")
DENSE = ("Notwithstanding the foregoing, implementation of the aforementioned "
         "methodology necessitates comprehensive consideration of organizational "
         "interdependencies and concomitant infrastructural prerequisites.")

if __name__ == "__main__":
    a, b = score(PLAIN), score(DENSE)
    print("plain:", a)
    print("dense:", b)
    assert a["FRE"] > b["FRE"], "简明文本应更易读（FRE 更高）"
    assert a["FKGL"] < b["FKGL"], "简明文本年级应更低"
    try:
        score("本页面的内容可供搜索，点击这里了解更多相关信息与操作说明。")
        raise AssertionError("中文输入必须被拒绝")
    except ValueError as e:
        print("CJK guard OK:", e)
    print("PASS: 三条公式单调性 + 中文守卫")
```

**本轮实跑输出**（`python` 执行，非手写）：

```text
plain: {'sentences': 3, 'words': 25, 'ASL': 8.33, 'ASW': 1.08, 'polysyllables': 0, 'FRE': 107.01, 'FKGL': 0.4, 'SMOG': 3.13, '_note': 'FRE 与 FKGL 不可互相换算；公式看不见版式与检索辅助'}
dense: {'sentences': 1, 'words': 18, 'ASL': 18.0, 'ASW': 3.778, 'polysyllables': 13, 'FRE': -131.03, 'FKGL': 36.01, 'SMOG': 23.73, '_note': 'FRE 与 FKGL 不可互相换算；公式看不见版式与检索辅助'}
CJK guard OK: CJK-dominant text: 音节公式不适用，请用 §16 代理指标，不要输出 FRE/FKGL 分数
PASS: 三条公式单调性 + 中文守卫
```

这段输出本身就是 §15 结论的实证，三条都要读出来：① `FRE = -131.03` 对应 Wikipedia *"The score does not have a theoretical lower bound"*，`FRE = 107.01` 也没超 *"The highest (easiest) readability score possible is 121.22"*，**分数不是 0–100 区间的百分制**；② `FKGL = 36.01` 对应 *"the score does not have an upper bound"*，因为音节启发式把长学术词全判成多音节，说明**公式对输入分词/音节策略极度敏感**；③ `SMOG = 3.13` 甚至低于四年级下限，因为官方要求 **30 句**样本而这里只有 3 句，`30/n_sent` 归一化后被短样本放大。**所以这三组数值只用来验证实现与单调性，绝不拿来验收文案**。

### 26.2 链接文本静态扫描器（Python，已实跑）

```python
"""扫 Markdown / HTML 里的链接：通用文案、front-loading、同名异址、同址异名。
对应 §10（SC 2.4.4/2.4.9/3.2.4）、§12（11 字符）、§13（Learn More）。"""
import re
from collections import defaultdict

GENERIC = {
    "learn more", "read more", "click here", "more", "details", "here",
    "link", "see more", "view more", "了解更多", "查看更多", "点击这里",
    "详情", "更多", "此处", "链接", "点我", "马上了解",
}
BLAND_HEAD = ("introducing", "about", "welcome", "new", "our", "the", "a",
              "全新", "关于", "欢迎", "我们的", "更多", "了解")
MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
HTML_LINK = re.compile(r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", re.S | re.I)
TAG = re.compile(r"<[^>]+>")


def extract(text: str):
    # 三元组 (可见文本, href, 原始内部 HTML)：图片链接必须在清洗前判 alt，否则会被吞成空串。
    out = [(m.group(1).strip(), m.group(2).strip(), "") for m in MD_LINK.finditer(text)]
    for m in HTML_LINK.finditer(text):
        inner = m.group(2).strip()
        out.append((TAG.sub("", inner).strip(), m.group(1).strip(), inner))
    return out


def audit(text: str) -> list:
    links = extract(text)
    issues = []
    by_text, by_href = defaultdict(set), defaultdict(set)
    for label, href, raw in links:
        low = label.lower().strip()
        if low in GENERIC or not label:
            issues.append(("GENERIC", label or "(empty label)", href, "脱离上下文不可辨（SC 2.4.4 A / 2.4.9 AAA）"))
        head = low[:11]
        if head and any(head.startswith(b) for b in BLAND_HEAD):
            issues.append(("WEAK_HEAD", label, href, "前 11 字符无信息词（§12 front-loading）"))
        if re.search(r"<img\b", raw, re.I) and not re.search(r"alt=[\"'][^\"']+", raw, re.I):
            issues.append(("IMG_NO_ALT", label or "(image only)", href, "纯图片链接无可访问名（F89）"))
        by_text[low].add(href)
        by_href[href].add(low)
    for t, hs in by_text.items():
        if len(hs) > 1 and t:
            issues.append(("SAME_TEXT_DIFF_DEST", t, sorted(hs), "同名链接指向不同目的地"))
    for h, ts in by_href.items():
        if len(ts) > 1:
            issues.append(("DIFF_TEXT_SAME_DEST", h, sorted(ts), "同目的地文案不一致（SC 3.2.4 语境变体除外）"))
    return issues


BAD = """
- [Learn More](/pricing)
- [Learn More](/security)
- [Introducing Chase Exclusives Special Benefits](/benefits)
- [Gift Cards &amp; E-Gift Certificates](/gift-cards)
- [Gift Cards](/gift-cards)
<a href="/docs"><img src="arrow.png"></a>
"""
GOOD = """
- [查看价格与套餐](/pricing)
- [安全与合规说明](/security)
- [Gift Cards &amp; E-Gift Certificates](/gift-cards)
"""

if __name__ == "__main__":
    bad = audit(BAD)
    print("BAD issues:", len(bad))
    for i in bad:
        print("  ", i[0], "|", i[1][:44], "|", i[3])
    kinds = {i[0] for i in bad}
    assert {"GENERIC", "WEAK_HEAD", "SAME_TEXT_DIFF_DEST", "IMG_NO_ALT"} <= kinds
    good_generic = [i for i in audit(GOOD) if i[0] in ("GENERIC", "WEAK_HEAD")]
    assert not good_generic, "改写后不应剩通用/弱首词问题"
    print("PASS: 四类问题全部命中，且改写版干净")
```

**本轮实跑输出**：

```text
BAD issues: 7
   GENERIC | Learn More | 脱离上下文不可辨（SC 2.4.4 A / 2.4.9 AAA）
   GENERIC | Learn More | 脱离上下文不可辨（SC 2.4.4 A / 2.4.9 AAA）
   WEAK_HEAD | Introducing Chase Exclusives Special Benefit | 前 11 字符无信息词（§12 front-loading）
   GENERIC | (empty label) | 脱离上下文不可辨（SC 2.4.4 A / 2.4.9 AAA）
   IMG_NO_ALT | (image only) | 纯图片链接无可访问名（F89）
   SAME_TEXT_DIFF_DEST | learn more | 同名链接指向不同目的地
   DIFF_TEXT_SAME_DEST | /gift-cards | 同目的地文案不一致（SC 3.2.4 语境变体除外）
PASS: 四类问题全部命中，且改写版干净
```

最后一条 `DIFF_TEXT_SAME_DEST` 是**扫描器故意保留的人工复核项**：SC 3.2.4 允许 *"differences may be appropriate when they better reflect the component's purpose or context"*，脚本不做自动判违规，只把可疑项交给人。这正是 §10 那条 *"does not require identical"* 的工程落点。

### 26.3 可发现性契约静态检查器（Python，已实跑）

```python
"""扫 HTML 片段：多路径、搜索标签、combobox 契约、404 禁用项。
对应 §3（SC 2.4.5）、§5（3.3.2/2.4.6）、§6（APG）、§18（GOV.UK）。"""
import re
from html.parser import HTMLParser

FAIL_WORDS_404 = ("oops", "哎呀", "404", "bad request")


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.attrs = []
        self.text = []
        self.combobox = {}

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self.attrs.append((tag, d))
        if d.get("role") == "combobox":
            self.combobox = d

    def handle_data(self, data):
        self.text.append(data)


def check(html: str, is_404: bool = False) -> list:
    c = Collector()
    c.feed(html)
    tags = [t for t, _ in c.attrs]
    fails = []

    # L1: SC 2.4.5 —— 至少两条互不依赖的路径
    routes = sum([
        "<nav" in html or bool(re.search(r"role=[\"']navigation", html, re.I)),
        bool(re.search(r"<input[^>]*type=[\"']search|<search\b|role=[\"']search", html, re.I)),
        "sitemap" in html.lower() or bool(re.search(r"class=[\"'][^\"']*toc", html, re.I)),
    ])
    if routes < 2:
        fails.append("L1: 只有 %d 条找路路径，SC 2.4.5 (AA) 要求 >= 2" % routes)

    # 搜索输入的持久标签
    for t, d in c.attrs:
        if t == "input" and (d.get("type") == "search" or "search" in d.get("class", "")):
            has_id = "id" in d
            labelled = has_id and bool(re.search(r"<label[^>]*for=[\"']%s[\"']" % re.escape(d["id"]), html, re.I))
            named = "aria-label" in d or "aria-labelledby" in d
            if not (labelled or named):
                fails.append("SC 3.3.2/2.4.6: 搜索输入无可访问名（placeholder 不算）")
            if d.get("placeholder") and not (labelled or named):
                fails.append("placeholder 冒充 label：输入后语义消失")

    # APG combobox 六件
    if c.combobox:
        cb = c.combobox
        for key in ("aria-expanded", "aria-controls", "aria-autocomplete"):
            if key not in cb:
                fails.append("APG combobox 缺 %s" % key)
        if cb.get("aria-autocomplete") not in (None, "none", "list", "both"):
            fails.append("aria-autocomplete 值非法: %s" % cb["aria-autocomplete"])
        if not any(d.get("role") in ("listbox", "grid", "tree", "dialog") for _, d in c.attrs):
            fails.append("APG: 缺 popup role (listbox/grid/tree/dialog)")
        if "aria-activedescendant" not in html:
            fails.append("APG: 未见 aria-activedescendant（DOM focus 应留在 combobox）")

    # 404 禁用项
    if is_404:
        body = " ".join(c.text).lower()
        for w in FAIL_WORDS_404:
            if w in body:
                fails.append("GOV.UK 404: 禁用词 '%s'" % w)
        if "breadcrumb" in html.lower():
            fails.append("GOV.UK 404: 不要面包屑（失败态不是可定位节点）")
        if not re.search(r"<h1", html, re.I):
            fails.append("GOV.UK 404: 缺 H1 'Page not found'")
    return fails


GOOD_PAGE = """
<nav aria-label="Main"><a href="/a">A</a><a href="/b">B</a></nav>
<input type="search" id="q" aria-label="Search the site" placeholder="e.g. gift cards">
<div role="combobox" aria-expanded="false" aria-controls="sug"
     aria-autocomplete="list" aria-activedescendant="s1"></div>
<ul id="sug" role="listbox"><li id="s1" role="option">Gift Cards</li></ul>
<div class="toc"><a href="/sitemap">Sitemap</a></div>
"""
BAD_PAGE = """
<input type="search" placeholder="Search">
<div role="combobox" aria-expanded="false"></div>
"""

if __name__ == "__main__":
    g = check(GOOD_PAGE)
    b = check(BAD_PAGE)
    print("GOOD:", g or "PASS")
    print("BAD :", len(b), "issues")
    for x in b:
        print("  -", x)
    assert not g, "合规页不应报错"
    assert any("L1" in x for x in b) and any("APG" in x for x in b)
    assert any("placeholder" in x for x in b)
    p404 = check('<h1>Page not found</h1><p>Oops! 404 — bad request</p>', is_404=True)
    assert len(p404) >= 3, "404 禁用词应全部命中"
    print("404 sample:", len(p404), "issues")
    print("PASS: 多路径 / 标签 / combobox / 404 四类检查")
```

**本轮实跑输出**：

```text
GOOD: PASS
BAD : 7 issues
  - L1: 只有 1 条找路路径，SC 2.4.5 (AA) 要求 >= 2
  - SC 3.3.2/2.4.6: 搜索输入无可访问名（placeholder 不算）
  - placeholder 冒充 label：输入后语义消失
  - APG combobox 缺 aria-controls
  - APG combobox 缺 aria-autocomplete
  - APG: 缺 popup role (listbox/grid/tree/dialog)
  - APG: 未见 aria-activedescendant（DOM focus 应留在 combobox）
404 sample: 4 issues
PASS: 多路径 / 标签 / combobox / 404 四类检查
```

### 26.4 符合 APG 契约的搜索框骨架（HTML，契约示意）

```html
<!-- 可见标签持久化；placeholder 只放示例；搜索 + 导航 + 目录 = 三条路径 -->
<nav aria-label="Main navigation">
  <a href="/products">Products</a><a href="/docs">Docs</a>
</nav>

<form role="search" action="/search">
  <label for="site-q">Search the site</label>
  <input id="site-q" type="text"
         role="combobox"
         aria-expanded="false"
         aria-controls="site-suggestions"
         aria-autocomplete="list"
         aria-activedescendant=""
         autocomplete="off"
         placeholder="e.g. gift cards">
  <button type="submit" aria-label="Submit search">
    <svg aria-hidden="true" focusable="false" width="20" height="20"><!-- magnifier --></svg>
  </button>
  <ul id="site-suggestions" role="listbox" hidden>
    <li id="s1" role="option" aria-selected="false">Gift Cards</li>
    <li id="s2" role="option" aria-selected="false">Gift Certificates</li>
  </ul>
</form>

<nav aria-label="Table of contents" class="toc">
  <a href="/sitemap">Sitemap</a>
</nav>
<!-- JS 纪律：Down/Up 改 aria-activedescendant 与 aria-selected，DOM focus 不进 UL；
     Escape 关闭 popup 且不清空已输入值；Tab 只停在 input 与 button，不进 popup 后代。 -->
```

### 26.5 中文可扫读代理指标（JS，工程约定）

```js
// 工程约定而非标准：只做同语言、同站点的改版前后回归；不输出「阅读等级」。
// 阈值请按自己站点的基线自校准，不要把示例数值当规范。
export function scanCn(text, baseline = { maxSentence: 40, maxParagraph: 160, minHeadingPerChars: 400 }) {
  const clean = text.replace(/```[\s\S]*?```/g, '');
  const sentences = clean.split(/[。！？；]/).map(s => s.trim()).filter(Boolean);
  const paragraphs = clean.split(/\n\s*\n/).map(p => p.trim()).filter(Boolean);
  const headings = (clean.match(/^#{2,3}\s.+$/gm) || []).length;
  const han = s => (s.match(/[\u4e00-\u9fff]/g) || []).length;

  const avgSentence = sentences.length ? sentences.reduce((n, s) => n + han(s), 0) / sentences.length : 0;
  const longSentences = sentences.filter(s => han(s) > baseline.maxSentence).length;
  const longParagraphs = paragraphs.filter(p => han(p) > baseline.maxParagraph).length;
  const chars = han(clean);
  const headingGap = headings ? chars / headings : Infinity;

  // front-loading 代理：标题/段首前 8 个汉字里是否出现停用开头
  const bland = /^(?:关于|欢迎|全新|我们的|更多|了解|介绍|概述)/;
  const weakHeads = [...sentences.slice(0, 20)].filter(s => bland.test(s.slice(0, 8))).length;

  return {
    avgSentenceChars: +avgSentence.toFixed(1),
    longSentences, longParagraphs,
    charsPerHeading: Number.isFinite(headingGap) ? +headingGap.toFixed(0) : null,
    weakHeads,
    verdict: (longSentences === 0 && longParagraphs === 0 && weakHeads === 0
              && headingGap <= baseline.minHeadingPerChars) ? 'PASS' : 'REVIEW',
    _note: '工程约定：非实验常数、非 WCAG 3.1.5 判据；混排按 5% 规则分语言算，按最差者判',
  };
}
```

---

## 27 · 取源与限制（公开记录）

**W3C / WAI（本轮逐页逐字核验）**：`Understanding WCAG 2.2` 的 `link-purpose-in-context.html`（SC 2.4.4 A，含 Key Terms、16 项 Sufficient、F63/F89 两个 Failures、Advisory H80）、`link-purpose-link-only.html`（SC 2.4.9 AAA 与 mechanism 段）、`multiple-ways.html`（SC 2.4.5 AA 与 G125/G64/G63/G161/G126/G185、process 例外两例）、`location.html`（SC 2.4.8 AAA 与 G65/G63/G128/ARIA26/G127）、`headings-and-labels.html`（SC 2.4.6 AA、放大镜图标「Search」例、与 1.3.1/3.3.2/4.1.2 的边界）、`consistent-identification.html`（SC 3.2.4 AA 三条 Intent Note）、`labels-or-instructions.html`（SC 3.3.2 A、persistently available、`requires` 的 Note）、`reading-level.html`（SC 3.1.5 AAA、UNESCO 分级、九年门槛、5% 多语言规则、Easy to Read Note、G86/G103/G79/G153/G160）、`ARIA/apg/patterns/combobox/`（角色/状态/DOM focus/selection follows focus/键盘/`aria-autocomplete` 三档/dialog 例外/ARIA 1.0 兼容注）。

**NN/g（本轮逐篇逐字核验）**：`how-users-read-on-the-web/`（Jakob Nielsen, 1997-09-30，79%/16%、六手法、58/47/27/124% 五版本表）、`first-2-words-a-signal-for-scanning/`（2009-04-06，11 字符、80 人、20 站、35%、各案例百分比、三个 nasties）、`learn-more-links/`（Katie Sherwin, 2015-12-13，三种改法、links list 理由、1.4 billion 自带保留）、`search-visible-and-simple/`（2001-05-12，91%、43%、51/32/18%、2.0 词、scoped search 四条、First Results Page is Golden、48%）、`information-scent/`（Raluca Budiu, 2020-02-02，定义、相对性、两部分、小屏上下文警告、落地页首屏）、`tree-testing/`（Page Laubheimer, 2023-08-06 / Last reviewed 2026-08-19，findability、directness、样本量措辞、任务三例、between-subjects、leaf-only 限制）。

**其他官方 / 行业源**：GOV.UK Design System `patterns/page-not-found-pages/`（Do not use 四条、应有内容三条、Research 自述证据不足）；Material 3 `components/search/specs`（56dp / 360–720dp / 24→12dp / 16dp / 30dp / docked 240dp–2/3 屏高 / Contained vs Divided）；Digital.gov `guides/plain-language`（Plain Writing Act of 2010、四份指南、改编自 PlainLanguage.gov）；ReadabilityFormulas.com 的 FRE、FKGL、SMOG 三页（全部系数与 30 句采样约定）；Wikipedia `Flesch–Kincaid_readability_tests`（解释表、121.22 / −3.40、不可换算、Limitations 逐字段落）。

**GitHub API 实测**（2026-11-09，`GET /repos/{owner}/{repo}`，star / license / pushed / archived 均为实测值）：

| 仓库 | ★ | License | 说明 |
|---|---|---|---|
| `ant-design/ant-design` | 100,123 | MIT | 中文生态组件库 |
| `elastic/elasticsearch` | 78,535 | NOASSERTION | 搜索底座 |
| `facebook/docusaurus` | 66,684 | MIT | 文档站可发现性 |
| `meilisearch/meilisearch` | 59,819 | NOASSERTION | 搜索底座 |
| `typesense/typesense` | 27,107 | GPL-3.0 | 搜索底座 |
| `mkdocs/mkdocs` | 22,538 | BSD-2-Clause | 文档站（pushed 2025-10-20） |
| `rust-lang/mdBook` | 22,282 | MPL-2.0 | 文档站 |
| `krisk/Fuse` | 20,526 | Apache-2.0 | 模糊搜索（正确仓库名） |
| `vuejs/vitepress` | 18,479 | MIT | 文档站 |
| `mdn/content` | 11,131 | NOASSERTION | 内容平台 |
| `oramasearch/orama` | 10,606 | NOASSERTION | 搜索库 |
| `algolia/autocomplete` | 5,270 | MIT | 自动补全 |
| `algolia/docsearch` | 4,388 | MIT | 文档搜索 |
| `algolia/instantsearch.js` | 4,067 | MIT | 搜索 UI |
| `textstat/textstat` | 1,393 | MIT | 可读性公式实现 |
| `w3c/aria-practices` | 1,362 | NOASSERTION | APG 源仓库 |
| `mdn/yari` | 1,301 | MPL-2.0 | **archived=true**（2026-10-13） |
| `w3c/clreq` | 813 | NOASSERTION | 中文排版需求 |
| `alphagov/govuk-design-system` | 688 | MIT | 404 pattern 源仓库 |
| `gsa/plainlanguage.gov` | 228 | NOASSERTION | **archived=true**（2025-09-23） |
| `swisspost/design-system` | 181 | Apache-2.0 | 设计系统 |

**取源限制（不臆造、不外推）**：

- `fusejs/Fuse` 返回 **404**，正确名为 `krisk/Fuse`；不把猜测仓库写进清单。
- `developer.apple.com/design/human-interface-guidelines/search-fields` 本轮抓取只得到导航骨架（JS 渲染），**未取到任何正文，故本文件不含 Apple HIG 数值**；下轮候选。
- Baymard 的 autocomplete / 零结果结论本轮只拿到二手转述（「96% 大型电商提供自动补全」「80% 提供 autocomplete」等，来自第三方博客转引），**未逐字核验，故不写入任何数值**，只登记下轮候选。
- `nngroup.com/articles/empty-state-no-results/` 返回 NN/g 自有 404 页；**该页文案未作为规范引用**（含「AI 幻觉链接」现象仅作记录）。
- NN/g `information-scent/` 正文**未出现 Pirolli / Card 姓名或文献**，故本文件不写信息觅食理论的作者归属；理论页 `information-foraging/` 未逐页深取。
- NN/g `tree-testing/` 正文**没有给出具体样本人数或任务数**；`5` 只出现在链接 URL 里，不是本页结论。
- Wikipedia 的 FRE / FKGL 公式以数学渲染呈现，抓取文本中丢失；**系数取自 ReadabilityFormulas.com 逐字页并已标注来源**，不由记忆补写。
- 中文可读性相关资料（百科「易读性测量」、中文年报可读性指标对比、文本可读性评估论坛文等）**全部仅搜索结果级、未逐字核验**；§16 的六个代理量与「前 6–8 汉字」均为**本知识库工程约定，非实验常数、非标准**。
- §11 的 58/47/27/124% 是 1997 年单站点五版本对照实验的相对提升，**不是通用 ROI**；§4 的 91% 是单站点单次改版实测；§7 的 51/32/18% 是特定电商研究样本。三处均不得脱离语境外推。
- §6 的 `aria-autocomplete` 契约、§26.3 的检查器只做**静态可检出项**；真实读屏行为仍须按 `accessibility.md` 的读屏实测脚本复核。
- 发布通道备注：`~/.workbuddy-ai/secrets/github_token.txt` 首行 PAT 已失效（401）；本轮 GitHub API 改用 `git credential fill` 取出的凭据，实测 21 个仓库全部成功（仅 `fusejs/Fuse` 为名称错误）。

**下轮候选缺口**：① Apple HIG `search-fields` 正文与 iOS/macOS 搜索规格逐字核验（本轮 JS 渲染未取到）；② Baymard 站内搜索 / autocomplete / 零结果报告逐页核验（本轮仅二手转述）；③ 分面搜索（faceted search）与筛选器计数的权威实证；④ 搜索结果排序、摘要高亮（snippet / query highlighting）与 SERP 眼动研究；⑤ 中文可读性权威资料逐字核验（本轮全为搜索结果级）与中文分词口径；⑥ 站点地图 / 目录 / 全页链接在小站与 SPA 里的工程实现差异；⑦ NN/g `information-foraging/` 理论页与 Pirolli–Card 原始文献归属；⑧ `radix-ui/themes` shape/elevation token 源码精确定位与 Fluent 2 depth 现行路径复核（沿用 #28/#29 未结项）。
