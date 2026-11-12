# 首次体验与用户引导：从启动到 Aha Moment 的判型、时机与可访问性契约

> 快照 2026-11-12 · 每日升级 #34（v37→v38）· 主题：Onboarding / First-Run Experience / Activation / Progressive Disclosure
> 取源：`Design-related websites.txt` 第二十三分区（本轮新增）+ Apple HIG 4 页 / NN/g 3 篇 / Material Design 1 onboarding / Ant Design Tour·Empty / Carbon Empty states / WCAG 2.2 Understanding 5 条 SC + GitHub API 实测 12 库。凡规范条文与数值均引官方原文，凡工程建议均标注「工程约定」；取源 URL 本轮全部 HTTP 200 复核（含定稿前补取的 NN/g 第 4 篇，该篇触发 §4 用词勘误）。
>
> **边界纪律（先读这段，避免误路由）**：本文件只管「用户第一次（以及版本更新后重新）从启动到完成第一个有价值动作之间，该不该教、教什么、什么时候教、什么时候要权限、什么时候算成功」。**coach mark / 引导浮层作为 overlay 的 inert / 焦点 / 退出 / 遮挡契约**归 `overlays-modality.md`；**五种空态结构与文案公式 / 404 / 骨架屏**归 `feedback-states.md`；**表单 label / 校验 / 自动补全 aria 明细**归 `form-table.md`；**WCAG 全量阈值与焦点可见样式**归 `accessibility.md`；**cookie 同意合法性 / 暗黑模式 / 一键关闭**归 `design-ethics-inclusion.md`；**按钮与错误文案措辞**归 `ux-writing.md`；**SUS / 样本量 / A-B 统计**归 `design-measurement-research.md`；**导航形态选型**归 `navigation-ia.md`。本文件不重复这些资产，只补「首次体验作为一条有时间起止、有权衡、有验收标准的路径」这条结构性空白。

---

## 0. 一句话立场

**Onboarding 不是「第一次打开时播放的介绍」，是「从启动到第一个保留相关动作的路径设计」；教程只是这条路径上最不该默认选的那一段。** 一个产品可以完全没有引导页却有极好的首次体验（把界面改到不用解释），也可以有五屏精美的欢迎轮播却让用户在第三屏退出。判断标准不是「引导做得好不好」，是「用户有没有更快到达第一个价值动作，且没有被要求先做与价值无关的事」。

三条裁决（§2）：① **默认不加教程**，NN/g 70 人 4 app 的实测里唯一显著的方向是「读了教程的人觉得任务更难」；② **权限按功能时机请求，不按会话起点批发**，Apple HIG 的 onboarding 例外有严格前置条件；③ **首次体验的可访问性是四条 WCAG 条款的合取**，不是「加个跳过按钮」——其中 SC 3.2.1 的官方失败例恰好就是一个抢焦点的 help dialog。

判型先答六问（§3），再选形态（§4），最后过四条款（§11）。**顺序不能换**：先看设计稿再答六问，一定会给「已经做好的五屏轮播」找理由。

---

## 1. 五段链路判层：Launch → First-run → Teach → Activate → Return

首次体验是一条有时间起止的链路，不是一个页面。把问题定位到具体段位，才知道该改界面、改文案、还是改权限时机。

| 段 | 用户所处状态 | 这一段必须回答 | 典型失败 | 主责资产 |
|---|---|---|---|---|
| **L 启动 Launch** | 点了图标，界面还没可用 | 多久能看到可操作的界面？ | 用 launch screen 做品牌动画、闪屏停留、首次大下载 | `performance-design.md` / `feedback-states.md`；Apple 分界见 §6 |
| **F 首运行 First-run** | 界面可用，但没有任何数据 | 用户第一眼能做什么？ | 空白仪表盘、无默认配置、强制注册墙 | 本文件 §13 / §5 |
| **T 教学 Teach** | 想做事，但某一步不会 | 这条信息现在给还是不给？ | 首启轮播、coach mark 盖住控件、教系统标准控件 | 本文件 §7 / §9 / §12 |
| **A 激活 Activate** | 完成了第一个核心动作 | 怎么定义「到了」？ | 把「注册成功」当激活、把跳过率当激活率 | 本文件 §14 |
| **R 回访 Return** | 第二次及以后进入 | 状态还在吗？引导还会再弹吗？ | 每次启动重播教程、上次填的东西没了 | 本文件 §5 / §8；状态恢复归 `feedback-states.md` |

**两条执行规则（工程约定）**：

1. **L 与 F 的分界以「可操作」为准，不以「动画播完」为准**。Apple HIG Launching 逐字：*"Launching begins when someone opens your app or game, includes an initial download, and ends when the first screen is ready."* 因此启动屏期间的加载不算 onboarding，把它算进去会掩盖真正的 LCP / 首包问题。
2. **T 不是必经段**。NN/g 逐字：*"For most mobile apps, **users should be able to learn the interface by using it and thus** instructional onboarding flows are not necessary."* 五段链路里 T 可以被整段跳过，其余四段不能。

---

## 2. 三条最重要裁决

### 裁决一 · 教程是最不该默认的引导形态；实证上它不提速、不提成功率，只提高「 perceived difficulty」

NN/g《Mobile Tutorials: Wasted Effort or Efficiency Boost?》（Alita Kendrick，2020-03-08）逐字摘要：*"Our research shows that tutorials don't make users faster or more successful at completing tasks; on the contrary, they make them perceive the tasks as more difficult."*

完整数值与限制见 §7。这里只给裁决：**读了教程组与跳过组在任务成功率（91% vs 94%，p=0.443）和耗时（93.49s vs 85.17s，p > 0.1）上均无显著差异，唯一显著的是 SEQ 主观难度 4.92 vs 5.49（p=0.047），方向对教程不利**。因此「加个教程」不是中性改动，是有实测代价的改动。

三份权威来源给出同一方向的落地：

- Apple HIG Onboarding：*"**Teach through interactivity.** People tend to grasp and retain information better when they can actually perform the task they're learning about instead of just viewing instructional material."* 且 *"**Consider providing a collection of context-specific tips instead of a single onboarding flow.**"*
- NN/g《Mobile-App Onboarding: An Analysis of Components and Techniques》（Alita Kendrick，2020-06-21）：*"**Instructional onboarding should not be used to supplement poor design.**"* / *"**Resources are better spent for making a UI more usable than for creating instructional content.**"*
- NN/g 结论：*"If you're still unsure whether your app needs onboarding, test the app with no onboarding before investing money into adding extra screens."*

**所以该怎么做**：先测「无引导版本」→ 若用户真的卡住，先问能不能改界面 → 改不了才原型化引导并复测 → 只有「用户更成功」才上线。这是四步闸门，不是一句"看情况"。

### 裁决二 · 权限按功能时机请求，不按会话起点批发；onboarding 不是授权窗口

Apple HIG Privacy「Requesting permission」逐字：

> *"**Request permission only when your app clearly needs access to the data or resource.** ... Ideally, wait to request permission until people actually use an app feature that requires access."*
> *"**Avoid requesting permission at launch unless the data or resource is required for your app to function.**"*

Apple HIG Onboarding 里那句常被断章取义的话，逐字带前置条件：*"**If your app or game needs access to private data or resources before it can function, consider integrating the permission request into your onboarding flow.** In this scenario, making the request during your onboarding flow gives you the opportunity to show people why your app or game needs their permission and the benefits of granting it. **Otherwise, present a permission request when people first access the specific function that relies on private data or resources.**"*

**裁决**：`before it can function` 是硬条件，不是「我们希望用户早点授权」。导航类、相机类 App 满足；「先要通知权限以便日后推送活动」不满足。把两页对读可以得到一条可验收规则：**每个权限请求都必须能指向一个已经可見、且用户刚表现出兴趣的功能入口**；指不出来的，延后到该入口被点击时再问。

purpose string 也有可逐字验收的写法：*"Aim for a brief, complete sentence that's straightforward, specific, and easy to understand. Use sentence case, avoid passive voice, and include a period at the end."* 正反例见 §10。

### 裁决三 · 首次体验的可访问性是四条 WCAG 条款的合取，不是「加个跳过按钮」

| SC | 级别 | 首次体验里最常踩的坑 | 逐字锚点 |
|---|---|---|---|
| **3.3.7 Redundant Entry** | A | 多步注册向导里重复要同一信息、出错后清空表单 | *"auto-populated, or available for the user to select"* |
| **3.3.8 Accessible Authentication (Minimum)** | AA | 禁止粘贴密码 / 验证码、要求手动转录 OTP | *"A cognitive function test ... is not required for any step in an authentication process unless that step provides at least one of the following"* |
| **3.2.1 On Focus** | A | 输入框一获得焦点就弹出引导卡并抢走焦点 | 官方失败例：*"Example of a Failure: A help dialog"* |
| **2.2.1 Timing Adjustable** | A | 限时验证码、自动跳过的引导、会话超时丢数据 | 六选项含 *"given at least 20 seconds to extend"* / *"at least ten times"* / *"longer than 20 hours"* |

**关键辨析（最容易误判的一处）**：SC 3.3.8 逐字写明 *"This success criterion is focused on authentication of existing users. It does *not* cover creation of a username or initiation of an account."* ——**注册 / 首次创建账号不在 3.3.8 的适用范围内**，但同页紧接着说：*"The techniques used to satisfy this criterion (particularly allowing pasting into inputs and not relying on transcription) can also reduce the cognitive burden in account creation."* 而**多步注册流程内的重复输入**由 SC 3.3.7 覆盖（3.3.7 的 `process` 定义是 *"series of user actions where each action is required in order to complete an activity"*，注册向导正是）。两者不是替代关系，是接力关系。把 3.3.8 拿来当「注册页必须支持密码管理器」的条文依据，是引错条款。

另有一条常被忽略：SC 3.3.7 Intent 逐字 *"The autocomplete feature of browsers is not considered sufficient because it is the content (the website) that needs to provide the stored information for a redundant entry"* ——**依赖浏览器 `autocomplete` 不能算满足 3.3.7**，站点自己必须回填或提供可选。这一条直接否掉了「我们加了 autocomplete 属性就行」的常见交差方式。

---

