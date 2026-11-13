# 定价页与结账流程（Pricing & Checkout）

> 覆盖：SaaS 定价页构型、价格数字排版、划线价与折扣合规、月付年付切换、结账流程骨架（单页/多步/review 页）、表单字段与自动填充、支付方式与钱包按钮、费用透明（运费/税费/附加费）、承诺闸门（SC 3.3.4）、总价变化播报、移动端结账、反模式与自检。
> 交叉：`patterns.md §定价表 / §Auth`（速记版，本章是其展开与纠偏）、`form-table.md`（字段与校验）、`accessibility.md`（SC 阈值）、`design-ethics-inclusion.md`（附加费 sneaking）、`feedback-states.md §6`（`role="status"`）、`ux-writing.md`（按钮与错误文案）、`content-findability.md`（分面搜索与筛选归此）。

## §0 一句话立场

**定价页的目标不是把价格说清楚，是让人敢点；结账的目标不是收集信息，是让人敢付完。**

由此三条铁律，任何一条破了都可以直接判为设计缺陷：

1. **总价先行，且不可变**——用户在**同意付款之前**必须看到一个确定的最终金额；此后再出现的任何加项都是缺陷（不是"体验问题"，是合规问题，见 §4 / §10）。
2. **结账是承诺，不是表单**——提交付款属于"不可逆的金融/法律承诺"，必须提供**可复核、可更正、可撤销**三者之一（SC 3.3.4，Level AA，见 §11）。
3. **每一步都能回头，且回头不丢已填**——同一进程内不重复索要同一信息（SC 3.3.7，Level A，见 §8）。

一句话给用户的建议模板：**"先说结论：你把运费/税费藏到最后一步，用户不是嫌贵，是嫌被骗。改成在填地址前就给区间、在付款前锁总额，再补一个 review 页。"**

## §1 判层：你被问的是哪一类

先分流，别一上来就画定价页。六问定位：

| # | 症状（用户原话） | 归哪节 | 交叉资产 |
|---|---|---|---|
| Q1 | "三档怎么排""推荐档怎么突出""要不要企业档" | §2 构型 | `patterns.md §定价表` |
| Q2 | "价格数字多大""货币符号怎么放""¥ 还是 CNY" | §3 排版 | `typography-system.md` |
| Q3 | "划线价怎么标""原价能写吗""折扣百分比会不会违法" | §4 合规 | `design-ethics-inclusion.md` |
| Q4 | "月付年付怎么切""默认选哪个" | §6 切换器 | `form-table.md` |
| Q5 | "结账几步""要不要 review 页""能不能游客下单" | §7 骨架 / §11 闸门 | `navigation-ia.md` |
| Q6 | "地址填两遍""卡号怎么填""支付方式图标怎么摆" | §8 字段 / §9 支付 | `form-table.md`、`accessibility.md` |

**判层口诀**：定价页解决"选哪个"，结账页解决"敢不敢付"。前者是说服问题，后者是信任与合规问题——把两件事混在一个页面里做，通常是两者都没做好。

## §2 定价页构型谱系（先选构型，再调尺寸）

| 构型 | 适用 | 推荐档处理 | 主要风险 |
|---|---|---|---|
| **① 三档并排**（默认首选） | SaaS 自助注册；买家能自己判断需求 | 中档：描边 2px 强调色 + "最受欢迎"角标 | 三档若功能行不对齐，用户读不出"差在哪" |
| **② 两档对照 + 企业横条** | 两个真实买家人群（个人 / 团队）差异明显 | 无"推荐"，靠人群命名区分 | 横条容易变成第二张价目表，信息重复 |
| **③ 单档 + 用量/阶梯计价表** | 价格随用量线性变化（API、存储、席位 > 50） | 无推荐档，改为"费量表 + 估算器" | 估算器不给区间，用户算不出自己的账单 |
| **④ 无定价（纯"联系销售"）** | 客单价极高、必须方案定制 | 不适用 | 页面上不出现任何数字 → 用户直接离开（除非销售线索充足） |

**尺寸与对齐（可直接抄）**：卡片内边距 32px；三档并排时容器宽 ≥ 960px，< 768px 转纵向堆叠且**推荐档置顶**；三张卡的功能行必须**同一行号对齐**（用 grid 行轨道或统一行高，不用各自 margin）；卡片等高，CTA 底对齐。

**为什么推荐档"描边 + 角标"而不是"放大"**：三档并排的价值在**可比较**。放大推荐档会破坏三列等宽的视觉基线，用户读价格时失去同一坐标，反而更难算差价；强调应该走**色与线**（描边、背景色阶、"最受欢迎"标签），不走**尺寸**。放大只在一档独占版面（移动端堆叠首屏）时才成立。

**功能行纪律**：每档 ≤ 12 行，超出就按"核心 / 协作 / 安全 / 支持"分组折叠；行文案统一句式（动词短语开头，如"支持 SSO""导出 CSV"），不用名词堆；"不支持"用灰色 ✕ **且必须带屏幕阅读器文本**（`<span class="sr-only">不支持</span>`），只给图标等于对读屏用户什么都没说（SC 1.1.1）。

## §3 价格数字排版（照数值抄）

价格的排版目标只有一个：**让三个数字能被竖向扫描比较**。所以纵向对齐优先于美观。

