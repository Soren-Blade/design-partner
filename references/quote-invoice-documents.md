# 报价与发票单据（Quote, Invoice & Order Documents）：报价单、发票、订单确认与对账的单据语法

> 适用：报价单 / 形式发票 / 订单确认 / 商业发票 / 贷项通知（红字发票）/ 对账单的字段设计、版式、状态机、打印与 PDF 产出；需要与 ERP、Peppol、ZUGFeRD/Factur-X、中国数电票对接的单据。
> 不适用：币种最小单位与含税口径的取值规则（→ `pricing-localization.md`）；结账页与承诺闸门（→ `pricing-checkout.md`）；发票投递邮件的版式（→ `email-design.md`）；多语言文案（→ `i18n-localization.md`）。

## §0 一句话立场

**发票不是一张好看的纸，而是「一条能被机器逐行复核的金额脊柱」+「一条能回溯到报价与订单的身份链」；设计能决定字段的层级、顺序、版式与可见性，不能决定税基、编号规则与红冲条件——所以先锁脊柱，再排版。**

由此分出两条界线：

- **设计能决定**：三件事在首屏是否同时可见（谁开给谁、单据号与日期、应付金额）；明细与合计的先后；金额右对齐与等宽数字；多页时每页重复什么；状态用文字还是颜色；打印成黑白后还剩多少信息。
- **设计不能决定**：税基怎么算、税额保留几位、发票号能不能重复、红冲要不要对方确认、报价单过期后能不能改日期续用。这些只有法条、规范和会计系统说了算——页面只能**如实呈现**，不能"美化"。

一句话判据：**任何一版单据设计，先把 BT-115（应付金额）算对，再谈它放在哪。**

## §1 判层：先问七个问题，再动手

| # | 问题 | 答"是"→去哪一节 | 答"否"→ 说明 |
|---|---|---|---|
| 1 | 这张单据是**请求**（报价/订单确认）还是**凭证**（发票/贷项）？ | §5 单据链 | 两者字段集不同，别用一张模板硬套 |
| 2 | 它会被**机器校验**（Peppol / EN 16931 / ZUGFeRD / 数电票平台）吗？ | §3 金额脊柱 + §6 载体 | 只在纸上给人看，可以省字段，但金额恒等式仍然成立 |
| 3 | 是否**跨境或多税率**（一张票上 ≥2 个税率）？ | §4 税与合规 | 单税率单地区可简化为一块小计 |
| 4 | 有没有**折扣 / 运费 / 预付款 / 尾差**？ | §3.5 增减项 | 有就必须决定"先减后税"还是"税后减"，且只能选一种 |
| 5 | 单据会不会**超过一页**？ | §7.4 多页规则 | 单页也要写页码，避免打印丢页无法察觉 |
| 6 | 出错时是**改**、**作废**还是**红冲**？ | §2.5 + §8 状态机 | 已开出的发票不能改，只能红冲或开更正票 |
| 7 | 主要读者是**财务/采购**还是**最终客户**？ | §7 版式 | 财务要"总额一眼可见 + 可核对"，客户要"我买了什么" |

### 四类构型：一张表定字段集

| 构型 | 何时用 | 必须有 | 绝不能有 | 编号 |
|---|---|---|---|---|
| **报价单** Quote | 成交前给价 | 有效期、版本号、币种、税口径、付款条件、接受方式 | "应付金额/已付"字样（会被误当账单） | `QUO-YYYY-NNNN-R01` |
| **订单确认** Order Confirmation | 收到 PO 后回执 | 客户 PO 号、行项、交期、变更说明 | 付款二维码/账号（不是付款请求） | `ORD-YYYY-NNNN` |
| **发票** Invoice | 履约完成、主张付款 | 发票号、开票日、税号、金额脊柱、付款期限、收款账户 | 未确定的金额、"约"、"暂定" | 法定序列，见 §2.1 |
| **贷项/红字** Credit Note | 退货、折让、开错票 | 原因、关联的原发票号与日期、负数或正数+方向声明 | 独立的新交易叙述 | 独立序列，必须引用原票 |

判层失败最常见的两种：把报价单做成"看起来像发票"（客户财务不敢收，也不敢付），把订单确认做成"付款请求"（客户付了不该付的钱）。

## §2 单据身份：号、日期、版本

### 2.1 发票号：唯一、连续、可排序

Peppol BIS Billing 3.0 对 BT-1（Invoice number）的字段定义逐字：

> "A unique identification of the Invoice. The sequential number required in Article 226(2) of the directive 2006/112/EC [2], to uniquely identify the Invoice within the business context, time-frame, operating systems and records of the Seller. No identification scheme is to be used."

设计后果，逐条可执行：

- 号码**全租户唯一**，不是"每个客户从 1 开始"；按字符串字典序排序必须等于按开出顺序排序（等宽补零，或纯数字）。
- 前缀只能表达**分组**（如公司实体、单据类型），不能表达**时间**：`INV-2026-000123` 里带年份可以，但排序必须靠后 6 位定宽数字，不能靠 `2026`。
- 同一号码**永不复用**：作废的号码也占位，重开必须新号。
- 不要在号码里放客户名、项目名——客户改名或项目重命名会让历史单据的"身份"漂移。
- 号码是**字符串**，不是整数：超过 15 位在 JS 里会丢精度（中国数电票 20 位就是例子，见 §2.3）。

反例：`INV-1`、`INV-2`、…、`INV-10` 的字典序是 `INV-1, INV-10, INV-2`；财务按号段对账时会把 10 号当成第 2 张。

### 2.2 日期：只写 `YYYY-MM-DD`

Peppol 业务规则 F001 逐字：

> "A date MUST be formatted YYYY-MM-DD."

BT-2（Invoice issue date）逐字：

> "The date when the Invoice was issued. Format \"YYYY-MM-DD\""

BT-9（Payment due date）逐字，并规定了"到期日与付款条件至少有一个"：

> "The date when the payment is due.Format \"YYYY-MM-DD\". In case the Amount due for payment (BT-115) is positive, either the Payment due date (BT-9) or the Payment terms (BT-20) shall be present."

设计后果：

- 页面显示可以是 `2026-11-19`，也可以是本地化 `19.11.2026`，但**写入数据层与电子载体的一律 `YYYY-MM-DD`**；两者由同一字段渲染，不做二次转换。
- **到期日与付款条件不能都空着**：要么给绝对日期，要么给 `Net 30` 这类条件，且系统必须能从开票日推出到期日（§13 段 F）。
- 不要用「开票后 30 天」这种相对文案替代到期日——客户财务系统只认日期。
- 日期字段不接受 `2026/11/19`、`11/19/2026`：`11/12/2026` 在美/欧是两张不同的票。

### 2.3 中国数电票：20 位号码是结构，不是流水

《国家税务总局关于推广应用全面数字化电子发票的公告》（国家税务总局公告 2024 年第 11 号，自 2024 年 12 月 1 日起施行）第四条逐字：

> "数电发票的号码为20位，其中：第1-2位代表公历年度的后两位，第3-4位代表开票方所在的省级税务局区域代码，第5位代表开具渠道等信息，第6-20位为顺序编码。"

拆成表：

| 位次 | 长度 | 含义 | 能不能拿来做 UI 分组 |
|---|---|---|---|
| 1–2 | 2 | 公历年度后两位 | 只能显示年份尾数，跨世纪会歧义 |
| 3–4 | 2 | 开票方省级税务局区域代码 | 可做区域标识，不可当客户地区 |
| 5 | 1 | 开具渠道等信息 | 不可反推"谁开的" |
| 6–20 | 15 | 顺序编码 | **唯一可排序段**，必须定宽显示 |

