# 实时协作与多人编辑（Real-time Collaboration & Presence）

> 快照 2026-11-16 · 每日升级 #43（v46→v47）· 主题：Realtime Collaboration / Presence / Multiplayer Undo / Comment Threads / Permission Matrix / Offline & Reconnect
> 取源：Figma 工程博客（Evan Wallace，2019-10-16）· Yjs `awareness.js` / `UndoManager.js` 源码与 relative-position 文档 · Automerge sync 模块文档 · Liveblocks Canvas / Presence / React API 文档 · WCAG 2.2 SC 4.1.3 Understanding · MDN `aria-live` · Figma Help 文件权限与评论 · GitHub API 实测 10 个库（2026-11-16）。规范数值逐字引原文，无官方来源的建议值显式标「工程约定」。
>
> **边界纪律（先读这段，避免误路由）**：本文件只管「两个以上的人同时改同一份内容时，谁看到什么、谁能改什么、冲突怎么落地、断线怎么回来」。**设计交付**（设计稿→开发的六关卡、spec sheet）归 `handoff-collaboration.md`；**保存状态 / toast / 加载五态** 归 `feedback-states.md`；**通知通道、偏好与去重** 归 `notifications-messaging.md`；**指针、拖拽、命中区的通用规则** 归 `direct-manipulation.md`；**WCAG 全量口径** 归 `accessibility.md`（本文件只补 SC 4.1.3 在协作场景的落地）；**模态与遮挡** 归 `overlays-modality.md`；**流式生成状态的播报** 归 `conversational-generative-ui.md`；**度量与实验口径** 归 `design-measurement-research.md`；**组件受控/非受控契约** 归 `component-api-design.md`。

---

## §0 一句话立场

**协作不是「让别人也能改同一个文件」，是「在谁都无法实时看见对方意图的情况下，仍让每个人相信自己看到的是当前真相，并知道下一步该做什么」。**

三条裁决：

1. **冲突粒度必须先于协作 UI 决定。** 数据层是「属性级 last-writer-wins」，UI 就只能承诺「最后一次写入生效」，不能承诺「两人同时改同一段文字会被合并」。Figma 原文把后果说得最清楚：文本值 B 被一人改成 AB、同时被另一人改成 BC，结果**只能是 AB 或 BC，永远不会是 ABC**。选型决定文案，不是文案弥补选型。
2. **Presence 是「临时真相」，不是数据。** 它随连接生灭，不能用来做审计、归属、权限判断，更不能把「头像还亮着」当成「人还在」。Yjs 的默认判离线阈值是 **30 秒**；这 30 秒里系统必须假装对方可能还在，但「正在编辑」的锁不能跟着等 30 秒。
3. **多人撤销必须只撤自己的。** 任何「全局 Undo」在并发下都会撤掉别人的工作；Yjs `UndoManager` 默认只跟踪本地 origin，源码注释逐字写着 *"By default, the UndoManager will never overwrite remote changes."*

判层先答三问（§1），再选模型（§2–§3），最后才画头像和光标（§4 起）。**顺序不能换**：先做一套漂亮的光标，再回头问「冲突怎么算」，一定会给已经画好的光标找理由。

---

## §1 六层判层：从「谁能改」到「断线怎么回来」

协作体验是一条会失败的链路。先把问题定位到层，再决定改协议、改状态、改 UI 还是改权限。

| 层 | 这一层回答 | 典型失败 | 主要归属 |
|---|---|---|---|
| **L1 文档模型** | 文档是什么？对象如何寻址、如何排序、如何删除？ | 用整数 index 排序，并发插入后顺序错乱；删除对象把评论一起带走 | 本文件 §3 |
| **L2 同步协议** | 谁有权威？离线能不能改？重连怎么对齐？ | 中心权威却宣传「离线可编辑」；CRDT 却按时间戳覆盖 | 本文件 §2 / §10 |
| **L3 存在层** | 谁在、在哪、在选什么、在输入什么？ | 光标 100ms 才动一次；头像不消失；同一人两个光标 | 本文件 §4 |
| **L4 冲突与合并** | 两人改同一处时，用户看到什么、能做什么？ | 静默覆盖不提示；提示了却没有「恢复我的版本」 | 本文件 §6 |
| **L5 权限与分享** | 谁能看、谁能评、谁能改、谁能再分享？ | 「可评论」被实现成「可编辑」；移除成员后 socket 还连着 | 本文件 §9 |
| **L6 回收** | 评论、撤销、历史、离线队列如何收尾？ | 对象删了评论变孤儿；撤销撤到别人；离线改动静默丢失 | 本文件 §7 / §8 / §10 |

**判层三问**：

1. 用户抱怨的是「看不到别人」还是「别人改了我的」？——前者在 L3，后者在 L1/L4，修法相反：一个加信号，一个减写入。
2. 这个功能在**断网 30 秒**后还能不能正确工作？答不上来，说明 L2/L6 没设计完。
3. 关掉协作功能后，这份文档还能不能被一个人正常编辑？不能，说明协作被做成了唯一路径，属于结构性风险。

---

## §2 协作模型选型：三种路线与它们能承诺的话

| 维度 | 中心权威 + 属性级 LWW | OT（Operational Transform） | CRDT（Yjs / Automerge） |
|---|---|---|---|
| 权威 | 服务器定顺序 | 服务器或中心节点变换操作 | 无中心，副本最终收敛 |
| 离线编辑 | 可（Figma：离线任意久，重连重放） | 难，操作历史依赖上下文 | 天然支持 |
| 同段文本并发 | **不合并**（AB/BC 只留一个） | 可合并，但实现与调试复杂 | 可合并（字符级） |
| 冲突语义 | 最后到达服务器的写入赢 | 操作变换后合并 | 自动合并，语义由数据类型决定 |
| 实现成本 | 低—中 | 高 | 中—高（但库成熟） |
| 适用 | 设计工具、结构化属性、图形画布 | 早期文本协同 | 富文本、代码、离线优先、P2P |

**Figma 的选择与理由（原文）**：Figma 明确说 *"Figma isn't using true CRDTs though."*——因为 CRDT 是为「没有中心权威」的去中心化系统设计的，有不可避免的性能与内存开销；Figma 有中心服务器，可以省掉这层开销。它也明确不用 OT：*"Since Figma isn't a text editor, we didn't need the power of OTs and could get away with something less complicated."* 它的 LWW 甚至不需要时间戳：*"except we don't need a timestamp because the server can define the order of events."*

**Automerge 的同步循环（原文）**：同步协议假设两个对等端之间是**可靠、有序的流**；每一端为每个对等端维护一个 `State`，记录对方 heads 与是否有在途消息；`generate_sync_message` / `receive_sync_message` 往返，直到双方都没有新消息（`None`）为止。

