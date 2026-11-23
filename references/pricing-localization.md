# 定价本地化（Pricing Localization）：币种、含税口径、地区价差与法定原价

> 适用：同一个价格卖到多个国家/地区时的**显示与计算口径**——币种小数位、含税还是不含税、税额怎么反算、地区价差怎么定、"原价"能不能随便写、单位价格要不要标、尾数与格式怎么落。
> 不适用：一国之内的定价页结构、结账流程、心理定价与推荐档（那些在 `pricing-checkout.md`）；纯数字/货币**格式排队**（`Intl.NumberFormat` 的 locale 分组规则）在 `i18n-localization.md` §十——本文只补"价格作为商业数字怎么定、怎么标、怎么算"。

---

## §0 一句话立场

**价格不是一个数字，是一个三元组 `(金额, 币种, 含税口径)`；少任何一元，这个价格就是错的。** 设计能决定的是这三元的**展示归属与时机**（哪个页面、哪一行、什么时候变），不能决定的是三元的**取值**（小数位由 ISO 4217 定、含税口径由销售地法规定、"原价"由法定回溯窗口定）。凡是设计师在稿子上写"9.9/月"，落地时必须补三个字段：哪个币种、含几位小数、含不含税——没补就是交付缺陷。

---

## §1 判层：先问七个问题，再动手

本地化定价出问题，九成是**没先判定自己落在哪一层**就画界面。开工前把七问答完，答不出的一律回退到"只显示一个市场"。

| # | 问题 | 答"是"→去哪一节 | 答"否"→ |
|---|---|---|---|
| 1 | 目标市场 ≥ 2 个，且币种不同？ | §2 币种与最小单位 → §9 多币种工程 | 单市场：只需 §3 含税口径 + §6 原价 |
| 2 | 展示币种 ≠ 平台结算/收款币种？ | §9（必须显式告知换汇与手续费） | 跳过 §9 |
| 3 | 该市场法规要求**含税标价**（EU/UK/JP/CN 消费者侧）？ | §3 → §10 法标清单 | 美国/加拿大：标不含税，结账加税，见 §3 |
| 4 | 有划线价/折扣/"省 X%"？ | §6 法定回溯窗口（硬红线） | 跳过 §6 |
| 5 | 有按重量/体积/长度售卖的商品？ | §7 单位价格（DE 是义务） | 跳过 §7 |
| 6 | 该币种小数位 ≠ 2？ | §2（JPY/KRW/VND/ISK 0 位；KWD 等 3 位） | 仍需 §8 格式 |
| 7 | 价格会随汇率重新定价？ | §5 价格点 → §9 FX 缓冲 | 跳过 §5 |

**四类构型**（先定型，再谈尺寸）：

| 构型 | 特征 | 典型 | 本文重点 |
|---|---|---|---|
| A 单币种单市场含税 | 一个价格，含税显示 | 日本电商、欧盟本土店 | §3、§6、§10 |
| B 多币种展示、单地结算 | 前端切币，后端一处收款 | 独立开发者 SaaS | §9、§5 |
| C 多市场本地主体 | 每市场独立税率/独立价目表 | 电商、订阅 | §3、§6、§7、§10 |
| D 平台内分发 | 价格点在平台定价工具里选 | App Store / Play | §5、§9 |

---

## §2 币种与最小单位：价格是"金额+币种+小数位"

### 2.1 小数位不是设计偏好，是 ISO 4217 的数据

ISO 4217 官方清单由 SIX 发布（本轮实测 `List One`，文件头 `<ISO_4217 Pblshd="2026-09-17">`），每个币种在 `<CcyMnrUnts>` 里给出"最小单位位数"。逐字样例：

> `<Ccy>JPY</Ccy><CcyNbr>392</CcyNbr><CcyMnrUnts>0</CcyMnrUnts>`

本轮实测取值（可直接照抄进代码常量）：

| 位数 | 币种（实测命中） |
|---|---|
| 0 | JPY（日元）、KRW（韩元）、VND（越南盾）、ISK（冰岛克朗）、XOF（西非法郎） |
| 2 | EUR、USD、HUF、TWD、IDR |
| 3 | KWD（科威特第纳尔）、BHD（巴林第纳尔）、JOD（约旦第纳尔）、OMR（阿曼里亚尔）、TND（突尼斯第纳尔） |
| 4 | CLF（智利发展单位）、UYW（乌拉圭工资指数单位） |
| `N.A.` | XDR（特别提款权）——**不是可结算货币**，不得出现在价格 UI |

设计后果，逐条可执行：

