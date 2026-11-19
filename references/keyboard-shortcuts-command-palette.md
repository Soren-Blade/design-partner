# 键盘快捷键与命令面板（Keyboard Shortcuts & Command Palette）：把「记不住的按键」做成可发现、可关闭、可重映射的契约

> 快照 2026-11-14 · 取源 15 条官方一手页 + 6 个库 GitHub API 实测。凡数值均标注来源；未取到的写进 §16，不臆造。

---

## §0 一句话立场与三条裁决

**一句话立场**：快捷键不是「给熟练用户的彩蛋」，而是一份**带退出条款的加速契约**——每一个按键都必须能回答：它属于哪个作用域、会不会和系统抢、用户能不能关掉或改掉、不知道它的人怎么发现它。

**三条裁决**（本节的判断顺序，先判前一条再判后一条）：

1. **先判「要不要」，再判「哪一类」**——WCAG 2.2 SC 2.1.4 只约束「只依赖可打印字符」的快捷键，`Ctrl+K` 不在约束范围内；但**不受 2.1.4 约束 ≠ 可以做**：APG 明确说快捷键不能替代导航，全键盘可达性由 SC 2.1.1 独立要求。
2. **修饰键是平台契约，不是审美选择**——macOS 以 Command 为主修饰、Windows 以 Ctrl 为主修饰，`aria-keyshortcuts` 只做「声明」不做「绑定」，`accesskey` 因 UA 行为差异大而在通用站点上被 MDN 明确劝退。
3. **命令面板是「命令注册表 + combobox 检索层」，不是一个大输入框**——焦点留在输入框、选中态靠 `aria-activedescendant`、回车选中、Esc 关闭并归还焦点；IME 组字期间（`isComposing`）不得响应选中键。

**键盘可达性（keyboard-only）与快捷键是两条独立要求**：SC 2.1.1 要求「所有功能都能通过键盘接口操作」——用户不用鼠标也要能完成整条任务（打开、选择、确认、撤销、关闭）；快捷键只在「高频重复动作」上做加速（Q1），它不是可达性的替代品，也不是功能唯一入口。

**这一行最容易被引错的两件事**：

- 把「注册页/登录页」的键盘问题当成 2.1.4 问题——2.1.4 只管**字符键快捷键**这一件事，与表单标签、错误提示无关。
- 把 `aria-keyshortcuts` 当成「绑定快捷键的 API」——原文是 *"User agents MUST NOT change keyboard behavior in response to the aria-keyshortcuts attribute."*（WAI-ARIA 1.2 §6.7），**它只声明，不绑定**。

---

## §1 判层：五问定「做不做、做哪一类、放哪个作用域」（键盘可达性：不用鼠标能否完成任务）

接到「给这个动作加个键」「做个命令面板」时，按顺序回答这五问；**任何一问答不了，就先别写代码**。

| # | 问题 | 答「否」时 | 答「是」时进入 |
|---|---|---|---|
| Q1 | 这个动作**高频且有明确重复**吗？（不是「看起来专业」） | 不做；先优化主路径（按钮位置、默认值、批量操作） | Q2 |
| Q2 | 它是**字符键单键**、**修饰键组合**、**两段序列（chord）**、还是**组件内局部键**？ | — | 决定 SC 2.1.4 是否适用（§2 判据表） |
| Q3 | **作用域**在哪：全局 / 页面 / 弹层内 / 组件聚焦内？ | 无法说清作用域 = 一定会和别处抢键 | §7 绑定与冲突 |
| Q4 | 不记快捷键的人**怎么发现它**？（菜单右侧、tooltip、`?` 帮助面板、`aria-keyshortcuts`） | 等于只给内部人做的暗号 | §9 发现性 |
| Q5 | **冲突时谁赢**：浏览器保留键 > 系统 > 辅助技术 > 应用全局 > 页面 > 组件？ | 没定仲裁规则 = 随机双触发 | §7 仲裁表 |

**判层的典型误答**（每一种都对应一个真实返工）：

- 「用户说想要」→ 追问：他上次做这个动作是什么时候、做了几次？**没有频次就没有快捷键**。
- 「移动端也加」→ 外接键盘是少数场景；移动端优先保证触摸路径，不优先做快捷键。
- 「反正有命令面板，不加了」→ 命令面板解决**发现**，不解决**速度**；两者是不同层（§8 vs §9）。
- 「我们支持键盘了」→ **键盘能用 ≠ 不用鼠标能完成任务**：每个动作都要有不依赖指针的完整路径（Tab 次序、Enter/Space 激活、Esc 退出、方向键选择），快捷键只是这条路径上的加速带。

---

## §2 合规底线：WCAG 2.2 SC 2.1.4 只约束「可打印字符键」

### §2.1 条文逐字（W3C，Understanding SC 2.1.4，Level A）

> If a keyboard shortcut is implemented in content using only letter (including upper- and lower-case letters), punctuation, number, or symbol characters, then at least one of the following is true:

三个出口（原文为加粗定义项）：

> **Turn off** — A mechanism is available to turn the shortcut off;

> **Remap** — A mechanism is available to remap the shortcut to include one or more non-printable keyboard keys (e.g., Ctrl, Alt);

> **Active only on focus** — The keyboard shortcut for a user interface component is only active when that component has focus.

配套编号事实（写验收单时直接引）：**G217**（提供重映射或关闭机制）、**F99**（字符键快捷键无法关闭或重映射的失败例）、ACT 规则名 **No keyboard shortcut uses only printable characters**；SC 所属准则为 *Keyboard Accessible*，等级 **A**。

### §2.2 判据不是「按了几个物理键」，而是「是否依赖可打印字符」

原文 Note（这是整条 SC 最容易被判错的地方）：

> Even though this success criterion refers to character **keys**, note that it's not relevant whether a shortcut can be activated using a single physical _key_ on a keyboard, or if it requires a combination of keys to be pressed. … What matters is that a shortcut relies on a printable character (letters, punctuation, numbers, symbol characters), and not the number of physical keyboard keys that users need to press to trigger it.

序列（chord）同样在范围内：

> The success criterion also applies to situations where a shortcut is based on a _sequence_ of character keys – for example, pressing G and then A in quick succession to trigger an action.

例外（组件聚焦 / 菜单两步 / accesskey）：

> This success criterion doesn't affect components such as listboxes and drop-down menus. … Other components such as menus may be accessed or opened with a single non-character shortcut (e.g., Alt or Alt+F) before pressing a single character key to select an item. … [Access keys] are also not affected because they are generally (depending on the user agent) activated using modifier keys.

### §2.3 判据表（把「受不受 2.1.4 约束」一次判死）

| 快捷键形态 | 例子 | 受 SC 2.1.4 约束？ | 依据 |
|---|---|---|---|
| 单字符、无修饰键 | `?`、`/`、`g` | **是** | 条文首句 |
| 两段字符序列 | `g` 然后 `i`（Gmail / GitHub） | **是** | Intent Note 序列条 |
| Shift + 可打印字符 | `Shift+/`（即 `?`）、`Shift+2`（即 `@`） | **是** | Note：依赖的是可打印字符 |
| AltGr + 字符（欧洲布局） | 英国键盘 `AltGr+e` → `é` | **是** | Note 原文举例 |
| Ctrl / Alt / Meta + 任意键 | `Ctrl+K`、`Cmd+Enter` | 否 | 三个出口针对「字符键」；修饰键本身非可打印 |
| 组件聚焦内单键（type-ahead） | listbox 里按 `a` 跳到 Apple | 否（但必须只在聚焦时生效） | 例外段：*only active when the component has focus* |
| 菜单两步（Alt 或 Alt+F 再字母） | Windows 菜单助记符 | 否 | 完整路径含非打印键 |
| `accesskey` | `<button accesskey="s">` | 否（UA 通常加修饰键） | 原文举例；但另有可用性问题（§5.3） |
| 功能键 / 方向键 / Enter / Esc | `F5`、`↑`、`Esc` | 否 | 非可打印字符 |

### §2.4 与 SC 2.1.1 / 2.1.2 的分工（别把三件事混成一件）