### 选型裁决（可直接回答「我们该用哪个」）

- **只做图形/属性/图层**（设计工具、白板、表格单元格）→ 中心权威 + 属性级 LWW。UI 文案禁止出现「自动合并」。
- **富文本、代码、需要离线优先**→ CRDT（Yjs 的 `Y.Text` / Automerge），或成熟 OT 服务。UI 可以承诺「合并」，但要为「合并后读起来怪」准备解释入口。
- **既要图形又要长文本**→ 分层：画布走 LWW，文本块走 CRDT；不要用一个模型硬套两种语义。
- **不能接受中心服务器**（P2P、本地优先）→ 只能 CRDT；同时接受「没有唯一真相时刻」带来的产品解释成本。
- **只是「多人查看 + 一个人改」**→ 不要上 CRDT。只读广播 + 编辑锁足够，复杂度差一个数量级。

---

## §3 文档模型：树、属性与 fractional index

Figma 把文档抽象成 `Map<ObjectID, Map<Property, Value>>`，并把它当树用。这个模型的设计含义比实现细节重要：

### 3.1 属性是冲突的最小单位

- 两个客户端改**同一对象的同一属性**→ 冲突，服务器最后收到的值赢。
- 改**同一对象的不同属性**→ 不冲突。
- 改**不同对象的同一属性**→ 不冲突。

**UI 规则**：属性面板的每次提交应当是一个**完整属性值**（例如 `x=120`），不要把一个拖动过程拆成无数中间值发给别人；也不要把「标题 + 描述」打包成一个属性，否则改描述会顶掉别人刚改的标题。

### 3.2 元素 ID 必须由客户端生成

Figma 给每个客户端一个唯一 client ID，新元素 ID 里带这个 ID。原因很实际：**离线时也必须能创建对象**，等服务端分配 ID 就做不到。代价是：ID 不是连续数字，排序不能依赖 ID。

### 3.3 创建与删除是 LWW set，删除会带走属性

对象是否存在，本身就是一个 LWW 布尔属性；删除对象会把它在服务器上的**所有属性**删掉。Figma 把被删对象的属性只留在**执行删除的那个客户端的 undo buffer** 里，由它负责恢复——这样长文档不会因为反复删除而膨胀。

**设计含义**：
- 别人删了对象，你本地的「撤销删除」未必能恢复全部属性；UI 不要把「撤销」说成「恢复原样」。
- 评论、标注、历史版本如果挂在对象 ID 上，对象删除后必须有**孤儿处理**（§8.4），不能静默消失。

### 3.4 父子关系与排序：parent + position 必须原子

Figma 把「父链接」存成子对象上的一个属性，于是可能出现 A 是 B 的父、B 又是 A 的父的环。服务器会拒绝造成环的 parent 更新；客户端不能拒绝服务器，所以会短暂出现「两个对象互相 parent」，Figma 的处理是把它们暂时移出树，等服务端拒绝后再归位。原文承认这会让对象**短暂消失**，但认为这是极罕见的临时问题，不值得做更复杂的客户端断环。

排序用 **fractional indexing**：子对象位置是 0 到 1（不含端点）之间的分数，按位置排序；插到两者之间就取平均值。**关键约束**：parent 链接与 position 必须存成**同一个属性**，否则「换父节点」和「换位置」会被拆成两次更新，中间态会被别人看到。

**工程规则**：
- 任何「有序列表的协同插入」都不要用整数 index；用 fractional index 或 CRDT list。
- 每次换父/换序是一个原子操作；UI 上表现为一次移动，不要先删后加（否则评论锚点与撤销历史都会断）。
- 分数精度会耗尽：连续在同一位置插入约 50 次后，double 的有效位可能不足以再取平均——实现要能重新平衡（工程约定，需按实际精度压测）。

### 3.5 文本为什么不能走属性 LWW

AB/BC 的例子说明：属性 LWW 对「整段文本」就是「整段替换」。如果产品需要两人同时编辑同一段文字，必须把文本拆成 CRDT 字符序列，或退一步做**块级/字段级锁**，并在 UI 上明确「这段文字同一时间只有一个人能改」。**不要**用属性 LWW 实现文本编辑然后再加一个「合并中」的假状态。

---

## §4 存在层（Presence）：五种信号，各自证明什么

Presence 是「临时状态」：Liveblocks 的定义是每个连接一个 JSON 对象，实时更新，**连接结束就消失**；永久内容放 Storage。Yjs 的 awareness 同样是**非持久**数据（光标、用户名、状态），把状态置 `null` 表示离线。

| 信号 | 证明什么 | 不证明什么 | 消失时机 |
|---|---|---|---|
| 在线头像 | 这个连接还在 | 人还在看、还在工作 | 连接断开即时；判离线有 30s 容忍（§10） |
| 光标 | 对方指针大概在哪 | 对方正在改什么 | 指针离开容器 / 断开 |
| 选区 | 对方选中了哪个对象/字段 | 对方拿到了编辑锁 | 失焦 / 切换选择 / 断开 |
| 正在输入 | 对方最近有输入 | 输入内容、是否会提交 | 1s 无输入或失焦（Liveblocks 示例） |
| 当前工具 | 对方处于什么模式 | 对方下一步动作 | 切换工具 / 断开 |
| 视口跟随 | 对方正在看哪一块 | 对方理解了什么 | 用户关闭跟随 / 断开 |

### 4.1 头像栈（Avatar Stack）

- **上限 5 + `+N`**：Liveblocks 的 `AvatarStack` 提供 `max`，超出折叠为 `+N`；多标签页的同一用户会**去重**。
- **排序稳定**：按加入房间时间或固定字母序，不要按「最近活跃」实时重排——每次重排都会让用户重新认人。
- **颜色来自服务端 user info，不来自客户端 presence**：Liveblocks 明确建议名字、颜色、头像放 user info（来自数据库、跨连接一致、客户端不能伪造），presence 只放会消失的状态。把颜色放进 presence，等于允许任何人冒充别人的颜色。
- **离线受邀者可显示，但要区分**：Liveblocks 允许传 `userIds` 把「被邀请但不在线」的人加进栈；这类头像应当空心/降饱和，并在 tooltip 写「未在线」。
- **名字截断**：中文 6 字、英文 12 字符后省略；tooltip 给全名 + 角色。
- **可达性**：头像栈是一个列表，不是一堆 `img`；键盘可聚焦，读屏读「3 人在线：A、B、C」。

### 4.2 光标（Live Cursors）