- **`¥1,234.50` 在日元下不存在**。写两位小数就是伪造精度。同理 `₩12,000.00`、`₫250,000.00` 都错。
- **3 位小数币种的价格列要多留 1 位**：`KWD 12.345` 比 `USD 12.34` 宽一个数字位（约 0.55–0.6em），列宽按 `min-width` 预留，不要靠 `width: auto` 让布局自己抖。
- **价目表用整数最小单位存储**（USD 存 999 表示 9.99；JPY 存 500 表示 500），展示层才乘小数位。用浮点存钱，`0.1+0.2 != 0.3` 会在第 7 件商品上暴露。
- **币种代码必须是大写三字母**；同一页面上符号与代码不得混用（`€` 与 `EUR` 二选一，按 §8 的规则选）。

### 2.2 `Intl.NumberFormat` 的四个显示开关（MDN 原文）

> "The currency to use in currency formatting. Possible values are the ISO 4217 currency codes, such as `"USD"` for the US dollar, `"EUR"` for the euro, or `"CNY"` for the Chinese RMB"

`currencyDisplay` 四档，逐字：

> "`"code"` Use the ISO currency code." / "`"symbol"` (default) Use a localized currency symbol such as €." / `"narrowSymbol"` Use a narrow format symbol ("$100" rather than "US$100")." / `"name"` Use a localized currency name such as `"dollar"`."

选择规则（可直接当评审口径）：

| 场景 | 用哪档 | 理由 |
|---|---|---|
| 单市场、符号无歧义（日本站的 ¥） | `symbol`（默认） | 最省宽度 |
| 多币种并列（切币器、价目表） | `code` 或 `symbol` + 明确市场标签 | `$` 一个符号对应 USD/CAD/AUD/HKD/SGD 至少 5 个币种，`narrowSymbol` 会把 `US$100` 收窄成 `$100`，**多市场页面禁用 `narrowSymbol`** |
| 报价单、发票、B2B | `code` | 法律与财务可审计 |
| 读屏长句（"每月九点九九美元"） | `name` | 只有纯文本场景用，别用在紧凑表格里 |

`currencySign` 逐字（MDN）：

> "In many locales, accounting format means to wrap the number with parentheses instead of appending a minus sign. Possible values are `"standard"` and `"accounting"`; the default is `"standard"`."

**退款、折扣、冲正金额**用 `accounting`：`(€12.34)` 而不是 `-€12.34`——财务表格里负号会被误读成连字符，括号是国际会计惯例。消费者页面（"已省 €12.34"）仍用 `standard`，别在营销位放括号。

MDN 示例注释里那句 **"// The Japanese yen doesn't use a minor unit"** 是本节的全部证据：环境自己知道 JPY 没有小数位，所以**不要自己拼 `toFixed(2)`**。

---

## §3 含税口径：三种世界，三套写法

同一件 9.99 的商品，在三个市场必须写三个样子：

| 市场 | 法定标价口径 | 9.99 怎么写 | 税额什么时候出现 |
|---|---|---|---|
| 欧盟 / 英国 | **含税**（B2C 明示总价） | `€9.99`（已含 19%/20% VAT） | 结账展开明细，或标注"含税" |
| 日本 | **含税（総額表示）** | `9.99` 不成立，须 `¥1,100（税込）` 这类整数含税价 | 发票/明细里给税额 |
| 中国 | **含税**（人民币金额） | `¥99.00` | 明细 |
| 美国 / 加拿大 | **不含税**（税后加到结账） | `$9.99` + `plus tax` | 结账页按 ZIP/州算税 |

### 3.1 欧盟：标准税率下限 15%，减税率下限 5%（欧盟委员会原文）

> "This is the rate EU countries must apply when supplying most goods and services. It must be no less than 15%, but there is no maximum (Art.97 VAT Directive)."

> "up to two reduced rates as low as 5% to the supply of goods and services in up to 24 categories included in Annex III of the VAT Directive (Art.98(1) VAT Directive)"

> "In the EU, the VAT Directive sets the general framework for VAT rates. Within this framework, it is up to each Member State to set the number and level of its VAT rates…"

设计含义：**不存在"欧盟税率"这个数**。欧盟只给框架（标准 ≥15%，最多两档减税 ≥5%，另有超减税率与零税率最多 7 类基本需求品），具体数字由成员国定。所以设计稿里写"EU VAT 20%"就是把英国税率当成了欧盟税率——**按成员国分别建价目表，不要建"EU 价目表"**。

### 3.2 德国：19% / 7% / 0%（UStG §12 原文）

> "Die Steuer beträgt für jeden steuerpflichtigen Umsatz 19 Prozent der Bemessungsgrundlage (§§ 10, 11, 25 Abs. 3 und § 25a Abs. 3 und 4)."

> §12(2) "Die Steuer ermäßigt sich auf sieben Prozent für die folgenden Umsätze:"

> §12(3) "Die Steuer ermäßigt sich auf 0 Prozent für die folgenden Umsätze:"（Solarmodule 等）