## 3. 六问判型决策树：要不要做、做哪一种

先答六问，**不要先看设计稿长什么样**：

| # | 问题 | 答「是」 | 答「否」 |
|---|---|---|---|
| Q1 | 不用任何用户信息，App 能不能完成第一个核心动作？ | 走向 Quickstart（不设前置表单） | 只收集**必需**信息，且每项要能说出它改变了第一屏的什么 |
| Q2 | 应用功能是否**高度依赖用户上下文/偏好**（如体重、语言水平、地区）？ | 可考虑 Self-Select，但选项须「有意义且可察觉」 | 不要为了「个性化」做十题问卷 |
| Q3 | 是否存在**用户看图也猜不到**的独特交互或全新心智模型（隐藏手势、新概念）？ | 只针对这一处做情境化教学 | 不做的理由不成立 → 不要做教程 |
| Q4 | 有没有测过**完全无引导**的版本，且用户真的卡住了？ | 进入下一步 | 先测，不要凭评审意见加引导 |
| Q5 | 卡住的原因能否靠**改界面**消除？ | 改界面，回到 Q4 | 才允许原型化引导并复测 |
| Q6 | 引导是否有**不依赖跳过的价值证明**（用户成功率提升）？ | 上线，但保持可跳过、可找回 | 不上线 |

**四条硬约束（工程约定，落到代码即可验收，见 §20.1）**：

1. **Q3 与 Q1 不能同时用来给轮播找理由**：「我们功能很独特」+「也要收集信息」≠ 五屏欢迎轮播；Material 1 明确 *"Don't combine Self-Select with Top User Benefits"*（§8）。
2. **Q4 是闸门不是建议**：NN/g 的原文是 *"test the app with no onboarding **before** investing money into adding extra screens"*，顺序写死。
3. **任何引导都必须可跳过、且跳过之后不再出现**：Apple HIG 逐字 *"If you let people skip the tutorial when they first launch your app or game, don't present it again on subsequent launches, but make sure it's easy for people to find if they want to view it later."*
4. **「永久跳过」要有回落入口**：同上，*"you could make the tutorial available in a help, account, or settings area"*；否则等于把帮助删了。

---

## 4. 六类引导形态选型矩阵

| 形态 | 什么时候用 | 硬约束 | 权威锚点 |
|---|---|---|---|
| **Quickstart（直接进界面）** | 界面用通用模式、没有必需信息、App 不新 | 首屏必须有「可做的事」，不能是空白 | Material 1 *"Start the user directly in the app"*；NN/g *"For most mobile apps, this means putting users directly into the interface."* |
| **Self-Select（自选配置）** | 有 setup / consent 要求，且选项会明显改变首屏 | 单屏或连通的多屏；每屏 **fewer than ten choices**；不问正常使用就能推断的偏好 | Material 1 §8 |
| **Top User Benefits（利益轮播）** | App 在解决新问题、提供新收益，或宣布重大改版 | **最多 3 条**收益、每 2–3 秒轮播、全程常驻 Get Started、用户一碰就停自动播放 | Material 1 §8 |
| **Contextual tips（情境提示）** | 某一控件/能力不显然，但用户正要做相关任务 | 1–2 句；单次 1 条；不盖住被解释的控件；用事件/参数规则控制频次 | Apple HIG Offering help §9 |
| **Coach marks / Tour（遮罩导览）** | 只剩「确实猜不到」的少数点，且已过 Q4–Q6 | **非模态优先**；必须可跳过 / Escape / 焦点归位 / 不遮挡焦点项 | 契约归 `overlays-modality.md`；Ant Design Tour 见 §12 |
| **教学型零数据位 / starter content** | 首次进入没有内容，但空白本身就是教学机会 | 五件套；只给一个主行动；替代原本要显示的元素 | Carbon Empty states §13 |

**三条组合禁令（Material 1 逐字）**：*"Don't combine Self-Select with Top User Benefits"*、*"Don't combine Top User Benefits with Self-Select"*、*"It's okay for your app to show setup after or as part of onboarding"*。第三条常被误读：允许的是 **setup**，不是允许把三种模型叠着放。

**push / pull 的用词纪律（定稿前勘误）**：NN/g **确有** `push revelation` / `pull revelation` 这一组成对术语——Page Laubheimer《Onboarding Tutorials vs. Contextual Help》（2023-02-12）逐字 *"Intrusive tutorials and lists of changes that are shown when an app is launched or at random points during the user's session are a type of **push revelation**."* / *"**Pull revelations** are help content triggered by some signal that the user would benefit from that information at that moment."*，并单列 `Why Tutorials (and Push Revelations) Don't Work`、`What Works: Pull Revelations`、`Guidelines for Implementing Pull Revelations` 三章，后者给出五条（可随时关闭且可找回 / 帮助内容本身用渐进披露 / 不让用户记忆 / 跳过显然的东西 / 理解用户抵达该功能之前的路径）。**本文件 §4 用的是另一套更粗的工程简称**（push＝前置推送 / pull＝按需取用），只用来标注六类形态的触发方向，**不等价于** Laubheimer 按「是否由用户当下信号触发」划分的 revelation 二分。转述纪律：① 不得再说「push/pull 不是 NN/g 术语」（初版已作废，见 §22 第 4 条勘误）；② 引用成对术语时必须连同作者、年份、篇名与 `revelation` 后缀一起给，不能简写成 push/pull 冒充本文件分类；③ 本文件矩阵里的 push/pull 一律标「工程简称」，不升格为文献术语。另三篇 NN/g（《Mobile Tutorials》/《Mobile-App Onboarding》/《Mobile Instructional Overlay》）用的是 *front-loading* / *"Avoid feature-promotion onboarding at first launch"* / *"highlight features while the user is in the app, through contextual help"* / *"a popup tip so that, if a user needed clarity, it would be a tap away"*，与 Laubheimer 篇口径不同，勿跨篇张冠李戴。

---

## 5. 设置后置与首启减负：把「以后再问」写成默认

渐进披露（progressive disclosure / staged disclosure）在首次体验里的落地不是「把教程拆成几步」，而是**把与第一个价值动作无关的事全部移出首启路径**。

Apple HIG Onboarding「Additional requests」逐字：

> *"**Postpone nonessential setup flows or customization steps.** Provide reasonable default settings so most people can immediately start interacting with your app or game without performing additional configuration."*
> *"**Prefer letting people experience your app or game before prompting them for ratings or purchases.**"*

NN/g 对「哪些个性化不该放首启」给了明确分界：*"**visual-design customization, such as selecting a color scheme, doesn't belong in onboarding.**"* 而 *"**Content customization can create a relevant experience and is more likely to be appropriate for initial app onboarding.**"* 理由是 *"a lot of research shows that people usually stick with defaults"*（NN/g 引 defaults 研究）。

**四类「可以延后」的清单（工程约定）**：

| 类 | 首启做法 | 何时再问 |
|---|---|---|
| 外观偏好（主题、配色、密度） | 给合理默认值，不问 | 用户进设置或明确表达不满时 |
| 可推断偏好（「多久看一次信息流」） | 不问，按行为推断 | 从不 |
| 营销类授权（通知、评价、订阅） | 不问 | 用户完成第一个价值动作之后，且要能说清收益 |
| 与非首屏相关的资料（手机号、头像、公司规模） | 不问 | 该功能第一次被用到时，且说明用途 |

**可验收判据**：每个首启问项都要能回答「它改变了用户接下来看到的**第一屏**的什么」。答不出来的，按 NN/g 逐字 *"If you can't explain why gathering that data is beneficial at launch, this information should be gathered later, once the user can better understand why it's necessary."* 移出首启。

**会话间状态的两条相反约束**：SC 3.3.7 Intent 逐字 *"This success criterion does not add a requirement to store information between sessions"*（不必跨会话存），但 Apple HIG Launching 逐字 *"**Restore the previous state when your app restarts so people can continue where they left off.**"*（应恢复上次位置）。二者不矛盾：**前者说 WCAG 不强制，后者说体验上应该**。把前者当「可以不恢复状态」的依据是误读。

---

## 6. 启动三分界：launch screen ≠ splash screen ≠ onboarding

Apple HIG 把三者分得很开，混用会同时踩性能与体验两条线：

| 概念 | 定义（逐字锚点） | 能不能放品牌 / 文字 / 动画 |
|---|---|---|
| **Launch screen** | *"the system displays your launch screen the moment your app or game starts and quickly replaces it with your first screen"* | *"**Don't advertise.**"* / *"**Avoid including text on your launch screen, even if your first screen displays text.** Because the content in a launch screen doesn't change, any text you display won't be localized."* |
| **Splash screen** | *"A splash screen is a beautiful graphic that succinctly communicates branding and other information you need to provide."* | 可以，但 *"Aim to display your splash screen just long enough for people to absorb the information at a glance without feeling that it's delaying their experience."*；且 Apple HIG Launching 建议 *"consider displaying it at the beginning of your onboarding flow"* |
| **Onboarding** | *"When available, onboarding occurs after launching is complete — it isn't part of the launch experience."* | 可以，但受 §2–§4 全部约束 |

**最容易犯的错**：把 launch screen 做成 2 秒 logo 动画，既违反 *"**Launch instantly.** People want to start interacting with your app or game right away, and sometimes they don't want to wait more than a couple of seconds."*，又违反 *"**Design a launch screen that's nearly identical to the first screen of your app or game.**"*（否则出现 *"an unpleasant flash between the launch screen and your first screen"*）。

另一条独立的首启性能线：*"**Don't let large downloads hinder onboarding.** ... Consider including enough media and other content in your software package to prevent people from having to wait for downloads to complete before they can start interacting"*。这条与 §1 的 L 段直接对接。

---

## 7. NN/g 实证全表与研究限制（数值只从一手原文取）

《Mobile Tutorials: Wasted Effort or Efficiency Boost?》，Alita Kendrick，2020-03-08，`nngroup.com/articles/mobile-tutorials/`。