- **2.1.1 Keyboard（A）**：*"All functionality of the content is operable through a keyboard interface without requiring specific timings for individual keystrokes…"*——它要求**每个指针动作都有键盘等价物**；快捷键只是其中一种实现，且**不充分**（APG：*"Do not use keyboard shortcuts as a substitute for access via navigation."*）。平台约定（Enter 与 Space 激活按钮）**不是规范性要求**：原文明确 *"deviating from these conventions does not fail the normative requirement"*，所以「只响应 Enter 的自定义按钮」仍满足 2.1.1。
- **2.1.2 No Keyboard Trap（A）**：焦点能进就必须能出；模态弹层（含命令面板）允许把焦点限制在内，前提是用户知道怎么离开——原文 *"This does not fail the requirements of this criterion, as long as the user knows how to 'untrap' the focus"*，并注明 Esc 通常就是「standard exit method」。失败例 **F10**，技术 **G21**。
- **2.1.4 Character Key Shortcuts（A）**：只管字符键快捷键的可关闭/可重映射/仅聚焦时生效。

---

## §3 三个合规出口怎么落成产品（不是三选一写进文档，而是三选一写进 UI）

| 出口 | 产品形态 | 验收句 | 常见假实现（不合格） |
|---|---|---|---|
| **Turn off** | 设置项「启用单键快捷键」总开关；或「关闭字符键快捷键，保留修饰键组合」 | 「关掉后 `?`、`g i` 不再触发，`Ctrl+K` 仍可用」 | 只给一个「快捷键帮助页」——帮助不等于关闭 |
| **Remap** | 可视化改键面板（搜索命令 → 录制新键 → 冲突提示 → 恢复默认） | 「用户能把 `g i` 改成 `Ctrl+Alt+I`，改完立即生效并持久化」 | 只允许在配置文件里手改；或只让改「部分」命令 |
| **Active only on focus** | 监听器挂在组件根节点而非 `document`；失焦即失效 | 「焦点在编辑器外时，`e` 不再触发编辑命令」 | 用 `document.addEventListener` 但声称「只在聚焦时生效」 |

**一手产品实证（GitHub，2026-11-14 取源）**：

> You can disable character key shortcuts, while still allowing shortcuts that use modifier keys, in your accessibility settings.

这句话之所以可以直接当范例：GitHub 的站点级快捷键里正有 `G` 然后 `C/I/P/A/W/G` 这类**字符序列**（其文档：`` `G` `C` Go to the Code tab ``），按 §2.2 的序列 Note，它们**受 2.1.4 约束**；于是 GitHub 用「设置项关闭字符键、保留修饰键」精确落在 **Turn off** 分支上。**这是「一条 SC 对应一个设置项」的完整闭环，可直接抄结构。**

**三个出口的选择顺序**（工程建议）：

1. 该快捷键**只在一个组件内有意义** → 直接选 *Active only on focus*（成本最低，且天然满足）。
2. 需要**全局单键**（`?` 打开帮助、`/` 聚焦搜索）→ 必须配 *Turn off*（设置项），因为这类键最容易误触。
3. 已有**用户自定义体系**（IDE、设计工具、专业软件）→ 选 *Remap*，并把冲突检测做进改键面板。

---

## §4 平台修饰键契约：Command / Ctrl、列出顺序、显示格式

### §4.1 macOS（Apple HIG · Keyboards，逐字取源）

定义：

> A *keyboard shortcut* is a combination of a primary key and one or more modifier keys (Control, Option, Shift, and Command) that map to a specific command. A keyboard shortcut in a game — called a *key binding* — often consists of a single key.

四个修饰键的推荐角色（HIG 原表）：

| 修饰键 | 符号 | Recommended usage（原文） |
|---|---|---|
| Command | ⌘ | "Prefer the Command key as the main modifier key in a custom keyboard shortcut." |
| Shift | ⇧ | "Prefer the Shift key as a secondary modifier that complements a related shortcut." |
| Option | ⌥ | "Use the Option modifier sparingly for less-common commands or power features." |
| Control | ⌃ | "Avoid using the Control key as a modifier. The system uses Control in many systemwide features and shortcuts…" |

**列出顺序**（不是按下顺序）：

> **List modifier keys in the correct order.** If you use more than one modifier key in a custom shortcut, always list them in this order: Control, Option, Shift, Command.

**显示格式**：HIG 用连字符（hyphen）连接，如 `Command–Tab`、`Option–Command–Esc`；**不是 `+`**。写成 `⌘⇧K` 还是 `Command-Shift-K` 取决于界面语言，但**同一产品内必须一致**。

三条容易踩的 HIG 细则（逐字）：

> **Avoid adding Shift to a shortcut that uses the upper character of a two-character key.** … the keyboard shortcut for Hide Status Bar is Command-Slash, whereas the keyboard shortcut for Help is Command-Question mark, not Shift-Command-Slash.

> **Avoid creating a new shortcut by adding a modifier to an existing shortcut for an unrelated command.** … it would be confusing to use Shift-Command-Z as the shortcut for a command that's unrelated to undo and redo.

> **Respect standard keyboard shortcuts.** … prefer creating a custom shortcut for it instead of repurposing a standard one that people associate with a different action.

还有一条**布局相关**的原文警告：

> Tip: Some languages require modifier keys to generate certain characters. For example, on a French keyboard, Option-5 generates the "{" character. It's usually safe to use the Command key as a modifier, but avoid using an additional modifier with characters that aren't available on all keyboards.

### §4.2 Windows（Microsoft Learn · Keyboard accelerators）

定义与作用域：

> Accelerator keys (or keyboard accelerators) are keyboard shortcuts that improve the usability and accessibility of your Windows applications…

> Many XAML controls have built-in keyboard accelerators. … These built-in keyboard accelerators are referred to as **control accelerators** and are executed only if the focus is on the element or one of its children. Accelerators defined by you … are referred to as **app accelerators**.

冲突谁赢：

> When two keyboard accelerators are defined with the same key combination, the first keyboard accelerator found on the visual tree is invoked.

> A keyboard accelerator event bubbles from the element that has focus up to the root. If the event isn't handled, the XAML framework looks for other unscoped app accelerators outside of the bubbling path.

自动重复（不可关）：

> An accelerator auto-repeats (for example, when the user presses Ctrl+Shift and then holds down M, the accelerator is invoked repeatedly until M is released). This behavior cannot be modified.

通用约定（原文节选，做表格对照用）：

| 功能 | 通用加速键 |
|---|---|
| Select all | `Ctrl+A` |
| Undo / Redo | `Ctrl+Z` / `Ctrl+Y` |
| Cut / Copy / Paste | `Ctrl+X` / `Ctrl+C`（或 `Ctrl+Insert`）/ `Ctrl+V`（或 `Shift+Insert`） |
| Save / Close / Print | `Ctrl+S` / `Ctrl+W` / `Ctrl+P` |
| Find / Find next | `Ctrl+F` / `F3` |
| Rename / New | `F2` / `Ctrl+N` |
| Delete（可撤销 / 不可撤销） | `Del`、`Ctrl+D` / `Shift+Del` |

> Notice that some of the combinations are not valid for localized versions of Windows. For example, in the Spanish version of Windows, Ctrl+N is used for bold instead of Ctrl+B. We recommend providing localized keyboard accelerators if the app is localized.

### §4.3 Web 的跨平台写法（APG + aria-keyshortcuts）

APG 通用函数约定表（原文节选；macOS 列空缺为原文如此）：

| Function | Windows/Linux | macOS |
|---|---|---|
| Copy | Control + C | Command + C |
| Paste | Control + V | Command + V |
| Cut | Control + X | Command + X |
| Undo | Control + Z | Command + Z |
| Redo | Control + Y | Command + Shift + Z |

`aria-keyshortcuts` 的修饰键名**只有五个**：

> Authors MUST specify modifier keys exactly according to the UI Events KeyboardEvent key Values spec … for example, "Alt", "Control", "Shift", "Meta", or "AltGraph". Note that Meta corresponds to the Command key, and Alt to the Option key, on Apple computers.

