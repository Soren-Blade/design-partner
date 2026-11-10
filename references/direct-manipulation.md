# 直接操纵与指针交互（Direct Manipulation / Pointer, Gesture & Drag-and-Drop）

> 快照 2026-11-10 · 26 节 · 12 场景 · 20 反模式 · 20 自检 · 5 段可抄代码（3 段 Python 已实跑）

把「加个拖拽手柄、绑几个 `mousemove`、再补个键盘快捷键」变成**有 WCAG 逐字条文、有 W3C 规范性因果链、有精确数值、能静态验收的输入契约**。本文件不替代 `accessibility.md`（WCAG 全档阈值与焦点三件套）、`component-api-design.md §12`（APG 复合组件键盘契约与 roving tabindex）、`motion-orchestration.md`（FLIP / 列表让位动画的工程实现）、`visual-hierarchy-gestalt.md §13`（Fitts 三形式）、`navigation-ia.md`（导航与 IA）、`feedback-states.md`（反馈层级与撤销提示），而是补上它们都在**假设**、却没人贯通的一层：**从「用户按下指针」到「操作可撤销」之间，浏览器接管了什么、规范强制了什么、以及不用拖动的人怎么完成同一件事**。

**一句话立场**：直接操纵不是「把对象跟着指针走」这一个动作，而是**四条并存且互不替代的完成路径**——单指针无拖动、指针取消、键盘、读屏播报。只做视觉上的拖动反馈，等于把交互做成了只有精细运动能力者能用的单点通道；W3C 用 `2.5.1 / 2.5.2 / 2.5.7` 三条**不同**的准则分别堵住这三条退路。

**本轮三条最重要裁决**（后文逐条给官方原文、数值与验收动作）：

1. **「补个键盘快捷键」不满足 SC 2.5.7，也不满足 SC 2.5.1**。W3C SC 2.5.7 Dragging Movements（AA）逐字：*"All functionality that uses a dragging movement for operation can be achieved by a single pointer without dragging, unless dragging is essential or the functionality is determined by the user agent and not modified by the author."* —— 要求的是**单指针、无拖动**，键盘不是「单指针」。SC 2.5.1 的 Intent 更明确：*"keyboard operability is not sufficient to conform to this success criterion."*，理由逐字 *"some users rely entirely on pointing devices"*（如头戴指针、eye-gaze、speech-controlled mouse emulator）。唯一列出的充分技术是 **G219**（箭头逐步移动 / 数字输入框 / 「移动到…」下拉菜单 / 点击径向控件另一位置），不是 `Space`+方向键。并且 SC 2.5.1 明确加了一句 WCAG 2.2 新增的交叉引用：*"the single pointer non-path-based alternative can't exclusively rely on a dragging movement, as this would fail the requirements of 2.5.7"* —— **两条准则互为约束，不能靠「另一种拖法」互相糊弄**。
2. **`pointercancel` 不是异常分支，是 W3C 规范性必达事件**。W3C Pointer Events Level 3 逐字：*"The user agent MUST suppress a pointer event stream when it detects that the web page is unlikely to continue to receive pointer events with a specific pointerId."*，抑制步骤第一步逐字 *"Fire a pointercancel event."*，随后 `pointerout` / `pointerleave` / `Implicitly release the pointer capture`；同一规范另一条：*"Viewport manipulations (panning and zooming) ... are intentionally NOT a default action of pointer events, meaning that these behaviors ... cannot be suppressed by canceling a pointer event. Authors must instead use `touch-action`..."*。**浏览器把手指判成滚动时，你的 `pointermove` 链必然断；没有 `pointercancel` 回滚逻辑的拖拽实现是确定性缺陷，不是偶发 bug**。MDN 同一口径：*"An application using Pointer events will receive a pointercancel event when the browser starts handling a touch gesture."*
3. **目标尺寸是三套不同口径，不能拿一个数字当全局规范**。W3C SC 2.5.8（AA）**合规下限**逐字 *"at least 24 by 24 CSS pixels"*，未达标时可用 *"a 24 CSS pixel diameter circle is centered on the bounding box of each, the circles do not intersect another target or the circle for another undersized target"* 的 **Spacing 例外**；W3C SC 2.5.5（AAA）是 *"at least 44 by 44 CSS pixels"*；Material 2 逐字 *"For most platforms, consider making touch targets at least 48 x 48 dp. A touch target of this size results in a physical size of about 9mm, regardless of screen size. The recommended target size for touchscreen elements is 7-10mm."* + *"Note that on iOS, 44 x 44 pt is the recommended touch target."* + *"Consider making pointer targets at least 44 x 44 dp."* + *"Android target sizes are 48 x 48 dp."* + *"In most cases, touch targets separated by 8dp of space or more"*。**24 是 AA 法条、44 是 AAA / iOS / 指针目标、48 是平台设计值；把 24 当「推荐点击区」或把 48 当「WCAG 要求」都是口径错置**。

**边界声明**：本文件管「指针 / 手势 / 拖放的完成路径、取消链、事件契约、目标尺寸三口径、读屏播报」的机制与验收；WCAG 全档阈值与焦点可见归 `accessibility.md`；复合组件通用键盘契约、roving `tabindex`、单 tab stop 归 `component-api-design.md §12`；列表重排 FLIP 与动画编排归 `motion-orchestration.md`；Fitts 定律三形式与 drop zone 距离论证归 `visual-hierarchy-gestalt.md §13`；hover / focus 态与 `:focus-visible` 归 `accessibility.md` / `form-table.md`；滚动容器与 `overscroll-behavior` 归 `responsive-layout.md`。**本文件不生产新的「拖多久算长按」魔法数**——NN/g 只给了 *"a timing delay of a few milliseconds"* 这一模糊措辞，本文件如实登记为「未量化」，不臆造 500ms 之类的常数。

---

## 1 · 为什么单列「直接操纵与指针交互」

40 份参考里，「拖拽 / 手势 / 指针 / 拖放」没有独立资产。缺口用 `dp_search.py` 与全域词频统计判定为**结构性空白**，不是覆盖不足。

**缺口实测**（本轮 `python scripts/dp_search.py "拖拽 手势 指针交互"` / `"drag and drop pointer capture touch-action"` + `grep -ril` 全域统计）：`拖拽` 只在 7 个文件里零星出现（多为「拖动滚动条」「上传拖拽区」的名词），`手势` 2 处，`Drag and drop` / `Pointer Events` / `setPointerCapture` / `dnd-kit` / `react-dnd` / `SortableJS` / `pragmatic-drag-and-drop` **几乎零命中**；`dp_search.py "拖拽 手势 指针交互"` 返回的首位是 `performance-design.md`、`design-system-docs.md`、`ai-design-toolchain.md` —— 检索器已经在用「最不相关的高频词」凑答案，这是典型的结构性空白信号。`accessibility.md` 确实在 §2 阈值表里列了 `2.5.7 / 2.5.8` 两行、§6.1 给了 24×24 判定、§7 写了「拖动必须有替代」，但那是**合规清单**，不回答：浏览器的 `pointercancel` 什么时候必然触发、`dragover` 为何必须 `preventDefault()`、键盘拖起的默认步长是多少、读屏该播报 index 还是 position、原生 HTML DnD 为什么在触屏上不成立。

**上游文件都在「用」这些结论**：`motion-orchestration.md` 讲列表让位动画却不给拖拽状态机；`component-api-design.md §12` 讲 APG 键盘契约却不给拖放的 `Space` 拿起 / 方向键移动 / `Escape` 取消；`form-table.md` 讲滑块和批量操作却不给 down-event / up-event 的取消要求；`responsive-layout.md` 提过一句「不要全站滥用 `touch-action: manipulation`」却没解释它和 `pointercancel` 的因果链。缺了这一层，「拖拽好用一点」就永远是没有理由的口诀。

**与相邻支柱的对照**：`visual-hierarchy-gestalt.md` 回答「目光先看哪」，`content-findability.md` 回答「能不能找到」，本文件回答「**找到之后，用户能不能用自己那套输入设备把它挪过去，并在中途反悔**」。这是认知链路的下游、也是交互链路的执行端。

---

## 2 · 四段链路模型：先判哪一段断，再谈改动画

任何「拖不动 / 拖到一半飞了 / 手机上不生效 / 读屏用户完全用不了 / 放错位置回不来」的问题，先判落在哪一段。

| 段 | 回答的问题 | 机制 | 典型失效 | 主武器 | 本文件 |
|---|---|---|---|---|---|
| **P1 抓得起** | 用户看得出能抓、抓了会怎样？ | signifier 双义、hover cursor、grab 反馈、目标尺寸 | 手柄图标像汉堡菜单、触屏无 hover、热区只有 16px | NN/g 两类 signifier + 2.5.8 / 2.5.5 三口径 | §8 §15 §16 |
| **P2 跟得住** | 指针离开元素 / 浏览器接管后还能跟吗？ | `setPointerCapture`、implicit capture、`touch-action`、`pointercancel` | 只用 `mousemove`、把 `pointercancel` 当异常、全站 `touch-action: none` | PE3 规范性链条 + MDN 事件表 | §9 §10 §11 |
| **P3 放得下** | 落点看得见、放错了能撤销吗？ | drop 指示、磁吸、SC 2.5.2 / G210 取消与撤销 | 只有幽灵图无落点预览、`pointerdown` 就提交、没有 Undo | G210 三种取消路径 + 2.5.8 例外 | §6 §15 §17 |
| **P4 换得了** | 不用拖动 / 用键盘 / 用读屏能完成同一件事吗？ | SC 2.5.1 / 2.5.7 / 2.1.1、G215 / G219、live region | 只补一个 `Space` 快捷键、播报「index 0 → index 1」 | 四类无拖动替代 + dnd-kit 契约 + 播报模板 | §3 §4 §13 §14 §19 |

**判段口诀**：先问「有没有非拖动的单指针路径」（P4，法条优先级最高）→ 再问「浏览器会不会把这次触摸判成滚动」（P2）→ 再问「按下就提交还是抬起才提交」（P3）→ 最后才问「手柄画得好不好看」（P1）。**把 P4 的合规缺口用 P1 的视觉打磨去补，是本主题最高频的返工来源**。

---

## 3 · 裁决一：SC 2.5.7 要的是「单指针无拖动」，不是「键盘也能拖」

W3C《Understanding SC 2.5.7 Dragging Movements》（Level AA）逐字：

> *"All functionality that uses a dragging movement for operation can be achieved by a single pointer without dragging, unless dragging is essential or the functionality is determined by the user agent and not modified by the author."*

**`dragging movement` 的 Key Terms 定义**（逐字）：*"an operation where the pointer engages with an element on the down-event and the element (or a representation of its position) follows the pointer until an up-event"*，Note 举例 *"Examples of draggable elements include list items, text elements, and images."* —— **看的是「元素是否跟随指针」，不是你代码里有没有叫 drag 的函数**；滑块、看板卡片、画布图形、径向控件全在范围内。

**`single pointer` 的 Key Terms 定义**（逐字）：*"an input modality that only targets a single point on the page/screen at a time – such as a mouse, single finger on a touch screen, or stylus."* Note 补充 *"Single pointer interactions include clicks, double clicks, taps, dragging motions, and single-finger swipe gestures."* —— **键盘不在此列**。