| 项 | 值（逐字核对） |
|---|---|
| 样本 | *"a quantitative usability test with 70 users and 4 mobile apps"*；*"In total, we had 70 participants, 35 in each group."* |
| 设计 | *"between-subject, remote unmoderated quantitative usability test"*；平台 *"Userlytics"* |
| App | Movesum、Brainsparker、LaunchCenter Pro、Sketch.Book，全部 iPhone；*"not highly complex applications"* |
| 分组 | A 组必看 deck-of-cards 教程，B 组必跳过；任务**正是教程教过的那个动作** |
| 任务成功率 | A **91%**（n=35）vs B **94%**（n=35）；*"This difference was not statistically significant (p=0.443)"* |
| 主观难度 SEQ | A **4.92** vs B **5.49**（1–7，越高越容易）；*"This difference was statistically significant (p=0.047)"*；*"Half a point is a fairly substantial difference on a 1–7 rating scale."* |
| 任务耗时 | A **93.49** 秒 vs B **85.17** 秒；*"This difference was not statistically significant (p > 0.1)"*；用**几何平均**而非算术平均 |
| 剔除 | *"In total, we removed 13 trials (5% of total trials)."* |
| 结论 | *"Think twice about creating a tutorial for simple applications."* |

**四条必须随数值一起转述的限制**（否则就是拿一组数字当普适定律）：

1. 任务耗时**不含**阅读教程的时间：*"the task-completion times reported here did not include the upfront time to read the tutorial before using the app"*；原文同时指出 *"seen from the perspective of total user burden, it's still a downside for tutorials"*。
2. 研究自述 *"This study focused on 4 iOS applications"*，明确列出两条泛化风险：*"It may not generalize to Android applications."* / *"It may not generalize to other iOS applications ... due to the low number of apps included."*
3. 对象是**简单 App 的 deck-of-cards 教程**，不是复杂企业软件、不是交互式 walkthrough、不是情境提示。NN/g 自己在结论里把替代方案指向 *"interactive methods of doing so, like contextual help"*。
4. SEQ 差异的解释是**感知**而非能力：*"tutorials can make apps seem overly complicated"*；*"a tutorial may shift users' perception and make them think the app is more complicated than it really is."* 不能转述成「教程让用户变笨」。

**§20.4 提供一个数值复核器**，把这张表编码成断言，防止后续转述把 4.92/5.49 或 p 值写反。

---

## 8. Material 1 三模型与精确数值（历史规范，不是现行 M3）

> **版本纪律**：本节数值取自 `m2.material.io`（Material Design 1 / Material 2 归档页），**不是 Material 3 现行规范**。它可用作「有出处的历史基线」，不可当作今天 M3 的合规值；M3 现行组件规范另见 `design-tokens.md` 与 `component-libraries.md`。

*"Onboarding is a virtual unboxing experience that helps users get started with an app."*，目标含 *"Drive users to take actions that increase engagement and retention in the first seven days"*，且 *"**Show onboarding to first-time users. Don't show it to returning users.**"*

| 模型 | 适用 | 不适用 |
|---|---|---|
| Self-Select | *"The UI can be customized"* / *"Your app has setup and consent requirements"* | *"Your app is tackling a new challenge or providing a new kind of benefit"* / *"To announce new uses or major UI changes"* |
| Quickstart | *"You've already identified the behaviors that correspond to increased engagement (in the first session) or increased retention (in the first seven days)"* | *"Your app is tackling a new challenge or providing a new kind of benefit"* |
| Top User Benefits | 同上「新挑战 / 新收益 / 重大改版」 | *"Your app's UI and benefits use patterns familiar to most users"* / *"Your app has no major changes"* |

**可抄的精确数值（全部逐字）**：

- Self-Select 选项三条标准：*"Be meaningful and noticeable"* / *"Provide new information"* / *"Be short"*；*"Limit choices to one screen, or make multiple screens feel connected to each other."*；*"**Each screen should have fewer than ten choices.**"*
- 不该问的：*"Don't ask for preferences that can be garnered from normal usage."* / *"Don't ask users to make selections that will become evident with normal use of the app and that won't meaningfully change the first-run experience."*
- Quickstart 教学时机：*"If it appears as though the user is unclear how to use the app towards the end of the average first-run experience (**90% of the way through the first session**), display a UI prompt offering the opportunity to learn how to use the app."* ——注意是**首会话末尾按需提供**，不是首会话开头强制；同一节的 Don't 是 *"Don't force education upfront."*
- Top User Benefits：*"should demonstrate **up to three primary benefits**"*；*"**A maximum of three illustrations should auto-rotate every two to three seconds and display pagination navigation.**"*；*"**Auto-advance the first screen more quickly** so that it's clear this isn't a single screen."*；*"**The auto-advance feature should be disabled if the user touches the carousel.**"*；*"Display a 'Get Started' button throughout the animation, and loop through the animation continuously until the 'Get Started' action is tapped."*；*"The screen should be swipe-enabled"*。
- 不应做的事：*"**Don't be UI literal** — Don't show app UI if users haven't experienced it yet. Show the user benefit first."*
- Specs（mobile/tablet portrait 与 landscape 同值）：`Headline: Type 24sp, Leading 32sp`；`Subhead 1: Type 15sp, Leading 24sp`（Desktop 为 `Subhead: Type 16sp, Leading 24sp`）；`32sp line height`；`56dp padding between the top of button and the center of copy (allowing room for 1-3 lines of text)`；`24dp vertical padding`；Desktop `Horizontal spacing from image to arrow: 48dp`；`Copy and UI are center-aligned ... with 24dp padding`；*"Ensure that the background and text color meet minimum contrast ratios for accessibility."*

**自动轮播与可访问性的冲突（工程约定）**：`every two to three seconds` 的自动推进是**内容自动变化**，与 SC 2.2.2 Pause, Stop, Hide / SC 2.2.1 的调整要求存在张力。本文件给出的裁决是：**用户一触碰就停**（原文已有），并且首屏更快推进只用于「表明这不是单屏」，不得用于阻止用户点 Get Started；`prefers-reduced-motion` 下应直接静态呈现。SC 2.2.2 的完整条文归 `accessibility.md`，此处只登记冲突点，不重复阈值。

---

## 9. Apple HIG 引导、按需帮助与 tips 的可验收条文

**Onboarding 五条 best practices（逐字要点）**：*"Teach through interactivity."* / *"Consider providing a collection of context-specific tips instead of a single onboarding flow."* / *"If you need to present a prerequisite onboarding flow, design a brief, enjoyable experience that doesn't require people to memorize a lot of information."* / *"If it makes sense to offer a separate tutorial, consider making it optional."* / *"Keep onboarding content focused on the experience you provide."*（最后一条即 *"they don't need to learn how to use the system or the device"*）。

总纲：*"Ideally, people can understand your app or game simply by experiencing it, but if onboarding is necessary, design a flow that's fast, fun, and optional."*

**Offering help 的精确阈值**：

| 条 | 逐字 | 落成验收 |
|---|---|---|
| 帮助形态按任务复杂度选 | *"In general, directly relate the help you provide to the precise action or task people are doing right now and make it easy for people to dismiss or avoid the help if they don't need it."* | 帮助必须与当前动作同屏可达、可关 |
| 不教标准控件 | *"**Avoid bloating your help content by explaining how standard components or patterns work.**"* | 引导文案里出现「点击按钮」「下拉菜单」即判冗余 |
| tip 的能力上限 | *"**Use tips for simple features.** ... **If a feature requires more than three actions, it's probably too complicated for a tip.**"* | >3 步改用交互式演练或改设计 |
| tip 长度 | *"**Keep your tips to one or two sentences** and avoid including content that's promotional"* | ≤2 句；不得夹带营销 |
| tip 频次 | *"set the display frequency so tips display at a reasonable cadence — for example, **once every 24 hours**"* | 全局节流，不按组件各自计数 |
| tip 受众 | *"Not everyone benefits from every tip. For example, people who've already used a feature won't appreciate viewing a tip that describes it."* | 用事件/参数 eligibility 规则，已用过就不再提示 |
| tooltip 长度（macOS / visionOS） | *"limit tooltip content to a **maximum of 60 to 75 characters** (note that localization often changes the length of text)"* | 中文本地化后要重新量，不能照搬英文字符数 |
| tooltip 措辞 | *"**In general, avoid repeating a control's name in its tooltip.**"* / *"Explain the action or task the control initiates."* / *"Use sentence case."* | 以动词开头，不复述控件名 |

**与 NN/g 的合流**：Apple 的 *"context-specific tips"* 与 NN/g 的 *"highlight it when it's actionable for them"*（例：用户记录 7 天习惯数据后才提示统计功能）是同一条规则——**信息在能被用上的那一刻才出现**。NN/g 逐字：*"Instead of advertising this functionality before users have the means to do anything with it, highlight it when it's actionable for them."*

---

## 10. 权限时机矩阵与 purpose string 验收

**时机矩阵（工程约定，依据 §2 裁决二）**：

| 场景 | 何时请求 | 依据 |
|---|---|---|
| 数据/资源是 App 能运行的**前提**（导航要定位、AR 要环境） | 可在首启流程内，但要当场说明原因与收益 | *"unless the data or resource is required for your app to function"* |
| 功能首次被使用 | **首次点击该功能入口时** | *"present a permission request when people first access the specific function"* |
| 只为营销 / 分析 / 日后推送 | 首启不问；完成第一个价值动作后再评估 | *"Asking for more data than a feature needs — or asking for data before a person shows interest in the feature — can make it hard for people to trust your app."* |
| 用户已拒绝过 | 不再自动弹；给设置入口与说明 | 工程约定（HIG 未逐字规定），与 `design-ethics-inclusion.md` 的对称选择一致 |

**purpose string 验收器（§20.2）依据的逐字标准**：*"Aim for a brief, complete sentence that's straightforward, specific, and easy to understand. **Use sentence case, avoid passive voice, and include a period at the end.**"*

Apple 给出的三行对照（逐字）：

| 例 | 裁决 |
|---|---|
| *"The app records during the night to detect snoring sounds."* | *"An active sentence that clearly describes how and why the app collects the data."* ✅ |
| *"Microphone access is needed for a better experience."* | *"A passive sentence that provides a vague, undefined justification."* ❌ |
| *"Turn on microphone access."* | *"An imperative sentence that doesn't provide any justification."* ❌ |

