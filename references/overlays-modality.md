# 叠加层与模态性：判型、焦点契约、顶层栈与非模态消隐

> 快照 2026-11-11 · 每日升级 #33（v36→v37）· 主题：Overlays & Modality / Dialog / Popover / Top Layer
> 取源：`Design-related websites.txt` 第二十二分区 + W3C APG / WCAG 2.2 Understanding / MDN / WHATWG HTML / Apple HIG / M3 / Radix / Open UI + GitHub API 实测 10 库。凡规范条文与数值均引官方原文，凡工程建议均标注「工程约定」；22 个取源 URL 本轮全部 HTTP 200 复核。
>
> **边界纪律（先读这段，避免误路由）**：本文件只管「一层内容盖在另一层之上时，谁还能被操作、焦点去哪、怎么退出、会不会挡住焦点项」。**反馈时长与 toast 语义**归 `feedback-states.md`；**弹窗文案措辞**归 `ux-writing.md`；**圆角 / 阴影 / 语义 z-index 刻度 / 表面层级**归 `shape-elevation.md`；**WCAG 全量阈值与焦点可见样式**归 `accessibility.md`；**组件 props 契约与键盘冻结面**归 `component-api-design.md`；**cookie 同意与欺骗性模态**归 `design-ethics-inclusion.md`；**下拉菜单与 combobox 的 aria 明细**归 `content-findability.md`；**抽屉作为导航形态的选型**归 `navigation-ia.md`。本文件不重复这些资产，只补「模态性作为一份交互契约」这条结构性空白。

---

## 0. 一句话立场

**模态不是一层半透明黑色遮罩，是一份「外部还能不能被操作」的交互契约。** 一个界面可以没有遮罩却是模态（代码阻止了外部交互），也可以有遮罩却不是模态（外部仍可点、Tab 仍能走出去）。把模态当成视觉效果来做，就会同时踩中四条独立规范：APG 焦点契约、ARIA 语义、WCAG 2.2 SC 2.4.11 遮挡、SC 2.1.2 键盘陷阱。反过来，**非模态也不等于「什么都不用做」**——hover / focus 触发的附加内容要过 SC 1.4.13 的 Dismissible / Hoverable / Persistent 三条，持久浮层还要过 SC 2.4.11。

判型只有四问，顺序不能换（§1）。判完再选实现（§5 原生 `<dialog>` / §6 Popover API / §16 库），最后过四条款矩阵（§8）。

---

## 1. 四问判型决策树：inert / 焦点 / 触发 / 退出

先答四问，**不要先看设计稿长什么样**：

| # | 问题 | 答「是」 | 答「否」 |
|---|---|---|---|
| Q1 | 层出现时，**页面其余内容是否对所有人不可交互**（不只是变暗、不只是 `pointer-events: none` 盖一层）？ | 走向模态 | 走向非模态 |
| Q2 | 焦点是否**必须**移进该层，且 `Tab` / `Shift+Tab` 不能把焦点带出层外？ | 走向模态 | 保持非模态（或该层根本不该接收焦点，见 §9 tooltip） |
| Q3 | 层是**由用户显式激活**（click / Enter / Space）触发，还是由 hover / focus 触发？ | 显式激活 → 可承载 change of context | hover / focus → 触发 SC 1.4.13，且禁止 change of context（§12） |
| Q4 | 该层有没有**不依赖鼠标、不依赖物理键盘、也不依赖「先找到关闭按钮」的退出路径**？ | 契约闭合 | 未闭合：SC 2.1.2 / 2.4.11 风险 |

**四条执行规则（工程约定，落到代码即可验收）**：

1. **Q1 与 Q2 必须同答「是」才允许标 `aria-modal="true"`**——W3C 原文见 §4 双条件。只答一个却标了，是「对读屏用户说外面不存在、对鼠标用户说外面还在」，属确定性缺陷而非体验瑕疵。
2. **Q3 答 hover / focus 时，不允许出现模态**。W3C 逐字：*"Modal dialogs are out of scope for this criterion because they must take keyboard focus and thus should not appear on hover or focus."*（§9）；SC 3.2.1 另有 help dialog 失败例（§12）。
3. **Q4 的退出路径要与触发路径对称**：键盘打开 → `Escape` 能关且焦点归位；触屏打开 → 有可见关闭按钮或下滑手势（MDN：*"it is important to provide a closing mechanism for every `<dialog>` element, and to ensure that this works on devices that might not have a physical keyboard"*）。
4. **判型结果必须写进组件 API**，不能靠调用方每次自觉：`modal={true}` 是 Radix 的默认值（§16），这是把契约写死在默认值里，而不是留给使用方。

**判型器见 §20.1**（Python 实跑），它把四问 + 三条硬约束编译成可执行断言。

---

## 2. 三条最重要裁决

### 裁决一 · 模态性由 inert 定义，不由遮罩定义；`aria-modal` 是「声明」不是「实现」

W3C APG 逐字：*"A dialog is a window overlaid on either the primary window or another dialog window. **Windows under a modal dialog are inert.** That is, users cannot interact with content outside an active dialog window. Inert content outside an active dialog is typically visually obscured or dimmed so it is difficult to discern, and in some implementations, attempts to interact with the inert content cause the dialog to close."*

注意 **typically** 与 **in some implementations** 两个限定词：变暗只是常见伴随现象，不是定义；点外部关闭也只是某些实现的副作用。MDN 给出浏览器侧等价物：*"Modal dialog boxes block interaction with other UI elements, making the rest of the page inert, while non-modal dialog boxes allow interaction with the rest of the page."*

**执行含义**：写 `aria-modal="true"` 是向辅助技术声明一份事实，不会替你实现 inert。原生 `showModal()` 由浏览器代劳（§5），自定义实现必须自己 `inert` 外部容器 + 焦点约束 + 视觉遮蔽，三者齐了才配标。APG 逐字警告：*"So, mark a dialog modal **only when both**: 1. Application code prevents all users from interacting in any way with content outside of it. 2. Visual styling obscures the content outside of it."*

### 裁决二 · Popover API 永远非模态；它与 `<dialog>` 是两套机制，不是彼此的轻量替代

MDN 逐字：*"**Popovers created using the Popover API are always non-modal.** If you want to create a modal popover, a `<dialog>` element is the right way to go."* 且明确两者可以叠加：*"You can turn a `<dialog>` element into a popover (`<dialog popover>` is perfectly valid) if you want to combine popover control with dialog semantics."* ——叠加后仍**非模态**，因为 popover 语义带 light dismiss。

由此产生最常见的工程错误：**用 `position: fixed` + `z-index: 9999` + 半透明遮罩做「弹窗」，然后发现 Tab 能跑到背后、读屏还能读到背景、iOS 上滚动穿透**。根因不是 z-index 不够大，是 top layer 与 inert 根本没参与（§7）。

`popover` 三态不是「三种动画」，是三套关闭与堆叠契约（§6）：`auto` 参与 auto stack 且通常一次只显示一个；`hint` 参与独立 hint stack 且不关闭 auto；`manual` 不参与任何栈、必须显式关闭、可多个并存。

### 裁决三 · 「浮层不挡焦点」是 WCAG 2.2 新增的 AA 硬要求，模态天然通过、伪模态最危险

SC 2.4.11 Focus Not Obscured (Minimum)（**Level AA**）逐字：*"When a user interface component receives keyboard focus, the component is not entirely hidden due to author-created content."* 目标口径是 *"Ensure when an item gets keyboard focus, it is at least partially visible."*；检查对象是 **focused component 本身**，不是外部 focus indicator（后者被全遮时另判 2.4.7 Focus Visible）。

W3C 直接给出本主题的裁决：*"**A properly constructed modal dialog will always pass this SC.** Even if it appears directly on top of an item with focus, the dialog takes focus on appearance, and thus the item receiving focus -- the dialog or one of its components -- is visible."* 反过来：*"A **dialog-like overlay that does not take focus on appearance** and does not either constrain interaction to the overlay or dismiss itself on loss of focus (thus allowing focus to exit into the content behind it) will be at risk of failing this SC, where it is positioned such that it can obscure other focusable items."*

也就是说：**「看起来像弹窗但既不接管焦点、也不让外部 inert、还不自动消失」的伪模态，是本轮四条款下最糟的一种形态**——它同时踩 2.4.11 遮挡、2.1.2 出不去、1.4.13 不可消隐，且不属于 Note 2 的 user-opened 豁免（§10）。

---

## 3. APG 对话框契约逐字条文：初始焦点、Tab 循环、Escape、关闭后归位

W3C APG《Dialog (Modal) Pattern》Keyboard Interaction 逐字（这是实现验收清单，不是建议）：

> - *When a dialog opens, focus moves to an element inside the dialog. See notes below regarding initial focus placement.*
> - `Tab`: *Moves focus to the next tabbable element inside the dialog.* / *If focus is on the last tabbable element inside the dialog, moves focus to the first tabbable element inside the dialog.*
> - `Shift` + `Tab`: *Moves focus to the previous tabbable element inside the dialog.* / *If focus is on the first tabbable element inside the dialog, moves focus to the last tabbable element inside the dialog.*
> - `Escape`: *Closes the dialog.*

同一页对 **tabbable element** 的定义与禁令：*"the term tabbable element refers to any element with a `tabindex` value of zero or greater. Note that values greater than 0 are strongly discouraged."*

### 3.1 初始焦点的四种情形（APG Note 1 逐字要点，按内容选，不是一律聚焦第一个按钮）

1. **内容含列表 / 表格 / 多段语义结构** → 给开头静态元素 `tabindex="-1"` 并聚焦它，*this makes it easier for assistive technology users to read the content by navigating the semantic structures*；此时 **建议省略 `aria-describedby`**（否则整段被压成一条不间断字符串播报）。
2. **内容很长，聚焦第一个交互元素会把开头滚出视口** → 给标题或首段 `tabindex="-1"` 并聚焦它。
3. **流程最后一步且不易撤销**（删除数据、完成交易）→ *"it may be advisable to set focus on the least destructive action"*；此类常用 `role="alertdialog"`（§3.3）。
4. **仅需「补充信息 / 继续」** → 聚焦最常用动作，如 OK / Continue。

MDN 的浏览器默认与显式覆盖：*"When using `HTMLDialogElement.showModal()` to open a `<dialog>`, focus is set on the first nested focusable element. Explicitly indicating the initial focus placement by using the `autofocus` attribute will help ensure initial focus is set on the element deemed the best initial focus placement"*；*"The `autofocus` attribute should be added to the element the user is expected to interact with immediately upon opening a modal dialog. If no other element involves more immediate interaction, it is recommended to add `autofocus` to the close button inside the dialog, or the dialog itself"*。**MDN 硬禁令**：*"**Warning:** The `tabindex` attribute must not be used on the `<dialog>` element."* / *"Do not add the `tabindex` property to the `<dialog>` element as it is not interactive and does not receive focus."*

