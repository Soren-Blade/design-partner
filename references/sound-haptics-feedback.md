# 声音与触觉反馈：把「要不要响一下 / 震一下」判成通道、时长与强度

声音反馈 / 音效 / 提示音 / earcon / 听觉图标 / 触觉反馈 / 震动 / 振动 / haptic / Taptic / Vibration API / navigator.vibrate / UIFeedbackGenerator / HapticFeedbackConstants / VibrationEffect / 静音开关 / autoplay / 音频会话 / 可访问性 / 听觉障碍 / 聋盲用户 —— 凡是「这个操作要不要给一声 / 给一下」的问题，本文给判定表、平台精确值、三通道配方与验收标准。

> **本文的口径**：平台语义、常量值、法条与官方行为一律逐字引英文原文（§4、§5、§7、§12、§13 标「原文」）；**官方没有给数值的地方，本文用「裁决」标注并说明推导依据**——裁决是可校准的工程值，不是平台规定，不得倒过来说成「官方要求」。

---

## §0 一句话立场

**视觉反馈是默认项，声音与触觉是例外项：只有当「看这一眼」会漏掉、来不及、或者根本没法看的时候，才值得再占用户一条感官通道。**

而占通道之前必须先回答一个问题：**这条反馈替代了用户的哪个动作？** 如果答案是「没有替代，只是让界面显得有生气」，那它就是噪音——触觉会变成「每次滑动都嗡嗡震」的廉价感，声音会变成别人会议室里的一声怪响。

补充三条硬度递减的底线：

1. **能借系统语义就别自造**——系统已经为「点按 / 成功 / 失败 / 切换 / 阈值」定义了语义与音色，自造的第 7 种「成功音」只会让用户重新学习一遍。
2. **可关闭性是验收项，不是加分项**——声音要能被静音开关关掉，触觉要能被系统「触感反馈」关掉，应用内还要各有一个开关。
3. **声音永远不能是唯一通道**——Apple 在 visionOS 的原文是 *"avoid communicating important information using only sound. Always provide additional ways to help people understand your app."*，这句话在任何平台都成立。

---

## §1 判层：先判「要不要」，再判「哪一种」

### 1.1 五问判层（按顺序问，任一问答完就可以停）

| # | 问题 | 若「是」→ | 若「否」→ |
|---|---|---|---|
| Q1 | **用户此刻看着屏幕吗？**（驾驶、运动、做饭、游戏手柄、盲操作场景 = 否） | 非视觉通道**可能是一等通道**，进 Q2 | 视觉能承担主反馈，进 Q2 仍需判时压 |
| Q2 | **反馈有时间压力吗？**（≤1 秒内必须知道成败/是否到位） | 触觉优先（延迟最低、不需要注视），声音次选 | 只有视觉就够，进 Q3 复核 |
| Q3 | **这件事是否高频重复？**（每秒多次的滚动、输入、切换） | **不加触觉、不加声音**（见 §3.7 禁用清单） | 进 Q4 |
| Q4 | **事件是否有「系统已定义」的语义？**（点击 / 成功 / 失败 / 切换 / 阈值 / 长按） | 用系统语义常量，不自造（§3） | 才考虑自定义触觉模式或 earcon（§5.6） |
| Q5 | **用户是否已关掉这个通道？**（静音开关、系统触感关闭、应用内开关） | 必须**静默降级且不丢信息**（§7.4） | 正常输出 |

### 1.2 判层表：场景 → 通道组合

| 场景 | 视觉 | 触觉 | 声音 | 判层理由 |
|---|---|---|---|---|
| 普通按钮点按 | 按下态（必做） | 系统默认（**不要自己加**） | 不加 | 系统已给 `VIRTUAL_KEY` / 键盘音，重复加等于双震 |
| 开关 / 复选切换 | 状态变化（必做） | 可选一次轻触（`TOGGLE_ON/OFF`） | 不加 | 状态可见，触觉只是确认「点到了」 |
| 表单校验失败 | 字段红框 + 文案（必做） | **推荐**错误触觉（`REJECT` / `.error`） | 谨慎：只在长表单提交时 | 错误常发生在视线上方/下方，触觉替代「找红字」 |
| 提交成功（不可逆，如付款） | 结果页（必做） | **推荐**成功触觉（`CONFIRM` / `.success`） | 可选 | 用户最想知道「到底成没成」，双通道冗余合理 |
| 长按启动（录音/对讲） | 录音态 + 计时（必做） | `GESTURE_START` + 结束时 `GESTURE_END` | 可选「开始/停止」提示音 | 长按是隐形门槛，触觉告诉用户「已经触发」 |
| 拖拽越过阈值（吸附件、排序落位） | 高亮/占位（必做） | `GESTURE_THRESHOLD_ACTIVATE` | 不加 | 触觉是「到位了」的唯一即时信号 |
| 滑块经过刻度 | 数值（必做） | `SEGMENT_TICK`（仅离散档位，不要连续） | 不加 | 连续拖动每秒几十次，加了就是噪音 |
| 扫码 / 扫脸成功 | 结果（必做） | 成功触觉 | 可选「叮」 | 用户常常不看屏幕（举着手机对准） |
| 支付/转账完成 | 结果页 + 金额（必做） | 成功触觉 | **建议**（收银场景外放） | 金额相关，多一条通道降低误判 |
| 后台任务完成（导出/上传） | 进度 → 完成态 | 仅应用在前台时 | 可选 | 用户可能已离开，应走通知（见 `notifications-messaging.md`） |
| 游戏 / 空间应用 | 主体（必做） | 一等通道 | 一等通道 | HIG 明确 *"Augment audio cues with visual cues."*（离屏内容） |
| 无障碍替代（读屏、听觉障碍） | 必须有 | **必须与声音配对** | 必须可关 | Apple 原文 *"Use haptics in addition to audio cues."*（§7.2） |

### 1.3 四条「不加」的拒绝条件

1. **冗余拒绝**：视觉已经给了同等信息、且没有时压 → 加了只是重复（例：列表滚动、页面切换、hover）。
2. **打断拒绝**：会外放、会打断他人、会盖住读屏语音 → 声音出局，触觉可留（WCAG 原文 *"Individuals who use screen reading software can find it hard to hear the speech output if there is other audio playing at the same time."*）。
3. **不可控拒绝**：做不出「关掉」的路径（例如 Web 上没做用户手势解锁、iOS 上用 Playback 类别无视静音开关）→ 先修可控性，再谈加反馈。
4. **语义挪用拒绝**：拿系统语义常量表达别的意思（用「错误」触觉表示「已完成」）→ HIG 原文：*"If the documented use case for a pattern doesn't make sense in your app or game, avoid using the pattern to mean something else."*

---

## §2 三通道分工：谁能承担什么

| 维度 | 视觉 | 触觉 | 声音 |
|---|---|---|---|
| 带宽 | 高（颜色/位置/文字/图标可叠加） | **低**（大致 2–3 个可分辨维度：有无、强度、节奏） | 中（音高/音色/节奏/时长） |
| 是否需要注视 | **是** | 否 | 否 |
| 延迟 | 一帧起（16.7ms） | 极低（系统级反馈几乎即时） | 低（受音频输出链路影响，Web 上还受解锁状态影响） |
| 能否被用户关闭 | 靠对比度/字号，不可「关」 | 系统「触感反馈」开关 + 应用内开关 | 静音开关/音量/应用内开关 |
| 主要失败模式 | 被遮挡、被忽略、看不到（离屏） | 设备无马达 / 马达太弱 / 过度使用变噪音 | 外放尴尬、被静音、被 autoplay 策略拦截、与读屏语音打架 |
| 承载的信息 | **为什么、接下来怎么办**（解释与引导） | **发生了**（确认/到位/失败） | **什么发生了**（区分类型） |

**一句话记忆**：触觉回答「发生了没有」，声音回答「是哪一种」，视觉回答「为什么」。三者的错误用法是让触觉去解释、让声音去引导、让视觉去承担「来不及看」的场景。

**通道不是越多越好**：HIG *"Prefer using haptics to complement other feedback in your app or game."* 的下一句是 *"When visual, auditory, and tactile feedback are in harmony — as they generally are in the physical world — the user experience is more coherent and can seem more natural."*——关键词是 **complement（互补）**，不是 **duplicate（重复）**。

---

## §3 触觉的语义层：能借系统常量就别自造

### 3.1 四层选择顺序（自上而下，命中即停）

1. **系统标准控件自带的触觉**——列表滚动、键盘、开关、滑块、长按菜单。**你不要再加一次**，否则就是「双震」，用户会觉得设备坏了。
2. **系统语义常量**——点击 / 成功 / 失败 / 切换 / 阈值 / 长按。iOS 用 `UIFeedbackGenerator` 子类，Android 用 `HapticFeedbackConstants`，watchOS 用 `WKHapticType`。
3. **自定义模式**——只有系统确实没有对应语义时（例：游戏里的「蓄力满格」、自家品牌的一次「盖章」），才用 transient/continuous + intensity/sharpness 自建。
4. **降级**——设备没有马达、用户关了系统触感、应用内开关关闭。此时**静默跳过，不能把信息只放在触觉里**。

