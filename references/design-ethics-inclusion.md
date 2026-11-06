# 设计伦理与包容性：欺骗性设计、隐私同意 UI、成瘾机制与认知无障碍

> 快照 2026-11-06 ｜ 24 节（§0 分层导语 + §1–§23）｜ 约 39.3k 字符 / 800 行 ｜ 法规条文、日期、数值取自官方原文；GitHub 仓库 star / 许可 / pushed_at 经 GitHub REST API 实测（2026-11-06）；**未取得原文的数值一律不写入**。
>
> **一句话立场**：设计伦理不是「别做坏事」的道德劝告，是**一组可以写进验收用例的路径长度、按钮构型、点击次数和默认值**。用户同意与否，取决于你给他的**另一条路有多难走**；把「拒绝」做得比「接受」多两步，就已经不是文案问题，是合规问题。本文件只回答一件事：**这个界面，我凭什么判它 PASS 或 FAIL？**

---

## 0. 与既有资产的分层（先判该读哪份）

| 你手上是什么问题 | 去哪份 | 本文件补什么 |
|---|---|---|
| 对比度阈值、焦点环、ARIA、读屏脚本、色盲色板 | `accessibility.md` | §16–§17 补**认知与学习障碍**（COGA 8 目标），不重讲 WCAG 数值 |
| 适老化 / GB/T 37668 硬指标 | `accessibility.md` §适老化 | §17 解释「合规达标但仍具操纵性」为什么可能同时成立 |
| 表单标签、校验、错误文案模板 | `form-table.md` | §7/§10 补**默认值与授权**的法定禁区，不重讲五件套 |
| toast / 弹窗 / 确认框时长与构型 | `feedback-states.md` | §6/§8 补**同意弹窗的按钮对称性**与**开屏广告一键关闭**，这是两套不同判据 |
| 界面文案写法（动词开头、禁 OK） | `ux-writing.md` | §4/§6 补**双重否定、Ask me later、按钮顺序反转**这类被法规点名的措辞陷阱 |
| AI 生成内容的标识与版权 | `ai-design-toolchain.md` | §1 把「判断层不能外包」延伸到**伦理裁决**：AI 同样不能替你判合规 |
| 未成年人 / 防沉迷 / 消费上限 | **本文件 §11（既有资产空白）** | 国务院令第 766 号第 42–45 条逐条落成设计动作 |
| 自动续费 / 取消订阅 / 默认勾选 | **本文件 §9–§10（既有资产空白）** | **2025 年修正后的现行条文**，并纠正广泛流传的过期口径 |
| 隐私同意 / cookie banner / 拒绝追踪 | **本文件 §4–§7（既有资产空白）** | CPPA §7004「对称选择」 + EDPB 六类 + PIPL 五条底线 |

> **边界纪律**：本文件不重讲 WCAG 四档对比度、不重讲 toast 时长、不重讲断点数值。它们是必要条件不是充分条件——**一个对比度 7:1 的按钮，如果「拒绝」藏在第三层设置里，依然是欺骗性设计**。两套判据必须同时过。

---

## 1. 三条不可商量的原则（先给立场，不和稀泥）

1. **对称优于说服。** 同意 UI 的合法性不看主按钮多醒目，看**拒绝路径与接受路径是否等长、等难、等耗时**。这是 CPPA §7004(a)(2) 的法条原文，不是行业最佳实践。
2. **默认即决定。** 预勾选、默认授权、把历史选择设为后续默认，在法律上常常**根本不构成同意**（EDPB：*"pre-ticked boxes or inactivity of the users do not constitute consent"*；中国《网络交易监督管理办法》第 13/17 条明禁）。设计侧不要把「用户可以取消」当免责声明。
3. **意图不是辩护理由。** CPPA §7004(c) 原文：*"A business's intent in designing the interface is not determinative…"* —— 没想操纵，但**知道有问题却不修**，仍可被认定为 dark pattern；「刻意不知情」同样不利。所以「我们没有恶意」在评审会上不是有效论据，**有没有回归测试才是**。

> **与 AI 的关系**：`ai-design-toolchain.md` §1 判定合规判断不能交给 AI。本文件把它写成硬约束——**法条会修订、分类会更新、日期会失效**（§2/§9 各有一处实证），模型最容易 confidently 输出过期口径。伦理裁决必须由人查官方原文后签字。

---

## 2. 分类体系裁决：别再照抄旧教程的那一套（暗黑模式 / dark patterns 现行 18 类）

`deceptive.design`（原 darkpatterns.org）现行 `/types` 页经本轮抓取，链接共 **18 类**，与大量中文教程仍在流传的旧分类（`Roach Motel` / `Privacy Zuckering` / `Forced Continuity` / `Bait and Switch` / `Price Comparison Prevention`）**已经不是同一套**。旧页面里 `Roach Motel`、`Privacy Zuckering` 在现行列表 HTML 中已检索不到；新增了 `addictive-design`、`preselection`、`hard-to-cancel`、`currency-confusion`。

> ⚠️ **反陈旧裁决**：写规范、做培训、建静态扫描规则库时，**以现行 18 类为准**，不要从记忆里默写。旧名可作为别名保留在检索层（见 `memory/aliases.json`），但**不能当作现行分类写进交付物**。

现行 18 类（slug 取自页面链接，中文为便于检索的自译，不是官方译名）：

| # | slug | 中文检索名 | 界面上的典型形态 | 一条可验收的否决规则 |
|---|---|---|---|---|
| 1 | `sneaking` | 偷渡 /  sneak into basket | 结算时多出一项用户没加的东西 | 购物车增项必须有用户显式动作且可单独移除 |
| 2 | `forced-action` | 强制动作 | 必须关注/填问卷才能继续 | 「继续」不得绑定无关附加义务 |
| 3 | `hard-to-cancel` | 难以取消 | 订阅一键开、取消要打电话 | 取消入口与订阅入口**同层级可达**（§9） |
| 4 | `preselection` | 预勾选 | 默认勾上营销授权 / 附加险 | 非必需项默认必须为**未选中**（§10） |
| 5 | `obstruction` | 阻碍 | 拒绝按钮灰掉、取消流程卡在客服 | 拒绝控件不得 disabled、不得依赖人工介入 |
| 6 | `hidden-subscription` | 隐藏订阅 | 免费试用悄悄转付费 | 转化前须显著提醒且可自主选择（§9） |
| 7 | `hidden-costs` | 隐藏费用 | 最后一步才出现服务费 | 总价在**用户承诺前**完整可见 |
| 8 | `trick-wording` | 诡辩措辞 | 双重否定、「不必不接收」 | 同 §4(3)，禁双重否定 |
| 9 | `visual-interference` | 视觉干扰 | 拒绝按钮低对比/极小/被遮挡 | 两选项视觉权重**同级**（§6） |
| 10 | `fake-social-proof` | 假社会认同 | 编造「刚刚有人购买」 | 无真实数据不得渲染动态人数 |
| 11 | `fake-urgency` | 假紧迫 | 恒定倒计时、假限时 | 倒计时须有真实服务端截止时刻 |
| 12 | `nagging` | 反复纠缠 | 拒绝后每次启动再弹 | 拒绝后不得就同一目的重复弹（§10 第 16 条） |
| 13 | `fake-scarcity` | 假稀缺 | 「仅剩 1 件」但库存不联动 | 库存文案须由实时数据驱动 |
| 14 | `disguised-ads` | 伪装广告 | 广告长得像正文/系统按钮 | 广告须可辨识（§8） |
| 15 | `confirmshaming` | 羞辱式确认 | 「不，我不想省钱」 | 拒绝文案不得带评价、贬损、情绪诱导 |
| 16 | `comparison-prevention` | 阻止比价 | 隐藏单价、单位不统一 | 可比规格与单位须同屏可见 |
| 17 | `addictive-design` | 成瘾设计 | 无限滚动、自动播放、连胜中断 | 须有可关闭开关与终点（§12） |
| 18 | `currency-confusion` | 货币混淆 | 虚拟币掩盖真实价格 | 须同时给出法币等值 |

> **用法边界**：18 类是**现象清单**，不是判定标准。真正能判 PASS/FAIL 的是 §3（EDPB 六类，按**操纵机制**分组）、§4（CPPA 五原则，按**路径**判定）和 §7–§11（法条红线）。**现象会变，机制与法条更稳**——所以静态扫描应优先断言「路径是否对称」「默认值是否为 false」，而不是去枚举某个花哨的新套路叫什么名字。

---

## 3. EDPB Guidelines 03/2022 v2.0：六类机制（官方 PDF 74 页，一手）

来源：EDPB《Guidelines 03/2022 on deceptive design patterns in social media platform interfaces》**Version 2.0, 14 February 2023**（v1.0 为 2022-03-14 公开征求意见版）。适用语境是社交媒体平台界面的 GDPR 合规，但**六类机制可直接迁移到任何同意/设置界面**。