> 口径提醒：APG 的「静态元素 `tabindex="-1"` 并聚焦」与 MDN 的「`<dialog>` 上禁 `tabindex`」不冲突——前者作用于 dialog **内部**的标题 / 首段，后者作用于 `<dialog>` **容器本身**。

### 3.2 关闭后焦点归位（APG Note 2 逐字）

> *When a dialog closes, focus returns to the element that invoked the dialog unless either:*
> - *The invoking element no longer exists. Then, focus is set on another element that provides logical work flow.*
> - *The work flow design includes the following conditions that can occasionally make focusing a different element a more logical choice: 1. It is very unlikely users need to immediately re-invoke the dialog. 2. The task completed in the dialog is directly related to a subsequent step in the work flow.*

官方给的例子是「工具栏 Add Rows → 输入行数 → 关闭后焦点落到新行的第一个单元格」。APG 另有一条**强推荐**：*"It is strongly recommended that the tab sequence of all dialogs include a visible element with role `button` that closes the dialog, such as a close icon or cancel button."* ——即：**不能只靠 `Escape` 或点遮罩关闭**；触屏、无物理键盘设备、读屏用户都需要可见的、在 tab 序列里的关闭控件。

### 3.3 语义清单（APG WAI-ARIA Roles, States, and Properties）

- 容器 `role="dialog"`；**操作该 dialog 所需的全部元素必须是该容器的后代**。
- 容器 `aria-modal="true"`（双条件见 §4）。
- `aria-labelledby` 指向可见标题，**或** `aria-label` 给名字；二者至少其一。
- `aria-describedby` 可选，但只在描述内容**简单且无需结构信息**时有益；含列表 / 表格 / 多段时应省略。
- **alertdialog** 变体（APG Alert and Message Dialogs Pattern）：`role="alertdialog"` + `aria-modal="true"` + `aria-labelledby`/`aria-label` + **`aria-describedby` 指向 alert message（此项为必需）**。键盘契约与 modal dialog 完全相同（该页写 *"See the keyboard interaction section for the modal dialog pattern."*）。用途是 *"interrupts the user's workflow to communicate an important message and acquire a response"*，如确认提示与错误消息确认。

### 3.4 关于 `aria-hidden` 的历史包袱

APG Note 逐字：*"The `aria-modal` property introduced by ARIA 1.1 replaces `aria-hidden` for informing assistive technologies that content outside a dialog is inert."* 但旧实现若仍用 `aria-hidden`，必须同时满足：*"1. `aria-hidden` is set to `true` on each element containing a portion of the inert layer. 2. The dialog element is not a descendant of any element that has `aria-hidden` set to `true`."* 第二条是最常见的自伤：把 dialog portal 挂进了被 `aria-hidden="true"` 的 `#app` 里，等于把自己也隐藏了。**工程结论：新代码直接用 `inert` + `aria-modal`，不要混用两套。**

---

## 4. `aria-modal="true"` 双条件与误标后果

APG 逐字（两处：Dialog Modal Pattern 与 Alert Dialog Pattern 措辞完全一致）：

> *Because marking a dialog modal by setting `aria-modal` to `true` can prevent users of some assistive technologies from perceiving content outside the dialog, users of those technologies will experience severe negative ramifications if a dialog is marked modal but does not behave as a modal for other users. So, mark a dialog modal **only when both**:*
> 1. *Application code prevents all users from interacting in any way with content outside of it.*
> 2. *Visual styling obscures the content outside of it.*

**误标的后果是「只对一部分用户关闭了半个页面」**：鼠标用户还能点背景（因为没真的 inert），读屏用户却被明确告知背景不存在。W3C 用 *severe negative ramifications* 定性，不是「建议改进」。

**可执行判定（工程约定）**：标 `aria-modal="true"` 之前，逐条断言——

- [ ] 背景所有可交互元素不可点击、不可聚焦、不被读屏读到（`inert` 或等价实现）；
- [ ] Tab / Shift+Tab 在层内循环；
- [ ] 背景有视觉遮蔽（`::backdrop` 或等价 scrim）；
- [ ] 背景滚动被锁定（否则键盘滚动仍可操作背景，此项属工程补强，规范原文未逐字要求）；
- [ ] 关闭后焦点归位，背景 `inert` 与滚动锁复原。

任一为否 → **不标 `aria-modal`，改走非模态契约**（§6 / §9 / §10）。

---

## 5. 原生 `<dialog>` 的浏览器代劳清单：showModal / show / open / closedby

MDN 逐字：*"The HTML `<dialog>` element is used to create both modal and non-modal dialog boxes."* 三种打开方式对应三种交互契约：

| 打开方式 | 模态性 | 浏览器代劳 |
|---|---|---|
| `dialog.showModal()` | **模态** | inert 外部、`::backdrop`、top layer、`Escape`、隐式 `aria-modal="true"`、焦点进首个可聚焦元素 |
| `dialog.show()` | **非模态** | 无 inert、无 backdrop；暴露为 `aria-modal="false"` |
| `open` 属性 / 改 CSS `display` | **非模态** | 同上；MDN 明确 *"If a `<dialog>` is opened using the `open` attribute, it is non-modal."*，且 *"It is recommended to use the `.show()` or `.showModal()` method to render dialogs, rather than the `open` attribute."* |

隐式 ARIA 逐字：*"`<dialog>` elements invoked by the `showModal()` method implicitly have `aria-modal="true"`, whereas `<dialog>` elements invoked by the `show()` method or displayed using the `open` attribute or by changing the default `display` of a `<dialog>` are exposed as `aria-modal="false"`."* ——**这条最容易翻车**：手写 `<dialog open>` 或 CSS `dialog { display: block }` 做「弹窗」，浏览器明确告诉读屏它不是模态，而 CSS 里又画了遮罩，正是 §4 的误标反例的镜像。

### 5.1 `closedby` 三值（MDN 逐字）

`closedby` 区分三类关闭动作：*"A **light dismiss user action**, in which the `<dialog>` is closed when the user clicks or taps outside it"*、*"A **platform-specific user action**, such as pressing the `Esc` key on desktop platforms, or a 'back' or 'dismiss' gesture on mobile platforms"*、*"A **developer-specified mechanism** such as a `<button>` with a `click` handler that invokes `HTMLDialogElement.close()` or a `<form>` submission"*。

| 值 | 逐字 | 可用关闭方式 |
|---|---|---|
| `any` | *"The dialog can be dismissed using any of the three methods."* | 点外部 + Esc/返回手势 + 自定义按钮 |
| `closerequest` | *"The dialog can be dismissed with a platform-specific user action or a developer-specified mechanism."* | Esc/返回 + 自定义按钮 |
| `none` | *"The dialog can only be dismissed with a developer-specified mechanism."* | 仅自定义按钮 |

缺省行为逐字：*"If the `<dialog>` element does not have a valid `closedby` value specified, then if it was opened using `showModal()`, it behaves as if the value was `"closerequest"`; otherwise, it behaves as if the value was `"none"`."*

**裁决（工程约定）**：涉及未保存内容的编辑层用 `closedby="none"` 并在 `cancel` 事件里做数据丢失确认（Apple HIG：*"When necessary, help people avoid data loss by getting confirmation before closing a modal view."*）；纯查看层可用 `any`；**不要**为了「防止误关」全局禁用 `Escape`——MDN 逐字：*"Keyboard users expect the `Esc` key to close modal dialogs; ensure that this behavior is implemented and maintained."* 想拦数据丢失，正确做法是 `cancel` 事件里 `preventDefault()` 并弹确认，不是砍掉 Esc。

### 5.2 其余必须记住的逐字点

- **多个模态层**：*"If multiple modal dialogs are open, pressing the `Esc` key should close only the last shown dialog. When using `<dialog>`, this behavior is provided by the browser."*（§14）
- **`cancel` 与 `returnValue`**：*"If the dialog is closed by pressing the `Esc` key or the `requestClose()` button, a `cancel` event gets triggered first, giving code a chance to prevent closure in some cases."*；`<form method="dialog">` 提交会关闭 dialog、保存但不提交表单状态，并把 `returnValue` 设为被激活按钮的 `value`。`requestClose()` 的参数会在 `close` 事件前覆盖 `returnValue`。
- **表单校验陷阱**：*"When a form inside a dialog has a required input, the user agent will only let you close the dialog once you provide a value for the required input. To close such dialog, either use the `formnovalidate` attribute on the close button or call the `close()` method"* ——**「取消」按钮关不掉**是必现现象，不是 bug。
- **每个 dialog 必须有可见关闭机制**：*"Ensure a mechanism is provided to allow users to close the dialog. The most robust way ... is to include an explicit button to do so, such as a confirmation, cancellation, or close button."*
- **进出场动画**：因为 dialog 在 `display: none ↔ block` 之间切换并被移入 / 移出 top layer，MDN 要求 CSS transition 四件套：`@starting-style` + 把 `display` 列入 transition + 把 `overlay` 列入 transition（让移除 top layer 延后到动画结束）+ `transition-behavior: allow-discrete`；CSS keyframe 动画则不需要 `@starting-style` / `overlay` / `allow-discrete`，但要在关键帧里包含 `display`。另：*"it wasn't possible to animate the backdrop fade out — the backdrop is immediately removed from the DOM when the `<dialog>` is closed"*。**退场遮罩淡出做不到，别在验收里写这条。**
- **Invoker Commands**：`commandfor` + `command="show-modal" | "close" | "request-close"` 可声明式开关模态 dialog；`popovertarget` + `popovertargetaction` 用于把 `<dialog>` 变成非模态 popover。

---

## 6. Popover API 三态：always non-modal 与 auto · hint · manual 双栈

### 6.1 逐字定调

MDN：*"**Popovers created using the Popover API are always non-modal.**"* 同一页把术语分清楚：*"This content can take several different names — overlays, popups, popovers, dialogs, etc. We will refer to them as popovers through the documentation. Generally speaking, these can be: **modal** ... **non-modal** ..."* —— 即「popover」在文档里是**上位概念**（泛指所有盖在上层的内容），而 **Popover API 造出来的具体机制恒为非模态**。这个措辞差异是大量误引的根源。

### 6.2 三态契约（MDN Using 逐字）

| 态 | light dismiss | 栈 | 一次可显示几个 | 典型用途 |
|---|---|---|---|---|
| `auto`（`popover` 无值等价 `auto`） | 可；*"you can hide the popover by clicking outside it"*，且 *"can also be closed, using browser-specific mechanisms such as pressing the `Esc` key"* | **auto stack** | *"Usually, only one `auto` popover can be shown at a time — showing a second popover when one is already shown will hide the first one. The exception ... nested auto popovers."* | 操作菜单、教学气泡、状态覆盖 |
| `hint` | 可，*"They can be light dismissed and will respond to close requests"* | **hint stack**（独立于 auto） | 显示新 hint 会关掉非祖先的其他 hint | tooltip（工具栏 hover 提示不打断已打开的菜单） |
| `manual` | *"The popover cannot be 'light dismissed'"* | *"do not participate in either stack"* | *"Multiple independent popovers can be shown simultaneously"* | 常驻面板、聊天窗、必须显式关闭的浮层 |