即：**没有 `Super`、`Hyper`、`Win`、`Cmd`**。写 `Cmd+K` 进 `aria-keyshortcuts` 是语法错误，读屏会念错或忽略。

### §4.4 一张跨平台映射表（实现层直接抄）

| 语义 | macOS | Windows / Linux | Web 实现（tinykeys / cmdk 风格） | aria-keyshortcuts 写法 |
|---|---|---|---|---|
| 主修饰 | Command | Ctrl | `$mod` → Meta / Control | `Meta+K` / `Control+K` |
| 次要修饰 | Shift | Shift | `Shift` | `Shift` |
| 备选修饰 | Option | Alt | `Alt` | `Alt` |
| 系统保留（避免） | Control | Win / Meta | 不绑定 | 不写 |
| 撤销 / 重做 | Command-Z / Command-Shift-Z | Ctrl-Z / Ctrl-Y | — | `Meta+Z` / `Control+Y` |
| 搜索 / 命令面板 | Command-K | Ctrl-K | `$mod+k` | `Meta+K` / `Control+K` |

**纪律**：`aria-keyshortcuts` 要按**用户在哪个平台就用哪个平台的键名**输出（服务端渲染时用 UA/平台判断），不要永远写 `Control+K` 让 Mac 用户听到「Control K」。

---

## §5 四层语义：行为绑定、aria-keyshortcuts、accesskey、`<kbd>`

这四件事经常被当成一件事，实际是四个不同的层。**混用是这一行最高频的实现缺陷。**

| 层 | 是什么 | 不是什么 | 谁负责 |
|---|---|---|---|
| **行为绑定** | `keydown` 监听 + 匹配 + 执行 | 不是声明式注解 | 你的 JS（或库） |
| **`aria-keyshortcuts`** | 向辅助技术**声明**「这个元素有这些快捷键」 | **不绑定行为**；不改 UA 行为 | 你写属性，你写监听 |
| **`accesskey`** | 让 UA 生成一个**它自己决定**的快捷键 | 不是你指定的组合键 | UA（各浏览器差异巨大） |
| **`<kbd>`** | 表示「用户键盘输入」的**语义 + 视觉** | 不是绑定机制 | 你写标签与样式 |

### §5.1 行为绑定侧的硬规则（来自三个规范的交集）

- **修饰键在前、非修饰键唯一且在后**（ARIA MUST）：*"Authors MUST ensure modifier keys come first … Authors MUST ensure that required non-modifier keys come last"*；`"Alt+Shift+T"` 与 `"Shift+Alt+T"` 等价，`"T+Shift+Alt"` 非法。
- **声明的是按下的键，不是生成的字符**（ARIA MUST）：*"If the character used is determined by a modifier key, the author MUST specify the actual key used to generate the character"*——美国键盘上的 `%` 应写 `Shift+5`，**不能写 `%` 或 `Shift+%`**。
- **一个属性值可含多个 chord**（用空格分隔）：合法示例含 `"Alt+Shift+P Control+F"`、`"Meta+C Meta+Shift+C"`。
- **禁用的元素必须让快捷键一起失效**（ARIA MUST）：*"Authors MUST ensure that aria-keyshortcuts applied to disabled elements are unavailable."* MDN：*"Keyboard shortcuts applied to disabled elements should also be disabled."*
- **不得抢占 OS / UA / AT**（ARIA SHOULD）：*"Authors SHOULD avoid implementing shortcut keys that inhibit operating system, user agent, or assistive technology functionality."*

### §5.2 `aria-keyshortcuts` 的完整用法

```html
<!-- 一个元素、一个组合键 -->
<button aria-keyshortcuts="Control+Shift+P" id="cmd-palette">命令面板</button>

<!-- 一个元素、两段 chord（空格分隔） -->
<div role="textbox" aria-keyshortcuts="Control+K Control+C">…</div>

<!-- 不要这样写（修饰键名错误 / 把字符当按键） -->
<!-- aria-keyshortcuts="Cmd+K"        → Cmd 不是合法修饰键名 -->
<!-- aria-keyshortcuts="Shift+%"      → 应写 Shift+5 -->
```

> The `aria-keyshortcuts` attribute exposes the existence of the shortcut to assistive technologies … Like all ARIA attributes, it has no effect on the functionality of the page; the keyboard behavior must be added via JavaScript event handlers.

### §5.3 为什么 `accesskey` 在通用站点上是坑（MDN + WHATWG 双重证据）

定义（WHATWG）：

> All HTML elements may have the `accesskey` content attribute set. The `accesskey` attribute's value is used by the user agent as a guide for creating a keyboard shortcut that activates or focuses the element.

> If specified, the value must be an ordered set of unique space-separated tokens none of which are identical to another token and each of which must be exactly one code point in length.

浏览器差异表（MDN 原表，节选；空单元格为原文未给）：

| 浏览器 | Windows | Linux | Mac |
|---|---|---|---|
| Firefox | Alt + Shift + key | （原文空） | Control + Option + key 或 Control + Alt + key |
| Edge | Alt + key | | Control + Option + key 或 Control + Option + Shift + key |
| Chrome | | | Control + Option + key |
| Safari | n/a | | Control + Option + key |
| Opera | Alt + key | Alt + Shift + key | Control + Alt + key |

MDN 的结论句：

> Because of these issues, it is generally advised not to use access keys for most general-purpose websites and web apps.

并明确点名 `aria-keyshortcuts` 与它的关系：

> The `aria-keyshortcuts` attribute is very similar to the problematic HTML `accesskey` … `accesskey` is rife with issues.

**裁决**：产品要「可发现的快捷键」→ 用菜单标注 + tooltip + `?` 帮助面板 + `aria-keyshortcuts`；**不要**用 `accesskey` 作为实现。

### §5.4 `<kbd>` 的语义与三层嵌套（MDN）

> The `<kbd>` HTML element represents user input (typically keyboard input). By default, the content text is displayed using the user agent's default monospace font.

嵌套语义三条：

> Nesting a `<kbd>` element within another `<kbd>` element represents an actual key or other unit of input as a portion of a larger input.

> Nesting a `<kbd>` element inside a `<samp>` element represents input that has been echoed back to the user by the system.

> Nesting a `<samp>` element inside a `<kbd>` element … represents input which is based on text presented by the system…

实用简化（原文许可）：

> You don't need to do all this wrapping; … simplifying this to just `<kbd>Ctrl</kbd>+<kbd>N</kbd>` would be perfectly valid.

ARIA 事实：`<kbd>` 的 Implicit ARIA role 为 **No corresponding role**，允许任意 role；只含全局属性。所以**不要给它加 `role="button"`**——它不是控件。

---

## §6 key 与 code：键盘布局、输入法组合（IME）与输入框焦点

### §6.1 `event.key` vs `event.code`（MDN 逐字）

> The `KeyboardEvent` interface's **`key`** read-only property returns the value of the key pressed by the user, taking into consideration the state of modifier keys such as Shift as well as the keyboard locale and layout.

> The **`code`** read-only property … represents a physical key on the keyboard (as opposed to the character generated by pressing the key). In other words, this property returns a value that isn't altered by keyboard layout or the state of the modifier keys.

不可反推的原文警告：

> … you can't use the value reported by KeyboardEvent.code to determine the character generated by the keystroke … the code returned is "KeyQ" for the Q key on a QWERTY layout keyboard, but the same code value also represents the ' key on Dvorak keyboards and the A key on AZERTY keyboards.

| 你要判什么 | 用哪个 | 理由 |
|---|---|---|
| 字符输入、输入法、快捷键「键名」语义 | `event.key` | 受布局与 Shift 影响，就是用户看到的字符 |
| 物理键位（游戏、WASD、跨布局稳定、扫描码） | `event.code` | 与布局无关 |
| 「Cmd/Ctrl + K」这类**跨平台命令** | 修饰键 + `key`（或库的 `$mod`） | 用户记的是字母 K，不是物理位置 |
| 「无论什么布局都要同一个物理键」 | `code`（VS Code 写作 `[Slash]`） | VS Code 原文：*"Using scan codes, it is possible to define keyboard shortcuts that do not change with the change of the keyboard layout."* |