- **坐标用容器相对百分比，不用视口像素**：Liveblocks 的 `Cursors` 组件就是这么做的，原文 *"Cursor coordinates are percentage-based relative to the container, so they stay accurate across screen sizes"*。用 `clientX/clientY` 直接广播，对方一缩放/滚动就全错。
- **平滑用 spring 插值**：收到的位置是离散采样，渲染层做插值，而不是把每次采样都当成一次跳变。
- **频率**：Liveblocks 的 `throttle` 默认 **100ms**，允许 **16–1000ms**，16ms 即 60fps。工程建议：光标 20–30Hz 足够顺滑，60Hz 只在「对方正在精确绘图」时有意义；用 60Hz 广播 20 个光标，就是每秒 1200 条消息。
- **上限与折叠**：同屏光标 >10 个时，折叠成「9+ 人正在此处」，或只显示最近活跃的 5 个；不要为了「热闹」渲染 50 个光标。
- **离屏不渲染**：容器外的光标用裁剪/虚拟化跳过；后台标签页暂停发送。
- **不显示自己**：`useOthers` 天然排除自己；如果自绘，记得过滤 `connectionId === self`。
- **标签**：名字 + 颜色；颜色对比度对非文本 ≥3:1（§11.4）；名字底色与白字要过对比度，不要只用品牌色。

### 4.3 选区（Selections）

- 选区用 **2px outline + 10% 填充**（工程约定），颜色取该用户色；不要用大面积半透明填充，遮住内容。
- **颜色 + 文字双编码**：色盲用户无法只靠颜色区分「谁选了它」，标签上要有名字或首字母。
- 选区变化是**低频**信号：只在 focus/blur/切换对象时发，不要随拖动每一帧发（拖动位置属于文档操作或光标，不属于选区）。

### 4.4 正在输入（Typing Indicator）

Liveblocks 示例的完整规则：输入时置 `typing: true`，**1 秒**无输入清除，失焦清除。因为 presence 是按连接的，关掉标签页后陈旧指示会自动消失。

- 不要每个按键发一次；用 300–500ms 的节流（工程约定）。
- 多人时合并为「3 人正在输入」，不要排三行。
- 「正在输入」不等于「将要提交」；不要用它做「对方马上会保存」的承诺。

### 4.5 当前工具与视口跟随

- 当前工具（选择/画笔/文本）适合白板与设计工具；用图标 + 颜色，不要只写文字。
- 视口跟随必须**显式开启**、随时可退出、显示「正在跟随 XX」；被跟随者停止操作 2s 后不要自动恢复自由视角，避免用户失去控制感（工程约定）。
- 演示/录屏模式默认关闭所有他人光标与头像，否则录出来的画面全是别人的名字。

### 4.6 Agent Presence：AI 也要在同一层出现

Liveblocks 的 Canvas 用例允许服务端/AI agent 用 `setPresence` 发布 presence（示例 `ttl: 60` 表示工作中，结束时 `ttl: 2`），于是 agent 会像人一样出现在 `useOthers` 里，复用已有的光标、头像、选区 UI。

**设计规则**：
- AI 的头像/光标必须有**明确标识**（「AI」徽标或不同形状），不能伪装成人。
- AI 的 presence 要能**随时中断**（停止按钮），并在停止后立即清除。
- AI 的操作要能区分「建议」与「已应用」；不要让它直接以人的身份写文档而不留痕。

### 4.7 什么时候不该显示 presence

- 公开分享页 / 只读访客：显示「N 人在看」可以，显示具体光标与选区是隐私风险。
- 高敏文档（HR、法务、财务）：默认关闭光标，只保留在线人数。
- 录屏、演示、投屏：一键「隐身」。
- 任何「显示 presence 会让用户不敢操作」的场合：给「隐身编辑」开关。

---

## §5 延迟预算：本地 0ms，远端有账可算

### 5.1 三条人类感知阈值（NN/g 原文）

- **0.1 秒**：用户感觉系统「即时响应」，除了显示结果不需要额外反馈。
- **1.0 秒**：思路不被打断，但用户会注意到延迟，且**失去「直接操作数据」的感觉**。
- **10 秒**：注意力还能留在对话上；更久用户会去做别的事，必须给进度反馈。

协作产品的特殊之处：**自己的操作必须走 0.1s 这一档，别人的光标可以走 1s 这一档**。把两者混为一谈，会得到「自己的输入都卡」或「别人的光标像幻灯片」。

### 5.2 一次远端光标要经过的账

| 段 | 典型耗时 | 可做的优化 |
|---|---|---|
| 本地采样 | 8–16ms（指针事件） | 合并同一帧的 move |
| 发送节流 | 50–100ms | 光标 20–30Hz；不要每事件一发 |
| 网络单程 | RTT/2，P95 50–150ms | 就近接入、WebSocket 长连接 |
| 服务端扇出 | 1–20ms | 房间内广播，不落库 |
| 接收渲染 | 1 帧（16.7ms） | spring 插值、`transform` 合成层 |

**预算规则（工程约定）**：同城 P95「对方光标可见延迟」≤150ms；跨洲 ≤300ms。超过 300ms 时，用户会开始怀疑「他是不是没在动」，此时应降低光标密度、增大插值时长，而不是提高发送频率。

### 5.3 本地优先：先改自己的屏幕，再等服务器

Figma 原文：属性变更**立即在客户端应用**，不等服务器确认；但如果同时应用服务器的每个变更，旧的服务端确认值会短暂覆盖更新的未确认本地值，产生 **flicker**。Figma 的解法是：对「尚未确认的本地改动」，丢弃与之冲突的服务端旧值。

**落地规则**：
- 本地输入 → 立即写入本地文档 → 打上 `pending` 标记 → 发服务器。
- 收到服务器广播时，如果本地该属性有更新的 `pending` 值，**不要回写**；等确认或超时（如 5s）再对齐。
- 不要用「等服务器返回再显示」实现协作输入——那会把 0.1s 档直接推到 RTT 档。

### 5.4 渲染性能：别让 presence 拖垮主线程

Liveblocks 文档明确警告：`useOthers` **无参**调用时，任何人 presence 的任何变化都会让组件重渲染，*"This might be way more often than you want!"*；只取某个子集时应用 `useOthersMapped`，它按用户做浅比较，避免整表重渲染。

**规则**：
- 光标位置放 `ref` / CSS 变量 / `transform`，不要放 React state；每帧 setState 会让 20 个光标变成 20 次渲染。
- 头像栈只在「用户集合」变化时重渲染，不要在 presence 每次心跳时重渲染。
- 使用 `requestAnimationFrame` 合并同一帧的多个远端更新。
- 后台标签页用 `document.visibilityState` 暂停发送与动画。

### 5.5 消息预算（单房间，工程约定，需压测）