逐字注意：*"Note also that `popover="hint"` falls back to `popover="manual"` in unsupporting browsers."* —— 用 hint 必须做能力检测与降级，**降级后「多个并存且不自动关」是预期行为，不是回归缺陷**。

### 6.3 双栈六条交互规则（MDN 逐字）

> *The browser maintains two independent stacks of open popovers: an **auto stack** for `auto` popovers, and a **hint stack** for `hint` popovers. ... Because the two stacks are separate, operations on one do not automatically affect the other.*
> - *Showing a `hint` popover does not close `auto` popovers.*
> - *Showing a `hint` popover closes other `hint` popovers, except those that are its ancestors in the hint stack.*
> - *Clicking outside a popover light-dismisses all open `auto` and `hint` popovers that are not its ancestor.*
> - *Hiding an `auto` popover does not close `hint` popovers that are not its descendants.*
> - *Showing an `auto` popover as a child of a `hint` popover downgrades the `auto` popover to `hint`.*
> - *Showing a popover while another is in the process of being shown or hidden is not permitted.*

补充两条逐字：*"Note: `popover="auto"` popovers are also dismissed by successful `HTMLDialogElement.showModal()` and `Element.requestFullscreen()` calls on other elements in the document."*（模态 dialog 打开会替你清掉 auto 浮层，是有意的层级优先）；*"An `auto` popover cannot have a `hint` popover as its parent in the `auto` popover stack ... the browser automatically downgrades the `auto` popover's effective type to `hint`"*。

### 6.4 焦点与 ARIA（最容易与 dialog 混淆的一节）

MDN 逐字：*"When a relationship is established between a popover and its control (invoker) via the `popovertarget` attribute, the API automatically makes two other changes"*：

1. *"When the popover is shown, the **keyboard focus navigation order is updated** so that the popover is next in the sequence ... Conversely, when closing the popover via the keyboard (usually via the `Esc` key), focus is shifted back to the invoker."*
2. *"an implicit `aria-details` and `aria-expanded` relationship is set up between them."*

**关键裁决**：**打开 popover 时浏览器不会把焦点移进去**，只把 popover 排进 Tab 序列的下一位。这与 `showModal()` 的「焦点立即进层 + 循环」是两套语义。因此：命令面板 / 搜索面板这类「打开就要能打字」的非模态浮层，必须自己 `focus()` 到输入框并自己处理 `Escape` / 外部点击 / 焦点归位——**别指望 Popover API 代劳**。若用 `showPopover({source})` 的 JS 形式，MDN 明确 *"only the focus navigation order changes are made, not the implicit ARIA relationship"*。

### 6.5 声明式与命令式 API 速查

HTML：`popover`（`auto` / `hint` / `manual`）、`popovertarget`（指向 id）、`popovertargetaction`（`hide` / `show` / `toggle`，缺省 `toggle`）、`interestfor`（interest invoker，用于 hover/focus 无 JS 显示）。
JS：`showPopover()` / `hidePopover()` / `togglePopover()`、`HTMLElement.popover`（可兼作特性检测）、`popoverTargetElement` / `popoverTargetAction`。
事件：`beforetoggle`（状态改变前，**可用于阻止打开**）、`toggle`（状态改变后）；`ToggleEvent` 是它们的事件对象。interest invokers 侧另有 `interest` / `loseinterest` 与 `InterestEvent.source`。
CSS：`:popover-open`、`:interest-source`、`:interest-target`、`::backdrop`、`interest-delay` / `interest-delay-start` / `interest-delay-end`。

> **与 SC 1.4.13 的接口**：`interestfor` / hover 显示天然落在 1.4.13 适用范围；`interest-delay-*` 可以缓解「不小心触发」，但**不能替代 Dismissible / Hoverable / Persistent 三条**（§9）。

---

## 7. top layer、inert、::backdrop 与 z-index 的分界

- **top layer 是独立绘制层，不是更大的 z-index**。MDN 逐字：`<dialog>` *"being removed from / added to the top layer and the accessibility tree"*；Popover API 的 `showPopover()` 逐字 *"Shows a popover element by adding it to the top layer"*，`hidePopover()` 逐字 *"Hides a popover element by removing it from the top layer and styling it with `display: none`"*。**结论：在 stacking context 里靠 `z-index: 2147483647` 抢层级，永远赢不了进了 top layer 的元素；父级 `overflow: hidden` 也裁不掉 top layer 内容。**这也是为什么 portal 到 `body` 只是解决 overflow / 层叠上下文，解决不了 inert。
- **inert 是行为，不是样式**。MDN：*"When implementing modal dialogs, everything other than the `<dialog>` and its contents should be rendered inert using the `inert` attribute. When using `<dialog>` along with the `HTMLDialogElement.showModal()` method, this behavior is provided by the browser."* `pointer-events: none` 只挡指针，挡不住 Tab、读屏、键盘滚动，也不是 inert。
- **`::backdrop` 只在模态 / top layer 场景有意义**。MDN：*"The CSS `::backdrop` pseudo-element can be used to style the backdrop of a modal dialog, which is displayed behind the `<dialog>` element when the dialog is displayed using the `HTMLDialogElement.showModal()` method. This pseudo-element could be used, for example, to blur, darken, or otherwise obfuscate the inert content behind the modal dialog."*；Popover API 侧 `::backdrop` 是 *"a full-screen element placed directly behind popover elements"*。**非模态浮层画满屏半透明遮罩 = 视觉宣称模态、行为仍是背景可点**，属 §4 误标的视觉版。
- **半透明遮罩还有独立的对比度责任**。WCAG 2.2 SC 2.4.11 Understanding 逐字：*"Another form of obscuring can occur when semi-transparent overlays, or overlays that apply a blur or other dimming effect, overlap the focused item. While the focused item may not be entirely obscured by these overlays, thereby passing this criterion, it may separately fail 1.4.11 Non-text Contrast. In such cases, the focus indicator must be evaluated against the contrast requirements of 1.4.11 while its appearance is affected by the overlays."* ——**过了 2.4.11 不等于过了对比度**。
- **伪类**：`:modal`（匹配模态 dialog）、`:open`（`:open` 不支持时用 `dialog[open]` 兜底）、`:popover-open`。

---

## 8. WCAG 2.2 四条款矩阵：谁管叠加层的哪一段

| 条款 | 级别 | 逐字核心 | 管的是 | 本文件落点 |
|---|---|---|---|---|
| **SC 1.4.13** Content on Hover or Focus | AA | Dismissible / Hoverable / Persistent 三条 | **由 hover / focus 触发的附加内容** | §9 |
| **SC 2.4.11** Focus Not Obscured (Minimum) | AA | *"the component is not entirely hidden due to author-created content"* | **任何层是否挡住获得键盘焦点的组件** | §10 |
| **SC 2.1.2** No Keyboard Trap | A | 焦点可只用键盘移走；非标准退出法须告知 | **焦点循环是否有出口** | §11 |
| **SC 3.2.1** On Focus | A | *"does not initiate a change of context"* | **focus 本身不许触发上下文变化** | §12 |

配套但不在本文件主线的：SC 2.4.12 Focus Not Obscured (Enhanced)（AAA，*"none of the component receiving focus should be obscured"*）、SC 2.4.7 Focus Visible（focus indicator 被全遮时另判）、SC 1.4.11 Non-text Contrast（遮罩下的 focus ring 对比度）、SC 2.1.1 Keyboard（hover 能触发的内容也要能由键盘 focus 触发，1.4.13 页原文：*"Content which can be triggered via pointer hover should also be able to be triggered by keyboard focus."*）。

**四条款的合取式验收（工程约定）**：一个浮层只有同时满足「触发方式合法（3.2.1）→ 触发出的内容可消隐可悬停可持久（1.4.13）→ 不遮死焦点项（2.4.11）→ 焦点若有循环则给得出键盘出口（2.1.2）」才算契约闭合。**任何单条通过都不能替代其余三条。**

---

## 9. SC 1.4.13 三条件：Dismissible / Hoverable / Persistent 逐字与可执行判定

《Understanding SC 1.4.13 Content on Hover or Focus》（**Level AA**）规范性条文逐字：

> *Where receiving and then removing pointer hover or keyboard focus triggers additional content to become visible and then hidden, the following are true:*
>
> **Dismissible**: *A mechanism is available to dismiss the additional content without moving pointer hover or keyboard focus, unless the additional content communicates an input error or does not obscure or replace other content;*
>
> **Hoverable**: *If pointer hover can trigger the additional content, then the pointer can be moved over the additional content without the additional content disappearing;*
>
> **Persistent**: *The additional content remains visible until the hover or focus trigger is removed, the user dismisses it, or its information is no longer valid.*
>
> *Exception: The visual presentation of the additional content is controlled by the user agent and is not modified by the author.*

官方 Note 逐字（范围界定）：

> *Note 1: Examples of additional content controlled by the user agent include browser tooltips created through use of the HTML `title` attribute.*
> *Note 2: **Custom tooltips, sub-menus, and other nonmodal popups that display on hover and focus are examples of additional content covered by this criterion.***
> *Note 3: This criterion applies to content that appears in addition to the triggering component itself. Since hidden components that are made visible on keyboard focus (such as links used to skip to another part of a page) do not present additional content they are not covered by this criterion.*

### 9.1 范围裁决：模态明确不适用

W3C Additional Notes 逐字：*"**Modal dialogs are out of scope for this criterion because they must take keyboard focus and thus should not appear on hover or focus.** Refer to Success Criterion 3.2.1 On Focus."*

这句话不是「模态可以随便做」，而是**模态根本不该由 hover / focus 触发**。若一个模态由 focus 触发，该判的是 SC 3.2.1 的 help dialog 失败例（§12），不是拿 1.4.13 来搪塞。

### 9.2 三条的可执行判定（工程约定，验收时逐条给证据）