**SC 2.5.1 的交叉封堵**：W3C《Understanding SC 2.5.1 Pointer Gestures》（Level A）Intent 逐字 *"While content authors generally need to provide keyboard operability as alternative for pointer operation ... keyboard operability is not sufficient to conform to this success criterion. That is because some users rely entirely on pointing devices"*，并给出具体人群 *"a head pointer, eye-gaze system, or speech-controlled mouse emulator"*。WCAG 2.2 新增的一句把两条准则扣死：*"the single pointer non-path-based alternative can't exclusively rely on a dragging movement, as this would fail the requirements of 2.5.7 Dragging Movements."*

**正式例外只有两类**（逐字）：*"unless dragging is essential or the functionality is determined by the user agent and not modified by the author."* `essential` 的 Key Terms 是双条件 **and**：*"if removed, would fundamentally change the information or functionality of the content, and information and functionality cannot be achieved in another way that would conform"*。Intent 明确**不适用**的是 UA 提供的滚动：*"This criterion does not apply to scrolling and dragging gestures enabled by the user agent, as it's the user agent's responsibility to provide an accessibility-supported mechanism for these."*，连 CSS `overflow` 也排除：*"This criterion also does not apply to the use of techniques such as CSS `overflow` that make a section of content scrollable"*。**但反向边界要记牢**：*"The criterion does apply if content actively suppresses the user agent's own scrolling functionality and/or implements its own scrolling mechanism"* —— 自定义滚动容器 / 自写轮播拖拽，仍受 2.5.7 约束。

**Sufficient Techniques 只有一项**：`- G219: Ensuring that an alternative is available for dragging movements that operate on content`（页面并注明 *"There may be other ways of meeting the criterion not covered by these techniques."*）。**验收动作**：列出所有「元素跟随指针」的功能 → 逐个找到**一次或多次单指针激活即可完成、且全程不拖动**的路径 → 若答案只有「键盘 Space+方向键」，判不合格 → 用 §25.3 静态扫描器扫。

---

## 4 · G219 的四类无拖动替代与两步验收

W3C Technique G219（Sufficient for 2.5.7）逐字描述目标：*"ensure that people with motor impairments who cannot carry out dragging movements are presented with an alternative single pointer interaction that does not involve dragging."*，实现口径 *"by one or several single pointer activations that don't require dragging"*，并点名 *"a single tap or click can reveal controls (arrows) to move a target in a stepwise fashion, or a drop-down menu can allow users to select the drop position"*。

**官方 Examples 逐条转写**（四类可直接抄的形态）：

| 形态 | G219 原文例 | 适用 | 交互成本 |
|---|---|---|---|
| **逐步箭头** | 单击后每项显示 up/down 箭头，*`"step-wise re-ordering of the list via single pointer inputs (taps or clicks at the up or down arrow)"`* | 列表排序、优先级调整 | O(位移次数) 次点击，但每次都是单击 |
| **数字位置输入** | 优先级列表左侧文本框显示当前位置，*`"users can put in another number. This leads to a dynamic reordering and renumbering"`* | 长列表跨距离移动 | 1 次输入 + 1 次确认，长距离最优 |
| **「移动到…」下拉** | 看板泳道，*`"A single pointer activation of a drop-down menu labelled 'Move selected items to' offers a selection of drop targets (other lanes)"`* | 跨容器归类、状态流转 | 2–3 次单击 |
| **点击目标位置** | 径向控件，*`"Users can also click or tap on another position of the radial control to change the value"`* | 滑块、色环、刻度盘 | 1 次单击，最省 |

**G219 的 Tests 两步**（逐字 Procedure）：*"1. Check the interface for the presence of functions triggered by dragging movements. 2. Check that there is a single pointer activation alternative that does not require dragging to operate the same function"*，Expected Results：*"Check #2 is true."*。同时页面自述 *"Techniques are examples of ways to meet WCAG ... They are not required to meet WCAG."* —— **G219 是充分技术不是唯一解，但它给了最可静态验收的判据**。

**与 2.5.1 的 G215 配套**：SC 2.5.1 的充分技术是 `G215: Providing controls to achieve the same result as path based or multipoint gestures` 与 `G216: Providing single point activation for a control slider`；失败例 `F105`。若你的组件同时含「滑动手势」与「拖动」，**两条准则要各交一份替代**：G215/G216 处理路径手势，G219 处理拖动；别用一个「键盘模式」同时申报两条。

**高频误判**：`Escape` 取消、Undo 按钮、确认对话框解决的是 **2.5.2 / G210（取消）**，**不解决 2.5.7（必须存在无拖动完成路径）**。把「拖错了能撤销」当成「不用拖也能做」，是本主题最容易被审计打回的一处。

---

## 5 · 裁决二：路径手势、拖动、指针取消是三条不同的准则

三者常被混成一句「手势要可访问」，但 W3C 分了三条不同级别、不同判据的准则。

| 准则 | 级别 | 逐字核心 | 触发条件 | 充分技术 | 失败例 |
|---|---|---|---|---|---|
| **2.5.1 Pointer Gestures** | A | *"All functionality that uses multipoint or path-based gestures ... can be operated with a single pointer without a path-based gesture, unless ... essential"* | 多点（双指捏合）/ 路径（直线 flick、画特定形状） | G215 / G216 | F105 |
| **2.5.7 Dragging Movements** | AA | *"can be achieved by a single pointer without dragging"* | 元素或位置表征跟随指针 | G219 | — |
| **2.5.2 Pointer Cancellation** | A | *"at least one of ... No Down-Event / Abort or Undo / Up Reversal / Essential"* | 单指针可操作的一切功能 | G210 / G212 | — |
| **2.5.3 Label in Name** | A | *"the name contains the text that is presented visually"* | 带可见文本标签的组件 | — | — |
| **2.5.4 Motion Actuation** | A | *"can also be operated by user interface components and responding to the motion can be disabled to prevent accidental actuation"* | 摇一摇 / 倾斜设备 | G213 | — |
| **2.5.8 / 2.5.5 Target Size** | AA / AAA | `24×24` / `44×44` CSS px | 所有指针目标 | — | — |

**SC 2.5.1 的「路径 vs 拖动」官方判例**（本文件最有用的一段）：W3C 逐字 *"In a path-based gesture, what matters is how the pointer moves: its path or direction (and sometimes its speed)"*，而 *"Dragging movements, on the other hand, generally involve 'picking up' or 'grabbing' an object ... and moving it to some other position."*，图注一句最干脆：*"With a dragging gesture only the start- and end-point matter."*

**滑块的三态裁决**（W3C 逐字，工程上极易写错）：绝大多数滑块使用 *"pointer capture"*，抓住 thumb 后可以 *"drift from the horizontal or vertical track"*，因此 **只算 dragging movement，不算 path-based gesture**；但如果实现成 *"straying from the track 'loses' the user's grip on the slider thumb"*，W3C 明确判 *"it is considered to be both a dragging movement and a path-based gesture at the same time"*，并可能同时不满足 2.5.1 与 2.5.7。**结论：滑块必须做 pointer capture，别做「必须贴着轨道走」的判定**。轮播同理：*"these only count as requiring a path-based gesture if they expect the user to perform a precise movement along a path"*。

**2.5.3 对拖拽手柄的具体约束**：SC 2.5.3 逐字 *"For user interface components with labels that include text or images of text, the name contains the text that is presented visually"*；In Brief：*"The visual label for controls is a trigger for speech activation."* / *"People who operate with voice interaction use the visible labels in their commands."* —— **手柄可见文字写「排序」，可访问名就不能只写「drag handle 3」**；语音控制用户念的是看得见的字。Note 澄清 *"The term label is not limited to the label element in HTML."*

**2.5.4 的两个例外**（逐字）：`"Supported Interface"` / `"Essential"`；充分技术 `G213: Provide conventional controls and an application setting for motion activated input`（页面第二项写作 `GXXX`，本文件不把它当正式编号引用）。摇晃撤销、倾斜滚动这类设计必须同时给常规控件和「关闭动作感应」开关。

---

## 6 · SC 2.5.2 与 G210：取消是硬要求，撤销不是可选项

W3C《Understanding SC 2.5.2 Pointer Cancellation》（Level A）逐字四选一：

> *"For functionality that can be operated using a single pointer, at least one of the following is true:"* — `No Down-Event`（*"The down-event of the pointer is not used to execute any part of the function"*）/ `Abort or Undo`（*"Completion of the function is on the up-event, and a mechanism is available to abort the function before completion or to undo the function after completion"*）/ `Up Reversal`（*"The up-event reverses any outcome of the preceding down-event"*）/ `Essential`（*"Completing the function on the down-event is essential"*）。

**官方最推荐的落点**（逐字）：*"The most accessible way to incorporate pointer cancellation is to make activation occur on the up-event."*；*"Authors can reduce the problem of users inadvertently triggering an action by using generic platform activation/click events ... the `click` event in JavaScript triggers on release of the primary mouse button, and is an example of an implicit up-event. Despite its name, the `click` event is device-independent and also works for touch and keyboard interaction."* —— **直接用 `click` 就白拿一条合规路径，别在 `pointerdown` 里提交业务动作**。

**复杂交互的加码**（逐字）：*"For more complex interactions, such as drag and drop, the down- and up-events may initiate and end a series of actions to complete a process. In such a complex action, the need for an Abort or Undo function increases."* W3C 给的两种落法：*"Designers may elect to confirm the move through something like a confirmation dialog or an undo button"*；或 *"the user returns the selected item to its original location and concludes the process there ... If other parts of the screen disallow a move, the user can conclude the drag and drop there, effectively nullifying the operation."*

**G210 的三种取消路径**（逐字）：*"This can be done either by releasing the item outside a drop area, or by moving the item back to its original position in a separate action that undoes the first action. A third option is to have a step after the element is dropped onto target, either with a dialog asking for confirmation of the action when the item is dropped, or providing an undo command."*

**G210 的 AT 支持警告**（逐字，值得单独记）：*"On touchscreen devices, author-supplied path-based and multipoint gestures usually do not work when OS level assistive technologies (AT) like a built-in screen reader is turned on. AT generally consumes path-based or multipoint gestures so they would not reach the authored content."* —— **读屏开启时，你精心做的自定义手势可能根本收不到事件**；这也是 §19 里「读屏路径必须是独立控件、不是同一套手势」的规范依据。

**`Essential` 的边界**：*"Completing the function on the down-event is only permitted when it is essential that the up-event not be used."*，官方例子是软件键盘（*"Functions that emulate a keyboard or numeric keypad key press are considered essential"*）、屏幕钢琴、飞碟射击；**拖拽排序不在这个名单里**，不能拿 `essential` 开脱。

---

## 7 · 拖放的完整状态机：从 down-event 到可撤销

把 §3–§6 的条文落到同一套状态机，避免「合规条款各自看过、代码里还是 `pointerdown` 提交」。