| 信号 | 频率上限 | 单条大小 | 备注 |
|---|---|---|---|
| 光标 | 20–30 Hz/人 | <100 B | 只发 x/y（百分比）与时间戳 |
| 选区 | 5 Hz/人 | <200 B | 只在变化时发 |
| 正在输入 | 2 Hz/人 | <50 B | true/false，1s 自动清 |
| 文档操作 | 10 Hz/人 | 视操作 | 拖动过程可本地插值，提交时发最终值 |
| 心跳 | 0.2 Hz/人 | <50 B | 5s 一次 |

按 20 人、每人 20Hz 光标计算：20 × 20 = **400 条/秒**；单条 100B 即 40KB/s 下行/人。超过这个量级要考虑「只广播视口内的光标」或「聚合采样」。

---

## §6 冲突界面：三种冲突，三种说法

### 6.1 先分类，再选 UI

| 冲突类型 | 例子 | 能否自动合并 | UI 策略 |
|---|---|---|---|
| **无关** | A 改标题、B 改颜色 | 能 | 静默，不提示 |
| **同属性** | A 把标题改成「甲」、B 改成「乙」 | 能（LWW），但会丢一个 | 静默保留赢家 + 可恢复输家；或编辑期软锁 |
| **同文本区间** | 两人同时改同一句话 | 属性 LWW 不能；CRDT 能 | 有 CRDT 就合并；没有就禁止同时编辑该段 |
| **结构冲突** | 一人删对象、一人改其属性 | 删除赢 | 提示「对象已被删除」，给撤销入口 |
| **重连冲突** | 离线期间同一属性被改 | 服务端赢 | 提示「已合并 N 条离线修改」，列出被覆盖项 |

### 6.2 软锁（Soft Lock）：提示占用，但不阻塞输入

硬锁（ pessimistic lock）在协作里通常是坏体验：一个人打开字段，所有人都不能改。软锁只做**归属提示**：

- 进入可编辑字段 200ms 后广播 `editing: fieldId`；失焦或 5s 无输入释放。
- 其他人看到字段边框变成「对方色」+ 标签「XX 正在编辑」；**仍然可以输入**，但提交时若对方已先提交，走 LWW 并提示。
- 同一字段同一时间只显示一个「正在编辑」标签；多人时显示「XX 等 2 人」。
- 软锁不能替代权限：只读用户不该看到「正在编辑」的输入框。

### 6.3 冲突提示的文案结构

三句话：**发生了什么 + 现在保留了什么 + 你能做什么**。

- 「你改标题时，XX 也改了。已保留 XX 的版本。」+「查看我的版本」+「撤销」
- 「XX 删除了这个图层，你的修改未保存。」+「撤销删除」
- 「已重新连接，合并了 3 条离线修改；其中 1 条被服务器版本覆盖。」+「查看详情」

**反模式**：只弹「保存冲突」不解释；把输家版本直接丢掉且无入口；用红色 toast 报「冲突」但文档其实已经正确合并。

### 6.4 删除 vs 编辑

Figma 的模型里删除会清掉服务器上的属性，只有删除者的 undo buffer 留着。这意味着：
- 被删对象的**评论、标注、历史**要么一起删，要么转成孤儿记录（§8.4）。
- 其他协作者点「撤销」时，如果本地没有属性备份，只能请求服务端恢复或提示「无法恢复，请联系删除者」。
- **UI 规则**：删除确认里写清「同时删除 N 条评论」；批量删除要二次确认。

### 6.5 重连合并

Figma 的离线模型：客户端可离线任意久；重连时**下载最新文档，再把离线编辑重放上去**。这适合「本地操作是最终值」的工具；如果是 CRDT，则走增量同步（Automerge 的 sync 循环直到无新消息）。

产品必须回答：离线编辑重放后，**如果与服务器版本冲突，谁赢？**
- 中心权威 LWW：服务器赢（Figma 路线），必须提示被覆盖项。
- CRDT：自动合并，但要提示「已合并」，并给「查看差异」入口。

---

## §7 多人撤销：只撤自己的，且要能解释

### 7.1 三条硬规则

1. **Undo 只撤本地 origin 的操作。** Yjs `UndoManager` 默认 `trackedOrigins = new Set([null])`，只跟踪本地的操作；源码注释：*"By default, the UndoManager will never overwrite remote changes."*
2. **连续输入合并成一次撤销。** Yjs 默认 `captureTimeout = 500ms`：500ms 内的连续输入算一次；超过就分成两次。UI 的「撤销」应当与这个粒度一致，否则用户按一次撤销只退半个字。
3. **撤销会改写重做历史。** Figma 的 undo 原则：*"if you undo a lot, copy something, and redo back to the present, the document should not change"*；实现上，undo 在撤销时修改 redo 历史，redo 在重做时修改 undo 历史。否则「撤销→复制→重做」会把复制的内容弄丢。

### 7.2 不能做的事

- ❌ 全局撤销（撤掉别人的修改）。
- ❌ 撤销「已被远端覆盖的本地值」却不提示——用户会以为恢复了，实际只是又写了一遍旧值。
- ❌ 把 presence 变更默认放进 undo 历史（切个工具就被撤销）。需要时显式加：Liveblocks `updateMyPresence(..., { addToHistory: true })`。
- ❌ 在多人时把菜单写成「撤销」而不说明范围；应写「撤销我的更改」（快捷键行为不变）。

### 7.3 历史面板

- 按人分色显示操作，支持「只看我的」。
- 撤销一次操作在历史里记为一条，不要展开成 20 条字符级变更。
- 版本快照（手动/自动）与 undo 是两套：快照可恢复整份文档，undo 只回退操作序列。UI 不要把两者混在一个按钮里。

---

## §8 评论与批注：锚点会死，线程不能死

### 8.1 三种锚点

| 锚点 | 适用 | 失效条件 | 处理 |
|---|---|---|---|
| 画布坐标 | 白板、图片、自由布局 | 内容移动/缩放 | 存相对坐标，随容器变换 |
| 对象 ID | 图层、图元、卡片 | 对象被删 | 转孤儿线程（§8.4） |
| 文本相对位置 | 文档、代码 | 文本被删/类型被删 | 用 relative position，解析失败退化为「段落级」 |

Yjs 的相对位置：`createRelativePositionFromTypeIndex(type, index, assoc)` 把位置绑在字符上，`assoc >= 0` 关联 index 之后的字符、`assoc < 0` 关联之前的字符；`createAbsolutePositionFromRelativePosition(relPos, doc)` 返回 `{type, index, assoc}`，**类型被删时返回 null**。普通整数索引会被远端修改弄错位，相对位置不会。