| 类 | 原文名 | 子型（原文列举） | 设计侧的诊断问句 |
|---|---|---|---|
| 1 | **Overloading**（过载） | `Continuous prompting` / `Privacy Maze` / `Too Many Options` | 用户是否被弹窗频次、层级深度或选项数量拖到放弃？ |
| 2 | **Skipping**（跳过） | `Deceptive Snugness` / `Look over there` | 界面是否用默认「看起来贴心」或视觉引导让用户**跳过**关键设置？ |
| 3 | **Stirring**（煽动） | `Emotional Steering` / `Hidden in plain sight` | 是否用情绪化措辞/配色，或把关键项混进大片文本里？ |
| 4 | **Obstructing**（阻碍） | `Dead end` / `Longer than necessary` / `Misleading action` | 拒绝是否走进死路、流程被拉长、按钮作用被误导？ |
| 5 | **Fickle**（多变） | `Lacking hierarchy` / `Decontextualising` / `Inconsistent Interface` / `Language Discontinuity` | 层级、上下文、控件位置、语言是否在流程中**不一致地变化**？ |
| 6 | **Left in the dark**（蒙在鼓里） | `Conflicting information` / `Ambiguous wording or information` | 不同页面的说法是否互相矛盾、措辞是否含糊？ |

**四条原文级硬口径**（可直接抄进验收表）：

- 预勾选与沉默不构成同意：*"pre-ticked boxes or inactivity of the users do not constitute consent"*。
- 撤回与给予**同难度**（"mirroring effect"）：*"it shall be as easy to withdraw as to give consent"* —— 与 §4 CPPA「对称选择」是同一条原则的两种表述。
- 组织责任：原文要求 *"interdisciplinary teams, consisting, among others, of designers, data protection officers and decision-makers"* —— **设计师被明确列为责任主体**，不能把 dark pattern 全推给法务或增长团队。
- `Annex II: Best practices`（PDF 第 73 页）给出正向建议，含 `Shortcuts`（把隐私设置做成直达捷径）等。

> **DSA 分工口径**（来自该 PDF 脚注，非二手转述）：DSA Article 25(2) 规定，已被 UCPD（不公平商业行为指令）或 GDPR 覆盖的实践**不再适用 DSA 25(1) 的禁止**，监管机构按领域分工。所以「同一个界面到底违反哪部法」不能一句「违反 DSA」糊过去，**先判法域**再判条款（§13 决策矩阵）。

---

## 4. CPPA §7004：把「对称选择」写成可测量的步数（本轮最硬的规则）

来源：California Privacy Protection Agency《CCPA Regulations》最终文本 `20230329_final_regs_text.pdf`（66 页）**§ 7004. Requirements for Methods for Submitting CCPA Requests and Obtaining Consumer Consent**。这是本文件最值得抄进设计系统的一组规则，因为它**给了测量方法**。

### 4.1 (a) 五条设计原则（逐条翻成界面动作）

| 原则（原文） | 界面动作 | 反例（法规点名） |
|---|---|---|
| `(1) Easy to understand` | 语言简明；适用时遵守 §7003 披露规则 | 法律术语堆砌、长句 |
| `(2) Symmetry in choice` | **更保护隐私的路径不得比更不保护隐私的路径更长 / 更难 / 更耗时** | 见 §4.2 |
| `(3) Avoid language or interactive elements that are confusing` | **禁双重否定**；toggle / 按钮须清楚表明选择；按钮位置符合预期 | 见 §4.3 |
| `(4) Avoid choice architecture that impairs choice` | 不设干扰屏、不捆绑不兼容用途；同意须 freely given / specific / informed / unambiguous | 见 §4.4 |
| `(5) Easy to execute` | 不加不必要摩擦；方法须经**功能测试** | 见 §4.5 |

### 4.2 (a)(2) 步数怎么数（法规自己给了起止点）

原文规定：`opt-out` 步数**从用户点击 "Do Not Sell or Share My Personal Information" 链接起算，到请求完成**；`opt-in` 步数**从用户首次向企业表示有意 opt-in 起算，到请求完成**。**两者必须对称**。

三个原文示例，逐条都是可直接写进测试用例的判据：

| 构型 | 法规判定 | 正确构型 |
|---|---|---|
| `Accept All` + `More Information` 或 `Accept All` + `Preferences` | **不对称**：接受只需 1 步，行使权利要额外步骤 | `Accept All` + `Decline All` |
| `Yes` + `Ask me later` | **不对称**：没有「拒绝」，`"Ask me later"` 意味着企业会继续追问 | `Yes` + `No` |
| opt-out 流程步数 > opt-in 流程步数 | **不对称** | 步数相等 |

> **落地口径**：把这两组按钮组合做成**设计系统里的固定组件变体**，不要允许业务方自行配置。出现 `Accept All` 就必须**同屏同级**出现 `Decline All`；「管理偏好」只能是**第三个**入口，不能替代拒绝按钮。

### 4.3 (a)(3) 措辞与控件的三个陷阱

- 在 `Do Not Sell or Share My Personal Information` 这句话旁边放 `Yes` / `No` = **双重否定**，法规明确列为混淆。
- Toggle / 按钮只标 `on` / `off` **可能混淆**，需要补充澄清语言（例如把状态写成「已允许个性化广告 / 已关闭个性化广告」）。
- **按钮顺序反转**：一直按 `Yes` → `No` 排列，却在「用户预期相反」的那一步忽然改成 `No` → `Yes`，法规点名为混淆设计。→ **同一流程内确认/取消的相对位置必须恒定**，写进组件规范。

### 4.4 (a)(4) 选择架构：不许捆绑

法规举例：提供**基于位置的服务**（如查附近油价）时，**不得**把「为提供服务所合理必要的位置使用」与「把地理位置卖给数据中介」这种**不兼容用途**捆成一个同意。必须给**单独选项**。→ 设计动作：**按用途拆分同意项，每项独立开关，服务必需项不出现在同意弹窗里**（它本就不需要同意）。

另：`(4)(A)` 把「提交 opt-out 请求前必须点过若干干扰屏」直接列为损害选择的架构。

### 4.5 (a)(5) 易执行：功能必须真的能跑

- 点击 `Do Not Sell or Share My Personal Information` 后，**不得要求用户在隐私政策长文里搜索/滚动**去找提交机制。
- **已知却不修的循环链接、坏链、无人监控或有激进过滤的邮箱**可能构成违规。
- 让用户**在页面上无谓等待**可能构成违规。

> 这三条的意义：同意 UI 的验收**不是视觉走查，是端到端功能测试**。「链接存在」不算 PASS，「点到底能真的完成」才算。

### 4.6 (b)(c) 法律效力与「意图不是决定性因素」

- `(b)` 不符合 (a) 的方法**可被认定为 dark pattern**；**通过 dark pattern 取得的同意不构成同意**——法规举例：用 dark pattern 取得出售个人信息的同意，企业处于**「从未取得过同意」**的地位。
- `(c)` 判定标准：界面**具有实质性颠覆或损害用户自主、决策或选择的效果**即为 dark pattern；**企业的设计意图不是决定性因素，只是考量因素之一**；企业**知情却不修复**仍可成立；**刻意的无知**（deliberate ignorance）同样不利。

---

## 5. CPPA §7003：可读性、无障碍与「显著链接」的具体要求

同一份法规 **§ 7003. Requirements for Disclosures and Communications to Consumers**：

- 披露与沟通须 **easy to read and understandable to consumers**。
- 格式须**在小屏上可读**（`Use a format that makes the disclosure readable, including on smaller screens`）。
- 须 **reasonably accessible to consumers with disabilities**；在线通知参照 **WCAG version 2.1 of June 5, 2018**（`incorporated herein by reference`）——**这是法规把 WCAG 2.1 写进引用，不是行业自选**。
- 网站上的 **conspicuous link** 须与其他同类链接**以相似方式呈现**，并使用**至少与相邻链接大致相当的字号与颜色**（`at least the approximate size or color as other links next to it`）。
- §7011 隐私政策补充：用平实语言、避免术语；格式小屏可读；**须以企业日常提供合同/免责声明/销售公告的相同语言提供**；须**可打印**；链接文字须含 `privacy` 一词。

> **设计动作**：把「隐私/隐私政策」入口做成页脚**同级链接**，不要变成 10px 灰色、不要塞进折叠区、不要只给图标。中文站的对应做法是入口文案含「隐私」二字且视觉权重与相邻链接一致。

---

## 6. 同意 UI 的 PASS/FAIL 构型表（可直接拿去评审）