第三条逐字给出票面基本内容 17 项：

> "数电发票的票面基本内容包括：发票名称、发票号码、开票日期、购买方信息、销售方信息、项目名称、规格型号、单位、数量、单价、金额、税率/征收率、税额、合计、价税合计、备注、开票人等。"

设计后果：

- 号码栏用**等宽字体**（`tabular-nums` + monospace 或至少等宽数字），分 4/4/4/4/4 组显示但**存储为 20 位连续字符串**；中间加空格会让复制粘贴出错。
- 20 位超过 JS `Number.MAX_SAFE_INTEGER` 的安全整数范围，**必须按字符串处理**，禁止 `parseInt`。
- 页面不要从号码里"推导"开票日期——年份只有后两位；日期字段独立存在。

### 2.4 报价单：编号与版本分离

报价单没有法定编号规范，它是**商务承诺**，所以身份设计是产品决策：

- **编号**标识"这一次报价"，**版本**标识"第几次改价"：`QUO-2026-0142` + `Rev 03`。改价只升版本，不换编号；客户手上的 Rev 02 仍然可被系统找到并标记为"已被 Rev 03 取代"。
- 版本号等宽两位（`R01`…`R99`），超过 99 次改价是流程问题，不是编号问题。
- 每次改版必须记录**改了什么**（价格/数量/有效期/条款），并在页面顶部给一行"本版替代 R02（2026-10-30）"。
- 有效期用绝对日期（`Valid until 2026-12-19`），不用"30 天内有效"；默认 30 天是**工程默认值，无规范强制**，写进模板参数而不是写死在文案里。
- 过期报价的页面状态必须变（灰化 + "已过期，请索取新报价"），不能只是日期变小字。

### 2.5 更正、作废、红冲：三条不同的路

Peppol 的发票类型码（UNCL1001 子集）里，三类"不是新交易"的单据定义逐字：

> `384` **Corrected invoice** — "Commercial invoice that includes revised information differing from an earlier submission of the same invoice."

> `381` **Credit note** — "(1113) Document/message for providing credit information to the relevant party."

> `386` **Prepayment invoice** — "An invoice to pay amounts for goods and services in advance; these amounts will be subtracted from the final invoice."

中国数电票的红冲规则（同公告第八条）更硬：

> 蓝字发票未做用途确认/入账确认的，开票方可直接开具红字发票；已确认的，由任一方发起、对方确认《红字发票信息确认单》后由开票方开具。
> "《确认单》发起后72小时内未经确认的，自动作废。"

设计后果：

- **已开出的发票页面上不提供"编辑"**，只提供"开红字/更正"与"下载"；编辑入口一旦存在，就一定会有人改出与税务局留存不一致的 PDF。
- 红冲单必须**引用原发票号 + 原开票日期 + 红冲原因**，且金额方向明确（负数或"红字"字样），不能只写"调整"。
- 作废（void）只适用于未交付/未入账的单据；作废后号码保留、状态可见、不再参与应收。
- "72 小时自动作废"是**确认单**的时效，不是发票的时效——文案不要把两者混成一句"72 小时内有效"。

## §3 金额脊柱：五个数必须自洽

这是整份文档最不能含糊的一节。任何一张发票，金额只有五个数，且由四条恒等式锁死。

### 3.1 五个数与四条恒等式

| 记号 | 名称 | 含义 |
|---|---|---|
| BT-106 | Sum of Invoice line net amount | 所有行净额之和 |
| BT-109 | Invoice total amount without VAT | 不含税总额（含单据级折扣/费用） |
| BT-110 | Invoice total VAT amount | 税额合计 |
| BT-112 | Invoice total amount with VAT | 价税合计 |
| BT-115 | Amount due for payment | **应付金额（唯一付款依据）** |

EN 16931 计算规则逐字（Peppol 规则库 `/rules/ubl-tc434/` 每页 "Message" 字段）：

> BR-CO-10: "Sum of Invoice line net amount (BT-106) = Σ Invoice line net amount (BT-131)."

> BR-CO-13: "Invoice total amount without VAT (BT-109) = Σ Invoice line net amount (BT-131) - Sum of allowances on document level (BT-107) + Sum of charges on document level (BT-108)."

> BR-CO-15: "Invoice total amount with VAT (BT-112) = Invoice total amount without VAT (BT-109) + Invoice total VAT amount (BT-110)."

> BR-CO-16: "Amount due for payment (BT-115) = Invoice total amount with VAT (BT-112) -Paid amount (BT-113) +Rounding amount (BT-114)."

把这四条画成一条脊柱：

```
行净额 BT-131 × n
   └─ Σ ────────────────→ BT-106
        − 单据级折扣 BT-107
        + 单据级费用 BT-108
        ────────────────→ BT-109（不含税总额）
        + 税额 BT-110
        ────────────────→ BT-112（价税合计）
        − 已付 BT-113
        + 尾差 BT-114
        ────────────────→ BT-115（应付）
```

设计后果：

- 页面上的"合计"**只有一个**："应付金额 BT-115"。BT-109 / BT-110 / BT-112 是过程数，可以并列展示，但不能都叫"合计"，否则客户财务会挑其中一个去付。
- 明细表最后一行必须是 BT-106 或 BT-109 的**明确标签**（"小计（不含税）"），不能只写一条横线。
- 任何"预计""参考""以实际为准"的字样都不能出现在 BT-115 附近。

一张两税率、带预付款的票，五个数长这样（§13 段 A 实跑）：

| 字段 | 值 | 怎么来的 |
|---|---|---|
| 行净额 | 37.50 / 99.00 / 8.40 | 3×12.50、1×99.00、2×4.20 |
| BT-106 | 144.90 | 三行相加 |
| BT-109 | 144.90 | 无单据级折扣/费用 |
| BT-110 | 26.53 | 19% 组 136.50×19%=25.935→25.94；7% 组 8.40×7%=0.588→0.59 |
| BT-112 | 171.43 | 144.90 + 26.53 |
| BT-115 | 121.43 | 171.43 − 预付款 50.00 |

### 3.2 行净额：乘法顺序写死

Peppol 业务规则 R120 逐字（原文结尾缺右括号，照抄）：

> "Invoice line net amount MUST equal (Invoiced quantity * (Item net price/item price base quantity) + Sum of invoice line charge amount - sum of invoice line allowance amount"

R130 逐字：

> "Unit code of price base quantity MUST be same as invoiced quantity."

设计/实现后果：

- 行净额 = `数量 × (净单价 ÷ 价格基数) + 行费用 − 行折扣`，**先除后乘**与**先乘后除**在 2 位小数下可能差 1 分；规范只给了公式，工程上必须固定一种并写进校验（本资产固定为"单价先除以基数，再乘数量"）。
- 价格基数不等于 1 时（如"每 1000 个 12.50"），**单位代码必须与开票数量一致**（R130）；页面上要同时显示"单价基数"，否则客户按 1 个算会觉得单价错了。
- 数量为 0 的行不应存在（`Document MUST not contain empty elements.`，R008）；赠品也要给 0 价行并注明。

### 3.3 舍入：每一层都保留 2 位

Peppol 每条 BR-CO 的 XPath 实现都能看到同一形状（以 BR-CO-15 为例）：

```
round( cbc:TaxExclusiveAmount * 10 * 10 ) div 100
      + round( cbc:TaxAmount * 10 * 10 ) div 100
```

即：**先乘 100、四舍五入取整、再除 100**，也就是每一层金额各自舍入到 2 位小数，而不是"最后合计时舍入一次"。

设计后果：