**设计含义**：评论锚点必须能回答「原文被改了，这条评论还挂在哪」。答不上来，就不要把评论做成「贴在字符之间」的精确锚点，退到段落/字段级。

### 8.2 线程生命周期

`open → resolved → reopened`；resolved **不删除**，只是从默认列表折叠。Figma 的评论支持回复、表情反应、resolve、删除、编辑内容、移动位置、排序筛选、dock/hide、通知设置——这些不是「功能清单」，是**线程必须能收尾**的证据。

- Resolve 按钮要可见、可撤销（reopen）；不要 resolve 后立刻消失。
- 编辑评论要留「已编辑」标记；删除要留痕（至少对管理员）。
- 线程排序默认「未解决优先 + 最新回复」，不要按创建时间把已解决的顶上来。

### 8.3 评论者与提及

- **可评论 ≠ 可编辑**：Figma 文件级 `can view` 的原文是 *"View and comment on the file, but not edit it."*。把 commenter 做成 editor 是最常见的越界。
- @提及只允许**有访问权**的人；候选列表不能泄露无权访问者姓名。
- 提及通知与评论回复通知要**去重**：同一条线程同一人只发一条；通知通道归 `notifications-messaging.md`，本文件只定义事件与 `dedupe_key`（如 `thread:123:mention:user:45`）。
- 访客（guest）评论要显示「访客」标识；匿名评论默认关闭。

### 8.4 孤儿线程

对象被删、文本被删、页面被删，线程不能静默消失：

- 列表里保留，标「所在对象已删除」，提供「定位到最后位置」或「删除线程」。
- 不要自动删评论——评论是决策记录，删对象不等于删历史。
- 恢复对象（undo/版本回滚）后，线程要能重新挂上；做不到就在删除确认里说清「评论将变为孤儿」。

### 8.5 评论 UI 的硬要求

- 侧栏可开合，宽度 ≥320px；主内容不被永久挤压（覆盖式或可折叠）。
- 未解决数 badge 可点击筛选；badge 数字与列表一致。
- 键盘：`C` 新建评论（不冲突时）、`Esc` 关闭、`Tab` 在线程内循环；resolve 按钮 ≥44×44。
- 评论气泡不遮挡被评论内容；靠近边缘时翻转方向。
- 只读分享页的评论入口要么给，要么明确「此页面不可评论」，不要给一个点了没反应的按钮。

---

## §9 权限与分享：角色矩阵、继承陷阱、即时回收

### 9.1 角色矩阵（以 Figma 文件级权限为锚）

| 能力 | Owner | Admin | Editor（can edit） | Commenter（can view） | Viewer | Guest |
|---|---|---|---|---|---|---|
| 查看内容 | ✓ | ✓ | ✓ | ✓ | ✓ | 视邀请 |
| 评论 | ✓ | ✓ | ✓ | ✓ | ✗ | 视设置 |
| 编辑内容 | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| 分享/改权限 | ✓ | ✓ | 可配置 | ✗ | ✗ | ✗ |
| 删除文件 | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| 管理团队/席位 | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |

Figma 原文的关键区分：文件级 `can view` = 看 + 评论，**不能编辑**，但**可以复制和导出**（除非显式限制复制/导出）；`can edit` = 完整编辑；Owner = 创建者；且「要编辑文件，既要有 can edit 权限，也要有包含该产品的席位」——**权限与席位是两道门**，UI 不能只显示其中一道。

### 9.2 继承陷阱（必读）

- Figma 的**每个文件、每个文件夹都有自己的 audience access**；文件可以比所在文件夹更严，也可以更松。
- 团队级「Anyone in [organization] can edit」**不会自动下传到每个 folder/file**；嵌套资源各自有 audience access 设置。
- Professional 计划不能改继承权限，嵌套文件夹**总是继承父级角色**；Organization/Enterprise 才能把某个文件夹限制到特定人。
- 因此分享弹窗必须显示**权限来源**：直接授予 / 从文件夹继承 / 从团队继承 / 链接访问。只显示最终角色，用户永远不知道为什么「他明明没被加进来却能看到」。

### 9.3 链接分享

- 默认关闭，或默认「仅查看」；「任何人可编辑」必须二次确认，并在弹窗里写明「拿到链接的人都能改」。
- 支持过期时间、密码、域限制（仅公司邮箱）中的至少一项。
- 链接权限变更要**即时生效**：已连接的 WebSocket 会话必须被服务端踢出或降级为只读，不能等下次刷新。
- 公开链接页面不显示协作者真实姓名与光标（隐私，§4.7）。

### 9.4 降级与移除

- 从 editor 降为 viewer：当前打开的编辑器要立即变只读，未提交的本地改动要么自动保存、要么提示「你的修改未保存，已被降权」。
- 移除成员：立即断开其连接；其未同步的离线改动在重连时被拒绝，并给出明确错误，不能静默丢弃。
- 权限变更要进审计日志：谁、何时、把谁、从什么改成什么。

### 9.5 反模式

- 把「可评论」实现成「可编辑」。
- 权限变更要刷新页面才生效。
- 分享弹窗只显示「有访问权限」，不显示来源。
- 默认「组织内任何人可编辑」，且没有「更严格」的快捷入口。
- 访客能看见成员列表与全部评论历史。

---

## §10 在线状态生命周期：连接、判离线、重连、离线编辑

### 10.1 状态机

`connecting → connected → reconnecting → offline → connected`

| 状态 | 触发 | UI | 文案 |
|---|---|---|---|
| connecting | 首次进入 | 骨架/轻量提示 | 「正在连接协作…」 |
| connected | WebSocket 可用 | 头像、光标正常 | 不提示 |
| reconnecting | 心跳丢失/网络切换 | 顶部细条 + 头像灰化 | 「重新连接中…你的修改已保存在本地」 |
| offline | 超过阈值仍失败 | 顶部条常驻 + 只读或本地编辑 | 「离线：修改将在恢复后同步」 |
| connected（恢复） | 重连成功 | 短暂提示合并结果 | 「已重新连接，合并了 N 条修改」 |

### 10.2 判离线的数值（Yjs 实测）

Yjs awareness 源码：`outdatedTimeout = 30000`（30s）；内部检查周期 `outdatedTimeout / 10` = **3000ms**；本地状态超过 `outdatedTimeout / 2` = **15000ms** 未更新会自动续期；`setLocalState(null)` 表示离线。

**规则**：
- 远端头像的「离线」判定可以等 30s（容忍抖动），但**「正在编辑」的软锁必须在 5s 无心跳时释放**，否则一个人断网会把字段锁 30 秒。
- 自己这一端：心跳 5s 一次，连续 3 次失败（15s）进入 reconnecting，30s 进入 offline（工程约定，与 Yjs 同量级）。
- 不要用「最后活跃时间」做权限或计费依据。