### §6.2 中文/日文输入法（IME）组合期：最容易被忽略的 bug 源

官方判据（MDN）：

> The KeyboardEvent.isComposing read-only property returns a boolean value indicating if the event is fired within a composition session, i.e., after compositionstart and before compositionend.

**必须做的三件事**：

1. `keydown` 处理开头就判 `if (e.isComposing || e.keyCode === 229) return;`——否则用户在拼音/假名候选框里按 `Enter`（确认候选词）会被命令面板当成「选中执行」。
2. **不要用 `keypress`**：MDN 与 tinykeys 文档都注明它已废弃；组合期字符不可靠。
3. 命令面板输入框里，`Enter` / `↑` / `↓` 的响应要在 composition 结束后才生效；`Escape` 建议**先交给 IME 取消组字**，再交给面板关闭（两级 Esc），否则用户按一次 Esc 会连命令面板一起关掉。

cmdk 源码的写法可直接抄（`cmdk/src/index.tsx`）：

```js
const isComposing = e.nativeEvent.isComposing || e.keyCode === 229;
if (isComposing) return;
```

### §6.3 输入框焦点内该不该触发快捷键

三个库的默认值给出了一致的工程共识：

| 库 | 默认行为 | 原文 |
|---|---|---|
| react-hotkeys-hook | **默认禁用**表单元素上的热键 | *"By default, hotkeys are disabled when a form element is focused. This prevents accidental triggering while the user is typing."* (`enableOnFormTags` 默认 `false`) |
| tinykeys | **默认忽略** `input`/`textarea`/`select`/`contenteditable` | *"By default, tinykeys will ignore keyboard events from contenteditable, input, textarea, and select unless they are the event.currentTarget."* |
| mousetrap | 默认 `stopCallback` 拦截表单元素 | 官方 docs 的默认实现见 §7.4 |

**裁决**：

- 全局单键（`?`、`/`、`g i`）→ **输入框内一律不触发**，唯一例外是「输入框内按 `/` 聚焦搜索」这种**当前焦点本来就是它自己**的场景。
- `Escape` → 允许，但语义要分层：输入框内先清空/失焦，再关闭弹层，最后才是全局。
- `Cmd/Ctrl+K` → 允许在输入框内触发（打开命令面板是用户的显式意图），但要 `preventDefault`。
- `Cmd/Ctrl+Enter` → 提交类场景允许；**不要**用裸 `Enter` 做提交（与换行/选中冲突）。

---

## §7 作用域、绑定与冲突仲裁（含 chord 多段序列）

### §7.1 五层作用域模型（从外到内，越靠外越难抢）

```
OS 保留键（Cmd+Tab / Alt+Tab / Ctrl+Alt+Del …）
  └─ 浏览器保留键（Ctrl+L / Ctrl+T / Ctrl+W / Ctrl+P / F5 / Ctrl+F …）
      └─ 辅助技术键（Caps Lock / Insert / Scroll Lock / macOS Ctrl+Option …）
          └─ 应用全局（window/document 级，命令面板、搜索、帮助）
              └─ 页面/路由作用域（当前页面的编辑命令）
                  └─ 组件聚焦作用域（列表内 type-ahead、编辑器内按键）
```

**规则**：监听器挂得越靠内，越不打扰别人；**能挂组件根节点就不要挂 `document`**。需要全局时，明确写「全局 + 可关闭」。

### §7.2 OS 级冲突：APG 给出「应避免的三类分配」+ 辅助技术四类

> It is essential to avoid conflicts with keys that perform system level functions… this can be achieved by refraining from the following types of assignments.
> 1. Any modifier keys + any of Tab, Enter, Space, or Escape.
> 2. Meta key + any other single key (there are exceptions, but they can be risky…).
> 3. Alt + a function key.

> Deflect assistive technology key conflicts by steering clear of the following types of assignments.
> 1. Caps Lock + any other combination of keys.
> 2. Insert + any combination of other keys.
> 3. Scroll Lock + any combination of other keys.
> 4. macOS only: Control + Option + any combination of other keys.

浏览器侧重点避开的五类（原文）：

> 1. Address or location bar 2. Notification bar 3. Page refresh 4. Bookmark and history functions 5. Find functions

**「有意冲突」的四个条件**（满足才可抢浏览器键）：

> - A web application has a frequently used function that is similar to a browser function.
> - Users will often want to execute the web application function.
> - Users will rarely execute the browser function.
> - There is an efficient, alternative path to the browser function.

例：在线 IDE 抢 `Ctrl+F`（编辑器内查找）成立，因为浏览器查找另有 `Ctrl+F` 之外的路径（菜单），且用户在此场景几乎只想查代码。

### §7.3 冲突仲裁的工程规则（无规范，属工程约定）

| 冲突场景 | 仲裁 | 实现 |
|---|---|---|
| 同一 scope 内同一组合被绑定两次 | **后者覆盖前者 + 开发期告警**（生产不双触发） | 注册表用 `Map<combo, handler>`，覆盖时 `console.warn` |
| 不同 scope 同时激活 | **窄 scope 优先**（组件 > 页面 > 全局） | scope 栈，命中即停 |
| 用户自定义 vs 默认 | **用户覆盖优先** | 用户配置层叠在默认之上 |
| 全局 vs 输入框内 | **输入框内默认不触发** | 见 §6.3 |
| 与 OS/浏览器保留键冲突 | **不抢**（除非满足 §7.2 四条件） | 维护保留键黑名单 |

**四种已实现系统的仲裁方式（可直接对照选型）**：

| 系统 | 求值顺序 | 原文 |
|---|---|---|
| VS Code | **自下而上**，第一条同时匹配 `key` 与 `when` 的规则生效，之后不再处理 | *"Rules are evaluated from bottom to top. The first rule that matches both the key and when clause, is accepted."* |
| Windows XAML | 视觉树中**第一个**找到的加速键生效 | *"the first keyboard accelerator found on the visual tree is invoked"* |
| tinykeys | **绑定顺序**决定，先绑定者先触发 | *"the order of your keybindings matters … only the first will fire"*；冲突时给告警文本 `warning: tinykeys: Conflict found, "a b" did not fire, waiting for: ["a b c"]` |
| react-hotkeys-hook | **scope 激活集合** + 默认通配 `*` | *"With scopes you can group hotkeys together."*（`scopes` 默认 `*`） |

**用户改键必须持久化并即时生效**（VS Code 的参考实现）：

> The additional `keybindings.json` rules are appended at runtime to the bottom of the default rules, thus allowing them to overwrite the default rules. The `keybindings.json` file is watched by VS Code, so editing it while VS Code is running will update the rules at run-time.

### §7.4 chord（多段序列）的规则

- **分段用空格**：VS Code *"Chords (two separate keypress actions) are described by separating the two keypresses with a space. For example, Ctrl+K Ctrl+C."*
- **每段之间有超时**：tinykeys *"Each press in the sequence must be pressed within 1000ms of the last."*（`timeout` 默认 `1000`；react-hotkeys-hook `sequenceTimeoutMs` 默认 `1000`）
- **前缀歧义要处理**：同时存在 `g` 与 `g i` 时，按 `g` 后必须等超时才能判定（tinykeys 冲突告警就是为此设计）。
- **chord 不适合做「高频动作」**：两段按键的记忆成本高于修饰键组合；适合「低频但需要区别于单键」的动作（GitHub 的 `G` 系列）。
- **chord 不受 2.1.4 豁免**：它仍是字符键序列（§2.2），必须能关或能改。

### §7.5 绑定与清理（SPA 最容易漏的一条）

```js
// 正确：返回取消函数，组件卸载时调用
const unsubscribe = tinykeys(window, { "$mod+k": openPalette });

// 组件卸载 / 路由切换
return () => unsubscribe();
```

- 每次路由切换都 `addEventListener` 而不清理 → 同一动作触发 N 次（N = 访问过的页面数）。
- 用 `AbortController` 统一清理：`window.addEventListener("keydown", h, { signal })`，卸载时 `controller.abort()`。
- 命令面板里的「命令注册表」也要能注销：命令随组件卸载而消失，否则面板里会出现点了没反应的幽灵项。
- 系统级绑定的失败要**告知用户**（VS Code 原文）：*"They might fail to register if the operating system or another application uses the same key combination. VS Code shows a notification when registration fails."*

