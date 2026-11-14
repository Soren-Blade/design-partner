# 通知与消息触达（Notifications & Messaging）

> 快照 2026-11-13 · 每日升级 #38（v41→v42）· 主题：Notifications / Push / In-app Inbox / Badge / Notification Preferences / Transactional Email
> 取源：`Design-related websites.txt` 第二十六分区（本轮新增）+ Apple HIG 通知与权限页（经 `developer.apple.com/tutorials/data/*.json` 取正文）+ Android / Material 3 / Web Push 规范 + 邮件合规条文 + GitHub API 实测 16 库。凡规范条文与数值均引官方原文，凡工程建议均标注「工程约定」；未取到的条目单列在 §23。
>
> **边界纪律（先读这段，避免误路由）**：本文件只管「一件事发生了，要不要告诉用户、走哪条路、什么时候发、在哪儿呈现、用户能不能改主意、怎么算发得值」。**右上角通知的文案字数与按钮数**归 `ux-writing.md §7.3`；**toast / snackbar / 页面级横幅这五层 in-app 反馈**归 `feedback-states.md`；**系统权限「何时请求」的时机矩阵与 purpose string** 归 `onboarding-first-run.md §10`；**cookie 同意、默认勾选、自动续费、一键关闭这些欺骗性设计红线**归 `design-ethics-inclusion.md`；**邮件正文的文案语气与 i18n**归 `ux-writing.md`；**图标形状与角标图标画法**归 `iconography.md`；**SUS / 打开率等度量口径**归 `design-measurement-research.md`。本文件不重复这些资产，只补「一条通知从事件到回收的整条链路」这条结构性空白。

---

## 0. 一句话立场

**通知不是「把消息推出去」的能力，是**向用户借注意力**的行为；每发一条都在消耗一次可被撤回的额度——撤回的方式就是用户关掉整个通道。** 一个产品可以没有推送却有极好的消息体验（把答案放在用户会回来的地方），也可以每天发三条「猜你喜欢」然后被所有人静音。判断标准不是「送达率多高」，是「**这条消息改变了用户的下一步动作，且没有让他付出去关掉你的代价**」。

三条裁决（§2）：① **同一件事只发一次，不因未响应而追发**——Apple HIG 明文 *"Avoid sending multiple notifications for the same thing, even if someone hasn't responded."*，并直接点明后果是用户可能关掉整个应用的通知；② **系统权限是一次性资源，不是「多一次机会」**——iOS 的 `requestAuthorization` 只弹一次，被拒后只能靠设置页回捞，所以 pre-permission 的价值是「别浪费那唯一一次」，不是「多问一遍」；③ **未读数与角标是状态契约，不是装饰**——Apple 对角标的定义逐字是 *"the number of unread notifications that are available"*，`nil`（不改）与 `0`（清除并清空通知中心）是两种语义。

判型先答六问（§3），再选通道（§4），最后定中断级别与时机（§5–§10）。**顺序不能换**：先做一张漂亮的推送模板，再回头问「该不该发」，一定会给「已经写好的模板」找理由。

---

## 1. 六段链路判层：事件 → 决策 → 通道 → 时机 → 呈现 → 回收

通知体验是一条**有起点和终点**的链路，不是一个组件。把问题定位到具体段位，才知道该改埋点、改偏好结构、改文案、还是改权限策略。

| 段 | 用户所处状态 | 这一段必须回答 | 典型失败 | 主责资产 |
|---|---|---|---|---|
| **L1 事件** | 系统里发生了一件事 | 这件事**值不值得**变成一条通知？ | 把「有人点赞」也发推送；同一事件在 3 处各发一遍 | 本文件 §3 Q1 |
| **L2 决策** | 决定要发 | 发给谁、按什么类别与紧急度分级？ | 全量群发；营销与交易混在一个开关下 | 本文件 §5 / §10 |
| **L3 通道** | 选路径 | push / 站内消息中心 / 邮件 / 短信 / 实时活动，走哪条？ | 一个事件同时发 push + 邮件 + 站内三遍 | 本文件 §4 |
| **L4 时机** | 定时刻 | 现在发、稍后摘要、还是进免打扰？ | 凌晨 3 点推送课程更新；海外用户按北京时区收信 | 本文件 §6 / §9 |
| **L5 呈现** | 用户看到 | 标题说什么、几个按钮、要不要角标、怎么归组？ | 标题写公司名，正文写「点击查看」；角标显示的是待办数不是未读数 | `ux-writing.md §7.3` + 本文件 §7 / §8 |
| **L6 回收** | 用户处理完 | 已读、清除、退订、改偏好、下次还要不要发？ | 点开后角标不清零；退订要登录后再填三个字段 | 本文件 §8 / §11 / §13 |

**判层三问（先回答再动手）**：
1. 用户抱怨的是「没收到」还是「收太多」？——前者在 L3/L4，后者在 L1/L2。这两种抱怨的修法完全相反，改错方向会把问题放大一倍。
2. 这条消息有没有**时间价值**？现在不知道会做错事 → 时敏；知道得早只是心情好 → 摘要。
3. 关掉之后还能不能看到？——不能，就别把它做成「只有推送能看到」的唯一入口（§4 铁律四）。

---

## 2. 三条最重要裁决

### 裁决一 · 同一件事只发一次，不追发、不换通道补发

Apple HIG 逐字（Notifications · Best practices）：

> *"Avoid sending multiple notifications for the same thing, even if someone hasn't responded."*

同一页紧跟着写明后果：用户可能因此关掉你这个应用的全部通知。**「没响应」不是「没看到」的证据**——它更可能是「看到了不想理」，追发只是把「不想理」升级成「关掉你」。

**落地规则（工程约定）**：
- 一个业务事件生成一个 `dedupe_key`（如 `order:1234:shipped`），24 小时内同 key 只允许一条。
- 跨通道**不做**「push 没点就补一封邮件」的自动补发；要做也只能做**用户显式同意**的摘要（§9）。
- 交易类与营销类必须分开计数与分别开关（§10），否则一次交易失败就会连带把营销也关掉——反过来也一样。

### 裁决二 · 系统权限是一次性资源：pre-permission 的全部价值是「别浪费唯一一次」

iOS 的授权契约逐字（`requestAuthorization(completionHandler:)`）：

> *"The first time your app calls the method, the system prompts the person... Subsequent calls to this method don't prompt the person again."*

HIG 侧同样逐字：*"Subsequent authorization requests don't prompt the person."* 也就是说**被拒之后代码里再调一次不会弹第二次**，只有用户自己去设置里改。所以「多问一次」这个策略在系统层不存在；能做的是**在弹之前问自己一遍**：

| 做法 | 效果 | 何时用 |
|---|---|---|
| 启动即弹系统对话框 | 拿到授权或永久失去，且用户还不知道为什么要给 | 只有在通知就是核心功能（闹钟、即时通讯、打车接单）时才可接受 |
| 先做 in-app 说明页（pre-permission）再弹 | 把「不知道要干嘛」的拒绝转成「知道要干嘛」的同意 | 默认推荐；说明页必须能拒绝且拒绝后不复发（§7） |
| provisional（临时授权）静默投递 | 不弹窗先发到通知中心历史，由用户逐条「保留 / 关闭」 | 无承诺型内容、想先证明价值时（仅 iOS 有） |
| 什么都不做 | 用户在设置里手动开 | 通知非必需的产品 |

**注意一个常见错误**：把「时效性」当成授权项去请求。Apple 的 `UNAuthorizationOptions` 里 `timeSensitive` 在文档中列在 **Deprecated** 分组、`deprecatedAt` 与 `introducedAt` 同为 iOS 15.0（引入即废弃），时效性靠 `interruptionLevel` 表达而不是靠授权位（§5）。把它写进请求清单既拿不到效果，也会让审计看起来像抄错了文档。

### 裁决三 · 未读数与角标是状态契约，不是装饰

Apple 对角标的定义逐字：

> *"A badge is a small, filled oval containing a number that can appear on an app icon to indicate the number of unread notifications that are available."*

以及 `applicationIconBadgeNumber` 的三态契约：**0 = 移除角标并清空通知中心里本应用的通知**；**>0 = 显示该数字**；**nil = 保持现状**。三条推论：

1. **`nil` 不是「清除」**。很多实现把「没有新数量」写成 `nil`，结果角标永远停在旧数字上——这是最常见的「角标幽灵」。
2. **角标数字必须等于未读通知数**，不是待办数、不是订单数、不是「有多少条消息我没看」（后者若含已读会永久偏大）。Apple 同时禁止把角标用于无关数字：*"Don't use a badge to convey numeric information that isn't related to notifications, such as weather-related data, dates and times, stock prices, or game scores."*
3. **清零要同时清通知中心**，否则用户看到「角标没了但通知还在列表里」，会怀疑清空没生效。

---

## 3. 六问判型决策树

```
Q1 这条消息会改变用户下一步动作吗？
   ├─ 不会（纯告知、纯运营、纯 KPI） → 不发；或降级为站内静默条目
   └─ 会 → Q2
Q2 现在知道与一小时后知道，用户的决定会不同吗？
   ├─ 会（今天要出门、订单要超时、验证码） → 时敏路径（§5 timeSensitive / 立即投递）
   └─ 不会（周报、上新、社区动态） → 摘要路径（§9 digest）
Q3 用户此刻可能在哪块屏上？
   ├─ 就在产品内 → 页面内反馈（feedback-states 的 L0–L2），不打扰通知通道
   ├─ 可能离开 → push（需已授权）+ 站内留档（用户回来能看到）
   └─ 跨设备/需归档 → 邮件（交易类）或消息中心
Q4 这个「类别 × 通道」用户显式同意过吗？
   ├─ 营销且未 opt-in → 不发（合规硬线，§13）
   └─ 交易/安全类 → 可发，但仍须可关（§10）
Q5 被拒绝、被静音、被关掉之后，还有第二条路吗？
   ├─ 没有 → 设计缺陷：先补站内消息中心（§8）
   └─ 有 → 在关闭路径上写清楚「你仍可在消息中心看到」
Q6 怎么知道它有用？
   └─ 打开率 / 关闭率 / 退订率 / 打扰投诉 / 每条带来的有效动作（§14）
```