### 3.2 iOS：`UIFeedbackGenerator` 三类

| 语义 | 生成器 | 用在什么事件 | 官方原话（HIG `playing-haptics`） |
|---|---|---|---|
| 成功 | `UINotificationFeedbackGenerator.notificationOccurred(.success)` | 提交成功、付款完成、扫码成功 | "Indicates that a task or action has completed." |
| 警告 / 错误 | 同上 `.warning` / `.error` | 校验失败、余额不足、权限被拒 | HIG 只列类型名（Warning / Error），未给单句描述——**不要替 Apple 补定义** |
| 物理冲击 | `UIImpactFeedbackGenerator(style:)`：Light / Medium / Heavy / Rigid / Soft | 拖拽落位、元素碰撞、越过阈值 | HIG 只给强度序列，未给毫秒值 |
| 选择变化 | `UISelectionFeedbackGenerator.selectionChanged()` | 滚轮刻度、分段切换、取色器 | "Indicates that a UI element's values are changing." |

**iOS 的关键现实**：HIG 通篇**没有任何毫秒数**（`playing-haptics` 全页无 ms 数值，已逐段核对）。所以「iOS 轻触 = 10ms」这类说法都是二手推测，**写进设计规范就是臆造**。iOS 的正确做法是选语义、不调参数；参数由系统按设备与 Taptic Engine 能力决定。

watchOS 九种 `WKHapticType`（HIG 原文列名）：`.notification`（提醒）、`.directionUp` / `.directionDown`（数值增减）、`.success`、`.failure`、`.retry`（需要重试）、`.start` / `.stop`（开始/结束）、`.click`（选择/滚动刻度）。HIG 对 `.click` 的警告原文：*"Overusing the click haptic tends to diminish its utility and can even be confusing when clicks overlap each other."*

macOS 三种（`NSHapticFeedbackPerformer`）：Alignment（对齐/吸附）、Level change（数值跨档）、Generic（通用确认）。

### 3.3 Android：`HapticFeedbackConstants` 常量表（逐条核自 AOSP）

| 常量 | 值 | 语义（源码注释） | 建议场景 |
|---|---|---|---|
| `NO_HAPTICS` | -1 | 不震 | 显式关闭 |
| `LONG_PRESS` | 0 | "long press on an object that is resulting in an action being performed" | 长按触发菜单/录音 |
| `VIRTUAL_KEY` | 1 | 虚拟按键按下 | 键盘、数字键盘 |
| `KEYBOARD_TAP` | 3 | 键盘敲击 | 软键盘 |
| `CLOCK_TICK` | 4 | 时钟/计时刻度 | 计时器刻度 |
| `CONTEXT_CLICK` | 6 | 上下文点击（长按菜单项） | 菜单项选中 |
| `KEYBOARD_RELEASE` | 7 | 键盘抬起 | 一般不用（系统已给） |
| `VIRTUAL_KEY_RELEASE` | 8 | 虚拟按键抬起 | 一般不用 |
| `TEXT_HANDLE_MOVE` | 9 | 文本选择手柄移动 | 选中手柄拖拽 |
| `GESTURE_START` | 12 | 手势开始 | 长按启动录音、拖拽开始 |
| `GESTURE_END` | 13 | 手势结束 | 录音结束、拖拽结束 |
| `CONFIRM` | 16 | "signal the confirmation or successful completion of a user interaction" | 提交成功、确认 |
| `REJECT` | 17 | "rejection or failure" | 校验失败、操作被拒 |
| `TOGGLE_ON` | 21 | 开关打开 | Switch 开启 |
| `TOGGLE_OFF` | 22 | 开关关闭 | Switch 关闭 |
| `GESTURE_THRESHOLD_ACTIVATE` | 23 | 越过激活阈值 | 拖拽吸附、滑动删除越过阈值 |
| `GESTURE_THRESHOLD_DEACTIVATE` | 24 | 退回阈值以下 | 取消吸附（**多数场景不要用**，避免抖动） |
| `DRAG_START` | 25 | 拖拽开始 | 长列表重排 |
| `SEGMENT_TICK` | 26 | 分段刻度经过 | 滑块/滚轮档位 |
| `SEGMENT_FREQUENT_TICK` | 27 | 快速连续刻度 | 只给「持续拨动」场景，且只在设备能给出极轻震时 |

`SEGMENT_FREQUENT_TICK` 的原话值得逐字记住：*"expected to be very soft, so as not to be uncomfortable when performed a lot in quick succession. If the device can't make a suitably soft vibration, then it may not make any vibration."*——即平台自己也承认「给不出够轻的震就干脆不震」。

**编号不连续**：2 / 5 / 10 / 11 / 14 / 15 / 18 / 19 / 20 在公开 SDK 不可见（`@hide` 或历史常量，如 11 `DRAG_CROSSING`、18–20 `SCROLL_TICK` / `SCROLL_ITEM_FOCUS` / `SCROLL_LIMIT`）。**因此永远不要按编号推断语义，只用常量名。**

上表 20 行 **不是全部公开名**：`KEYBOARD_PRESS` 在 AOSP 源码里直接写成 `public static final int KEYBOARD_PRESS = KEYBOARD_TAP;`（同值别名，源码 2026-11-14 复核），所以公开常量名共 **21 个**（19 个独立值 + 该别名 + `NO_HAPTICS`）；`FLAG_IGNORE_VIEW_SETTING` / `FLAG_IGNORE_GLOBAL_SETTING` 是传入 `performHapticFeedback` 的**标志位**，不是触觉语义，不要当第 22、23 个效果用。

### 3.4 一致性：一种事件只能有一种触觉

HIG 原文：*"Use haptics consistently throughout your app or game."* 并补了一句判据：*"If a haptic doesn't reinforce a cause-and-effect relationship, it can be confusing and seem gratuitous."*

可执行的验收写法：

- 全应用**最多 5 种**触觉语义（成功 / 失败 / 切换 / 阈值 / 长按），多一种就要写理由。
- 同一事件在**所有页面**用同一种；同一页面里「保存成功」和「删除成功」不要给两种不同触觉（除非删除是破坏性、需要在确认对话框里区分）。
- 触觉**只跟因果关系绑定**：用户做了什么 → 发生了什么。不能因为「后台数据到了」就震（那是通知的事，见 §6 与 `notifications-messaging.md`）。

### 3.5 禁用清单（比「该用什么」更重要）

1. **高频重复**：滚动、输入、hover、每秒多次的刻度 → 不震（`SEGMENT_FREQUENT_TICK` 只在能给出极轻震时可用）。
2. **系统已有**：列表滚动到边界、键盘、系统开关 → 不重复加。
3. **无因果**：加载中动画、自动轮播、随机奖励 → 不震。
4. **长触觉**：HIG 原文 *"In most apps, prefer playing short haptics that complement discrete events."*，长触觉 *"can dilute the meaning of the feedback and distract people from their task"*。
5. **与动画不同步**：HIG 要求触觉与动画的强度/锐度一致（*"you generally want to match the intensity and sharpness of a haptic with the intensity and sharpness of the animation it accompanies."*）——动画很轻、触觉很重，就是「廉价感」的来源。
6. **打扰他人硬件的**：HIG 提醒 *"Be aware that playing haptics might impact other user experiences."*（麦克风、相机、陀螺仪场景，如录音、拍视频）。

---

## §4 触觉的数值与实现

### 4.1 Android `VibrationEffect` 精确值（源码逐条）

| 参数 | 合法取值 | 后果 / 原文 |
|---|---|---|
| `createOneShot(ms, amplitude)` 的 `ms` | 正整数 | "This must be a positive number." |
| 同上 `amplitude` | **1–255**，或 `DEFAULT_AMPLITUDE`（= -1） | 0 非法：`IllegalArgumentException("amplitude must either be DEFAULT_AMPLITUDE, or between 1 and 255 inclusive (amplitude=0)")` |
| `createWaveform(timings, amplitudes, repeat)` 的 `amplitudes` | **0–255**，或 `DEFAULT_AMPLITUDE` | "An amplitude value of 0 implies the motor is off." |
| 同上 `timings` | 毫秒，0 值对被忽略 | "Timing values of 0 will cause the pair to be ignored." |
| 同上 `repeat` | -1 = 不重复；≥0 = 从该索引循环 | 循环会 "played indefinitely and should be cancelled via Vibrator#cancel()" |
| 单次反馈时长上限（源码注释） | **1000 ms** | `// If a vibration is playing for longer than 1s, it's probably not haptic feedback` |
| 组合段数上限（源码注释） | **3 段** | `// If a vibration is playing more than 3 constants, it's probably not haptic feedback` |
| 自定义包络强度/锐度 | **0.0–1.0** | "Supported intensity values guarantee sensitivity levels (SL) above 10 dB SL to ensure human perception." |
| 包络终止条件 | 必须结束于 intensity 0 | 否则 `IllegalStateException("Basic envelope effects must end at a zero intensity control point.")` |
| 包络控制点数 | 建议 **≤16** | "it's recommended to limit the number of control points to a maximum of 16" |