| 检查项 | PASS | FAIL | 依据 |
|---|---|---|---|
| 首屏按钮 | `同意全部` + `拒绝全部` 同屏同级 | `同意全部` + `管理偏好` / `了解更多` | §7004(a)(2)(C) |
| 拒绝措辞 | 中性、无评价 | 「不，我愿意继续被追踪」「算了，我不要优惠」 | confirmshaming / EDPB Stirring |
| 双重否定 | 「关闭个性化广告」+ 明确的开/关状态 | 「是否不禁止不出售信息？」+ 是/否 | §7004(a)(3)(A) |
| 按钮顺序 | 全流程恒定 | 关键一步反转 | §7004(a)(3)(C) |
| 步骤数 | 拒绝路径 = 接受路径（按 §4.2 起止点测） | 拒绝多一层、多一次确认 | §7004(a)(2)(A) |
| 撤回入口 | 与授予入口同层级、可达 ≤ 同深度 | 藏在三级设置 / 需联系客服 | EDPB mirroring effect / PIPL 15 |
| 默认值 | 非必需项全部**未选中** | 预勾选、默认授权 | EDPB / 《网络交易办法》13 条 |
| 不同意后果 | 仍可使用服务（必需处理除外） | cookie wall、不授权就退出 | PIPL 16 条 |
| 视觉权重 | 两选项字号/对比度/尺寸同级 | 拒绝按钮低对比、极小、被浮层遮挡 | visual-interference / §7003 |
| 端到端 | 点到底真的完成并留痕 | 坏链、循环、无限等待、无人看管的邮箱 | §7004(a)(5) |
| 干扰屏 | 无 | 拒绝前插 2 屏挽留 | §7004(a)(4)(A) |
| 用途粒度 | 按用途独立开关 | 一个总开关捆绑服务必需 + 数据出售 | §7004(a)(4)(B) |

> **一条容易漏的**：`管理偏好 / Preferences` **不是拒绝按钮**。它把用户带进更长的路径，恰恰构成 §7004(a)(2)(C) 点名的不对称。允许保留它，但只能作为**第三个**入口。

---

## 7. 中国《个人信息保护法》五条 UI 底线（官方全文逐字）

来源：全国人大 `npc.gov.cn` 公布的《中华人民共和国个人信息保护法》全文。以下为条文原意与逐字要点，均可直接转成 UI 验收项。

| 条 | 原文关键句 | 界面红线 |
|---|---|---|
| **第 14 条** | 同意应由个人「**在充分知情的前提下自愿、明确作出**」；处理目的、方式和种类**变更的，应当重新取得个人同意** | 静默扩大用途 = 违规；新增用途必须**重新弹一次**，不能靠「更新了隐私政策」代替 |
| **第 15 条** | 个人**有权撤回其同意**；处理者「**应当提供便捷的撤回同意的方式**」 | 撤回入口必须**便捷**：与授权入口同层级、可自助完成 |
| **第 16 条** | 「**不得以个人不同意处理其个人信息或者撤回同意为由，拒绝提供产品或者服务**」；处理个人信息属于提供产品或服务所必需的除外 | **cookie wall / 不授权不给用 = 直接违反**；只有「必需」才可例外，且举证责任在企业 |
| **第 17 条** | 以**显著方式、清晰易懂的语言**真实、准确、完整告知四项（处理者名称与联系方式 / 目的·方式·种类·保存期限 / 行使权利的方式和程序 / 其他法定事项）；变更须告知变更部分；处理规则须**公开、便于查阅和保存** | 告知不能只在长政策里；入口显著、可查阅、可保存 |
| **第 24 条** | 自动化决策须**透明、结果公平公正**，不得在交易价格等条件上实行不合理差别待遇；信息推送/商业营销须「**同时提供不针对其个人特征的选项，或者向个人提供便捷的拒绝方式**」；对个人权益有重大影响的有权要求说明并**拒绝仅通过自动化决策**作出决定 | 个性化推荐必须给「非个性化」开关或便捷拒绝；**大数据杀熟**是明示禁止项 |

> **与 §4 的关系**：PIPL 15 的「便捷撤回」与 CPPA §7004 的「对称选择」、EDPB 的 mirroring effect 是**同一条原则在三个法域的三种写法**。做一套合规组件时，**按最严的那一套（对称 + 同层级 + 端到端可用）实现，三地同时覆盖**。

---

## 8. 中国《互联网广告管理办法》第 10 条：一键关闭的量化红线

施行：**2023-05-01**。第 10 条对**弹出等形式**发布的互联网广告，要求「**显著标明关闭标志，确保一键关闭**」，并明确列举禁止情形：

1. **没有关闭标志**，或者**计时结束才能关闭**广告；
2. 关闭标志**虚假、不可清晰辨识或者难以定位**等，为关闭广告设置障碍；
3. 关闭广告**须经两次以上点击**；
4. 在浏览**同一页面、同一文档**过程中，**关闭后继续弹出**广告，影响用户正常使用网络；
5. 其他影响一键关闭的行为。

附加口径：

- **开屏广告同样适用**：「启动互联网应用程序时展示、发布的开屏广告适用前款规定」。
- 罚则：拒不改正的，**处五千元以上三万元以下罚款**。

> **可直接量化的三条**：点击次数 **≤1**；关闭标志**无需等待计时**；**同页面同文档内不得复弹**。这三条能写成自动化 E2E 用例，比「体验流畅」有用得多。
>
> **来源层级说明**：本条全文经央广网报道逐字引用核验；市场监管总局官方原文页面本轮未取得可访问 URL，故**不臆造令号**，落地以官方公布文本为准（这是取源纪律，不是遗漏）。

---

## 9. 自动续费：2025 年修正后的现行规则，以及一条必须纠正的过期口径

### 9.1 ⚠️ 反陈旧裁决：「续费前五日」已不是现行表述

大量设计/合规文章、甚至地方法院普法稿仍在写：《网络交易监督管理办法》第 18 条要求**自动续费日期前五日**提醒。**这是 2021 年旧版的表述。**

依据：湖南省人民政府门户网站转载、标注「信息来源：国家市场监督管理总局网站」的《网络交易监督管理办法》全文，版本行明确写着：

> `(2021年3月15日国家市场监督管理总局令第37号公布 根据2025年3月18日国家市场监督管理总局令第101号修正)`

央广网 2025-03-31 报道亦逐字给出第 101 号令《国家市场监督管理总局关于废止和修改部分部门规章的决定》的修改内容与施行日期：**自 2025 年 5 月 1 日起施行**（废止规章 1 部、修改 16 部）。

**现行第十八条全文**（与央广网所引修改后条文一致）：

> **第十八条** 网络交易经营者采取自动展期、自动续费等方式提供服务的，应当在消费者接受服务前和自动展期、自动续费等**日期前**，以显著方式提请消费者注意，由消费者自主选择。
>
> 网络交易经营者采取自动展期、自动续费等方式提供服务的，**在服务期间内**，应当为消费者提供**显著、简便的随时取消或者变更的选项**，并**不得收取不合理费用**。

**裁决**：旧版的「前五日」具体天数在现行条文中**已被「等日期前」取代**。因此：
- ❌ 不要再把「**必须提前 5 日**」写成普适法定数值、写进设计系统规范或做成扫描规则。
- ✅ 应当写成：「**接受服务前 + 每次自动展期/续费日期前均须显著提醒**」（**两个时点**，不是单一个提前量）；业务若有内部提前量（如 T-5）作为风险控制，须标注为**企业自定标准**，不能冒充法条。
- ✅ 若法务要求引用具体天数，**先复核现行有效文本与令号**，不要把旧稿当现行法。

> 这条是本轮「深度蒸馏」最典型的产出：**不是多收了一条链接，而是让一条被广泛抄错的规则不再含糊**。

### 9.2 现行第十八条 → 四条 UI 验收项

| 条款片段 | UI 验收项 | 判据 |
|---|---|---|
| 「消费者接受服务前…显著方式提请消费者注意，由消费者自主选择」 | 开通页告知 | 自动续费事实、周期、金额在**用户点确认之前同屏可见**；不得默认勾选 |
| 「自动展期、自动续费等日期前…显著方式」 | 续费前提醒 | 每个扣费周期前触发一次显著提醒（渠道+留痕） |
| 「服务期间内…显著、简便的随时取消或者变更的选项」 | 取消/变更入口 | **服务全周期**可达；路径深度 ≤ 开通路径；不需联系客服 |
| 「不得收取不合理费用」 | 取消费用 | 取消/变更不附加违约金类不合理收费 |

罚则（同份全文第四十一条）：违反**第十八条第二款**，法律、行政法规无规定的，责令限期改正，**可以处三万元以下罚款**；违反**第十八条第一款**、第二十一条的，依《消费者权益保护法实施条例》第五十条处理。

> **设计口径**：把「取消订阅」做成与「开通订阅」**同一个设置页、同一层级**的对称控件，而不是把它塞进「帮助中心 → 联系客服」。这既是 §9 的法条要求，也是 §4 对称选择、deceptive.design `hard-to-cancel` 的共同指向。

---

## 10. 默认勾选、概括授权、搭售与商业信息：同份规章的另外三条

《网络交易监督管理办法》（2025 修正版）还有三条直接约束 UI 默认值，逐字要点：