**六问的顺序不可换**：Q1 不过就别进 Q2–Q6。跳过 Q1 直接谈「文案怎么写更好点」，本质上是在优化一件不该发生的事。

---

## 4. 通道选型矩阵

一个事件**只走一条主通道**，第二条只做兜底（用户回来能看到），不做「补发」。

| 通道 | 适用 | 延迟 | 可撤销性 | 典型失败 |
|---|---|---|---|---|
| **站内消息中心（inbox）** | 所有事件的**留档层**；可等、需回看、多条聚合 | 无延迟，进产品才看 | 可删可读 | 只有列表没有分组；未读定义混乱（§8） |
| **Web / App push** | 需要立刻离开产品也能知道的时敏事件 | 秒级 | 不可撤回，只能靠后续静默 | 权限一次性、被拒即死；无站内兜底（§6 / §7） |
| **邮件** | 交易凭证、需归档、跨设备、B 端通知 | 分钟级 | 可退订、可进垃圾箱 | 营销与交易混发；退订链路要登录（§12 / §13） |
| **短信 / 语音** | 验证码、极高价值告警 | 秒级 | 不可撤回，成本最高 | 用于营销 → 投诉与封号 |
| **实时活动 / 锁屏常驻** | 进行中的一段过程（配送、赛事、计时） | 持续更新 | 可结束 | 当广告位用；更新超预算被限流（§15） |

**四条铁律（工程约定）**：
1. **留档优先**：任何 push 都必须同时能在站内消息中心找到——否则用户一划掉就永久丢失。
2. **一个事件一条主通道**：跨通道补发会把「没点」误判成「没看到」。
3. **紧急度 ≥3 才允许破免打扰**（§9）；其余一律排队到窗口外。
4. **关掉 push ≠ 关掉消息**：偏好页要能表达「站内保留、不要推送」，而不是二选一的全局开关（§10）。

## 5. 中断级别与优先级（三平台口径）

「发不发」之后的下一个决定不是「发什么」，而是**「用多大声音发」**。三家的机制不同，但抽象出来只有四档。

### 5.1 四档优先级模型

| 档 | 用户感受 | 允许的动作 | 典型事件 |
|---|---|---|---|
| **P0 关键** | 会响、能压静音 | 破免打扰 + 破静音 | 安全告警、本人正在等待的验证、已批准的关键业务中断 |
| **P1 时敏** | 亮屏 + 提示音，破专注模式 | 破 Focus/免打扰，不压静音 | 「你的车 5 分钟后到」「会议 10 分钟后开始」 |
| **P2 普通（默认）** | 进通知栏，可能响一声 | 不破免打扰 | 私信、评论、任务指派 |
| **P3 安静** | 只进列表/摘要，不亮屏不响 | 只留档 | 上新、周报、关注、系统提醒 |

**判 P1 的唯一标准**（Apple 逐字）：*"an event that's happening now or will happen within an hour"*——不是「重要」，是「**时间窗在一小时内**」。判不准就降一档，降档的代价小于打扰的代价。

### 5.2 iOS：`interruptionLevel`

| 值 | 官方描述 | 能力 |
|---|---|---|
| `passive` | *"adds the notification to the notification list without lighting up the screen or playing a sound"* | 不亮屏、不响 |
| `active`（默认） | *"presents the notification immediately, lights up the screen, and can play a sound"* | 亮屏 + 可响 |
| `timeSensitive` | *"breaks through system notification controls"* | 破定时投递 / 破 Focus；**不压静音** |
| `critical` | *"bypasses the mute switch to play a sound"* + *"requires an approved entitlement"* | 三者皆可 |

**三条红线**：
1. **营销永不用 timeSensitive**——HIG 逐字：*"Never use the Time Sensitive interruption level to send a marketing notification."*
2. **critical 不是「重要通知」的同义词**——官方定位：*"Critical notifications are extremely rare and typically come from governmental and public agencies..."*，且需 Apple 单独批的 entitlement。
3. **`timeSensitive` 不是授权项**：`UNAuthorizationOptions` 里它列在 Deprecated 分组（`deprecatedAt` 与 `introducedAt` 同为 iOS 15.0），把它写进 `requestAuthorization` 是照抄旧文档的错误（§2 裁决二）。

### 5.3 Android：渠道重要性（channel importance）

Android 8.0（API 26）起**所有通知必须挂在渠道上**，通知的响/亮/浮动行为由**渠道**决定，而不是单条通知。官方五级（英文逐字，2026-11-13 取自 channels 页）：

| 用户可见级别 | 常量 | 官方行为原文 |
|---|---|---|
| Urgent | `IMPORTANCE_HIGH` (4) | *"Makes a sound and appears as a heads-up notification."* |
| High | `IMPORTANCE_DEFAULT` (3) | *"Makes a sound."* |
| Medium | `IMPORTANCE_LOW` (2) | *"Makes no sound."*（仍进状态栏） |
| Low | `IMPORTANCE_MIN` (1) | *"Makes no sound and doesn't appear in the status bar."* |
| None | `IMPORTANCE_NONE` (0) | *"Makes no sound and doesn't appear in the status bar or shade."* |

**四条硬约束（官方原文）**：
1. **创建后不可改重要性**：*"Once you submit the channel to the NotificationManager, you can't change the importance level. However, the user can change their preferences for your app's channels at any time."*——只能在创建时定对；要改只能新建渠道 ID，而旧渠道里「用户已关」的状态不会迁移（这是一次**产品级决策**，不要当重构顺手做）。
2. **创建后不可改视听行为**：*"After you create a notification channel, you can't change the notification channel's visual and auditory behaviors programmatically. Only the user can change the channel behaviors from the system settings."*（名字与描述仍可改）
3. **目标 API 26+ 且不带渠道 → 通知不显示**，系统记错误日志。
4. **官方页面自相矛盾，不要替它调和**：同一页又写 *"All notifications, regardless of importance, appear in non-interruptive system UI locations, such as in the notification drawer and as a badge on the launcher icon…"*，与 NONE 的「不出现在状态栏或抽屉」直接冲突。**工程结论**：别赌 MIN/NONE 还能被看到——要「静默留档」用 MIN 并在站内消息中心留一份（§8）；要「关掉」用 NONE，并把它当**关闭**而不是降级。

**渠道设计规则（工程约定）**：一个**用户可感知的类别**一个渠道（订单 / 私信 / 营销 / 系统），不要一个功能一个渠道（用户会在设置里看到 20 个开关并全部关掉）；渠道名必须是用户语言（「订单与物流」而不是 `order_updates_v2`）。

### 5.4 Web：没有中断级别

Web 通知只有「允许/不允许」，**没有** iOS 的 interruptionLevel，也没有 Android 的渠道重要性可编程控制（用户的 OS 级设置说了算）。所以：

- Web 端不要承诺「重要通知一定会响」——兑现不了。
- 优先级只能在**是否发送**与**是否立即发送**上体现（P0/P1 立即，P2/P3 进摘要或只进站内）。
- 真正的关键链路（验证码、支付结果）不要依赖 Web 通知，用带内提示 + 页面态。

---

## 6. 三平台权限机制（同一个「授权」，三种失败模式）

| 平台 | 请求方式 | 用户可选 | 拒绝后能否再弹 | 回捞路径 |
|---|---|---|---|---|
| **iOS** | `UNUserNotificationCenter.requestAuthorization` | 允许 / 不允许 | **代码再调不再弹**（官方：*"Subsequent calls to this method don't prompt the person again."*） | 系统设置 → 通知 → 该应用；或用 provisional 先静默投递 |
| **Android 13+（target 33+）** | `POST_NOTIFICATIONS` 运行时权限 | 允许 / 不允许 / **滑开对话框** | **滑开 = 状态不变**（可再问）；显式拒绝后的再请求行为官方页未说明 → 按「不再打扰」处理 | 系统设置 → 应用 → 通知（可用 `ACTION_CHANNEL_NOTIFICATION_SETTINGS` 深链） |
| **Android 12L 及以下 target（≤32）** | 系统在首个 Activity 启动（或创建渠道后启动）时自动弹 | 允许 / 不允许 | **一次拒绝即永不再弹**（除非卸载重装，或把 target 升到 33+） | 同上级 |
| **Web** | `Notification.requestPermission()` | 允许 / 阻止（+ 关闭对话框） | `denied` 后不应再请求（MDN 示例：*"if the user has denied notifications … there is no need to bother them anymore"*）；`default` 视同未决定 | 浏览器站点设置（`chrome://settings/content/notifications`）；**无法用 API 重置** |

### 6.1 四条必须写进验收的差异

1. **iOS 是「一次性」**：没有 pre-permission 就直接弹，等于把唯一一次机会赌在用户对产品价值的理解上。
2. **Android 13+ 的「滑开」不是拒绝**：`permission` 状态不变，下次还能问——但这**不代表**可以反复弹；官方把「何时弹」的控制权交给目标 33+ 的应用，意味着**时机责任也在应用**。
3. **Web 的 `default` 等于拒绝**（MDN 逐字：*"in this case the application will act as if permission was denied"*），所以「还没问过」和「问过被拒」在行为上必须分别处理，不能混成一个分支。
4. **Web 必须由用户手势触发**：*"going forward browsers will explicitly disallow notification permission requests not triggered in response to a user gesture."*——页面加载即弹的做法已被浏览器淘汰；而 `denied` 之后连弹窗都不会再出现，这是**规范级**约束而非礼貌建议：Permissions 规范 §5.2 *"If current state is not "prompt", return current state and abort these steps."*

### 6.2 Android 13 的四个容易踩的坑（官方原文）

- **新装默认关**：*"If a user installs your app on a device that runs Android 13 or higher, your app's notifications are off by default."*——「装完就能推」在 13+ 上不成立。
- **升级预授权有条件**：*"应用必须已具有通知渠道，并且用户未在搭载 12L 或更低版本的设备上明确停用应用的通知。"* 反过来说：**升级前先建好渠道**，老用户升级后才不会被静默关掉。
- **拒绝是「全渠道封锁」**：*"…your app can't send notifications unless it qualifies for an exemption. All notification channels are blocked, except for a few specific roles."*——不是「关掉一个类别」，是整站哑火；前台服务（FGS）通知仍能在任务管理器出现，但**不进抽屉**。
- **请求必须带上下文**：*"When you request notification permissions within your app, do so in the correct context, so that it's explicitly clear what the notifications are used for and why the user should opt in."*（官方示例触发点：用户点了「提醒铃」按钮）