**注意来源层级**：1000 ms 与 3 段是 AOSP **源码注释里的工程判断**，不是强制校验——写判定标准时可以当「平台自己认为的上限」，但不能说成「Android 规定不得超过」；包络 API 属 flagged API，公开 SDK 未必可用。

### 4.2 时长与强度的裁决（本文口径，可校准）

| 场景 | 建议时长 | 建议强度 | 理由 |
|---|---|---|---|
| 点按确认（离散事件） | 10–50 ms 等价的「一次点击」 | 轻 | 超过这个量级就接近「震一下」，会被当成通知 |
| 成功确认 | 两次极短轻触（节奏 1-2） | 中轻 | 用节奏区分「完成」而非「错误」 |
| 失败/拒绝 | 一次中重触（可加第二次短触） | 中重 | 错误必须比成功更有「阻力感」 |
| 越过阈值 | 一次轻触，**只响一次** | 轻 | 抖动会让用户以为设备故障 |
| 连续动作（录音/拖动） | 随动作持续，结束即停 | 极轻 | 必须是 continuous，且时长无固定值 |

**三条硬性验收**：

1. 单次离散事件 ≤ 1000 ms（AOSP 注释口径），且**理想 ≤ 100 ms**。
2. 组合段数 ≤ 3；超过 3 段请改用「声音 + 视觉」。
3. 触觉必须在事件**发生的那一刻**触发（同一帧内），延迟到动画结束就失去意义。

### 4.3 Web：`navigator.vibrate()` 的真实限制

`Vibration` API 的数值规则（W3C `https://www.w3.org/TR/vibration/` 与 MDN 原文）：

| 规则 | 原文 / 数值 |
|---|---|
| 参数形态 | 单个毫秒数，或 `[振, 停, 振, …]` 交替数组 |
| 数组语义 | 偶数位=振动，奇数位=停顿（原文："… vibrate the device for time milliseconds. Otherwise wait for time milliseconds."） |
| 末尾停顿 | 不必写："you don't have to provide a pause as your last entry since the vibration automatically stops at the end of each vibration period." |
| 取消 | `navigator.vibrate(0)`、空数组、全 0 数组 |
| 段数上限 | **10 段**（"Let max length have the value 10."，超出截断） |
| 单段上限 | **10000 ms**（"Let max duration have the value 10000."，超出按 10000 处理） |
| 激活要求 | **必须 sticky activation**（"If global does not have sticky activation, return false and terminate these steps."；MDN："Sticky user activation is required."） |
| 可见性 | 文档不可见时直接返回 false；页面切到后台会中止正在跑的模式 |
| 速率限制 | 规范 SHOULD 级建议（"The user agent SHOULD employ global rate limiting to restrict the number of vibration requests"） |
| 浏览器支持 | **非 Baseline**：MDN 顶栏 *"Limited availability — This feature is not Baseline because it does not work in some of the most widely-used browsers."* |
| 用户设置 | MDN："Some devices may not vibrate if they are in Silent mode or Do Not Disturb (DND) mode." |

**裁决**：Web 触觉只能当**增强**，不能当唯一反馈——iOS Safari 上 `navigator.vibrate` 不存在，桌面浏览器普遍没有马达。任何「靠震动告诉用户成功了」的 Web 流程都必须在视觉上自洽。

### 4.4 系统设置不可绕过（硬证据）

- Android `HapticFeedbackConstants.FLAG_IGNORE_GLOBAL_SETTING` 已 `@Deprecated`，原文：*"Starting from TIRAMISU only privileged apps can ignore user settings for touch feedback."*
- `VibrationAttributes.FLAG_BYPASS_USER_VIBRATION_INTENSITY_OFF` 同样注明只有 privileged apps 能用。
- Apple HIG 的要求是反向的：*"Make haptics optional."*（"Let people turn off or mute haptics, and make sure people can still enjoy your app or game without them."）

**验收**：设置页必须有「触感反馈」开关；关闭后所有触觉静默跳过，且**不丢失任何信息**（信息必须在视觉或声音里还有一份）。

### 4.5 跨端语义映射表（写设计稿时直接抄）

| 事件 | iOS | Android | watchOS | Web |
|---|---|---|---|---|
| 普通点按 | 不需要（系统控件自带） | `VIRTUAL_KEY` | `.click` | 不需要 |
| 开关打开 | `UISelectionFeedbackGenerator` 或自定义轻触 | `TOGGLE_ON` | `.click` | `vibrate(10)`（仅增强） |
| 开关关闭 | 同上 | `TOGGLE_OFF` | `.click` | 同上 |
| 选择/刻度变化 | `.selectionChanged()` | `SEGMENT_TICK` | `.directionUp/Down` | `vibrate(8)`（仅增强） |
| 越过阈值 | `UIImpactFeedbackGenerator(.light)` | `GESTURE_THRESHOLD_ACTIVATE` | `.start` | `vibrate(15)`（仅增强） |
| 长按开始 | `UIImpactFeedbackGenerator(.medium)` | `GESTURE_START` / `LONG_PRESS` | `.start` | `vibrate(20)` |
| 成功 | `notificationOccurred(.success)` | `CONFIRM` | `.success` | `vibrate([10,40,10])` |
| 失败/拒绝 | `notificationOccurred(.error)` | `REJECT` | `.failure` | `vibrate([20,60,20])` |

### 4.6 官方指南给的调参数值（`developer.android.com`，2026-10-26 版）

| 调参项 | 官方数值 / 原文 | 设计含义 |
|---|---|---|
| Composition 原语常量 | `PRIMITIVE_CLICK=1`、`THUD=2`、`SPIN=3`、`QUICK_RISE=4`、`SLOW_RISE=5`、`QUICK_FALL=6`、`TICK=7`、`LOW_TICK=8`（CLICK / QUICK_FALL / QUICK_RISE / SLOW_RISE / TICK 为 **API 30**；THUD / SPIN / LOW_TICK 为 **API 31**） | 常量值不连续，**别按编号猜语义**；旧设备只保证 API 30 那一批 |
| 原语缩放 | "value is between 0.0f and 1.0f inclusive"；"0 actually maps to a minimum amplitude at which this primitive can be (barely) felt" | 0 不是「关」，是「刚好能感觉到」——要静音就别调用 |
| 强度分档 | "create strength ratios of 1.4 or more"；"Don't try to create more than three intensity levels … because they aren't perceptually distinct"；示例 scales `0.5 / 0.7 / 1.0` | 同一原语最多三档，相邻档强度比 ≥1.4 |
| 两段间隔 | "a 5 to 10 ms gap between two primitives is too short to be detectable"；"Use a gap on the order of 50 ms or longer if you want to create a discernible gap" | 想做「嗒—嗒」必须 ≥50 ms；<10 ms 等于连击 |
| 事件排布漂移 | "allow sufficient time (e.g. 50 ms or more) between consecutive haptic events" | 过密事件会被框架顺移，节奏走样 |
| spin 间隔 | 0 ms = "tight spinning sensation"；10→50 ms = "looser"；">100 ms … begin to feel like individual effects" | 旋转/惯性类效果的可控区间 **0–100 ms** |
| 包络控制点 | "minimum duration of 20 ms between control points and at least 16 points for envelope effects"；"envelope effects must start and end with an intensity of 0.0" | 长触觉（ramp）最小可分辨步长 20 ms；起止必须归零 |
| 预设缩放 | "Presets can be scaled from 0.0f to 1.0f" | 与原语同一套三档上限 |
| 无振幅控制设备 | "Non-zero amplitude values are rounded up to 100%"；"all amplitude values will map to off or on based on whether they are zero or non-zero" | 低端机上 0.3 与 1.0 一样响——**强度分级不可依赖** |
| one-shot / waveform 语义 | "A one-shot pattern refers to vibrating once for N milliseconds."；"The timings start with the duration spent off." | waveform 首值是「先停」，写 `[0, 20]` 才是立刻振 20 ms |
| 权限与后台 | "your app must declare the VIBRATE permission"；后台振动须给 attentional usage（notification / ringtone / alarm） | 后台「完成震动」不成立，改发通知 |
| Builder 校验 | 元素 startTime 必须非降序；"best-effort validation … (such as 1 ms for presets)"，重叠抛 `IllegalArgumentException`；播放时自动顺移到下一空位 | 交付写绝对时间线，别靠相对延时层层叠加 |
| 版本优选 | Android 16（26Q4）起 `VibrationEffect.Builder` 首选；`Composition` 自 Android 11 保留但**无自动回退**（一个原语不支持则整段不响） | 跨设备可用性：Builder > Composition |