**Pre-alert（系统弹窗前的自定义说明页）——平台特定规则，不可泛化到 Web**：

- *"**Include only one button and make it clear that it opens the system alert.**"*
- *"Another type of manipulation is using a term like 'Allow' to title the custom screen's button ... **Use a term like 'Continue' or 'Next'**"*
- *"**Don't include additional actions in your custom screen or window, unless needed to obtain a legal consent.**"* 原文连列两条禁令：*"Don't include an option to cancel."* / *"Don't include an option to close the view."*

> **边界警告**：这条「不能有取消/关闭」与 `design-ethics-inclusion.md` 的「对称选择 / 一键关闭」看似冲突，实则是**作用域不同**。Apple 这条只约束「受保护资源的系统权限弹窗之前的自定义页」，理由是防止自定义页稀释系统弹窗的选择权；Web 上的 cookie / 追踪同意、营销弹窗、模态框**不受此规则豁免**，仍受对称选择与 `overlays-modality.md` 的退出契约约束。把 Apple 的 pre-alert 规则搬到 Web 同意层，是本文件明确禁止的误用。

**Tracking requests（逐字）**：*"If you want to perform app tracking as soon as people launch your app, you must display the system-provided alert **before you collect any tracking data**."* / *"**Never precede the system-provided alert with a custom screen or window that could confuse or mislead people.**"* / *"**Don't offer incentives for granting the request.** You can't offer people compensation for granting their permission, and you can't withhold functionality or content or make your app unusable until people allow you to track them."* 原文列出的会被拒的设计：offering incentives、displaying a screen that looks like a request、displaying an image of the alert、annotating the screen behind the alert。

---

## 11. WCAG 四条款矩阵：首次体验的合取验收

### 11.1 重复输入与自动回填：autocomplete 不足够的 3.3.7 裁决（Level A）

条文逐字：*"Information previously entered by or provided to the user that is required to be entered again in the same process is either: auto-populated, or available for the user to select."* 三例外：*"re-entering the information is essential"* / *"the information is required to ensure the security of the content"* / *"previously entered information is no longer valid"*。

首次体验落地：

- 注册向导多步之间**不得重复索要**同一信息；出错回显时 *"Submitted information, such as credit card number, is not cleared from the form."*（原文 Examples）。
- *"Data which is 'available to select' would need to be on the same page. Ideally, it would be visible by default and closely associated with the input where the data is required."* ——「藏在上一页让用户回去抄」不合格。
- *"The autocomplete feature of browsers is not considered sufficient"*（见 §2 裁决三）。
- 充分技术：`G221 Provide data from a previous step in a process`。
- 隐私提醒（原文）：*"authors should ensure data protection when storing information even temporarily during a process."*

### 11.2 SC 3.3.8 Accessible Authentication (Minimum)（Level AA）

条文逐字见 §2 表格；四选项 `Alternative` / `Mechanism` / `Object Recognition` / `Personal Content`。`Note 2` 逐字：*"Examples of mechanisms that satisfy this criterion include: support for password entry by password managers to reduce memory need, and copy and paste to reduce the cognitive burden of re-typing."*

首次体验落地（注意适用范围）：

- **适用**：老用户登录、OTP 验证、找回账号、2FA。*"If there is more than one step in the authentication process ... **all steps need to comply**"*；*"A service that requires *manual* transcription of a verification code is not compliant."*
- **不适用但建议照做**：*"It does *not* cover creation of a username or initiation of an account."*；密码管理器与粘贴的技巧 *"can also reduce the cognitive burden in account creation"*。
- 明令失败：*"Blocking people from pasting into authentication fields ... or using a different format between the copied text and the input field (for example, 'Enter the 1st, 3rd, and 5th character of your password'), would force the user to transcribe information and therefore fail this criterion"*。
- **不要**把「选图识别」当万能解：*"such techniques do not fully support the cognitive accessibility community and should be avoided if possible"*；且 AAA 的 3.3.9 *"are *not* excepted"*。
- 充分技术：`G218 Email link authentication` / `H100 Providing properly marked up email and password inputs`。

### 11.3 聚焦即弹帮助框的禁令：G107 与 3.2.1 合取裁决（Level A）

条文逐字：*"When any user interface component receives focus, it does not initiate a change of context."* 官方失败例逐字：*"**Example of a Failure: A help dialog** — When a field receives focus, a help dialog window describing the field and providing options opens. As a keyboard user tabs through the web page, the dialog opens, moving the keyboard focus away from the control every time the user attempts to tab past the field."*

**这条是「首次体验自动弹引导」最直接的合规红线**：任何「字段一聚焦就弹出引导卡并接管焦点」的实现，逐字命中官方失败例。`changes of context` 定义含 *"focus"* 与 *"viewport"*；充分技术 `G107: Using "activate" rather than "focus" as a trigger for changes of context`；常见失败 `F55`。

配套：hover/focus 触发的附加内容还要过 SC 1.4.13 的 Dismissible / Hoverable / Persistent 三条件，浮层遮挡过 SC 2.4.11 —— 这两条的详细矩阵归 `overlays-modality.md`，本文件只登记**合取关系**。

### 11.4 SC 2.2.1 Timing Adjustable（Level A）

六选项逐字：`Turn off` / `Adjust`（*"at least ten times the length of the default setting"*）/ `Extend`（*"given at least 20 seconds to extend the time limit with a simple action ... and the user is allowed to extend the time limit at least ten times"*）/ `Real-time Exception` / `Essential Exception` / `20 Hour Exception`。

首次体验落地：限时 OTP、限时优惠、自动跳过的引导、超时清空的注册表单都在此列。原文明确安全理由不自动豁免：*"Certain time limits implemented for security reasons, such as time-based / time-limited two-factor authentication tokens, can be considered *essential*, and may be exempt from this criterion. **However, other criteria may apply, such as 3.3.7 Redundant Entry, 3.3.8 Accessible Authentication (Minimum)**"* ——即 OTP 即使靠 essential 过了 2.2.1，仍要过 3.3.8 的粘贴要求。技术：`G133` / `G198`；失败 `F58`；并可能触发 `2.2.5 Re-Authenticating`。

**四条款合取表（工程约定）**：

| 首启元素 | 3.3.7 | 3.3.8 | 3.2.1 | 2.2.1 |
|---|---|---|---|---|
| 多步注册向导 | ✅ 必查 | ⚪ 不适用但建议 | ✅ 必查 | ✅ 必查（超时清空） |
| 登录 / OTP | ⚪ | ✅ 必查 | ✅ 必查 | ✅ 必查 |
| 字段聚焦弹引导 | ⚪ | ⚪ | ✅ **重点** | ⚪ |
| 自动轮播欢迎页 | ⚪ | ⚪ | ⚪ | ⚪（另查 2.2.2 / reduced-motion） |
| 限时验证码 | ✅ 出错别清空 | ✅ 允许粘贴 | ⚪ | ✅ 六选项 |

**§20.3 把这张表编译成可执行断言**。

---

## 12. Coach mark 与 Tour 的叠加层契约、Tour 组件精确 props 与冻结面

**本文件不重复 `overlays-modality.md`**：coach mark 作为一层内容盖在界面上时，`inert` / 焦点循环 / `aria-modal` 双条件 / top layer / Escape / 焦点归位 / SC 1.4.13 / SC 2.4.11 的判定全部去那里。这里只给**首次体验专属**的四条：

1. **优先非模态**。Ant Design Tour 逐字：*"Use `mask={false}` to make Tour non-modal. At the meantime it is recommended to use with `type="primary"` to emphasize the guide itself."* 默认 `mask` 是 `true`，**要显式关掉才是非模态**——这是默认值层面就存在的引导副作用。
2. **被解释的控件必须仍可操作**：Ant Design Tour 的 `disabledInteraction` 默认 `false`（5.13.0），即默认允许与高亮区交互；把它改成 `true` 会把「边做边学」变成「只能看」，与 Apple 的 *"Teach through interactivity"* 相反。
3. **一次只一条、不与任务抢焦点**：§11.3 的 SC 3.2.1 是硬红线；`scrollIntoViewOptions` 默认 `true` 会在切步骤时滚动视口，属于 `changes of context` 定义里的 *"viewport"* 范畴，须确认它是**用户点「下一步」的结果**而非自动发生。
4. **必须有键盘与关闭出口**：`keyboard` 默认 `true`（6.2.0）、`closeIcon` 默认 `true`、`onClose` / `onFinish` 都要接；否则违反 `overlays-modality.md` 的退出契约。

**Ant Design Tour 精确 props（官方文档逐字核对，2026-11-12）**：

| prop | 类型 | 默认 | 版本 | 首次体验含义 |
|---|---|---|---|---|
| `arrow` | `boolean \| { pointAtCenter: boolean }` | `true` | — | 指向元素的箭头 |
| `closeIcon` | `React.ReactNode` | `true` | 5.9.0 | 关闭出口必须存在 |
| `disabledInteraction` | `boolean` | `false` | 5.13.0 | 别设 `true`，否则不能边做边学 |
| `gap` | `{ offset?: number \| [number, number]; radius?: number }` | `{ offset?: 6; radius?: 2 }` | 5.0.0（数组 offset 5.9.0） | 高亮区半径与偏移 |
| `keyboard` | `boolean` | `true` | 6.2.0 | 键盘快捷键开关 |
| `placement` | 12 方向 + `center` | `bottom` | — | `target={null}` 时居中 |
| `mask` | `boolean \| { style?, color? }` | `true` | — | **`mask={false}` 才非模态** |
| `type` | `default \| primary` | `default` | — | 非模态时建议 `primary` |
| `open` / `current` | `boolean` / `number` | — | — | 受控，便于「跳过即不再出现」 |
| `scrollIntoViewOptions` | `boolean \| ScrollIntoViewOptions` | `true` | 5.2.0 | 视口滚动要由用户动作触发 |
| `zIndex` | `number` | `1001` | 5.3.0 | 与 `overlays-modality.md` 的语义 z-index 分界对齐 |
| `getPopupContainer` | `(node) => HTMLElement` | `body` | 5.12.0 | 影响 top layer / 遮挡判定 |
| `indicatorsRender` / `actionsRender` | 函数 | — | 5.2.0 / 5.25.0 | 进度与操作可定制 |
| `onClose` / `onFinish` / `onChange` | 回调 | — | — | 跳过与完成的持久化埋点 |