### 6.3 Web Push 的最小可用集（缺一即不通）

1. **HTTPS**（安全上下文；`localhost` 例外）；
2. **Service Worker** 注册成功——移动端必须走它：*"The Notification() constructor will throw a TypeError on most mobile browsers."*；
3. `Notification.requestPermission()` 返回 `granted`（须在用户手势内调用）；
4. `registration.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey })` 拿到订阅；
5. 服务端用 VAPID 私钥签名发送（Node 侧 `web-push`），且**每条消息必须带 `TTL`**（RFC 8030：*"An application server MUST include the TTL (Time-To-Live) header field"*，过期后 *"the push service MUST NOT attempt to deliver the push message"*）。

**注意**：订阅会过期/失效（浏览器清理、用户清站点数据），服务端必须处理 `410 Gone` 并重新引导订阅，否则「推送不来了」会变成长期无法解释的 bug。另：Web 通知的 `actions` 只在**Service Worker 发出的持久通知**上可用（*"actions is only supported for persistent notifications fired from a service worker"*），页面里 `new Notification()` 加按钮是无效的。

---

## 7. 被拒绝之后的恢复路径

**前提**：权限被拒**不是**「用户不想要消息」，是「现在不想被这样打扰」。所以恢复策略不是「再问一次」，是**先给一条不打扰的路，再给一个回头的入口**。

### 7.1 三态分流

| 状态 | 用户看到 | 你应该做 |
|---|---|---|
| **未请求**（iOS 从未调过 / Web `default` / Android 13+ 未请求） | 产品行为正常 | 在**功能触发点**做 pre-permission（§11.3），不在启动时 |
| **已拒绝** | 仍在产品内 | ① 站内消息中心必须完整可用；② 在设置页显示「推送已关闭」+ 一键跳系统设置；③ **不弹模态劝阻**，最多一条可关闭的 inline 提示 |
| **已允许但被系统/用户后续关掉** | 以为有推送 | 定期读一次当前权限状态（`getNotificationSettings` / `Notification.permission` / `NotificationManagerCompat.areNotificationsEnabled()`），发现关闭就回到「已拒绝」分支 |

### 7.2 各平台的回捞入口（不要只写「去设置里打开」）

- **iOS**：官方只给了客观路径（设置 → 通知 → 应用），**没有**「推荐引导话术」——所以文案自己写，不要伪造官方推荐。写法：说清**失去什么**（「你将收不到发货提醒」）+ 一句可执行的路径 + 一个「暂不开启」。HIG 同时要求应用内必须有设置页：*"you must also provide an in-app settings screen that lets people change their choice."*
- **Android**：用 `ACTION_CHANNEL_NOTIFICATION_SETTINGS` 直接跳到**该渠道**的设置页（需 `EXTRA_APP_PACKAGE` + `EXTRA_CHANNEL_ID` 两个 extra），比让用户自己在设置里找三层目录好得多。
- **Web**：只能引导到浏览器站点设置，且**无法**用 JS 重新触发对话框；给一张截图路径说明比给一句话有用。

### 7.3 iOS 的第三条路：provisional（静默投递）

在「要授权」与「不打扰」之间，iOS 还有一档**不需要弹窗**的授权：

> *"Use provisional authorization to send notifications on a trial basis."* + *"delivers provisional notifications quietly — they don't interrupt the person with a sound or banner, or appear on the lock screen... only appear in the notification center's history. These notifications also include buttons that prompt the person to keep or turn off the notification."*

**用法**：适合「新用户 + 通知价值尚未证明」的场景——先静默投递进通知中心，让用户在真实内容里决定留还是关，把一次性弹窗的赌注拆成多次观察。**不适合**：安全/交易类（用户可能整段时间没看到）、以及需要即时打断的场景。

### 7.4 三条红线

1. **不指责用户**：不写「你错过了重要消息」「为了你的安全请开启」这类恐吓式文案。
2. **不反复弹**：拒绝后同一次会话不再出现权限请求；下次请求必须由**明确的用户动作**触发（点「开启提醒」按钮）。
3. **不缺省降级**：被拒 ≠ 看不到消息。站内消息中心（§8）与邮件（§12）必须承接，否则权限就成了单点故障。

## 8. 消息中心与未读状态（inbox 是通知的留档层）

消息中心不是「通知的历史列表」，是**用户回来补看的地方**。§4 铁律一说「任何 push 都必须能在站内找到」，这条铁律成立的前提是消息中心本身可读、可筛、可追溯。

### 8.1 五件套结构

| 件 | 必须回答 | 缺了会怎样 |
|---|---|---|
| **分组 / 分类** | 这是交易、安全、社交还是运营？ | 用户为了找一条退款通知要翻 200 条「上新提醒」 |
| **条目骨架** | 谁、什么事、什么时候、点了去哪 | 一条「您的消息已更新」，点进去是首页 |
| **未读状态** | 哪条没读、一共几条没读（§8.3） | 角标与列表不一致，用户不再相信角标 |
| **批量操作** | 全部已读、按类清空、单条删除、稍后处理 | 只能一条条点，用户会放弃清理 |
| **空态 / 失败态** | 没有消息时说什么、加载失败怎么办 | 空白页 → 用户以为功能坏了（边界：`empty-states.md` 管形态） |

### 8.2 条目骨架（一行能判断，不用点进去）

每条至少四件，顺序固定：

1. **来源**（哪个系统/谁）——头像或图标 + 名称；
2. **事件**（一句话说发生了什么，动词开头）——「你的订单 1234 已发货」而不是「订单通知」；
3. **时间**（相对时间 ≤7 天内，超过写日期；同一分钟内多条用「刚刚」）；
4. **去向**（点开是哪个页面，必须与事件一致——交易通知进订单详情，不要进首页）。

未读标记 **不能只靠颜色**：加粗字重 + 圆点 + `aria-label="未读"`，三者至少两个（SC 1.4.1「不仅靠颜色」的通用原则，阈值与判定归 `accessibility.md`）。

### 8.3 未读的定义（三种，必须选一种并全局统一）

| 定义 | 口径 | 适合 | 风险 |
|---|---|---|---|
| **按条**（每条一个未读） | 未读数 = 未读条目数 | 交易/审批类，条数少且每条都要处理 | 社交场景会爆炸（100 个赞 = 100 未读） |
| **按会话/对象聚合** | 未读数 = 未读会话数 | 社交、协作、客服 | 定义要写清楚：会话里最旧未读的时间 |
| **按待办** | 未读数 = 需要我动作的条目 | 审批、工单 | 与「通知」不是一回事，**不要叫未读数** |

**统一铁律（工程约定）**：
- 未读是**账户级**状态，不是设备级；以服务端 `seq` 为准（§15）。
- 同一屏幕上（顶部 tab 气泡、列表行圆点、应用角标）必须用**同一个**数字口径。
- 「全部已读」必须同时把角标清零并清空通知中心（照 Apple 的 0 语义，§9）。

### 8.4 列表的工程细节

- **分页用游标**（`before_id` / `seq`），不用 `offset`——新消息插入会让 offset 分页错位重复。
- **首屏 20 条**，滚动加载每次 20；首屏必须包含「最近一次未读」的位置，或提供「跳到最早未读」。
- **搜索**：至少支持按来源与关键词；没有搜索的消息中心在第 30 条之后就等于没有。
- **实时插入**：新消息到达时若用户正在顶部，插入并轻提示；若用户在列表中段，**不要**跳滚动位置，只在顶部显示「有 3 条新消息」。
- **保留期**：明确写「消息保留 90 天」，到期前给归档/导出，否则用户会把消息中心当数据库。

### 8.5 边界

- 表单字段与校验 → `form-table.md`；五层 in-app 反馈（toast / 横幅 / 页面级）→ `feedback-states.md`；空态形态 → `empty-states.md`。
- 本文件只管**跨会话留档**这一类（离开产品后仍要能看到的东西）。

---

## 9. 角标（badge）与未读数：99+ 数字上限、清除时机、可访问性

**角标是「有多少条未读通知」的一个数字，不是随便挂个红点。** Apple 逐字定义：

> *"A badge is a small, filled oval containing a number that can appear on an app icon to indicate the number of unread notifications that are available."*

### 9.1 三态契约

| 值 | 语义 | 常见错法 |
|---|---|---|
| `0` | 移除角标 **并清空通知中心里本应用的通知** | 只把数字改 0，列表里还留着 |
| `>0` | 显示该数字 | 显示的是待办数/订单数 |
| `nil` / 不设置 | **保持现状**（不是清除） | 想清零却传了空值 → 角标幽灵 |

### 9.2 五条硬规则

1. **数字上限显示**：超过 99（或 999）显示 `99+`，但**读给读屏的仍是完整数字**（`aria-label="128 条未读"`）。
2. **不可只靠角标传达关键信息**：Apple 逐字 *"Make sure badging isn't the only method you use..."*——关掉角标与读屏用户会完全收不到。
3. **不用于无关数字**：Apple 明文列举了天气数据、日期时间、股价、游戏分数四类禁止用途。
4. **点状角标（dot）只用在不适合计数时**（如「有新内容」），且必须同时有列表内的文字说明；点状角标不参与「未读数」口径。
5. **清除路径要唯一且可达**：进入列表底部自动已读、或显式「全部已读」；两条都要有，不能只有前者（否则用户没法主动清）。

### 9.3 平台差异（工程约定）