来源：`https://developer.android.com/develop/ui/views/haptics/haptics-apis`（同批还有 `custom-haptic-effects` 与 `reference/android/os/VibrationEffect.Composition` 两页；均 2026-10-26 抓取）。

**裁决（可直接写进设计文档）**：设计稿只写三件事——**用哪个原语（常量名）／强度档（≤3 档、相邻比 ≥1.4）／与上一段的间隔（≥50 ms 才可分辨）**；毫秒级波形交给平台预设，不要自己编 ms 数。

---

## §5 声音：能不能响、响给谁听、被谁打断

### 5.1 先选音频类别，再谈音色（iOS）

`playing-audio` 的类别表是本文最硬的裁决依据（原文逐字）：

| 类别 | 描述 | 对静音开关的响应 | 与其他音频混音 | 后台播放 |
|---|---|---|---|---|
| Solo ambient | "Sound isn't essential, but it silences other audio." | **响应**（静音即静） | 不混音 | 不可 |
| Ambient | "Sound isn't essential, and it doesn't silence other audio." | **响应** | 混音 | 不可 |
| Playback | "Sound is essential and might mix with other audio." | **不响应** | 可能混音 | 可 |
| Record | "Sound is recorded." | 不响应 | 不混音 | 可（录音） |
| Play and record | 录制并播放 | 不响应 | 可能混音 | 可 |

**裁决**：**UI 音效必须落在 Ambient / Solo ambient 一侧**。用 Playback 播「叮」的后果是：用户在会议里把手机静音了，你的 App 还是会响——这不是「体验问题」，是违背平台契约，也是 App Store 审核里常见的「无视静音开关」投诉来源。

HIG 同页的 **Silence** 段说明了原因："People switch a device to silent when they want to avoid being interrupted by unexpected sounds like ringtones and incoming message tones. In this scenario, they also want to silence nonessential sounds, such as keyboard clicks, sound effects, game soundtracks, and other audible feedback. When a device is in silent mode, it plays only the audio that people explicitly initiate, like media playback, alarms, and audio/video messaging."

### 5.2 短音效不要自建播放器

HIG（iOS/iPadOS）：*"Use the system's sound services to play short sounds and vibrations."*（AudioToolbox 的 audio services）——为一声 80ms 的「叮」加载一个 `AVAudioPlayer`，在低端设备上就是卡顿与延迟的来源。

需要同时满足「短、低延迟、可并发」时，iOS 侧用系统音效服务；跨端需要自定义音色时，Web 侧用预解码的 `AudioBuffer`（见 §5.5）。

### 5.3 打断、耳机与恢复

- 播放临时音效结束要还回去：HIG *"Let other apps know when your app finishes playing temporary audio."*（`notifyOthersOnDeactivation`），否则用户的播客会被永久压低。
- 耳机拔出：HIG 要求 *"playback to pause immediately"*；重新插入自动改道。
- 被打断（来电、闹钟、其他 App 抢占）：区分 resumable / nonresumable，恢复与否用 `shouldResume` 决定——**设计稿里要写「被打断后是否自动继续」**，这是产品决策不是实现细节。
- HIG 三条音量纪律："Adjust levels automatically when necessary — don't adjust the overall volume."；"Permit rerouting of audio when possible."；"Avoid repurposing audio controls."（别把音量键改成别的功能）。

### 5.4 Android 的声音属性

音效走 sonification 语义，而不是媒体语义：`AudioAttributes` 的 `USAGE_ASSISTANCE_SONIFICATION` + `CONTENT_TYPE_SONIFICATION`。系统据此决定音量通道（铃声/媒体/通话）与是否该被「勿扰」拦截。这与触觉侧的映射一致——AOSP 明确把 `USAGE_TOUCH` 触觉映射到 `USAGE_ASSISTANCE_SONIFICATION`，**说明平台认为「触觉反馈」与「界面音效」是同一类打扰级别**。

播放短音效时申请**短暂焦点**（`AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK` 一类），让媒体自动压低，播完立刻释放；不要申请长期焦点，那会让用户的音乐停掉。

### 5.5 Web：autoplay 是硬墙，不是建议

MDN《Autoplay guide》原文列出了「允许自动播放」的四种情形：

1. *"The audio is muted or its volume is set to 0"*
2. *"The user has interacted with the site (by clicking, tapping, pressing keys, etc.)"*
3. *"If the site has been allowlisted"*
4. *"If the autoplay Permissions Policy is used to grant autoplay support to an `<iframe>` and its document."*

且 *"playback of any media that includes audio is generally blocked if the playback is programmatically initiated in a tab which has not yet had any user interaction."*；*"Autoplay blocking is not applied to `<video>` elements when the source media does not have an audio track, or if the audio track is muted. Media with an active audio track are considered to be audible, and autoplay blocking applies to them."*

工程上要做的三件事：

1. **查策略**：`navigator.getAutoplayPolicy("mediaelement")` / `("audiocontext")`，返回 `"allowed"` / `"allowed-muted"` / `"disallowed"`；页面加载时查一次即可（没有 change 事件）。
2. **接住失败**：`play()` 返回 Promise，被拒时抛 `NotAllowedError`（MDN：*"If the user agent is configured not to allow automatic or script-initiated playback of media, calling `play()` will cause the returned promise to be immediately rejected with a `NotAllowedError`."*）。**不要假设会响**，失败要静默降级或改成「点击开启声音」。
3. **解锁 AudioContext**：页面加载即创建的 `AudioContext` 处于 `suspended`，必须在用户手势后 `resume()`；MDN 原文：*"If an `AudioContext` is created before the document receives a user gesture, it will be created in the "suspended" state, and you will need to call `resume()` after the user gesture."* 状态除 `running` / `suspended` / `closed` 外还有 `interrupted`（*"The audio context has been interrupted by an occurrence outside of the control of the web app."*，触发条件各浏览器不同）。

Safari/WebKit 的额外纪律（原文）：*"Websites should assume any use of `<video>` or `<audio>` requires a user gesture click to play. It's important to detect if auto-play was denied, since users now have the ability to turn off all forms of auto-play, including silent videos."* 以及 *"Remember that audio tracks that render silence are still audio tracks, and their existence affects whether a video will auto-play at all."*

### 5.6 earcon 还是听觉图标（auditory icon）

| | **earcon（抽象音）** | **听觉图标（拟声）** |
|---|---|---|
| 定义 | 与语义无现实对应关系的抽象音（如「成功=上行三音」） | 模仿现实声音（如「删除=纸张撕裂」） |
| 学习成本 | 需要学习，但学会后跨场景通用 | 通常零学习 |
| 文化/场景风险 | 低（无现实联想） | 高（拟声可能不雅、可能引起误解） |
| 适用 | 高频、同类事件、需要「品牌感」 | 低频、强隐喻、游戏 |

**生态现实（GitHub API 实测）**：搜索 `earcon` 全站只有 **38** 个仓库，最大的 UI 用途库是 `smolgroot/earcons`（7★，MIT，纯 Web Audio、不带音频文件）——**没有成熟的 earcon 库可用，只有原语**。搜索 `"web audio"` 共 11,187 个仓库，前 10 全是音乐制作/播放/录音/DSP，没有一个是 UI 反馈库。真正可用的通用播放层是 `howler.js`（25,444★ MIT）、React 侧 `use-sound`（3,163★ MIT）。

**裁决**：一套 UI 声音**最多 3–5 个 earcon**（成功 / 失败 / 提醒 / 切换），超出就退化成噪音；不要指望现成音库，音高与节奏必须自己定义并写进规范。

### 5.7 声音句法（裁决值，可校准）

| 语义 | 音高走向 | 时长 | 说明 |
|---|---|---|---|
| 成功 | **上行**（如 大二度 / 大三度） | 80–200 ms | 上行=完成、打开、向上 |
| 失败 / 拒绝 | **下行**（小二度或大三度下行） | 100–250 ms | 下行=关闭、错误 |
| 提醒 / 注意 | 同音重复两次 | 每声 60–100 ms，间隔 ≥120 ms | 不升不降，只抢注意力 |
| 切换 / 选中 | 单声短音 | 40–80 ms | 越短越不烦 |
| 起始 / 结束（录音） | 低→高 / 高→低 | 60–120 ms | 与视觉的「开始/结束」一致 |

三条硬规则：