组件 token 精确值：`closeBtnSize = 22`、`zIndexPopup = 1070`、`primaryNextBtnHoverBg = rgb(240,240,240)`、`primaryPrevBtnBg = rgba(255,255,255,0.15)`。全局 token 里 `colorPrimary = #1677ff`、`fontSize = 14`、`borderRadiusLG = 8`、`motionDurationMid = 0.2s`、`motionDurationSlow = 0.3s`。

> 数值归属提醒：`zIndex` / `zIndexPopup` 是**组件实现默认值**，不是本知识库的语义层级刻度；语义 z-index 与 top layer 的分界归 `shape-elevation.md` / `overlays-modality.md`。

---

## 13. 教学型 starter content：首启教学分量与单主行动

首次进入尚无内容时，零数据位本身就是最短的教学位：先替换原本要显示的元素，再按主次分配教学分量，别用尚未学会的行话。

Carbon Empty states 逐字：*"Empty states occur when there is no data to display, often during first-time use or when content has been deleted or is unavailable."* 并明确把 onboarding / starter content 列为空态的 *"in-depth supplements and alternatives for first use empty states"*。

** anatomia 五件套（Carbon 逐字结构）**：`Image (optional)` → `Title`（*"A short and concise explanation. Where possible, write this as a positive statement."*，例 *"Start by adding data assets"* 优于 *"You don't have any data assets."*）→ `Body`（*"Explain clearly the next action to populate the space. You may also explain why the space is empty and include the benefit of taking this step."*）→ `Primary action—button or link in copy (optional)` → `Secondary call to action (optional)`。

**四条首次体验专属裁决**：

1. **空态要替换原本会出现的元素**：*"**Empty states should replace the element that would ordinarily show**. For example, an empty state for a table would replace the table and the column headers and footer should not be present. This practice avoids having a screen reader read the entire table before getting to the message that there is no content in the table."* ——这条把可访问性和首次体验绑在一起。
2. **只给一个主行动**：*"**Don't cover multiple options in one empty state.** If there are multiple things a user can do, pick the most important and keep the focus on that action."* 与 Material 1 Quickstart 的 *"Rather than leaving users on a blank screen, your UI should encourage interaction."* / *"Don't leave users with nothing to do."* 一致。
3. **别用用户还没学会的行话**：*"Don't use product-specific terms that the user may not yet understand."*；也 *"don't lead the user into a dead end. If there are useful next steps, include them."*
4. **教学分量按主次分配**：*"save the more involved educational moments for primary features and more complex situations"*；*"a primary resource on a page could benefit from a more educational approach, while basic empty states may suffice for secondary resources."*

**多空态并存时的按钮降级**：*"In situations where there could be multiple empty states showing at once, we recommend using a tertiary button for the call to action. This avoids scenarios with multiple primary action buttons in the UI."* 对齐方式：*"Empty state elements should be left-aligned as a block. The one exception ... is an empty state in a small tile."*

**starter content 的定位（工程约定）**：它是「让零数据位看起来像已经能用」的示例内容，不是教程；一旦用户产生真实数据必须可一键清除，且不得污染统计口径。Carbon 把 `in-line documentation / onboarding / starter content` 并列为 first-use 的补充路径，但**没有给出逐字数值**（见 §22 限制）。

Ant Design `Empty` 组件提供 `description` / `image` / `imageStyle` / `children` 等承载位（`ant.design/components/empty`，本轮 HTTP 200），本文件只登记其存在，不把组件 props 当设计规范。

> 边界：`feedback-states.md §5` 管五种空的类型、五件套结构与文案公式；本文件只管**「首次使用」这一时刻把空态当教学位**的选型与分量。两者互补，不互相覆盖。

---

## 14. Activation / Aha Moment / Time to Value 的口径

这一节只定义口径与常见误判，**统计方法归 `design-measurement-research.md`**（SUS、样本量、A-B 检验都在那里）。

| 指标 | 口径（工程约定） | 常见误判 |
|---|---|---|
| **Activation rate** | 某注册 cohort 在 N 天内到达「与留存相关的首个核心动作」的比例 | 把「注册成功」「看完引导」当激活；跨产品比数值（定义不同则不可比） |
| **Time to Value (TTV)** | 从注册 / 首启到该核心动作的时长中位数 | 用均值（长尾严重）；把教程播放时长排除在用户总负担之外 |
| **Step completion** | 每一设置步骤的完成率 | 把跳过率下降当成激活率上升 |
| **Aha moment** | 用户第一次感知到产品价值的事件，须由留存相关性确定，不能拍脑袋 | 把「第一次点击任意按钮」当 aha |

**三条裁决**：

1. **先定义激活事件，再谈引导效果**。Material 1 的措辞值得借用：*"Choose the action most closely linked to engagement in the first seven days."* / *"You've already identified the behaviors that correspond to increased engagement (in the first session) or increased retention (in the first seven days)"*。**没识别出这个行为就没资格上 Quickstart 模型**，因为 Quickstart 的适用条件正是「你已经知道哪个动作对应留存」。
2. **跳过率 ≠ 激活率**。把某步设为可跳过会稳定抬高该步完成率，却常常对激活无影响（跳过的人恰好没经过那步所承载的价值）。要看 cohort 的 activation，不要看漏斗某一段的完成率。
3. **NN/g 研究给的是「任务级指标」不是「激活指标」**：91%/94% 是任务成功率、SEQ 是单任务主观难度、93.49/85.17 是任务耗时，**都不是留存或激活**。把它转述为「教程降低激活率」是越界推论。

---

## 15. 引导文案与本地化的最小约束

措辞体系归 `ux-writing.md`，这里只登记三条首次体验专属约束：

1. **不教系统、不教标准控件**：Apple HIG *"Keep onboarding content focused on the experience you provide."* + *"Avoid bloating your help content by explaining how standard components or patterns work."*；NN/g *"No matter the form, instructional onboarding should be brief, optional, and should only highlight the minimum that users need to know to use the app."*
2. **平台词要对**：*"don't write copy that tells people to click a button on an iPhone or tap a menu item on a Mac"*；*"If someone's using the Siri Remote with your tvOS experience, don't show tips or images that feature a game controller."*
3. **本地化会改变长度**：Apple tooltip 的 60–75 字符上限逐字带括号 *"(note that localization often changes the length of text)"*；launch screen 禁文字的理由也是 *"any text you display won't be localized"*。中文引导文案不能以英文字符数验收，断行与溢出要按 `i18n-localization.md` / `typography-system.md §6` 复核。

---

## 16. 组件库生态实测（GitHub REST API，2026-11-12 快照）

| 仓库 | star | license (SPDX) | pushed_at | archived | 用途 |
|---|---:|---|---|---|---|
| `kamranahmedse/driver.js` | 27054 | MIT | 2026-11-12 | False | 轻量 product tour / 高亮遮罩 |
| `usablica/intro.js` | 23454 | NOASSERTION | 2026-11-12 | False | 步骤式导览 |
| `shipshapecode/shepherd` | 13829 | NOASSERTION | 2026-11-12 | False | 基于 floating-ui 的 tour |
| `openreplay/openreplay` | 13138 | NOASSERTION | 2026-11-12 | False | 会话回放（用于定位首启流失，非引导组件） |
| `gilbarbara/react-joyride` | 7896 | MIT | 2026-07-09 | False | React tour |
| `elrumordelaluz/reactour` | 4097 | MIT | 2026-05-19 | False | React tour |
| `focus-trap/focus-trap` | 1564 | MIT | 2026-11-11 | False | 焦点约束（配合 `overlays-modality.md`） |
| `ant-design/ant-design` | 100173 | MIT | 2026-11-12 | False | `Tour` / `Empty` 组件（§12 / §13） |
| `mui/material-ui` | 99333 | MIT | 2026-11-12 | False | 组件基线 |
| `radix-ui/primitives` | 19493 | MIT | 2026-10-14 | False | 无样式可访问原语 |
| `carbon-design-system/carbon` | 9616 | Apache-2.0 | 2026-11-12 | False | Empty states pattern（§13） |
| `coryhouse/react-slingshot` | 9623 | MIT | 2023-09-26 | False | **仅供对照：3 年未推送，不推荐新项目** |

**选型裁决**：库只解决「怎么画高亮与步骤」，不解决「该不该引导」。因此先过 §3 六问，再选库；选库时把 `mask` / `disabledInteraction` / `keyboard` / `closeIcon` / 焦点归位当作**冻结的验收面**（改动按 `component-api-design.md` 的 SemVer 判级）。`NOASSERTION` 不等于无许可，须读仓库 LICENSE（§22）。

**本轮 404 记录**：`tether/shepherd`（旧组织名，正确为 `shipshapecode/shepherd`）、`reactour/reactour`（正确为 `elrumordelaluz/reactour`）、`apple/swiftui-tipkit`（无此仓库，TipKit 文档走 Apple Developer Documentation）——按协议登记为取源限制，不作为「库不存在」的结论。

---

## 17. 十二个场景（判型 → 动作）

| # | 场景 | 判型 | 该怎么做 |
|---|---|---|---|
| 1 | 简单工具类 App 要做五屏欢迎轮播 | Q3 否 / Q4 未测 | 砍掉，先测无引导版本；资源投界面 |
| 2 | 空白仪表盘，用户不知道从哪开始 | F 段 / 无数据 | 教学型零数据位：正向标题 + 一句说明 + 单个主行动 |
| 3 | 首次启动就连弹通知 + 定位 + 追踪三个权限 | 裁决二 | 只保留「不授权就不能运行」的；其余移到对应功能首次使用 |
| 4 | 导航 App 首启要定位 | 裁决二例外成立 | 可在首启流程内请求，但当场说明原因与收益 |
| 5 | 输入框一聚焦就弹引导卡并抢焦点 | SC 3.2.1 | 改为显式激活触发（`G107`）；引导不接管焦点 |
| 6 | 多步注册第 3 步又要填一遍邮箱 | SC 3.3.7 | 自动回填或同页可选；不能只靠 `autocomplete` |
| 7 | 注册页禁止粘贴密码 / OTP | SC 3.3.8 边界 | 3.3.8 不覆盖注册，但按同页建议允许粘贴；登录/OTP 则必须 |
| 8 | 60 秒验证码倒计时后清空整张表单 | SC 2.2.1 + 3.3.7 | 走六选项之一；超时不清空已填内容 |
| 9 | 隐藏手势「左滑归档」没人发现 | Q3 是 | 只在该列表第一次出现时给一条情境提示，1–2 句 |
| 10 | 用户已跳过教程，第二次启动又弹 | HIG 跳过契约 | 持久化跳过状态；在帮助/设置里保留入口 |
| 11 | 首启让用户选主题配色 | §5 | 延后；视觉定制不属于首启 |
| 12 | 大版本改版，老用户找不到新入口 | R 段 / 新功能 | 可对**现有用户**做一次性功能引导；NN/g *"feature onboarding can be helpful to existing users when new features are released"*，但 *"Limit the usage of feature onboarding to what is truly new to users"* |