德国"总价"（Gesamtpreis）的法定定义，PAngV §2(3) 逐字：

> „Gesamtpreis" den Preis, der einschließlich der Umsatzsteuer und sonstiger Preisbestandteile für eine Ware oder eine Leistung zu zahlen ist.

即：**德国 B2C 展示的主价格必须是含增值税的最终应付额**。设计上"价格 + 小字 19% VAT"这种拆开写法，只有在税额另标且总价清晰时才成立；把税藏在结账的写法在德国直接违法。

### 3.3 英国：20% / 5% / 0%

> "The standard VAT rate is 20%"

页内表格原文：`Standard rate | 20% | Most goods and services`、`Reduced rate | 5% | Some goods and services, for example, children's car seats and home energy`、`Zero rate | 0% | Zero-rated goods and services, for example, most food and children's clothes`。

> "The standard rate of VAT increased to 20% on 4 January 2011 (from 17.5%)."

### 3.4 日本：総額表示是义务（消法 63）

国税庁 No.6902 逐字：

> 「総額表示義務とは、事業者が消費者に対してあらかじめ価格を表示する場合に、消費税額（地方消費税額を含む。）を含めた価格（税込価格）を表示することを義務付けるものです。」

> 「総額表示の義務付けは、事業者が消費者に対してあらかじめ表示する価格が対象となります。したがって、価格を表示していない場合にまで、税込価格の表示を義務付けるものではありません。」

消费税率（No.6101 原文）：

> 「標準税率10パーセント（うち2.2パーセントは地方消費税）、軽減税率8パーセント（うち1.76パーセントは地方消費税）」

设计含义三条：

1. **"あらかじめ価格を表示する場合"才触发义务**——商品列表、详情页、广告位、落地页主价全部算"预先显示"；只在结账才显示的"总价"不算免责。
2. 含税价必须能**独立读懂**：`¥1,100` 旁边若写"税抜 ¥1,000"，两者并列时被比较/强调的主体必须是税込价。
3. **2027-04-01 前的税率变动已在官方口径里预告**："令和9年4月1日から令和11年3月31日までの2年間、飲食料品の譲渡について、消費税率が引き下げられます。"（令和 9 年 = 2027 年）——价目表与文案里的"8%"必须在设计系统里做成**变量**，不能出现硬编码的税率字符串。

### 3.5 中国：人民币金额 + 明码标价

《明码标价和禁止价格欺诈规定》（市场监管总局令第 56 号）逐字：

> 第七条 经营者销售商品应当标示商品的品名、价格和计价单位。

> 第八条 不得在标价之外加价出售商品或者提供服务，不得收取任何未予标明的费用。

> 第九条 经营者标示价格，一般应当使用阿拉伯数字标明人民币金额。

> 第二十条 经营者不得实施下列价格欺诈行为：（一）在首页或者其他显著位置标示的商品或者服务价格低于在详情页面标示的价格；（二）公布的促销活动范围、规则与实际促销活动范围、规则不一致……

第二十条(一) 是本轮**最可执行的跨页一致性硬规则**：**首页价 ≤ 详情价**。多币种站点把它通用化就是——同一商品在列表页、详情页、购物车、结账四处出现的价格（含币种与含税口径）必须同源渲染；任何一处"为了好看"手工压低价格，在中国是价格欺诈，在其他市场是信任崩塌。

### 3.6 美国：标不含税，但"总价"仍受 FTC 约束

美国零售商习惯标 `$9.99` 不含销售税，结账才加。注意这不是"可以不告诉用户总价"——FTC 的 total price 规则要求广告里能算出最终应付额（`pricing-checkout.md` §4 已详述）。多市场设计时最容易犯的错：**把美国的不含税写法直接套到欧盟/日本站**，导致含税价看起来贵 20% 而用户结账发现没变——两边的信任都掉。

---

## §4 税额反算与取整：四种取整位置，一种记账方式

含税价已知、税率已知时，**税额不是乘出来的，是反算出来的**：

```
税额 = 含税价 × r / (1 + r)      （r = 税率，如 0.19）
净额 = 含税价 − 税额
```

为什么不能 `净额 × (1+r)`：净额若先取整，含税价就会差 1 分，用户看到的价和收单价对不上。

### 4.1 取整位置决定会不会差 1 分

| 取整位置 | 做法 | 风险 |
|---|---|---|
| 逐行取整后汇总 | 每行 `split_tax()` 取到最小单位，再加总 | 各行舍入误差累积，汇总与"总价×税率"对不上 |
| 汇总后取整 | 先加总含税，再整体反算 | 行明细相加 ≠ 总税额（明细差 1 分） |
| **逐行取整 + 差额记账**（推荐） | 逐行反算取整，与发票总额的差额单独记一行 | 明细自洽，总额自洽，差额可审计 |
| 不做取整（保留全精度） | 全精度累加，只在显示时取整 | 数据库里出现 0.005 级金额，对账地狱 |