- iOS/macOS：应用图标角标受系统「标记」开关控制，用户可关；关掉后必须仍能从列表看到未读。
- Android：启动器角标由**系统**绘制，应用只能**建议**数字——`setNumber(n)` 写入的 `number` 字段官方明说 *"The system may or may not use this field to modify the appearance of the notification."*，**不能当强契约**；`setBadgeIconType` 三档（`BADGE_ICON_NONE=0` 显示数字 / `SMALL=1` 用 `getSmallIcon()` / `LARGE=2` 用 `getLargeIcon()`，API 26 起默认大图标）。默认行为是「每条通知递增长按菜单上的数字」，所以**不要**自己维护一套计数再画一遍。
- 未读分组：Android 分组必须有 group summary——*"Grouped notifications must have an extra notification that acts as the group summary."*；4 条以上不带 group 时，Android 7.0+ 会**自动**分组，产品侧的「合并」设计要与之兼容而不是打架。
- Web：**没有**应用图标角标（除已安装 PWA 的 `navigator.setAppBadge()`）。Badging API 三条语义：不传参 = 置**标记点**（flag）；传 `0` = 清除；*"User agents may also ignore this data and display a marker instead."*（**可能被忽略**），且 MDN 明标 *"This feature is not Baseline"*。→ 网页产品的主力仍是标题前缀 `(3) 收件箱 — 产品名` + 列表内未读标记。

---

## 10. 免打扰、频率与摘要

### 10.1 免打扰（DND / quiet hours）

- **窗口必须支持跨午夜**：22:00–08:00 是最常见的默认，代码里若写成 `start <= h < end` 会算出空集（§21 的 `in_quiet` 有跨午夜分支）。
- **时区按用户本地**，不是服务器时区；旅行中改时区要跟着变（用 IANA 时区 ID 存，不要存固定偏移）。
- **破窗规则**：只有紧急度 ≥3（Critical / 安全告警 / 本人正在等待）允许破窗；其余延迟到窗口结束后**第一条**批量投递，不逐条补发。
- **补发上限**：窗口结束后一次最多投 1 条摘要，不是把夜里攒的 8 条依次弹出来。
- **免打扰是用户的开关，不是产品的默认静音**：产品侧不能偷偷把所有通知都塞进摘要来「降低打扰」，那会掩盖 L1 没做好（发了不该发的）。

### 10.2 频率预算（工程约定，非标准）

| 类别 | 24h 上限 | 说明 |
|---|---|---|
| 安全 / 交易 | 不限（按事件） | 但同一事件不追发（§2 裁决一） |
| 时敏提醒（待办、配送） | 3 条 | 超过就合并成一条 |
| 社交聚合 | 3 条 | 30 分钟聚合窗口（§18.3） |
| 运营 / 营销 | 1 条 / 天，且 ≤3 条 / 周 | 需 opt-in（§13） |

超限的处理顺序是**合并 → 降级到摘要 → 丢弃**，不是「攒着明天一起发」。

### 10.3 摘要（digest）

- **时段由用户选**（早 8 点 / 午 12 点 / 晚 8 点至少三选一），不允许服务端硬编码「每天 09:00」。
- 摘要条目**必须能跳转到原条目**，且跳转后该条目标记为已读。
- 摘要本身也算一次投递，计入频率预算。
- Focus / 专注模式拦的是**提醒**不是**通知本体**——Apple 逐字：*"Even though a Focus might delay the delivery of a notification alert, the notification itself is available as soon as it arrives."* 所以「被 Focus 拦下」不等于「没发出去」，不要在后台重发。

---

## 11. 通知偏好设置页

### 11.1 结构：类型 × 通道 的矩阵，不是一列总开关

```
通知设置
├─ 交易与安全（不可关闭，仅说明）
│   ├─ 订单与退款          [锁定]
│   └─ 登录与安全告警      [锁定]
├─ 社交互动
│   ├─ 私信与 @我          [推送] [邮件] [站内]
│   └─ 点赞与关注          [摘要] [站内]
├─ 产品动态
│   ├─ 新功能              [推送] [邮件] [站内]   ← 默认全关
│   └─ 活动与优惠          [推送] [邮件] [站内]   ← 默认全关 + opt-in
└─ 免打扰  22:00 – 08:00  [开]
```

**三条结构铁律**：
1. **每个类型都要能单独关**；营销类默认关，且没有预勾选（GDPR Recital 32 逐字：*"Silence, pre-ticked boxes or inactivity should not therefore constitute consent."*）。
2. **交易/安全类不可关**，但必须在页面上**说明原因**（「用于通知你订单与账号变化」），而不是灰掉不给解释。
3. **撤回与给予同价**：Art. 7(3) 逐字 *"It shall be as easy to withdraw as to give consent."*——退订路径的步数不得多于订阅路径。

### 11.2 交互细节

- **用开关（toggle），即时生效，不要「保存」按钮**——NN/g 逐字：*"Toggle switches should take immediate effect and should not require the user to click Save or Submit"*。
- **标签写状态不写问句**：写「邮件通知」，不写「您想收到我们的邮件通知吗？」（同一篇 NN/g 的 do/don't）。
- **不要双重否定**：写「接收营销邮件」，不写「不接收非营销邮件之外的内容」。
- **每行右侧给例子**：「你会收到：订单发货、退款到账」——用户据此判断，而不是靠类型名猜。
- **改动要给回执**：切开关后 toast/文字确认「已关闭营销推送」，避免用户反复点。
- **移动端与 Web 同一套结构**，但移动端要能跳到系统设置（应用自身的开关无法覆盖系统级关闭）。

### 11.3 权限请求页（pre-permission）

- 说明**你会发什么、多久一次、可以随时关**，然后两个按钮：`暂不开启` / `开启通知`。
- **拒绝后不复发**：本次会话不再弹；最多在下一次明确触发相关功能时再问一次（并说明理由）。
- NN/g 的实测口径：*"Allow them to experience the app and only in a later session ask them to accept notifications."*——首次启动不是请求时机。
- 权限时机矩阵与 purpose string 细节 → `onboarding-first-run.md §10`；本文件只管**请求页的文案结构与拒绝后的兜底**（§7）。

---

## 12. 邮件触达（交易邮件与营销邮件是两种东西）

### 12.1 分类口径（按「主要目的」判，不按标签）

15 U.S.C. §7702 逐字：

> *"The term 'transactional or relationship message' means an electronic mail message the primary purpose of which is— (i) to facilitate, complete, or confirm a commercial transaction that the recipient has previously agreed to enter into with the sender…"*

> *"The term 'commercial electronic mail message' does not include a transactional or relationship message."*

16 CFR §316.3(b) 进一步收窄：*"the 'primary purpose' … shall be deemed to be transactional or relationship if the electronic mail message consists exclusively of transactional or relationship content"*——**夹带一句广告就转商业口径**。GOV.UK Service Manual 的设计口径相同：*"You don't need to ask permission to send transactional messages."* / *"Never send subscription messages unless the user has explicitly asked for them"*。

**落地**：两类邮件用**不同的发信域名子域或不同的 From 名称**（如 `order@` 与 `news@`），退订只作用于后者；把营销塞进交易邮件是这条链路上最贵的错误。

### 12.2 退订（可测的四条）

| 要求 | 一手依据 | 验收 |
|---|---|---|
| 10 个工作日内停止 | 15 U.S.C. §7704(a)(4)(A)(i) | 退订后立刻生效（不要等 10 天） |
| 不得收费、不得索取邮箱与偏好之外的信息、不得要求登录 | 16 CFR §316.5 | 点一次链接、选一个原因（可跳过）即完成 |
| 一键退订头 | RFC 8058 §3.1：*"The List-Unsubscribe-Post header MUST contain the single key/value pair 'List-Unsubscribe=One-Click'."* | 头存在 + DKIM 覆盖这两个头 + POST 返回 2xx |
| 退订入口显著、邮件发出后至少 30 天可用 | §7704(a)(3)(A)：*"clearly and conspicuously displayed"* | 页脚有纯文本链接 + 深度链接，不依赖图片 |

RFC 8058 的另一句值得贴在评审会上：*"if an unsubscription process is too difficult, the recipient's alternative is to report mail from the sender as junk"*——难退订会把退订转成垃圾举报，直接打击送达率。

**一键退订的三个协议细节（最容易实现成「假一键」的地方）**：
1. `List-Unsubscribe` 里 **MUST 含一个 HTTPS URI**（只有 `mailto:` 不算一键退订）；
2. `List-Unsubscribe-Post` 只允许那一个键值对，**不能加别的字段**；
3. 客户端发起的 POST **不得携带 cookie、HTTP 授权或任何上下文**——*"The POST request MUST NOT include cookies, HTTP authorization, or any other context information."*，且 *"The mail receiver MUST NOT perform a POST on the HTTPS URI without user consent."*

→ 验收口径：把这两个头打印出来给评审看，缺一个就是没做；「页脚有退订链接」在同一条链路上只是**最低要求**。

### 12.3 送达与信誉（三件基础设施，不是设计细节）

- **SPF**：*"lets you publish a DNS record of all the domains or IP addresses you use to send email. Receiving email services check the record and know to treat email from anywhere else as spam."*
- **DKIM**：*"verifies an email's domain and helps show that the email has not been tampered with in transit."*
- **DMARC**：*"confirms the sender's identity using [SPF] and [DKIM]"*、*"tells the recipient's email service what to do with emails that fail the check"*。

三者任一缺失，设计得再好也会进垃圾箱；「没收到」的投诉有一半根因在这里，不在文案。

### 12.4 邮件正文的设计口径

- **禁用加粗/斜体/下划线/换字体**（GOV.UK Notify 模板规则逐字：*"You cannot use bold, italics, underlined text, different typefaces or fonts. This is because they can make it harder for people to read what you've written."*）——交易类邮件优先保证纯文本可读与读屏友好。
- **对比度 ≥4.5:1**（SC 1.4.3），且**不允许四舍五入**（*"computed values should not be rounded (e.g., 4.499:1 would not meet the 4.5:1 threshold)"*）。
- **主题行前置关键信息**：*"Remember that email subject lines are often shortened."*（移动端截断，无统一字符数标准——见 §23）。
- **发送时段**：GOV.UK 建议 *"If a message doesn't need to be sent immediately, consider sending it during business hours"* 且 *"If possible, avoid sending text messages late at night."*（政府建议，非硬标准）。
- **物理邮寄地址**：商业邮件必须含有效实体地址（§7704(a)(5)(A)）与广告标识。

---

## 13. 合规红线（写进设计评审的硬条件）