- 行净额、税基、税额、价税合计是**四个可独立舍入的数**，加起来天然可能差 1 分；差额必须有落点（保留在 BT-115，或作为 BT-114 尾差显式列出）。
- 显示层**不得重算**：页面必须渲染后端给的值，JS 里 `qty * price` 只用于输入校验提示，不能覆盖已定稿金额。
- 舍入方向（半进位规则）在 XPath `fn:round` 里由规范定义，本资产未逐字取到 fn:round 的 .5 处理条文（见 §14），工程上统一用"四舍五入、远离零"并在测试里钉死。

### 3.4 一分钱去哪：两个实跑样例

同样三行、同样 19%，两种算法差 1 分（§13 段 B 实跑输出）：

| 样例 | 行 | 逐行取整税额 | 汇总取整税额 | 差 |
|---|---|---|---|---|
| A | 3.99 + 19.99 + 0.99 = 24.97 | 0.76 + 3.80 + 0.19 = **4.75** | 24.97 × 19% = 4.7443 → **4.74** | +0.01 |
| B | 7.49 + 12.49 + 5.95 = 25.93 | 1.42 + 2.37 + 1.13 = **4.92** | 25.93 × 19% = 4.9267 → **4.93** | −0.01 |

两个方向都出现，说明这不是"取整误差总是偏向某边"，不能靠调方向消除。

裁决（写死）：

1. 税额按 **BG-23 每个税率分组**算一次（BR-S-08 语义），组内不逐行取整再相加。
2. BT-112 = BT-109 + BT-110，BT-115 = BT-112 − BT-113 + BT-114；**页面上的应付必须等于这条方程的结果**，四舍五入只发生在等式右侧的每一项。
3. 差额如果必须落在某一行（例如系统按行开票），把差额记在该税率组的最后一行，并在备注写"尾差调整"，不要让总额自己漂。

### 3.5 增减项：折扣、运费、预付款、尾差

| 字段 | 记在哪 | 先减还是后减 | 设计后果 |
|---|---|---|---|
| 单据级折扣 BT-107 | BT-109 之前 | 先减，**再计税** | 票面必须写出折扣前金额，否则客户无法验算 |
| 单据级费用 BT-108 | BT-109 之前 | 先加，**再计税** | 运费若免税，必须单独成税率组，不能混进主税率 |
| 行折扣 / 行费用 | 行内 | 先于行净额 | 与 R120 一致，票面可只显示净额+折扣说明 |
| 已付 BT-113 | BT-115 之前 | 税后减 | 预付款发票（386）必须有，否则同一笔钱被收两次 |
| 尾差 BT-114 | BT-115 | 最后加 | 只在有明确来源时出现，不能当"凑整"用 |

一个常见错误：把"折扣"写成负数量行。R120 的行净额允许负值，但许多 ERP 与 Peppol 校验把负数量视为退货；折扣应走 BT-107 或行折扣字段。

### 3.6 多税率：按税率分组，不按商品分组

BR-S-08 逐字（以标准税率为例）：

> "For each different value of VAT category rate (BT-119) where the VAT category code (BT-118) is "Standard rated", the VAT category taxable amount (BT-116) in a VAT breakdown (BG-23) shall equal the sum of Invoice line net amounts (BT-131) plus the sum of document level charge amounts (BT-99) minus the sum of document level allowance amounts (BT-92)…"

R053 逐字：

> "Only one tax total with tax subtotals MUST be provided."

设计后果：

- 一张票上出现 19% 与 7% 时，票面底部必须是**两张小计**（税基 / 税额），而不是一行"税额合计"。
- 小计的排列顺序固定：按税率降序，或按税基降序，**全站统一**；不要按行出现顺序，否则同一客户两张票的小计顺序会变。
- 每个小计必须带税率与税基两个数；只写税额等于让客户无法验算。

## §4 税与合规字段

### 4.1 税分类码：0 不等于免税

Peppol 税分类码（UNCL5305 子集）逐字：

> `S` **Standard rate** — "Code specifying the standard rate."
> `Z` **Zero rated goods** — "Code specifying that the goods are at a zero rate."
> `E` **Exempt from Tax** — "Code specifying that taxes are not applicable."
> `AE` **Vat Reverse Charge** — "Code specifying that the standard VAT rate is levied from the invoicee."
> `K` **VAT exempt for EEA intra-community supply of goods and services** — "A tax category code indicating the item is VAT exempt due to an intra-community supply in the European Economic Area."
> `G` **Free export item, VAT not charged** — "Code specifying that the item is free export and taxes are not charged."
> `O` **Services outside scope of tax** — "Code specifying that taxes are not applicable to the services."

设计后果：

- 票面**不能只显示"税额 0"**：零税率、免税、反向征收、范围外是四件不同的事，税额都是 0；必须显示分类与一句法定说明（"Reverse charge: VAT to be accounted for by the recipient" 之类）。
- 分类码与税率互斥：`E` / `O` / `AE` 不应同时出现非零税率；`S` 必须有正税率。
- 中文票面用"税率/征收率"一栏承载同类信息，**不要自造"免税 0%"** 的写法替代法定栏目。

### 4.2 卖方税号：至少一个能自动识别

Peppol 对 BT-31/32 的填法逐字：

> "For Seller VAT identifier (BT-31), use value "VAT", for the seller tax registration identifier (BT-32), use != "VAT""

并要求卖方标识至少一个（BT-29/30/31）：

> "In order for the buyer to automatically identify a supplier…"

设计后果：

- 税号是**结构化字段**（scheme + value），不是一段自由文本；`VAT` 与 `tax registration` 是两个 scheme，不能混用一个 label。
- 页面上税号要带国家前缀（`DE` / `FR` / `CN`），且与注册地址的国家一致；跨境票缺前缀是退单第一原因。
- 中国数电票的"销售方信息"含名称与纳税人识别号，18 位统一社会信用代码按字符串存。

### 4.3 单币种：一张票只能一种币

BT-5 逐字：

> "The currency in which all Invoice amounts are given, except for the Total VAT amount in accounting currency. Only one currency shall be used in the Invoice…"

R051 逐字：

> "All currencyID attributes must have the same value as the invoice currency code (BT-5), except for the invoice total VAT amount in accounting currency (BT-111)."

CL007 逐字：

> "Currency code must be according to ISO 4217:2005"

设计后果：

- 币种是**单据级**属性，显示在金额表头或每个金额旁；不要逐行切币（同一张票两种币，客户无法付款）。
- 会计币种（BT-111）只用于税额的记账口径，不是第二个展示币种；页面若显示，必须标"记账币种，仅税额"。
- 金额格式的小数位由币种决定（JPY 0 位、KWD 3 位），规则在 `pricing-localization.md` §2，本资产只负责"整张票同币"。

### 4.4 中国票面：17 项基本内容

公告第三条逐字列出 17 项（见 §2.3）。设计上按"四个区"组织：

| 区 | 含哪些项 | 版式要求 |
|---|---|---|
| 抬头区 | 发票名称、发票号码、开票日期 | 号码等宽、日期 `YYYY-MM-DD` 或法定格式，二者同一行 |
| 双方区 | 购买方信息、销售方信息 | 名称 + 纳税人识别号成对；缺一不可 |
| 明细区 | 项目名称、规格型号、单位、数量、单价、金额、税率/征收率、税额 | 数量/单价/金额右对齐，单位左对齐 |
| 合计区 | 合计、价税合计、备注、开票人 | 价税合计为唯一最大字；备注不省略 |

"合计"与"价税合计"是两个数，不能合并显示；备注区即使为空也要保留位置（数电票的备注承载差额征税、建筑项目地址等法定信息）。