- **Dismissible**：在不移动鼠标、不移动键盘焦点的前提下能关掉。W3C Intent 逐字给了标准做法：*"such as pressing the `Esc` key"*；并给两项豁免 *"The additional content communicates an input error message"* 与 *"The additional content does not replace or obscure other meaningful content (including the trigger element itself)"*。**注意**：`Escape` 必须在浮层显示时由全局键处理，**不能**要求用户先 Tab 到浮层内的关闭按钮（那已经移动了焦点）。
- **Hoverable**：指针从触发元素移到浮层内容上，浮层不得消失。W3C Intent 说明动机：屏幕放大用户需要 pan/滚动才能看完大段内容、大指针会遮住内容；*"A technique to view the content fully in both situations is to move the mouse pointer directly from the trigger onto the new content."* 实现上触发元素与浮层之间不能有「鼠标一离开就 `mouseout` 关闭」的空隙——常见修复是给两者共同的 `hover` 容器，或用 `relatedTarget` 判断是否移入浮层（工程约定）。
- **Persistent**：不能定时自动消失。三个合法消失条件逐字：*"The user removes hover or focus from the trigger and the additional content"* / *"The user dismisses the additional content via the mechanism provided to satisfy the Dismissible condition"* / *"The information conveyed by the additional content becomes invalid, such as a 'busy' message that is no longer valid"*。**给 tooltip 加 3 秒自动隐藏 = 违反 Persistent**（对比：`feedback-states.md` 的 toast 有时长，但 toast 不是 hover/focus 触发的附加内容，两者不冲突）。

### 9.3 tooltip 的正确形态（APG Tooltip Pattern）

APG 逐字：*"A tooltip is a popup that displays information related to an element when the element receives keyboard focus or the mouse hovers over it. It typically appears after a small delay and disappears when `Escape` is pressed or on mouse out."* / *"**Tooltip widgets do not receive focus.** A hover that contains focusable elements can be made using a non-modal dialog."*

键盘契约逐字：`Escape`: *Dismisses the Tooltip.*；Note 三条：*"1. Focus stays on the triggering element while the tooltip is displayed. 2. If the tooltip is invoked when the trigger element receives focus, then it is dismissed when it no longer has focus (onBlur). 3. If the tooltip is invoked when a pointing cursor moves over the trigger element, then it remains open as long as the cursor is over the trigger or the tooltip."*

WAI-ARIA：容器 `role="tooltip"`；触发元素用 `aria-describedby` 指向 tooltip。

**裁决**：一旦 tooltip 里出现链接 / 按钮 / 输入框/ 可复制内容，它就不再是 tooltip，必须升级为 non-modal dialog 或 popover（并重新走 §1 四问）。**APG 该页自述 WIP、未达 task force consensus**，因此这里只引「不接收焦点 + Escape + 焦点留触发元素」这些明确文本，不把该页当稳定规范引数值。

**校验器见 §20.2**（Python 实跑）。

---

## 10. 浮层遮挡裁决：2.4.11 的四类官方判词、两条例外、通过手段与 F110

### 10.1 条文与两条 Note 逐字

> *When a user interface component receives keyboard focus, the component is not entirely hidden due to author-created content.*
>
> *Note 1: Where content in a configurable interface can be repositioned by the user, then only the initial positions of user-movable content are considered for testing and conformance of this success criterion.*
>
> *Note 2: Content opened by the **user** may obscure the component receiving focus. If the user can reveal the focused component without advancing the keyboard focus, the component with focus is not considered visually hidden due to author-created content.*

Intent 逐字：*"this AA criterion allows for the component receiving focus to be **partially** obscured ... For best visibility, **none** of the component receiving focus should be obscured. This preferred outcome is covered by the AAA criterion Focus Not Obscured (Enhanced)."* 判定对象注：*"This criterion evaluates the focused **component**, rather than the focus **indicator**."*（外部 focus indicator 被全遮 → 另判 2.4.7）。

### 10.2 四类叠加层的官方裁决表

| 形态 | W3C 裁决（逐字要点） | 结论 |
|---|---|---|
| 正确构建的模态 dialog | *"A properly constructed modal dialog will always pass this SC. Even if it appears directly on top of an item with focus, the dialog takes focus on appearance..."* | **PASS（确定性）** |
| 既不移入焦点、也不约束交互、也不失焦自关的 dialog-like overlay | *"will be at risk of failing this SC, where it is positioned such that it can obscure other focusable items."* | **FAIL 风险最高** |
| 用户显式打开、持续存在的 chat window / popover non-modal dialog | *"Such persistent content has the potential to fail Focus Not Obscured (Minimum)."*；但 Note 2 给了出路 | **可通过设计达标，非自动豁免** |
| 非持久展开内容（menu / select / combobox / date picker / tooltip） | *"Such non-persistent disclosures do not fail this SC since they do not obscure the item with focus. However, if an author allows such components to **persist** after the user has 1) activated one of the opened items or 2) moved the focus away ... it is at risk of failing this criterion"* | **默认 PASS，异常持久即转风险** |
| 作者预置 sticky footer/header、系统警告 | *"Content pre-positioned by the author (such as a sticky footer), or content that appears without direct user initiation, such as system warnings, must not prevent the item receiving focus from being immediately visible in the viewport."*；F110 为官方 Failure | **不享 Note 2 豁免，FAIL** |

### 10.3 Note 2 的三条合法出路（W3C 逐字示例）

> *keyboard actions that may allow the item with focus to be revealed include: using the `Escape` key to dismiss the obscuring content; using keys to scroll the content in the viewport to reveal the item with focus; issuing a key to move between overlays.*

官方三例：chat interface（*popover non-modal dialog*）遮住链接 → 按 `Escape` 关掉即露出；展开的 feedback 组件 → 方向键 / Space 滚动页面露出；多 overlay 协作应用 → `F6` 切换两层 overlay 的堆叠顺序。**共同点是「不推进键盘焦点就能显形」**——若必须 Tab 回浮层里点关闭按钮，Note 2 不成立。

### 10.4 通过手段（官方与工程分列）

- 官方充分技术 **C43**：*"Using CSS scroll-padding to un-obscure content"*；官方 Failure **F110**：*"due to a sticky footer or header completely hiding focused elements"*。
- 官方 Intent 里给 cookie banner 的两条路：*"making the banner modal so the user has to dismiss the banner before navigating through the page, or using scroll padding so the banner does not overlap other content"*；以及 *"Notifications that do not require user action could also meet this criterion by closing on loss of focus."*
- 另一条官方通过形态是**重排而非覆盖**：*"When the additional content appears, existing content reflows ... As a result, there is no overlapping content between the two sections; the item receiving focus ... will not be obscured"*（WCAG 标准的 pop-out sidebar 例）。**这是最稳的一条：能重排就别叠。**
- 工程约定（非规范）：焦点项进视口时给 `scroll-padding-block` 留出 sticky 高度；持久浮层提供 `Escape` 全局关闭 + `F6` 层间切换 + 关闭后 `focus` 归位；Tab 到被遮元素时自动把浮层降级或让位。这些是手段，不是条文。

**裁决器见 §20.3**（Python 实跑）。

---

## 11. SC 2.1.2 No Keyboard Trap：焦点循环允许的前提是「退出可知、可达」

条文（**Level A**）逐字：

> *If keyboard focus can be moved to a component of the page using a keyboard interface, then focus can be moved away from that component using only a keyboard interface, and, if it requires more than unmodified arrow or tab keys or other standard exit methods, the user is advised of the method for moving focus away.*
>
> *Note: Since any content that does not meet this success criterion can interfere with a user's ability to use the whole page, **all content on the web page ... must meet this success criterion.** See Conformance Requirement 5: Non-Interference.*

W3C Intent 直接点名本主题：*"There may be times when it's appropriate for a web page to restrict focus to a subsection of the content – **for example, when the user is inside a modal dialog or popover. This does not fail the requirements of this criterion, as long as the user knows how to 'untrap' the focus and leave that component.**"* 以及 *"Generally, in most environments with a physical keyboard, pressing the `Esc` key is a commonly used 'standard exit method'"*。

官方「A modal dialog box」示例逐字：*"When the dialog is open, focus is trapped within the dialog – tabbing from the last control in the dialog takes focus to the first control in the dialog ... The dialog is dismissed by activating the 'Cancel' button, the 'OK' button, or the `Esc` key."*

**三条可执行结论**：

1. **模态里的 Tab 循环合法**，因为 `Escape` / Cancel / OK 都构成键盘出口；这与 APG §3 的循环要求一致，不构成矛盾。
2. **若退出需要非标准键**（例如某编辑器用 `Alt+F10`），必须**事先告知**——官方 WYSIWYG 例：*"an instruction appears, letting users know that they can use `Alt+F10` / `Option+F10` to move focus back out"*。规范不定义 standard exit method，*this is dependent on the user's hardware, user agent, and operating system*，所以要按平台判断而不是硬编码。
3. **「有 `aria-modal` 但没有 Escape、没有可见关闭按钮」= 同时违反 2.1.2 与 APG §3.2 强推荐**；因为 Conformance Requirement 5 Non-Interference，这一处失败会拖累整页一致性声明。

---

## 12. SC 3.2.1 On Focus：focus 不得触发 change of context，hover 触发也不等于可以抢焦点

条文（**Level A**）逐字：*"When any user interface component receives focus, it does not initiate a change of context."*

`changes of context` 官方定义逐字：*"major changes that, if made without user awareness, can disorient users who are not able to view the entire page simultaneously"*；包括 *"changes of: user agent; viewport; focus; content that changes the meaning of the web page"*，例子 *"Opening a new window, moving focus to a different component, going to a new page ... or significantly re-arranging the content of a page"*。官方同时澄清：*"A change of content is not always a change of context. Changes in content, such as an expanding outline, dynamic menu, or a tab control do not necessarily change the context, unless they also change one of the above (e.g., focus)."*

**官方失败例（几乎就是本主题最常见的翻车）**：*"Example of a Failure: A help dialog — When a field receives focus, a help dialog window describing the field and providing options opens. As a keyboard user tabs through the web page, the dialog opens, **moving the keyboard focus away from the control every time the user attempts to tab past the field**."*

充分技术 **G107**：*"Using 'activate' rather than 'focus' as a trigger for changes of context"*。

**三条裁决**：

- **focus 打开模态 = 明确失败**。正确做法是把触发从 `onFocus` 改为显式激活（点击 / Enter / Space 的 `?` 帮助按钮），或改为不抢焦点的 tooltip / 行内说明。
- **hover 显示的内容也必须能由键盘 focus 触发**（1.4.13 Additional Notes 逐字），但**显示时不能移走焦点**——这正是 tooltip「不接收焦点」的意义。两条准则合起来给出同一结论：**用 activate 触发层，用 focus/hover 触发信息**。
- **「内容变化」与「上下文变化」要分开判**：展开菜单、tab 切换通常只是 change of content；一旦把焦点搬进新层，就升级为 change of context。

---

## 13. 关闭契约矩阵：closedby 三值与七条退出路径