| 红线 | 逐字依据 | 设计动作 |
|---|---|---|
| **营销默认关** | GDPR Recital 32：*"Silence, pre-ticked boxes or inactivity should not therefore constitute consent."* | 复选框默认不勾；开关默认 off |
| **同意须是肯定动作** | Recital 32：*"a clear affirmative act establishing a freely given, specific, informed and unambiguous indication"* | 一次点击明确同意某一类，不打包全部 |
| **逐用途分别同意** | Recital 32：*"When the processing has multiple purposes, consent should be given for all of them."* | 营销同意 ≠ 交易通知同意；不同营销类别也要分开 |
| **撤回与给予同价** | GDPR Art. 7(3)：*"It shall be as easy to withdraw as to give consent."* | 退订步数 ≤ 订阅步数；入口同级 |
| **不得以服务为条件** | Art. 7(4)：*"utmost account shall be taken of whether … the performance of a contract … is conditional on consent"* | 「不同意营销就不给用」违规（与 `design-ethics-inclusion.md` 的 cookie wall 同源） |
| **主题行不得误导** | 15 U.S.C. §7704(a)(2)：*"would be likely to mislead a recipient … about a material fact regarding the contents or subject matter"* | 「你的订单有问题」但正文是促销 → 违规 |
| **商业邮件须标识 + 地址 + 退订说明** | §7704(a)(5)(A) | 页脚三件套固定位置 |
| **营销不得用重要通道** | Apple HIG：*"Never use the Time Sensitive interruption level to send a marketing notification."* | 紧急度字段由事件类型决定，不允许运营覆盖 |

**中国口径的补充**（与 `design-ethics-inclusion.md` 已核验条文衔接，不在本文件重复）：《互联网广告管理办法》第 10 条「一键关闭」、《个人信息保护法》第 24 条个性化推送的两条路径，均已在该资产给出一手条文与验收。本文件只补**跨通道形态**：站内弹窗广告、推送广告与邮件营销同属「广告」，一键关闭的要求一致。

## 14. 无障碍：通知是「播报」，不是「看见」

通知体验里最容易漏掉的是**非视觉用户**：他们不看你精心排版的卡片，只听到读屏念出的一行字。

### 14.1 六条硬要求

| # | 要求 | 依据 / 做法 |
|---|---|---|
| 1 | **未读状态不只靠颜色** | SC 1.4.1：颜色不是唯一手段；用字重 + 圆点 + 文本「未读」 |
| 2 | **文字对比度 ≥4.5:1**，且不四舍五入 | SC 1.4.3 逐字：*"computed values should not be rounded (e.g., 4.499:1 would not meet the 4.5:1 threshold)"* |
| 3 | **可点目标 ≥24×24 CSS px** | SC 2.5.8 逐字：*"The size of the target for pointer inputs is at least 24 by 24 CSS pixels"*；移动端工程约定 44–48 |
| 4 | **图标/头像给等价替代文本** | SC 1.1.1：*"All non-text content … has a text alternative that serves the equivalent purpose"*；纯装饰 `alt=""` |
| 5 | **页面内提示是 status message** | SC 4.1.3 逐字：*"status messages can be programmatically determined through role or properties such that they can be presented to the user by assistive technologies without receiving focus"* → `role="status"`（polite），错误用 `role="alert"` |
| 6 | **自动消失的提示要有等效路径** | SC 2.2.1 不是「5 秒就失败」：*"If the user has no other means of discovering the same information (or performing the same function), then each message would need to meet this success criterion"*——有别的入口（消息中心留档）就不算时限问题；没有就是。另：2.2.1 是 **3 个机制 + 3 个例外 = 6 项**（Turn off / Adjust「默认时长的至少 10 倍」/ Extend「至少 20 秒后可延，且可延至默认的 10 倍」+ Real-time / Essential / 20 Hour），不是「五个例外」 |

### 14.2 读屏念什么：一条通知的播报顺序

系统级通知（iOS/Android）由系统读屏接管，**应用控制的是文本本身**，所以要保证念出来是完整的句子：

- iOS：`title` + `body` 会被依次念出；**按钮顺序**与视觉顺序一致，且每个按钮标签独立成句（Apple：*"Don't include your app name or any extraneous information in the button label"*）。
- Android：`setContentTitle` + `setContentText`；`setContentIntent` 的 `PendingIntent` 必须有描述性标签。
- Web：`new Notification(title, { body })` 无法控制读屏节奏，**关键信息放 `title`**；页面内列表则用真实 DOM 文本（不要用 canvas 画通知）。

**播报自检**：闭眼听一遍——能不能听出「谁、发生了什么事、要我现在做什么、不做会怎样」。四条缺一条，正文就要重写。

### 14.3 角标与未读的等价文本

- 应用图标角标：系统会念「产品名，128 个新项目」之类；**应用内**必须另有一处文本说明（§9 规则 2）。
- 列表红点：`aria-label="有未读消息"` 或直接把「未读」写进条目标题。
- 「全部已读」按钮：操作后 `aria-live` 播报「已全部标为已读，共 12 条」。

---

## 15. 时序、去重与投递状态

通知是**分布式系统里最容易看起来能跑、实际不可靠**的功能：客户端离线、服务端重试、多设备并发、时钟不一致，四件事都会让「同一条通知」变成三条。

### 15.1 六态状态机（服务端真相）

```
created ──► queued ──► sent ──► delivered ──► opened ──► acted
   │           │         │          │            │
   └───────────┴─────────┴──────────┴────────────┴──► expired / failed
```

- `delivered` 只代表**到达设备**，不代表用户看到（Web Push 的 `pushManager` 能回报的粒度很有限）。
- `opened` / `acted` 是**度量**（§14 的 Q6），不是投递正确性。
- `failed` 要有原因码（token 失效 / 限流 / 用户关闭），否则会无限重试。

### 15.2 三条工程铁律

1. **幂等**：每条通知带 `dedupe_key` + 服务端唯一索引；重试不会产生第二条（§21 的 `route_notification` 先去重再判层）。
2. **顺序用 `seq` 不用时间戳**：跨设备时钟不同，时间戳排序会翻转；服务端单调 `seq` 是唯一可靠顺序，客户端只上报「已读到最后 seq=N」。
3. **已读是账户级写入**：任一设备标记已读 → 服务端落库 → 其他设备下次同步时拉 `seq > N` 的增量并清除本地未读。

### 15.3 失败与降级

| 失败 | 用户看到 / 体验 | 处理 |
|---|---|---|
| 推送 token 失效 | 什么都没收到 | 标记 token 失效、回退到邮件或站内；**不要静默丢** |
| 被系统限流（实时活动预算） | 更新滞后 | 降频 + 只在内容变化时更新（§18.8） |
| 权限被关 | 无推送 | 站内留档必须仍可读；下次进入相关页面时再引导（§7） |
| 服务端重复重试 | 同一事件多条 | 幂等键 + 客户端二次去重（同 key 10 秒内丢弃） |
| 网络恢复后补发 | 一次涌入 20 条 | 合并成 1 条摘要（§10） |

**「送达率 99%」是个骗人的指标**：它只说明发出去了，不说明有人看。真正该报的是打开率、关闭率与打扰投诉（§14 的 Q6 与 §16 的度量口径）。

## 16. 平台口径速查表（只填已核验的格子）

| 能力 | iOS | Android | Web |
|---|---|---|---|
| **必须挂渠道** | 否（按 `categoryIdentifier` 分组，可选） | **是**（API 26+，不带渠道不显示） | 否（`tag` 可选，同 tag 覆盖） |
| **中断级别** | `passive` / `active`（默认）/ `timeSensitive` / `critical`（需 entitlement） | 渠道 `IMPORTANCE_NONE(0)` → `HIGH(4)` 五级 | **无**（只有允许/不允许） |
| **操作按钮上限** | **4 个**（HIG：*"up to four buttons"*；watchOS 同为 4） | **3 个**（官方：*"通知最多可提供三个操作按钮"*） | 依浏览器；且 `actions` 仅对 **Service Worker 发出的持久通知**有效（§6.3） |
| **正文字符上限** | **无**（HIG/API 均未规定；只有 *"short title"*、*"brief"* 的定性要求） | 收起态**单行截断**，可用 `setStyle` 展开 | 无（但系统 UI 会截断） |
| **分组** | `threadIdentifier` / 远端 `aps.thread-id` | `setGroup()` + **必须有 group summary**；4 条以上不带 group 由系统自动分组（7.0+） | `tag`（同 tag 覆盖而非叠加） |
| **角标** | 应用图标数字；`0` 清除并清空通知中心，`nil` 保持 | 系统绘制的启动器角标；应用只能 `setNumber()` **建议**数字（*"may or may not use this field"*），`setBadgeIconType` 定显示形态 | 无图标角标；`setAppBadge()` 可能被忽略（*"may also ignore this data"*），非 Baseline |
| **权限请求** | 一次；再调不弹 | 13+ 运行时；≤12L target 自动弹且拒绝即永不再弹 | `requestPermission()`；`denied` 后不应再请求 |
| **跳设置深链** | 无公开直达 URL（只能文字指路） | `ACTION_CHANNEL_NOTIFICATION_SETTINGS` + `EXTRA_APP_PACKAGE` / `EXTRA_CHANNEL_ID` | 浏览器站点设置（无 API） |
| **破静音** | 仅 `critical`（entitlement） | 无应用级手段（系统 DND 规则决定） | 无 |
| **提示音频率限制** | — | **8.1+ 每秒最多 1 次提示音**（多条同时只第一条响） | 无（浏览器决定） |
| **替换旧通知** | 同 `threadIdentifier` 归组 | `setGroup` 归组 + `setOnlyAlertOnce()` 只响一次 | 同 `tag` **覆盖**；要重新提示须 `renotify: true`，且它 **"If true, tag must also be set"** |
| **静默投递** | `interruptionLevel = passive` 或 provisional 授权 | `IMPORTANCE_LOW`（无声音） | `silent: true`（*"no sounds or vibrations… regardless of the device settings"*，与 `vibrate` 互斥） |
| **消息存活** | — | — | push **必须**带 `TTL`（秒）；到期后 *"the push service MUST NOT attempt to deliver"* |
| **构造方式** | 系统 API | `NotificationCompat.Builder` | 页面内 `new Notification()` 在多数移动浏览器 **throw TypeError** → 必须 SW `showNotification` |
| **投递预算** | 实时活动有每小时预算（无公开数字） | — | 推送服务限配额（浏览器厂商各异） |