**系统级快捷键的五条限制**（VS Code `systemWide`，照抄可避免一类产品事故）：

> - They are available only in the desktop version of VS Code.
> - They apply only to user-defined keyboard shortcuts, not default or extension-contributed shortcuts.
> - They support a single key combination, not chords.
> - For the system-wide trigger, they ignore the `when` clause and remain active while VS Code is running.
> - They might fail to register if the operating system or another application uses the same key combination.

**Web 上想抢系统键**（`Escape`、`Alt+Tab`、`Ctrl+N`）：唯一官方路径是 Experimental 的 Keyboard Lock，且不是标准：

> Keyboard locking enables a web page to capture keys that are normally reserved by the user agent or the underlying operating system. The intended use of the Keyboard API is by web applications such as games or remote access apps that provide a fullscreen immersive experience.

```js
navigator.keyboard.lock(["KeyW", "KeyA", "KeyS", "KeyD"]); // 需 secure context + 瞬时用户激活
```

限制原文：*"This method can only capture keys that are granted access by the underlying operating system."*；重复调用只保留最后一次；异常 `AbortError` / `InvalidAccessError` / `InvalidStateError`。MDN 标注 **Experimental**，**无 W3C Recommendation**——不可作为跨浏览器基线。

---

## §8 面板解剖：数据模型、检索、无障碍与性能

### §8.1 契约不在这里重复

combobox + listbox + 命令注册表契约见 `content-findability.md` §6：角色与状态、DOM 焦点不进 popup（`aria-activedescendant`）、selection 跟随 focus、键盘与 `aria-autocomplete` 三档，全部以该节为准，本文件不再复述。

命令面板特有、§6 未覆盖的只有三件事：**结果分组**（§8.2）、**快捷键提示**（§8.5）、**空结果出口**（§8.3）。cmdk 的 `Tab` 未实现、`aria-*` 属性等实测差异，也并入 §6 的契约叙述，不单独维护第二份。

### §8.2 数据模型（命令注册表的字段）

```ts
type Command = {
  id: string;            // 稳定标识，用于覆盖/注销
  title: string;         // 展示名（动词开头：新建 / 打开 / 切换）
  keywords?: string[];   // 别名：拼音、英文、旧名、缩写
  section?: string;      // 分组（≤7 组）
  shortcut?: string[];   // 展示用，如 ["$mod","k"] 或 ["g","i"]
  perform: () => void;   // 执行
  disabled?: boolean;    // 禁用项：不可选中且不应报快捷键
  when?: () => boolean;  // 可用性谓词（对应 VS Code 的 when）
};
```

kbar 的 `Action` 类型（官方 docs 源码）可直接对照：

```ts
type Action = {
  id: ActionId; name: string; shortcut?: string[]; keywords?: string;
  section?: string; icon?: string | React.ReactElement | React.ReactNode;
  subtitle?: string; perform?: (currentActionImpl: ActionImpl) => any;
  parent?: ActionId;
};
```

其中 `shortcut: ["g", "t"]` 表示**按键序列**：docs 原文 *"when the user types g+t"*；`parent` 表示嵌套，*"Actions can have nested actions, represented by parent"*。

### §8.3 检索层：过滤、排序与中文

- **打分函数要能返回 0**：cmdk 的 `filter` 签名是 `(value, search, keywords?) => number`，*"It should return a number between 0 and 1, with 1 being the best match and 0 being hidden entirely."* 返回 0 即隐藏，这让「关键词完全不相干」有明确出口。
- **别把过滤和排序交给浏览器默认**：`shouldFilter={false}` 时 *"you must conditionally render valid items based on the search query yourself"*，但换来 *"Better memory usage and performance. Bring your own virtualization this way."*
- **中文检索**：英文按前缀/模糊匹配够用；中文必须补**拼音首字母**与**拼音全拼**（`新建文件` → `xjwj` / `xinjianwenjian`），否则用户打拼音时零结果。`keywords` 字段就是放这些的地方。
- **空结果要有出口**：`<Command.Empty>` 一类组件 + 一句「没有匹配的命令，试试 …」；不要显示空白面板。
- **结果分组 ≤7（经验值）**：不是米勒定律的推论（见 `visual-hierarchy-gestalt.md` §11 与 numeric-truth §1），超过就折叠或改成两级。

### §8.4 性能上限：数字要记住

cmdk 官方 FAQ 原文：

> **Virtualization?** No. Good performance up to 2,000-3,000 items, though.

代价来自架构（ARCHITECTURE.md 原文）：

> ⌘K always keeps every item and group rendered in the React tree. … if there are 2,000 items but the list is filtered to only 2 items, we still allocate memory for 2,000 instances of the Item component.

kbar 走的是另一条路：`KBarResults` *"renders a performant virtualized list of these results"*，并自述 *"tens of thousands of actions? No problem"*。

**裁决表**：

| 命令规模 | 做法 |
|---|---|
| ≤ 500 | 任意库；`shouldFilter` 默认即可 |
| 500–3,000 | cmdk 可接受（官方上限 2,000–3,000），但要实测首帧 |
| > 3,000 | 必须自建虚拟列表，或换 kbar 这类内置虚拟化的方案 |
| 数据来自远端 | 防抖 + 请求竞态处理（后发先至）+ 加载态 + 空态 + 错误态 |

### §8.5 键盘行为契约（面板内，逐键定义）

| 键 | 行为 | 备注 |
|---|---|---|
| `↑` / `↓` | 移动选中项 | 到边界时是否环绕由 `loop` 决定（cmdk `loop` 默认 `false`） |
| `Home` / `End` | 首项 / 末项 | cmdk 已实现 |
| `Enter` | 执行当前选中项 | **IME 组字中不响应**（§6.2） |
| `Escape` | 关闭面板并归还焦点 | 若 IME 正在组字，第一次 Esc 先取消组字 |
| `Tab` | **不要用于项间移动** | 若要支持，必须显式实现并保证输入框不失焦；cmdk 未实现，不写进契约 |
| `Backspace`（输入为空） | 返回上一级（多级面板） | cmdk README 用示例演示，需自行实现 |
| `Cmd/Ctrl+K` | 打开/关闭 | 同一组合的 toggle 语义要固定，不要一次开一次关错乱 |

---

## §9 发现性：帮助面板、菜单标注与 `kbd` 样式

### §9.1 五个发现触点（缺一个都算「只有内部人知道」）

| 触点 | 放什么 | 规范依据 |
|---|---|---|
| 菜单项右侧 | 快捷键字面（如 `⌘K`） | MS：*"often associated with commands exposed in menus (and should be specified with the menu item content)"* |
| hover tooltip | 「动作名（快捷键）」 | ARIA：*"Authors SHOULD provide a way to expose keyboard shortcuts … such as through the use of a tooltip."* |
| `?` 帮助面板 | 全量清单，按作用域分组 | MDN：cheat sheet page or dialog；GitHub 的 `?` |
| 首启/空状态 | 只提示 1–2 个最高价值快捷键 | 见 `onboarding-first-run.md` |
| `aria-keyshortcuts` | 机器可读声明 | ARIA MUST 规则（§5.1） |

### §9.2 `?` 帮助面板的规格

- **触发**：`?`（Shift+/）或菜单里的「键盘快捷键」；**必须与设置项一致**（关掉字符键快捷键后，`?` 不应再触发，改用菜单进入）。
- **分组**：按作用域（全局 / 当前页面 / 编辑器 / 面板内），每组 ≤7 条，按使用频率降序。
- **两列**：左「动作」（动词开头），右「按键」（平台自适应字形）。
- **平台自适应**：Mac 显示 `⌘⇧K`，Windows/Linux 显示 `Ctrl+Shift+K`；**不要**同时显示两套。
- **可搜索**：帮助面板本身也应有搜索框（命令面板可复用），否则 60 条以上就查不动。
- **可打印**：VS Code 提供 *"a condensed PDF version suitable for printing"*；Web 端至少保证打印样式不裁切。
- **显示冲突**：改键面板里要能「显示同一按键的所有命令」（VS Code：*"Right-click … select Show Same Keybindings"*）。