| 元素 | 值 | 依据 / 说明 |
|---|---|---|
| 价格数字 | 40–48px（视口 ≥ 1200px）；28–32px（< 768px） | 与 `patterns.md` 一致；行高 1.1；`font-variant-numeric: tabular-nums` |
| 货币符号 | 0.5em，baseline 上移 0.12–0.15em | 缩小**不得低于正文字号的 0.75 倍**，否则读不清（比"好看"重要） |
| 小数位 | 同一页内统一 | ¥ 整数价默认不带 `.00`；跨境/美元价带 `.00`。混用会被读成"不同精度" |
| 周期单位 | 14–16px，与数字同基线 | 写 `/月`、`/年`，不缩写 `p/m`；年付要同时给"折合每月"和"一次性支付"两个数 |
| 折后价 | 与常规价同字号（差异 ≤ 20%） | 不靠字号大小表达"便宜"——那是营销噪音，不是信息 |
| 划线价 | 原价 × 0.875 + 1px `line-through` | 必须有可见标签（"原价"/"were"），否则用户不知道这条线是什么意思 |
| 省额 | "省 ¥240" 与 "-20%" **只给一个口径** | 两个口径都给且不一致 = 用户开始怀疑全部数字 |
| 数字右对齐 | 对比表内所有金额右对齐 | 左对齐时位数不同的数字无法竖向比较 |

`tabular-nums` 是硬要求：对比表里 `¥1,200` 与 `¥980` 若用比例数字（proportional figures），"1"与"9"占宽不同，整列会歪。中文界面里这条同样成立（中文字体通常自带等宽数字，但拉丁回退字体不一定）。

## §4 划线价、折扣与"原价"的合规红线

价格呈现不是纯审美问题——**被比较的价格有法律含义**。三条纪律先给，再给一手依据。

**纪律一：被比较价格必须真实、有依据、可追溯。** "原价/划线价"若从未真实成交、或只短暂挂过一天，就是虚假比较。设计侧的落点：划线价组件必须能绑到一个**历史成交价字段**，而不是设计师手填的数字。

**纪律二：折扣口径与总价口径不能互相打架。** 页面上一处写"立省 20%"，另一处写"¥ 低至 99"，两套口径会让用户算出第三个数字，信任从这一刻开始崩。

**纪律三：任何费用都不得在用户同意付款之后才出现**（详见 §10）。

**一手依据（本次取到全文的，逐字）**

FTC《Rule on Unfair or Deceptive Fees》（16 CFR Part 464，Source 90 FR 2166, Jan. 10, 2025）§464.1 定义 **total price** 为：

> *"the maximum total of all fees or charges a consumer must pay for any good(s) or service(s) and any mandatory ancillary good or service, except that government charges, shipping charges, and fees or charges for any optional ancillary good or service may be excluded."*

§464.2(a) 禁止在**未清楚显著披露总价**的情况下展示任何价格；§464.2(b) 要求总价必须比**任何其他价格信息更显著**：

> *"must disclose the total price more prominently than any other pricing information. However, where the final amount of payment for the transaction is displayed, the final amount of payment must be disclosed more prominently than, or as prominently as, the total price."*

§464.2(c) 要求消费者**同意付款前**披露被排除费用的性质、目的、金额，以及最终支付金额。**适用范围要说清**：该规则只覆盖两类商品/服务——**live-event tickets** 与 **short-term lodging**，不是全品类。所以**不要**把它当"全球电商法条"引用；但它的两条机制（总价定义 / 总价显著性 ≥ 其他价格信息）可以作为设计纪律外推到任何品类，且这正是行业正在对齐的方向。

"清楚显著"（clearly and conspicuous）的定义里有一条对设计最直接：

> *"In any communication using an interactive electronic medium, such as the internet, a mobile application, or software, the disclosure must be unavoidable."*（§464.1(4)）

以及：

> *"A visual disclosure, by its size, contrast, location, the length of time it appears, and other characteristics, must stand out from any accompanying text or other visual elements so that it is easily noticed, read, and understood."*（§464.1(2)）

> *"must not be contradicted or mitigated by, or inconsistent with, anything else in the communication."*（§464.1(7)）

**这三条直接翻译成 UI 验收**：总价必须在折叠之上、不靠 hover 才出现、不被"限时优惠"横幅挤压、不与任何其他文案矛盾（包括脚注、tooltip、"起"字）。

**欧盟：《Omnibus 指令》(EU) 2019/2161 第 2 条第 (1) 项**修改《价格标示指令》98/6/EC，插入第 6a 条（OJ L 328, 18.12.2019, p. 7；EUR-Lex CELEX 32019L2161）：

> *"Article 6a"*
>
> *"1. Any announcement of a price reduction shall indicate the prior price applied by the trader for a determined period of time prior to the application of the price reduction."*
>
> *"2. The prior price means the lowest price applied by the trader during a period of time not shorter than 30 days prior to the application of the price reduction."*
>
> *"3. Member States may provide for different rules for goods which are liable to deteriorate or expire rapidly."*
>
> *"4. Where the product has been on the market for less than 30 days, Member States may also provide for a shorter period of time than the period specified in paragraph 2."*
>
> *"5. Member States may provide that, when the price reduction is progressively increased, the prior price is the price without the price reduction before the first application of the price reduction."*

**设计落点**：划线价必须绑到「应用本次折扣前、不少于 30 天内该商品的最低成交价」，而不是"我们上周标过的那个价"。阶梯式加码促销（折扣逐步加大）时，基准取**第一次加码前**的价格；上市不足 30 天的商品，成员国可另行规定更短期间。这三条直接决定划线价组件的取值来源：**取交易流水的最低价，不取标价历史**。