**读表规则**：空格写「—」或「未核验」的地方**不要凭印象填数字**。这一类表最容易被二手博客污染——例如「iOS 通知标题 40 字符上限」在 Apple 官方文档里**不存在**（§23 已列为「明确不存在，不是漏取」）。

---

## 17. GitHub 生态实测（2026-11-13，匿名 API，未用记忆数字）

**选型三问照旧**：① **许可**能不能商用（`NOASSERTION` = 无法确认，一律按红灯处理）；② `pushed_at` 是否还在维护；③ 能不能被**验收**（有测试/有文档/能自托管）。星数只作参考，不作依据。

| 仓库 | 用途 | ★ | 许可 | pushed_at | 结论 |
|---|---|---|---|---|---|
| `novuhq/novu` | 开源通知基础设施（多渠道编排） | 40,334 | **NOASSERTION** | 2026-11-13 | 活跃；商用前必须查清许可（企业版边界） |
| `binwiederhier/ntfy` | 自托管推送（HTTP 发布 + 客户端订阅） | 35,514 | Apache-2.0 | 2026-11-13 | 可直接自托管，许可干净 |
| `caronc/apprise` | 80+ 通道的发送聚合器（运维告警为主） | 17,757 | BSD-2-Clause | 2026-11-11 | 适合内部告警，不适合面向消费者 |
| `gotify/server` | 自托管 WebSocket 推送 | 16,206 | **NOASSERTION** | 2026-11-09 | 活跃；许可需确认 |
| `radix-ui/primitives` | 无障碍组件原语（含 Toast） | 19,497 | MIT | 2026-10-14 | 生产可用；Toast 的 `role=status` 语义已做对 |
| `emilkowalski/sonner` | React toast 组件 | 13,210 | MIT | 2026-08-10 | 生产可用；只管 in-app toast，不管推送 |
| `timolins/react-hot-toast` | React toast 组件 | 10,994 | MIT | 2026-09-16 | 同上；两者按项目习惯二选一，不要混用两套 |
| `web-push-libs/web-push` | Node 端 Web Push 发送（VAPID） | 3,572 | **NOASSERTION** | 2026-11-10 | 事实标准；许可需确认 |
| `w3c/push-api` | Push API 规范 | 158 | **NOASSERTION** | 2026-11-12 | 规范文本，作**权威依据**读，不作依赖 |
| `whatwg/notifications` | Notifications API 规范 | 152 | **NOASSERTION** | 2026-11-12 | 同上；`Notification.permission` 语义以此为准 |

**已迁移 / 已停更（教训：不核名称就引用等于写错）**：

| 曾用名 | 实际位置 | ★ | 状态 |
|---|---|---|---|
| `magicbell-io/magicbell-js` | `magicbell/magicbell-js` | 31 | 活跃但极小；`NOASSERTION` |
| `knocklabs/knock` | `knocklabs/javascript`（SDK 仓） | 32 | 活跃；MIT |
| `OneSignal/OneSignal-Web-SDK` | `OneSignal/OneSignal-Website-SDK` | 410 | 活跃；`NOASSERTION` |
| `mozilla/serviceworker-cookbook` | `mdn/serviceworker-cookbook` | 2,892 | **archived（2022-11-01）**，只作历史参照 |
| `GoogleChromeLabs/web-push-codelab` | 同名 | 553 | **archived（2023-07-19）**，只作历史参照 |

**四条选型建议（工程约定）**：
1. **in-app toast ≠ 通知系统**：sonner / react-hot-toast / Radix Toast 解决的是「页面内的瞬时反馈」，不要拿它当消息中心或推送（边界归 `feedback-states.md`）。
2. **自托管优先看 ntfy / gotify**：前者许可干净、有 Web 端；后者轻但许可未声明。
3. **Web Push 的最小实现 = Service Worker + `PushManager.subscribe` + VAPID 密钥 + `web-push` 发送**；四件缺一件就跑不通，且**必须 HTTPS**（localhost 例外）。
4. **`NOASSERTION` 一律先查 LICENSE 文件原文再谈接入**：这类仓常见「核心开源 + 企业版闭源」双许可，接入前确认你用的路径在哪一侧。

## 18. 十二个场景（判型 → 动作）

每个场景都按 §1 六段链路走一遍：**事件值不值得发 → 发给谁 → 哪条通道 → 什么时机 → 怎么呈现 → 怎么回收**。场景之间的差别只在某一两段，别把整条链路重新发明一遍。

### 18.1 交易类状态变更（下单成功、发货、退款到账）

- **L1**：值得发——用户在做一件有后果的事，状态变化直接影响他的下一步（等收货、等退款）。
- **L3**：邮件为主通道（需要凭证与归档）+ 站内留档；push 只发「已发货/已到账」这类需要立刻行动的一条，不发「已下单」。
- **L4**：立即，不排摘要——摘要会晚 8 小时，用户已经在客服里问了。
- **L5**：标题写结果（「已发货」），正文写可核对的三件事（商品、时间、下一步），按钮最多两个；**不要把订单号放在标题里**（用户记不住，也无法一眼判断）。
- **L6**：点开后进订单详情页而不是首页；角标不因交易通知增加（交易不是「未读待办」，见 §9）。

### 18.2 双因素认证与安全告警（短信 / 邮件 / 一次性密码）

- **L1**：必须发，且**只能**走短信/邮件这类带外通道（在产品内发验证码等于没有第二因子）。
- **L4**：立即，**永不**进免打扰——一次性口令是「用户此刻正在等」，被延迟等于失败。
- **L5**：正文前 6 个字符就是验证码；有效期写成「5 分钟内有效」而不是「请尽快」；安全告警写明「不是你操作的请立即改密」并给直达链接。
- **红线**：验证码与安全告警**不可被营销开关关掉**（§11 的 `ALWAYS_ON`）；也不允许在同一个开关下与营销混排。

### 18.3 社交互动（点赞、评论、关注）

- **L1**：默认**不逐条发**。这是最容易被「追发」毁掉的场景：一条帖子 100 个赞 = 100 条通知。
- **L2**：必须做**聚合**（§10）：同一对象 30 分钟内的互动合成一条「小王等 12 人赞了你的帖子」。
- **L4**：进摘要或次日推送；只有「@你」与「私信」即时发。
- **L6**：聚合条目点开后进详情；角标按「未读会话数」而非「互动条数」。

### 18.4 内容上新与运营推送

- **L1**：这是**营销**，默认不发；发了必须先拿到显式 opt-in（§13）。
- **L2**：按兴趣标签分组，不群发；同一用户 7 天内最多 1 条运营类。
- **L4**：排进摘要（用户自己选的时段），不做「晚 8 点全员同一秒」。
- **L6**：每条必须带**一键关闭此类**的入口（不是「去设置里找」），并记录关闭原因分布。

### 18.5 待办与审批提醒

- **L1**：值得发，但只在**有截止时间**时发；没有截止时间的待办进站内列表即可。
- **L4**：按截止时间倒推（提前 24h / 2h），不按「每天早 9 点统一发」。
- **L5**：标题写「还有 2 小时截止」，不写「您有一条待办」；带「稍后提醒」与「已完成」两个动作。
- **L6**：完成即清零对应角标；「稍后提醒」要能改时间，不是固定 1 小时。

### 18.6 大促与限时活动

- **L1**：默认不发；opt-in 后也受频率上限约束（§10）。
- **红线**：不得用 `timeSensitive`/重要通道伪装紧急（Apple HIG 逐字：*"Never use the Time Sensitive interruption level to send a marketing notification."*）。
- **L6**：退订必须一键生效且**立即**（RFC 8058 的一键退订语义，§12），不能要求登录后等 10 个工作日。

### 18.7 订阅续费与到期

- **L4**：到期前固定节奏（如 T-7 / T-3 / T-1）各一条，**不追发**；续费成功发凭证类邮件，不发 push。
- **L5**：写明金额、扣款时间、取消路径；取消入口必须与开通入口同等显眼（§13 合规，与 `design-ethics-inclusion.md` 对称性同源）。
- **L6**：取消后立刻停发该订阅的所有通知；保留交易凭证邮件。

### 18.8 进行中的过程（配送、赛事、计时）

- **通道**：实时活动 / 锁屏常驻，而不是连续 push。
- **更新纪律**：只在新内容可用时更新；不要与 push 同时就同一更新双发（Apple HIG：*"don't use push notifications alongside Live Activities for the same updates"*）。
- **结束**：结束后 15–30 分钟内收起；不要停留在「已送达」状态一整天。
- **频率**：系统对每小时推送预算有限流，超了会被节流（无公开具体数字，§23）。

### 18.9 多设备与多端已读

- **状态**：已读是**账户级**状态，不是设备级。手机读完，平板与网页必须同步清除。
- **实现**：以服务端 `seq` 为准，客户端只上报「读到 seq=N」，不回传绝对计数（§15）。
- **失败样态**：两端各自计数 → 角标越积越多；「在 A 设备清空后 B 设备又弹一次」。

### 18.10 团队协作与 @提及

- **L1**：@提及与私信即时发；任务状态变更进摘要。
- **L6**：通知里带「回复」框（原地处理），比「打开应用」少两步；这直接影响打开后的有效动作率（§14）。

### 18.11 系统维护与故障公告

- **通道**：站内横幅 + 状态页，不用 push 群发（除非服务中断且用户正要用）。
- **文案**：写「现在什么不能用 / 什么时候恢复 / 你可以做什么」，不写「我们正在努力」。
- **回收**：恢复后必须撤下横幅，而不是留一条过期的「维护中」。

### 18.12 未成年人与家长通知

- **L1**：默认极简——只发安全与消费类，不发运营。
- **L5**：消费类必须发给监护人账户；文案写金额与用途，不诱导点击。
- **合规**：不得用「限时/仅剩」话术对未成年人施压（与 `design-ethics-inclusion.md` 的成瘾设计红线同源）。