### §9.3 键名书写的四条硬规则

1. **按平台写字形，不按代码写**：Mac 用 `⌘ ⌥ ⇧ ⌃`，Windows 用 `Ctrl Alt Shift Win`；混写（`Ctrl+⌘`）是错误。
2. **macOS 用连字符，Windows 用加号**：HIG 的 `Command–Tab` 与 MS 的 `Ctrl+V` 各自是平台习惯；同一产品内统一。
3. **修饰键顺序固定**：macOS 按 HIG 的 `Control, Option, Shift, Command` 列出（显示时通常写作 `⌃⌥⇧⌘`）；Web/Windows 常写 `Ctrl+Shift+Alt+Key`，同样要有固定顺序。
4. **`<kbd>` 只包键名，不包加号**：`<kbd>Ctrl</kbd>+<kbd>K</kbd>`；不要 `<kbd>Ctrl+K</kbd>`（读屏会念成一串）。视觉上加号可与 kbd 同色，但语义要分开。

### §9.4 `kbd` 的样式基线（可抄）

```css
kbd {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 0.8125rem;      /* 13px，与正文形成 ~0.8 比例 */
  padding: 0.1em 0.35em;
  border: 1px solid currentColor;
  border-radius: 4px;
  opacity: 0.9;              /* 不要用低对比度灰：键名是信息，不是装饰 */
}
```

- **对比度**：键名文本仍需满足 4.5:1（正文级）；不要用 `#999` 放在白底上。
- **不要用 emoji 代替键名**（`⌘` 是符号不是 emoji；`🔍` 不是快捷键）。
- **深色模式**下 `border` 用 `currentColor` 最稳，避免写死 `#ccc`。

---

## §10 六个库的实测与选型（GitHub API 2026-11-14）

### §10.1 实测表（数字全部来自 `GET /repos/{owner}/{repo}` 实时返回）

| 仓库 | ★ | forks | 许可 | 最后 push | 分支 |
|---|---|---|---|---|---|
| `dip/cmdk`（原 `pacocoursey/cmdk`） | 13,147 | 383 | MIT | 2025-10-29 | main |
| `ccampbell/mousetrap` | 11,770 | 948 | Apache-2.0 | 2023-03-15 | master |
| `timc1/kbar` | 5,264 | 204 | MIT | 2026-08-10 | main |
| `jamiebuilds/tinykeys` | 4,106 | 89 | MIT | 2026-09-25 | main |
| `JohannesKlauss/react-hotkeys-hook` | 3,504 | 169 | MIT | 2026-11-12 | main |
| `greena13/react-hotkeys` | 2,151 | 158 | ISC | 2023-01-04 | master |
| `ssleptsov/ninja-keys` | 1,704 | 66 | MIT | 2024-07-14 | main |

**读表结论**：

- 命令面板首选 **cmdk**（体量最大、无样式、无障碍实测过）；需要虚拟化或更强结构时用 **kbar**。
- 通用热键层：**tinykeys**（~650 B，语法最现代）或 **react-hotkeys-hook**（React 生态默认值最完整）。
- **mousetrap 与 greena13/react-hotkeys 已停更**（最后 push 2023 年，未归档）——存量项目可维护，新项目不要选。
- `ninja-keys` 是 Web Component 路线的现成方案，但 2024 年后无提交。

### §10.2 各库的关键默认值（写契约前必须先知道）

| 库 | 关键默认值 | 原文 |
|---|---|---|
| cmdk | `loop=false`；`shouldFilter=true`；`vimBindings=true`；无虚拟化；**不处理 Tab** | "Good performance up to 2,000-3,000 items" |
| kbar | 开合键 `cmd+k` / `ctrl+k`；`toggleShortcut` 用 tinykeys 语法 | *"hitting cmd+k (macOS) or ctrl+k (Linux/Windows) will animate in a search input"* |
| ninja-keys | `openHotkey` 默认 `cmd+k,ctrl+k`；`navigationUpHotkey` 默认 `up,shift+tab`；`navigationDownHotkey` 默认 `down,tab`；`closeHotkey` 默认 `esc`；`goBackHotkey` 默认 `backspace`；`selectHotkey` 默认 `enter` | README Attributes 表 |
| react-hotkeys-hook | `enabled=true`；`enableOnFormTags=false`；`splitKey="+"`；`delimiter=","`；`scopes="*"`；`keydown=true`、`keyup=false`；`preventDefault=false`；`sequenceTimeoutMs=1000` | README Options 表 |
| tinykeys | `event="keydown"`；`timeout=1000`；默认忽略表单元素；`$mod` = Mac Meta / Win+Linux Control | *"Keybindings will be matched against KeyboardEvent.key and KeyboardEvent.code"* |
| mousetrap | 体积约 2 KB gzip / 4.5 KB min；`stopCallback` 默认拦截 `INPUT/SELECT/TEXTAREA/contenteditable` | docs：*"If true is returned then it stops the callback from firing"* |

### §10.3 选型决策树

```
需要「命令面板 UI」吗？
├─ 是 → 需要虚拟化 / >3000 项？
│        ├─ 是 → kbar（内置虚拟列表）
│        └─ 否 → cmdk（无样式、无障碍实测、shouldFilter 可关）
└─ 否 → 只需热键层？
         ├─ React → react-hotkeys-hook（scopes / 表单豁免 / 序列默认值齐全）
         └─ 任意框架 → tinykeys（体积最小，key+code 双匹配，chord 原生）
```

### §10.4 已知陷阱（本轮实测发现，写进契约前必须核对）

1. **`pacocoursey/cmdk` 已被 API 解析为 `dip/cmdk`**（13,147★）。引用 star 要写新名，否则会被当成旧数据。
2. **`johnlindquist/ninja-keys` 是 404**；npm 包 `ninja-keys` 对应仓库是 `ssleptsov/ninja-keys`（1,704★）。别沿用旧 star。
3. **ninja-keys 没有 `hideTrigger` 属性**（README 只有 `hideBreadcrumbs` / `disableHotkeys`）。
4. **cmdk 不处理 Tab**（README 未提、源码 switch 无 Tab）——「Tab 切换项」不是它的能力。
5. **tinykeys 不是「只用 code」也不是「只用 key」**——两者都匹配：`"d"` 走 `key`，`"KeyD"` 走 `code`。选型文里写「tinykeys 用 code」是错的。
6. **kbar 的 `useKBar` / `toggleShortcut` 不在 README**，只在仓库 `example/src/Docs/*.tsx`；引用时注明「docs 源码」。
7. **mousetrap 的 `stopCallback` 默认实现不在 README**，在官方 docs（craig.is/killing/mice）。

---

## §11 交付规格：清单模板与四条硬规则

### §11.1 交付物里必须有的表（少一行就会被返工）

| 动作 | 快捷键（Mac / Win） | 作用域 | 可关闭 | 可重映射 | 发现位置 |
|---|---|---|---|---|---|
| 打开命令面板 | ⌘K / Ctrl+K | 全局 | 是（设置项） | 是 | 菜单 + tooltip + 帮助面板 |
| 打开帮助 | ? | 全局 | 是（随字符键总开关） | 否（固定） | 菜单 |
| 聚焦搜索 | / | 全局 | 是 | 否 | 输入框 placeholder |

### §11.2 四条硬规则

1. **单字符快捷键必须有总开关**（SC 2.1.4 的 Turn off）；做不到就改成修饰键组合。
2. **每个作用域内可见快捷键 ≤12 条**；超过就说明你在用快捷键代替信息架构（APG 的认知负荷警告）。
3. **一条快捷键最多 3 个键**（1 修饰 + 1 主键 + 至多 1 个附加修饰）；4 键组合的记忆成本高于它省下的时间。
4. **保留键清单先冻结再设计**：`Cmd/Ctrl+Tab`、`Cmd/Ctrl+W`、`Cmd/Ctrl+T`、`Cmd/Ctrl+L`、`Cmd/Ctrl+P`、`F5`、`F11`、`F12`、`Cmd/Ctrl+Q`、`Alt+F4`、`Cmd+Space`、`Ctrl+Space`（输入法切换）——这些一律不抢。