### 4.2 Stripe 的官方处理方式（照抄这个思路）

> "For invoices where the `amount` is fractional after prorations, coupons, or taxes, Stripe automatically rounds that amount to the nearest number evenly divisible by 100. We credit or debit any difference from rounding to the customer balance."

注意三个细节，设计稿要能表达它们：

1. **取整是"就近取到 100 的整数倍"**（两位小数币种里 100 个最小单位 = 1 个主单位），不是"向下抹零"。
2. **差额不丢，记到客户余额**（credit 或 debit）——所以 UI 上可能需要一行"舍入调整 ±€0.01"。
3. 这条只针对"invoice 的 amount 变成分数"的情形，不要把它当成"所有金额都可以随便取整"。

### 4.3 最小收款额的坑

> "Stripe enforces a minimum payment amount for all charges to make sure the Stripe fee doesn't exceed your charge. The minimum amount you can charge depends on the payout bank account settlement currency."

本轮实测原文数值（照录，单位与小数位保留原样）：`0.50 USD`、`0.30 GBP`、`0.50 EUR`、`0.50 AUD`、`0.50 CAD`、`0.50 CHF`、`4.00 HKD`、`50 JPY`、`50 KRW`、`0.50 SGD`、`0.50 INR`、`2.00 AED`、`2.00 MYR`、`10 MXN`、`10 THB`、`15.00 CZK`、`175.00 HUF`、`2.50 DKK`、`3.00 NOK`、`2.00 PLN`、`2.00 RON`、`3.00 SEK`、`0.50 ZAR`。

设计含义：**最低收款额按"结算币种"算，不按"展示币种"算**：

> "For example, if you have GBP and USD bank accounts, with GBP set as your default currency, any non-USD charges you create convert to GBP. These charges must meet the minimum amount required for GBP after conversion."

所以当你在印度站标 `₹9`（≈0.11 USD）这种低价试用档时，结算是按 GBP 判定的，**0.30 GBP 的门槛会把整笔拒掉**。低价市场（印度、东南亚、拉美）的试用价必须先在结算币种下过一遍最小额校验，再决定展示价——不是设计师在稿子上写 9 就完事。

### 4.4 零小数币种的特殊写法

> "Enter 10 to charge 10 JPY (or any other zero-decimal currency)"

> "ISK transitioned to a zero-decimal currency, but backward compatibility requires you to represent it as a two-decimal value, where the decimal amount is always `00`."

冰岛克朗是"法定 0 位、API 仍要两位且必须是 `.00`"的活例子：**展示层 0 位、传输层 2 位、两者不是一个数**。设计系统里价格组件的 props 不能只写 `{amount, currency}`，至少要能表达"显示位数"与"传输位数"两个值，否则 ISK 这类币种一定写错。

---

## §5 地区定价：三种体系，选一种并写进设计系统

| 体系 | 定价依据 | 优点 | 代价 |
|---|---|---|---|
| 成本加成 + 汇率 | 成本 → 目标毛利 → 按汇率折算 → 缓冲 | 保毛利，简单 | 富市场显得便宜、穷市场显得贵，转化差 |
| 购买力/区域价（PPP） | 按市场支付能力分档 | 转化好 | 需要防套利（跨区购买、代购） |
| 平台价格点 | 在平台给定价格点里选 | 结算合规、税率平台代收 | 自由度受限，价格点会变 |

### 5.1 Apple App Store 的价格点（官方原文）

> "Apps with auto-renewable subscriptions can choose from 800 price points across all available currencies and price tiers, with an additional 100 higher price points available upon request."

> "The App Store Connect pricing tool can help you manage pricing based on current exchange rates."

> "If there's a tax change or currency adjustment in a particular region, the price of subscriptions won't generally be affected unless you decide to pass the change on to your users."

> "The default pricing in the App Store Connect pricing tool is inclusive of applicable taxes that Apple collects and remits."

> 德国例："…the revenue you'll receive will be the purchase price minus the European Union's value added tax (VAT) and minus Apple's commission."

设计后果（很具体）：

- **800 + 100 个价格点**意味着平台内不存在"任意定价"——设计价目表时是"挑点"，不是"算数"。
- **默认价含税**：德国站显示 €9.99 时，你的收入是 9.99 减 VAT 减佣金，不是 9.99 减佣金。做收入测算 UI 时必须先除法再减佣金。
- **汇率/税率变化默认不传导给用户**："won't generally be affected unless you decide to pass the change on"——所以"自动跟随汇率"不是默认行为，是需要显式开关的产品决策；设计稿里那个"汇率自动同步"的开关，文案必须写清"开启后部分地区价格会上涨"。