**中国：《明码标价和禁止价格欺诈规定》（市场监管总局令第 56 号，2022-07-01 施行）**——来源为 gov.cn 国务院公报 2022 年第 19 号与市场监管总局官方页面（两处文本互校一致）：

- **第十六条**：被比较价格必须真实准确；未标明被比较价格详细信息的，以**同一经营场所价格比较前七日内的最低成交价格**作为被比较价格；以厂商建议零售价作被比较价格的，须标明其为厂商建议零售价。
- **第十七条**：禁止在折价、减价前**临时显著提高**标示价格；禁止以无依据或无从比较的价格作为被比较价格。
- **第十九条**：列举八项价格欺诈行为，与定价页直接相关的两项是 (二)"以低价诱骗……以高价进行结算"、(三)"通过虚假折价、减价或者价格比较等方式销售商品或者提供服务"。
- **第二十一条**：给出三类不属于价格欺诈的除外情形（具体情形以官方公报原文为准，本文件不转述细节）。

> **术语纪律**：该规章**不使用"原价"这个术语**，用的是"被比较价格"与"折价、减价的计算基准"。作品里写"虚构原价"等于引用已废止的旧《禁止价格欺诈行为的规定》表述——**现行法规下应写"虚假的被比较价格"或"折价前临时抬价"**。

**自动续费：《消费者权益保护法实施条例》（国务院令第 778 号，2024-07-01 施行）第十条第二款**：

> *"经营者采取自动展期、自动续费等方式提供服务的，应当在消费者接受服务前和自动展期、自动续费等日期前，以显著方式提请消费者注意。"*

**设计落点**：两个时点都要提示——**开通前**与**每次扣款前**；只在开通时勾一次、扣款日静默扣费，不满足"在……日期前，以显著方式提请"。违反第十条至第十四条的处罚见该条例第五十条第一款。

**取源方式（可复核）**：EUR-Lex 对脚本客户端返回 HTTP 202 + WAF JS 挑战（空正文），上述欧盟条文经**本机 headless Chrome 渲染同一 CELEX 文档**取回 OJ HTML 后逐字抄录；中国条文经政府网国务院公报与市场监管总局两处官方页面互校。复核遇拦截请用浏览器访问（见 §18 第 4 条）。本文件**只逐字引用已核对的句子**，其余以条号 + 要点转述。

## §5 对比表与 CTA

- **推荐档的语义不能只靠颜色**：角标文字（"最受欢迎"/"推荐"）+ `aria-label`；只给强调色 = 对色觉障碍用户与读屏用户同时失效（SC 1.4.1 Use of Color）。
- **CTA 写动作 + 对象**："开始 14 天免费试用"＞"立即开始"＞"了解更多"。"了解更多"做主 CTA 等于承认这一档没想清楚。
- **免费档放最左、企业档放最右**：读序从"最便宜/最简"到"最贵/最定制"，与用户的自我定位方向一致。
- **企业档不标价**时，价格位写"定制"或"按需报价"，**不要**写 "—"（会被读成"免费"或"未定价"）。
- **下单前的价格变更**：涨价公告要给老用户保护窗口（提前告知 + 生效日 + 锁定条件），三件缺一，用户就会把它读成"偷偷涨价"。

## §6 月付 / 年付切换器

- **控件选型**：两个选项互斥且**两个标签必须同时可见** → 用 **radio group**（`<input type="radio">` + `<label>` 并排），**不要**用 switch。switch 的语义是"开/关一个状态"，用户看不出"关"等于月付还是年付。
- **默认值**：默认年付是合法的，但必须同时显示两个数——「按年 ¥1,188（折合 ¥99/月）」与「按月 ¥129/月」。只显示折合月价 = 隐藏一次性支出，属于 §4 纪律二的违反。
- **切换行为**：就地更新、不跳转、不重置已选档位；在 `role="status"` 里播报"已切换为按年付费，总额 ¥1,188"（见 §12）。
- **可分享状态**：`?billing=annual` 写进 URL；否则用户把链接发给同事，对方看到的是另一个价格。
- **折扣展示**：折扣率必须能从两个价格算回来（`1 - 1188/(129×12) ≈ 23.3%`）。写"省 30%"却算不出来，是 §4 纪律二的典型违反。

## §7 结账骨架：单页 / 分段 / 多步

| 型 | 判据 | 结构 | 何时不要用 |
|---|---|---|---|
| **单页** | 字段 ≤ 8，无地址拆分，单一收货方式 | 一个表单 + 内联错误 + 底部总额 | 字段一多就变成"滚动到底找按钮" |
| **分段单页**（推荐默认） | 字段 9–20，需要地址/配送选择 | 同页分区（联系 → 配送 → 支付），锚点式进度 | 分区超过 4 段，用户会迷路 |
| **多步** | 需要账号决策、多地址、发票/税号、预订类 | 每步一屏 + 步骤指示（≤ 3 步） | 步骤 ≥ 4 且每步只有 1–2 个字段，弃单率上升 |

**步骤数 ≤ 3** 是经验上限：信息、支付、（确认）。步骤指示器要如实——不要显示 4 步却在第 2 步收完所有信息。

**必须有一个"复核页"（check answers）**，这是 §11 承诺闸门的载体。照 GOV.UK Design System 的规范做：