| 退出路径 | 适用层 | 契约要求 | 官方依据 |
|---|---|---|---|
| `Escape` | 模态 dialog / auto·hint popover / tooltip | 模态必须；多个模态时**只关最后一层**；键盘关闭后焦点归 invoker | APG `Escape: Closes the dialog.`；MDN；APG Tooltip；MDN Using *focus is shifted back to the invoker* |
| 点 / 轻触外部（light dismiss） | `popover=auto|hint`、`<dialog closedby="any">` | 非模态可用；`manual` 与 `closedby="none|closerequest"` 不可用 | MDN Using / MDN `closedby` |
| 可见关闭按钮 | **所有层** | APG 强推荐在 tab 序列里；MDN 要求在没有物理键盘的设备上仍可关闭 | APG Note 3 / MDN |
| 平台返回 / dismiss 手势 | `closedby="any|closerequest"` 的 dialog | 触屏等价于 Esc；不要只实现 Esc | MDN `closedby` 定义 |
| 失焦自动关闭 | 非持久 tooltip / 菜单 | 持久浮层不能用它冒充「可消隐」，但可用于满足 2.4.11 的 notification 通过条件 | APG Tooltip Note 2 / W3C 2.4.11 Intent |
| 信息失效 | hover/focus 附加内容 | 唯一允许「非用户主动」消失的第三条（如 busy 状态结束） | SC 1.4.13 Persistent |
| `close()` / `requestClose()` / `<form method="dialog">` | 原生 dialog | `cancel` 事件先行，可 `preventDefault()` 做数据丢失确认；`returnValue` 承载结果 | MDN |

**关闭状态归位表（工程约定，逐项都要复位，缺一项就是「关了但没关干净」）**：

| 复位项 | 为什么 |
|---|---|
| `inert` / `aria-hidden` 解除 | 否则背景永久不可操作 |
| 背景滚动锁解除 | 否则页面卡死不可滚 |
| 焦点归还触发元素（或 APG Note 2 允许的逻辑后继） | 否则焦点掉到 `body`，键盘用户丢失位置 |
| `aria-expanded` / `aria-details` 状态复位 | 否则读屏仍报「已展开」 |
| 双栈 / 层叠栈出栈 | 否则下一次 `Escape` 关错层 |
| `returnValue` / 表单草稿状态处理 | 未保存内容要么保存、要么明确丢弃并确认 |
| 事件监听与定时器清理 | 否则重复打开叠加多个 handler |

**数据丢失裁决**：Apple HIG 逐字 *"When necessary, help people avoid data loss by getting confirmation before closing a modal view. Regardless of whether people use a dismiss gesture or a button, if closing the view could result in the loss of user-generated content, be sure to explain the situation and give people ways to resolve it."* → **确认要挂在所有关闭路径上**（含 Esc 与下滑手势），不是只挂在 X 按钮上。

---

## 14. 层叠与嵌套：一次一个、双栈、Escape 只关最后一层

- **Apple HIG 逐字**：*"**Let people dismiss a modal view before presenting another one.** Allowing multiple modal views to be visible at the same time tends to create visual clutter and can make your app seem scattered and disorganized. ... presenting multiple views adds to people's cognitive load, especially when a modal view hides another one by appearing on top of it. Although an alert can appear on top of all other content — including other modal views — you never want to display more than one alert at the same time."* 另一条：*"Take care to avoid creating a modal experience that feels like an app within your app. In particular, presenting a hierarchy of views within a modal task can make people forget how to retrace their steps."*
- **浏览器侧的对应规则**：多个 `<dialog>` 用 `showModal()` 时后进 top layer 者在上，`Escape` 只关最后一层（MDN，§5.2）；popover 侧 auto stack / hint stack 各自独立，隐藏时会 *walks back down that stack, closing any descendant popovers on that stack first*（§6.3）。
- **混合层级**：`showModal()` 会 dismiss 文档里其他元素的 `auto` popovers（MDN，§6.3）；`hint` 与 `manual` 不受影响。所以「打开确认弹窗时下拉菜单自动收起」是规范行为，**不要写额外的手动关闭逻辑去重复实现**（重复实现常导致关闭后 `aria-expanded` 状态错乱）。
- **portal 与 layer 的分工**：portal 到 `document.body` 解决的是 `overflow: hidden` / stacking context / 继承样式；top layer 解决的是绘制顺序；`inert` 解决的是交互权限。**三者互不替代**，Radix 把 `Dialog.Portal` 默认挂 `document.body` 正是前者的工程化（§16）。
- **层间切换键**：W3C 2.4.11 官方示例用 `F6` 在两个持久 overlay 间切换堆叠顺序（§10.3）。这是给「必须同时存在多层」的场景留的合规出路；**工程约定**：若产品确实需要多层持久浮层，提供 `F6` 并在帮助里告知（这也顺带满足 §11 的非标准退出法需告知）。

---

## 15. 组件族谱判型表（12 类；先判型再选实现）

| 形态 | Q1 inert | Q2 焦点进层/循环 | 建议机制 | 必过条款 | 备注 |
|---|---|---|---|---|---|
| Modal dialog | 是 | 是 | `<dialog>.showModal()` | 2.4.11 天然通过 / 2.1.2 给 Esc / APG 焦点契约 | 需 `aria-labelledby` 或 `aria-label` |
| Alert dialog（删除确认） | 是 | 是 | `role="alertdialog"` + 模态 | 同上 + `aria-describedby` 必需 | 初始焦点偏「最不破坏性动作」 |
| Non-modal dialog（查找替换、工具面板） | 否 | 可进层但**不循环** | `dialog.show()` / `closedby` | 2.4.11 遮挡（Note 2 三出路） | 外部仍可操作是设计目的 |
| Popover / 下拉菜单 / 操作菜单 | 否 | 不移入（只更新 tab 顺序） | `popover="auto"` | 2.4.11 非持久默认通过 | 一次一个；嵌套是例外 |
| Tooltip | 否 | **不接收焦点** | `role="tooltip"` / `popover="hint"` / `interestfor` | **1.4.13 三条件** | 含可聚焦元素即升级为 non-modal dialog |
| Toast / 轻提示 | 否 | 不抢焦点 | 归 `feedback-states.md` | 4.1.3 状态消息 | 不是 hover/focus 触发的附加内容，1.4.13 不适用 |
| Bottom sheet / 抽屉（模态） | 是 | 是 | 模态 dialog + 平台手势 | 同模态 + 返回手势 | 形态归 M3 / `navigation-ia.md`，契约归本文件 |
| 命令面板 / ⌘K | 否或视实现 | **必须自己 focus 输入框** | popover + 手动 focus / 或模态 | 2.1.2 + 2.4.11 | Popover API 不会自动移焦点（§6.4） |
| 常驻聊天窗 / 反馈组件 | 否 | 视实现 | `popover="manual"` | **2.4.11 重点风险** | 官方点名 *chat window* 有失败可能 |
| Cookie banner / sticky 提示 | 否 | 否 | 重排 或 模态化 | **2.4.11 / F110 重点风险** | 作者预置，不享 Note 2 豁免 |
| Lightbox / 图片查看 | 是 | 是 | 模态 dialog | 同模态 | 全屏可用（Apple HIG 允许 in-depth 全屏模态） |
| 新手引导 / 教学气泡 | 否 | 视实现 | `popover="auto"` | 2.4.11 + 1.4.13（若 hover 触发） | auto stack 天然保证一次一个 |

**一条速记**：**要不要模态，只取决于「用户此刻是否必须处理完才能回到原任务」**；Apple HIG 逐字 *"Present content modally only when there's a clear benefit. A modal experience takes people out of their current context and requires an action to dismiss"*、*"Aim to keep modal tasks simple, short, and streamlined"*、*"Make it easy to identify a modal view's task"*（给标题命名任务）。

---

## 16. 平台与设计系统口径（原文 vs 工程约定分列）

### 16.1 Apple HIG Modality（逐字）

定义：*"Modality is a design technique that presents content in a separate, dedicated mode that prevents interaction with the parent view and requires an explicit action to dismiss."* —— 与 APG 的 inert 定义在语义上完全一致：**阻止与父视图交互 + 需要显式动作关闭**。

Best practices 逐字要点：*"Present content modally only when there's a clear benefit."* / *"Aim to keep modal tasks simple, short, and streamlined."* / *"Take care to avoid creating a modal experience that feels like an app within your app."* / *"Consider using a full-screen modal style for in-depth content or a complex task."* / *"**Always give people an obvious way to dismiss a modal view.**"* / *"When necessary, help people avoid data loss by getting confirmation before closing a modal view."* / *"Make it easy to identify a modal view's task."* / *"**Let people dismiss a modal view before presenting another one.**"* 平台差异：iOS/iPadOS/watchOS 常在顶部工具栏给按钮或下滑；macOS/tvOS 期望主内容区按钮；visionOS / 全屏模态另有口径。变更日志：2023-12-05 强化 in-depth 与多模态指引，2023-06-21 加入 visionOS。

### 16.2 Radix Primitives Dialog（逐字）

Features 逐字：*"Supports modal and non-modal modes."* / *"**Focus is automatically trapped within modal.**"* / *"Manages screen reader announcements with `Title` and `Description` components."* / *"Esc closes the component automatically."*
API：`Root.modal` 类型 `boolean`，**默认 `true`**；`Portal.container` 默认 `document.body`；`Overlay` 被描述为 *"A layer that covers the inert portion of the view when the dialog is open."*；`Content` 暴露 `onOpenAutoFocus` / `onCloseAutoFocus` / `onEscapeKeyDown` / `onPointerDownOutside` / `onInteractOutside`。
Accessibility 页逐字：*"Adheres to the Dialog WAI-ARIA design pattern."*；键盘表 `Space` / `Enter` 开关、`Tab` / `Shift+Tab` 移动、`Esc` *"Closes the dialog and moves focus to `Dialog.Trigger`"*。
`Description` 页逐字：*"An optional accessible description to be announced when the dialog is opened ... If you want to remove the description entirely, remove this part and pass `aria-describedby={undefined}` to `Dialog.Content`."* —— 这条常被忽略：删了组件但没清 `aria-describedby`，读屏会指向不存在的 id。

**裁决（工程约定）**：用库时把「modal 默认值」当作契约的一部分写进设计系统文档；切 `modal={false}` 属于改变键盘与 inert 行为，按 `component-api-design.md` 的 SemVer 冻结面应判 **MAJOR 级别的行为变更**（该资产 §14 已把「键盘与 tab stop 策略」列为 MAJOR）。

### 16.3 Material 3 / Open UI（口径限制）

M3 `components/dialogs/overview` 与 `components/bottom-sheets/overview` 本轮均返回 200，但内容为 JS 动态渲染，未取得可逐字核验的尺寸 / 时长 / 行为数值，**因此本文件不引用任何 M3 精确数值**（见 §22 取源限制）。Open UI 是 Popover API 提案来源（`openui/open-ui` API 实测 4,540★ / NOASSERTION / 2026-11-10），但规范条文一律以 WHATWG HTML + MDN 为准，不以提案文档为准。

### 16.4 GitHub API 实测 10 库（2026-11-11）