### 4.5 中国：额度与红冲是两个不同机制

第六条逐字：

> "发票总额度，是指一个自然月内，纳税人发票开具总金额（不含增值税）的上限额度。"

第八条逐字的红冲流程见 §2.5。设计后果：

- 开票界面的"还可开票额度"必须显示**不含税**口径，并注明"本月"；显示含税额会让用户以为额度更多。
- 额度不足时，界面要给"下月再开/拆票/申请调整"三条出口，而不是只报错。
- 红冲入口只在"已开具"状态出现，且必须先选原因；不要做成"删除发票"。

## §5 单据链：报价 → 订单 → 确认 → 发票

### 5.1 三单对齐：每张票都要能回溯

R003 逐字（fatal）：

> "A buyer reference or purchase order reference MUST be provided."

BT-10 逐字：

> "An identifier assigned by the Buyer used for internal routing purposes. An invoice must have buyer reference or purchase order reference (BT-13)."

设计后果：

- 发票上必须至少有 **Buyer reference** 或 **PO 号** 之一；客户内部没有 PO 时，按 Peppol 惯例填 `NA`，但字段不能空。
- 报价单号也要能回溯：发票的"客户订单号"栏可以放报价号+PO 号两个，别只留一个自由文本给人手填。
- 三单的**行项 ID 要对齐**（同一行的 SKU/描述在报价、订单、发票里一致），否则对账时要人肉匹配。

字段映射（`→` 表示必须原样带过去，`≈` 表示允许按规则重算，`×` 表示不带）：

| 字段 | 报价单 | 订单确认 | 发票 | 规则 |
|---|---|---|---|---|
| 客户与地址 | 有 | → | → | 发票地址决定税率与运费，改了要重算 |
| 行项 SKU + 描述 | 有 | → | → | 描述可在发票上更完整，但不改 SKU |
| 数量 | 有 | → | ≈ | 发票按实际交付量，偏差需在备注说明 |
| 单价 | 有 | → | → | 发票价以订单价为准；改价必须换报价版本 |
| 折扣 | 有 | → | ≈ | 发票折扣按订单条件重算，不抄报价的"预估折扣" |
| 税率 | 有 | → | ≈ | 税率由开票时点与销售地决定，不能从订单抄 |
| 币种 | 有 | → | → | 一张票只能一种币 |
| 付款条件 | 有 | → | → | 到期日按开票日重推（§5.4） |
| 单据号 | QUO | ORD | 法定序列 | 各自独立，互不复用 |
| Buyer reference / PO | 可空 | 必有 | 必有 | R003：发票缺 PO 必须有 buyer reference |

### 5.2 报价单必备字段（15 项）

| # | 字段 | 判据 |
|---|---|---|
| 1 | 报价单号 + 版本 | §2.4 |
| 2 | 客户名称 + 联系人 + 地址 | 地址决定税与运费 |
| 3 | 报价日期 / 有效期至 | 绝对日期 |
| 4 | 币种 | 单据级唯一 |
| 5 | 含税/不含税口径 | 与税额栏一致 |
| 6 | 行项：描述、规格、单位、数量、单价、折扣 | 单价基数写清 |
| 7 | 税率与小计 | 多税率分组 |
| 8 | 运费/安装费/其他费用 | 单独成行，不并入单价 |
| 9 | 付款条件 | Net 30 / 预付比例 / 分期 |
| 10 | 交货期或交付方式 | 与订单确认一致 |
| 11 | 报价有效期内的价格锁定声明 | "Prices valid until…" |
| 12 | 接受方式 | 签字回传 / 线上下单 / 邮件确认 |
| 13 | 条款链接 | 完整条款另页，正文只放链接与版本号 |
| 14 | 版本变更摘要 | 顶部一行 |
| 15 | 联系人 | 客户要能问"这行是什么意思" |

反模式：报价单只给总价，不给单价与小计——客户无法比较，销售也无法解释折扣。

### 5.3 订单确认：Order-X 的三类文档

FeRD 对 Order-X 的说明逐字（德语）：

> "ORDER…vom Käufer zum Lieferanten"、"ORDER_RESPONSE, Versand einer Bestätigung, Ablehnung oder Änderungsempfehlung"、"ORDER_CHANGE"

即：买方下单（ORDER）、卖方回执（ORDER_RESPONSE，可以是确认、拒绝或改单建议）、变更（ORDER_CHANGE）。

设计后果：

- 订单确认**不是付款请求**：不要放收款账户、二维码、金额大写；放了客户就会付。
- 拒绝与改单建议必须走同一条"回执"通道，页面要有明确的三态（已确认 / 有变更 / 已拒绝），并用文字而不是只用一个颜色点。
- 客户 PO 号是主键：确认单顶部第一行应是"Your PO: …"，而不是我们自己的订单号。

### 5.4 付款条件与折扣（Skonto）

BT-20（Payment terms）是自由文本，但德国 Peppol 规则对"提前付款折扣"给了机器可读的写法，DE-R-018 逐字：

> "First segment "SKONTO", second segment amount of days ("TAGE=N"), third segment percentage ("PROZENT=N"). Percentage must be separated by dot with two decimal places… Each entry shall start with a #, the segments must be separated by # and a row shall end with a #… All statements on cash discount for prompt payment shall be given in capital letters."

例：`#SKONTO#TAGE=10#PROZENT=2.00#`（10 天内付款享 2% 折扣）。

设计后果：

- 付款条件在票面上要写成**人能算的句子**：`2% discount if paid within 10 days, net 30`，并在数据层存结构化折扣（天数 + 百分比），不要只存一句自由文本。
- 折扣是**税后**还是**税前**必须明确；B2B 常见是"按含税金额折"，页面要写清基数。
- 到期日由 `开票日 + 条件` 推出（§13 段 F），且必须与 BT-9 一致；两者不一致时以 BT-9 为准并告警。
- 多个折扣档（2/10, 1/20, net 30）要按天数升序显示，不要把最优档藏起来。

### 5.5 发票类型码：别把贷项开成发票

UNCL1001 子集逐字：

> `380` **Commercial invoice** — "(1334) Document/message claiming payment for goods or services supplied under conditions agreed between seller and buyer."
> `389` **Self-billed invoice** — "An invoice the invoicee is producing instead of the seller."
> `71` **Request for payment** — "Document/message issued by a creditor to a debtor to request payment of one or more invoices past due."
> `326` **Partial invoice** — "Document/message specifying details of an incomplete invoice."

设计后果：

- 类型码是**单据头字段**，页面上应有一行人类可读的类型（"Commercial invoice" / "Credit note"），而不是只靠文件名。
- 自开票（389）必须显示"由买方代开"，否则卖方会以为是别人伪造的票。
- 催款单（71）不是发票：不能占用发票号段，也不能带"发票"字样。

## §6 电子发票载体

### 6.1 混合格式：PDF 是给人看的，XML 是给机器看的

FeRD 对 ZUGFeRD 的说明逐字（德语）：

> "Als hybrides Datenformat integriert ZUGFeRD in einem PDF-Dokument (PDF/A-3) strukturierte Rechnungsdaten im XML-Format… PDF und XML müssen die Vorgaben des § 14 Abs. 4 Umsatzsteuergesetz (UStG) berücksichtigen, um inhaltlich identische Mehrstücke derselben Rechnung darzustellen."

> "Da die Finanzverwaltung keine konkreten Prüfpflichten bzw. Kontrollmaßnahmen für dieses Verfahren festgelegt hat, ist dem Rechnungssender und dem Rechnungssteller zu empfehlen, eigene Prüfmechanismen zur Sicherstellung der inhaltlichen Identität der beiden Rechnungen einzuführen."