- **位置**：小而中的交易放在确认屏**之前**一页；大交易可在每个 section 末尾各放一个。
- **布局**：多数服务用 **two-thirds 布局**——不是为了好看，是**避免行长过长**，并让 Change 链接离内容更近（屏幕放大器用户放大后仍能同时看到值与 Change）。
- **页面标题说明要做什么**，并明确 **"交易在用户确认信息正确之前不算完成"**（GOV.UK 原文要求 *"make it clear the transaction will not be complete until a user confirms their information is correct"*）。
- **每个 section 一个 `Change` 链接**，并带视觉隐藏文本说明改什么（`<span class="govuk-visually-hidden">收货地址</span>`），否则读屏用户听到的是 5 个一模一样的"Change"。
- **返回即预填**：*"The answers pages should look the same way they did when the user last used them."*；改完 Continue 直接回复核页，中间不再追问无关问题。
- **未答的可选项显示 "Not provided"**，不要留空（留空读屏用户无法区分"没填"和"没读到"）。
- **提交按钮写动作**："支付 ¥1,188" / "提交订单"，不写"继续"。
- 参考实现：`dl` + `dt`/`dd` 三列（key / value / actions），`h1` 用大标题样式。

GOV.UK 给的两条收益值得抄进 brief：复核页 *"increase users' confidence as they can clearly see that they have completed all the sections and that their data has been captured"*，并且 *"reduce error rates as users are given a second chance to notice and correct errors before submitting data"*。

**游客结账**：默认允许。强制注册是弃单的头号自造原因，且与 SC 3.3.7 的精神相抵（同一进程内不该重复索要信息）。账号可以在**付款成功后**再邀请创建。

## §8 表单字段与自动填充

### 8.1 字段计划表（结账最小集）

| 字段 | `autocomplete` token | `type` / `inputmode` | 校验时机 |
|---|---|---|---|
| 邮箱 | `email` | `type=email` + `inputmode=email` | blur |
| 收件人姓名 | `shipping name`（或 `name`） | `type=text` | blur |
| 地址行 1 | `shipping address-line1` | `type=text` | blur |
| 地址行 2 | `shipping address-line2` | `type=text` | 不校验（可选） |
| 城市 | `shipping address-level2` | `type=text` | blur |
| 省/州 | `shipping address-level1` | `select` 或 `text` | change |
| 邮编 | `shipping postal-code` | `type=text` + `inputmode=numeric` | blur |
| 国家 | `shipping country` | `select` | change |
| 电话 | `tel` | `type=tel` + `inputmode=tel` | blur（按国家放宽） |
| 卡号 | `cc-number` | `type=text` + `inputmode=numeric` | 分组后 Luhn |
| 有效期 | `cc-exp` | `type=text` + `inputmode=numeric` | MM/YY 补斜杠 |
| 安全码 | `cc-csc` | `type=text` + `inputmode=numeric` | blur |
| 持卡人 | `cc-name` | `type=text` | blur |

### 8.2 SC 1.3.5 Identify Input Purpose（Level AA）

要求"每个收集用户信息的字段的**用途**能被程序判定"。三条常见误解，逐条破：

- **`type=tel` / `type=email` 不够**——它们只说明**数据类型**，不说明**用途**（同一个 `type=text` 可能是姓名也可能是公司）。必须用 `autocomplete` 的 Input Purposes token。
- **浏览器实际有没有自动填充不重要**。官方 Intent 逐字：*"Whether or not user agents actually autofill inputs is not relevant when evaluating this criterion. What matters is whether or not the inputs programmatically expose their purpose."* 反过来，浏览器靠启发式猜着填**也不能**算满足：*"user agents may use heuristics, rather than programmatically determined purposes, to autofill inputs – this is not sufficient to meet the requirements of this criterion."*
- **`name` 不等于 `given-name`**：`name` 是全名，`given-name` / `family-name` 是拆分。拆分字段必须用拆分 token，否则自动填充会填错格。

技术参考：**H98**（用 `autocomplete` 提供用途），失败例 **F107**。`billing` / `shipping` 前缀用于区分同一 token 的两种地址（官方 Example 即 *"using the HTML autocomplete detail tokens 'billing' and 'shipping'"*）。

### 8.3 SC 3.3.7 Redundant Entry（Level A）

同一条交易进程内，**已经提供过的信息不得要求再填**，除非：①重填是必要的（如"确认新密码"）②安全原因（如重新验证）③此前信息已失效。

三条落地：

- **地址复用**：勾选"账单地址与收货地址相同"（`available for the user to select` 的官方示例之一），勾选后**折叠**账单地址字段，不要求用户再选一遍。
- **浏览器 autocomplete 不算数**。官方 Intent 逐字：*"The autocomplete feature of browsers is not considered sufficient because it is the content (the website) that needs to provide the stored information for a redundant entry, or avoid asking for the same information again."* 站点自己必须回填。
- **范围可以跨域**：*"a process can run across different domains, so if a check-out process includes a 3rd party payment provider, that would be in scope."* 跳第三方支付再回来，也要保留订单上下文。
- **PII 警告**：回填实现不当会泄露信息——*"it is also possible that a poor implementation (for meeting this criterion) could leak additional PII"*。共享设备场景下，回填要能一键清除。
- **价格已填过就不该再问一次**：同一进程里"再次输入卡号"（官方失败例：*"A user submits a checkout form with an incorrect credit card number… Submitted information, such as credit card number, is not cleared from the form."* 反过来说，出错重填时**已填内容不得清空**）。
- 技术参考：**G221**（提供自动填充或可选复用）。

### 8.4 标签、错误与输入便利