---

## 18. 二十条反模式

1. 首启五屏 deck-of-cards 轮播，教的是界面上已经写着的标签。
2. 用教程补救一个本来就该重做的界面（*"Instructional onboarding should not be used to supplement poor design."*）。
3. 把 launch screen 做成品牌动画 / 放 logo / 放未本地化的文字。
4. 把 splash screen 停留到「用户能读完」，而不是「一瞥就够」。
5. 首次启动批量申请所有权限。
6. purpose string 写被动句（*"Microphone access is needed for a better experience."*）或命令句（*"Turn on microphone access."*）。
7. 把 Apple 的 pre-alert「不许有关闭按钮」搬到 Web cookie 同意层。
8. tracking 系统弹窗前放诱导页、给授权奖励、或把 App 变得不可用直到授权。
9. 把「用户注册成功」定义为激活。
10. 把某步完成率 / 跳过率当成激活率汇报。
11. 引导卡盖住它正在解释的控件。
12. 遮罩 + 聚光灯挡住待办任务，用户只能乱点找出口。
13. 自动轮播每 2–3 秒推进且用户触碰后仍不停。
14. `mask` 用默认值 `true` 却宣称「我们做的是轻量提示」。
15. `disabledInteraction=true`，把边做边学改成只能看。
16. 字段聚焦即弹引导并抢焦点（SC 3.2.1 官方失败例）。
17. 多步流程重复索要同一信息，或出错后清空表单。
18. 只加 `autocomplete` 属性就宣称满足 SC 3.3.7。
19. 禁止粘贴验证码 / 要求「输入密码第 1、3、5 位」。
20. 引导只做「跳过」不做「以后在哪找回」。

---

## 19. 二十项自检（交付前逐条过）

1. 有没有测过完全无引导的版本？卡点有记录吗？
2. 每个首启问项都能说出「它改变了第一屏的什么」吗？
3. 引导是否可跳过？跳过后是否持久化、不再出现？
4. 跳过后在帮助 / 账户 / 设置里能找回吗？
5. 教程 / 提示是否只针对用户猜不到的独特之处？
6. 是否避免了教标准控件、教系统、教设备？
7. 帮助是否出现在用户当前动作附近，且可立即关闭？
8. 每条 tip 是否 ≤2 句、≤3 步、无营销内容？
9. tip 是否有全局频次节流与「已用过就不再提示」的受众规则？
10. 每个权限请求能否指向一个用户刚表现出兴趣的具体功能入口？
11. purpose string 是否为句末带句号的主动、具体、完整句？
12. pre-alert 是否只有一个按钮、且未用 "Allow" 之类字样？
13. tracking 系统弹窗是否在任何追踪数据采集**之前**显示、且无激励？
14. 多步流程是否自动回填或同页可选，而非依赖浏览器 autocomplete？
15. 认证 / OTP 是否允许粘贴与密码管理器填充？是否所有步骤都过？
16. 是否有任何「聚焦即弹出并抢焦点」的实现？
17. 时限是否落在 SC 2.2.1 六选项之一？超时是否不清空已填内容？
18. coach mark 是否非模态优先、有 Escape / 关闭 / 焦点归位 / 不遮挡焦点项？
19. 零数据位是否替换了原本的元素、只给一个主行动、不用行话？
20. 激活事件是否已定义为「与留存相关的首个核心动作」，并按 cohort 度量？

---

## 20. 五段可抄代码（严格模式，实跑 5/5 rc=0）

以下脚本是本知识库的**工程裁决编码**，不是 W3C / Apple / NN/g 提供的判定程序；把逐字条文简化成布尔断言，**不能替代真机、读屏器与键盘走查**。均以 `python references/_tmp_xxx.py` 方式独立运行，标准库即可，无第三方依赖。

### 20.1 六问判型器：`onboarding_decide.py`

```python
# -*- coding: utf-8 -*-
"""§3 六问判型：把「要不要做、做哪种」编译成断言。"""
import sys

def decide(needs_user_info, highly_personalized, unique_interaction,
           tested_without, fixable_by_design, proven_uplift,
           wants_combined_models=False, skip_persisted=True,
           findable_later=True):
    # 硬约束 1：Q4 是闸门
    if not tested_without:
        return "BLOCK: 先测无引导版本（NN/g: test the app with no onboarding before investing）"
    # 硬约束 2：能改界面就不许加引导
    if fixable_by_design:
        return "FIX_UI: 改界面后回到 Q4（Resources are better spent for making a UI more usable）"
    if wants_combined_models:
        return "BLOCK: Self-Select 与 Top User Benefits 不得组合（Material 1 逐字禁令）"
    if not skip_persisted:
        return "BLOCK: 跳过状态必须持久化，不得在后续启动重播"
    if not findable_later:
        return "BLOCK: 跳过后须在 help/account/settings 保留入口"
    if unique_interaction and not proven_uplift:
        return "PROTOTYPE: 只对独特交互做情境提示原型并复测，先不上线"
    if highly_personalized and needs_user_info:
        return "SELF_SELECT: 单屏、每屏 <10 项、选项须可察觉且不可由正常使用推断"
    if unique_interaction and proven_uplift:
        return "TOP_USER_BENEFITS: <=3 条收益、2-3s 轮播、常驻 Get Started、触碰即停"
    return "QUICKSTART: 直接进界面；首屏必须有可做的事，不能是空白"

CASES = [
    # (Q1,Q2,Q3,Q4,Q5,Q6, 组合禁令, 跳过持久化, 可找回, 期望)
    (False, False, False, True,  False, False, False, True, True, "QUICKSTART"),
    (True,  True,  False, True,  False, False, False, True, True, "SELF_SELECT"),
    (False, False, True,  True,  False, True,  False, True, True, "TOP_USER_BENEFITS"),
    (False, False, True,  True,  False, False, False, True, True, "PROTOTYPE"),
    (False, False, False, False, False, False, False, True, True, "BLOCK"),
    (False, False, True,  True,  True,  True,  False, True, True, "FIX_UI"),
    (True,  True,  True,  True,  False, True,  True,  True, True, "BLOCK"),
    (False, False, False, True,  False, False, False, False, True, "BLOCK"),
    (False, False, False, True,  False, False, False, True, False, "BLOCK"),
]

def main():
    bad = []
    for i, row in enumerate(CASES, 1):
        *args, expected = row
        got = decide(*args)
        if not got.startswith(expected + ":") and got != expected:
            # BLOCK/FIX_UI 以 "XXX: ..." 返回，统一取前缀比较
            if not got.startswith(expected):
                bad.append((i, expected, got))
        print("  case %d -> %s" % (i, got.split(":")[0]))
    if bad:
        print("FAIL", bad)
        return 1
    print("OK 六问判型 9/9，Q4 闸门 / 组合禁令 / 跳过契约全部生效")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### 20.2 权限时机与 purpose string 验收器：`permission_gate.py`

```python
# -*- coding: utf-8 -*-
"""§10：purpose string 四条硬标准 + pre-alert / tracking 禁令。"""
import sys

VAGUE = ("better experience", "improve", "enhance", "体验", "优化服务")
PASSIVE = (" is needed", " is required", " is used", "被需要", "被用于")
IMPERATIVE = ("turn on ", "enable ", "allow ", "请开启", "请允许")

def check_purpose(s: str):
    errs = []
    t = s.strip()
    if not t.endswith("."):
        errs.append("缺句末句号（HIG: include a period at the end）")
    low = t.lower()
    if any(p in low for p in PASSIVE):
        errs.append("被动句（HIG 反例: Microphone access is needed for a better experience.）")
    if any(p in low for p in IMPERATIVE):
        errs.append("命令句且无理由（HIG 反例: Turn on microphone access.）")
    if any(v in low for v in VAGUE):
        errs.append("理由模糊未定义")
    if t[:1].isupper() is False:
        errs.append("首字母未大写")
    if len(t.split()) < 5:
        errs.append("过短，未构成完整句")
    return errs

def check_timing(required_to_function: bool, at_launch: bool,
                 feature_first_used: bool, has_reason: bool):
    if required_to_function:
        return [] if has_reason else ["首启例外成立但缺「为什么需要 + 授予收益」说明"]
    if at_launch and not feature_first_used:
        return ["违反 HIG: Avoid requesting permission at launch unless ... required for your app to function"]
    if not at_launch and not feature_first_used:
        return ["请求时机没有落到「功能首次被访问」"]
    return []

def check_pre_alert(buttons, labels, has_cancel, has_close, legal_consent=False):
    errs = []
    if len(buttons) != 1 and not legal_consent:
        errs.append("pre-alert 只允许一个按钮（unless needed to obtain a legal consent）")
    if any(l.strip().lower() in ("allow", "允许", "同意") for l in labels):
        errs.append("自定义按钮不得用 Allow 类字样，应使用 Continue / Next")
    if (has_cancel or has_close) and not legal_consent:
        errs.append("pre-alert 不得提供 cancel / close")
    return errs

def check_tracking(alert_before_collection, incentive, blocks_app, mimics_system_alert):
    errs = []
    if not alert_before_collection:
        errs.append("系统弹窗必须在采集任何 tracking 数据之前显示")
    if incentive:
        errs.append("不得为授权提供激励")
    if blocks_app:
        errs.append("不得因拒绝追踪而使 App 不可用")
    if mimics_system_alert:
        errs.append("自定义页不得仿冒系统弹窗 / 展示弹窗图片 / 标注弹窗背景")
    return errs