### 10.3 多标签与多设备

- 同一 `userId` 的多个连接在头像栈里**合并为一个**（Liveblocks 默认去重）；需要时在 tooltip 写「2 个标签页」。
- 同一用户不要显示两个光标：取最近活跃的连接，其余隐藏。
- 多设备同时编辑同一字段：仍按连接级 presence 处理；软锁标签显示「XX（手机）」。
- 用 `BroadcastChannel` 在本地标签页之间同步「谁在编辑」，避免同一个人跟自己冲突。

### 10.4 离线编辑

- **允许离线编辑**是产品承诺，不是技术默认。Figma 明确可离线任意久，重连时下载最新文档再重放离线编辑；这要求本地有完整的文档副本与操作队列。
- LWW 模型下，离线期间被服务器改过的属性，重连时**服务器赢**；必须提示被覆盖的项，并保留本地版本供「另存/复制」。
- CRDT 模型下，离线改动自动合并；仍要提示「已合并」，并在冲突语义可能产生怪结果时给「查看差异」。
- 离线队列要有上限（条数/字节/时长），超限时提示「离线修改过多，请先联网同步」。
- 不要在离线时假装「已保存到云端」；文案必须是「已保存在本地」。

### 10.5 降级路径

- WebSocket 不可用 → 尝试长轮询/SSE；仍失败 → 只读 + 本地草稿。
- 协作服务整体不可用 → 单机编辑模式，恢复后走「离线重放」。
- 任何时候都不能因为协作层失败而**阻塞本地编辑**；这是协作产品的底线。

---

## §11 无障碍：协作的「噪音」必须可关，状态必须可说

### 11.1 SC 4.1.3 原文与适用范围

WCAG 2.2 SC 4.1.3 Status Messages（AA）：

> *"In content implemented using markup languages, status messages can be programmatically determined through role or properties such that they can be presented to the user by assistive technologies without receiving focus."*

「状态消息」的定义（同页）：不是 context change，而是告知**动作成功/结果、等待状态、进度、错误存在**的内容。页面的明确 failure 例子：*"Using role=\"alert\" or aria-live=\"assertive\" on content which is not important and time-sensitive"*；sufficient techniques 包括 ARIA22 `role=status`、ARIA23 `role=log`、ARIA25/ARIA27 的进度语义。

**协作场景的推论**：
- 「已保存」「已重新连接」「XX 加入了」「评论已解决」都是 status message，应当进入 `role=status` 的 live region，**不抢焦点**。
- 光标移动、头像变化、打字指示**不是**状态消息；它们不应该被逐条播报，只应提供可查询的聚合信息。
- 不要用 `role=alert` 播报「XX 正在输入」——这属于典型 failure。

### 11.2 aria-live 三档怎么选（MDN 原文）

- `assertive`：最高优先级，立即播报，可能清空语音队列。
- `polite`：在下一个合适时机播报（说完当前句、停止输入时）。
- `off`（默认）：除非用户聚焦该区域，否则不播报。

**协作产品的分配**：

| 事件 | 档位 | 说明 |
|---|---|---|
| 保存成功/失败 | polite | 失败可 assertive（若会导致数据丢失） |
| 重连中/已恢复 | polite | 不要每秒播报 |
| 评论提及/@我 | polite | 聚合到「1 条新提及」 |
| 权限被撤销 | assertive | 用户必须立刻知道 |
| 连接彻底失败且无法本地保存 | assertive | 仅此一类 |
| 光标/头像/输入指示 | off | 纯视觉，`aria-hidden` |

MDN 的警告要抄进规范：*"Because an interruption may disorient users or cause them to not complete their current task, don't use the assertive value unless the interruption is imperative."*

### 11.3 聚合与限流

- 协作者加入/离开：合并成「3 人在线」，**≥5s 最多播报一次**；不要每来一个人播一次。
- 评论：按线程聚合，不按单条回复播报。
- 保存状态：只有在「保存中 → 已保存」状态切换时播报，不要每次自动保存都播。

### 11.4 颜色与识别

- 用户色对非文本 ≥3:1；文字标签与底色 ≥4.5:1（详见 `accessibility.md`）。
- **颜色 + 名字/首字母/图标**双编码；只靠颜色等于对色盲用户隐藏协作信息。
- 同一房间的用户色要稳定；不要按加入顺序随机分配导致「同一个人这次是蓝色下次是绿色」。
- 色板参考 Okabe–Ito（见 `color-science.md`），避免红绿对立作为唯一区分。

### 11.5 键盘、焦点与动效

- 协作者列表、评论线程、resolve 按钮都可 Tab 到达；不要用 `div` 模拟按钮。
- 远端更新**不得抢焦点、不得滚动当前视口**；插入内容时保持焦点元素不动。
- `prefers-reduced-motion: reduce` 时：光标 spring 动画降为直接定位；关闭视口跟随的平滑滚动；头像不弹跳。
- 光标是装饰：`aria-hidden="true"`；选区变化不播报，除非用户主动查询「谁选了它」。

### 11.6 只读与读屏

- 只读分享页也要有「N 人在看」的可读文本，而不是只有头像图片。
- 评论线程用 `role="list"` / `listitem`，回复层级用嵌套列表而非纯缩进。
- 「正在编辑」标签要是文本，不是只有彩色边框。

---

## §12 移动端与触摸：没有 hover，也没有「光标」

- 手机上不显示他人光标（没有指针隐喻）；用**选区高亮 + 当前工具 + 头像栈**表达存在。
- 触摸拖动时 presence 频率降到 10Hz（工程约定）；后台/锁屏暂停。
- 小屏把「XX 正在编辑」放顶部条或字段下方一行，不要浮层遮挡。
- 双指缩放/平移与「跟随视口」手势冲突：跟随模式下手势应退出跟随，而不是同时执行。
- 横竖屏切换后，百分比坐标仍成立；像素坐标会错位。
- 移动端默认不显示「谁在看」，只显示在线人数；点开才看列表。

---

## §13 性能、成本与容量

### 13.1 容量预算（工程约定，需按实际压测调整）

| 项 | 建议上限 | 超限策略 |
|---|---|---|
| 单文档并发编辑者 | 50 | 超出转只读/排队，或提示「文档繁忙」 |
| 同屏光标 | 10（渲染）/ 20（接收） | 折叠为「N 人」 |
| presence 单条 | 1KB | 拆分字段，禁止塞文档内容 |
| 文档操作 | 10 Hz/人 | 本地合并，提交最终值 |
| 离线队列 | 1,000 条 / 5MB / 24h | 超限提示先同步 |

### 13.2 前端