### 5.2 自建站：FX 缓冲与价格点三段式

自建多币种站的可执行流程（附录段 D 实现）：

1. `目标价 = 成本 / (1 − 目标毛利率) × 汇率 × (1 + FX 缓冲)`
2. FX 缓冲取 **2%–5%**（覆盖结算周期内的汇率波动与换汇费；低于 2% 会在汇率跳一下时吃掉毛利，高于 5% 会让富市场明显贵于竞品）
3. 再套价格点：两位小数币种取 `x.99`，零小数币种取 **10 的整数倍**（日本站 `¥2,580` 而不是 `¥2,577`）
4. 每次重算都要**校验毛利下限**，跌破就打回人工

**价格点不是审美，是换算保护**：日元没有小数位，`2,577` 这种数字在日站看起来像没定完价；而 `x.99` 在日元下根本表达不出来（`¥2,577.99` 不存在）。

---

## §6 「原价」不是设计自由度：法定回溯期对照（DE / CN / JP）

这是本轮**第一条硬红线**：划线价、`-30%`、`省 €20` 里的那个"原价"，在多数市场是**有法定计算期间的**，不是文案可以挑的数字。

| 市场 | 法定窗口 | 原价必须等于 | 逐字依据 |
|---|---|---|---|
| 德国（PAngV §11(1)） | **降价前 30 天** | 该 30 天内曾向消费者适用的**最低总价** | "…den niedrigsten Gesamtpreis anzugeben, den er innerhalb der letzten 30 Tage vor der Anwendung der Preisermäßigung gegenüber Verbrauchern angewendet hat" |
| 中国（56 号令 第十六条） | **前 7 日** | 同一经营场所前 7 日内**最低成交价**；7 日内无交易则用最后一次交易价 | "被比较价格应当不高于该经营者在同一经营场所进行价格比较前七日内的最低成交价格；前七日内没有交易的，应当不高于本次价格比较前最后一次交易价格。" |
| 日本（CAA 二重価格表示） | **8 周内**，且该价售卖期占**过半**、累计**≥2 周**、最后售卖日距展示日**未满 2 周** | 满足三条才算"最近相当期间にわたって販売していた価格"，才能当比较对照价 | "…8週間において、当該価格で販売されていた期間が、当該商品が販売されていた期間の過半を占め、2当該価格での販売期間が通算で2週間以上であり、3当該価格で販売された最後の日から2週間経過していなければ…" |

三条配套禁令，同样逐字：

- 德国 PAngV §11(2)：**逐步降价可以继续以"降价前最低价"为基准**，不允许在每轮降价时把基准一起往下挪。
- 中国 第十七条："经营者没有合理理由，不得在折价、减价前临时显著提高标示价格并作为折价、减价计算基准。"（先提价再打折 = 价格欺诈）
- 中国 第十六条后段："与厂商建议零售价进行价格比较的，应当明确标示被比较价格为厂商建议零售价。"（拿 MSRP 当"原价"必须标注 MSRP，不能装作历史成交价）

两条豁免（德国 PAngV §11(4) 原文指向）：**个性化降价**（"individuellen Preisermäßigungen"，如会员券）与**易腐商品**（"schnell verderbliche Waren"）不适用 30 日窗口。

中国 第二十一条还有一条"不算欺诈"的出口，设计上要会用：

> "（三）成交结算后，实际折价、减价幅度与标示幅度不完全一致，但符合舍零取整等交易习惯。"（不属价格欺诈）

——意思是**因舍零取整导致的几分钱差异是允许的**，但"标 -30% 实际 -25%"不属于舍零。

**6.1 设计层落法（可直接实施）**

1. **划线价旁边必须有来源标签**：`原价` / `近 30 天最低价` / `厂商建议零售价` 三选一，按 §10 选市场对应说法；空白标签的划线价在德/中/日三地都是风险项。
2. **折扣率由系统算，不由文案填**：`discount = 1 − 现价/原价`，四舍五入到整数百分比；`9.99 → 7.49` 是 **25%** 不是 30%——文案写死百分比是本轮最常见的落地事故。
3. **禁止"倒计时 + 原价"组合拳**在德语区：触发 PAngV §11 的 30 日回溯，并踩 UCPD Annex I 第 7 类紧迫感条款（EUR-Lex 2026-11-20 仍 202 空正文，逐字未取到，标「未验证」，见 §14）。不依赖法条也可判：倒计时须可暂停 / 隐藏，见 `pricing-checkout.md` §4 纪律四。
4. **MSRP 场景要显式**：`建议零售价 ¥1,980`，不要只画一条线。

---

## §7 单位价格：按量计价是义务，不是装饰

德国 PAngV §4(1) 逐字：