1. **同一语义在所有页面用同一个音**；同一页面里两个不同音必须对应两个不同语义。
2. **音高变化方向必须与语义方向一致**（成功上行、失败下行）；反过来会让人反复误判。
3. **绝不叠加**：两个音效间隔 < 120 ms 会糊成一个怪音；连续事件（如批量删除）要做**节流**（例如 300 ms 内只响一次，其余静默）。

### 5.8 音频资源工程

| 约束 | 建议值 | 原因 |
|---|---|---|
| 单文件体积 | ≤ 50 KB | 首屏要预解码，越大越慢 |
| 声道 | 单声道 | UI 音效不需要立体声，省一半体积 |
| 采样率 | 44.1 kHz 或 22.05 kHz | 短音效 22.05 kHz 足够且更小 |
| 编码 | iOS/Android 原生侧短音效优先无损/低延迟格式；Web 侧优先 `AudioBuffer` 预解码 | Web 上 `decodeAudioData` 一次，之后零延迟触发 |
| 复用 | **全站一个 `AudioContext`** | 每个音效新建上下文会被浏览器限制数量并增加延迟 |
| 预加载 | 用户第一次交互时解锁 + 预解码全部 UI 音效 | 首次触发的延迟最容易被听出来 |

### 5.9 声音的三条法律级红线

1. **不能自动播放超过 3 秒且无控制**：WCAG 1.4.2（§7.1 全文）。
2. **不能只用声音传达重要信息**：Apple visionOS 原文 *"avoid communicating important information using only sound. Always provide additional ways to help people understand your app."*
3. **不能让声音盖住读屏语音**：WCAG 原文 *"Individuals who use screen reading software can find it hard to hear the speech output if there is other audio playing at the same time."*——所以「读屏开启时自动静音装饰性音效」不是可选项，是正确性要求。

---

## §6 三通道配方表（设计交付时直接填）

| # | 事件 | 视觉（必做） | 触觉 | 声音 | 频率 | 全部关闭后还剩什么 |
|---|---|---|---|---|---|---|
| 1 | 主按钮点按 | 按下态 → 提交态 | 系统自带，不加 | 不加 | 极高频 | 视觉状态 |
| 2 | 表单校验失败 | 字段红框 + 错误文案 + 滚动到首个错误 | `REJECT` / `.error` | 长表单可选一次「下行」 | 中 | 红框与文案 |
| 3 | 提交成功（不可逆） | 结果页 + 关键信息 | `CONFIRM` / `.success` | 可选「上行」 | 中 | 结果页 |
| 4 | 破坏性操作确认 | 二次确认对话框 + 危险色 | 确认时 `CONFIRM`，取消时轻触 | 可选「下行」 | 低 | 对话框 |
| 5 | 长按启动录音 | 录音态 + 计时 + 波形 | `GESTURE_START` | 起止各一声 | 低 | 波形与计时 |
| 6 | 拖拽越过吸附阈值 | 高亮槽位 + 磁吸动画 | `GESTURE_THRESHOLD_ACTIVATE`（仅一次） | 不加 | 中 | 槽位高亮 |
| 7 | 滑块/滚轮刻度 | 当前值 + 刻度标尺 | `SEGMENT_TICK`（仅离散档位，连续拖动不加） | 不加 | 中 | 数值 |
| 8 | 扫码/扫脸成功 | 结果态 + 打勾动画 | `.success` | 可选「叮」 | 中 | 结果态 |
| 9 | 支付完成 | 金额 + 收款方 + 成功态 | `.success` | 建议（收银场景） | 低 | 金额页 |
| 10 | 后台任务完成 | 进度 → 完成，或推送 | 仅前台时轻触 | 可选 | 低 | 通知 |
| 11 | 列表到达底部 | 「没有更多了」 | 不加 | 不加 | 高频 | 文案 |
| 12 | 游戏/空间交互 | 主体视觉 | 一等通道 | 一等通道 | 高 | 视觉（必须够用） |

**用法**：先用 §1 五问判层确定「要不要非视觉通道」，再用本表填「用哪一条、什么参数」，最后用 §9 自检清单与 §7 可访问性复验。任何一格写「无」的地方都要能回答：**如果这一格是空的，用户会不会漏掉信息？**

---

## §7 可访问性：这是硬约束，不是「关怀选项」

### 7.1 WCAG 2.2 SC 1.4.2 Audio Control（Level A，逐字）

> "If any audio on a web page plays automatically for more than 3 seconds, either a mechanism is available to pause or stop the audio, or a mechanism is available to control audio volume independently from the overall system volume level."

理解文档（Understanding 1.4.2）里的三条关键原文：

- "In the context of this success criterion, "plays automatically" broadly refers to audio that is not started/played as a direct result of a user's intentional activation."
- "Having control of the volume includes being able to reduce its volume to zero. **Muting the system volume is not "pausing or stopping" the autoplay audio.** Both the "pause or stop" and control of audio volume need to be independent of the overall system volume."
- "Individuals who use screen reading software can find it hard to hear the speech output if there is other audio playing at the same time."

充分技术与失败例：G60（3 秒内自动关）、G170（页面开头提供关闭控件）、G171（只在用户请求时播放）；F23（超过 3 秒且无法关闭）、F93（自动播放的 HTML5 媒体没有暂停/停止方式）。

**判层结论**：一条自动播放的 80 ms 音效**不触发** 1.4.2（< 3 秒）；但背景音乐、环境音、循环音效一旦超过 3 秒，就必须给「独立于系统音量」的控制，否则直接不通过。「静音系统音量」不算通过。

### 7.2 WCAG 2.2 SC 1.4.7 Low or No Background Audio（Level AA，适用于预录纯音频内容）

原文条件（三条满足其一即可）："The audio does not contain background sounds." / "The background sounds can be turned off." / "20 dB — The background sounds are at least 20 decibels lower than the foreground speech content, with the exception of occasional sounds that last for only one or two seconds."

判据：**20 dB ≈ 背景音约为前景语音的 1/4 响度**（Understanding 注："approximately four times quieter"）。如果 App 有语音播报（读屏、导航、健身教练），音效必须 ≥20 dB 低于语音，否则就是「盖住说话」。

### 7.3 声音不能是唯一通道（三处官方原文）

1. Apple HIG `accessibility`：*"Use haptics in addition to audio cues."*（"If your interface conveys information through audio cues — such as a success chime, error sound, or game feedback — consider pairing that sound with matching haptics for people who can't perceive the audio or have their audio turned off."）
2. Apple HIG `accessibility`：*"Augment audio cues with visual cues."*（"This is especially important for games and spatial apps where important content might be taking place off screen."）
3. Apple HIG `playing-audio`（visionOS Important）：*"In visionOS, as in every platform, avoid communicating important information using only sound. Always provide additional ways to help people understand your app."*

还有一条常被忽略：*"It's important that dialogue and crucial information about your app or game isn't communicated through audio alone."*，并要求提供 Captions / Subtitles / Audio descriptions / Transcripts 四类文本替代。

**推论**：声音与触觉**都必须有视觉的等价物**；反过来，视觉也应有触觉/声音的等价物（HIG 那句 *"in addition to"* 的意思是「配对」，不是「声音优先、触觉补充」）。

### 7.4 可关闭性矩阵（验收用）

| 用户 | 声音偏好 | 触觉偏好 | 你的界面必须做到 |
|---|---|---|---|
| 聋 / 重听 | 无法感知 | 可感知（可能更强） | 声音信息必须有视觉；**有声音的地方配触觉** |
| 盲 / 低视力 | 依赖读屏语音 | 可感知 | 触觉不能替代文字；读屏时**静音装饰性音效**否则盖住语音 |
| 听障 + 视障（聋盲） | 无法感知 | 可感知 | 只剩触觉 + 盲文/震动编码；此时触觉**必须**承载语义，不能只是「轻点」 |
| 前庭敏感 / 听觉过敏 | 需要可预测 | 可能需要关闭 | 无突发大音量、无随机触觉、有总开关 |
| 公共场合用户 | 静音开关常开 | 常开 | 音频类别必须响应静音开关（§5.1） |

### 7.5 没有「减少声音」的系统偏好——必须自己做开关

- CSS 只有 `prefers-reduced-motion`（管动效）、`prefers-reduced-transparency`、`prefers-contrast`、`prefers-reduced-data`、`prefers-color-scheme`；**没有 `prefers-reduced-sound`**（MDN 无此页面，404；`@media` 特性索引里也没有声音类 `prefers-*`）。
- 所以「跟随系统减少声音」在 Web 与 App 都没有平台级开关可用，**必须在设置里给应用内开关**（这也是 HIG *"Make haptics optional."* 的落点）。

### 7.6 触觉不是无障碍的「升级」，而是另一条通道

常见错误：加了震动就以为照顾了视障用户。事实上视障用户主要靠**读屏语音**（声音）与**盲文/手势**，震动只是辅助；而听障用户才更需要震动。因此触觉标签要写成「这是给听不见的用户的信息通道」，而不是「无障碍优化已完成」。