| 状态 | 进入条件 | 必须做的事 | 对应条文 | 退出 |
|---|---|---|---|---|
| `idle` | — | signifier 可辨、热区达标、可访问名含可见文本 | 2.5.8 / 2.5.3 / §15 | `pointerdown` 或 `click` |
| `armed` | 按下但未移动（可加时序延迟区分 tap / swipe / grab） | **不提交任何业务动作**；`setPointerCapture(e.pointerId)` | 2.5.2 No Down-Event | 位移超阈值 → `dragging`；抬起 → 视为 click |
| `dragging` | 元素或其表征开始跟随指针 | 抓取反馈 + 落点预览；DOM 移动后再设 capture | §10 / §15 | `pointerup` / `pointercancel` / `Escape` |
| `over-target` | 进入有效 drop zone | 明确激活态 signifier（磁吸区可超出可见边界） | NN/g magnetism | 离开 → `dragging` |
| `committed` | 在 drop zone 抬起 | **此时才提交**；写可撤销记录 | 2.5.2 Abort or Undo / G210 | Undo / 确认框 |
| `cancelled` | `pointercancel` / `Escape` / 放回原位 / 落在非 drop 区 | 完整回滚：位置、capture、live region、视觉态 | PE3 / G210 | → `idle` |

**三条最容易漏的回滚**：① `pointercancel` 里必须同时清 `pointercapture`、清幽灵层、播报「已取消」；② `Escape` 要**对所有 sensor 生效**，dnd-kit 逐字 *"It is recommended to allow users to cancel the drag operation using the `escape` key for all sensors, not just the Keyboard sensor."*；③ 落在非 drop 区的原生行为是 *"a 'fly-back' animation displays, indicating that the drag and drop failed"*（MDN），自定义实现必须自己补这个反馈，不能静默消失。

---

## 8 · 裁决三：目标尺寸三套口径，24×24 是 AA 下限不是设计值

**W3C SC 2.5.8 Target Size (Minimum)（AA）** 逐字：

> *"The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except when:"* — `Spacing` / `Equivalent` / `Inline` / `User Agent Control` / `Essential` 五项。

Spacing 例外逐字：*"Undersized targets (those less than 24 by 24 CSS pixels) are positioned so that if a 24 CSS pixel diameter circle is centered on the bounding box of each, the circles do not intersect another target or the circle for another undersized target"*。**注意是「以每个 undersized target 的 bounding box 为圆心画直径 24 CSS px 的圆，圆与圆、圆与其他目标都不相交」**，不是「间距 ≥24px」的简化说法。

尺寸判定逐字：*"For a target to be 'at least 24 by 24 CSS pixels', it must be conceptually possible to draw a solid 24 by 24 CSS pixel square, aligned to the horizontal and vertical axis such that the square is completely within the target"*；圆角目标可能因 *"The rounded corners do not leave sufficient space to draw a 24 by 24px square"* 被判 undersized。**独立于缩放**逐字：*"The requirement is independent of the zoom factor of the page; when users zoom in, the CSS pixel size of elements does not change ... authors cannot meet it by claiming that the target will have enough spacing or sufficient size if the user zooms into the page."*

**W3C SC 2.5.5 Target Size (Enhanced)（AAA）** 逐字：*"The size of the target for pointer inputs is at least 44 by 44 CSS pixels except when:"* — `Equivalent` / `Inline` / `User Agent Control` / `Essential` 四项（**没有 Spacing 例外**）。

**Material 2（官方逐字，注意是 M2 不是 M3）**：

> *"For most platforms, consider making touch targets at least 48 x 48 dp. A touch target of this size results in a physical size of about 9mm, regardless of screen size. The recommended target size for touchscreen elements is 7-10mm."*
> *"Note that on iOS, 44 x 44 pt is the recommended touch target."*
> *"Pointer targets are similar to touch targets, but apply to the use of motion-tracking pointer devices such as a mouse or a stylus. Consider making pointer targets at least 44 x 44 dp."*
> *"Android target sizes are 48 x 48 dp."*
> *"In most cases, touch targets separated by 8dp of space or more promote balanced information density and usability."*
> *"For example, an icon may appear to be 24 x 24 dp, but the padding surrounding it comprises the full 48 x 48 dp touch target."*

**三套口径对照表**（工程取值，不是新规范）：

| 场景 | 取值 | 来源与级别 | 说明 |
|---|---|---|---|
| 合规下限（桌面图标按钮） | `24 × 24 CSS px` + 间距圆例外 | W3C 2.5.8 **AA** | 法条，不是设计推荐值 |
| 更高合规 | `44 × 44 CSS px` | W3C 2.5.5 **AAA** | 无 Spacing 例外 |
| iOS 触屏 | `44 × 44 pt` | Material 2 转述（**Apple HIG 本轮未逐字核验**） | 平台单位 pt ≠ CSS px |
| Android / 通用触屏 | `48 × 48 dp` ≈ `9mm`（推荐 `7–10mm`） | Material 2 | 视觉 24dp + padding 撑满 48dp |
| 鼠标 / 触控笔指针目标 | `44 × 44 dp` | Material 2 | 与触屏分列 |
| 目标间距 | `8dp` 及以上 | Material 2 | 与 2.5.8 的 24px 圆是**两套不同判据**，别相加 |

**裁决**：**拿 24 当「点击区推荐尺寸」是拿法条当设计值，拿 48 当「WCAG 要求」是拿设计值当法条**。写设计规格时两行并列：`合规下限 24×24 CSS px（2.5.8 AA，含 spacing 例外）` / `实现目标 48×48 dp（Material 2；图标视觉 24dp + padding）`。`accessibility.md §6.1` 已有 24/44/60 三档判定表，本文件只补「为什么 48 不属于 WCAG」与「8dp 间距与 24px 圆不可混用」。

---

## 9 · W3C Pointer Events Level 3 的规范性因果链：pointercancel 什么时候必然触发

**`touch-action` 为什么不能用 `preventDefault()` 代替**（PE3 §4.1.3.1 逐字）：

> *"Viewport manipulations (panning and zooming) — generally, as a result of a direct manipulation interaction — are intentionally NOT a default action of pointer events, meaning that these behaviors (e.g. panning a page as a result of moving a finger on a touchscreen) cannot be suppressed by canceling a pointer event. Authors must instead use `touch-action` to explicitly declare the direct manipulation behavior for a region of the document. Removing this dependency on the cancelation of events facilitates performance optimizations by the user agent."*

（原文此处 `must` 是小写，不是 RFC 2119 全大写关键词；PE3 §2 明确 *"when, and only when, they appear in all capitals"*。本文件照录，不把小写 must 冒充规范性 MUST。）

**`pointercancel` 的规范性来源**（PE3，三段连起来才是完整链条）：

> *"The user agent MUST suppress a pointer event stream when it detects that the web page is unlikely to continue to receive pointer events with a specific pointerId."*
> 场景之一：*"The pointer is subsequently used by the user agent to manipulate the page viewport (e.g. panning or zooming). See the section on `touch-action` CSS property for details."*
> *"The user agent MUST run the following steps to suppress a pointer event stream:"* → *"Fire a pointercancel event."* → *"Fire a pointerout event."* → *"Fire a pointerleave event."* → *"Implicitly release the pointer capture if the pointer is currently captured."*
> *"The user agent MUST fire a pointer event named pointercancel when it detects a scenario to suppress a pointer event stream."*
> *"The `coalescedEvents` and `predictedEvents` lists in the pointercancel event MUST be empty, and the event's cancelable attribute MUST be false."*

**`setPointerCapture()` 的规范性定义**（PE3 §5 逐字）：

> *"Set pointer capture for the pointer identified by the argument pointerId to the element on which this method is invoked. For subsequent events of the pointer, the capturing target will substitute the normal hit testing result as if the pointer is always over the capturing target, and they MUST always be targeted at this element until capture is released."*
> *"The pointer MUST be in its active buttons state for this method to be effective, otherwise it fails silently."*
> *"When the provided method's argument does not match any of the active pointers, throw a 'NotFoundError' DOMException."*

**隐式捕获**（PE3 §4.1.3 逐字，措辞是 `direct manipulation device` 不是「touch」）：*"If the event is pointerdown, the associated device is a direct manipulation device, and the target is an Element, then set pointer capture for this pointerId to the target element as described in implicit pointer capture."*；引言把触屏 pan/zoom 归入同一概念：*"An additional key goal is to enable multi-threaded user agents to handle direct manipulation actions for panning and zooming (for instance, with a finger or stylus on a touchscreen), without blocking on script execution."*

**取源纠偏（不臆造）**：PE3 逐字只说 *"This revision of Pointer Events supersedes [PointerEvents2]."*，**没有**「supersedes Touch Events」这句话；关于 Touch Events 只有一条非规范性 Note：*"This specification does not provide any advice on the expected behavior of user agents that support both Touch Events ... and Pointer Events."* 而 PE3 §2 明确 *"all authoring guidelines, diagrams, examples, and notes in this specification are non-normative"*。**不要写「Pointer Events Level 3 已取代 Touch Events」**。

---

## 10 · MDN PointerEvent 工程契约：设备、事件、捕获、取消

MDN《Pointer events》逐字定义：*"Pointer events are DOM events that are fired for a pointing device. They are designed to create a single DOM event model to handle pointing input devices such as a mouse, pen/stylus or touch (such as one or more fingers)."*；*`PointerEvent` interface inherits all of the `MouseEvent` properties, thus facilitating the migration of content from mouse events to pointer events.*；事件语义：*"The pointerdown, pointerup, pointermove, pointerover, pointerout, pointerenter, and pointerleave events have similar semantics to their mouse event counterparts, but work with other pointing devices as well, such as pens and touchscreens."*

**设备判别**：`pointerType` 逐字 *"Indicates the device type that caused the event (mouse, pen, touch, etc.)."*；`isPrimary` 表示该 pointer 是否为该 pointerType 的 primary pointer，规则：mouse 只有一个 pointer 故始终 primary；touch 在「没有其他 active touches」时 primary；pen 在「初次接触且无其他 active pens」时 primary。其余 `PointerEvent` 扩展属性：`pointerId` / `width` / `height` / `pressure` / `tangentialPressure` / `tiltX` / `tiltY` / `twist` / `altitudeAngle` / `azimuthAngle` / `persistentDeviceId`。

**事件表**（MDN 逐条口径，含拖拽实现最常漏的三个）：

| 事件 | 含义 | 拖拽实现要点 |
|---|---|---|
| `pointerdown` | 进入 *active buttons state*（`buttons` 非零） | 只 armed，不提交；此后设 capture |
| `pointermove` | 坐标变化或状态变化 | 主体逻辑；可能被随时截断 |
| `pointerup` | 不再是 active buttons state | 此时才 commit；capture 隐式释放 |
| `pointercancel` | 浏览器判定不再产生事件 | **一等公民**，必须完整回滚 |
| `gotpointercapture` / `lostpointercapture` | 捕获获得 / 释放 | 用来同步幽灵层与视觉态 |
| `pointerover` / `pointerenter` / `pointerout` / `pointerleave` | 边界事件 | **捕获期间不触发**，别用它们判 hover 态 |
| `pointerrawupdate` | 不改变 down/up 的属性变化 | 高频，慎用 |