| 仓库 | ★ | SPDX | pushed_at | archived |
|---|---|---|---|---|
| `radix-ui/primitives` | 19,493 | MIT | 2026-10-14 | False |
| `floating-ui/floating-ui` | 32,800 | MIT | 2026-11-04 | False |
| `adobe/react-spectrum` | 16,025 | Apache-2.0 | 2026-11-11 | False |
| `ariakit/ariakit` | 8,632 | 未检出 SPDX | 2026-11-11 | False |
| `tailwindlabs/headlessui` | 28,823 | MIT | 2026-04-13 | False |
| `openui/open-ui` | 4,540 | NOASSERTION | 2026-11-10 | False |
| `w3c/aria-practices` | 1,362 | NOASSERTION | 2026-11-11 | False |
| `KittyGiraudel/a11y-dialog` | 2,492 | MIT | 2026-11-09 | False |
| `focus-trap/focus-trap` | 1,564 | MIT | 2026-11-11 | False |
| `reactjs/react-modal` | 7,405 | MIT | 2026-03-02 | False |

> 口径纪律：`NOASSERTION` ≠ 无许可、未检出 SPDX ≠ 未授权；`ariakit/ariakit` 与 `openui/open-ui` 的具体许可须到仓库 LICENSE 文件逐字核验，本表只记录 API 返回的字段，**不做推断**。★ 与 pushed_at 为 2026-11-11 快照，不可当长期事实。

---

## 17. 12 场景决策速查

1. **删除确认**：`role="alertdialog"` + 模态 + `aria-describedby` 指向后果说明；初始焦点落「取消」（APG 最不破坏性动作）；Esc / 取消 / 确认三条路径都归位焦点。
2. **登录 / 支付等不可中断流程**：模态，但按 Apple HIG 保持 simple / short；嵌套子视图改为单路径，避免「app within your app」。
3. **表单字段的帮助说明**：**不要** `onFocus` 开模态（SC 3.2.1 官方失败例）；改为行内说明、`?` 按钮显式激活、或 tooltip（不接收焦点 + Esc）。
4. **表格行操作菜单**：`popover="auto"`，一次一个；`popovertarget` 让浏览器建立 `aria-details` / `aria-expanded`；键盘关闭后焦点回 invoker。
5. **工具栏按钮的 hover 提示**：`popover="hint"`（不打断已打开的 auto 菜单）或 `interestfor`；必须过 1.4.13 三条件；`hint` 在不支持浏览器会降级为 `manual`，需能力检测。
6. **包含链接 / 复制按钮的「富 tooltip」**：升级为 non-modal dialog / popover，重新走 §1 四问；不能再叫 tooltip。
7. **⌘K 命令面板**：popover 不会替你移焦点——`showPopover()` 后自己 `input.focus()`，自己实现 Esc / 外部点击 / 关闭后焦点回触发处；若同时锁背景交互，就老实做成模态。
8. **常驻客服聊天窗**：官方点名 `chat window` 有 2.4.11 失败可能；给出 `Escape` 收起 + `F6` 切层 + 关闭后归位；或改为重排式侧栏（WCAG pop-out sidebar 例）。
9. **底部 cookie banner**：作者预置、不享 Note 2 豁免；二选一——**模态化**（必须先处理才能导航）或 **`scroll-padding` / 重排**（不覆盖焦点项）；sticky footer 完全遮住焦点项是 F110。
10. **移动端 bottom sheet**：模态时接管焦点 + inert + 返回手势等价于 Esc；`closedby` 的 *"a 'back' or 'dismiss' gesture on mobile platforms"* 正是为此；关闭前若有草稿要确认。
11. **弹窗内还有第二个确认弹窗**：浏览器 Escape 只关最后一层；但 Apple HIG 要求先关前一个再呈现下一个，工程上优先**串行而非堆叠**；确需堆叠时给 `F6` 切层并显式告知。
12. **半透明遮罩下的焦点环**：2.4.11 可能 PASS，但 focus indicator 受遮罩影响后要按 **1.4.11 Non-text Contrast** 重算，不能只看「没被完全挡住」。

---

## 18. 20 反模式（每条都给出违反的契约）

1. 用 `position: fixed` + `z-index: 9999` + 半透明遮罩冒充 inert 层：没有 top layer、Tab 跑到背景 → §2 裁决二 / §7。
2. `<dialog open>` 或 CSS `display: block` 打开，却按模态设计：浏览器暴露 `aria-modal="false"` → §5。
3. 只加 `aria-modal="true"` 不做 inert / 不循环焦点：对读屏用户「关闭了半个页面」 → §4。
4. 用 `pointer-events: none` 盖背景冒充 inert：挡不住 Tab / 读屏 / 键盘滚动 → §7。
5. 给 hover 触发的 tooltip 加 3 秒自动消失：违反 Persistent → §9。
6. tooltip 里塞链接 / 按钮：APG 明确 tooltip 不接收焦点，应升级为 non-modal dialog → §9.3。
7. `onFocus` 打开帮助弹窗并抢焦点：SC 3.2.1 官方 Failure 例 → §12。
8. 模态不给 `Escape`，只给右上角 X：违反 APG 键盘契约与 2.1.2 出口 → §3 / §11。
9. 模态不给可见关闭按钮：违反 APG 强推荐且触屏 / 无物理键盘设备无路可退 → §3.2。
10. 关闭后焦点掉到 `body`：违反 APG Note 2 → §3.2。
11. dialog portal 挂进被 `aria-hidden="true"` 的容器：把自己也隐藏了 → §3.4。
12. 全局禁用 `Escape` 来「防误关」：MDN 明确键盘用户期望 Esc；应改用 `cancel` + `preventDefault()` → §5.1。
13. 表单 dialog 的「取消」按钮不带 `formnovalidate`：required 输入未填时关不掉 → §5.2。
14. 把 `popover` 当模态用（以为 `popover="manual"` 就是模态）：Popover API 恒非模态 → §6.1。
15. 命令面板 `showPopover()` 后不手动 focus：浏览器只更新 tab 顺序，输入框收不到焦点 → §6.4。
16. 用 `popover="hint"` 却不做降级：`hint` 在不支持浏览器回落 `manual`（可多个并存、不自动关） → §6.2。
17. 同时叠两层持久 overlay 且不给切层键：2.4.11 风险 + Apple HIG 认知负荷 → §10.3 / §14。
18. 持久 chat window 只提供「点 X 关闭」：Note 2 要求**不推进键盘焦点**就能显形，Tab 回浮层点 X 不算 → §10.3。
19. 给「看起来像弹窗」的层既不接管焦点、也不约束交互、也不失焦自关：W3C 点名 `dialog-like overlay` 失败风险最高 → §2 裁决三 / §10.2。
20. 验收里写「遮罩淡出动画」：MDN 明确 backdrop 关闭时立即从 DOM 移除，无法做退场淡出 → §5.2。

---

## 19. 20 项自检（交付前逐条给证据）

- [ ] 四问答完并写进组件 API（inert / 焦点 / 触发 / 退出），没有「先画遮罩再补逻辑」？
- [ ] `aria-modal="true"` 只在 inert + 视觉遮蔽双条件都成立时才出现？
- [ ] 打开时焦点进层；`Tab` / `Shift+Tab` 在层内循环；没有正 `tabindex`？
- [ ] `Escape` 能关；多个模态时只关最后一层；关闭后焦点归位到触发元素或 APG Note 2 允许的逻辑后继？
- [ ] tab 序列里有**可见**的关闭控件，且无物理键盘设备也能关？
- [ ] 容器有 `aria-labelledby`（指向可见标题）或 `aria-label`？含语义结构时省略了 `aria-describedby`？
- [ ] alertdialog 的 `aria-describedby` 指向警告正文？初始焦点落在最不破坏性动作？
- [ ] `<dialog>` 容器本身**没有** `tabindex`；内部静态标题用的 `tabindex="-1"` 与之不混淆？
- [ ] 用 `showModal()`（而非 `open` 属性 / CSS display）来表达模态？`autofocus` 指向最合理的初始落点？
- [ ] `closedby` 按数据丢失风险选 `any` / `closerequest` / `none`；需要拦 Esc 时用 `cancel` + `preventDefault()`？
- [ ] `<form method="dialog">` 的取消按钮有 `formnovalidate`？`returnValue` 三出口（按钮 / Esc / requestClose）都验过？
- [ ] dialog 进出场动画用了 `@starting-style` + `display` + `overlay` + `allow-discrete` 四件套，且**没有**声称 backdrop 能淡出？
- [ ] 非模态浮层选了正确的 popover 态（auto 一次一个 / hint 不关 auto / manual 必须显式关）？`hint` 做了降级？
- [ ] hover 打开的内容自己 focus 输入框了吗（若有），并且关闭时焦点回 invoker？
- [ ] hover/focus 附加内容逐条过 Dismissible（Esc 不移动焦点）/ Hoverable（指针可移到浮层）/ Persistent（无定时器）？
- [ ] tooltip 不接收焦点、焦点留在触发元素、内容里没有可聚焦元素？
- [ ] 所有层都不遮死获得键盘焦点的组件；持久层给了 Escape / 滚动 / F6 切层之一？sticky 层用了 `scroll-padding`（C43）或重排？
- [ ] 半透明 / 模糊遮罩下的 focus indicator 按 1.4.11 重算过对比度？
- [ ] 模态内部没有「app within your app」的多层视图层级；同时存在的 alert 只有一个？
- [ ] 关闭时七项复位（inert / 滚动锁 / 焦点 / aria 状态 / 层叠栈 / 草稿与 returnValue / 监听器）逐项验过？`§20.1`–`§20.3` 三个校验器跑过？

---

## 20. 5 段可抄代码（§20.1–§20.3 为 Python 实跑）

### 20.1 模态性判型器（Python，实跑 PASS）

把 §1 四问 + §4 双条件 + §2 裁决三编译成可执行断言。输入是组件声明，输出是应走的契约与违规项。