保存与"打印件不算"逐字：

> "Das Umsatzsteuergesetz sieht vor, dass Rechnungen acht Jahre aufzubewahren sind (§ 14b Abs. 1 S. 1 UStG). … elektronische Rechnungen sind originär elektronisch aufzubewahren und müssen maschinell auswertbar sein (Randziffer 128 GoBD vom 28. November 2019). Eine Aufbewahrung elektronischer Rechnungen in ausgedruckter Form ist nicht möglich."

邮件只是信封，逐字：

> "Wird die elektronische Rechnung per E-Mail übersandt, so ist die E-Mail selbst als reines Transportmittel der Rechnung (= Briefumschlag der elektronischen Rechnung) grundsätzlich nicht aufzubewahren…"

设计后果：

- PDF 与 XML **必须由同一份数据渲染**，不允许"PDF 一个模板、XML 另一个拼装"；两份分别生成就一定会出现金额或日期不一致。
- 混合格式的 PDF 必须满足 PDF/A-3（字体嵌入、无外部依赖、色彩空间可预测）；扫描件贴一层 XML 不算。
- 下载按钮给的是**一个文件**（PDF 内含 XML），不是两个文件；拆开发送会让客户只归档 PDF，八年后 XML 丢失。
- 打印件只作阅读副本，页面应有"电子版为准"的说明；不要设计"打印后盖章回传"的流程来替代电子归档。

### 6.2 版本与时效

ZUGFeRD 当前版本 **2.5.2，2026-08-04 发布**（FeRD 页面 Infopaket 标题："Infopaket für das E-Rechnungsformat ZUGFeRD 2.5.2 vom 04.08.2026"）。基础规范是 EN 16931（2017-06-28 发布）与 EU 指令 2014/55/EU（2014-04-16），语法来自 UN/CEFACT CII，PDF 侧来自 ISO 19005-3:2012（PDF/A-3）。

设计后果：

- 模板与校验器要**同时记录版本号**（ZUGFeRD 2.5.2 / EN 16931 / Peppol BIS 3.0 "May 2026 Release"），并在 PDF 元数据里写；客户投诉"格式不对"时，版本是第一诊断项。
- 版本升级只改语法映射，不改金额脊柱；升级验收先跑 §13 段 A/B，再跑官方校验器。

### 6.3 中国数电票：单一联次、自动交付、次数可见

公告第二条逐字："数电发票为单一联次，以数字化形态存在"；第一条："数电发票与纸质发票具有同等法律效力。"

第九条逐字：

> "已开具的数电发票通过电子发票服务平台自动交付。开票方也可以通过电子邮件、二维码、下载打印等方式交付数电发票。选择下载打印方式交付的，数电发票的票面自动标记并显示"下载次数""打印次数"。"

设计后果：

- 不要设计"第一联存根/第二联客户"——数电票只有一联；任何"联次"字样都是旧思维。
- 下载/打印次数是**票面字段**，会随交付方式自动出现；UI 不要在票面外再自造一个"已打印 3 次"的徽标，避免与票面数字冲突。
- 二维码交付要给出**有效期与刷新**规则；二维码指向的页面必须能在手机上一屏看到号码、金额、开票方。
- 邮件交付时，附件文件名应含发票号与开票日（`发票_20261119_12345678901234567890.pdf`），便于客户归档检索。

### 6.4 交付渠道矩阵

| 渠道 | 适用 | 设计要点 | 风险 |
|---|---|---|---|
| 平台自动交付（数电票） | 中国境内 | 交付状态回执、失败重试 | 客户未登录平台看不到 |
| 邮件附件 | 通用 | 单文件、文件名含号与日期、正文写明金额与到期日 | 被当垃圾邮件、附件过大 |
| 客户门户下载 | B2B 大客户 | 列表可按号/日期/状态筛，批量下载 zip | 权限与审计日志 |
| 二维码/短链 | 移动端、现场 | 一屏可读、限时、可刷新 | 截图外传、链接过期 |
| API/Peppol 网络 | 欧洲 B2B/B2G | 回执与状态码、重发幂等 | 地址（EAS/ID）配错 |

## §7 版式：一页 A4 能读多少

### 7.1 页面与安全边距

| 项 | 值 | 来源 |
|---|---|---|
| 纸张 | A4 210 mm × 297 mm | ISO 216 标称尺寸（原文付费，见 §14） |
| 安全边距 | 上下左右 ≥ 10 mm，推荐 15 mm | **工程默认，无规范强制** |
| 内容宽度 | 180 mm（A4 减 2×15 mm） | 由上两行推出 |
| 字体嵌入 | PDF/A-3 必须嵌入全部字体 | ISO 19005-3（转引，见 §14） |
| 出血 | 单据不需要出血；有底色的色块也必须落在安全区内 | 工程默认 |

打印机的不可打印区通常 4–5 mm，10 mm 是"大多数打印机 + 大多数装订方式都不吃字"的下限；15 mm 给打孔与订书留位。

### 7.2 字号与层级（工程默认，无规范强制）

| 层 | 字号 | 字重 | 用途 |
|---|---|---|---|
| 单据类型标题 | 16–20 pt | 600–700 | "发票 / INVOICE" |
| 应付金额 | ≥ 14 pt，建议 18–24 pt | 700 | 全页最大字，唯一焦点 |
| 分区标题 | 10–11 pt | 600 | "Bill to / 明细 / 付款信息" |
| 表头 | 8–9 pt | 600 | 列名 |
| 表格正文 | 8–9 pt | 400 | 行项 |
| 条款与页脚 | 7–8 pt | 400 | 法务、银行信息 |

结论句：**应付金额的字号必须是全页最大，且比第二大的数字至少大 1.4 倍**；否则客户财务在扫读时找不到该付多少。

### 7.3 表格列与对齐

| 列 | 对齐 | 数字格式 | 宽度建议 |
|---|---|---|---|
| 描述 | 左 | 自动换行，最多 3 行 | 剩余宽度 |
| 规格/SKU | 左 | 等宽或常规 | 18–25 mm |
| 数量 | 右 | 千分位，按单位精度 | 15–20 mm |
| 单位 | 左 | 缩写（pcs / kg / h） | 10–12 mm |
| 单价 | 右 | 2 位小数（按币种） | 22–28 mm |
| 税率 | 右 | `19%` 或 `0%` | 12–15 mm |
| 金额 | 右 | 2 位小数，千分位 | 26–32 mm |

- 所有金额列使用 `font-variant-numeric: tabular-nums`，否则数字列会在右对齐时抖动。
- 金额与币种：整列同币时币种写在列头（`Amount (EUR)`），逐行重复会把列撑宽且噪音大。
- 负值（红字）用**括号或前置负号**二选一，全站统一；不要用红色单独表示负数（黑白打印会丢）。

### 7.4 多页规则

| 规则 | 判据 |
|---|---|
| 每页重复 | 单据号 + 页码 `n / N` + 客户名（至少三项，缺一项就可能在打印后拼错页） |
| 表头重复 | 每页表格都有列头（`thead` 在打印时重复） |
| 行不拆页 | `break-inside: avoid` 用于行；一行被拆到两页等于读不出来 |
| 合计不孤页 | 合计区与至少 2 行明细同页；`break-before: avoid` |
| 末页留白 | 末页至少保留签名/付款信息区，不允许只有一行合计 |
| 页脚 | 公司名、地址、税号、银行信息、条款链接——每页或仅末页，二选一并全站统一 |

### 7.5 首屏三件事