---

## §8 反模式（看到就该打回）

1. **双震**：系统控件已给触觉，自己又加一次。
2. **震动雨**：滚动、输入、hover 每秒多次触发。
3. **成功音用下行、失败音用上行**（或同一音效表示两种语义）。
4. **用 Playback 类别播 UI 音效**：静音开关失效。
5. **把声音当唯一反馈**：扫码成功只「叮」一声，不给打勾。
6. **自动播放背景音乐**且无控制（WCAG 1.4.2 直接失败）。
7. **音效盖住读屏语音**（1.4.7 的 20 dB 与「读屏可听」要求）。
8. **没有总开关**：设置里找不到「声音」与「触感」两项。
9. **无视系统设置**：靠私有 flag 绕过用户的触感关闭（非特权应用做不到，且违反 HIG）。
10. **用震动做「加载中」**：用户控制不了、也解释不了。
11. **震动与动画强度不匹配**：动画极轻、震动极重（HIG 明说要对齐 intensity/sharpness）。
12. **毫秒数值拍脑袋**：写「iOS 轻触 10ms」这类文档里查不到的数字。
13. **音效超过 3 秒且无关闭**：WCAG 1.4.2 失败。
14. **Web 上假设 `navigator.vibrate` 存在**：iOS Safari 没有，桌面也没有。
15. **autoplay 直接 `play()` 不接 Promise**：控制台一串 `NotAllowedError`，用户什么也没听到。
16. **每个音效新建 `AudioContext`**：延迟高、数量受限。
17. **音效文件 300 KB、立体声、48 kHz**：首屏卡顿，没必要。
18. **同一事件在不同端给不同语义**（iOS 成功触觉、Android 用 REJECT）。
19. **把触觉当通知**：后台数据到达就震，用户不知道发生了什么。
20. **没有降级路径**：设备无马达/静音/系统关闭时，流程卡住或信息丢失。

---

## §9 自检清单（交付前逐条打勾，20 条）

1. 每个非视觉反馈都能回答「它替代了用户哪个动作」吗？
2. 高频事件（滚动、输入、切换）是否一条触觉/声音都没加？
3. 系统标准控件自带的触觉是否被重复添加了？
4. 触觉语义是否全部映射到平台常量（iOS 生成器 / Android 常量 / watchOS 类型）？
5. 全应用触觉语义是否 ≤5 种、且同一事件只有一种？
6. 触觉是否在事件发生那一帧触发（不是动画结束）？
7. 单次离散触觉是否 ≤1000 ms、理想 ≤100 ms、段数 ≤3？
8. Android 振幅是否全部落在 1–255 或 `DEFAULT_AMPLITUDE`（0 只在 waveform 里表示关）？
9. Web 振动模式是否 ≤10 段、单段 ≤10000 ms、且是在用户手势之后调用？
10. 触觉与动画的强度/锐度是否匹配？
11. UI 音效的音频类别是否响应静音开关（Ambient / Solo ambient 一侧）？
12. 是否复用了唯一一个 `AudioContext` 并在用户手势后 `resume()`？
13. 是否检查了 autoplay 策略（`getAutoplayPolicy`），并接住了 `play()` 的 `NotAllowedError`？
14. 声音语义是否 ≤5 个、成功上行/失败下行、且没有叠音？
15. 是否存在自动播放超过 3 秒且无独立控制的音频（WCAG 1.4.2）？
16. 有语音播报时，音效是否比语音低 ≥20 dB（WCAG 1.4.7）？
17. 声音与触觉是否都有视觉等价物；关键信息是否不止一条通道？
18. 设置页是否有「声音」与「触感」两个独立开关，关闭后流程仍完整？
19. 是否会绕过系统静音/触感设置（不允许）？
20. 设备无马达、无扬声器、读屏开启、静音开启四种环境下，是否都验过一遍？

---

## §10 场景速查

| 你被问到的问题 | 翻到 |
|---|---|
| 「这个操作要不要加音效/震动？」 | §1 五问判层 + §1.2 判层表 |
| 「按钮点一下要不要震？」 | §3.1 第 1 层（系统自带，不加） |
| 「成功和失败分别用什么触觉？」 | §3.2 iOS / §3.3 Android 表 |
| 「震动应该多长、多强？」 | §4.1 精确值 + §4.2 裁决表 |
| 「Web 上能震动吗？可靠吗？」 | §4.3（非 Baseline、需 sticky activation） |
| 「用户静音了为什么还在响？」 | §5.1 音频类别表 |
| 「网页自动播放被拦了怎么办？」 | §5.5 策略检查 + Promise 拒绝 |
| 「提示音怎么设计？用现成的吗？」 | §5.6 earcon vs 听觉图标 + 生态现状、§5.7 音高句法 |
| 「怎么做无障碍验收？」 | §7 全节 + §9 第 15–19 条 |
| 「设计稿要交付什么？」 | §6 三通道配方表（每事件一行）+ §9 清单 |

---

## §11 可执行校验（以下代码已实跑通过）

用法：`python -I -X utf8 shf_check.py`。它做三件事：校验振动模式是否越过 W3C/Android 的硬边界、校验 Android 振幅合法性、校验 §6 配方表是否自相矛盾。