- **可见 label + `for`**，`placeholder` 只做示例不做标签（SC 3.3.2）。
- **错误两处**：字段内联提示 + 顶部错误摘要（可聚焦的 `error summary`），摘要项链接到对应字段。错误文案写**修复动作**（"邮编应为 6 位数字"），不写"格式错误"（SC 3.3.3）。
- **卡号分组**：4-4-4-4 分组用 `letter-spacing` 或视觉分隔，**不要**把空格写进 `value`（会把长度校验与剪贴板填入搞坏）。
- **剪贴板可用**：卡号与一次性口令都必须允许用户从剪贴板填入，不得拦截。
- **键盘类型**：数字字段 `inputmode=numeric`，不要用 `type=number`（会出上/下箭头、滚轮误改、且无法保留前导零）。

## §9 支付方式与钱包按钮

- **Apple Pay 标记规范（逐字）**：*"The Apple Pay mark is available only in white with an outline rule. Other color options aren't available. Don't alter the artwork in any way or create your own version of the Apple Pay mark."* 即：**只有白描边版**，不得改色、不得重绘。
- **清space**：*"For marketing communications, the minimum clear space for the mark is one quarter the height of the mark."*
- **不得共享边框**：*"Don't allow the Apple Pay mark to share its surrounding border with another button or graphic."*——把 Apple Pay 与 Google Pay、PayPal 拼进同一条 1px 边框的分组按钮里，是明确违规。
- **背景**：*"A white or light background is preferred when displaying the Apple Pay mark."*
- **显隐**：按设备能力判断是否展示，用 Apple 的 [`canMakePayments`](https://developer.apple.com/documentation/apple_pay_on_the_web/applepaysession/1778027-canmakepayments/) 检测，不要按 UA 猜。
- **Google Pay 按钮规范本次未取到官方全文**（`developers.google.com` 两次 `fetch failed`），**不臆造**；沿用同一机制：官方素材、不改比例、留白边、按设备能力显隐。
- **卡组织图标**：等高等宽排列，容器 `aria-hidden="true"`，旁边用文本说明"支持 Visa / Mastercard"。
- **PSD2 / 3DS 跳转**：跳银行页面前后都要显示**订单摘要与金额**；返回后不重新收一遍信息（§8.3）。
- **一个主行动**：结账页只允许一个提交按钮。多个同级按钮（"支付"+"稍后支付"+"保存"）会让主行动失效。

## §10 费用透明：运费、税费、附加费

**铁律**：用户在**填地址之前**能看到费用政策（运费区间/税费规则/是否含税），在**付款之前**锁定最终总额。中间任何一步"突然多出一笔"，都是 §0 铁律一被破。

三级披露：

| 阶段 | 展示 | 允许的不确定 |
|---|---|---|
| 商品页 / 报价页 | 单价 + "运费与税费在结账时计算" 的**明确说明** | 可以不给总额，但必须说明为什么 |
| 购物车 | 小计 + 运费估算（按区域或"从 ¥X 起"） | 可以给区间 |
| 结账（填地址后） | 运费确切值 + 税费 + 总额 | **不再允许变化** |

**一致性检查**（三个数字必须逐字相同）：购物车页、结账页、支付跳转页上的总额；货币写法统一（`¥` 与 `CNY` 不混用，`$` 要标 USD/CAD）。任一处不一致，用户就会怀疑其他数字。

**附加费纪律**（与 `design-ethics-inclusion.md` 的 sneaking 同源）：

- 默认**不勾选**任何附加项（延保、加急、会员折扣后置捆绑）。
- 附加项出现在总价**上方**，且带"移除"。
- 用户可以只移除附加项而保留订单（"购物车增项必须有用户显式动作且可单独移除"）。
- 不在总价下方用小字加一行"服务费"，那是最典型的暗黑模式。

## §11 承诺闸门：SC 3.3.4（Level AA）

SC 3.3.4 Error Prevention (Legal, Financial, Data) 管的就是结账。适用条件：页面会导致**法律承诺或金融交易**、修改/删除用户数据、或提交测试答案。满足方式**三选一**（原文）：

> **Reversible**：*"Submissions are reversible."*
> **Checked**：*"Data entered by the user is checked for input errors and the user is provided an opportunity to correct them."*
> **Confirmed**：*"A mechanism is available for reviewing, confirming, and correcting information before finalizing the submission."*

**推荐组合**：复核页（Checked/Confirmed，G98）+ 提交前确认（G155，复选框或二次按钮）+ 短时撤销窗口（Reversible，G164）。

- **G98**：提交前让用户复核并更正。→ §7 的 check answers 页。
- **G155**：在提交按钮之外再提供一个确认机制（复选框"我已确认订单信息"）。→ 适用于高金额、不可退。
- **G164**：说明在线请求/交易**可修改或取消的时间窗**。→ "下单后 30 分钟内可在订单页取消"。
- **不要过度**：官方 Intent 明说 *"It is not the intent to require a confirmation for each save command or the simple creation or editing of documents, records or other data."* 每保存一次弹一次确认，既烦人也不合规性加分。
- **不可撤销必须写在按钮上方**：退款政策、不可退说明、扣款时间。放在折叠面板、tooltip、脚注里，等于没写（参见 §4 的 "must be unavoidable"）。
- 官方意图句可作评审话术：*"The intent of this success criterion is to help users with disabilities avoid serious consequences as the result of a mistake when performing an action that cannot be reversed."*

## §12 总价变化与无障碍播报

结账页里金额会随运费、优惠、数量变化。静默更新对读屏用户等于"什么都没发生"，对视力用户也容易漏看。

- **播报容器**：`<div role="status" aria-live="polite" aria-atomic="true">`，文本给**完整金额 + 原因**："已选择顺丰陆运，运费 ¥12，应付总额 ¥1,188.00"。
- **`aria-atomic="true"`**：否则读屏只念变化的数字片段，听不出是哪个金额。
- **只在关键变更播报**：总额、运费、折扣、税费。不要每敲一个字符都播报（输入过程中会变成噪音轰炸）。
- **防抖 300ms**：数字滚动动画期间不播报，动画结束播报最终值。
- **不要**用 `aria-live="assertive"`（会打断用户正在输入的内容）。
- 这与 SC 4.1.3 Status Messages（Level AA）同源，实现细节交叉 `feedback-states.md §6`。

## §13 信任与社会证明

- **只放可验证的信号**：支付方式标识、退货/退款政策、客服入口、实体信息（公司名/地址/联系方式）、HTTPS 与隐私链接。
- **不伪造**：评价、倒计时、"3 人正在浏览"、库存告急——造一个就是 §4 纪律一的同族问题，且被识破的代价远高于收益。
- **社会证明的位置**：可以放金额附近增强信心，但**不得**抢主行动；评价模块不放默认展开的大段文字。
- **只需什么问什么**：结账不需要生日、性别、公司规模。字段每多一个，弃单概率上升，且违反 SC 3.3.7 的精神。
- **卡号不落地**：用支付服务商的 iframe/SDK token，自己的 DOM 不接触完整卡号（PCI 边界）。

## §14 移动端结账

- **单列**，字段高 44–48px（触摸目标 ≥ 44×44，SC 2.5.5 AAA；最低 24×24，SC 2.5.8 AA）。
- **键盘类型正确**（见 §8.1），键盘弹起时不遮挡当前字段（`visualViewport` 或滚动到可视区）。
- **钱包按钮置顶**：Apple Pay / 快捷支付放在表单之前，能跳过整个表单。
- **地址简化**：邮编自动补城市、地址联想（但要允许手填）。
- **卡号扫描/相机**：可提供，但不作为唯一入口。
- **不要在移动端做横向对比表**：三档转纵向堆叠，推荐档置顶（§2）。

## §15 反模式清单（20 条）

1. 结账最后一步才出现运费或"服务费"。
2. 总价用小字，划线价/优惠横幅用大字（显著性倒挂）。
3. 附加项默认勾选（延保、加急、会员）。
4. 强制注册才能下单。
5. 地址要求填两遍，且不能复用。
6. 出错后清空已填内容（尤其卡号）。
7. 用 `placeholder` 当标签，聚焦后提示消失。
8. 卡号字段禁止从剪贴板填入。
9. 用一个 switch 表达"月付/年付"。
10. 年付只显示"折合每月"，不显示一次性扣款。
11. 折扣率算不回来（写"省 30%"，实际 18%）。
12. 划线价没有历史成交依据。
13. "企业档"价格写 "—" 或 "0"。
14. 推荐档只靠颜色区分。
15. 复核页的 Change 链接全部叫 "Change"。
16. 复核页返回后字段被清空。
17. 提交按钮写"继续"而不是"支付 ¥X"。
18. 多个同级主按钮争夺注意力。
19. Apple Pay 标记改色 / 与其它按钮共享边框。
20. 金额变化完全静默（无 `role="status"`）。

## §16 自检清单（20 条）

- [ ] 填地址**之前**能看到运费/税费政策。
- [ ] 付款前总额唯一且锁定，三处（购物车/结账/支付页）逐字一致。
- [ ] 货币写法全站统一，`$` 有国家限定。
- [ ] 划线价能追溯到历史成交价字段。
- [ ] 折扣率=页面两个价格算出来的值。
- [ ] 推荐档有文字角标 + 标签，不只靠颜色。
- [ ] 三档功能行同行对齐，容器 ≥ 960px，移动端纵向堆叠。
- [ ] 价格用 `tabular-nums`，对比表金额右对齐。
- [ ] 周期单位、小数位同页统一。
- [ ] 月/年切换用 radio group，两个标签同时可见，状态进 URL。
- [ ] 结账步骤 ≤ 3，有一个可复核的 review 页。
- [ ] review 页每段有 Change + 视觉隐藏文本，返回预填。
- [ ] 未答可选项显示 "Not provided"。
- [ ] 每个收集用户信息的字段都有正确的 `autocomplete` token（含 billing/shipping 前缀）。
- [ ] 账单地址可复用收货地址，勾选后不再要求重填。
- [ ] 支付失败/校验失败时不清空已填。
- [ ] SC 3.3.4 三选一至少满足一条（推荐 G98 + G155 + 撤销窗口）。
- [ ] 不可逆后果写在提交按钮上方，不藏折叠。
- [ ] 金额变化有 `role="status" aria-live="polite" aria-atomic="true"` 播报，且防抖。
- [ ] 结账页只有一个主提交按钮，文案写明金额或动作。

## §17 可抄代码（5 段，均可在标准库下直接跑）

### 17.1 价格排版生成器（字号/等宽数字/货币符号/周期）

```python
def price_html(amount, currency="¥", period="/月", big=True):
    """金额 → 内联 HTML 片段。字号取 §3 的数值区间，数字强制等宽。"""
    symbol_size = 0.5          # em，§3：货币符号 0.5em
    lift = "0.13em"            # baseline 上移
    font_size = 44 if big else 30   # px，§3：40–48 / 28–32
    assert 40 <= font_size <= 48 or 28 <= font_size <= 32
    assert 0 < symbol_size < 1
    nice = f"{amount:,.2f}".rstrip("0").rstrip(".") if amount != int(amount) else f"{amount:,.0f}"
    return (
        f'<span class="price" style="font-size:{font_size}px;line-height:1.1;'
        f'font-variant-numeric:tabular-nums;font-feature-settings:\'tnum\' 1">'
        f'<span class="cur" style="font-size:{symbol_size}em;vertical-align:{lift}">{currency}</span>'
        f'{nice}<span class="per" style="font-size:0.34em">{period}</span></span>'
    )


if __name__ == "__main__":
    a = price_html(1188, period="/年")
    assert "tabular-nums" in a and "font-size:44px" in a
    assert "¥" in a and "/年" in a
    b = price_html(99.5, big=False)
    assert "99.5" in b and "49.5" not in b
    c = price_html(1200)
    print(a)
    print(c)
    assert "1,200" in c      # 千分位
```

### 17.2 划线价台账校验（"原价"是否有依据）

```python
from datetime import date, timedelta


def validate_was_price(history, claimed_was, window_days=30, today=None):
    """history: [(date, price)]；claimed_was: 页面标的'原价'。
    返回 (ok, note)。规则见 §4 纪律一：被比较价格须真实且有依据。"""
    today = today or date.today()
    cutoff = today - timedelta(days=window_days)
    recent = [p for d, p in history if d >= cutoff]
    if not recent:
        return False, "窗口内无成交记录：不能标'原价'"
    lowest = min(recent)
    if float(claimed_was) < lowest - 0.005:
        return False, f"标的原价低于窗口最低成交价 {lowest}，属虚假比较"
    if float(claimed_was) > max(recent) + 0.005:
        return False, "标的原价高于窗口内最高成交价：从未以此价成交"
    return True, f"通过：窗口内成交价 {lowest}–{max(recent)}，标价 {claimed_was} 有成交依据"


def discount_percent(was, now):
    """折扣率必须能由两个价格算回，禁止单独手填（§4 纪律二、§6）。"""
    assert float(was) > 0
    return round((1 - float(now) / float(was)) * 100, 1)


if __name__ == "__main__":
    today = date(2026, 11, 13)
    hist = [(date(2026, 11, 1), 1299), (date(2026, 11, 8), 1299), (date(2026, 11, 12), 1188)]
    ok, note = validate_was_price(hist, 1299, today=today)
    print(ok, note)
    assert ok
    bad, why = validate_was_price(hist, 1999, today=today)
    assert not bad and "最高" in why
    stale, why2 = validate_was_price([(date(2026, 6, 1), 1999)], 1999, today=today)
    assert not stale
    assert discount_percent(1299, 1188) == 8.5
```

### 17.3 结账字段计划器（autocomplete token + 地址复用）

```python
ALLOWED_TOKENS = {
    "email", "tel", "name", "given-name", "family-name", "organization",
    "shipping name", "shipping address-line1", "shipping address-line2",
    "shipping address-level2", "shipping address-level1", "shipping postal-code",
    "shipping country", "billing address-line1", "billing postal-code",
    "cc-number", "cc-exp", "cc-csc", "cc-name",
}


def checkout_fields(needs_shipping=True, billing_same=True, card=True):
    """返回 [(field, autocomplete, inputmode)]，并校验 token 合法（§8.1 / SC 1.3.5）。"""
    plan = [("邮箱", "email", "email")]
    if needs_shipping:
        plan += [
            ("收件人", "shipping name", None),
            ("地址1", "shipping address-line1", None),
            ("城市", "shipping address-level2", None),
            ("邮编", "shipping postal-code", "numeric"),
            ("国家", "shipping country", None),
        ]
    if not billing_same:
        plan += [("账单地址", "billing address-line1", None)]
    else:
        plan += [("__billing_reuse__", "shipping address-line1", None)]  # 复用钩子
    if card:
        plan += [
            ("卡号", "cc-number", "numeric"),
            ("有效期", "cc-exp", "numeric"),
            ("安全码", "cc-csc", "numeric"),
        ]
    bad = [t for _, t, _ in plan if t not in ALLOWED_TOKENS and t != "__billing_reuse__"]
    assert not bad, f"非法 autocomplete token: {bad}"
    return plan


if __name__ == "__main__":
    p = checkout_fields(billing_same=True)
    print(len(p), "fields")
    for row in p:
        print(row)
    assert not any(f == "账单地址" for f, _, _ in p)   # 复用后不再收一遍（SC 3.3.7）
    assert any(f == "卡号" for f, _, _ in p)
    p2 = checkout_fields(billing_same=False)
    assert any(f == "账单地址" for f, _, _ in p2)
```

### 17.4 总价对账器（三处一致 + 加项透明）

```python
def reconcile(items, shipping, tax, extras=None, tolerance=0.01):
    """items: [(name, price)]；extras: [(name, price)] 必须为用户显式添加项。
    返回 (total, problems)，problems 非空即不能提交（§10）。"""
    extras = extras or []
    problems = []
    subtotal = sum(p for _, p in items)
    total = round(subtotal + shipping + tax + sum(p for _, p in extras), 2)
    if total <= 0:
        problems.append("总额非正数")
    for name, p in extras:
        if p > 0 and name.startswith("默认"):
            problems.append(f"默认勾选附加项：{name}")
    if tax < 0 or shipping < 0:
        problems.append("运费/税费出现负值")
    return total, problems


def assert_same_total(places):
    """places: {来源: 金额}，三处必须逐字一致（§10）。"""
    vals = set(round(v, 2) for v in places.values())
    assert len(vals) == 1, f"总额不一致: {places}"
    return list(vals)[0]


if __name__ == "__main__":
    t, prob = reconcile([("耳机", 999), ("保护套", 49)], 12, 0, [("延保", 0)])
    print(t, prob)
    assert t == 1060 and not prob
    t2, prob2 = reconcile([("耳机", 999)], 12, 0, [("默认延保", 59)])
    assert t2 == 1070 and prob2, "默认勾选必须报错"
    same = assert_same_total({"购物车": 1060.0, "结账": 1060, "支付页": 1060.00})
    assert same == 1060.0
    try:
        assert_same_total({"购物车": 1060, "结账": 1072})
        raise AssertionError("应当抛错")
    except AssertionError as e:
        assert "不一致" in str(e)
```

### 17.5 SC 3.3.4 承诺闸门验收器 + 总额播报片段

```python
def commitment_gate(reversible=False, checked=False, confirmed=False,
                    irreversible_notice_above_cta=False, amount_announced=None):
    """SC 3.3.4 三选一（§11）。返回 (pass, reasons)。"""
    reasons = []
    pass_gate = reversible or checked or confirmed
    if not pass_gate:
        reasons.append("三选一未满足：需 Reversible / Checked / Confirmed 之一")
    if not irreversible_notice_above_cta:
        reasons.append("不可逆后果未写在提交按钮上方（'must be unavoidable'）")
    if amount_announced is None:
        reasons.append("总额未播报（role=status）")
    else:
        text = str(amount_announced)
        if "总额" not in text or "¥" not in text:
            reasons.append("播报文本须含'总额'与金额")
    return (not reasons), reasons


def status_line(text):
    """§12：金额/费用变化的播报容器。aria-atomic 保证整句被读。"""
    safe = text.replace("<", "&lt;").replace(">", "&gt;")
    return (f'<div role="status" aria-live="polite" aria-atomic="true" '
            f'class="sr-only">{safe}</div>')


if __name__ == "__main__":
    ok, r = commitment_gate(checked=True, irreversible_notice_above_cta=True,
                            amount_announced="应付总额 ¥1,188.00")
    print(ok, r)
    assert ok and not r
    bad, why = commitment_gate()
    assert not bad and len(why) == 3
    s = status_line("已选顺丰陆运，运费 ¥12，应付总额 ¥1,188.00")
    assert 'role="status"' in s and "aria-atomic" in s and "总额" in s
    assert "&lt;" in status_line("<script>")
```

## §18 取源限制（公开记录，不臆造）

1. **Baymard 购物车放弃率榜单全文不可得**：`baymard.com/blog/cart-abandonment-rate`（标题 *"Cart Abandonment Rate: 50 Statistics (2026)"*）两次抓取均被站点全局导航占满并 "Content truncated"，`r.jina.ai` 代理与 `learn/reduce-cart-abandonment` 同样失败。**本章因此不引用任何 Baymard 百分比**，只做定性引用；需要数字时须先补取正文。
2. **Google Pay 官方按钮规范未取到**：`developers.google.com/pay/api/web/guides/brand-guidelines` 两次 `fetch failed`。本章只给不依赖该文档的通用原则（官方素材、不改比例、留白、按能力显隐），未引用其条文。
3. **Apple HIG 的 Apple Pay 页为 JS 渲染**：`developer.apple.com/design/human-interface-guidelines/apple-pay` 正文为空；本章 Apple Pay 全部引文来自可静态读取的 **Apple Pay Marketing Guidelines**（`developer.apple.com/apple-pay/marketing/`）。
4. **欧盟/中国法条的取源方式不是常规抓取**：EUR-Lex、legislation.gov.uk、europarl doceo 对脚本客户端返回 HTTP 202 + AWS WAF JS 挑战（空正文），`web_fetch` 与 curl 均被拦；欧盟第 6a 条经本机 headless Chrome（CDP）渲染 CELEX:32019L2161 取回 OJ HTML 后逐字抄录，中国条文经 gov.cn 国务院公报 2022 年第 19 号与 samr.gov.cn 两处官方页面互校（文本一致）。二次复核须用浏览器访问；本文件只逐字引用已核对句子，其余以条号 + 要点转述。
5. **FTC 官方站 403 + eCFR 跳转拦截**：改读 `ecfr.io/Title-16/Part-464`（Daily eCFR 版 2026-10-30，Source 90 FR 2166, Jan. 10, 2025），条文与 §464.1/§464.2 一致；正式引用请以 eCFR 原站为准。
6. **`patterns.md §定价表` 的旧数值未被推翻**：卡内边距 32px、价格 40–48px、货币符号 0.5em 三处与本章一致，本章仅补充「上移 0.12–0.15em」「`tabular-nums`」「差异 ≤ 20%」等可执行细则，未改旧值。
7. **折中效应**本章只称机制名（compromise effect），未引用实验原句与具体百分比；若要写进对外文案，须先补取原始研究。
8. 本章引用的 WCAG 条款级别：**SC 3.3.4 AA**、**SC 1.3.5 AA**、**SC 3.3.7 A**、**SC 4.1.3 AA**、**SC 1.4.1 AA**、**SC 3.3.2 / 3.3.3 A**、**SC 2.5.8 AA**、**SC 2.5.5 AAA**。