无论屏幕还是纸张，读者在前 5 秒要能回答三个问题：

1. **谁开给谁**（双方名称 + 地址 + 税号）
2. **这是哪张单**（类型 + 号码 + 日期）
3. **要付多少、什么时候付**（BT-115 + 到期日）

三者不在同一屏（或同一页上半部），版式就是失败的——其余信息再漂亮也救不回来。

首屏骨架（A4，15 mm 边距，屏幕同构）：

```
┌──────────────────────────────────────────────────────────────┐
│  [Logo]                            INVOICE 发票               │  类型：最大字号之一
│                                    发票号 INV-2026-000123    │  号码：等宽
│                                    开票日 2026-11-19         │  日期：YYYY-MM-DD
├───────────────────────────┬──────────────────────────────────┤
│ 开票方 Seller             │ 购买方 Bill to                   │  双方：并列，不上下堆叠
│ 名称 / 地址 / 税号        │ 名称 / 地址 / 税号 / Your PO     │  税号带国家前缀
├───────────────────────────┴──────────────────────────────────┤
│ 明细表（描述｜SKU｜数量｜单价｜税率｜金额）                    │  金额列右对齐 + tabular-nums
│ …                                                            │
├──────────────────────────────────────────────────────────────┤
│                    小计（不含税）            144.90           │  右对齐，标签明确
│                    税额 19% 25.94 / 7% 0.59   26.53           │  按税率分组
│                    已付（预付款）            -50.00           │
│  ┌────────────────────────────────────────┐                  │
│  │ 应付金额  EUR 121.43                   │                  │  全页最大、唯一焦点
│  └────────────────────────────────────────┘                  │
│  到期日 2026-12-19 ｜ 付款条件 2% 10 天, net 30               │  紧贴应付，不隔断
├──────────────────────────────────────────────────────────────┤
│ 收款账户 ｜ 条款链接 ｜ 页脚：第 1 / 2 页                      │  每页重复
└──────────────────────────────────────────────────────────────┘
```

三条硬约束：应付金额框的视觉重量必须大于任何明细行；到期日与付款条件必须与应付金额同屏；双方信息必须并列而不是"卖方在上、买方藏在下"。

### 7.6 打印验收（黑白 + A4）

- 通用规则（纸张、分页、去色、页脚）一律走 `print-export.md`，本节不抄第二份。
- 单据特有：去色后表头 / 合计行 / 必填标记靠字重与边框区分；金额列不出现半行裁切（`overflow: visible`）；长描述换行不破坏数字列（表格布局，不用绝对定位）。

## §8 状态与对账

### 8.1 单据状态机

```
draft ──issue──> issued ──send──> sent ──pay──> paid
                    │                 │
                    ├─void──> void    ├─overdue──> overdue ──pay──> paid
                    └─credit─> credited（生成红字单，原票标记已冲）
```

| 迁移 | 允许 | 说明 |
|---|---|---|
| draft → issued | 是 | 一旦 issued，金额冻结 |
| issued → sent | 是 | 交付动作，不是状态装饰 |
| sent → paid | 是 | 以收款回执为准，不以"客户说付了"为准 |
| sent → overdue | 是 | 到期日次日自动 |
| issued → void | 是 | 仅未交付/未入账 |
| sent → credited | 是 | 生成红字单，原票保留 |
| paid → * | 否 | 已收款不能改状态；退款走红字/退款单 |
| void → issued | 否 | 作废即终态，重开新号 |

设计后果：状态是**数据**，不是颜色。每个状态都要有文字标签；颜色只做辅助，且对比度 ≥ 3:1（非文本）与 ≥ 4.5:1（文字）。

### 8.2 对账单与账龄

对账单（statement of account）不是发票，字段不同：期初余额、本期发票、本期收款、期末余额、逾期明细。

| 账龄桶 | 区间 | 用途 |
|---|---|---|
| 未到期 | 到期日 ≥ 今天 | 正常 |
| 1–30 天 | 逾期 1–30 | 首次催收 |
| 31–60 天 | 逾期 31–60 | 二次催收 |
| 61–90 天 | 逾期 61–90 | 升级 |
| 90+ 天 | 逾期 > 90 | 法务/坏账准备 |

账龄桶的边界是**工程惯例，无规范强制**；一旦选定就固定，且区间必须左闭右开，避免同一张票进两个桶。

### 8.3 催收文案的三段式

`事实（哪张票、多少钱、逾期几天）→ 影响（将暂停服务/计息）→ 动作（付款链接/联系方式）`。不要用"最后通牒"式的单独大字红色——它会让正常客户反感，也让真逾期客户麻木。

## §9 工程实现

### 9.1 数据模型（最小可用）

```json
{
  "docType": "380",
  "invoiceNumber": "INV-2026-000123",
  "issueDate": "2026-11-19",
  "dueDate": "2026-12-19",
  "currency": "EUR",
  "seller": {"name": "…", "vatId": "DE123456789", "address": "…"},
  "buyer": {"name": "…", "buyerReference": "PO-7781", "address": "…"},
  "lines": [
    {"id": "1", "description": "…", "quantity": "3", "unit": "H87",
     "unitPrice": "12.50", "priceBaseQuantity": "1", "vatRate": "19.00",
     "lineNet": "37.50"}
  ],
  "taxBreakdown": [
    {"category": "S", "rate": "19.00", "taxableAmount": "37.50", "taxAmount": "7.13"}
  ],
  "totals": {"lineNet": "37.50", "taxExclusive": "37.50",
             "taxAmount": "7.13", "taxInclusive": "44.63",
             "prepaid": "0.00", "rounding": "0.00", "payable": "44.63"}
}
```

- 金额一律存**字符串**（或十进制定点），不存浮点；JSON 里 `0.1 + 0.2` 的坑在财务数据上是事故。
- 每个金额都有唯一来源字段；渲染层只格式化，不计算。
- `docType` 用 UNCL1001 码，`unit` 用 UN/ECE Rec 20（Peppol 代码表），不要把中文单位塞进 `unit`。

### 9.2 渲染管线

```
数据库 → 领域对象（金额已定稿） → 模板（HTML） → PDF/A-3（嵌 XML） → 交付
                        └────────→ XML（CII/UBL）────────┘
```

- PDF 与 XML **从同一个领域对象**出，禁止两条链路各自拼装。
- 渲染层不得做舍入；若模板里出现 `round()`，视为缺陷。
- 打印样式与屏幕样式共享同一套 token（间距、字号），但允许打印字号更小（§7.2）。

### 9.3 可访问性（PDF 与网页）

- PDF 要打标签（tagged PDF），表格有 `th` 与 `scope`；否则读屏读出来是一串数字。
- 网页版单据的表格用真 `<table>`，不要用 div 拼；金额列给 `aria-label` 说明币种。
- 颜色不单独承载状态（WCAG 1.4.1）；红字必须同时有负号或"红字"字样。
- 下载按钮的链接文本要有单据号（"下载 INV-2026-000123"），不要全是"下载"。

## §10 法标与规范清单