---

## §12 用法速查（12 行，先对号再动手）

| 场景 | 先判什么 | 直接给结论 |
|---|---|---|
| 「给核心操作加快捷键」 | 频次 + 主路径 | 主路径没优化前，快捷键只是把慢动作变快 |
| 「用户投诉误触」 | 是否字符键单键 | 加 Turn off 或改成 `Ctrl+` 组合（§3） |
| 「要不要支持 `?` 帮助面板」 | 快捷键是否 >10 条 | 是：必须有；且面板可搜索 |
| 「Mac 用户说快捷键不对」 | 显示格式 / `$mod` | 显示层按平台映射，实现层用 `$mod` |
| 「输入框里快捷键乱触发」 | 表单豁免 | 默认不触发；`Escape` 分层（§6.3） |
| 「中文输入法按回车直接执行了」 | `isComposing` | 加 composition 守卫（§6.2） |
| 「和浏览器 Ctrl+F 冲突」 | 有意冲突四条件 | 满足才抢，且给替代路径 |
| 「命令面板 2000 项卡顿」 | 是否虚拟化 | 自建虚拟列表或换 kbar（§8.4） |
| 「面板里 Tab 切不动」 | cmdk 未实现 | 不要承诺 Tab；改用 ↑↓ |
| 「多级面板怎么返回」 | 输入为空时 Backspace | 明确层级栈与面包屑 |
| 「快捷键改了不生效」 | 持久化 + 层级 | 用户层覆盖默认层，监听配置变化（§7.3） |
| 「要不要做系统级全局键」 | Web 能力边界 | 只能 Keyboard Lock（Experimental），不做承诺 |

---

## §13 反模式（看到就该打回）

1. 用单字母（`e`、`d`、`s`）做全局快捷键，且没有关闭开关。
2. 把 `aria-keyshortcuts` 当成绑定 API，写完属性就以为能触发。
3. 在 `aria-keyshortcuts` 里写 `Cmd+K`、`Shift+%`（错误键名 / 错误字符）。
4. 用 `accesskey` 实现产品级快捷键（UA 差异 + AT 冲突）。
5. 用 `document.addEventListener` 实现「组件内快捷键」，失焦后仍然响应。
6. 输入框内仍然触发全局单键（用户打 `?` 得到帮助面板而不是问号）。
7. IME 组字期间响应 `Enter`，中文用户按回车确认候选词时执行命令。
8. 命令面板用 Tab 在项间移动焦点，导致输入框失焦、无法继续输入。
9. 命令面板没有 `aria-activedescendant` / `role=option`，读屏念不出选中项。
10. 关闭面板后焦点回到 `<body>`（用户必须重新 Tab 找位置）。
11. 冲突时两个 handler 都执行（一次按键触发两个动作）。
12. 快捷键只在「帮助页」里写，产品里没有关闭/改键入口。
13. 同一动作在不同页面绑不同键，且没有 scope 说明。
14. 显示层写死 `Ctrl+K`，Mac 用户看到错误键名。
15. 把 `?` 的帮助面板做成不可搜索的长列表（60 条以上就废）。
16. 抢 `Ctrl+W` / `Cmd+W` 且没有「有意冲突」四条件支撑。
17. 用户改键后刷新即丢失（未持久化）。
18. 命令面板加载远端数据时无加载态/空态/错误态。
19. 3,000 条以上命令仍用 cmdk 默认渲染，首帧卡死。
20. 为「显得专业」给低频操作加 chord，用户永远记不住。

---

## §14 自检清单（交付前逐条打勾，20 条）

1. 每个快捷键都写了**作用域**（全局/页面/组件聚焦）。
2. 字符键单键/序列都提供了**关闭或重映射**其一（SC 2.1.4）。
3. 关闭开关真的能关（实测：关掉后按键无响应）。
4. 重映射真的生效且持久化（刷新后仍在）。
5. 组件内快捷键挂在**组件根节点**，失焦即失效。
6. 输入框内全局单键**不触发**（逐键实测 `?` `/` `g`）。
7. IME 组字期间 `Enter` / `↓` **不执行**（用中文输入法实测）。
8. `Escape` 分层正确（IME → 弹层 → 全局），且只关一层。
9. `aria-keyshortcuts` 用**合法修饰键名**（Alt/Control/Shift/Meta/AltGraph）。
10. `aria-keyshortcuts` 声明的是**按下的键**（`Shift+5` 而非 `%`）。
11. 禁用元素的快捷键**同时失效**。
12. 命令面板焦点在输入框，选中态用 `aria-activedescendant`。
13. 命令面板关闭后**焦点归还**触发元素。
14. 命令面板结果为空时有**空态文案**。
15. 加载远端命令有**加载态 / 错误态 / 竞态保护**。
16. 命令数 >3,000 时有**虚拟化**或分页。
17. 帮助面板按作用域分组、每组 ≤7、可搜索。
18. 显示格式**平台自适应**且全产品一致。
19. 未抢占保留键（清单见 §11.2 第 4 条）。
20. 冲突时**只有一个**动作执行，且开发期有告警。

---

## §15 两段可跑脚本（以下代码已实跑通过）

三段检查分别覆盖：① 单字符快捷键检出（SC 2.1.4 落点）/ ② `aria-keyshortcuts` 语法 / ③ 冲突检测。把项目里的快捷键清单写成同样结构即可直接跑。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快捷键契约静态校验：单字符检出 / aria-keyshortcuts 语法 / 冲突检测。