- **第 13 条**：不得采用「**一次概括授权、默认授权、与其他授权捆绑、停止安装使用**」等方式，强迫或变相强迫消费者同意收集、使用**与经营活动无直接关系**的信息；收集个人生物特征、医疗健康、金融账户、个人行踪等**敏感信息，应当逐项取得消费者同意**。
  → 设计动作：**一个用途一个开关**；敏感权限逐项单独申请；不能用一个「同意全部」覆盖；不能以「不同意就停止安装/使用」相要挟（与 PIPL 16 呼应）。
- **第 16 条**：未经同意或请求不得发送商业性信息；发送时须明示真实身份与联系方式，并「**向消费者提供显著、简便、免费的拒绝继续接收的方式**」；消费者明确拒绝的「**应当立即停止发送，不得更换名义后再次发送**」。
  → 设计动作：退订入口显著·简便·免费；**拒绝后真正停止**，换马甲再发是明文禁止；与 `nagging` 反模式合并检查。
- **第 17 条**：搭售须显著提醒；提供多种可选项时，「**不得将搭售商品或者服务的任何选项设定为消费者默认同意，不得将消费者以往交易中选择的选项在后续独立交易中设定为消费者默认选择**」。
  → 设计动作：**默认值不继承历史选择**。这是最容易被「记住用户偏好」这个好意踩中的坑——**便利性与自主性冲突时，此条优先**。

> **一条给组件库的硬规则**：`defaultChecked` / `defaultValue` 用于「授权类、搭售类、营销类」控件时，一律 `false`。把它作为 lint 规则，而不是评审时的口头约定。

---

## 11. 未成年人防沉迷：国务院令第 766 号第 42–45 条逐条落成设计动作

来源：中国政府网《未成年人网络保护条例》，**国务院令第 766 号**，2023-09-20 国务院第 15 次常务会议通过，**2023-10-24 发布，自 2024-01-01 起施行**。

| 条 | 原文要点 | 设计动作 | 可验收判据 |
|---|---|---|---|
| **42** | 建立健全**防沉迷制度**；**不得向未成年人提供诱导其沉迷的产品和服务**；及时修改可能造成沉迷的**内容、功能和规则**；**每年向社会公布防沉迷工作情况** | 产品侧需有可迭代的规则配置与年度公开报告机制 | 是否存在「规则可修改」的后台能力；是否有年度报告入口 |
| **43** | 网络游戏/直播/音视频/社交等须**针对不同年龄阶段**设置**未成年人模式**，在**使用时段、时长、功能和内容**四方面按国家规定和标准提供服务；并「**以醒目便捷的方式**」为监护人提供**时间管理、权限管理、消费管理**三项功能 | 未成年人模式 + 监护人控制台（三类管理） | 四维度是否逐项可配；监护人三个入口是否**醒目便捷**、不需翻找 |
| **44** | 应当**合理限制不同年龄阶段未成年人在使用其服务中的单次消费数额和单日累计消费数额**；**不得向未成年人提供与其民事行为能力不符的付费服务** | 单次 + 单日双上限；按年龄分档 | 两个限额是否同时存在、是否按年龄分档、超额是否有明确拦截 |
| **45** | 防范和抵制**流量至上**；**不得设置以应援集资、投票打榜、刷量控评等为主题的网络社区、群组、话题**；**不得诱导未成年人参与**上述活动；并预防和制止其用户诱导未成年人实施上述行为 | 榜单/集资/打榜类功能在未成年人模式下**整体下线** | 未成年人模式下是否存在任何打榜/应援/控评入口；是否有举报与处置链路 |
| **47**（补充） | 落实**适龄提示**，按年龄阶段对游戏分类，并在**用户下载、注册、登录界面**等位置**显著提示** | 三处界面均有适龄标识 | 下载页 / 注册页 / 登录页三处是否都可见 |

> **设计立场**：未成年人保护**不是把成人模式加个弹窗**，而是**另一套产品构型**。第 43 条列了四个维度、第 44 条列了两类额度、第 45 条直接点了三类功能必须不存在——这些是**功能取舍**，不是视觉降级。
>
> **与成瘾设计的关系**：第 42 条「不得提供诱导其沉迷的产品和服务」把 §12 的成瘾机制从「伦理建议」提升为**法定义务**（针对未成年人）。面向未成年人的界面里，无限滚动、自动播放、连胜中断、变比率奖励等机制都需要重新论证必要性。

---

## 12. 成瘾设计：机制清单与「可关闭」红线

**取源纪律（重要）**：U.S. Surgeon General 2023《Social Media and Youth Mental Health》advisory 官方 PDF 在本机出口多次返回 **403**（返回体是 473/490 字节 HTML 错误页，非 PDF），**未取得原文**。因此本节**不引用该 advisory 的逐字结论、不臆造统计数字**。可核验的是 HHS 官方 landing page 给出的面向科技公司的建议方向（加强隐私默认、限制推送、提供时间管理工具等），此处仅作为**方向性参考**，不作为法条或数值依据。

可稳定判定的**机制清单**（来自 deceptive.design 现行 `addictive-design` 类与 EDPB `Overloading: Continuous prompting`）：

| 机制 | 界面形态 | 对用户的实际作用 | 最小整改 |
|---|---|---|---|
| 无限滚动 / 无终点 feed | 无「到底了」状态 | 消除自然停止点 | 提供分页或「已看完」终点 |
| 自动播放下一条 | 倒计时后自动续播 | 取消「是否继续」的决策点 | 默认关闭，或每次需确认 |
| 变比率奖励 | 下拉刷新、随机红点 | 强化重复检查 | 可预测的结果反馈 |
| 连胜 / 连续打卡中断 | streak 归零恐吓 | 用损失厌恶制造登录压力 | 提供补签/暂停且不使用恐吓文案 |
| 高频推送与重复提示 | 拒绝后再弹 | 与 `nagging` / EDPB Continuous prompting 同构 | 拒绝后不再就同一目的提示 |
| 社交认可计量 | 点赞数、公开排名 | 与未成年人条例第 45 条「流量至上」直接冲突 | 未成年人模式下隐藏或下线 |

**四条可验收红线**：
1. **必须存在一个明确的「结束」状态**（到底了 / 今日已看完）。
2. **必须存在可关闭开关**，且关闭状态**被记住**（与 `ai-design-toolchain.md` §10 HAX「可关闭且记住」同构）。
3. **不得以损失厌恶文案驱动回访**（「你的 37 天记录将归零」）。
4. **面向未成年人时按 §11 第 42/45 条整体重新论证**，不是加个提示条。

> **未取得原文的一律不写**：ICO Children's Code Standard 12 `nudge techniques` 的精确条文（旧 ICO URL 本轮 404）、OECD《Dark Commercial Patterns》报告定义与 prevalence 数据（页面 4xx / PDF 404）——**均不写入本资产**，只在 §22 记录为未决取源项。

---

## 13. 欧盟 DSA 第 25 条与 FTC 2022：两套执法口径，别混成一句

### 13.1 DSA Article 25

European Commission `digital-strategy.ec.europa.eu` 的 DSA 政策页把 **"Ban on dark patterns"** 列为平台义务：禁止以**设计、组织或操作**在线界面的方式**欺骗或操纵**用户、或**实质扭曲/损害其自由且知情的决策**。

> **取源限制**：EUR-Lex 官方全文（CELEX 32022R2065 的 HTML/PDF 多种入口）在本轮多次返回 `202 Accepted` 且**响应体为 0 字节**，**未取得 Article 25(1) 官方逐字文本**。因此本资产**不给出该条的逐字引用**，只记录 EC 官方概述的可核验结论，并把可逐字引用的 DSA 25(2) 法域分工口径归给 EDPB 指南脚注（§3）。落地引用请以 EUR-Lex 官方全文为准。

### 13.2 FTC 2022 报告的四类 tactics

来源：FTC 官方 press release（2022-09）*FTC Report Shows Rise in Sophisticated Dark Patterns Designed to Trick and Trap Consumers*，对应 staff report *Bringing Dark Patterns to Light*（**September 2022**）。报告点名四类：

1. **误导与伪装广告**（deceptive ads / disguised advertising）——广告伪装成内容或其他品牌；
2. **难以取消订阅**（subscription traps / 难取消）——服务费难停、取消流程被阻挠；
3. **埋关键条款与 junk fees**——关键限制藏在细则、结算时冒出附加费；
4. **诱导共享数据**——用界面诱导用户交出更多个人信息。

> **取源限制**：FTC staff report 官方 PDF 多次返回 403/404，`WebFetch` 亦不支持该 PDF 资源。上述四类来自 **FTC 官方新闻稿**（一手），**不是报告正文逐字**；不要在交付物里把它们标成「报告原文定义」。

### 13.3 判法域的决策顺序（写进评审模板）