MDN 逐字：*"A browser fires this event if it concludes the pointer will no longer be able to generate events (for example, if the related device is deactivated, or the browser decided to interpret the interaction as a pan/zoom instead)."*；捕获期 *"pointerover, pointerenter, pointerleave, pointerout will not fire"*；释放方式 *"manually ... or implicitly after pointerup / pointercancel"*；**DOM 移动顺序**：*"If you need to move an element in the DOM, make sure to call setPointerCapture() after DOM movements ... so it does not lose track"*（`Element.append()` 之后才设捕获）。

`hasPointerCapture()` 判定某元素是否持有给定 `pointerId` 的捕获；`setPointerCapture()` 逐字 *"Designates a specific element as the capture target of future pointer events."*；`releasePointerCapture()` 逐字 *"Releases (stops) pointer capture that was previously set for a specific pointer event."*

**兼容鼠标事件的边界**（MDN）：浏览器 *may map generic pointer input to mouse events*（compatibility mouse events），*"Mouse events can only be prevented when the pointer is down"*，`mouseover/out/enter/leave` 永不因 `pointerdown` 被阻止；`click` / `auxclick` / `contextmenu` 是 higher-level actions，键盘也能触发。**别在 `pointerdown` 里 `preventDefault()` 指望干掉 click**。

---

## 11 · `touch-action` 全值表、形式语法与三条工程陷阱

MDN《touch-action》正式语法（逐字）：

```css
touch-action = 
  auto                                                |
  none                                                |
  [ [ pan-x | pan-left | pan-right ] || [ pan-y | pan-up | pan-down ] || pinch-zoom ]  |
  manipulation
```

| 值 | MDN 逐字含义 | 拖拽场景用法 |
|---|---|---|
| `auto` | *"Enable browser handling of all panning and zooming gestures."* | 默认值；页面主体 |
| `none` | *"Disable browser handling of all panning and zooming gestures."* | **仅限**自定义拖拽/画布/地图表面，且必须局部 |
| `pan-x` | *"Enable single-finger horizontal panning gestures."* | 横向轮播：让浏览器管横滑、自己管其他 |
| `pan-y` | *"Enable single-finger vertical panning gestures."* | 纵向列表内嵌可拖项：保留页面滚动 |
| `pan-left/right/up/down` | 起始方向受限；*"Once scrolling has started, the direction may still be reversed"* | 组合约束；`"pan-left pan-right"` 非法（有更简单的 `pan-x`） |
| `pinch-zoom` | *"Enable multi-finger panning and zooming of the page."* | 与 `pan-*` 组合，保留缩放 |
| `manipulation` | *"Enable panning and pinch zoom gestures, but disable additional non-standard gestures such as double-tap to zoom ... This is an alias for 'pan-x pan-y pinch-zoom'"* | 去掉双击缩放延迟；**不等于 `none`** |

**三条工程陷阱**（全部有官方原文）：

1. **手势开始后改值无效**：MDN Note 逐字 *"After a gesture starts, changes to `touch-action` will not have any impact on the behavior of the current gesture."* —— 别在 `pointerdown` 里动态切 `touch-action`；要在渲染时就声明。
2. **祖先求交**：*"When a gesture is started, the browser intersects the `touch-action` values of the touched element and its ancestors, up to the one that implements the gesture (in other words, the first containing scrolling element)."* —— 子元素写 `pan-y` 救不了父级 `none`。MDN 因此说 *"touch-action is typically applied only to top-level elements which have some custom behavior"*。
3. **`none` 的可访问性代价**：MDN Accessibility 段逐字 *"A declaration of `touch-action: none;` may inhibit operating a browser's zooming capabilities. This will prevent people experiencing low vision conditions from being able to read and understand page content."*，并链接 WCAG 1.4.4 —— **全站 `touch-action: none` / `user-scalable=no` 是双重红线**（`responsive-layout.md` 已记后半句，本文件补前半句的规范出处）。

形式定义：初值 `auto`；`Inherited: no`；`Animation type: Not animatable`；应用于 *"all elements except: non-replaced inline elements, table rows, row groups, table columns, and column groups"*。MDN 页面标注 Baseline *"Widely available"*、*"available across browsers since September 2019"*。

**`pointercancel` 因果链一句话**：`touch-action` 声明谁处理手势 → 浏览器接管 viewport pan/zoom → UA *MUST* suppress pointer event stream → 第一步 *MUST* fire `pointercancel` → 同时隐式释放 capture → 你的拖拽若没监听 `pointercancel`，状态机永久停在 `dragging`。**这不是「某浏览器兼容性问题」，是规范要求的必然路径**。

---

## 12 · HTML Drag and Drop API：七事件、DataTransfer 与 drop target 规则

MDN《HTML Drag and Drop API》逐字：*"The user may select draggable elements with a mouse, drag those elements to a droppable element, and drop them by releasing the mouse button. A translucent representation of the draggable elements follows the pointer during the drag operation."* —— **定义里写的是 mouse**；本轮搜索到的「移动端原生 DnD 不可用」说法全为中文教程 / 博客级二手资料，**不作为规范引用**，只登记为取源限制（§26）。但 MDN 对「三种用例」的划分本身足够据此做工程判断：

> *"Drag and Drop actually has three distinct use cases: dragging elements within a page, dragging data out of a page, and dragging data into a page. They have subtly different requirements and implementations."*

**七事件表**（MDN 逐条）：

| 事件 | 触发 | 触发在谁身上 |
|---|---|---|
| `dragstart` | 可拖项开始被拖 | 被拖项 |
| `drag` | 正在拖（反复触发） | 被拖项 |
| `dragenter` | 可拖项进入 | 潜在 drop target |
| `dragleave` | 可拖项离开 | 潜在 drop target |
| `dragover` | 悬停在上方（反复触发） | 潜在 drop target |
| `drop` | 在 drop target 上放下 | drop target |
| `dragend` | 拖动结束 | 被拖项 |

MDN Note：*"The `dragstart`, `drag`, and `dragend` events are fired on the dragged item, and therefore can't fire when dragging a file into the browser from the OS."*；另一半 *"the `dragenter`, `dragleave`, `dragover`, and `drop` events are fired on elements that are potential drop targets, and therefore can't fire when dragging an item out of the browser."*

**drop target 规则（最高频 bug）** 逐字：*"By default, most elements are not drop targets, and if you release the drag, a 'fly-back' animation displays, indicating that the drag and drop failed. Any element can become a drop target by canceling the `dragover` event that fires on it with `preventDefault()`."*；*"The `drop` event only fires on drop targets, and it is the only time you can read the drag data store."*

**`DataTransfer` 的读写窗口** 逐字：*"Each drag and drop operation has an associated drag data store, which is a `DataTransfer` object accessible via the `DragEvent`'s `dataTransfer` property ... The only time to make any modifications to the data store is within the `dragstart` handler—for the `dataTransfer` of any other drag event, the data store is unmodifiable."*；*"the only time you can read from the data store, apart from the `dragstart` event, is during the `drop` event ... For all other events, the data store cannot be accessed."* 序列化约束：*"You can't transfer JavaScript objects directly to arbitrary webpages ... the data must be serialized to a string (or as a File)"*，封装为 `DataTransferItem`，带 `type`（MIME 如 `text/html`）。

**`draggable` 属性破坏选文本** 逐字：*"When an element is made draggable, text or other elements within it can no longer be selected in the normal way by clicking and dragging with the mouse. Instead, the user must hold down the `Alt` key to select text with the mouse, or use the keyboard."*；*"In HTML, images, links, and selections are draggable by default"*，非默认元素才需要 `draggable="true"`。**把整行卡片设 `draggable` 会让用户无法选中卡片中的编号/文案**——把手柄单独设 `draggable` 是常见解法。

**选型裁决**：原生 HTML DnD 适合「页内拖动 + 与 OS/外部应用交换文件/数据」；需要精确落点、触控笔/触屏一致行为、自定义幽灵层、自动滚动、`pointercancel` 语义时，用 Pointer Events 自建或成熟库（§20）。两者不要在同一容器里混绑，事件模型不同（DragEvent 继承 MouseEvent，不产生 `pointercancel`）。

---

## 13 · 键盘拖放契约：dnd-kit 的逐字键盘参数

W3C APG 的通用键盘原则先立地基（《ARIA Authoring Practices Guide — Keyboard Interface》本轮逐字核验）：*"The visual focus indicator must always be visible."*；*"It is essential that there is always a component within the user interface that is active (document.activeElement is not null or is not the body element) and that the active element has a visual focus indicator."*；*"For a web page to be accessible, all interactive elements must be operable via the keyboard."*；**关键一句**：*"Do not use keyboard shortcuts as a substitute for access via navigation."*；*"The tab sequence should include only one focusable element of a composite UI component."*；正 `tabindex` 逐字 *"Authors are strongly advised NOT to use these values."*（1–32767）；`aria-activedescendant` 路线要求 *"draw a visual focus indicator on the active element and ensure the active element is scrolled into view"*。APG 当前页**没有** `accesskey` / 单字符快捷键 / 拖放专门段落（页面还含 `To be written.` 标记），本文件不据此写任何「APG 反对某做法」的结论。

**dnd-kit《Accessibility》逐字契约**（`role` / `aria-roledescription` / `aria-describedby` 是 `useDraggable` 默认值）：

| 项 | 默认值 / 逐字规则 |
|---|---|
| 焦点 | activator *"must be able to receive focus"*；原生 `button` / `a` / 表单控件默认 `tabindex=0`；自定义 `div` / `li` 必须显式 `tabindex="0"`，`useDraggable` 默认就设了 |
| 拿起 | *"both the `enter` (on Windows) or `return` (on macOS) and the `space` key"*；依据 ARIA 第三规则 *"all interactive ARIA controls must be usable with the keyboard"* |
| 移动 | *"The arrow keys are used to move the draggable item in any given direction."* |
| 放下 | 再次 `enter` / `return` / `space` |
| 取消 | *"A drag operation can be cancelled using the `escape` key. It is recommended to allow users to cancel the drag operation using the `escape` key for all sensors, not just the Keyboard sensor."* |
| 默认步长 | *"By default, the Keyboard sensor moves in any given direction by `25` pixels when the arrow keys are pressed while dragging."*，并自述 *"This is an arbitrary default"*，建议用 `getNextCoordinates` 定制（`useSortable` 已用其定位下一个可排序元素） |
| `role` | `"button"`；*"If possible, we recommend you use a semantic `<button>` element"* |
| `aria-roledescription` | `"draggable"`；*"we recommend you customize this value to something that is tailored to your use-case"* |
| `aria-describedby` | `"DndContext-[uniqueId]"`，指向离屏指令元素 |
| 默认传感器 | Keyboard sensor 是 `<DndContext>` **两个默认启用传感器之一** |

**默认指令逐字**（`<DndContext>` 渲染在离屏元素里）：

> *"To pick up a draggable item, press space or enter. While dragging, use the arrow keys to move the item in any given direction. Press space or enter again to drop the item in its new position, or press escape to cancel."*

dnd-kit 逐字提醒：*"We recommend you customize and localize these instructions to your application and use-case"*；*"The `<DndContext>` component only ships with instructions in English due to bundle size concerns."* —— **中文产品必须自己给 `screenReaderInstructions`**，见 §14。