> „…hat neben dem Gesamtpreis auch den Grundpreis unmissverständlich, klar erkennbar und gut lesbar anzugeben. Auf die Angabe des Grundpreises kann verzichtet werden, wenn dieser mit dem Gesamtpreis identisch ist."

即：**总价之外还要给"基准价"**（每 kg / 每 L / 每 m 的价格），清晰可读。仅当基准价与总价相同（如 1 kg 装标 1 kg 价）可省。

豁免（§4(3) 8 类，含逐字）：

> "Waren, die über ein Nenngewicht oder Nennvolumen von weniger als 10 Gramm oder 10 Milliliter verfügen"

——**净含量小于 10 g 或 10 ml 的商品可免标基准价**。

设计规格（可直接进组件）：

| 元素 | 规格 | 说明 |
|---|---|---|
| 基准价位置 | 主价**下一行**，间距 4–8px | 不放价格右侧（会撑宽商品卡） |
| 基准价字号 | 主价的 0.7–0.78 倍（主价 40px → 基准价 12–13px 偏小，电商卡主价 24px 时取 15–16px 更稳） | 与主价形成层级但不抢 |
| 基准价颜色 | 次要文本色（对比度仍需 ≥4.5:1） | 它是法律信息，不能为了弱化而降到 3:1 以下 |
| 单位写法 | `€9.96 / 1 kg`、`€2.65 / 1 L` | 斜杠 + 空格 + 数字 + 单位，别写 `9.96€/kg` |
| 换算基数 | 重量按 **1 kg**、体积按 **1 L**、长度按 **1 m** | 德国惯例；欧盟各国大体一致，个别国另有基数 |

电商卡里最容易被砍的就是这一行——砍掉在德国属违反 PAngV，不是"信息密度取舍"。

---

## §8 尾数与数字格式：符号、分组、空格、括号

### 8.1 格式层（`i18n-localization.md` §十 已给 locale 分组规则，这里只补价格专属项）

| 项 | 规则 | 反例 |
|---|---|---|
| 货币符号位置 | 由 locale 决定：`en-US → €1,234.50`（符号前）、`de-DE → 1.234,50 €`（符号后 + NBSP） | 全站统一把符号放前面 |
| 小数分隔符 | `en` 系用 `.`，`de/fr/es/it` 系用 `,` | 用 `.` 硬拼德语价 |
| 千分位 | `en` 系 `,`，`de` 系 `.`，`fr` 系 NBSP，`hi-IN` 3-2-2 分组 | 手写正则加逗号 |
| 数字与符号之间 | `de-DE` 与 ISO 写法要求 NBSP（U+00A0），不是普通空格 | 普通空格在换行处会把 `€` 和数字拆开 |
| 负数 | 财务场景 `accounting`（括号），营销场景 `standard` | 全站混用 |

### 8.2 尾数（charm pricing）的文化边界

- **`x.99` 不是普世最优**：日本、韩国电商大量使用整数价（`¥1,980`、`₩19,000`），`.99` 反而显得廉价；德国/奥地利对 `9.99` 接受度高；中国偏好整数或 `x8`/`x9` 尾数。
- **零小数币种不能有尾数**：`¥1,999` 是整日元，`¥1,999.99` 不存在。
- **3 位小数币种慎用尾数**：`KWD 12.345` 的"尾数"是第三位小数，视觉上很弱，通常直接取整到 `0.005` 的倍数。
- **同一市场内尾数风格要统一**：价目表里混着 `9.99 / 10.00 / 9.5` 会被读成"定价没做完"。

### 8.3 价格排版的尺寸（沿用 `pricing-checkout.md` §3，不重复推导）

主价 40–48px、`font-variant-numeric: tabular-nums`、货币符号 0.5em 且上移 0.13em、价格差异 ≤20% 时不加额外强调。**本地化新增两条**：

1. **整数部分对齐**：多币种价格列右对齐 + `tabular-nums`，否则 `€9.99` 与 `₩12,000` 的小数点/个位不在一条竖线上。
2. **符号列宽按币种最大值预留**：同一列里混 `€`（1 字符）与 `CHF`（3 字母代码）时，符号槽宽取最长者，避免每行错位。

---

## §9 多币种工程：price book、FX 缓冲、结算币种

### 9.1 数据结构：price book 是三层，不是一层

```
product
  └─ market (country/region)          # 决定税率、法定标价口径、价格点体系
       └─ price entry                  # {amount_minor, currency, tax_posture, valid_from}
```

设计评审要看的三件事：

1. **每个 market 有自己的 `currency` 与 `tax_posture`**（`inclusive` / `exclusive`），不是全局一个开关。
2. **每个 price entry 有 `valid_from`**——"原价"的 30 日/7 日窗口靠它算，没有时间戳就无法审计。
3. **币种切换不改变 market**：德国用户看 USD 只是"展示币种"变了，含税口径仍是 DE 含税（19%），结算币种仍可能是 EUR。这三者必须分开建模。