def main():
    cases = [
        ("The app records during the night to detect snoring sounds.", 0),
        ("Microphone access is needed for a better experience.", 2),
        ("Turn on microphone access.", 2),
        ("The app uses your location to show nearby stores.", 0),
    ]
    for text, n in cases:
        got = check_purpose(text)
        print("  purpose %-62s -> %d errs" % (text[:60], len(got)))
        if len(got) < n:
            print("FAIL 漏判:", text, got); return 1
    assert check_timing(False, True,  False, False), "启动批发权限应被拒"
    assert not check_timing(True,  True, False, True), "功能前提型首启应放行"
    assert not check_timing(False, False, True, False), "功能首用应放行"
    assert check_pre_alert(["continue", "cancel"], ["Allow"], True, True), "pre-alert 违规应被拒"
    assert not check_pre_alert(["continue"], ["Next"], False, False), "单按钮合规应放行"
    assert check_tracking(False, True, True, True), "tracking 四项违规应被拒"
    assert not check_tracking(True, False, False, False), "tracking 合规应放行"
    print("OK purpose 4 例 + 时机 3 例 + pre-alert 2 例 + tracking 2 例")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### 20.3 WCAG 四条款合取检查器：`first_run_a11y_gate.py`

```python
# -*- coding: utf-8 -*-
"""§11：3.3.7 / 3.3.8 / 3.2.1 / 2.2.1 的首次体验合取断言。"""
import sys

def sc337(repeats_info, autopopulated, selectable_on_same_page,
          browser_autocomplete_only, essential_or_security_or_stale):
    if not repeats_info or essential_or_security_or_stale:
        return []
    if autopopulated or selectable_on_same_page:
        return []
    errs = ["SC 3.3.7: 重复信息必须 auto-populated 或 available for the user to select"]
    if browser_autocomplete_only:
        errs.append("SC 3.3.7: The autocomplete feature of browsers is not considered sufficient")
    return errs

def sc338(step, blocks_paste, allows_password_manager, transcription_required,
          has_alternative_without_cft, is_account_creation=False):
    # 3.3.8 明确不覆盖账号创建；但工程上仍按同页建议检查粘贴
    scope = "（3.3.8 不覆盖注册，按同页建议检查）" if is_account_creation else ""
    errs = []
    if blocks_paste or transcription_required:
        if not has_alternative_without_cft:
            errs.append("SC 3.3.8 %s: 阻止粘贴 / 要求转录且无替代认证路径" % step + scope)
    if not allows_password_manager and not has_alternative_without_cft:
        errs.append("SC 3.3.8 %s: 未提供 Mechanism（密码管理器填充）或 Alternative" % step + scope)
    return errs

def sc321(focus_triggers_overlay, overlay_moves_focus, triggered_by_activate=False):
    if focus_triggers_overlay and overlay_moves_focus and not triggered_by_activate:
        return ["SC 3.2.1: 命中官方失败例 Example of a Failure: A help dialog（应改用 G107 activate 触发）"]
    return []

def sc221(has_time_limit, turn_off, adjustable_10x,
          warn_20s_and_extend_10x, real_time, essential, over_20_hours,
          empties_form_on_timeout):
    errs = []
    options = [turn_off, adjustable_10x, warn_20s_and_extend_10x,
               real_time, essential, over_20_hours]
    if has_time_limit and not any(options):
        errs.append("SC 2.2.1: 六选项一个都不满足（20s / 10x / 10 次 / 20 hours）")
    if has_time_limit and empties_form_on_timeout:
        errs.append("SC 2.2.1 + 3.3.7: 超时清空已填内容，会话恢复与重复输入双风险")
    return errs

def main():
    assert sc337(True, False, False, True, False), "只靠 autocomplete 应被拒"
    assert not sc337(True, True, False, False, False), "自动回填应放行"
    assert not sc337(True, False, False, False, True), "三例外应放行"
    assert sc338("OTP", True, False, True, False), "OTP 禁粘贴应被拒"
    assert not sc338("OTP", False, True, False, False), "OTP 允许粘贴应放行"
    assert sc321(True, True, False), "聚焦抢焦点应命中官方失败例"
    assert not sc321(True, True, True), "activate 触发应放行"
    assert sc221(True, False, False, False, False, False, False, False), "无限选项应被拒"
    assert not sc221(True, False, False, True, False, False, False, False), "Extend 应放行"
    assert sc221(True, False, False, True, False, False, False, True), "清空表单应被拒"
    print("OK 3.3.7 三例 / 3.3.8 两例 / 3.2.1 两例 / 2.2.1 三例")
    print("   合取关系：OTP 即使靠 essential 过 2.2.1，仍须过 3.3.8 的粘贴要求")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### 20.4 NN/g 数值复核器：`nng_tutorial_guard.py`

```python
# -*- coding: utf-8 -*-
"""§7：把 NN/g 2020-03-08 研究编码成断言，防止转述走样。"""
import sys

STUDY = {
    "participants": 70, "per_group": 35, "apps": 4,
    "success_tutorial": 91, "success_skip": 94, "p_success": 0.443,
    "seq_tutorial": 4.92, "seq_skip": 5.49, "p_seq": 0.047,
    "time_tutorial_s": 93.49, "time_skip_s": 85.17, "p_time": "> 0.1",
    "trials_removed": 13, "trials_removed_pct": 5,
    "seq_scale": (1, 7), "mean": "geometric",
}

def assert_facts(d):
    errs = []
    if d["participants"] != d["per_group"] * 2 or d["apps"] != 4:
        errs.append("样本/分组/应用数不一致")
    if d["success_tutorial"] >= d["success_skip"]:
        errs.append("成功率方向写反：教程组应低于跳过组")
    if d["seq_tutorial"] >= d["seq_skip"]:
        errs.append("SEQ 方向写反：教程组应觉得更难（分数更低）")
    if d["p_success"] < 0.05 or d["p_seq"] >= 0.05:
        errs.append("显著性写反：成功率不显著、SEQ 显著")
    if d["time_tutorial_s"] <= d["time_skip_s"]:
        errs.append("耗时方向写反")
    if d["mean"] != "geometric":
        errs.append("任务耗时用几何平均，不是算术平均")
    return errs

def conclusion():
    # 允许的推论 vs 越界推论
    return {
        "allowed": ["简单 App 的 deck-of-cards 教程不提速、不提成功率",
                    "读教程者主观认为任务更难", "资源应优先投界面"],
        "forbidden": ["教程降低激活率/留存", "所有产品的所有引导都无效",
                      "教程让用户能力下降", "Android 上结论相同"],
    }

def main():
    errs = assert_facts(STUDY)
    if errs:
        print("FAIL", errs); return 1
    c = conclusion()
    print("OK 数值/方向/显著性/统计口径 全部一致（70=35x2, 4 apps, 13 trials / 5%）")
    print("   唯一显著项: SEQ 4.92 vs 5.49 (p=0.047)，方向对教程不利")
    print("   允许推论 %d 条 / 明确禁止越界推论 %d 条" %
          (len(c["allowed"]), len(c["forbidden"])))
    for f in c["forbidden"]:
        print("     ✗", f)
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### 20.5 首启问项归位器：`first_run_questions.py`