**别忘裁决一的边界**：这套键盘契约满足的是 **2.1.1 Keyboard** 与读屏可达，**不能拿来申报 2.5.7**。用 dnd-kit 也要另外做 G219 的单指针无拖动路径（§4）。

---

## 14 · 读屏指令、live region 播报与中文 announcements

dnd-kit 的三问框架（逐字）：*"1. Identity: What element is the user interacting with? 2. Operation: How can the user interact with the element? 3. State: What is the current state of the element?"*；三个落点：*Keyboard support* / *Screen reader instructions* / *Live regions to provide screen reader announcements*。live region 用途逐字：*"notify screen readers of content changes ... in real-time of time-sensitive information of what is currently happening with draggable and droppable elements without having to move focus."*

**默认四条 announcements（逐字，可直接作为中译母本）**：

```js
const defaultAnnouncements = {
  onDragStart({active})   { return `Picked up draggable item ${active.id}.`; },
  onDragOver({active, over}) {
    if (over) return `Draggable item ${active.id} was moved over droppable area ${over.id}.`;
    return `Draggable item ${active.id} is no longer over a droppable area.`;
  },
  onDragEnd({active, over}) {
    if (over) return `Draggable item ${active.id} was dropped over droppable area ${over.id}`;
    return `Draggable item ${active.id} was dropped.`;
  },
  onDragCancel({active}) { return `Dragging was cancelled. Draggable item ${active.id} was dropped.`; },
};
```

**position 优于 index（逐字裁决）**：*"When authoring screen reader announcements that rely on an element's position (index) in a list, use positions rather than indices to describe the element's current position."* 官方反例 *"Item with index 0 was picked up. Item was moved to index 1 of 4."*；正例 *"Item at position 1 was picked up. Item was moved to position 2 of 5."* —— **从 0 开始的下标对读屏用户是程序员黑话**。

**中文落地模板**（`screenReaderInstructions` + `announcements`，工程约定，非 dnd-kit 内置）：

```js
const screenReaderInstructions = {
  draggable: '按空格键或回车键拿起该项。拖动时用方向键移动。再按空格键或回车键放下，按 Esc 键取消。',
};
const announcements = {
  onDragStart({active}) { return `已拿起「${label(active.id)}」，当前第 ${position(active.id)} 项，共 ${count} 项。`; },
  onDragOver({active, over}) {
    return over ? `「${label(active.id)}」移动到第 ${position(over.id)} 项位置。` : `「${label(active.id)}」已离开可放置区域。`;
  },
  onDragEnd({active, over}) {
    return over ? `「${label(active.id)}」已放到第 ${position(over.id)} 项，共 ${count} 项。` : `「${label(active.id)}」已放下。`;
  },
  onDragCancel({active}) { return `已取消拖动，「${label(active.id)}」回到原位。`; },
};
```

**三条纪律**：① 播报**业务名称**而不是 DOM id（`active.id` 常是 `item-3`）；② 取消也要播报，且明确「回到原位」，不能静默；③ dnd-kit 逐字 *"If your application supports multiple languages, make sure you also translate these announcements"*，多语言站点按 locale 切换整套 announcements 与 instructions，不是只翻译指令。

**G210 的 AT 拦截提醒**（§6）在这里落地：读屏开启时自定义手势可能被 OS 层消费，所以 §19 的「读屏路径」应是**可 Tab 到的独立控件**（上移/下移按钮、位置输入框、移动到下拉），而不是「同一套拖拽 + 播报」。

---

## 15 · signifier 与两类反馈：NN/g 的可发现性裁决

NN/g《Drag-and-Drop: How to Design for Intuitive Interactions》（2020-02-23）Summary 逐字：*"Clear signifiers and clear feedback at all stages of the interaction make drag–and–drop discoverable and easy to use."*；立场不是「拖放不好」，而是 *"Drag–and–drop is not always the best choice, but when users expect it, the familiarity of the metaphor can make the interaction relatively simple and straightforward."*

**signifier 必须同时表达两件事**（逐字，本文件最想留下的一句）：

> *"Creating an obvious signifier for drag–and–drop is challenging. While a button can have a subtle drop shadow to indicate that it is raised and clickable, a drag–and–drop signifier has to signal two functions — (1) that the item is 'grabbable' and (2) what dragging it somewhere will accomplish (moving or resizing)."*

NN/g 把可抓取性的视觉 signifier 分两类：`grab-handle icons` 与 `cursor changes`。对手柄图标的判断很硬：*"icons in use for this purpose are not nearly as universal as designers may think and they are often a poor visual metaphor ... the lack of a universal convention reduces their efficacy and recognizability."*；*"Some of the handle icons ... resemble familiar icons conventionally used for other functionalities, such as a hamburger icon or the kebab icon."*；缩放手柄 *"often pretty subtle: a single vertical line between columns ... or a pair of diagonal lines in the bottom right corner."* 光标侧：*"avoid creating new, custom icons. Use the platform's standard cursor for moving or resizing."*

**两类反馈**（逐字）：*"Once the user has 'grabbed' the object ... two types of feedback are needed: (1) feedback that the object was 'grabbed', and (2) feedback previewing what will happen before the user 'drops' the object."* 列表让位动画的量化口径：*"use a quick animation (roughly 100 ms) to show them moving towards their new location"* —— **约 100ms，不是 300ms 的入场动画**；归 `motion-orchestration.md` 执行，本文件只登记数值与使用条件。

**磁吸 / snapping / haptics**（逐字）：*"One way to mitigate this challenge is by simulating a magnetic effect that snaps objects into place, even if the user hasn't yet fully acquired the target."*；但 *"To use magnetism, you need to clearly indicate to the user when the drop zone is active, by showing a visual signifier when the dragged object is within the active drop zone (especially if the droppable area extends outside the visible border)."*；移动端 *"a subtle haptic 'bump' can indicate that an object has been grabbed, and another one can indicate that an object has been dragged over a drop zone."*

**拖放本身的两类任务**（逐字）：*"All the interactions that drag–and–drop is used for can be grouped in two main types: resizing objects and moving objects. These two capabilities need different microinteraction design to succeed"* —— **移动与缩放不要共用同一套手柄与反馈**。

**不要用点击数单独判优劣**（Gmail 例，逐字）：*"Gmail on desktop (top) offers drag–and–drop ... However, on mobile (bottom), the drag-and-drop interaction has been removed and instead the functionality is available through a menu."*；*"While this solution may take a few additional steps ... the likelihood of error is lower ... so this tradeoff prioritizes overall usability, rather than simply counting clicks."*

---

## 16 · 触屏拖放的硬性前提：1cm×1cm、几毫秒、约 100ms

NN/g 对触屏的判断是本主题最强的「别做」依据。逐字：

> *"Drag–and–drop can be hard to implement on touchscreens because they lack hover states, which are often used to signal the availability of drag–and–drop."*
>
> *"Furthermore, due to the fat-finger problem, you need to ensure that draggable objects have at least 1cm x 1cm of unused space for dragging and that fingers don't cover any important feedback (such as a highlighted 'grab' state). Another important consideration is that you must distinguish among a tap, a swiping gesture (such as scrolling), and an intentional 'grab' by using a timing delay of a few milliseconds, and providing clear feedback that the object has been grabbed."*
>
> *"Since hover signifiers for drag–and–drop (such as a cursor change) are not available on touchscreens, it is recommended to use drag–and–drop only when: 1. You have clear evidence (from research such as usability testing) that your users expect drag–and–drop to be available, and 2. There is no reasonable alternative with lower interaction cost (such as cut–and–paste or a menu-driven interaction)."*

**三个数值的口径纪律**：

| 数值 | 原文措辞 | 能不能当常数写进代码 |
|---|---|---|
| `at least 1cm x 1cm` | *"unused space for dragging"* | 是**物理尺寸**下限，换算到 CSS px 需按设备 DPI，**本文件不给换算系数**；只作为「手指周围要留空白」的验收项 |
| `a timing delay of a few milliseconds` | 用于区分 tap / swipe / grab | **未量化**。"a few milliseconds" 字面只有几毫秒，明显不是常见的 500ms 长按阈值；本文件**不臆造具体 ms**，实现按平台长按约定并在测试中验证 |
| `roughly 100 ms` | 让位动画 | 约值，归 `motion-orchestration.md`；不是 WCAG 要求 |

**判断是否该做拖放的方法论**（逐字）：*"Because it is inherently a tricky physical interaction, understand your users' mental model ... During usability testing, observe if users attempt to drag–and–drop objects (but don't ask them about it directly)."* —— **观察自发尝试，别在问卷里问「你希望支持拖拽吗」**。

**不该优先的四种场景**（NN/g 原文可反推）：*"The downsides to drag–and–drop are that it can be inefficient, imprecise, and even physically challenging, especially over long distances"*；*"As described by Fitts's Law, moving the cursor to a precise location on screen is challenging"*（距离与精度论证归 `visual-hierarchy-gestalt.md §13`）；用户无拖放心理模型；移动端存在菜单等更低成本替代。补偿手段：*"dragging a shape in Photoshop can get it to the general desired area, and then arrow keys can be used to precisely position it"* —— **拖放负责粗定位，方向键负责精定位**，这条同时是 §4 替代路径的自然落点。

---

## 17 · 阈值与时序决策表

把散落在各源的数值收成一张可执行表；**「工程约定」列一律不是标准**。

| 决策点 | 数值 / 口径 | 来源 | 性质 |
|---|---|---|---|
| 合规目标下限 | `24 × 24 CSS px` + `24 CSS px` 直径圆 spacing 例外 | W3C 2.5.8 AA | 法条 |
| 增强目标 | `44 × 44 CSS px`（无 spacing 例外） | W3C 2.5.5 AAA | 法条 |
| 平台实现值 | `48 × 48 dp` ≈ `9mm`，推荐 `7–10mm`；间距 `8dp` | Material 2 | 设计值 |
| 图标视觉 / 热区 | `24 × 24 dp` 视觉 + padding 撑到 `48dp` | Material 2 | 设计值 |
| iOS / 指针目标 | `44 × 44 pt` / `44 × 44 dp` | Material 2（Apple 未逐字核验） | 平台值 |
| 键盘方向键步长 | `25 px`（*"an arbitrary default"*，建议用 `getNextCoordinates` 定制） | dnd-kit | 库默认值 |
| 列表让位动画 | `roughly 100 ms` | NN/g | 约值 |
| 触屏拖拽空白 | `at least 1cm x 1cm` | NN/g | 物理尺寸下限 |
| tap / swipe / grab 时序 | `a timing delay of a few milliseconds` | NN/g | **未量化，不臆造** |
| 手势开始后改 `touch-action` | 无效（*"will not have any impact"*） | MDN | 规范行为 |
| `pointercancel` 的 `cancelable` | `MUST be false`；`coalescedEvents` / `predictedEvents` 为空 | PE3 | 规范性 |
| `setPointerCapture` 前提 | pointer 必须处于 `active buttons state`，否则静默失败；`pointerId` 不匹配抛 `NotFoundError` | PE3 | 规范性 |
| `touch-action` Baseline | *"Widely available"*，自 2019-09 起跨浏览器可用 | MDN | 兼容性事实 |

---

## 18 · 决策一图流