| 来源 | 条款 | 一句话 | 用在哪 |
|---|---|---|---|
| Peppol BIS Billing 3.0（May 2026 Release） | BT-1 | 发票号唯一、连续、无识别方案 | §2.1 |
| 同上 | F001 / BT-2 / BT-9 | 日期 `YYYY-MM-DD`；到期日或付款条件至少一个 | §2.2 |
| 同上 | BR-CO-10/13/15/16 | 四个金额恒等式 | §3.1 |
| 同上 | R120 / R130 | 行净额公式；价格基数的单位一致 | §3.2 |
| 同上 | BR-S-08 / R053 | 按税率分组税基；只能一个税汇总 | §3.6 |
| 同上 | R051 / CL007 / BT-5 | 单币种；ISO 4217 | §4.3 |
| 同上 | UNCL5305 | 税分类码 S/Z/E/AE/K/G/O | §4.1 |
| 同上 | UNCL1001 | 发票类型 380/384/386/389/71/326；贷项 381 | §2.5 §5.5 |
| 同上 | UNCL4461 | 付款方式码（30 转账 / 58 SEPA / 49 直接借记…） | §5.4 |
| 同上 | R003 / BT-10 | 买方参考或 PO 号必须有 | §5.1 |
| FeRD ZUGFeRD/Factur-X | 混合格式、§14 Abs.4 UStG、GoBD Rz 128/131、§14b UStG | PDF/A-3 + XML 内容一致；8 年电子保存 | §6.1 |
| FeRD Order-X 1.0 | ORDER / ORDER_RESPONSE / ORDER_CHANGE | 订单确认三态 | §5.3 |
| 国家税务总局公告 2024 年第 11 号 | 第 1–9 条 | 数电票法律效力、20 位号、17 项内容、交付、额度、红冲 | §2.3 §4.4 §6.3 |
| 发票管理办法（2023 修订） | 第 3、20、21、28 条 | 发票定义与效力；不合规可拒收；如实一次性开具；存根 5 年 | §4.4 §6.3 |

## §11 反模式（20 条）

1. 把"合计"写成三个不同数（小计/合计/总额）却都不标含义。
2. 应付金额不是全页最大字，客户要拿计算器找。
3. 已开出的发票提供"编辑"按钮。
4. 作废后号码被复用。
5. 红冲单不引用原票号与原开票日。
6. 折扣写在税后，票面却按税前解释（或反之）。
7. 多税率只显示一个"税额合计"。
8. 免税票只写"税额 0"，不写分类与法定说明。
9. 一张票出现两种币种。
10. 数量为 0 的占位行留在明细里。
11. 发票号用整数存储，20 位数电票号丢精度。
12. 日期混用 `11/19/2026` 与 `2026-11-19`。
13. 报价单过期后原地改日期续用（版本与历史全乱）。
14. 订单确认页放收款二维码。
15. 多页单据只有第一页有单据号，打印后无法拼页。
16. 表格行跨页拆断，金额与描述分居两页。
17. 用红色单独表示红字/逾期，黑白打印后信息消失。
18. PDF 与 XML 分别生成，金额差一分。
19. 打印件盖章回传替代电子归档。
20. 明细行用绝对定位排版，长描述直接盖住金额列。

## §12 自检清单（20 条）

- [ ] 1. 发票号全租户唯一、连续、定宽可排序，作废号不复用。
- [ ] 2. 开票日与到期日都是 `YYYY-MM-DD`，且到期日或付款条件至少有一个。
- [ ] 3. 到期日 = 开票日 + 付款条件（段 F 跑过）。
- [ ] 4. BT-106/109/110/112/115 五数自洽，页面应付 = BT-115。
- [ ] 5. 行净额按 R120 的固定乘法顺序算，价格基数 ≠ 1 时单位一致。
- [ ] 6. 税额按税率分组计算，不逐行取整后相加。
- [ ] 7. 折扣/费用在税前处理，已付在税后减，尾差有来源。
- [ ] 8. 多税率票底部有多组小计（税基 + 税额），顺序固定。
- [ ] 9. 税分类码正确，免税/零税/反向征收各有法定文案。
- [ ] 10. 卖方税号带国家前缀，scheme 不是自由文本。
- [ ] 11. 整张票单一币种；会计币种只用于税额并标注。
- [ ] 12. 发票上有 Buyer reference 或 PO 号；客户无 PO 时填 `NA`。
- [ ] 13. 发票能回溯到报价单号与订单号，行项 ID 对齐。
- [ ] 14. 报价单号与版本分离，改价升版本并记录变更摘要。
- [ ] 15. 已开票不可编辑；红冲引用原票；作废是终态。
- [ ] 16. PDF 与 XML 同源生成；PDF 满足 PDF/A-3 且嵌入字体。
- [ ] 17. 多页单据每页有单据号、页码 `n/N`、客户名。
- [ ] 18. 行不跨页拆，合计不孤页，表头每页重复。
- [ ] 19. 黑白打印后状态、红字、合计仍可辨。
- [ ] 20. 打印实测：A4、15 mm 边距、真实打印机一次。

## §13 可跑校验代码（6 段）

每段独立可跑（`python -I -X utf8`，仅标准库），末尾打印 `段 X OK`。

### 段 A · 金额脊柱校验（BR-CO-10/13/15/16）

```python
from decimal import Decimal, ROUND_HALF_UP

D = Decimal

def r2(x):
    return D(x).quantize(D("0.01"), rounding=ROUND_HALF_UP)

def spine(lines, doc_allowance="0.00", doc_charge="0.00",
          prepaid="0.00", rounding="0.00"):
    # 行净额：数量 * (净单价 / 价格基数)，每行各自 r2
    nets = [r2(D(l["qty"]) * (D(l["price"]) / D(l.get("base", "1")))) for l in lines]
    bt106 = r2(sum(nets))
    bt109 = r2(bt106 - D(doc_allowance) + D(doc_charge))
    # 按税率分组税基与税额（BR-S-08 语义）
    groups = {}
    for l, net in zip(lines, nets):
        groups.setdefault(l["rate"], D("0")) 
        groups[l["rate"]] += net
    tax = D("0")
    for rate, base in groups.items():
        tax += r2(base * D(rate) / D("100"))
    bt110 = r2(tax)
    bt112 = r2(bt109 + bt110)
    bt115 = r2(bt112 - D(prepaid) + D(rounding))
    assert bt106 == r2(sum(nets)), "BR-CO-10"
    assert bt109 == r2(bt106 - D(doc_allowance) + D(doc_charge)), "BR-CO-13"
    assert bt112 == r2(bt109 + bt110), "BR-CO-15"
    assert bt115 == r2(bt112 - D(prepaid) + D(rounding)), "BR-CO-16"
    return {"bt106": bt106, "bt109": bt109, "bt110": bt110,
            "bt112": bt112, "bt115": bt115, "groups": groups}

lines = [
    {"qty": "3", "price": "12.50", "rate": "19"},
    {"qty": "1", "price": "99.00", "rate": "19"},
    {"qty": "2", "price": "4.20", "rate": "7"},
]
res = spine(lines, prepaid="50.00")
print(res)
assert str(res["bt115"]) == "121.43"
print("段 A OK")
```

### 段 B · 舍入差：逐行 vs 汇总

```python
from decimal import Decimal, ROUND_HALF_UP

D = Decimal

def r2(x):
    return D(x).quantize(D("0.01"), rounding=ROUND_HALF_UP)

def compare(prices, rate="19"):
    total = sum(D(p) for p in prices)
    line_tax = sum(r2(D(p) * D(rate) / D("100")) for p in prices)
    agg_tax = r2(total * D(rate) / D("100"))
    return total, r2(line_tax), agg_tax

case_a = compare(["3.99", "19.99", "0.99"])
case_b = compare(["7.49", "12.49", "5.95"])
print("A", case_a)
print("B", case_b)
assert case_a == (D("24.97"), D("4.75"), D("4.74"))
assert case_b == (D("25.93"), D("4.92"), D("4.93"))
assert case_a[1] - case_a[2] == D("0.01")
assert case_b[1] - case_b[2] == D("-0.01")
print("段 B OK")
```

### 段 C · 单据号与日期