```
1. 用户在哪 → 中国 / 加州 / 欧盟 / 美国联邦
2. 界面在做什么 → 收集同意 / 收费与续费 / 广告展示 / 面向未成年人 / 信息流机制
3. 命中哪条 → 
   中国：PIPL 14·15·16·17·24 ｜ 广告办法 10 ｜ 网络交易办法 13·16·17·18 ｜ 未成年人条例 42–45·47
   加州：CCPA Regs §7003·§7004
   欧盟：GDPR（EDPB 03/2022）→ UCPD → DSA 25（注意 25(2) 分工）
   美国：FTC 四类 tactics（Section 5 语境）
4. 判「现象 / 机制 / 法条」三层 → §2 现象 → §3 机制 → 对应条款红线
5. 出 PASS/FAIL 用例（§20 自检 + §21 脚本），签字人 = 设计 + 法务（EDPB 明确要求跨学科）
```

---

## 14. 包容性设计地基：不是「无障碍的补充」，是另一种起点

Microsoft Inclusive Design 的三条原则（官方表述）：

1. **Recognize exclusion** —— 承认排斥：设计的起点是「谁被排除在外」，不是「平均用户」。
2. **Solve for one, extend to many** —— 为一个人解，扩展到许多人：为永久性障碍设计的方案，往往同样帮助临时/情境性障碍者。
3. **Learn from diversity** —— 从多样性中学习：把当事人放进研究与设计过程。

**Persona Spectrum**（永久 / 临时 / 情境）：

| | 永久性 | 临时性 | 情境性 |
|---|---|---|---|
| 触觉 | 单手 / 肢体差异 | 手臂骨折 | 抱着孩子、提着东西 |
| 视觉 | 低视力 / 色觉差异 | 白内障术后、散瞳 | 强光下、屏幕反光 |
| 听觉 | 听障 | 耳部感染 | 嘈杂地铁、没戴耳机 |
| 言语 / 认知 | 口吃、阅读障碍、认知障碍 | 发烧、药物影响 | 赶时间、被打断、压力大 |

> **本文件的关键交叉点**：**情境性认知负荷正是 dark pattern 的作用面**。一个在赶时间、被打断、压力大的用户，就是 §3 `Overloading` / `Stirring` 最有效的目标。所以「包容性」与「反欺骗」不是两个议题——**操纵界面优先伤害的，恰恰是认知资源最紧张的人**。

---

## 15. Inclusive Design Principles 七原则（逐条 + 设计动作）

来源：`https://inclusivedesignprinciples.info/`，贡献者为 **Henny Swan、Ian Pouncey、Heydon Pickering、Léonie Watson**。页面立场原文：*"designing for the needs of people with permanent, temporary, situational, or changing disabilities — all of us really."*

| # | 原则（原文） | 设计动作 | 与反欺骗的接口 |
|---|---|---|---|
| 1 | **Provide comparable experience** | 界面须让所有人以适合自己的方式完成任务，且不损害内容质量 | 拒绝路径与接受路径**体验可比**（§4 对称） |
| 2 | **Consider situation** | 为不同情境（噪音、光线、赶时间、单手）提供同等可用性 | 不利用情境压力促成同意 |
| 3 | **Be consistent** | 结构、命名、顺序、行为跨页一致 | 正对 EDPB `Fickle: Inconsistent Interface / Language Discontinuity` |
| 4 | **Give control** | 用户能控制时长、动效、自动播放、通知 | 正对 §12 成瘾机制与 `addictive-design` |
| 5 | **Offer choice** | 提供多种完成方式与多种交互通道 | 与 §7004 的「真实可拒绝选项」同义 |
| 6 | **Prioritise content** | 核心内容与任务优先于装饰与外围功能 | 反 `visual-interference` / `disguised-ads` |
| 7 | **Add value** | 每项功能须对人有明确价值 | 反 `forced-action` / 无关附加义务 |

> **注意 `comparable` 不是 `identical`**：第 1 条要求的是**任务完成质量相当**，不是像素级同样。允许为不同通道提供不同构型，但**不能让某条通道明显更慢或更难**——这与 §4.1(2) 的 symmetry 是同一个词的分寸。

---

## 16. W3C COGA 八个目标：认知无障碍的可验收问句

来源：W3C《Making Content Usable for People with Cognitive and Learning Disabilities》（`w3.org/TR/coga-usable/`），章节 3.1–3.8，八个 Objective 标题逐字如下：

| 章节 | Objective（原文标题） | 可验收的测试问句（文档为每章提供 user testing 问题） |
|---|---|---|
| 3.1 | **Objective 1: Help Users Understand What Things are and How to Use Them** | 用户能否说出这个控件是什么、怎么用？ |
| 3.2 | **Objective 2: Help Users Find What They Need** | 用户能否找到目标入口（尤其是「拒绝/取消/设置」）？ |
| 3.3 | **Objective 3: Use Clear and Understandable Content** | 内容是否清楚易懂（无双重否定、无术语）？ |
| 3.4 | **Objective 4: Help Users Avoid Mistakes and Know How to Correct Them** | 误操作能否被发现并纠正（撤销、回退）？ |
| 3.5 | **Objective 5: Help Users Focus** | 是否减少干扰、避免无关弹窗与动画？ |
| 3.6 | **Objective 6: Ensure Processes Do Not Rely on Memory** | 多步流程是否不要求记住前页信息？ |
| 3.7 | **Objective 7: Provide Help and Support** | 卡住时是否有就地帮助而非跳转长文档？ |
| 3.8 | **Objective 8: Support Adaptation and Personalization** | 是否支持字号、密度、动效、通道的个性化？ |

**文档关于测试的三条原文级口径**：

- 独立小节 **`Test with real users`**：*"Involve people with cognitive and learning disabilities in the research, design, and development process. They're the experts in what works for them."* 列举三类参与形式：`focus groups`、`usability tests`、`the design and research team`。
- **`Testing Each Pattern`**：每个设计模式的 `use` / `avoid` 示例**可作为可测试用例**——「For each pattern, a 'use' example is implemented」「the items identified as 'avoid' examples are avoided」。
- **Section 5** 明确：小团队也应找到可负担的方式让用户参与；并给出逐 objective 的测试问题。

> **工程含义**：COGA 把「测试」写成了**可测试陈述**（testable statements），而不是主观感受。所以 §21 的脚本与 §20 的自检，本质上就是 COGA 思路在伦理议题上的复用：**每条原则都要能落到一条能判通过/不通过的用例**。

---

## 17. 合规达 ≠ 包容：两套判据的正交关系

| 组合 | 例子 | 结论 |
|---|---|---|
| ✅ WCAG AA + ✅ 无操纵 | 对称同意弹窗、可键盘操作、对比度达标、拒绝一步完成 | 目标状态 |
| ✅ WCAG AA + ❌ 操纵 | 拒绝按钮对比度 7:1、可聚焦、有 aria-label，但被放在第三层设置里 | **仍违规**：§4 对称、PIPL 15 便捷撤回 |
| ❌ WCAG AA + ✅ 无操纵 | 两个按钮都在首屏同级，但字号过小、对比度不足 | **仍违规**：§5 §7003 引用 WCAG 2.1 |
| ❌ 两者皆失 | 低对比度 + 羞辱式拒绝文案 + 预勾选 | 上线阻断 |

> **给评审的一句话**：「无障碍审查看**能不能用**，伦理审查看**是不是被引导着用**」。两张检查表都要签，不能互相顶替。

---

## 18. 决策矩阵：什么场景套哪套

| 场景 | 主判据 | 辅判据 | 一票否决项 |
|---|---|---|---|
| 首次进入的 cookie / 追踪同意 | CPPA §7004 对称 + EDPB mirroring | PIPL 14/15/16 | `Accept All` 无同级 `Decline All`；cookie wall；预勾选 |
| 隐私政策与入口 | CPPA §7003 / §7011 | PIPL 17 | 入口低对比、只给图标、小屏不可读、不可打印 |
| 开通/取消订阅 | 《网络交易办法》18（**2025 修正**） | FTC 难取消 / `hard-to-cancel` | 取消需联系客服；服务期内无随时取消入口 |
| 自动续费提醒 | 同上：接受前 + 每次日期前 | — | 沿用旧「前五日」当现行法；只在扣费后才告知 |
| 权限 / 敏感信息 | 《网络交易办法》13 + PIPL 14 | §7004(a)(4)(B) 不捆绑 | 概括授权、默认授权、以停止使用相要挟 |
| 开屏 / 弹窗广告 | 《互联网广告办法》10 | `disguised-ads` | 需两次点击才能关、计时才能关、同页复弹 |
| 营销推送 / 通知 | 《网络交易办法》16 | `nagging` | 拒绝后换名义再发；退订收费 |
| 搭售 / 附加选项 | 《网络交易办法》17 | `sneaking` / `preselection` | 默认勾选；把历史选择设为后续默认 |
| 未成年人模式 | 未成年人条例 42–45·47 | §12 成瘾机制 | 打榜/应援/控评入口存在；无单次与单日消费双限 |
| 信息流 / 推荐 | PIPL 24 + §12 | COGA Objective 5 | 无「非个性化」选项且无便捷拒绝；无终点、无法关闭 |
| 出海欧盟 | GDPR→UCPD→DSA 25（注意 25(2) 分工） | EDPB 六类 | 一句「违反 DSA」代替法域判定 |
| 出海加州 | CCPA §7003·§7004 | FTC 四类 | 用「意图良好」为已知缺陷辩护（§7004(c)） |