```
接到「拖拽 / 排序 / 手势 / 滑块 / 看板」需求
        │
        ├─ Q1 用户真的预期拖放吗？（可用性测试里是否自发尝试；NN/g「别直接问」）
        │      └─ 否 / 触屏且存在菜单、剪切粘贴等更低成本替代 → 直接做非拖动控件，结束
        │
        ├─ Q2 有没有「单指针、全程不拖动」的完成路径？（2.5.7 AA / G219）
        │      └─ 没有 → 先补 §4 四类之一（箭头 / 数字输入 / 移动到下拉 / 点击目标位置）
        │
        ├─ Q3 有没有多点或路径手势？（2.5.1 A / G215·G216）
        │      └─ 有 → 补单指针控件；注意 slider/carousel 若「偏离轨道即失焦」会同时踩两条
        │
        ├─ Q4 提交发生在 down-event 还是 up-event？（2.5.2 A / G210）
        │      └─ down-event 提交 → 改成 click / up-event，或补 Abort·Undo·Up Reversal
        │
        ├─ Q5 指针实现选哪套？
        │      ├─ 页内拖动 / 与 OS 交换文件 → HTML DnD（§12 七事件 + dragover preventDefault）
        │      └─ 需要触屏一致 / 自定义落点 / 自动滚动 → Pointer Events（§9–§11）
        │            必须监听 pointercancel；touch-action 局部声明，勿全站 none
        │
        ├─ Q6 键盘与读屏路径齐了吗？（2.1.1 / APG / dnd-kit）
        │      Tab 可聚焦 → Space·Enter 拿起 → 方向键移动 → Space·Enter 放下 → Esc 取消
        │      role=button + aria-roledescription + aria-describedby + live region（播报 position 非 index）
        │
        └─ Q7 热区与反馈达标吗？
               24×24 AA 下限 / 48×48dp 实现值 / 1cm×1cm 触屏空白
               signifier 双义 + 抓取反馈 + 落点预览（约 100ms 让位）+ 磁吸激活态
```

---

## 19 · 替代路径矩阵：四种输入各自满足哪条 SC

这张表用来回答「我们做了键盘模式，为什么还不过审」。

| 输入路径 | 2.5.1（A，路径/多点手势） | 2.5.7（AA，拖动） | 2.5.2（A，取消） | 2.1.1（A，键盘） | 读屏可用 |
|---|---|---|---|---|---|
| **单指针无拖动控件**（G219 箭头 / 数字 / 下拉） | ✅ 若同时替代了路径手势则走 G215 | ✅ **唯一直接命中** | ✅ 用 `click` 即 up-event | ❌ 仍需键盘可达 | ✅ 语义控件天然可读 |
| **键盘 Space + 方向键**（dnd-kit Keyboard sensor） | ❌ 键盘非 single pointer | ❌ | ✅ `Escape` 取消 | ✅ | ✅ 需指令 + live region |
| **`Escape` / Undo / 确认框**（G210） | ❌ | ❌ 只是取消，不是完成路径 | ✅ | — | 需播报 |
| **原生 `click` 抬起激活**（G212） | ❌ | ❌ | ✅ No Down-Event | ✅ 键盘也触发 click | ✅ |
| **读屏独立控件**（上移/下移按钮、位置输入框） | ✅ 单指针可点 | ✅ | ✅ | ✅ | ✅ **最稳** |

**结论**：**一套设计要同时过 2.5.1 / 2.5.7 / 2.5.2 / 2.1.1，最低成本组合是「语义按钮形态的无拖动控件 + `click` 提交 + `Escape` 取消 + live region 播报」**；拖拽本身只是给有精细运动能力且预期它的用户提供的**加速通道**，不是主路径。这也解释了 NN/g 为什么把「用户是否预期拖放」放在第一位。

---

## 20 · 库生态实测与选型

GitHub API 实测（2026-11-10，`GET /repos/{owner}/{repo}`，star / license / pushed_at / archived 均为实测值）：

| 仓库 | ★ | License | pushed | 定位 |
|---|---|---|---|---|
| `clauderic/dnd-kit` | 17,787 | MIT | 2026-10-31 | 键盘 sensor / ARIA 默认值最完整，**本文件 §13 §14 的参照实现** |
| `react-dnd/react-dnd` | 21,625 | MIT | 2025-07-06 | 抽象 DnD 后端分层，年久未推送 |
| `SortableJS/Sortable` | 31,207 | MIT | 2026-03-24 | 框架无关列表排序 |
| `atlassian/pragmatic-drag-and-drop` | 12,795 | NOASSERTION | 2026-11-10 | Atlassian 低层原语，活跃 |
| `taye/interact.js` | 12,941 | MIT | 2026-08-01 | 拖拽 / 缩放 / 手势统一 |
| `pmndrs/use-gesture` | 9,627 | MIT | 2024-07-15 | 手势状态层 |
| `motiondivision/motion` | 35,046 | MIT | 2026-11-10 | 动画层（重排动画归 `motion-orchestration.md`） |
| `FormidableLabs/react-swipeable` | 2,111 | MIT | 2024-12-23 | 滑动识别 |
| `w3c/pointerevents` | 83 | NOASSERTION | 2026-10-08 | 规范源仓库 |
| `reactjs/rfcs` | 5,820 | MIT | 2024-06-11 | 生态背景 |

**选型三问**（工程约定）：① 需不需要开箱即用的键盘与读屏契约 → 需要就优先看 dnd-kit 的默认值并**照 §19 补齐无拖动控件**；② 是页内排序还是与 OS 交换数据 → 后者才考虑原生 HTML DnD；③ 是否有触屏/手写笔一致行为要求 → 有则必须核查库的 `touch-action` / `pointercancel` 处理，而不是只看 demo 里的鼠标效果。**库的 star 数不是合规证据**；`NOASSERTION` 表示 API 未给出可识别许可，商用前需自行核对 LICENSE 文件。

---

## 21 · 与既有资产的边界矩阵

| 问题 | 归本文件 | 归别处 |
|---|---|---|
| 拖动必须有单指针替代、G219 四类形态 | ✅ §3 §4 §19 | `accessibility.md §2` 只列阈值表 |
| `pointercancel` / capture / `touch-action` 因果链 | ✅ §9 §10 §11 | `responsive-layout.md` 只有一句全站滥用提醒 |
| WCAG 2.5.8 / 2.5.5 与 Material 2 三口径分离 | ✅ §8 | `accessibility.md §6.1` 是 24/44/60 判定表 |
| 复合组件通用键盘契约、roving tabindex、单 tab stop | ❌ | `component-api-design.md §12` / APG |
| 焦点三层、`:focus-visible`、对比度 3:1 / 4.5:1 | ❌ | `accessibility.md` / `color-science.md` |
| FLIP、stagger、@starting-style、让位动画实现 | ❌（只登记约 100ms 口径） | `motion-orchestration.md` |
| Fitts 三形式、drop zone 距离论证 | ❌（只引用结论） | `visual-hierarchy-gestalt.md §13` |
| 零结果 / 404 / 空态文案 | ❌ | `content-findability.md §18` / `feedback-states.md §5 §6` |
| 表单校验、滑块标签、表格批量操作 | ❌ | `form-table.md` |
| toast / Undo 提示条的时长与层级 | ❌ | `feedback-states.md §3` |

---

## 22 · 场景速查（12）

| # | 场景 | 先读 | 最小动作 |
|---|---|---|---|
| 1 | 看板卡片跨列拖动 | §3 §19 | 补「移动到…」下拉（G219），卡片本身保留拖拽为加速通道 |
| 2 | 长列表排序 | §4 §14 | 上/下箭头 + 位置输入框；播报「第 N 项，共 M 项」 |
| 3 | 手机上拖照片排序 | §16 §19 | 先验证用户预期；无证据改菜单 / 剪切粘贴 |
| 4 | 自定义滑块 thumb | §5 §9 | 做 pointer capture，别做「偏离轨道即失效」；补 G216 单点激活 |
| 5 | 拖到一半飞了 / 手机上断 | §9 §11 | 监听 `pointercancel` 完整回滚；局部声明 `touch-action` |
| 6 | `drop` 事件不触发 | §12 | `dragover` 里 `preventDefault()`；`drop` 是唯一可读 data store 时机 |
| 7 | 卡片文字选不中 | §12 | 只给手柄 `draggable`，别整卡设 |
| 8 | 全站禁止缩放被投诉 | §11 | 移除全站 `touch-action: none` / `user-scalable=no`（1.4.4） |
| 9 | 语音控制喊「排序」没反应 | §5 §8 | SC 2.5.3：可访问名必须含可见文本 |
| 10 | 读屏用户不知道能拖 | §13 §14 | `tabindex=0` + 中文指令 + live region + position 播报 |
| 11 | 放错位置回不来 | §6 §7 | `escape` 对所有 sensor 生效 + Undo / 放回原位即取消 |
| 12 | 摇一摇撤销 | §5 | 2.5.4：常规控件 + 关闭动作感应开关（G213） |

---

## 23 · 反模式（20）

1. 用「补了 Space + 方向键」申报 SC 2.5.7 合规（键盘不是 single pointer）。
2. 把 `Escape` / Undo 当成「不用拖也能完成」的替代（那是 2.5.2，不是 2.5.7）。
3. 只在 `pointerdown` 里提交业务动作，没有 up-event 或撤销路径。
4. 完全不监听 `pointercancel`，把浏览器接管滚动当「偶发兼容性问题」。
5. 全站 `touch-action: none` 或 `user-scalable=no`（1.4.4 缩放红线）。
6. 在 `pointerdown` 里动态改 `touch-action`，指望本手势生效。
7. 父容器 `none`、子元素写 `pan-y` 以为能救回来（祖先求交）。
8. 用 `mousemove` + `mouseup` 做跨端拖拽，触屏直接失效。
9. DOM 移动元素**之前**调 `setPointerCapture()`，导致跟踪丢失。
10. 捕获期间还依赖 `pointerover/leave` 判悬停态（捕获期不触发）。
11. `dragover` 不 `preventDefault()`，却奇怪 `drop` 不触发。
12. 在 `dragenter` / `dragover` 里读 `DataTransfer`（只在 `dragstart` 可写、`drop` 可读）。
13. 整个卡片 `draggable="true"`，用户再也无法选中卡片里的编号与文案。
14. 把 `24 × 24 CSS px` 写成「推荐点击区」，或把 `48dp` 写成「WCAG 要求」。
15. 把 2.5.8 的 24px 圆间距与 Material 的 `8dp` 间距相加 / 混算。
16. 自创拖拽手柄图标、或让手柄长得像汉堡 / kebab 菜单。
17. signifier 只表达「可抓」，不表达「抓了会移动还是缩放」。
18. 只有抓取反馈，没有释放前的落点预览；或让位动画做成 300ms 入场。
19. 读屏播报「index 0 → index 1 of 4」；取消时不播报；中文产品沿用英文默认指令。
20. 把「拖放能少点几次」当唯一论据，忽略 NN/g 的错误率与触屏交互成本。

---

## 24 · 自检（20）