```python
from dataclasses import dataclass, field

@dataclass
class OverlaySpec:
    name: str
    background_inert: bool          # Q1
    focus_moves_in: bool            # Q2
    tab_cycles_inside: bool         # Q2
    trigger: str                    # Q3: "activate" | "hover" | "focus"
    escape_closes: bool             # Q4
    visible_close_control: bool     # Q4
    background_obscured: bool       # aria-modal 条件 2
    aria_modal: bool = False        # 作者声明
    focus_returns: bool = True
    persistent: bool = False        # 是否会一直盖着不走


@dataclass
class Verdict:
    kind: str
    contract: list = field(default_factory=list)
    violations: list = field(default_factory=list)

    @property
    def ok(self):
        return not self.violations


def classify(s: OverlaySpec) -> Verdict:
    v = Verdict(kind="undetermined")
    modal_behavior = s.background_inert and s.focus_moves_in and s.tab_cycles_inside
    v.contract.append("inert+focus" if modal_behavior else "non-modal")

    # 硬约束一：Q3。hover/focus 触发不允许模态，且构成 3.2.1 / 1.4.13 适用面
    if s.trigger in ("hover", "focus") and modal_behavior:
        v.violations.append(
            "SC 3.2.1 / 1.4.13: modal must not appear on hover or focus")
    if s.trigger == "focus" and s.focus_moves_in:
        v.violations.append(
            "SC 3.2.1: focus changed the context (help-dialog failure)")

    # 硬约束二：Q4。焦点循环必须有键盘出口 + 可见关闭控件
    if s.tab_cycles_inside and not (s.escape_closes and s.visible_close_control):
        v.violations.append("SC 2.1.2 / APG: focus loop without keyboard exit")
    if not s.visible_close_control:
        v.violations.append("APG Note 3 / MDN: no visible close mechanism")

    # 硬约束三：aria-modal 双条件（APG 逐字）
    if s.aria_modal and not (s.background_inert and s.background_obscured):
        v.violations.append(
            "APG: aria-modal=true requires inert code AND obscured visuals")
    if modal_behavior and not s.aria_modal:
        v.violations.append("modal behavior should declare aria-modal=true")

    # 伪模态：W3C 点名 2.4.11 最高风险
    pseudo = (s.persistent and not s.focus_moves_in
              and not s.background_inert)
    if pseudo:
        v.kind = "dialog-like-overlay (SC 2.4.11 risk)"
        v.violations.append(
            "SC 2.4.11: persistent overlay takes no focus, does not inert, "
            "and does not dismiss on loss of focus")

    if v.kind == "undetermined":
        v.kind = "modal dialog" if modal_behavior else "non-modal overlay"
    if modal_behavior and not s.focus_returns:
        v.violations.append("APG Note 2: focus must return on close")
    if s.trigger in ("hover", "focus"):
        v.contract.append("SC 1.4.13 Dismissible/Hoverable/Persistent")
    if s.persistent:
        v.contract.append("SC 2.4.11 reveal-without-advancing-focus")
    return v


CASES = [
    OverlaySpec("ok-modal", True, True, True, "activate", True, True, True,
                aria_modal=True),
    OverlaySpec("aria-modal-lie", False, True, True, "activate", True, True,
                True, aria_modal=True),
    OverlaySpec("focus-help-dialog", True, True, True, "focus", True, True,
                True, aria_modal=True),
    OverlaySpec("no-escape", True, True, True, "activate", False, True, True,
                aria_modal=True),
    OverlaySpec("pseudo-overlay", False, False, False, "activate", True, True,
                False, persistent=True),
    OverlaySpec("ok-popover", False, False, False, "hover", True, True, False,
                persistent=False),
]

if __name__ == "__main__":
    for c in CASES:
        r = classify(c)
        print("%-20s %-38s ok=%-5s %s"
              % (c.name, r.kind, r.ok, "; ".join(r.violations) or "-"))
    assert classify(CASES[0]).ok is True
    assert "aria-modal=true requires" in " ".join(classify(CASES[1]).violations)
    assert any("3.2.1" in x for x in classify(CASES[2]).violations)
    assert any("exit" in x for x in classify(CASES[3]).violations)
    assert any("2.4.11" in x for x in classify(CASES[4]).violations)
    assert classify(CASES[5]).ok is True
    print("20.1: 6/6 assertions PASS")
```

### 20.2 SC 1.4.13 三条件校验器（Python，实跑 PASS）

```python
from dataclasses import dataclass

@dataclass
class HoverContent:
    name: str
    trigger: str                 # "hover" | "focus" | "activate"
    dismiss_without_moving: bool # Escape 全局可关，不移动 hover/focus
    pointer_reaches_content: bool
    stays_until: str             # "trigger_removed" | "user_dismissed"
                                 # | "info_invalid" | "timeout"
    input_error: bool = False
    obscures_content: bool = True
    ua_controlled: bool = False
    receives_focus: bool = False


def check_1413(c: HoverContent) -> list:
    """返回违反项；空列表即通过。逐字口径见 §9。"""
    if c.trigger == "activate" or c.ua_controlled:
        return []                        # 不在适用范围 / UA Exception
    bad = []
    if not c.dismiss_without_moving and not (c.input_error
                                             or not c.obscures_content):
        bad.append("Dismissible")
    if c.trigger == "hover" and not c.pointer_reaches_content:
        bad.append("Hoverable")
    if c.stays_until == "timeout":
        bad.append("Persistent (timeout is not one of the three exits)")
    if c.receives_focus:
        bad.append("APG: tooltip widgets do not receive focus; "
                   "upgrade to a non-modal dialog")
    return bad


CASES_1413 = [
    HoverContent("good-tooltip", "hover", True, True, "trigger_removed"),
    HoverContent("auto-hide-3s", "hover", True, True, "timeout"),
    HoverContent("gap-closes", "hover", True, False, "trigger_removed"),
    HoverContent("input-error", "hover", False, True, "trigger_removed",
                 input_error=True, obscures_content=True),
    HoverContent("focusable-tooltip", "focus", True, True, "trigger_removed",
                 receives_focus=True),
    HoverContent("title-attr", "hover", False, False, "timeout",
                 ua_controlled=True),
    HoverContent("click-menu", "activate", False, False, "timeout"),
]

if __name__ == "__main__":
    want = [[], ["Persistent"], ["Hoverable"], [],
            ["APG"], [], []]
    for c, w in zip(CASES_1413, want):
        got = check_1413(c)
        print("%-20s -> %s" % (c.name, got or "PASS"))
        assert all(any(k in g for g in got) for k in w), (c.name, w, got)
        assert len(got) == len(w), (c.name, w, got)
    print("20.2: 7/7 assertions PASS")
```

### 20.3 SC 2.4.11 遮挡裁决器（Python，实跑 PASS）

```python
from dataclasses import dataclass

@dataclass
class ObscureCase:
    name: str
    properly_modal: bool
    takes_focus_on_appearance: bool
    constrains_interaction: bool
    dismisses_on_loss_of_focus: bool
    persistent: bool
    user_opened: bool
    author_prepositioned: bool
    entirely_hides_focused: bool
    reveal_without_advancing_focus: bool


def check_2411(c: ObscureCase) -> str:
    """返回 PASS / EXEMPT / RISK / FAIL，口径见 §10。"""
    if c.properly_modal:
        return "PASS"          # W3C: will always pass this SC
    if not c.entirely_hides_focused:
        return "PASS"          # partially obscured 仍可满足 AA
    if not c.persistent and c.dismisses_on_loss_of_focus:
        return "EXEMPT"        # non-persistent disclosures 不因遮挡失败
    if c.user_opened and c.reveal_without_advancing_focus:
        return "EXEMPT"        # Note 2
    if c.author_prepositioned:
        return "FAIL"          # sticky footer / system warnings: F110
    # 只有「非用户发起」的三不 dialog-like overlay 才直接 FAIL（§10.2 第 2 行）；
    # user-opened 持久层缺 Escape / F6 出路时，按 §10.2 第 3 行判 RISK
    # （"has the potential to fail"，非自动豁免、亦非确定性失败）。
    if (not c.user_opened
            and not c.takes_focus_on_appearance
            and not c.constrains_interaction
            and not c.dismisses_on_loss_of_focus):
        return "FAIL"          # dialog-like overlay，W3C 点名风险最高
    return "RISK"              # user-opened 持久层：Note 2 三条出路缺失


CASES_2411 = [
    ObscureCase("modal-dialog", True, True, True, False, True, True, False,
                True, False),
    ObscureCase("partial-overlay", False, False, False, False, True, True,
                False, False, False),
    ObscureCase("open-menu", False, False, False, True, False, True, False,
                True, False),
    ObscureCase("chat-esc", False, False, False, False, True, True, False,
                True, True),
    # chat-tab-back：用户自己打开的持久浮层，但只能 Tab 回去点 X，
    # 不满足「不推进键盘焦点即可显形」 → Note 2 不成立 → RISK。
    ObscureCase("chat-tab-back", False, False, False, False, True, True,
                False, True, False),
    ObscureCase("sticky-footer", False, False, False, False, True, False,
                True, True, False),
    # pseudo-overlay：非用户发起、不请自来的 dialog-like overlay（三不），
    # 不享 Note 2 豁免 → FAIL。与上行 chat-tab-back 的唯一区别是 user_opened。
    ObscureCase("pseudo-overlay", False, False, False, False, True, False,
                False, True, False),
]

if __name__ == "__main__":
    want = ["PASS", "PASS", "EXEMPT", "EXEMPT", "RISK", "FAIL", "FAIL"]
    for c, w in zip(CASES_2411, want):
        got = check_2411(c)
        print("%-18s -> %s (want %s)" % (c.name, got, w))
        assert got == w, (c.name, got, w)
    print("20.3: 7/7 assertions PASS")
```

### 20.4 原生 HTML / CSS 契约骨架（可抄）

```html
<button id="edit-trigger" commandfor="edit-dlg" command="show-modal">编辑资料</button>

<dialog id="edit-dlg" closedby="none" aria-labelledby="edit-title">
  <h2 id="edit-title">编辑资料</h2>
  <!-- 静态标题不抢焦点；容器本身禁止 tabindex -->
  <form method="dialog" id="edit-form">
    <label>显示名 <input name="displayName" required autofocus></label>
    <button value="save">保存</button>
    <button value="cancel" formnovalidate>取消</button>
  </form>
</dialog>

<!-- 非模态操作菜单：auto 态一次只显示一个；hint 态不关闭它 -->
<button popovertarget="row-menu" popovertargetaction="toggle" id="row-btn">操作</button>
<div id="row-menu" popover="auto" role="menu">…</div>
<button interestfor="hint-1" id="hint-src">为何禁用？</button>
<div id="hint-1" popover="hint" role="tooltip">需先完成验证</div>
```

```css
/* 进出场四件套：display / overlay 必须进 transition 列表 */
dialog {
  opacity: 0;
  transform: translateY(8px);
  transition: opacity .18s ease, transform .18s ease,
              display .18s allow-discrete, overlay .18s allow-discrete;
}
dialog:open { opacity: 1; transform: none; }
@starting-style { dialog:open { opacity: 0; transform: translateY(8px); } }
dialog::backdrop { background: rgb(0 0 0 / .5); }

/* C43：给 sticky 层留出焦点项滚动余量（工程约定，数值按实际高度定） */
html { scroll-padding-block-end: 96px; }
```

> 提醒：`closedby="none"` 时 Esc / 点外部都不关，必须靠表单里的「取消」按钮；若要拦数据丢失，用 `cancel` 事件 `preventDefault()` + 确认，不要全局屏蔽 Esc。`<dialog>` 上加 `tabindex` 是 MDN 明文禁止的。

### 20.5 自定义实现的关闭契约状态机（TypeScript，可抄）