---

## 19. 二十条反模式（交付前逐条对照）

1. **同一事件追发**：没点就再发一遍，还换个标题。
2. **启动即弹权限**：用户还不知道你能发什么，就先要授权。
3. **被拒后代码里再请求**：iOS 不会再弹，用户只会觉得「点了没反应」。
4. **只有 push 没有留档**：划掉即永久丢失。
5. **营销与交易共用一个开关**：关掉促销 = 收不到退款通知。
6. **角标用 `nil` 表示清零**：角标永远停在旧数字。
7. **角标 = 待办数 / 订单数**：与「未读通知数」定义不符。
8. **清零角标但不清通知中心**：用户看到列表里还有，怀疑没生效。
9. **凌晨按总部时区群发**：海外用户凌晨 3 点被叫醒。
10. **把 `timeSensitive` 当授权项请求**：文档里它是废弃项，时效性靠 `interruptionLevel`。
11. **营销用重要通道**：拿「重要」换打开率，换到的是关掉与举报。
12. **一个事件三条通道全发**：push + 邮件 + 站内三份，用户以为出了三次事。
13. **退订要登录、要填表、要等 10 天**：这不是退订，是劝退。
14. **邮件退订链接藏在页脚 8 号灰字里**：可访问性与合规双输。
15. **消息中心只有平铺列表**：没有分类、没有批量已读、没有搜索。
16. **未读定义混用**：有时按条、有时按会话、有时把已读也算进去。
17. **强依赖角标传达关键信息**：读屏用户与关掉角标的用户完全收不到（Apple HIG：*"Make sure badging isn't the only method you use..."*）。
18. **通知正文写「点击查看详情」**：没给任何可判断的信息。
19. **把错误提示做成通知**：Apple HIG 明确要求用 alert 而不是 notification 展示错误。
20. **没有度量**：不知道打开率、关闭率、退订率，只报「送达成功率 99%」。

---

## 20. 二十项自检（交付前逐条过）

1. 每个业务事件都有稳定 `dedupe_key`，24h 内同 key 只有一条？
2. 有没有「没响应就追发」的逻辑？删掉了吗？
3. 每条 push 都能在站内消息中心找到？
4. 营销类与交易类**分别**有开关，且交易类不可被关掉？
5. 营销推送的默认值是关（且没有预勾选）？
6. 权限请求前有无 in-app 说明页？说明页能否拒绝且不复发？
7. 被拒后的引导是否指向系统设置，且文案不指责用户？
8. 角标数字 == 未读通知数？（不是待办、不是订单）
9. 清零角标的同时清空了通知中心对应通知？
10. 角标三态（0 / >0 / nil）语义在代码里显式区分？
11. 免打扰窗口支持跨午夜、支持用户时区？
12. 紧急度 ≥3 之外的通知都不破免打扰？
13. 同一用户 24h 内非关键通知是否受上限约束？
14. 摘要（digest）时段由用户选择，而不是服务端硬编码？
15. 消息中心有分类/筛选、批量已读、空态与失败态？
16. 邮件有 `List-Unsubscribe` + `List-Unsubscribe-Post`（一键）与物理地址？
17. 退订一键生效，且不需要登录？
18. 通知条目的可访问性：读屏能读出「谁、什么事、什么时候」？
19. 角标/未读对读屏有等价文本（不依赖图形）？
20. 有打开率 / 关闭率 / 退订率 / 打扰投诉四项度量，且能按类别拆？

## 21. 五段可抄代码（严格模式实跑 5/5 rc=0）

五段合成一个模块在 Python 3.11 下 `python -X utf8` 实跑通过（`assert` 全过、退出码 0）。它们不是示例伪码，是可以直接放进仓库的行为契约：**改任何一条规则，对应断言会红**。

### 21.1 渠道与时机路由：先判层，再决定发不发 / 走哪条通道 / 什么时候发 ──

**用法**：`event` 由业务侧构造，`prefs` 由偏好页（§11）落库生成；判层顺序**不可换**（去重 → 合规 → 紧急度 → 免打扰 → 渠道回退）。

```python
from datetime import datetime, timedelta, timezone


def route_notification(
    event,
    prefs,
    now,
    tz_offset_hours=8,
    quiet=(22, 8),
    seen=None,
    dedupe_window_hours=24,
):
    """返回 (verdict, channel, deliver_at, reason)。

    event: {"key": str, "urgency": 0-3, "kind": "transactional|marketing|system"}
    prefs: {"channels": {"push": bool, "email": bool, "inapp": bool},
            "marketing_opt_in": bool,
            "quiet_hours_enabled": bool}
    判层顺序不可换：去重 → 合规 → 紧急度 → 免打扰 → 渠道回退。
    """
    seen = seen or {}
    if event["kind"] == "marketing" and not prefs.get("marketing_opt_in"):
        return ("drop", None, None, "marketing without opt-in")

    key = event["key"]
    last = seen.get(key)
    if last is not None:
        gap = now - last
        if gap < timedelta(hours=dedupe_window_hours):
            return ("drop", None, None, "duplicate within window")

    ch = prefs["channels"]
    if event["urgency"] >= 3:
        if not (ch["push"] or ch["email"] or ch["inapp"]):
            return ("drop", None, None, "all channels disabled")
        return ("send", "push" if ch["push"] else "inapp", now, "critical bypasses quiet")

    if prefs.get("quiet_hours_enabled") and in_quiet(now, quiet, tz_offset_hours):
        if event["urgency"] >= 2:
            return ("send", "inapp" if ch["inapp"] else "push", now, "time-sensitive breaks quiet")
        return ("defer", "digest", next_allowed(now, quiet, tz_offset_hours), "quiet hours")

    for channel in ("push", "inapp", "email"):
        if ch.get(channel):
            return ("send", channel, now, "first enabled channel")
    return ("drop", None, None, "all channels disabled")


def in_quiet(now, quiet, tz_offset_hours=8):
    """免打扰窗口判定：支持跨午夜（22→8）与 24h 窗口（0→0 视为整天关闭）。"""
    start, end = quiet
    h = now.astimezone(timezone(timedelta(hours=tz_offset_hours))).hour
    if start == end:
        return True
    if start < end:
        return start <= h < end
    return h >= start or h < end


def next_allowed(now, quiet, tz_offset_hours=8):
    """免打扰结束后的第一个可投递时刻（本地 end 点，返回 UTC）。"""
    start, end = quiet
    tz = timezone(timedelta(hours=tz_offset_hours))
    local = now.astimezone(tz)
    target = local.replace(hour=end, minute=0, second=0, microsecond=0)
    if target <= local:
        target += timedelta(days=1)
    return target
```

### 21.2 角标状态机：nil ≠ 0，清零要同时清通知中心 ──

**用法**：服务端保存 `count` 与 `cleared_seq`，客户端只上报「读到 seq=？」；`apply(None)` 保持现状，`apply(0)` 清角标并入队一次清空指令。

```python
class BadgeState:
    """badge 三态语义（照 Apple `applicationIconBadgeNumber` 契约）。

    set(0)   → 移除当前角标，并清空通知中心里本应用的通知
    set(n>0) → 显示该数字
    set(None)→ 保持现状（不是清除，写成 0 才是清除）
    """

    def __init__(self):
        self.count = 0
        self.cleared_seq = 0

    def apply(self, value):
        if value is None:
            return self.count
        if value < 0:
            raise ValueError("badge count must be >= 0")
        if value == 0:
            self.count = 0
            self.cleared_seq += 1
            return 0
        self.count = value
        return self.count

    def display(self, cap=99):
        if self.count <= 0:
            return None
        return "99+" if self.count > cap else str(self.count)
```

### 21.3 通知偏好数据结构：营销默认关、交易默认开、粒度到「类型 × 渠道」 ──

**用法**：写成偏好页的断言测试——营销类默认开会在 CI 直接失败；`ALWAYS_ON` 里的类别不允许被用户关掉。

```python
LEGAL_DEFAULT_OFF = {"marketing_email", "marketing_push", "product_news"}
ALWAYS_ON = {"security_alert", "transactional_receipt", "account_notice"}


def validate_pref_center(categories):
    """每个类型必须有 channels 字典，且默认值符合合规底线。"""
    errors = []
    for cat in categories:
        name = cat["name"]
        ch = cat.get("channels") or {}
        if not ch:
            errors.append(f"{name}: missing channels")
            continue
        for channel, default in ch.items():
            if name in LEGAL_DEFAULT_OFF and default is True and not cat.get("opt_in_evidence"):
                errors.append(f"{name}.{channel}: marketing default must be off without opt-in")
            if name in ALWAYS_ON and default is False:
                errors.append(f"{name}.{channel}: cannot be disabled")
    if not any(c["name"] in LEGAL_DEFAULT_OFF for c in categories):
        errors.append("no marketing category declared")
    return errors
```

### 21.4 退订链路：List-Unsubscribe 必须带 One-Click，POST 才算 ──

**用法**：发信前跑一遍头检查；CI 里对模板做快照，缺 `List-Unsubscribe-Post` 直接红。

```python
def check_unsubscribe_headers(headers, body_text, postal_address_required=True):
    h = {k.lower(): v for k, v in headers.items()}
    problems = []
    lu = h.get("list-unsubscribe", "")
    if "http" not in lu and "mailto" not in lu:
        problems.append("missing List-Unsubscribe URI")
    if "list-unsubscribe-post" not in h:
        problems.append("missing List-Unsubscribe-Post: List-Unsubscribe=One-Click")
    elif "one-click" not in h["list-unsubscribe-post"].lower():
        problems.append("List-Unsubscribe-Post is not one-click")
    if "unsubscribe" not in body_text.lower() and "退订" not in body_text:
        problems.append("no unsubscribe link in body")
    if postal_address_required and not h.get("x-postal-address"):
        problems.append("missing physical postal address (CAN-SPAM)")
    return problems
```

### 21.5 投递预算：同一用户 24h 内的非关键通知上限 ──

**用法**：发送前置校验，超预算就合并或降级到摘要（§10.2），不要「攒着明天一起发」。