### 9.2 展示币种 ≠ 结算币种时的三条 UI 义务

1. **显式告知**：结账页展示"将以 EUR 结算，发卡行可能收取换汇费"。
2. **锁定汇率与锁定时间**：展示价一旦进入结账，汇率与金额在本次会话内不变；下单后重新换算会导致"看到的 9.99 收到 10.12"。
3. **展示价不得高于结算价**：向上取整的方向只能落在商户承担的差额上（吸收），否则属第八条"标价之外加价"的同类问题。

### 9.3 免运费门槛、优惠券、阶梯价都要跟着币种走

`满 $50 免运费` 是多币种站最典型的断裂点：€ 站用户永远达不到 `$50`（因为展示的是 €）。规则：

- 门槛存**最小单位整数 + 基准币种**，展示时按当天 FX 换算并向上取到价格点（`满 €50 免运费`，不是 `满 €45.87`）。
- 优惠券面额、阶梯折扣档位同理：**按市场建表**，不要用一张 USD 表换算。
- 换币后**购物车金额必须即时重算**，不能等到结账。

### 9.4 汇率数据的工程约束（设计要能提需求）

- 汇率记录必须带 `updated_at` 与 `source`；UI 上"价格约合"类文案要有"汇率更新于 …"的落点。
- 汇率刷新频率与价格点重算频率**分开**：汇率可以每天刷，价格点改动必须走审批（改动会改所有市场的展示价）。
- **价格点改动要有 diff 视图**：老价 → 新价 → 毛利率，逐市场列出，这本身就是一张设计要画的表。

---

## §10 法标清单：按市场查表

产出前按下表核对该市场要出现的信息。**"要不要标"不是偏好，是市场决定的。**

| 市场 | 必须出现 | 位置 | 依据 |
|---|---|---|---|
| EU 消费者 | 含税总价；适用时单位价格 | 主价即含税；单位价在下一行 | 成员国转写（见 §3.1、§14） |
| 德国 | 含税总价 + Grundpreis（≥10g/10ml 时）+ 30 日最低价（打折时） | 主价 / 价格下一行 / 划线价旁 | PAngV §2(3)、§4(1)、§11(1) |
| 英国 | 含税（20%/5%/0%） | 主价即含税 | GOV.UK VAT rates |
| 日本 | 税込总价（総額表示）；二重価格的真实性 | 主价必须含税 | 消法 63；CAA Q18/Q21 |
| 中国 | 品名 + 价格 + 计价单位；人民币金额；前 7 日最低价（比较价） | 主价 / 划线价旁 | 56 号令 第七条、第九条、第十六条 |
| 美国 | 可算出最终应付额（total price） | 广告/价格块内 | FTC total price（详见 `pricing-checkout.md` §4） |
| App Store 分发 | 价格点选择；含税默认 | 平台定价工具 | Apple 官方页（§5.1） |

**税额明细的呈现时机**：B2C 含税市场里，税额是"可展开的明细"而不是"主价旁的小字"；B2B/发票必须逐行给净额、税率、税额三列。

---
## §11 反模式（原 20 条已并入 §12 自检）

> v60 合并：原「反模式 20 条」与 §12「自检 20 条」逐条镜像（1↔1、8↔14、14↔3、19↔20…），留两张只会漂移。打回一律看 §12；促销前临时抬价的法条见 §6。只剩三条属整体做法、不是单点检查：

1. 全站一套价格写死，只在文案里把 `$` 换成 `€`。
2. 汇率写死在前端常量，无 `updated_at`、无来源。
3. 尾数或门槛跨市场硬搬（日本站 `9.99`、`满 $50` 搬 € 站）。

---

## §12 自检 20 条（原「反模式 20 条」已并入此表）