---

## 19. 反模式 20 条：反操纵红线与合规验收判据（每条都能判 FAIL）

1. `Accept All` 配 `More Information` / `Preferences`，把「拒绝」变成一条更长的路。
2. 用 `Ask me later` 代替 `No`，让拒绝在语义上不存在。
3. 在否定句旁放 `Yes` / `No`，制造双重否定。
4. 流程中途反转确认/取消按钮顺序。
5. Toggle 只写 `on/off` 不写状态含义。
6. 拒绝前插挽留屏、问卷或倒计时。
7. 授权类控件使用 `defaultChecked={true}`。
8. 一个总开关捆绑「服务必需」与「数据出售」两类用途。
9. 不同意就拒绝提供产品或服务（cookie wall）。
10. 撤回同意入口藏在三级设置或需要联系客服。
11. 已知坏链/循环链接/无人监控的反馈邮箱却不修。
12. 关闭广告需两次以上点击，或必须等计时结束。
13. 同一页面同一文档内关闭后继续弹出广告。
14. 自动续费照抄 2021 年旧版「前五日」当现行法定数值。
15. 服务期内没有「随时取消或变更」的显著入口。
16. 拒绝营销后换名义再发；退订收费或不生效。
17. 把用户上一次交易的选择设为后续独立交易的默认值。
18. 用羞辱/损失厌恶文案写拒绝按钮或流失挽留。
19. 未成年人模式下保留打榜、应援集资、刷量控评入口。
20. 拿「我们没有恶意」「转化率会掉」作为不修复已知操纵性缺陷的理由（§7004(c)）。

---

## 20. 上线自检 22 项

**同意与隐私**
1. 首屏是否 `同意全部` + `拒绝全部` 同屏同级？`管理偏好` 是否只是第三入口？
2. 按 §4.2 的起止点实测，拒绝路径步数是否 **≤** 接受路径？
3. 是否无双重否定、无 `Ask me later`、按钮顺序全程恒定？
4. 非必需授权项默认值是否全部为**未选中**？
5. 用途是否按项拆分、敏感信息是否**逐项**取得同意？
6. 不同意或撤回后，产品是否仍可使用（必需处理除外）？
7. 撤回入口是否与授权入口**同层级**且端到端真的能完成（坏链/等待/邮箱已测）？
8. 告知四项（处理者 / 目的方式种类期限 / 权利行使方式 / 其他）是否显著、清晰、可查阅可保存？
9. 处理目的、方式、种类变更时，是否会**重新取得同意**？
10. 个性化推送是否提供「不针对个人特征」选项或便捷拒绝？
11. 隐私入口是否与相邻链接**字号/颜色相当**、含「隐私」字样、小屏可读、可打印？

**交易与广告**
12. 开通页是否在确认前同屏展示自动续费事实、周期与金额？
13. 每个自动展期/续费**日期前**是否有显著提醒与留痕？
14. 服务全周期是否有**显著、简便**的随时取消/变更入口，且不收不合理费用？
15. 规范文档里是否**已删除**旧版「前五日」的普适表述（或明确标为企业自定）？
16. 开屏/弹窗广告是否 **1 次点击**可关、无需计时、同页同文档不复弹、关闭标志清晰可辨？
17. 搭售可选项是否无默认勾选、不继承历史选择？
18. 营销信息是否提供显著·简便·免费退订，且拒绝后**立即停止、不换名义**？

**未成年人与成瘾机制**
19. 未成年人模式是否覆盖**时段/时长/功能/内容**四维 + 监护人**时间/权限/消费**三类管理，且醒目便捷？
20. 是否有**单次**与**单日累计**双消费限额并按年龄分档？打榜/应援/控评入口是否已整体下线？适龄提示是否在下载/注册/登录三处显著可见？
21. 信息流是否有明确终点、可关闭开关且状态被记住？是否未用损失厌恶文案驱动回访？

**包容性与流程**
22. COGA 八目标是否各有至少一条**可判 PASS/FAIL** 的用例？焦点小组/可用性测试中是否**包含认知与学习障碍者本人**（不是只由团队代判）？两套检查表（无障碍 / 伦理）是否**分别签字**？

---

## 21. 可抄代码（4 段，3 段 Python 已实跑）

> 三段 Python 均只依赖标准库，直接从本文件复制即可跑。设计意图：把 §4 / §8 / §9 / §10 的条文变成**能进 CI 的断言**，而不是评审会上的口头约定。每段都自带 PASS 与 FAIL 双用例。

### 21.1 同意 UI 对称性检查器（CPPA §7004 / PIPL 15·16 / EDPB mirroring）

```python
# consent_symmetry.py —— 判一份同意弹窗配置是否对称
import re

DOUBLE_NEG_RE = re.compile(r"(不\s*(得|要|能|会|应)?\s*(不|禁止|拒绝|否))|(不必不)|(是否不)", re.U)
SHAME_RE = re.compile(r"(不.{0,6}(愿意|想|舍得|聪明))|(算了)|(继续被)|(甘心)", re.U)

def check_consent(cfg: dict) -> list[tuple[str, bool, str]]:
    """返回 [(检查项, 是否通过, 依据)]。任一 False 即不得上线。"""
    out = []
    def put(name, ok, why):
        out.append((name, bool(ok), why))

    buttons = [b.strip() for b in cfg.get("buttons", [])]
    labels = [b.lower() for b in buttons]
    has_accept = any(("accept" in x or "同意" in x) for x in labels)
    has_decline = any(("decline" in x or "拒绝" in x or x == "no") for x in labels)
    put("同级拒绝按钮存在", has_accept and has_decline,
        "§7004(a)(2)(C)：Accept All 必须与 Decline All 同屏")
    put("未用 More Information / Preferences 替代拒绝",
        not any(("more information" in x or "preferences" in x or "了解更多" in x
                 or "管理偏好" in x) for x in labels) or has_decline,
        "§7004(a)(2)(C)：这类入口会拉长拒绝路径")
    put("未用 Ask me later 代替 No",
        not any("ask me later" in x or "稍后再说" in x for x in labels) or has_decline,
        "§7004(a)(2)(B)：必须有真实拒绝选项")

    put("拒绝路径步数 <= 接受路径步数",
        cfg.get("reject_steps", 99) <= cfg.get("accept_steps", 0),
        "§7004(a)(2)(A)：从点击入口起算到请求完成")
    put("无挽留/干扰屏", cfg.get("interrupt_screens", 99) == 0,
        "§7004(a)(4)(A)")
    put("按钮顺序全流程恒定", cfg.get("button_order_consistent", False),
        "§7004(a)(3)(C)：中途反转属混淆设计")
    put("端到端真的可完成", cfg.get("e2e_completes", False),
        "§7004(a)(5)：不得有坏链/循环/无限等待")

    copies = cfg.get("copy", [])
    put("无双重否定", not any(DOUBLE_NEG_RE.search(c) for c in copies),
        "§7004(a)(3)(A)")
    put("无羞辱式拒绝文案", not any(SHAME_RE.search(c) for c in copies),
        "confirmshaming / EDPB Stirring")
    put("非必需项默认未选中", not any(cfg.get("defaults", {}).values()),
        "EDPB 预勾选不构成同意 / 网络交易办法 13·17 条")
    put("不同意仍可用服务", cfg.get("service_without_consent", False),
        "PIPL 16 条（cookie wall 红线）")
    put("撤回入口与授予入口同层级",
        cfg.get("withdraw_depth", 99) <= cfg.get("grant_depth", 0),
        "PIPL 15 便捷撤回 / EDPB mirroring effect")
    put("用途按项拆分、未捆绑不兼容用途",
        cfg.get("purpose_switches_count", 0) >= 2 and not cfg.get("bundles_incompatible", True),
        "§7004(a)(4)(B) / PIPL 14 条")
    put("视觉权重同级",
        cfg.get("reject_weight", 0) >= cfg.get("accept_weight", 1),
        "visual-interference / §7003 conspicuous link")
    return out

if __name__ == "__main__":
    good = dict(buttons=["Accept All", "Decline All", "Preferences"],
                accept_steps=1, reject_steps=1, interrupt_screens=0,
                button_order_consistent=True, e2e_completes=True,
                copy=["选择是否允许个性化广告", "已关闭个性化广告"],
                defaults={"marketing": False, "analytics": False},
                service_without_consent=True, withdraw_depth=1, grant_depth=1,
                purpose_switches_count=3, bundles_incompatible=False,
                accept_weight=1, reject_weight=1)
    bad = dict(good, buttons=["Accept All", "More Information"],
               reject_steps=3, interrupt_screens=2,
               button_order_consistent=False, e2e_completes=False,
               copy=["您是否不禁止不出售个人信息？", "算了，我继续被追踪"],
               defaults={"marketing": True}, service_without_consent=False,
               withdraw_depth=4, bundles_incompatible=True, reject_weight=0)
    for tag, cfg in (("good", good), ("bad", bad)):
        r = check_consent(cfg)
        fails = [n for n, ok, _ in r if not ok]
        print(tag, "PASS" if not fails else "FAIL", "|", len(r), "checks |",
              len(fails), "violations:", ", ".join(fails[:4]))
```