```python
# -*- coding: utf-8 -*-
"""sound-haptics-feedback.md §11 的可执行校验器（两条函数 + 自检示例）。

规则来源：
- Web Vibration API：W3C https://www.w3.org/TR/vibration/（max length 10、max duration 10000、偶数位=振动）
- Android VibrationEffect：振幅 1-255 或 DEFAULT_AMPLITUDE(-1)；源码注释 1s / 3 段
运行：python -I -X utf8 shf_check.py
"""

MAX_SEGMENTS_WEB = 10          # W3C：max length
MAX_ENTRY_MS = 10_000          # W3C：max duration
MAX_DISCRETE_MS = 1_000        # AOSP 注释：超过 1s 大概不是触觉反馈
MAX_DISCRETE_SEGMENTS = 3      # AOSP 注释：超过 3 段大概不是触觉反馈
AMP_MIN, AMP_MAX = 1, 255      # VibrationEffect.createOneShot 的振幅范围
DEFAULT_AMPLITUDE = -1         # VibrationEffect.DEFAULT_AMPLITUDE
HIGH_FREQ = {"极高频", "高频"}


def audit_web_pattern(pattern, event="离散事件"):
    """校验 Web Vibration 模式；返回 (verdict, errors, warnings)。偶数位=振动，奇数位=停顿。"""
    if isinstance(pattern, int):
        pattern = [pattern]
    errs, warns = [], []

    if not pattern:
        errs.append("空模式：至少需要一段振动")
    if len(pattern) > MAX_SEGMENTS_WEB:
        errs.append(f"段数 {len(pattern)} > W3C 上限 {MAX_SEGMENTS_WEB}，规范要求截断")

    for i, ms in enumerate(pattern):
        kind = "振动" if i % 2 == 0 else "停顿"
        if not isinstance(ms, int) or isinstance(ms, bool) or ms < 0:
            errs.append(f"第 {i + 1} 段（{kind}）{ms!r} 不是非负整数毫秒")
        elif ms > MAX_ENTRY_MS:
            errs.append(f"第 {i + 1} 段（{kind}）{ms} ms > W3C 上限 {MAX_ENTRY_MS} ms")

    vibrate = sum(m for i, m in enumerate(pattern) if i % 2 == 0 and isinstance(m, int) and m > 0)
    if vibrate > MAX_DISCRETE_MS:
        warns.append(f"振动总时长 {vibrate} ms > {MAX_DISCRETE_MS} ms：AOSP 注释认为这已不是触觉反馈")
    if len(pattern) > MAX_DISCRETE_SEGMENTS and event == "离散事件":
        warns.append(f"离散事件却用了 {len(pattern)} 段（AOSP 注释支持 ≤{MAX_DISCRETE_SEGMENTS} 段）")

    verdict = "FAIL" if errs else ("WARN" if warns else "PASS")
    return verdict, errs, warns


def audit_android_amplitudes(amplitudes):
    """校验 VibrationEffect 振幅：每个值必须 1-255 或 DEFAULT_AMPLITUDE(-1)；0 非法。"""
    errs = []
    for i, a in enumerate(amplitudes):
        if a == DEFAULT_AMPLITUDE:
            continue
        if not isinstance(a, int) or isinstance(a, bool) or not (AMP_MIN <= a <= AMP_MAX):
            errs.append(f"第 {i + 1} 个振幅 {a!r} 非法：必须 1-{AMP_MAX} 或 DEFAULT_AMPLITUDE({DEFAULT_AMPLITUDE})")
    return ("FAIL" if errs else "PASS"), errs


def audit_recipe(rows):
    """校验三通道配方表；rows 元素为 (事件, 视觉, 触觉, 声音, 频率档, 是否有时压)。"""
    problems = []
    for event, visual, haptic, sound, freq, urgent in rows:
        if not visual:
            problems.append(f"[{event}] 没有视觉通道：任何情况下视觉都是必做项")
        if freq in HIGH_FREQ and (haptic or sound):
            problems.append(f"[{event}] 高频事件却加了非视觉通道：会退化成噪音")
        if urgent and not haptic and not sound:
            problems.append(f"[{event}] 有时压却只有视觉：用户来不及看")
        if haptic and not sound and not visual:
            problems.append(f"[{event}] 触觉成了唯一通道：设备无马达即信息丢失")
    return problems


# §6 配方表（与文档同源，改文档时改这里）
RECIPE = [
    ("主按钮点按", True, False, False, "极高频", False),
    ("表单校验失败", True, True, False, "中", True),
    ("提交成功", True, True, True, "中", False),
    ("破坏性操作确认", True, True, True, "低", False),
    ("长按启动录音", True, True, True, "低", True),
    ("拖拽越过阈值", True, True, False, "中", True),
    ("滑块刻度", True, True, False, "中", False),  # 仅离散档位；连续拖动不加
    ("扫码成功", True, True, True, "中", True),
    ("支付完成", True, True, True, "低", False),
    ("后台任务完成", True, False, False, "低", False),
    ("列表到底", True, False, False, "高频", False),
    ("游戏交互", True, True, True, "高", True),
]

DEMO_PATTERNS = [
    ("成功确认", [10, 40, 10], "离散事件"),
    ("失败提示", [20, 60, 20], "离散事件"),
    ("合法长振动", [900], "离散事件"),
    ("五段组合", [10, 30, 10, 30, 10], "离散事件"),
    ("超长振动", [1500], "离散事件"),
    ("十一段", [10, 10] * 5 + [10], "离散事件"),
    ("含负数", [10, -5], "离散事件"),
]


def main():
    print("== 1. 振动模式校验 ==")
    for name, pattern, event in DEMO_PATTERNS:
        verdict, errs, warns = audit_web_pattern(pattern, event)
        detail = "; ".join(errs + warns) or "无问题"
        print(f"[{verdict}] {name} {pattern} -> {detail}")

    print("\n== 2. Android 振幅校验 ==")
    for amps in ([255], [DEFAULT_AMPLITUDE], [0], [256], [128, 0]):
        verdict, errs = audit_android_amplitudes(amps)
        print(f"[{verdict}] {amps} -> {'; '.join(errs) or '合法'}")

    print("\n== 3. 三通道配方校验 ==")
    problems = audit_recipe(RECIPE)
    if problems:
        for p in problems:
            print(f"[WARN] {p}")
    else:
        print(f"[PASS] {len(RECIPE)} 行配方全部通过：视觉必在、高频不带非视觉通道、时压有触觉兜底")

    bad = [("列表到底", True, True, False, "高频", False)]
    bad_problems = audit_recipe(bad)
    print(f"[自检] 故意违规的行被拦下：{bool(bad_problems)} -> {bad_problems[0] if bad_problems else '未拦下'}")

    ok = (
        audit_web_pattern([10, 40, 10])[0] == "PASS"
        and audit_web_pattern([1500])[0] == "WARN"
        and audit_web_pattern([10, 10] * 5 + [10])[0] == "FAIL"
        and audit_web_pattern([10, -5])[0] == "FAIL"
        and audit_android_amplitudes([0])[0] == "FAIL"
        and audit_android_amplitudes([DEFAULT_AMPLITUDE])[0] == "PASS"
        and not audit_recipe(RECIPE)
        and bool(audit_recipe(bad))
    )
    print(f"\n总判定: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

实跑输出（2026-11-14，`python -I -X utf8`）：

```text
== 1. 振动模式校验 ==
[PASS] 成功确认 [10, 40, 10] -> 无问题
[PASS] 失败提示 [20, 60, 20] -> 无问题
[PASS] 合法长振动 [900] -> 无问题
[WARN] 五段组合 [10, 30, 10, 30, 10] -> 离散事件却用了 5 段（AOSP 注释支持 ≤3 段）
[WARN] 超长振动 [1500] -> 振动总时长 1500 ms > 1000 ms：AOSP 注释认为这已不是触觉反馈
[FAIL] 十一段 ... -> 段数 11 > W3C 上限 10，规范要求截断; 离散事件却用了 11 段（AOSP 注释支持 ≤3 段）
[FAIL] 含负数 [10, -5] -> 第 2 段（停顿）-5 不是非负整数毫秒

== 2. Android 振幅校验 ==
[PASS] [255] -> 合法
[PASS] [-1] -> 合法
[FAIL] [0] -> 第 1 个振幅 0 非法：必须 1-255 或 DEFAULT_AMPLITUDE(-1)
[FAIL] [256] -> 第 1 个振幅 256 非法：必须 1-255 或 DEFAULT_AMPLITUDE(-1)
[FAIL] [128, 0] -> 第 2 个振幅 0 非法：必须 1-255 或 DEFAULT_AMPLITUDE(-1)

== 3. 三通道配方校验 ==
[PASS] 12 行配方全部通过：视觉必在、高频不带非视觉通道、时压有触觉兜底
[自检] 故意违规的行被拦下：True -> [列表到底] 高频事件却加了非视觉通道：会退化成噪音