- [ ] 1. 每个价格都能回答"哪个币种、几位小数、含不含税"三元。
- [ ] 2. 零小数币种页面里搜不到 `,00`/`,50` 这类小数尾巴。
- [ ] 3. 三位小数币种的价格列宽度能容下多一位数字，不换行不截断。
- [ ] 4. 金额存储用最小单位整数，展示层才套小数位。
- [ ] 5. 多币种并列处用 `code` 或明确市场标签，**没有**用 `narrowSymbol` 把 `US$` 收窄成 `$`。
- [ ] 6. 负数金额在财务场景用 `accounting`（括号）。
- [ ] 7. 含税市场的主价是含税价，且"含税"标识出现在价格块内（不是页脚）。
- [ ] 8. 税额由含税价反算（`×r/(1+r)`），不是净额乘出来的。
- [ ] 9. 取整位置明确写成"逐行取整 + 差额记账"，或明确声明"汇总取整"。
- [ ] 10. 有"舍入调整"金额时，UI 有落点（一行明细或余额说明）。
- [ ] 11. 最低收款额按**结算币种**校验过低价档（尤其印度/东南亚/拉美）。
- [ ] 12. 划线价旁有来源标签（原价 / 近 30 天最低价 / MSRP）。
- [ ] 13. 折扣率是算出来的，不是填出来的；抽查一个商品手算对齐。
- [ ] 14. 打折商品能回答"这个原价在过去 30 天/7 天内真的卖过吗"。
- [ ] 15. ≥10g/10ml 的按量商品有单位价格，且位置在价格下一行。
- [ ] 16. 单位价格的换算基数是 1kg / 1L / 1m，写法 `€9.96 / 1 kg`。
- [ ] 17. 同一市场内尾数风格统一，没有混排。
- [ ] 18. 币种切换不改变税率与含税口径；切换后购物车即时重算。
- [ ] 19. 展示币种 ≠ 结算币种时，结账页有换汇与手续费告知，且金额在会话内锁定。
- [ ] 20. 免运费门槛、优惠券、阶梯价按市场建表，不是一张 USD 表换算。

---

## §13 工程细节：可跑校验代码（附录）

六段校验代码整体迁出正文 → `references/appendix/pricing-localization-code.md`（段 A–F，`python -I -X utf8 <file>` 可单跑，只用标准库）。

**何时必须跑**：评审抽查 §12 第 4、8、9、14、15 条时把对应段拷出来跑，不靠嘴对；改价、改税、改汇率口径后跑 A–C 验算。正文只留判断与自检，不留实现。

---

## §14 取源限制（本轮实测，未取到的一律不臆造）

| 目标 | 状态 | 处理 |
|---|---|---|
| EUR-Lex 指令 98/6/EC（价格标示）、2019/2161（Omnibus，prior price）、2018/302（Geo-blocking） | **HTTP 202 空正文**，`/TXT/HTML/`、`/TXT/PDF/`、`/eli/…/oj/eng` 变体同样 202 空；legislation.gov.uk 的 2019/2161 副本亦为 202 空 | 不引 EU 条文原文；EU 侧改引**成员国转写本**（德国 UStG §12、PAngV §2(3)/§4/§11；日本 消法 63 与 CAA Q18/Q21；中国 56 号令），并在 §3/§6/§7 逐条注明依据归属 |
| iso.org `iso-4217-currency-codes.html` | **HTTP 403**（Cloudflare "Just a moment..." 挑战） | 改用 ISO 4217 官方维护机构 SIX 发布的 `list-one.xml`（`Pblshd="2026-09-17"`）取 `<CcyMnrUnts>` |
| `docs.stripe.com/currencies`（HTML） | HTTP 200 但正文被截断（仅剩标题） | 改用同站 `.md` 版本取全文 |
| `developer.apple.com/help/app-store-connect/manage-app-pricing/` | HTTP 200 但正文为 "Page Not Found - Apple Developer"；`/set-a-price` 变体 200 但正文被巨型导航截断 | 改用 `developer.apple.com/app-store/subscriptions/` 取价格点、含税默认、汇率传导三段原文 |
| Google Play 开发者价格区间页 | `TypeError: fetch failed`（网络层不可达，加 `?hl=en`/`?hl=ja` 重试同样失败） | 不写 Play 价格区间数值；§5.1 只保留 Apple 的 800+100 价格点 |
| 印度 Legal Metrology（MRP 声明） | `fetch failed`（https/http 均不可达） | 不写 MRP 条文；印度市场在本轮仅作为"低价市场 + 结算币种最小额"案例出现，不作法规断言 |
| 日本 CAA 総額表示专页（`…/fair_labeling/price/`、`…/representation/consumption_tax/`） | 404 | 改引 CAA FAQ Q18 与国税庁 No.6902 原文 |
| EU 不公平商业行为指令（紧迫感/虚假紧迫）原文 | 未取（EUR-Lex 202） | §6.1 第 3 条只写"触发风险"，不引条文编号与原文 |

**已逐字取到并可直接引用的源**：SIX ISO 4217 List One、Stripe `currencies.md`、MDN `Intl.NumberFormat`、欧盟委员会 VAT rates 页、GOV.UK VAT rates、德国 UStG §12、德国 PAngV §2/§4/§11、日本国税庁 No.6902 与 No.6101、日本 CAA 表示規約 FAQ Q18/Q21、中国市场监管总局令第 56 号、Apple `app-store/subscriptions`。

**时效提醒**：日本消费税率已有官方预告的减免窗口（令和 9 年 4 月 1 日–令和 11 年 3 月 31 日，饮食料品），价目表与文案里的税率必须是变量；ISO 4217 清单的 `Pblshd` 日期须随抓取更新，小数位变动极少但非零。