### 21.2 一键关闭静态扫描（《互联网广告管理办法》第 10 条）

```python
# ad_close_scan.py —— 扫描开屏/弹窗广告组件配置
import re

COUNTDOWN_RE = re.compile(r"(countdown|计时|倒计时|setTimeout\s*\(|delay\s*[:=])", re.I)
REPOP_RE = re.compile(r"(re-?show|again|复弹|再次弹出|repeat\s*[:=]\s*true)", re.I)

def check_ad_close(cfg: dict, source: str = "") -> list[tuple[str, bool, str]]:
    out = []
    def put(n, ok, why): out.append((n, bool(ok), why))

    put("存在关闭标志", cfg.get("has_close_affordance", False), "第 10 条：显著标明关闭标志")
    put("关闭标志可清晰辨识且易定位",
        cfg.get("close_label_clear", False) and cfg.get("close_position_stable", False),
        "第 10 条第 2 项：虚假/不可辨识/难以定位均禁止")
    put("关闭点击次数 <= 1", cfg.get("close_clicks", 99) <= 1,
        "第 10 条第 3 项：须经两次以上点击即违规")
    put("无需等待计时结束",
        not bool(COUNTDOWN_RE.search(source)) and not cfg.get("timer_gated", False),
        "第 10 条第 1 项：计时结束才能关闭即违规")
    put("同页面同文档内关闭后不复弹",
        not bool(REPOP_RE.search(source)) and not cfg.get("repeats_in_same_page", False),
        "第 10 条第 4 项")
    put("广告可辨识（非伪装成正文/系统按钮）",
        cfg.get("ad_labeled", False), "disguised-ads / 第 10 条广告可识别要求")
    return out

if __name__ == "__main__":
    good = dict(has_close_affordance=True, close_label_clear=True,
                close_position_stable=True, close_clicks=1, timer_gated=False,
                repeats_in_same_page=False, ad_labeled=True)
    bad = dict(good, close_label_clear=False, close_clicks=2,
               timer_gated=True, repeats_in_same_page=True, ad_labeled=False)
    src_bad = "setTimeout(() => showAdAgain(), 5000); // 复弹"
    for tag, cfg, src in (("good", good, ""), ("bad", bad, src_bad)):
        r = check_ad_close(cfg, src)
        fails = [n for n, ok, _ in r if not ok]
        print(tag, "PASS" if not fails else "FAIL", "|", len(r), "checks |",
              len(fails), "violations:", ", ".join(fails[:4]))
```

### 21.3 自动续费 UI 检查器 + **陈旧法条守卫**（《网络交易办法》18 条 2025 修正）

```python
# subscription_ui_check.py —— 含「前五日」过期口径拦截
import re

STALE_RULE_RE = re.compile(r"(自动续费|自动展期|第\s*18\s*条|第十八条)"
                           r"[^。；\n]{0,40}(前\s*五\s*日|提前\s*5\s*日|5\s*天前)", re.U)

def check_subscription(cfg: dict, spec_text: str = "") -> list[tuple[str, bool, str]]:
    out = []
    def put(n, ok, why): out.append((n, bool(ok), why))

    put("接受服务前同屏显著告知（事实/周期/金额）",
        all(cfg.get(k, False) for k in ("disclose_before_purchase", "show_period", "show_amount")),
        "第十八条第一款：接受服务前显著提请注意、由消费者自主选择")
    put("每个自动展期/续费日期前都有显著提醒",
        cfg.get("remind_before_each_renewal", False),
        "第十八条第一款：等日期前（注意是「等日期」，不是单一提前量）")
    put("服务期内有显著·简便的随时取消/变更入口",
        cfg.get("cancel_anytime", False) and
        cfg.get("cancel_depth", 99) <= cfg.get("subscribe_depth", 0),
        "第十八条第二款 + §4 对称选择 / hard-to-cancel")
    put("取消/变更不收不合理费用", not cfg.get("cancel_fee", True),
        "第十八条第二款")
    put("未默认勾选开通", not cfg.get("preselected", True),
        "第十七条 / 第十三条 / EDPB 预勾选不构成同意")
    put("规范文档未把「前五日」当现行法定数值",
        not bool(STALE_RULE_RE.search(spec_text)),
        "2025-03-18 总局令第 101 号修正，2025-05-01 施行；现行条文为「等日期前」")
    return out

if __name__ == "__main__":
    good = dict(disclose_before_purchase=True, show_period=True, show_amount=True,
                remind_before_each_renewal=True, cancel_anytime=True,
                cancel_depth=1, subscribe_depth=1, cancel_fee=False, preselected=False)
    bad = dict(good, remind_before_each_renewal=False, cancel_anytime=False,
               cancel_depth=4, cancel_fee=True, preselected=True)
    doc_good = "自动续费须在接受服务前及每次续费日期前显著提醒；企业自定 T-5 作为内部风控。"
    doc_bad = "依据第十八条，自动续费应当在日期前五日以显著方式提醒消费者。"
    for tag, cfg, doc in (("good", good, doc_good), ("bad", bad, doc_bad)):
        r = check_subscription(cfg, doc)
        fails = [n for n, ok, _ in r if not ok]
        print(tag, "PASS" if not fails else "FAIL", "|", len(r), "checks |",
              len(fails), "violations:", ", ".join(fails[:4]))
```

### 21.4 包容性 / COGA 验收清单（YAML，进 CI 或 PR 模板）

```yaml
# inclusive-acceptance.yml —— 每个 objective 至少一条可判 PASS/FAIL 的用例
meta:
  spec: "W3C COGA 8 objectives + Inclusive Design Principles 7 原则"
  rule: "无障碍表与伦理表分别签字，不得互相顶替"
  real_users_required: true   # Test with real users：须包含认知与学习障碍者本人
objectives:
  - id: 3.1
    name: "Help Users Understand What Things are and How to Use Them"
    test: "5 名用户能正确说出拒绝按钮的作用，≥4 人通过"
  - id: 3.2
    name: "Help Users Find What They Need"
    test: "在无提示下 10 秒内找到「取消订阅」与「撤回同意」，成功率 ≥80%"
  - id: 3.3
    name: "Use Clear and Understandable Content"
    test: "静态扫描双重否定/羞辱文案命中数 = 0"
  - id: 3.4
    name: "Help Users Avoid Mistakes and Know How to Correct Them"
    test: "误点同意后可在同页撤销，且状态可回读"
  - id: 3.5
    name: "Help Users Focus"
    test: "任务期间无无关弹窗；prefers-reduced-motion 生效"
  - id: 3.6
    name: "Ensure Processes Do Not Rely on Memory"
    test: "三步流程任一页均回显已选项，无需返回上一页查看"
  - id: 3.7
    name: "Provide Help and Support"
    test: "卡住时有就地帮助，不跳转到长政策文档"
  - id: 3.8
    name: "Support Adaptation and Personalization"
    test: "字号/密度/动效/通知四类均可关闭或调节且状态持久化"
gates:
  - "§21.1 consent_symmetry 全部 PASS"
  - "§21.2 ad_close_scan 全部 PASS（含开屏广告）"
  - "§21.3 subscription_ui_check 全部 PASS（含陈旧法条守卫）"
  - "§20 上线自检 22 项逐项签字"
```

> **实跑结果（2026-11-06，本机 Python 标准库）**：`consent_symmetry` → good `PASS 14 checks / 0 violations`、bad `FAIL 14 checks / 13 violations`；`ad_close_scan` → good `PASS 6/0`、bad `FAIL 6/5 violations`；`subscription_ui_check` → good `PASS 6/0`、bad `FAIL 6/5 violations`，其中**陈旧法条守卫成功拦截**「日期前五日」的过期表述。三段均通过 PASS/FAIL 双用例验证，不是伪代码。

---

## 22. 数据来源与取源纪律

**一手法规 / 官方原文**