- 光标层用 `position:absolute` + `transform: translate3d()`，避免 layout。
- 只渲染视口内的光标与选区；用 `IntersectionObserver` 或画布裁剪。
- `useOthers` 取子集用 `useOthersMapped`；组件外订阅，避免整树重渲染。
- 跨标签页用 `BroadcastChannel` 同步本地状态，减少服务端消息。

### 13.3 后端

- 房间内广播不落库；文档操作按 16ms 批处理。
- 心跳与判离线分离：心跳 5s，判离线 30s；不要让判离线阻塞写入。
- 重连时先发「文档摘要/版本向量」，再发增量；避免全量下载。
- 权限检查在**每次写入**时做，不只建连时做；被降权的连接要立即拒绝。

### 13.4 指标

- 同步延迟 P50/P95（本地→远端可见）。
- 重连成功率、平均恢复时长。
- 冲突率（同属性并发写入次数/总写入）、冲突提示后的恢复率。
- presence 渲染帧率、每房间消息数/秒。
- 评论解决时长、孤儿线程占比。
- 权限误配率（审计发现的比例）。

---

## §14 文案词表（直接抄）

| 场景 | 用 | 不用 |
|---|---|---|
| 对方在改 | 「XX 正在编辑标题」 | 「有人正在编辑」 |
| 自己保存 | 「已保存」/「保存中…」 | 「同步成功」 |
| 离线 | 「离线：修改已保存在本地，联网后自动同步」 | 「网络错误」 |
| 重连 | 「重新连接中…」 | 「正在同步数据」 |
| 合并完成 | 「已合并 3 条离线修改」 | 「同步完成」 |
| 被覆盖 | 「XX 的版本已保留；你的修改在历史里」 | 「冲突已解决」 |
| 被删对象 | 「这个图层已被 XX 删除」 | 「对象不存在」 |
| 降权 | 「你已改为仅查看，未保存的修改已保留为草稿」 | 「权限不足」 |
| 撤销 | 「撤销我的更改」 | 「撤销」 |
| 跟随 | 「正在跟随 XX · 退出」 | 「视角同步」 |

规则：**名字 + 动作 + 结果**；不写「实时」「无缝」「永不丢失」这类无法兑现的形容词；时间用「刚刚 / 2 分钟前」。

---

## §15 十二条反模式

1. **用属性 LWW 做文本编辑**，再补一个「合并中」假状态 → 用户丢字。
2. **光标 100ms 一跳**，还说「实时」→ 改成插值 + 20–30Hz。
3. **头像永远不消失**（只靠页面刷新）→ 连接断开即移除，判离线 30s。
4. **同一人两个光标** → 按 userId 合并，取最近活跃连接。
5. **全局撤销** → 只撤本地 origin。
6. **可评论 = 可编辑** → 权限矩阵拆开。
7. **权限变更要刷新** → 服务端即时踢出/降级。
8. **离线改动静默丢弃** → 重连提示被覆盖项 + 本地副本。
9. **删除对象连带删评论** → 孤儿线程保留。
10. **每次 presence 变化都 `setState`** → 用 ref/transform，订阅切片。
11. **把「正在输入」用 `role=alert` 播报** → 违反 SC 4.1.3 failure。
12. **只靠颜色区分协作者** → 颜色 + 名字/首字母双编码。

---

## §16 验收清单（18 条，可勾选）

**数据与冲突**
1. 两人同时改同一属性，最终值等于服务端最后收到的值，且输家可从历史/提示中找回。
2. 两人同时改同一段文本：要么 CRDT 合并，要么 UI 明确「该段同一时间只能一人编辑」，没有中间态。
3. 并发插入有序列表 20 次，顺序稳定，无重复/丢失。
4. 删除对象后，相关评论进入孤儿状态并可定位/删除，不静默消失。

**Presence**
5. 光标坐标在缩放 50%–200%、滚动后仍指向同一内容位置。
6. 同屏 20 个光标时，帧率 ≥50fps；超过 10 个有折叠策略。
7. 同一用户多标签只显示一个头像、一个光标。
8. 关闭标签页后，头像在 1s 内消失；断网后 30s 内标记离线。
9. 「正在输入」1s 无输入自动清除，失焦立即清除。

**撤销与历史**
10. A 输入、B 输入、A 撤销：只回退 A 的内容；B 的内容不变。
11. 连续输入 500ms 内合并为一次撤销；超过 500ms 分成两次。
12. 撤销后重做，文档回到撤销前状态，复制的内容不丢。

**权限**
13. `can view` 用户能评论但不能编辑；输入框不出现或只读。
14. 移除成员后，其已连接会话在 5s 内被断开/降级。
15. 分享弹窗显示权限来源（直接/继承/链接），文件可比文件夹更严或更松。
16. 「任何人可编辑」链接需二次确认，并可设过期时间。

**无障碍与降级**
17. 保存/重连/评论提及通过 `role=status` 播报，不抢焦点；光标 `aria-hidden`。
18. 断网后仍可本地编辑，恢复后自动同步；协作服务不可用不阻塞本地编辑。

---

## §17 度量与实验

- **协作感知**：用户能否在 5s 内说出「还有谁在」；presence 开关 A/B 对「误改率」的影响。
- **冲突成本**：冲突提示出现率、提示后 24h 内该文档的撤销/回滚次数。
- **离线价值**：离线编辑用户占比、重连成功率、被覆盖修改的申诉率。
- **评论闭环**：首次响应时长、解决率、孤儿线程占比。
- **性能**：P95 光标延迟、每秒消息数、长任务（>50ms）次数。

实验注意：协作功能有强网络效应，**不要按用户随机分组**（同一文档的人必须同组），按文档/团队分组。

---

## §18 交付检查单（设计 / 前端 / 后端）

**设计**
- 画出「连接中/在线/重连/离线」四态与对应文案。
- 给出权限矩阵与分享弹窗的权限来源展示。
- 给出冲突提示的三种文案与恢复入口。
- 给出移动端无光标方案。
- 给出只读/公开页的隐私开关。

**前端**
- 光标用百分比坐标 + transform + spring；订阅切片。
- presence 与文档状态分离；本地乐观 + pending 标记。
- `aria-live` 聚合限流；reduced-motion 降级。
- 多标签去重；后台暂停。

**后端**
- 属性级 LWW 或 CRDT 选型落地；对象 ID 客户端生成。
- 心跳/判离线/软锁释放三套阈值分离。
- 每次写入校验权限；降权即时生效。
- 离线队列上限与重放冲突策略。

---

## §19 可执行验算（Python，纯标准库）