```python
# -*- coding: utf-8 -*-
"""§5：每个首启问项都要能说出「它改变了第一屏的什么」。"""
import sys

KEEP = {
    "目标语言": "决定首屏课程内容与界面文案",
    "当前体重": "决定首屏热量目标",
    "账户身份验证": "法规要求，且是进入核心动作的前提",
}
POSTPONE = {
    "主题配色": "视觉定制不属于 onboarding（NN/g 逐字）",
    "多久看一次信息流": "Don't ask for preferences that can be garnered from normal usage",
    "通知权限（仅用于日后推送）": "移到功能首用 / 完成首个价值动作之后",
    "公司规模（仅用于销售分层）": "不改变第一屏，且用户当下无法理解为何要问",
}

def triage(item, changes_first_screen, explainable_now, required_to_start):
    if required_to_start:
        return "KEEP_REQUIRED"
    if changes_first_screen and explainable_now:
        return "KEEP_SELF_SELECT"
    return "POSTPONE"

def main():
    bad = []
    for k in POSTPONE:
        if triage(k, False, False, False) != "POSTPONE":
            bad.append(k)
    for k in KEEP:
        if triage(k, True, True, False) != "KEEP_SELF_SELECT":
            bad.append(k)
    if triage("账户身份验证", False, False, True) != "KEEP_REQUIRED":
        bad.append("账户身份验证")
    if bad:
        print("FAIL", bad); return 1
    print("OK 保留 %d 项 / 后置 %d 项 / 必需 %d 项" %
          (len(KEEP), len(POSTPONE), 1))
    for k, why in POSTPONE.items():
        print("   POSTPONE %-28s %s" % (k, why))
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

---

## 21. 来源与引用（含置信度）

| # | 来源 | 用到的逐字内容 | 置信度 |
|---|---|---|---|
| 1 | Apple HIG · Onboarding（Change log 2024-06-10 / 2023-06-21） | 总纲、五条 best practices、splash / 下载 / 许可 / 非必要设置后置 / 权限整合前置条件 / 评分购买时机 | **厂商指南 / 原文核对** |
| 2 | Apple HIG · Launching | 起止定义、Launch instantly、Downplay、nearly identical、避免文字、Don't advertise、状态恢复、splash 归属 | 厂商指南 / 原文核对 |
| 3 | Apple HIG · Offering help | 帮助形态、>3 actions、1–2 句、24 小时频次、60–75 字符、动词开头、sentence case | 厂商指南 / 原文核对 |
| 4 | Apple HIG · Privacy（Requesting permission / Pre-alert / Tracking / Best practices） | 时机两铁律、purpose string 四条与三行正反例、单按钮与 Continue/Next、禁 cancel/close、tracking 四禁令 | **厂商指南 / 原文核对** |
| 5 | NN/g · *Mobile Tutorials: Wasted Effort or Efficiency Boost?*（A. Kendrick, 2020-03-08） | 70/35+35/4 apps、91/94、p=0.443、4.92/5.49、p=0.047、93.49/85.17、p>0.1、13 trials、几何平均、研究限制、结论 | **一手实证 / 原文核对** |
| 6 | NN/g · *Mobile-App Onboarding: An Analysis of Components and Techniques*（A. Kendrick, 2020-06-21） | *"Instructional onboarding should not be used to supplement poor design."*、三种正当情形、无引导先测四步、视觉 vs 内容定制、feature onboarding 只对现有用户 | 一手分析 / 原文核对 |
| 7 | NN/g · Mobile Instructional Overlay（页面 200，本轮仅作交叉核对） | 情境化 / brief·optional·minimum / overlays 常属 nice-to-have / popup tip 一触即达 | 一手分析 / 交叉核对 |
| 8 | Material Design 1 · Onboarding（`m2.material.io`，**归档版**） | 三模型选型表与组合禁令、fewer than ten choices、90% of the way、up to three、2–3 秒、24sp/32sp/15sp/16sp/56dp/24dp/48dp | **历史规范 / 原文核对，非现行 M3** |
| 9 | W3C WCAG 2.2 Understanding 3.3.7 Redundant Entry（Level A） | 条文、三例外、autocomplete 不足、process 定义、same page、G221、隐私提醒 | **规范级 / 原文核对** |
| 10 | W3C WCAG 2.2 Understanding 3.3.8 Accessible Authentication (Minimum)（Level AA） | 条文四选项、Note 2、不覆盖账号创建、OTP 手动转录不合规、Object Recognition 慎用、G218/H100 | **规范级 / 原文核对** |
| 11 | W3C WCAG 2.2 Understanding 3.2.1 On Focus（Level A） | 条文、changes of context 定义、help dialog 官方失败例、G107、F55 | **规范级 / 原文核对** |
| 12 | W3C WCAG 2.2 Understanding 2.2.1 Timing Adjustable（Level A） | 六选项、20 seconds / ten times / 10x / 20 hours、essential 与 3.3.7·3.3.8 联动、G133/G198/F58 | **规范级 / 原文核对** |
| 13 | W3C WCAG 2.2 Understanding 1.4.13 / 2.4.11 | 仅登记与 coach mark 的合取关系，条文归 `overlays-modality.md` | 规范级 / 交叉引用 |
| 14 | Ant Design · Tour / Empty 组件文档 | `mask`/`disabledInteraction`/`keyboard`/`gap`/`zIndex` 默认值与版本、token 精确值、非模态用法 | 官方文档 / 原文核对 |
| 15 | IBM Carbon · Empty states pattern | 定义、anatomy 五件套、替换元素、单主行动、tertiary 降级、左对齐与例外、教学分量按主次 | 官方文档 / 原文核对 |
| 16 | GitHub REST API `/repos/{owner}/{repo}` | 12 库 star / SPDX / pushed_at / archived（2026-11-12 实测） | 实测快照，会过期 |
| 17 | NN/g · *Onboarding Tutorials vs. Contextual Help*（P. Laubheimer, 2023-02-12） | `push revelation` / `pull revelation` 两条逐字定义、三个章节标题、Implementing Pull Revelations 五条 | **一手分析 / 定稿前补取并触发 §4 勘误** |

**引用纪律**：逐字英文只在本文件出现一次，SKILL.md / README 的转述不得升格为条文；NN/g 的结论必须连同「4 个简单 iOS App / deck-of-cards 教程」限定一起给；Material 1 数值必须连同「归档版、非现行 M3」一起给；Apple pre-alert 规则必须连同「仅限受保护资源的系统权限弹窗之前」一起给。

---

## 22. 取源限制（公开记录，不臆造）

1. **NN/g 教程研究外推边界**：4 个 iPhone App、均为简单应用、仅测 deck-of-cards 教程；原文自列两条泛化风险。本文件不据此断言 Android、复杂企业软件、交互式 walkthrough 或情境提示无效。
2. **任务耗时不含阅读教程时间**，且用几何平均；若把阅读时间计入，原文明确总负担会显著更高。转述 93.49/85.17 时必须带上这两条。
3. **Material 1 是归档规范**：`m2.material.io` 页本轮 200 且数值可逐字核验，但它不是 Material 3 现行规范。§8 全部数值标为历史基线，M3 项目不得直接当合规值；M3 的 onboarding 页为 JS 动态渲染，本轮**未取到**可逐字核验的等价数值（与 #33 的 M3 限制一致）。
4. **本轮勘误：`push / pull revelation` 确实是 NN/g 官方术语**（初版误判为「非官方术语」，已作废）。定稿前补取 Page Laubheimer《Onboarding Tutorials vs. Contextual Help》（2023-02-12），页面含 `Why Tutorials (and Push Revelations) Don't Work` / `What Works: Pull Revelations` / `Guidelines for Implementing Pull Revelations` 三个章节并给出两条逐字定义。故 §4 改为「两套口径并存且不等价」：Laubheimer 的 revelation 二分按触发信号划分，本文件 §4 的 push/pull 是六类形态矩阵的工程简称。保留初版误判于此以便审计；其余三篇 NN/g 文章（front-loading / contextual help / popup tip）的口径不变，勿跨篇混用。
5. **starter content / in-line documentation 无逐字数值**：Carbon 只把它们列为 first-use 补充路径，未给条数、时长或字数阈值；§13 相关建议一律标「工程约定」。
6. **Ant Design Tour 的 props 默认值来自当前文档版本**（含 6.x 字段如 `keyboard` 6.2.0 / `classNames` 6.0.0），升级后须重读；`zIndex` 等是实现默认值，不是设计规范刻度。
7. **GitHub star / pushed_at / archived 是 2026-11-12 快照**，不可当长期事实；`NOASSERTION` 不等于无许可，须读仓库 LICENSE。
8. **三个 404 仓库**（`tether/shepherd`、`reactour/reactour`、`apple/swiftui-tipkit`）本轮已改走正确路径或 Apple 文档，仅登记为取源限制，不推断「库不存在 / 已废弃」。
9. **§14 的 activation / TTV / aha 口径是本知识库的工程约定**，不是 NN/g 或 W3C 给出的标准定义；「与留存相关的首个核心动作」需要各产品自己用 cohort 数据识别，本文件不给跨产品基准值。
10. **§20 五个脚本是工程裁决编码**，把逐字条文简化为布尔条件，不能替代真机 / 读屏器 / 跨浏览器走查；尤其 §20.2 的被动句检测是字符串启发式，不是语法分析器。
11. **本轮未做用户实测**（无真实用户、无读屏器、无跨设备矩阵），所有「场景 / 反模式 / 自检」是规范 + 官方文档 + 一手实证的推理产物，标注为工程约定。
12. **Apple HIG 是平台厂商指南，不是法规**：pre-alert 的「不得提供 cancel/close」只在受保护资源系统权限弹窗语境成立；Web / 小程序 / 桌面端不适用，见 §10 边界警告。
13. **17 个取源 URL 本轮全部 HTTP 200**，但 NN/g / Apple / Material 页面可能随版本更新改文；引用时以页面 Change log 与快照日期为准。

---

## 23. 与既有资产边界矩阵

| 相邻资产 | 它管什么 | 本文件管什么 | 重叠处的裁决 |
|---|---|---|---|
| `overlays-modality.md` | coach mark / 浮层的 inert、焦点、退出、遮挡、Popover 三态 | 引导**该不该出现、什么时候出现、教什么** | 引导作为 overlay 的契约全归前者；时机与内容归本文件 |
| `feedback-states.md` | 五种空态、文案公式、404、toast 时长、骨架屏 | 首次使用把零数据位当教学位的选型与分量 | 空态结构归前者；「首启该用 basic 还是 in-depth」归本文件 |
| `form-table.md` | 表单 label、校验、错误提示、3.3.2/3.3.7/3.3.8 表格侧明细 | 多步注册向导在**首次体验链路**里的合取验收 | 条款明细归前者；四条款合取与接力关系归本文件 |
| `accessibility.md` | WCAG 2.2 全量阈值、focus ring、目标尺寸 | 四条 SC 在首启环节的联合裁决 | 阈值数值归前者；合取表归本文件 |
| `design-ethics-inclusion.md` | cookie wall、对称选择、一键关闭、成瘾设计 | tracking 弹窗前的诱导页禁令、pre-alert 作用域 | 同意合法性归前者；Apple 平台特定规则归本文件并标作用域 |
| `design-measurement-research.md` | SUS / 样本量 / A-B 统计 / 量表方法 | activation / TTV / aha 的**口径定义**与误判 | 统计方法归前者；指标定义与跳过率陷阱归本文件 |
| `ux-writing.md` | 语气、大小写、标点、按钮文案 | purpose string 的句法验收、tip 长度、本地化长度漂移 | 措辞体系归前者；权限文案四条硬标准归本文件 |
| `performance-design.md` | LCP / INP / 首包 / 加载性能 | 启动屏与首启大下载对 L 段的影响 | 性能指标归前者；「launch ≠ splash ≠ onboarding」分界归本文件 |
| `navigation-ia.md` | 导航形态、面包屑、可发现性 | 首启引导不与导航抢位置 | 选型归前者；首启时机归本文件 |
| `component-api-design.md` | props 所有权、SemVer 冻结面、键盘冻结面 | Tour 的哪些默认值属于冻结验收面 | 判级规则归前者；具体默认值清单归本文件 |
| `design-tokens.md` / `component-libraries.md` | 现行 token 与组件库 | Material 1 历史数值、Ant Design Tour token | 现行值归前者；历史基线归本文件并标版本 |
| `knowledge-map.md` | L0→L4 学习路线与支线 | 新增首次体验支线 AF | 路线图归前者；本文件只提供支线内容 |

---

## 24. 接线

**接线**：SKILL.md 资产表 / 意图路由 / 第 5 步 / 第 42 条自检 · mindmap INTENTS · regression NEW_QUERIES · knowledge-map 支线 AF · memory/aliases.json 检索层别名（**不改路由优先级**）· README 统计重算 · `Design-related websites.txt` 第二十三分区。