- EDPB《Guidelines 03/2022 on deceptive design patterns in social media platform interfaces》**v2.0（2023-02-14）** 官方 PDF（74 页，六类机制 / Annex II best practices / DSA 25(2) 脚注）：`https://www.edpb.europa.eu/system/files/documents/2023-02/edpb_03-2022_guidelines_on_deceptive_design_patterns_in_social_media_platform_interfaces_v2_en_0.pdf`
- EDPB 文档页：`https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-032022-deceptive-design-patterns-social-media_en`
- CPPA《CCPA Regulations》最终文本 PDF（66 页，**§7003 / §7004 / §7011**）：`https://cppa.ca.gov/regulations/pdf/20230329_final_regs_text.pdf`
- CPPA 法规页：`https://cppa.ca.gov/regulations/consumer_privacy_act.html`
- 全国人大《中华人民共和国个人信息保护法》全文（**第 14/15/16/17/24 条**）：`http://www.npc.gov.cn/npc/c2/c30834/202108/t20210820_313088.html`
- 中国政府网《未成年人网络保护条例》（**国务院令第 766 号**，第 42–45、47 条）：`https://www.gov.cn/zhengce/content/202310/content_6911288.htm`
- 湖南省人民政府门户网站《网络交易监督管理办法》全文（**2025-03-18 总局令第 101 号修正版**，第 13/16/17/18/41 条）：`http://www.hunan.gov.cn/zqt/zcsd/202508/t20250804_33757595.html`
- 央广网《市场监管总局修订规章强化涉企检查有关要求，5 月 1 日起实施》（第 101 号令修改第十八条逐字条文、施行日期）：`https://www.cnr.cn/jingji/ycbd/20250331/t20250331_527118971.shtml`
- 央广网《互联网广告管理办法》第 10 条「一键关闭」五类禁止情形与施行日期解读（2023-05-01）：本轮经该站报道逐字核验。
- FTC 官方 press release（2022-09，四类 dark pattern tactics）：`https://www.ftc.gov/news-events/news/press-releases/2022/09/ftc-report-shows-rise-sophisticated-dark-patterns-designed-trick-trap-consumers`
- FTC report 页（September 2022）：`https://www.ftc.gov/reports/bringing-dark-patterns-light`
- European Commission DSA 政策页（**Ban on dark patterns**）：`https://digital-strategy.ec.europa.eu/en/policies/digital-services-act-package`
- HHS Surgeon General advisory landing page（仅方向性参考）：`https://www.hhs.gov/surgeongeneral/priorities/youth-mental-health-social-media/index.html`

**标准 / 设计准则**

- `deceptive.design` 现行 18 类 types 页（本轮抓取，slug 18 条）：`https://www.deceptive.design/types`
- W3C《Making Content Usable for People with Cognitive and Learning Disabilities》（**3.1–3.8 八目标 / Test with real users / Testing Each Pattern**）：`https://www.w3.org/TR/coga-usable/`
- Inclusive Design Principles 七原则（Henny Swan / Ian Pouncey / Heydon Pickering / Léonie Watson）：`https://inclusivedesignprinciples.info/`
- Microsoft Inclusive Design（三原则 / Persona Spectrum / Solve for one, extend to many）：`https://www.microsoft.com/design/inclusive/`

**GitHub REST API 实测（2026-11-06，逐条 `GET /repos/{owner}/{repo}`）**

| 仓库 | stars | license | pushed_at | archived | 用途 |
|---|---|---|---|---|---|
| `aruneshmathur/dark-patterns` | 141 | GPL-3.0 | 2019-08-06 | false | Princeton CSCW 2019《Dark Patterns at Scale: Findings from a Crawl of 11K Shopping Websites》代码与数据；**学术存档，非活源** |
| `Heydon/inclusive-design-checklist` | 2759 | — | 2020-06-11 | false | 包容性设计 checklist，star 最高但已停更 6 年 |
| `w3c/coga` | 83 | NOASSERTION | 2026-01-19 | false | COGA Task Force 交付物，**活跃**；许可需人工复核 |
| `guardian/consent-management-platform` | 30 | Apache-2.0 | 2026-11-01 | false | 真实生产 CMP 实现，可作同意 UI 参考，**极活跃** |
| `68publishers/consent-management-platform` | 65 | NOASSERTION | 2026-11-05 | false | cookie widget；许可 NOASSERTION 红灯 |
| `ericwbailey/empathy-prompts` | 197 | MIT | 2021-07-18 | false | 包容性设计同理心提示词集 |
| `swisspost/design-system` | 181 | Apache-2.0 | 2026-11-06 | false | 明确以 inclusive UX 为目标的设计系统，**当日活跃** |
| `Owl-Listener/inclusive-design-skills` | 108 | MIT | 2026-06-09 | false | 面向 AI coding agent 的包容性设计技能包 |
| `yamanalab/why-darkpattern` | 5 | Apache-2.0 | 2024-01-10 | false | IEEE BigData 2023 暗黑模式可解释自动检测 |
| `Owl-Listener/designpowers` | 256 | MIT | 2026-06-23 | false | 多 agent 包容性设计流程 |

> **选型立场**：本主题**不存在「装一个库就合规」的方案**。CMP 只能解决「记录同意」，解决不了「路径是否对称」。`guardian/consent-management-platform`（Apache-2.0 / 活跃）适合读实现，`w3c/coga` 适合读标准；`NOASSERTION` 两项不作生产依赖；`aruneshmathur/dark-patterns` 是 2019 年学术存档，**不可当活源**（沿用 `ai-design-toolchain.md` §13 选型三问：许可 / pushed_at / 可验收）。

**取源纪律 —— 未取得原文的一律不写入**

| 线索 | 本轮状态 | 处理 |
|---|---|---|
| EUR-Lex DSA 官方全文（CELEX 32022R2065） | 多种 HTML/PDF 入口返回 `202` 且响应体 0 字节 | **不引用 Article 25(1) 逐字**；只记录 EC 官方概述 + EDPB 脚注的 25(2) 分工 |
| FTC staff report PDF | 403 / 404，`WebFetch` 不支持 PDF 资源 | 四类 tactics 归给**官方新闻稿**，不标为报告原文 |
| HHS advisory PDF | 403，返回 473/490 字节 HTML 错误页（pypdf 报 invalid pdf header） | **不引用逐字结论、不臆造统计数字**；只用 landing page 方向 |
| OECD《Dark Commercial Patterns》 | 页面 4xx，直链 PDF 404 | 定义 / prevalence / 政策建议**全部不写入** |
| ICO Children's Code Standard 12 `nudge techniques` | 旧 URL 404 | 精确条文**不写入** |
| 市场监管总局《互联网广告管理办法》官方原文页 | 猜测 URL 404 | 第 10 条据央广网逐字引用核验，**不臆造令号** |
| CAC《必要个人信息范围规定》 | URL 404 | 不采用 |
| `deceptive-design/deceptive.design`、`microsoft/inclusive-design`、`EFForg/https-everywhere` 等 | API 404 / archived | 404 线索剔除；archived 仓库不列活源 |
| Princeton 论文 `11,286 / 1,818 / 15 types` 等精确数字 | 仅见搜索结果，未在 README / 原文复核 | **不写入**；只保留 README 可核验的「11K Shopping Websites」与 arXiv 1907.07032 |

> **本轮最值得保留的方法论**：法规会修订（§9）、分类会更新（§2）、官方页面会 403（§13）。所以知识资产必须**同时记录「写的是什么」和「凭什么这么写」**，并把未取得原文的洞明确列出来——**空白比编造更有价值**。

---

## 23. 本轮让哪类问题不再含糊

1. **「这个同意弹窗合不合规」** → 不再是审美讨论：CPPA §7004 给了**步数起止点**、`Accept All + Decline All` 的**固定构型**、双重否定与按钮顺序反转的**明令禁止**，配上 §21.1 的 **14 条断言**，能判 PASS/FAIL。
2. **「自动续费到底要提前几天提醒」** → **裁决了广泛流传的过期口径**：2021 年旧版「前五日」已被 2025-03-18 总局令第 101 号修正（2025-05-01 施行）的「**等日期前**」取代；现行要求拆成**两个时点 + 服务期内的随时取消/变更 + 不得收不合理费用**，并做了**能拦截旧文案的静态守卫**（§21.3 已实跑）。
3. **「一键关闭算不算做到」** → 变成三个可测数值：点击 **≤1**、**无需计时**、**同页面同文档不复弹**，另有开屏广告同样适用、拒不改正 5000–30000 元罚则（§8 / §21.2）。
4. **「未成年人保护是不是加个弹窗」** → 变成**另一套产品构型**：第 43 条四维度 + 监护人三类管理、第 44 条**单次与单日累计**双限额、第 45 条三类功能**整体下线**、第 47 条三处适龄提示（§11）。
5. **「暗黑模式有哪些类型」** → 以现行 **18 类**为准并公开点名旧分类已变；同时给出更稳的**机制层**（EDPB 六类）与**法条层**（§4/§7–§11）判据，避免清单过时即失效。
6. **「无障碍过了是不是就包容了」** → 用 §17 四象限明确**两套判据正交**：无障碍审查看「能不能用」，伦理审查看「是不是被引导着用」，COGA 八目标各自落到一条可测用例（§16 / §21.4），且**必须分别签字**。
7. **「我们没恶意」能不能当辩护理由** → 不能。CPPA §7004(c) 原文：意图非决定性，知情不修、刻意不知情同样不利；EDPB 亦把设计师列为跨学科责任主体（§1 / §4.6）。

> **只加链接不算升级。** 本轮给出：18 类现行分类、6 类机制、5 条对称原则、3 处法域的逐条红线、22 项自检、20 条反模式、4 段可抄代码（3 段已实跑、双用例验证），以及 **2 条明确的反陈旧裁决**（旧分类 / 前五日）。