```ts
type Layer = {
  id: string;
  trigger: HTMLElement;
  el: HTMLElement;
  modal: boolean;
  onClose?: (reason: string) => void;
};

class OverlayStack {
  private stack: Layer[] = [];

  open(layer: Layer) {
    if (layer.modal) {
      // 背景 inert 与滚动锁必须成对，且 dialog 不能是被 inert 的容器的后代
      document.getElementById('app')?.setAttribute('inert', '');
      document.body.style.overflow = 'hidden';
      layer.el.setAttribute('aria-modal', 'true');
      layer.el.querySelector<HTMLElement>('[data-autofocus]')?.focus();
    }
    this.stack.push(layer);
  }

  close(reason: string) {
    const layer = this.stack.pop();
    if (!layer) return;
    if (layer.modal) {
      document.getElementById('app')?.removeAttribute('inert');
      document.body.style.overflow = '';
      layer.el.removeAttribute('aria-modal');
    }
    layer.trigger.setAttribute('aria-expanded', 'false');
    // APG Note 2：归位触发元素；触发元素已不存在时交给逻辑后继
    (layer.trigger.isConnected
      ? layer.trigger
      : layer.el.querySelector<HTMLElement>('[data-successor]')
        ?? document.body)?.focus();
    layer.onClose?.(reason);
  }

  // 只关最后一层；不许一次清栈（MDN + 双栈语义）
  onEscape = () => { if (this.stack.length) this.close('escape'); };
  onF6 = () => { /* 两个持久 overlay 间切换堆叠顺序，2.4.11 官方示例 */ };
}
```

> 这是**工程约定骨架**，不是规范实现。原生 `showModal()` 已代劳 inert / top layer / Escape / 隐式 `aria-modal`，能用原生就不要自己写；这段只用于必须自定义（如跨框架 portal、非 HTML 渲染器）的场景。生产代码还需补：Tab 循环、`inert` 的 SSR 一致性、`cancel` 事件的数据丢失确认、`hint` 降级能力检测、focus ring 在遮罩下的 1.4.11 对比度。

---

## 21. 来源与引用（含置信度）

| # | 来源 | 用到的逐字内容 | 置信度 |
|---|---|---|---|
| 1 | W3C APG Dialog (Modal) Pattern | inert 定义、Keyboard Interaction 全表、Note 1/2/3、`aria-modal` 双条件、WAI-ARIA 清单、`aria-hidden` 旧实现两条 | **规范级 / 原文核对** |
| 2 | W3C APG Alert and Message Dialogs | `role=alertdialog`、`aria-describedby` 必需、键盘契约指向 modal dialog | 规范级 / 原文核对 |
| 3 | W3C APG Tooltip Pattern | tooltip 定义、不接收焦点、Escape、三条 Note、`role=tooltip` / `aria-describedby` | **WIP 页**（自述未达共识），仅取明确文本 |
| 4 | MDN `<dialog>` | showModal/show/open、隐式 aria-modal、closedby 三值、autofocus、`tabindex` 禁令、Escape 只关最后一层、cancel/returnValue、动画四件套、Invoker Commands | 官方文档 / 原文核对 |
| 5 | MDN Popover API + Using | always non-modal、三态、双栈六规则、light dismiss、焦点只更新 tab 顺序、隐式 aria-details/aria-expanded、hint 降级、事件与方法 | 官方文档 / 原文核对 |
| 6 | MDN `inert` / Top layer / `::backdrop` | inert 行为、top layer 与 accessibility tree | 官方文档 |
| 7 | W3C WCAG 2.2 Understanding 1.4.13 | 规范性条文三条件、Exception、Note 1–3、modal out of scope、Intent 两豁免、Intent 三条件解释 | **规范级 / 原文核对** |
| 8 | W3C WCAG 2.2 Understanding 2.4.11 | AA 条文 + Note 1/2、modal always pass、dialog-like overlay 风险、user-opened 三出路、C43 / F110、overlay 与 1.4.11 交叉 | **规范级 / 原文核对** |
| 9 | W3C WCAG 2.2 Understanding 2.1.2 | A 条文、Non-Interference Note、modal/popover 焦点限制合法、Esc 为 standard exit method、modal dialog 示例 | 规范级 / 原文核对 |
| 10 | W3C WCAG 2.2 Understanding 3.2.1 | A 条文、changes of context 定义、help dialog 失败例、G107、content≠context | 规范级 / 原文核对 |
| 11 | Apple HIG Modality | 定义 + 8 条 Best practices 逐字 + 平台差异 + Change log 2023 两条 | 厂商指南 / 原文核对 |
| 12 | Radix Primitives Dialog | modal 默认 true、focus trap、Esc 回 Trigger、Overlay 描述、Description 的 `aria-describedby={undefined}`、键盘表 | 官方文档 / 原文核对 |
| 13 | WHATWG HTML popover / Open UI | 规范指向与提案沿革 | 仅登记，条文一律以 MDN/W3C 为准 |
| 14 | GitHub REST API `/repos/{owner}/{repo}` | 10 库 star / license / pushed_at / archived（2026-11-11 实测） | 实测快照，会过期 |

**引用纪律**：逐字英文只在本文件出现一次，SKILL.md / README 的转述不得升格为条文；`popover` 术语的「上位概念 vs 具体 API」差异（§6.1）在转述时必须保留，否则会把「always non-modal」误读成「所有浮层都非模态」。

---

## 22. 取源限制（公开记录，不臆造）

1. **M3 两页为 JS 动态渲染**：`components/dialogs/overview` 与 `components/bottom-sheets/overview` 均 200，但无可逐字核验的尺寸 / 时长 / 交互数值，故本文件**不含任何 M3 精确数值**；M3 相关形态只作定性描述并标「形态归 M3，契约归本文件」。
2. **APG Tooltip Pattern 自述 WIP**：页面首行 *"this design pattern is work in progress; it does not yet have task force consensus"*，因此只引「不接收焦点 / Escape / 焦点留触发元素」等明确文本，不把该页当稳定规范；tooltip 的合规条文以 WCAG SC 1.4.13 为准。
3. **`hint` 态与 interest invokers 属较新能力**：MDN Popover API 页标注 `Baseline 2025`（*"Since January 2025, this feature works across the latest devices and browser versions"*，页尾 last modified 2025-12-17），但 `popover="hint"` / `interestfor` 的跨浏览器可用性本轮**未做逐浏览器实测**，故一律要求能力检测与降级，不写成「已全面可用」。
4. **SC 2.4.11 的「not entirely hidden」没有独立术语定义**：Understanding 的 Key Terms 只定义了 `user interface component`；`at least partially visible` / `always partially visible in the user's viewport` 属 In Brief / Intent 的解释性表述，不是术语定义。本文件按解释性表述引用。
5. **SC 2.1.2 未定义 standard exit method**：原文明确 *"This specification does not define what constitutes a 'standard exit method'"*，故 `Alt+F10` 一类按键是否标准须按平台判断，不能写成全局常量。
6. **`NOASSERTION` / 未检出 SPDX 不等于无许可**：`ariakit/ariakit`、`openui/open-ui`、`w3c/aria-practices` 的许可字段未给出具体 SPDX，具体条款须读仓库 LICENSE，本表只记录 API 返回，不做推断。
7. **GitHub star / pushed_at 是 2026-11-11 快照**，不可当长期事实；`archived=False` 同理。
8. **§13 归位表的「背景滚动锁」「aria 状态复位」「监听器清理」为工程约定**，规范原文未逐字要求；`scroll-padding-block-end: 96px` 是示意值，不是官方数值（官方只给 C43 技术方向）。
9. **§20.1–§20.3 三个校验器是本知识库的工程裁决编码**，不是 W3C 提供的判定程序；它们把逐字条文简化成布尔条件，**不能替代真机 / 读屏 / 键盘走查**。
10. **§20.5 的 TypeScript 骨架是伪实现级别**，未覆盖 portal SSR、`inert` polyfill、嵌套 dialog 栈、读屏播报；引用时必须连同这段限制一起给。
11. **本轮未做用户实测**（无真实用户、无读屏器、无跨浏览器矩阵），所有「场景 / 反模式 / 自检」是规范 + 官方文档的推理产物，标注为工程约定。

---

## 23. 与既有资产边界矩阵

| 相邻资产 | 它管什么 | 本文件管什么 | 重叠处的裁决 |
|---|---|---|---|
| `feedback-states.md` | 五层反馈、toast 时长、确认框八条、五级错误 | 层的 inert / 焦点 / 退出 / 遮挡契约 | toast 的**时长**归前者；toast 若为 `popover` 且持久，则**遮挡**归本文件 |
| `shape-elevation.md` | 圆角、阴影、语义 z-index 刻度、表面层级 | top layer 与 z-index 的分界 | `z-index` 数值归前者；「z-index 抢不过 top layer」归本文件 |
| `accessibility.md` | WCAG 2.2 全量阈值、focus ring 样式、目标尺寸 | 1.4.13 / 2.4.11 / 2.1.2 / 3.2.1 四条款的叠加层专用裁决 | 阈值数值归前者；四条款合取验收归本文件 |
| `component-api-design.md` | props 所有权、SemVer 冻结面、单 tab stop | 把判型结果写进组件 API 的哪些字段 | 「改键盘策略 = MAJOR」归前者；`modal` 默认值改动按该裁决判级 |
| `design-ethics-inclusion.md` | cookie wall、对称选择、一键关闭 | cookie banner 的 2.4.11 遮挡与 F110 | 同意机制的合法性归前者；是否遮住焦点项归本文件 |
| `content-findability.md` | combobox / 自动补全 aria 明细、搜索体验 | 下拉面板作为 popover 的三态与遮挡 | aria 明细归前者；`popover=auto` 栈规则归本文件 |
| `navigation-ia.md` | drawer / rail / tab 的导航选型 | 抽屉作为模态 / 非模态的契约 | 选型归前者；inert 与焦点归本文件 |
| `ux-writing.md` | 对话框文案、按钮文案 | 标题作为 `aria-labelledby` 目标、任务命名 | 措辞归前者；「必须有可访问名」归本文件 |
| `motion-orchestration.md` | `@starting-style` / `allow-discrete` 动效原理 | dialog 专属四件套与 backdrop 无法淡出 | 原理归前者；dialog 落地限制归本文件 |
| `conversational-generative-ui.md` | 聊天输出链路、状态播报 | 聊天窗作为持久浮层的 2.4.11 遮挡与切层 | 输出链路归前者；窗口作为 overlay 归本文件 |

---

## 24. 接线

**接线**：SKILL.md 资产表 / 意图路由 / 第 5 步 / 第 41 条自检 · mindmap INTENTS · regression NEW_QUERIES · knowledge-map 支线 AE · memory/aliases.json 检索层别名（**不改路由优先级**）· README 统计重算。