1. 所有「元素跟随指针」的功能都列出来了吗？逐个有单指针无拖动路径吗（2.5.7 / G219）？
2. 该路径是「一次或多次单击」，不是「另一种拖法」吗？2.5.1 的交叉引用过了吗？
3. 键盘模式是否被误当成 2.5.7 的合规证据？2.1.1 单独验了吗？
4. 多点 / 路径手势另有 G215 / G216 的控件替代吗？滑块/轮播是否因「偏离轨道失效」同时踩两条？
5. 提交发生在 up-event / `click` 吗？若必须 down-event，`essential` 能举证吗（2.5.2）？
6. `Escape` 对**所有** sensor 生效吗？Undo / 放回原位 / 非 drop 区释放都能回滚吗（G210）？
7. `pointercancel` 有完整回滚吗（位置、capture、幽灵层、live region、视觉态）？
8. `touch-action` 是渲染时局部声明的吗？有没有全站 `none` / `user-scalable=no`？
9. `setPointerCapture()` 是否在 DOM 移动之后、且 pointer 处于 active buttons state？
10. 捕获期间是否还依赖 `pointerover/leave`？`pointerId` 不匹配时是否防了 `NotFoundError`？
11. 原生 DnD 场景：`dragover` 里 `preventDefault()` 了吗？data store 只在 `dragstart` 写、`drop` 读吗？
12. `draggable` 只加在手柄上吗？卡片内文字还能选中吗？
13. 热区写了两行吗：`合规下限 24×24 CSS px（2.5.8 AA + spacing 圆例外）` / `实现 48×48 dp`？
14. 2.5.5（AAA，44×44，无 spacing 例外）与 2.5.8 的例外集分开验了吗？
15. `8dp` 间距与 24px 圆是否被当成同一件事？
16. 可见文本与可访问名一致吗（2.5.3，语音控制）？动作感应有常规控件与关闭开关吗（2.5.4 / G213）？
17. activator 可 Tab 聚焦吗？`role=button` / `aria-roledescription` / `aria-describedby` 齐吗？
18. 中文 `screenReaderInstructions` 与 `announcements` 都本地化了吗？播报用 position 而非 index 吗？取消有播报吗？
19. signifier 同时表达「可抓」与「抓了会怎样」了吗？抓取反馈 + 落点预览 + 约 100ms 让位都有吗？
20. 触屏：有 `1cm × 1cm` 空白吗？tap/swipe/grab 能区分吗？可用性测试里观察到用户自发尝试拖放了吗？没有证据时是否改用了菜单 / 剪切粘贴？

---

## 25 · 可抄代码（5 段；§25.1–§25.3 为 Python，本轮已实跑 PASS）

### 25.1 · WCAG 2.5.8 目标尺寸与 24px 圆间距判定器

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SC 2.5.8 (AA) 静态判定：24x24 CSS px 尺寸要求 + spacing 圆例外。
口径：以每个 undersized target 的 bounding box 中心画直径 24 CSS px 的圆，
      圆与另一个目标、或与另一个 undersized target 的圆均不得相交。
注意：2.5.5 (AAA) 没有 spacing 例外，本函数只判 2.5.8。
"""
import math

MIN = 24.0
R = MIN / 2.0


def _center(box):
    x, y, w, h = box
    return (x + w / 2.0, y + h / 2.0)


def spacing_ok(box, others):
    """others: 其他目标的 bounding box 列表；任一相交即 False。"""
    cx, cy = _center(box)
    for other in others:
        ox, oy = _center(other)
        # 圆与「另一个圆」相交：中心距 < 2R
        if math.hypot(cx - ox, cy - oy) < 2 * R:
            return False
        # 圆与「另一个目标矩形」相交：最近点距离 < R
        x, y, w, h = other
        nx = min(max(cx, x), x + w)
        ny = min(max(cy, y), y + h)
        if math.hypot(cx - nx, cy - ny) < R:
            return False
    return True


def verdict(box, others=(), equivalent=False, inline=False,
            ua_control=False, essential=False, aaa=False):
    x, y, w, h = box
    floor = 44.0 if aaa else MIN
    if w >= floor and h >= floor:
        return "PASS:size"
    if equivalent:
        return "PASS:equivalent"
    if inline:
        return "PASS:inline"
    if ua_control:
        return "PASS:user-agent-control"
    if essential:
        return "PASS:essential"
    if aaa:
        return "FAIL:2.5.5-has-no-spacing-exception"
    return "PASS:spacing" if spacing_ok(box, others) else "FAIL:2.5.8"


if __name__ == "__main__":
    # 20x20 视觉图标、彼此相距 60px：spacing 圆不相交 → 靠例外通过
    assert verdict((0, 0, 20, 20), [(60, 0, 20, 20)]) == "PASS:spacing"
    # 两个 undersized 目标贴太近 → 不通过
    assert verdict((0, 0, 20, 20), [(10, 0, 20, 20)]) == "FAIL:2.5.8"
    # 达标尺寸直接通过
    assert verdict((0, 0, 24, 24), [(10, 0, 24, 24)]) == "PASS:size"
    # AAA 44x44 无 spacing 例外
    assert verdict((0, 0, 20, 20), [(60, 0, 20, 20)], aaa=True) == \
           "FAIL:2.5.5-has-no-spacing-exception"
    assert verdict((0, 0, 44, 44), [(10, 0, 44, 44)], aaa=True) == "PASS:size"
    print("PASS §25.1 · 2.5.8 尺寸/圆间距 + 2.5.5 无 spacing 例外")
```

### 25.2 · 三体系目标尺寸对照 + CSS 静态风险扫描

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三套口径并列产出规格行，并扫描 CSS 里的缩放/手势风险声明。"""
import re

SYSTEMS = [
    ("W3C 2.5.8 AA", "24 x 24 CSS px", "法条下限；含 24 CSS px 直径圆 spacing 例外"),
    ("W3C 2.5.5 AAA", "44 x 44 CSS px", "无 spacing 例外"),
    ("Material 2 touch", "48 x 48 dp", "约 9mm；推荐 7-10mm；间距 8dp+"),
    ("Material 2 pointer", "44 x 44 dp", "鼠标 / 触控笔目标，与触屏分列"),
    ("Material 2 iOS 注", "44 x 44 pt", "本轮 Apple HIG 未逐字核验"),
]


def spec_rows():
    return ["%s | %s | %s" % row for row in SYSTEMS]


def scan_css(css):
    """返回风险码列表；只做静态可检出项。"""
    flags = []
    # 全站 none：选择器为 * / html / body 且值为 none
    for sel, val in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        v = re.search(r"touch-action\s*:\s*([^;]+)", val)
        if not v:
            continue
        value = v.group(1).strip().lower()
        s = sel.strip().lower().replace("\n", " ")
        if value == "none" and any(k in s for k in ("*", "html", "body", ":root")):
            flags.append("TOUCH_ACTION_NONE_GLOBAL:1.4.4-zoom-risk")
        if value == "none":
            flags.append("TOUCH_ACTION_NONE:verify-pinch-zoom")
    if re.search(r"user-scalable\s*=\s*no", css, re.I):
        flags.append("USER_SCALABLE_NO:1.4.4-zoom-risk")
    return sorted(set(flags))


if __name__ == "__main__":
    rows = spec_rows()
    assert len(rows) == 5 and "24 x 24 CSS px" in rows[0]
    assert "48 x 48 dp" in rows[2]

    good = """
    .board__handle { touch-action: none; }
    .board__list   { touch-action: pan-y; }
    """
    bad = """
    html { touch-action: none; }
    """
    assert scan_css(good) == ["TOUCH_ACTION_NONE:verify-pinch-zoom"]
    assert "TOUCH_ACTION_NONE_GLOBAL:1.4.4-zoom-risk" in scan_css(bad)
    assert "USER_SCALABLE_NO:1.4.4-zoom-risk" in scan_css(
        '<meta name="viewport" content="user-scalable=no">')
    for r in rows:
        print("  ", r)
    print("PASS §25.2 · 三口径规格行 + touch-action/缩放静态扫描")
```

### 25.3 · 拖拽可访问性契约静态扫描器

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描一段组件源码，检查直接操纵的四条并存路径是否接线。
只做静态可检出项；真实读屏行为仍需按 accessibility.md 的实测脚本复核。
"""
import re

CHECKS = [
    ("P2-pointercancel", r"pointercancel", "PE3 规范性必达事件：必须完整回滚"),
    ("P2-capture", r"setPointerCapture\s*\(", "指针移出手柄后仍需持续跟踪"),
    ("P2-touch-action", r"touch-action\s*:\s*(?!none\b)(?:pan-x|pan-y|manipulation|auto|pinch-zoom)",
     "局部声明手势归属；全站 none 有 1.4.4 风险"),
    ("P3-escape", r"Escape|Esc\b|onDragCancel", "取消对所有 sensor 生效"),
    ("P4-no-drag-control", r"aria-label\s*=\s*[\"'][^\"']*(?:上移|下移|移动到|Move up|Move down|Move to)",
     "SC 2.5.7 / G219：单指针无拖动完成路径"),
    ("P4-keyboard-pickup", r"Space|space|Enter|enter", "2.1.1：Space/Enter 拿起与放下"),
    ("P4-focusable", r"tabindex\s*=\s*[\"']0[\"']|<button\b", "activator 可 Tab 聚焦"),
    ("P4-role", r"role\s*=\s*[\"']button[\"']", "dnd-kit 默认 role=button"),
    ("P4-roledescription", r"aria-roledescription", "身份播报：可拖拽项"),
    ("P4-describedby", r"aria-describedby", "操作指令指向离屏说明"),
    ("P4-live-region", r"aria-live|role\s*=\s*[\"']status[\"']", "实时播报拖动状态"),
    ("P3-label-in-name", r">\s*排序\s*<", "2.5.3：可见文本须出现在可访问名里"),
]


def audit(src):
    missing = [(name, why) for name, pat, why in CHECKS
               if not re.search(pat, src)]
    return {"passed": len(CHECKS) - len(missing),
            "total": len(CHECKS),
            "missing": missing,
            "verdict": "PASS" if not missing else "REVIEW"}


if __name__ == "__main__":
    bad = """<div class="card" draggable="true" onmousemove="move()">排序</div>"""
    good = """
    <button role="button" tabindex="0" aria-roledescription="可拖拽项"
            aria-describedby="dnd-instructions" aria-label="排序 上移">
      排序
    </button>
    <button aria-label="上移">↑</button>
    <button aria-label="移动到…">…</button>
    <div id="dnd-instructions">按空格键或回车键拿起，方向键移动，Esc 取消</div>
    <div aria-live="assertive" role="status"></div>
    <style>.handle { touch-action: pan-y; }</style>
    <script>
      el.addEventListener('pointerdown', e => el.setPointerCapture(e.pointerId));
      el.addEventListener('pointercancel', rollback);
      onKey('Space', pickup); onKey('Escape', cancel);
    </script>
    """
    r_bad, r_good = audit(bad), audit(good)
    assert r_bad["verdict"] == "REVIEW" and len(r_bad["missing"]) >= 8
    assert r_good["verdict"] == "PASS", r_good["missing"]
    print("  坏例: %d/%d → %s" % (r_bad["passed"], r_bad["total"], r_bad["verdict"]))
    print("  好例: %d/%d → %s" % (r_good["passed"], r_good["total"], r_good["verdict"]))
    print("PASS §25.3 · 拖拽四段路径静态接线检查")
```