```python
# 19.1 fractional index：中点插入与精度耗尽
def mid(lo, hi):
    return (lo + hi) / 2

lo, hi = 0.0, 1.0
pos = mid(lo, hi)
seq = [pos]
for _ in range(60):
    pos = mid(lo, pos)          # 一直往左插
    seq.append(pos)
assert seq == sorted(seq, reverse=True)
assert len(set(seq)) == len(seq), "精度耗尽后出现重复位置"
print("19.1 PASS", len(seq), "unique positions; last =", seq[-1])
```

```python
# 19.2 presence 消息预算：20 人 × 20Hz 光标
people, hz, size = 20, 20, 100          # 100 B/条
per_sec = people * hz
down_kbps = per_sec * size * 8 / 1000
assert per_sec == 400
assert down_kbps == 320.0
print("19.2 PASS", per_sec, "msg/s,", down_kbps, "kbps per receiver")
```

```python
# 19.3 离线判定与软锁释放必须分离
HEARTBEAT = 5          # s
OFFLINE_AFTER = 30     # s, Yjs outdatedTimeout
LOCK_RELEASE = 5       # s, 工程约定

def state(seconds_since_last_seen, editing):
    if seconds_since_last_seen >= OFFLINE_AFTER:
        return "offline", False
    if seconds_since_last_seen >= HEARTBEAT * 3:
        return "reconnecting", editing and seconds_since_last_seen < LOCK_RELEASE
    return "online", editing

assert state(4, True) == ("online", True)
assert state(16, True) == ("reconnecting", False)   # 软锁先释放
assert state(31, True) == ("offline", False)
print("19.3 PASS", state(16, True), state(31, True))
```

```python
# 19.4 权限矩阵的最小校验：commenter 不得写
CAPS = {
    "owner":    {"view", "comment", "edit", "share", "delete"},
    "editor":   {"view", "comment", "edit"},
    "commenter":{"view", "comment"},
    "viewer":   {"view"},
}
assert "edit" not in CAPS["commenter"]
assert "edit" not in CAPS["viewer"]
assert "comment" in CAPS["commenter"] and "comment" not in CAPS["viewer"]
assert CAPS["editor"] < CAPS["owner"]          # owner 是 editor 的超集
print("19.4 PASS", sorted(CAPS["commenter"]))
```

---

## §20 取源限制与未取到项（逐条登记）

1. **Liveblocks 的服务端容量上限（单房间连接数、消息速率）未公开**：文档只给客户端 `throttle` 范围与用法，未给「每房间最多多少人」。§13.1 的 50 人/10 光标是**工程约定**，不是官方值。
2. **Figma 的文本协同边界只来自 2019 博客**：原文明确「同时编辑同一文本值不工作」，但 Figma 后续是否在部分场景引入文本合并，本轮未取到更新的官方说明；引用时须带 2019-10-16 日期。
3. **Google Docs / Office 365 的实时协作细节未逐条取源**：本轮未抓取其帮助页，故不对其冲突/离线行为下断言。
4. **Yjs 的 30s/15s/3s 是 awareness 默认值**，可被配置覆盖；引用时写「默认」。
5. **Yjs `captureTimeout=500` 是 UndoManager 默认值**，不同绑定（如 y-prosemirror）可能改写；以所用集成为准。
6. **Liveblocks `throttle` 默认 100ms、允许 16–1000ms** 来自 React API 参考页；16ms = 60fps 是原文表述。
7. **Figma 权限表是「文件/文件夹」级**；团队级权限另有文章，且 Org/Enterprise 与 Professional 的继承规则不同，不能混用。
8. **WCAG 页面标注 Updated 04 October 2026**；SC 4.1.3 文本本身自 2.1 起未变，但 Understanding 文档会更新，引用带日期。
9. **本文的 20–30Hz 光标、5s 软锁、2s 跟随恢复、1000 条离线队列**均为工程建议值，无官方来源，不得当规范引用。
10. **边界声明**：本文不覆盖「服务端 CRDT 存储引擎选型」「端到端加密协作」「音视频共编」「版本控制式分支合并」；这些属实现或另立资产。

---

## §21 来源（2026-11-16 取用）

- Figma Engineering, *How Figma's multiplayer technology works*（Evan Wallace，2019-10-16）：https://www.figma.com/blog/how-figmas-multiplayer-technology-works/
- Yjs awareness 源码：https://raw.githubusercontent.com/yjs/y-protocols/master/src/awareness.js
- Yjs UndoManager 源码：https://raw.githubusercontent.com/yjs/yjs/main/src/utils/UndoManager.js
- Yjs Relative Positions：https://docs.yjs.dev/api/relative-positions
- Automerge sync 模块：https://automerge.org/automerge/automerge/sync/
- Liveblocks Canvas 用例：https://liveblocks.io/docs/use-cases/canvas
- Liveblocks Presence 用例：https://liveblocks.io/docs/use-cases/presence
- Liveblocks React API：https://liveblocks.io/docs/api-reference/liveblocks-react
- WCAG 2.2 SC 4.1.3 Understanding：https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
- MDN `aria-live`：https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-live
- Figma Help, *File and folder permissions*：https://help.figma.com/hc/en-us/articles/35361119554711-File-and-folder-permissions
- Figma Help, *Team permissions*：https://help.figma.com/hc/en-us/articles/360039970673-Team-permissions
- Figma Help, *Guide to comments*：https://help.figma.com/hc/en-us/articles/360039825314-Comments-in-Figma
- NN/g, *Response Times: The 3 Important Limits*（Jakob Nielsen，1993-01-01）：https://www.nngroup.com/articles/response-times-3-important-limits/

**GitHub API 实测（2026-11-16，stars / license / pushed_at / 默认分支）**

| 仓库 | ★ | License | pushed |
|---|---:|---|---|
| yjs/yjs | 23,072 | NOASSERTION | 2026-11-14（main） |
| automerge/automerge | 6,741 | MIT | 2026-11-16 |
| automerge/automerge-repo | 718 | MIT | 2026-11-16 |
| liveblocks/liveblocks | 4,772 | NOASSERTION | 2026-11-16 |
| tldraw/tldraw | 51,434 | NOASSERTION | 2026-11-16 |
| excalidraw/excalidraw | 135,784 | MIT | 2026-11-16（master） |
| partykit/partykit | 5,750 | MIT | 2026-10-09 |
| yjs/y-websocket | 715 | MIT | 2026-10-28（master） |
| yjs/y-protocols | 165 | MIT | 2026-05-05（master） |
| microsoft/FluidFramework | 4,949 | MIT | 2026-11-16 |

**一句话选型**：图形/白板优先看 tldraw 与 Liveblocks；文本/离线优先看 Yjs 与 Automerge；协议层自建看 y-websocket / y-protocols / partykit；企业级结构化协作可参考 FluidFramework。