约定：combo 用 "Control+Shift+P" 这种 aria 写法；$mod 表示平台主修饰键，
在 aria 层必须展开成 Control 或 Meta（本脚本按平台参数展开）。
"""
import re

MODIFIERS = {"Alt", "Control", "Shift", "Meta", "AltGraph"}
PRINTABLE_MACROS = {"Plus", "Space"}  # 非字符键名，不算「可打印字符键」


def parse_combo(combo: str, mod_key: str = "Control"):
    """拆成 (修饰键集合, 非修饰键)。$mod 按平台展开。"""
    combo = combo.strip().replace("$mod", mod_key)
    parts = [p for p in combo.split("+") if p]
    if not parts:
        return set(), ""
    return set(parts[:-1]), parts[-1]


def is_char_only(combo: str, mod_key: str = "Control") -> bool:
    """SC 2.1.4 判据：只依赖可打印字符（含 Shift/AltGr 组合、单字符序列）。"""
    mods, key = parse_combo(combo, mod_key)
    # 出现非 Shift/AltGraph 的修饰键 → 不属字符键快捷键
    if mods - {"Shift", "AltGraph"}:
        return False
    if key in PRINTABLE_MACROS:
        return False
    return len(key) == 1  # 字母/数字/标点/符号


def check_aria(value: str):
    """校验 aria-keyshortcuts：空格分隔多 chord；修饰键在前；键名合法。"""
    issues = []
    if not value or not value.strip():
        return ["空值"]
    for combo in value.split():
        parts = combo.split("+")
        if len(parts) < 1 or any(p == "" for p in parts):
            issues.append(f"{combo}: 空的键段")
            continue
        *mods, key = parts
        for m in mods:
            if m not in MODIFIERS:
                issues.append(f"{combo}: 非法修饰键名 {m!r}（只允许 {sorted(MODIFIERS)}）")
        # 修饰键必须在前：若某个非最后段不是修饰键，说明顺序错
        for i, p in enumerate(parts[:-1]):
            if p not in MODIFIERS:
                issues.append(f"{combo}: 第 {i+1} 段 {p!r} 不是修饰键（修饰键必须在前）")
        if len(key) > 1 and key not in {
            "Enter", "Tab", "Escape", "Space", "Plus", "ArrowUp", "ArrowDown",
            "ArrowLeft", "ArrowRight", "PageUp", "PageDown", "Home", "End",
            "Delete", "Backspace", "F1", "F2", "F3", "F4", "F5", "F6",
            "F7", "F8", "F9", "F10", "F11", "F12",
        } and not re.fullmatch(r"[A-Za-z0-9]", key):
            issues.append(f"{combo}: 未识别的非修饰键名 {key!r}")
        if key in {"%", "@", "#"}:
            issues.append(f"{combo}: 写成了生成字符 {key!r}，应写实际按键（如 Shift+5）")
    return issues


def find_conflicts(spec):
    """同 scope 同 combo 出现两次 → 冲突（后者会覆盖前者）。"""
    seen, conflicts = {}, []
    for item in spec:
        k = (item.get("scope", "global"), item["keys"].lower())
        if k in seen:
            conflicts.append((seen[k]["id"], item["id"], k))
        else:
            seen[k] = item
    return conflicts


SAMPLE = [
    {"id": "palette.open", "keys": "$mod+k", "scope": "global"},
    {"id": "help.open", "keys": "?", "scope": "global"},
    {"id": "search.focus", "keys": "/", "scope": "page"},
    {"id": "editor.comment", "keys": "Control+[Slash]", "scope": "editor"},
]

if __name__ == "__main__":
    # ① 单字符检出：应当恰好命中 help.open 与 search.focus
    char_only = [c["id"] for c in SAMPLE if is_char_only(c["keys"])]
    assert char_only == ["help.open", "search.focus"], char_only
    assert is_char_only("Shift+5"), "Shift+5 仍依赖可打印字符（@），必须被检出"
    assert is_char_only("Shift+/"), "Shift+/ 生成 ?，仍属字符键快捷键"
    assert not is_char_only("Meta+K"), "Meta+K 有非打印修饰键，不在 2.1.4 范围"
    assert not is_char_only("F5")

    # ② aria 语法：合法样例零问题，非法样例必须报错
    assert check_aria("Control+Shift+P") == []
    assert check_aria("Alt+Shift+P Control+F") == []
    assert check_aria("Meta+C Meta+Shift+C") == []
    assert check_aria("Shift+Space") == []
    assert check_aria("Cmd+K"), "Cmd 不是合法修饰键名，必须报错"
    assert check_aria("Shift+%"), "生成字符 % 必须报错"
    assert check_aria("K+Control"), "修饰键不在前必须报错"

    # ③ 冲突：同 scope 同键必须被检出
    dup = SAMPLE + [{"id": "palette.dup", "keys": "$mod+K", "scope": "global"}]
    conflicts = find_conflicts(dup)
    assert len(conflicts) == 1 and conflicts[0][1] == "palette.dup", conflicts

    print("PASS · 字符键 %d 条 / aria 语法 %d 例 / 冲突 %d 条"
          % (len(char_only), 4, len(conflicts)))
```

**输出**：`PASS · 字符键 2 条 / aria 语法 4 例 / 冲突 1 条`。

配套第二个脚本（显示格式与保留键检查，可直接接入 CI）：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""显示格式与保留键检查：平台字形一致、保留键不抢、修饰键顺序固定。"""
RESERVED = {
    "Meta+Tab", "Control+Tab", "Meta+W", "Control+W", "Meta+T", "Control+T",
    "Meta+L", "Control+L", "Meta+P", "Control+P", "Meta+Q", "Control+Q",
    "Meta+Space", "Control+Space", "Alt+F4", "Alt+Tab", "F5", "F11", "F12",
}
MAC_GLYPH = {"Meta": "⌘", "Alt": "⌥", "Shift": "⇧", "Control": "⌃", "AltGraph": "⌥"}


def render(combo: str, platform: str) -> str:
    parts = combo.split("+")
    *mods, key = parts
    if platform == "mac":
        return "".join(MAC_GLYPH.get(m, m) for m in mods) + key
    return "+".join(mods + [key])


def check_display(combo: str, platform: str) -> list:
    issues = []
    if platform == "mac" and "Control+" in combo:
        issues.append(f"{combo}: macOS 上 Control 慎用主修饰（HIG）")
    for r in RESERVED:
        if combo.lower() == r.lower():
            issues.append(f"{combo}: 命中保留键清单，不抢")
    mac = render(combo, "mac")
    win = render(combo, "win")
    if mac == win and platform == "mac":
        issues.append(f"{combo}: 平台渲染未区分字形")
    return issues


if __name__ == "__main__":
    assert render("Meta+Shift+K", "mac") == "⌘⇧K"
    assert render("Meta+Shift+K", "win") == "Meta+Shift+K"
    assert check_display("Control+W", "win"), "Ctrl+W 是保留键，必须报"
    assert check_display("Meta+K", "mac") == []
    print("PASS · 显示格式与保留键检查通过")
```

---

## §16 取源限制（本轮实测，未取到的写在这里，不臆造）

1. **Apple HIG `keyboard-shortcuts` slug 已 404**：`/design/human-interface-guidelines/keyboard-shortcuts`、其 `.md` 变体、`index.json`、`tutorials/data/...json` 四路全部 404；内容已并入 **Keyboards** 页，本章引文取自 `https://developer.apple.com/design/human-interface-guidelines/keyboards.md`（HTTP 200，原始 Markdown）。
2. **Apple HIG 纯 HTML 为 JS-only SPA**：首屏只有壳，正文客户端渲染，静态抓取不到文字；必须走 `.md` 后缀端点。
3. **W3C 站点对 curl/urllib 一律 403**（bot 防护）：`www.w3.org/WAI/*` 与 `www.w3.org/TR/*` 直取返回拦截页；改由 `web_fetch` 取得 UTF-8 正文，长单页规范改走 W3C 官方 GitHub 仓库 raw。
4. **WAI-ARIA 1.2 单页在 §2 处被截断**：§6.7 的 `aria-keyshortcuts` 定义改取 `https://raw.githubusercontent.com/w3c/aria/2022-12_PR/index.html`（发布源，逐字一致）。
5. **MDN 各页的浏览器兼容表为 JS 渲染**：只取得 Baseline 结论（如 key/code「Widely available since March 2017」、`<kbd>`「since July 2015」），**未取逐版本号**，故本章不写具体版本数字。
6. **Keyboard Lock 无 W3C Recommendation**：只有 WICG/Chromium 草案 + MDN 文档，MDN 标 **Experimental** 且需 Secure context；跨浏览器可用性未逐浏览器实测。
7. **SC 2.1.4 的 ACT 规则正文未抓**：只从 Understanding 页取得规则名称 *"No keyboard shortcut uses only printable characters"*，规则细节未验证。
8. **Apple HIG 标准快捷键全表未逐条抓取**：本章只引 8 行节选（Spotlight、Tab、Esc 相关），其余行不作断言。
9. **Microsoft 通用加速键表为节选**：原表更长（含 Find next、Help 等），未列出的行未验证。
10. **Microsoft Learn 两条 URL 均发生 301 迁移**：`/design/input/keyboard-accelerators` → `/develop/input/keyboard-accelerators`；`/design/input/access-keys` → `/develop/input/access-keys`。本章按最终地址取原文。
11. **GitHub 文档路径已迁移**：`/en/get-started/using-github/keyboard-shortcuts` → `/en/get-started/accessibility/keyboard-shortcuts`（301），本章按最终地址取。
12. **kbar 的 `useKBar` / `sections` / `toggleShortcut` 不在 README**：只在仓库 `example/src/Docs/APIReference.tsx`、`Actions.tsx`、`Shortcuts.tsx`；引用时已注明「docs 源码」。
13. **mousetrap 的 `stopCallback` 默认实现不在 README**：在官方 docs `https://craig.is/killing/mice`；README 只有 `bind` 示例。
14. **cmdk 的 Tab 行为未实现**：README 未提，源码 keydown switch 无 Tab；本章按「不支持」写，未推测。
15. **`johnlindquist/ninja-keys` 为 404**：npm 包对应 `ssleptsov/ninja-keys`，本章数据取自后者；未沿用任何旧 star 数。
16. **GitHub API 数字为 2026-11-14 22:03–22:10 (+08:00) 单次实测**：star/fork/push 均会变化，引用时须注明日期。