### 25.4 · Pointer Events + `touch-action` + capture + Esc 取消骨架（JS/CSS）

```js
// 只在自定义拖拽表面局部声明；页面主体保留 pan-y / pinch-zoom。
// CSS: .drag-surface { touch-action: none; }  ← 不要写到 html/body/:root
let state = 'idle', origin = null, ghost = null, pid = null;
const el = document.querySelector('.drag-surface');

function rollback(reason) {
  if (pid !== null && el.hasPointerCapture?.(pid)) el.releasePointerCapture(pid);
  pid = null; ghost?.remove(); ghost = null;
  if (origin) el.style.transform = origin;   // 位置回滚
  el.classList.remove('is-dragging', 'is-over-target');
  state = 'idle';
  liveRegion.textContent = reason === 'cancel'
    ? '已取消拖动，回到原位。' : '';       // 取消也要播报
}

el.addEventListener('pointerdown', e => {
  if (state !== 'idle') return;
  state = 'armed'; pid = e.pointerId; origin = el.style.transform;
  // 注意：不要在此提交任何业务动作（SC 2.5.2 No Down-Event）
});

el.addEventListener('pointermove', e => {
  if (state === 'idle' || e.pointerId !== pid) return;
  if (state === 'armed') {
    // DOM 移动之后才设 capture（PE3 / MDN 顺序要求）
    state = 'dragging'; el.classList.add('is-dragging');
    el.setPointerCapture(pid);             // pointer 必须处于 active buttons state
  }
  // 抓取反馈 + 落点预览；约 100ms 让位动画交给 motion-orchestration.md
});

el.addEventListener('pointerup', e => {
  if (state === 'armed') { rollback('click'); return; }   // 未移动 → 视为 click
  if (state === 'dragging' && el.classList.contains('is-over-target')) {
    commit();                                             // 此时才提交
  }
  rollback('drop');
});
el.addEventListener('pointercancel', () => rollback('cancel')); // 一等公民
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && state !== 'idle') rollback('cancel'); // 对所有 sensor
});
```

### 25.5 · dnd-kit 中文指令与 position 播报（JS，模板见 §14）

```js
// 要点：播报业务名称而非 active.id；用「第 N 项，共 M 项」而非 index；取消也要播报。
const screenReaderInstructions = {
  draggable: '按空格键或回车键拿起该项。拖动时用方向键移动。再按空格键或回车键放下，按 Esc 键取消。',
};
const announcements = {
  onDragStart({active})  { return `已拿起「${label(active.id)}」，当前第 ${position(active.id)} 项，共 ${count} 项。`; },
  onDragOver({active, over}) {
    return over ? `「${label(active.id)}」移动到第 ${position(over.id)} 项位置。`
                : `「${label(active.id)}」已离开可放置区域。`;
  },
  onDragEnd({active, over}) {
    return over ? `「${label(active.id)}」已放到第 ${position(over.id)} 项，共 ${count} 项。`
                : `「${label(active.id)}」已放下。`;
  },
  onDragCancel({active}) { return `已取消拖动，「${label(active.id)}」回到原位。`; },
};
// 另需按 G219 补上「上移 / 下移 / 移动到…」语义按钮 —— 键盘 sensor 不能申报 2.5.7。
```

---

## 26 · 取源与限制（公开记录）

**W3C / WAI（本轮逐页逐字核验）**：`Understanding WCAG 2.2` 的 `pointer-gestures.html`（SC 2.5.1 A、path-based 定义、slider/carousel 三态判例、keyboard 不足的 Intent、G215·G216·F105、Key Terms 的 down/up-event、dragging movement、single pointer、essential）、`pointer-cancellation.html`（SC 2.5.2 A 四选一、up-event 最可访问、drag-and-drop 的 Abort/Undo 加码、G210·G212 与 `Potential future technique`）、`dragging-movements.html`（SC 2.5.7 AA 逐字、两类正式例外、UA 滚动与 CSS `overflow` 的排除、作者自写滚动的反向边界、唯一充分技术 G219）、`label-in-name.html`（SC 2.5.3 A、In Brief 语音控制、label/name 术语）、`motion-actuation.html`（SC 2.5.4 A、`Supported Interface` / `Essential`、G213）、`target-size-minimum.html`（SC 2.5.8 AA、24×24、24 CSS px 直径圆、五例外、Size requirement 的方形判定、`independent of the zoom factor`）、`target-size-enhanced.html`（SC 2.5.5 AAA、44×44、四例外、无 Spacing）、`Techniques/general/G219`、`Techniques/general/G210`（含 AT 消费手势的警告）、`WAI/ARIA/apg/practices/keyboard-interface/`（焦点、快捷键不替代导航、tabindex 数值、composite 单 tab stop、`aria-activedescendant`）。

**W3C Pointer Events Level 3**（`https://www.w3.org/TR/pointerevents3/`）：§4.1.3 的 `pointer capture target override` 与 direct manipulation 隐式捕获、§4.1.3.1 的 `touch-action` 段落（小写 must，已标注）、§4.2 的 `MUST suppress a pointer event stream` 四步与 `pointercancel` 的 `cancelable=false`、§5 的 `setPointerCapture` 规范性定义与 `NotFoundError`、§2 的 RFC 2119 全大写规则与 notes 非规范性说明。

**MDN**：`Web/API/Pointer_events`（统一模型、`pointerType` / `isPrimary`、事件表、capture 三方法、捕获期边界事件不触发、`pointercancel`、DOM 移动顺序、compatibility mouse events）、`Web/CSS/touch-action`（全值表、`manipulation` 别名、祖先求交、手势开始后改值无效、`none` 的 1.4.4 风险、形式语法与形式定义、Baseline 2019-09）、`Web/API/HTML_Drag_and_Drop_API`（三种用例、七事件、`draggable` 破坏选文本、drag data store 读写窗口、drop target 的 `preventDefault()` 与 fly-back）。

**NN/g**：`Drag-and-Drop: How to Design for Intuitive Interactions`（2020-02-23；signifier 双义、两类 visual signifiers、两类反馈、roughly 100 ms、`at least 1cm x 1cm`、`a timing delay of a few milliseconds`、触屏 only-when 两条件、Gmail 移动端菜单例、Fitts 与长距离缺陷、magnetism / snapping / haptics、键盘与读屏两步、观察而非询问）。

**dnd-kit**：`Accessibility - Legacy`（三问框架、Keyboard sensor 默认值 `25` pixels、Space/Enter/方向键/Escape、`tabindex="0"`、`role="button"`、`aria-roledescription="draggable"`、`aria-describedby`、默认英文 instructions、四段 defaultAnnouncements、position 优于 index、多语言需自行翻译、Escape 对所有 sensor）。

**Material 2（注意是 M2）**：`m2.material.io/design/usability/accessibility.html`（48×48 dp / 9mm / 7–10mm / 44×44 pt iOS / 44×44 dp pointer / Android 48×48 dp / 8dp 间距 / 视觉 24dp + padding 48dp）；`m2.material.io/design/interaction/gestures.html`（手势分类）。

**GitHub API 实测**（2026-11-10）：§20 的 10 个仓库 star / license / pushed_at / archived 均为 `GET /repos/{owner}/{repo}` 实测值。

**取源限制（不臆造、不外推）**：

- `https://m3.material.io/foundations/accessible-design/accessibility-basics` 返回 **404 This page cannot be found**；本文件所有 Material 数值均来自 **Material 2** 官方页，**不含任何 M3 触摸目标数值**。
- `https://developer.apple.com/design/human-interface-guidelines/accessibility` 本轮抓取只得到站点骨架（颜色方案、Skip Navigation），**Apple HIG 的 `44pt` 未逐字核验**；§8 的 iOS 数值明确标注来自 Material 2 的转述句，下轮候选。
- `https://www.w3.org/TR/wai-aria-1.2/` 两次返回 `"Just a moment..."`（疑似反机器人页），**`aria-grabbed` / `aria-dropeffect` 的官方弃用原文未取到**；WebSearch 得到的二手说法互相冲突，**一律不写入本文件**，下轮候选。
- W3C APG 当前提供的键盘接口文本里**没有** `accesskey`、单字符快捷键、drag-and-drop 的专门段落，页面还含 `To be written.` / `... to be continued ...` 未完成标记；本文件只采用已明确出现的焦点、导航、tabindex、快捷键原则，**不推断完整 APG 站点没有这些内容**。
- WebSearch「HTML5 原生 DnD 在 iOS/Android 不可用」的结果全为中文教程 / 博客 / 问答站，**不足以作为规范依据**；本文件只按 MDN 原文写「定义里是 mouse」「三种用例」，**不把移动端不可用写成官方结论**。
- **PE3 不是「supersedes Touch Events」**：逐字只有 *"This revision of Pointer Events supersedes [PointerEvents2]"*，Touch Events 仅出现在非规范性 Note 且措辞是 *"does not provide any advice"*。
- PE3 §4.1.3.1 的 `Authors must instead use touch-action` 中 `must` 为**小写**，按同规范 §2 的 RFC 2119 全大写规则不算规范性关键词；本文件照录并标注，未升格为 MUST。
- NN/g 的 `a few milliseconds` **未量化**；本文件没有把它换算成 300/500ms 之类常数。`1cm × 1cm` 是物理尺寸，本文件不提供 CSS px 换算系数。
- §17 的「键盘 `25 px`」是 dnd-kit **库默认且自述 arbitrary**，`roughly 100 ms` 是 NN/g 约值，`48dp / 8dp / 7–10mm` 是 Material 2 设计值；三者都不是 WCAG 要求。
- §25 的三段 Python 只做**静态可检出项**；真实读屏与 AT 手势消费行为仍须按 `accessibility.md` 的读屏实测脚本与 G210 的 AT 支持警告复核。
- §19 的「最低成本组合」与 §20 的「选型三问」是**本知识库工程裁决**，不是任何规范的原文要求。

**下轮候选缺口**：① Apple HIG `Gestures` / `Drag and drop` / `Accessibility` 正文逐字核验（本轮 JS 渲染只得到骨架）；② WAI-ARIA 1.2 官方 TR 的 `aria-grabbed` / `aria-dropeffect` 弃用原文（本轮被拦截，改走 GitHub raw 或 ED 版）；③ Atlassian pragmatic-drag-and-drop 官方文档的 `touch-action` / 自动滚动 / drop indicator 精确实现；④ Material 3 现行 drag & drop / touch target 页面（本轮 M3 accessibility-basics 404，需找现行路径）；⑤ 自动滚动边缘速度、虚拟列表拖拽、跨容器嵌套 drop zone 的工程实证；⑥ 手写笔压感 / `pointerType=pen` / palm rejection 与倾斜的设计口径；⑦ 长按时序的权威量化来源（本轮 NN/g 只给 "a few milliseconds"）；⑧ 沿用 #28/#29/#30 未结项（Apple HIG `search-fields`、Baymard 站内搜索报告、分面搜索、中文可读性权威资料、`radix-ui/themes` shape token 源码定位）。