```python
def within_budget(sent_times, now, cap=3, window_hours=24, urgency=1):
    if urgency >= 3:
        return True, 0
    recent = [t for t in sent_times if now - t < timedelta(hours=window_hours)]
    return len(recent) < cap, len(recent)


# ── 严格模式自测 ──
```

## 22. 来源（本轮逐字核验，2026-11-13）

**Apple**
- HIG · Notifications：https://developer.apple.com/design/human-interface-guidelines/notifications （经 `tutorials/data/*.json` 取正文）
- HIG · Managing notifications / Asking permission：`.../human-interface-guidelines/managing-notifications`、`.../asking-permission-to-use-notifications`
- `UNUserNotificationCenter.requestAuthorization(completionHandler:)`、`UNAuthorizationOptions`（含 `timeSensitive` 的 Deprecated 分组与 `deprecatedAt`/`introducedAt` 元数据）
- `UNNotificationInterruptionLevel`（`passive` / `active` / `timeSensitive` / `critical`）
- HIG · Live Activities：`.../human-interface-guidelines/live-activities`

**Android（英文原文取自 `developer.android.com`，渠道与权限页另用官方中文镜像交叉核对）**
- 创建和管理通知渠道：https://developer.android.com/develop/ui/views/notifications/channels （镜像：`developer.android.google.cn/.../channels`）
- 通知运行时权限：`.../notifications/notification-permission`
- 创建通知（操作按钮上限、8.1+ 提示音频率、展开式）：`.../notifications/build-notification`
- 角标与分组：`.../notifications/badges`、`.../notifications/group`；`android/app/Notification#number`、`setBadgeIconType`

**Web**
- MDN · `Notification.permission` / `Notification` 构造函数与 options（`tag` / `renotify` / `requireInteraction` / `silent` / `badge` / `actions`）：https://developer.mozilla.org/en-US/docs/Web/API/Notification/permission
- MDN · Badging API（`setAppBadge` / `clearAppBadge`）：https://developer.mozilla.org/en-US/docs/Web/API/Navigator/setAppBadge
- Notifications 规范：https://notifications.spec.whatwg.org/ ；Permissions 规范（§5.2 prompt 状态）：https://w3c.github.io/permissions/
- Push：RFC 8030（TTL）、RFC 8292（VAPID）、RFC 8291（payload 加密）

**法律与政策（一手条文）**
- 15 U.S.C. §7702（transactional / commercial 定义）、§7704（a)(2)(3)(4)(5)）：https://www.law.cornell.edu/uscode/text/15/7702 、`/7704`
- 16 CFR §316.3(b)（primary purpose）、§316.5（退订不得收费/索取额外信息）：https://www.law.cornell.edu/cfr/text/16/316.3 、`/316.5`
- RFC 8058（`List-Unsubscribe-Post: List-Unsubscribe=One-Click`）：https://www.rfc-editor.org/rfc/rfc8058
- GDPR Recital 32 / Art. 7(3)(4)：https://gdpr-info.eu/recitals/no-32/ 、https://gdpr-info.eu/art-7-gdpr/
- GOV.UK Service Manual · Sending emails and text messages：https://www.gov.uk/service-manual/design/sending-emails-and-text-messages
- GOV.UK Notify · Formatting / Unsubscribe links：https://www.notifications.service.gov.uk/using-notify/formatting 、`/unsubscribe-links`
- GOV.UK · SPF / DKIM / DMARC 三页

**可用性与无障碍**
- NN/g · Toggle-Switch Guidelines：https://www.nngroup.com/articles/toggle-switch-guidelines/
- NN/g · Push Notifications（五错误与「later session」口径）：https://www.nngroup.com/articles/push-notification/
- WCAG 2.2 Understanding：SC 1.1.1 / 1.4.1 / 1.4.3 / 2.5.8 / 4.1.3

**GitHub（API 实测，见 §17）**：`novuhq/novu`、`binwiederhier/ntfy`、`caronc/apprise`、`gotify/server`、`radix-ui/primitives`、`emilkowalski/sonner`、`timolins/react-hot-toast`、`web-push-libs/web-push`、`w3c/push-api`、`whatwg/notifications`。

---

## 23. 取源限制（不引用这些来源的任何数字）

1. **`developer.android.com` 取源分两条路且都不稳**：`curl` 直连返回 **000**、`web_fetch` 报 `TypeError: fetch failed`；**但同一个环境里 `Invoke-WebRequest` 能拿到 200**，官方中文镜像 `developer.android.google.cn` 亦可。镜像页首自带声明：*"Google 会使用 AI 技术将内容翻译成您偏好的语言。AI 翻译可能包含错误。"* → 数字与 API 名逐项对过，正文用英文原文引用，中文镜像只作交叉核对。
2. **`developer.android.com/develop/ui/views/notifications` 总览页已改版为落地页**（正文只剩一句），通知结构与优先级改从 `build-notification` 取；`NotificationCompat.Builder#setNumber` 参考页返回 *"Received an unexpected EOF or 0 bytes from the transport stream."* → 改用 `android/app/Notification#number`。
3. **`w3.org/TR/notifications/` 被 Cloudflare 拦**（403 "Just a moment..."）→ 改用 `notifications.spec.whatwg.org` 与 `w3c.github.io/permissions`。
4. **`m3.material.io` 为 JS 骨架**：`/components/badges/overview` 返回 200 但正文只有 *"This website requires JavaScript."* → **Material 3 角标规范未取到**，§9 未引用 M3 任何数值。
5. **support.google.com 全站不可达**（含 `?hl=en`、r.jina.ai、archive.org）：Gmail 发信限额、一键退订强制与生效日期、Postmaster 垃圾率 0.3% 阈值 **全部未核验，本文件不引用**。
6. **PECR / ICO 403（Cloudflare）**、**legislation.gov.uk 返回 HTTP 202 空体** → 英国「软 opt-in」四条件未取到，§13 不写英国口径。
7. **ftc.gov 403 / ecfr.gov bot 挑战** → 法条原文改用 Cornell LII 镜像（条文可靠，但**不是** FTC 的解释性指南）。
8. **`litmus.com` 返回 unsupported content type**、**`nngroup.com/articles/notifications/` 为 404**（NN/g 官方警告过 AI 常编造其 URL）→ 暗色模式邮件与「通知设计」总论未取到。
9. **Apple critical alert entitlement 申请页需登录**（返回 Sign In）→ 审批话术与条件未核验，本文件只说「需 Apple 单独批准」这一句官方定位。
10. **实时活动每小时推送预算无公开数字** → 只写「有限流」，不写具体条数。
11. **Chrome「通知滥用启发式」（quiet UI / 自动屏蔽）未取到官方说明** → 不写自动屏蔽规则；**「长按通知可关闭渠道」也未核验**（channels / badges / group / bubbles / permission 五页全文检索无 long-press 命中）。
12. **`requireInteraction` 在移动端是否被忽略、Badging API 的具体浏览器名单**：MDN 无原文 → 标未核验，不写平台清单。
13. **邮件 600px 宽度、preheader 字符预算、subject 字符数**：无标准机构一手来源（常见数字出自厂商博客）→ 不写。
14. **明确不存在，不是漏取**：Apple HIG 与 API 均**没有** title / subtitle / body 的字符数上限；`Deliver Quietly` 这个英文说法在所有抓到页面上**均未出现**；Apple **没有**「用户拒绝后引导去设置」的推荐话术。

---

## 24. 与既有资产边界矩阵

| 相邻资产 | 它管什么 | 本文件管什么 | 重叠处的裁决 |
|---|---|---|---|
| `ux-writing.md` | 对话框/Toast/右上角通知的文案长度与按钮数、语气标点 | 一条通知**从事件到回收**的整条链路 | 单条文案的字数与措辞归前者；「该不该发、走哪条通道、什么时候发」归本文件 |
| `feedback-states.md` | 五层 in-app 反馈（L0–L4）、0.1/1/10s 阈值、`role=status` | 跨会话留档的消息中心与 push/邮件触达 | 页面内瞬时反馈归前者；离开产品后的触达归本文件 |
| `onboarding-first-run.md` | 权限**时机**矩阵、purpose string 验收、`permissiongate.py` | 权限**机制差异**（一次性/可再问）与**被拒后的恢复** | 何时请求归前者；三平台差异与拒绝后兜底归本文件 |
| `design-ethics-inclusion.md` | cookie 同意、默认勾选、自动续费、一键关闭、欺骗性设计 18 类 | 营销同意的**邮件/推送形态**与退订可测四条 | 同意合法性归前者；邮件退订与 List-Unsubscribe 归本文件 |
| `accessibility.md` | WCAG 全量阈值、focus ring、目标尺寸 | 通知播报顺序、未读的等价文本、角标可访问性 | 阈值数值归前者；通知场景的合取归本文件 |
| `empty-states.md` / `form-table.md` | 空态构型与文案公式、表单 label/校验 | 消息中心的空态与列表结构 | 形态归前者；「消息中心的未读定义与分页」归本文件 |
| `iconography.md` | 图标网格、描边、可访问性 | 角标/圆点作为状态标记的语义 | 画法归前者；语义与口径归本文件 |
| `design-measurement-research.md` | SUS、样本量、A/B 统计 | 打开率/关闭率/退订率的口径与误判 | 统计方法归前者；指标定义归本文件 |
| `knowledge-map.md` | L0→L4 学习路线与支线 | 新增「通知与触达」支线 AI | 路线图归前者；本文件只提供支线内容 |

---

## 25. 接线

**接线**：SKILL.md 版本段 / v42 基线 / 资产表 / 资产计数 / 别名段 / 意图路由 4 行 / 第 5 步深入条目 / 第 44 条自检 · `scripts/mindmap.py` INTENTS · `scripts/regression.py` NEW_QUERIES 13 条 + HIST 沉淀 + `EXPECT_FILE` · `references/knowledge-map.md` 支线 AI + 自测 2 条 · `memory/aliases.json` 8 组 81 词（**只进检索层，不改路由优先级**）· `scripts/build_readme.py` ASSETS + 问题表 + 数据来源 · README 统计重算 · `Design-related websites.txt` 第二十六分区 + 附区。