总判定: PASS
```

**注意**：`[1500]` 是 WARN 不是 FAIL——1000 ms 是 AOSP 源码注释里的工程判断，不是规范硬限制；而 W3C 的 10000 ms 上限才是硬限制。这个区分本身就是验收口径的一部分。

---

## §12 精确值总表（按来源分级）

### 12.1 规范/平台原文（可直接引）

| 值 | 内容 | 来源 |
|---|---|---|
| 3 秒 | 自动播放音频超过 3 秒必须有独立控制 | WCAG 2.2 SC 1.4.2 |
| 20 dB | 背景音至少低于前景语音 20 dB（≈1/4 响度） | WCAG 2.2 SC 1.4.7 |
| 1–2 秒 | 1.4.7 允许的偶发短音例外 | WCAG 2.2 SC 1.4.7 |
| 10 段 | Vibration 模式最大长度（超出截断） | W3C Vibration API |
| 10000 ms | Vibration 单段最大时长 | W3C Vibration API |
| 偶数位=振动 | `[振, 停, 振, …]` 交替语义 | W3C Vibration API / MDN |
| sticky activation | 无用户激活则 `vibrate()` 返回 false | W3C Vibration API |
| 1–255 / -1 | Android 单次振动振幅范围，或 DEFAULT_AMPLITUDE | AOSP `VibrationEffect.createOneShot` |
| 0 非法 | `createOneShot` 传 0 抛 IllegalArgumentException | AOSP 源码异常消息 |
| 0 = 马达关 | waveform 振幅 0 表示关闭 | AOSP `createWaveform` 注释 |
| 0 = 忽略 | waveform timing 0 的对被忽略 | AOSP `createWaveform` 注释 |
| 1000 ms | 「超过 1s 大概不是触觉反馈」 | AOSP 源码注释 |
| 3 段 | 「超过 3 段大概不是触觉反馈」 | AOSP 源码注释 |
| 0.0–1.0 | 自定义包络 intensity / sharpness | AOSP `BasicEnvelopeBuilder` |
| 10 dB SL | 支持强度保证的可感知下限 | AOSP `BasicEnvelopeBuilder` |
| ≤16 点 | 包络控制点建议上限 | AOSP `BasicEnvelopeBuilder` |
| 64 kbps HE-AAC | watchOS 音频编码建议 | Apple HIG `playing-audio` |
| 7 秒 / 200×140 px | Chrome MEI 允许自动播放的条件（仅桌面） | Chrome Autoplay Policy 官方博客 |
| Chrome 66 / 71 | 音视频元素 / Web Audio 的自动播放策略版本 | Chrome Autoplay Policy 官方博客 |
| 1–8 | Composition 原语常量值（CLICK=1、THUD=2、SPIN=3、QUICK_RISE=4、SLOW_RISE=5、QUICK_FALL=6、TICK=7、LOW_TICK=8） | Android 官方 API reference |
| API 30 / 31 | Composition 五原语 / THUD·SPIN·LOW_TICK 的引入版本 | Android 官方 API reference |
| 20 ms | 包络两个控制点之间的最小间隔 | Android 官方 `haptics-apis` |
| ≥16 点 | 包络控制点数下限（框架要求设备支持） | Android 官方 `haptics-apis` |
| 50 ms | 两段触觉可分辨间隔下限（5–10 ms 不可辨） | Android 官方 `custom-haptic-effects` |
| 100 ms | spin 间隔上限（超过即失去整合感） | Android 官方 `custom-haptic-effects` |
| 1.4× / ≤3 档 | 同一原语的相邻强度比与最多档数 | Android 官方 `custom-haptic-effects` |
| 0.0–1.0 | 原语 scale / 预设 scale 取值范围（0 = 刚好可感） | Android 官方 `VibrationEffect.Composition` |
| Android 16 (26Q4) | `VibrationEffect.Builder` 成为首选组合 API | Android 官方 `haptics-apis` |

### 12.2 本技能裁决（可校准，非官方）

| 值 | 裁决 | 依据 |
|---|---|---|
| 离散触觉 ≤100 ms | 单次确认类触觉的目标上限 | AOSP 1000 ms 注释 + 手感经验 |
| 组合 ≤3 段 | 超出改用声音+视觉 | AOSP 3 段注释 |
| 滑块/刻度仅离散档位 | 连续拖动不加 | 高频噪音 |
| 触觉语义 ≤5 种 | 成功/失败/切换/阈值/长按 | HIG「一致性」要求 |
| 音效 ≤5 个 | 成功/失败/提醒/切换/起止 | earcon 学习成本 |
| 成功上行 / 失败下行 | 音高方向与语义方向一致 | 心理声学惯例（非规范） |
| 音效间隔 ≥120 ms | 避免糊音 | 听觉掩蔽经验值 |
| 音效 ≤50 KB、单声道 | 预解码与首屏成本 | 工程经验 |
| 连续事件节流 300 ms | 批量操作只响一次 | 防噪音 |
| 有语音时音效低 20 dB | 与 1.4.7 对齐 | WCAG 1.4.7 |

### 12.3 生态实测（GitHub API，2026-11-14 快照）

| 仓库 | ★ | 许可 | 用途 |
|---|---|---|---|
| `goldfire/howler.js` | 25,444 | MIT | Web 音频播放层 |
| `Tonejs/Tone.js` | 14,901 | MIT | Web Audio 框架（偏音乐） |
| `joshwcomeau/use-sound` | 3,163 | MIT | React UI 音效 hook |
| `lochie/web-haptics` | 2,848 | MIT | 移动 Web 振动模式 |
| `expo/expo` | 53,532 | MIT | `expo-haptics` 跨端触觉 |
| `WebAudio/web-audio-api` | 1,138 | 未声明 | Web Audio 规范仓 |
| `w3c/vibration` | 20 | 未声明 | Vibration 规范仓 |
| `smolgroot/earcons` | 7 | MIT | 唯一对靶的 earcon 库（极小） |

搜索实测：`earcon` 全站 38 个仓库；`"web audio"` 11,187 个仓库但前 10 全是音乐/DSP，**没有 UI 反馈库**。

---

## §13 取源限制（本轮抓取实况，如实登记）

1. **`developer.android.com` 直连 `web_fetch` 失败**（任意 URL 均 `TypeError: fetch failed`）；本轮改经 `https://www.w3.org/services/html2txt?url=…` 取到 guide 正文（页脚 "Last updated 2026-10-26 UTC"），§4.6 与 §12 的 Android 数值均出自该渠道。**参考页 javadoc 仍不稳定**：`AudioAttributes`（`USAGE_ASSISTANCE_SONIFICATION` / `CONTENT_TYPE_SONIFICATION`）与 `AudioManager`（`AUDIOFOCUS_*` 数值）未取到，故只给常量名。
2. **AOSP main 分支比公开 SDK 新**：`BasicEnvelopeBuilder`、`USAGE_IME_FEEDBACK` 等属 flagged API（`FLAG_NORMALIZED_PWLE_EFFECTS` 等），公开 SDK 未必可用；旧设备无此能力，落地前须按目标 API level 复核。
3. **Apple HIG 无毫秒数值**：`playing-haptics` / `playing-audio` / `accessibility` 三页均无 ms 数值（已逐段核对），因此本文不提供任何「iOS 触觉毫秒值」，并明确该项为不可得信息。
4. **HIG 正文本轮通过 `.md` 后缀取得**（`developer.apple.com/design/human-interface-guidelines/<slug>.md`）；普通页面为 JS 外壳，直接 fetch 只回标题。
5. **Material Design 3 未取得「声音/触觉」专章**：`m3.material.io` 与 `m2.material.io/design/platform-guidance/android-haptics.html` 对本机均返回 "This website requires JavaScript."，无法核对原文，故全文不引用 M3 的声音/触觉规范；**不得据此推断 M3 没有相关要求**。
6. **Android 音频焦点**：`AUDIOFOCUS_*` 的**具体数值未核**（`AudioManager.java` 未取），文中只给常量名（如 `AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK`），不给数字。
7. **HTML Living Standard 的 autoplay「allowed to play」定义未取全**：`html.spec.whatwg.org/multipage/media.html` 返回被截断在 track 元素一节，故以 MDN《Autoplay guide》与 Chrome 官方博客替代，**不冒充规范原文**。
8. **`developer.chrome.com` 直连失败**：Chrome 自动播放策略文本取自其官方站点在 GitHub 上的同一篇源文件（`GoogleChrome/developer.chrome.com` 仓库 `site/en/blog/autoplay/index.md`），内容与发布页一致，已注明来源。
9. **Safari 自动播放**以 WebKit 官方博客（`webkit.org/blog/7734/...`）为准，未取得 Safari 开发者文档对应页。
10. **Vibration API 的「非 Baseline」状态**来自 MDN 顶栏标注；Firefox 桌面版对该 API 的支持行为未逐版本核对。
11. **`prefers-reduced-sound` 不存在**是负向结论：依据 MDN 无此页面（404）与 `@media` 特性索引未收录，**不等于**所有浏览器未来都不会加。
12. **国内平台（微信/支付宝/抖音）的震动与提示音规范**未取得官方文档，故未纳入；不得用二手博客数值替代。
13. **GitHub star / license / pushed_at 为 2026-11-14 抓取快照**，会随时间变化；`WebKit/WebKit` 与 `w3c/vibration` 的 license 字段为 `null`（API 未声明），不等于无许可。
14. **iOS 的 Core Haptics 参数（CHHapticEngine/ AHAP）**本轮未逐项核原文，故本文只写「transient / continuous + sharpness / intensity」这一层，不给具体 AHAP 字段值。

15. **Composition 原语的毫秒时长未取到官方原文**（`VibrationEffect.Event` / 预设时长页未能稳定取得），本文因此**不给任何原语毫秒值**，只给常量名、API level、强度与间隔规则；不要拿二手博客的「CLICK = 12 ms」当官方值。
16. **`VibrationAttributes` 的 int 数值表未取到**（参考页被限流/被侧栏截断），文中只给常量名与语义分类。
17. **W3C `html2txt` 是中转渠道**：它返回的是页面渲染后的纯文本，URL 与机构属实，但个别代码示例会被折行（如 `PRESET_CLICK` 被断成两行），引用时以官方页面为准。

---

## §14 与既有资产的分工

| 问题 | 去哪个资产 |
|---|---|
| 视觉反馈有哪些状态（loading/empty/error/success） | `feedback-states.md` |
| 动效时长、曲线、距离 | `motion-system.md`（触觉要与它的强度/锐度对齐） |
| 无障碍总则、对比度、键盘、读屏 | `accessibility.md`、`design-ethics-inclusion.md`（本文给 WCAG 1.4.2/1.4.7 细目） |
| 通知发不发、怎么发、权限 | `notifications-messaging.md`（后台完成应走通知，不是震动） |
| 拖拽、长按、阈值手势的交互规则 | `direct-manipulation.md`（本文补触觉常量映射） |
| 错误文案怎么写 | `ux-writing.md`（触觉不能替代文案） |
| 选哪个播放/触觉库 | `tools.md`（howler / use-sound / expo-haptics / web-haptics） |

**下轮候选（按缺口与可取证性排序）**：

1. **离线与网络状态（Offline & Connectivity States）**——`离线` 全域仅 4 处、`断网` 0 处、`offline` 1 处，无专章；可取证的一手源包括 MDN `navigator.onLine`（明确其不可靠）、Service Worker 规范、Cache API、`Background Sync`、Chrome 离线页设计、App Store 审核对「无网络时崩溃」的态度。与 `feedback-states.md` 的 error 态、`notifications-messaging.md` 的重试策略天然衔接。
2. **游戏化与进度（Gamification, Streaks & Progress）**——`游戏化` 0 处、`排行榜` 0 处、`streak` 1 处；需要定义「积分/徽章/连续天数」的伦理边界（与 `design-ethics-inclusion.md` 的成瘾设计红线联动）。
3. **数据表格与密集信息（Data Tables & Dense Data UI）**——未做词频实测，暂列待挖；一手源可走 W3C WAI 表格教程、Ant Design/Carbon 数据表规范。

---

## 附：一句话总结

**先问「看不看得到」，再问「来不来得及」，最后才问「响不响、震不震」；响和震都必须能被关掉，而且关掉之后用户一点信息都不该少。**