```python
import re
from datetime import date

CN_RE = re.compile(r"^\d{20}$")

def check_cn_invoice_no(no: str, expect_year: int) -> dict:
    assert CN_RE.match(no), "数电票号必须 20 位纯数字"
    yy = no[0:2]
    assert int(yy) == expect_year % 100, "第 1-2 位是公历年度后两位"
    prov = no[2:4]
    channel = no[4]
    serial = no[5:20]
    assert len(prov) == 2 and len(serial) == 15
    return {"year": yy, "province": prov, "channel": channel, "serial": serial}

def check_date(s: str) -> str:
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", s), "必须 YYYY-MM-DD"
    y, m, d = map(int, s.split("-"))
    date(y, m, d)  # 非法日期抛 ValueError
    return s

r = check_cn_invoice_no("26110000000000012345", 2026)
print(r)
assert r["province"] == "11" and r["serial"] == "000000000012345"
assert check_date("2026-11-19") == "2026-11-19"
for bad in ["2026/11/19", "19.11.2026", "2026-02-30"]:
    try:
        check_date(bad)
    except (AssertionError, ValueError):
        pass
    else:
        raise AssertionError("应当拒绝: " + bad)
print("段 C OK")
```

### 段 D · 单据状态机

```python
ALLOWED = {
    "draft": {"issued"},
    "issued": {"sent", "void"},
    "sent": {"paid", "overdue", "credited"},
    "overdue": {"paid", "credited"},
    "paid": set(),
    "void": set(),
    "credited": set(),
}

def can_move(a: str, b: str) -> bool:
    return b in ALLOWED.get(a, set())

def move(state: str, target: str) -> str:
    if not can_move(state, target):
        raise ValueError(f"非法迁移 {state} -> {target}")
    return target

assert move("draft", "issued") == "issued"
assert move("sent", "overdue") == "overdue"
assert move("overdue", "paid") == "paid"
for a, b in [("paid", "issued"), ("void", "issued"), ("draft", "paid")]:
    assert not can_move(a, b), (a, b)
print("段 D OK")
```

### 段 E · 版式静态检查（打印 CSS 与金额列）

```python
import re

HTML = """
<html><head><style>
@page { size: A4; margin: 15mm; }
table { width: 100%; border-collapse: collapse; }
td.num { text-align: right; font-variant-numeric: tabular-nums; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
</style></head>
<body><table><thead><tr><th>Item</th><th>Amount</th></tr></thead>
<tbody><tr><td>Shoes</td><td class="num">44.63</td></tr></tbody></table></body></html>
"""

def audit(html: str) -> list:
    problems = []
    if not re.search(r"@page\s*\{[^}]*size:\s*A4", html, re.S):
        problems.append("缺 @page size: A4")
    if not re.search(r"margin:\s*\d+mm", html):
        problems.append("缺 mm 边距")
    if not re.search(r"tabular-nums", html):
        problems.append("金额列缺 tabular-nums")
    if not re.search(r"text-align:\s*right", html):
        problems.append("金额列未右对齐")
    if not re.search(r"thead\s*\{[^}]*table-header-group", html, re.S):
        problems.append("表头不会在分页处重复")
    if not re.search(r"break-inside:\s*avoid", html):
        problems.append("行可能被跨页拆断")
    return problems

problems = audit(HTML)
print("problems:", problems)
assert problems == []

bad = HTML.replace("tabular-nums", "normal")
assert "金额列缺 tabular-nums" in audit(bad)
print("段 E OK")
```

### 段 F · 付款条件与到期日

```python
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

D = Decimal

def due_date(issue: date, terms_days: int) -> str:
    return (issue + timedelta(days=terms_days)).isoformat()

def discounted(amount: str, rate: str, days: int, issue: date, term_days: int) -> dict:
    total = D(amount)
    disc = (total * D(rate) / D("100")).quantize(D("0.01"), rounding=ROUND_HALF_UP)
    return {
        "pay_by": due_date(issue, days),
        "discount": str(disc),
        "pay": str(total - disc),
        "net_due": due_date(issue, term_days),
    }

issue = date(2026, 11, 19)
assert due_date(issue, 30) == "2026-12-19"
r = discounted("1000.00", "2", 10, issue, 30)
print(r)
assert r == {"pay_by": "2026-11-29", "discount": "20.00",
             "pay": "980.00", "net_due": "2026-12-19"}
print("段 F OK")
```

## §14 取源限制

| 目标 | 状态 | 处理 |
|---|---|---|
| EUR-Lex 指令 2014/55/EU 原文 | **HTTP 202 空正文**（两个入口均失败） | 未取到条文；仅引 FeRD 对该指令的转述与 Peppol 对 VAT 指令 2006/112/EC 第 226(2) 条的转述，**不引原文** |
| VAT 指令 2006/112/EC 第 226 条 | 未取到 | 只在 BT-1 定义里转引"the sequential number required in Article 226(2)" |
| ISO 216（A4 尺寸）原文 | 付费标准，未取 | §7.1 的 210×297 mm 为标称尺寸，非逐字引文 |
| ISO 19005-3:2012（PDF/A-3）原文 | 付费标准，未取 | 只作"PDF/A-3"名称引用，不引条款 |
| Factur-X 官网 | fetch failed（TypeError: fetch failed） | 用 FeRD 页面对 Factur-X/ZUGFeRD 的说明替代 |
| FeRD 英文页 `/en/standards/zugferd` | HTTP 404 | 用德语原文页 |
| FeRD "Pflichtangaben" 明细表 | 页面只有图片，无文字 | 不引其表格内容；必填项以 Peppol 字段定义与中国公告为准 |
| 陕西税局红冲公告页 | HTTP 412（WAF） | 用 gov.cn 同名公告替代 |
| Peppol `codelist/UNCL1001/`（不带 `-inv`） | HTTP 404 | 用 `UNCL1001-inv` 与 `UNCL1001-cn` 两个子集页 |
| XPath `fn:round` 的 .5 方向定义 | 未取到 | §3.3 只陈述"乘 100、四舍五入取整、除 100"的实测形状，不裁决 .5 方向 |

**已逐字取到并可直接引用的源**

- Peppol BIS Billing 3.0（May 2026 Release）：`rules/ubl-tc434/BR-CO-10/13/15/16`、`rules/ubl-peppol/`（R003/R008/R010/R020/R040/R046/R051/R053/R120/R130/F001/CL007/DE-R-018）、`syntax/ubl-invoice/tree/`（BT-1/2/3/5/9/10/31/32）、`codelist/UNCL1001-inv/`、`codelist/UNCL1001-cn/`、`codelist/UNCL5305/`、`codelist/UNCL4461/`。
- FeRD `standards/zugferd`：混合格式、§14 Abs. 4 UStG、§14b UStG 八年、GoBD Rz 128/131、邮件只是信封、ZUGFeRD 2.5.2（2026-08-04）。
- FeRD `standards/order-x`：ORDER / ORDER_RESPONSE / ORDER_CHANGE，Order-X 1.0（2021-04-13）。
- 中国政府网：《国家税务总局关于推广应用全面数字化电子发票的公告》（2024 年第 11 号，2024-12-01 施行）第 1–9 条；《发票管理办法》（2023-07-20 第三次修订）第 3、20、21、28 条。

**时效提醒**

- Peppol 版本页标注 "May 2026 Release"；规则与代码表以该版本为准，换代需重跑 §13 段 A/B。
- 数电票公告为 2024 年发布，后续如有新公告（如全面数字化后的红冲细则）应替换引用。
- ZUGFeRD 2.5.2 为 2026-08-04 版本；模板与校验器应记录该版本号。
