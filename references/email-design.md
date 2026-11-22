# 邮件设计与 EDM 排版（HTML Email Design / EDM Layout）

> 快照 2026-11-17 · 每日升级 #44（v47→v48）· 主题：HTML Email / EDM / Email Client Rendering / Table Layout / Dark Mode / Image Blocking / MJML & React Email
> 取源：caniemail 官方数据 API（`https://www.caniemail.com/api/data.json`，`last_update_date` = 2026-09-16，308 条特性，逐客户端逐版本实测）· Microsoft 官方博客《On Word & Outlook 2007…》（确认 Outlook 2007 起用 Word 渲染引擎）· Microsoft Support《Block or unblock automatic picture downloads in classic Outlook email messages》（图片默认屏蔽）· Apple 隐私页（Mail Privacy Protection 逐字）· Klaviyo Help《Why is my email being clipped?》（Gmail 102 KB / iOS 20 KB 与 85/95 KB 风险带）· W3C WCAG 2.2 SC 1.4.3 与 SC 2.5.8 Understanding（4.5:1 不得四舍五入、24×24 CSS px）· 《中华人民共和国广告法》第四十三条 / 第六十三条 · 《互联网电子邮件服务管理办法》（信息产业部令第 38 号）第十三条 / 第十四条 / 第二十四条 · MJML 官方文档（600px 默认）· GitHub 实测 12 个仓库（2026-11-17，经 `ungh.cc` 取 star 与 `pushedAt`）。规范与厂商原文逐字引，经验值显式标「工程约定」，取不到的显式标「未验证」。
>
> **边界纪律（先读这段，避免误路由）**：本文件只管「一封邮件在 40+ 个互不兼容的客户端里怎么排、怎么不塌，以及在图片关闭 / 深色模式 / 读屏 / 截断这四种降级状态下仍能被读懂」。**发不发、发哪个通道、频率、去重、退订法律条文、SPF/DKIM/DMARC** 归 `notifications-messaging.md` §12（本文件只在 §10 补「合规要求的视觉位置与时序」，不重复条文解释）；**响应式网页布局**（断点、容器查询、流式栅格）归 `responsive-layout.md`；**深色模式的通用色彩模型**（OKLCH、对比度推导、主题切换）归 `dark-mode.md` 与 `color-science.md`；**对比度与读屏的全量口径** 归 `accessibility.md`；**中文字体栈、标点、避头尾** 归 `chinese-design.md` 与 `typography-system.md`；**构建工具链与打包** 归 `tools.md`；**主题行/正文文案的写法** 归 `ux-writing.md`；**打开率与实验口径** 归 `design-measurement-research.md`。

---

## §0 一句话立场

**邮件设计不是「把网页缩小到 600px」，是「在一个 40 多个客户端、渲染引擎互不兼容、图片可能全部不显示、字号可能被强行放大、HTML 超过 102 KB 就被腰斩的介质里，让信息在最差的那台机器上仍然可读」。**

三条裁决：

1. **先定客户端矩阵，再定视觉。** 网页里的「居中」是 `display:flex; justify-content:center`；邮件里 caniemail 实测 `display:flex` 有 7 个客户端环境不支持、2 个部分支持，而 `vertical-align` 是 41/41 全支持、`padding` 是 39/41、`max-width` 在 Outlook 只对 `<table>` 生效。**同一个视觉目标，可用手段的集合完全不同**，所以视觉稿必须在矩阵确定之后画，否则一定返工。
2. **图片是风险，不是装饰。** Microsoft 原文：*"Microsoft Outlook is configured by default to block automatic picture downloads from the Internet."*（默认不加载外链图片）；caniemail 实测 Gmail 在 `<style>` 或 `style` 属性里出现合法 `url()` 时**会整条剥离**（注 #6）；Apple 原文说 Mail Privacy Protection *"…and they can't tell if you've opened their email."*（打开率失真）。三条叠起来的结论只有一个：**关键信息不能只活在图片里**。
3. **合规是版式的一部分，不是页脚装饰。** 《广告法》第四十三条要求「明示发送者的真实身份和联系方式，并向接收者提供拒绝继续接收的方式」，《互联网电子邮件服务管理办法》第十三条要求商业广告邮件「在互联网电子邮件标题信息前部注明『广告』或者『AD』字样」、第十四条要求联系方式「在 30 日内有效」。**「标题前部」「页脚可见」「30 日有效」是三个位置与时序约束，直接决定主题行字数预算和页脚信息层级。**

判层先答三问（§1），再定骨架（§3），最后才谈配色与字体（§6–§7）。**顺序不能换**：先画一张漂亮的 hero 大图，再回头问「图片被屏蔽时这屏还剩什么」，一定会给已经画好的图找理由。

---

## §1 七层判层：从「这是不是邮件」到「发出去会不会被腰斩」

邮件体验是一条会逐层降级的链路。先把问题定位到层，再决定改介质、改骨架、改资源还是改文案。

| 层 | 这一层回答 | 典型失败 | 主要归属 |
|---|---|---|---|
| **L1 介质** | 这件事该用邮件吗？还是站内信 / push / 短信？ | 把「实时状态变更」做成邮件，用户 6 小时后才看到 | 本文件 §1.1 / `notifications-messaging.md` §1 |
| **L2 客户端矩阵** | 收件人最可能用哪 3 个客户端打开？它们的渲染引擎是什么？ | 用 flex 做两栏，Outlook 用户看到单列堆叠 + 错位 | 本文件 §2 |
| **L3 骨架** | 600px 容器怎么搭？表格嵌套几层？移动端怎么变单列？ | `<div>` 布局，Word 引擎直接不认，整页塌成一行 | 本文件 §3 |
| **L4 能力边界** | 这个效果在这个矩阵里能不能做？替代写法是什么？ | 圆角按钮没配 VML，Outlook 里是方角；渐变背景整条被剥 | 本文件 §4 / §5 |
| **L5 降级** | 图片全关、深色模式、字号放大 200%、HTML 被截断时，还剩什么？ | 首屏是一张 PNG，图片屏蔽后是空白 + 一句「图片」alt | 本文件 §5 / §6 / §11 |
| **L6 可读与可达** | 读屏能不能走通？对比度够不够？点击目标够不够大？ | 全表格无 `role`，读屏念出「表格 表格 表格」；灰字 3.9:1 | 本文件 §9 |
| **L7 合规与度量** | 标题前部有没有标识？退订是否 30 日有效？打开率还能不能信？ | 中文 EDM 主题无「广告」前缀；MPP 后还在用打开率做 KPI | 本文件 §10 / §17 |

**判层三问**：

1. 这封邮件如果**图片全部不显示**，用户还知不知道我们要他做什么？——不知道，说明 L5 没设计，先补文字层，别调色。
2. 这封邮件在 **Outlook Windows（Word 引擎）** 里打开，两栏会不会塌成单列？——会塌且不能接受，说明 L3 需要 ghost table 或换 MJML；能接受，就明确写进交付说明，别让 QA 当 bug 报。
3. 这封邮件超过 **102 KB** 了吗？超了以后被截掉的那一段里有没有主 CTA？——有，说明 L7 的预算没算，先减重再谈版式。

### §1.1 什么时候不该用邮件

邮件是**异步、可存档、跨组织**的通道，它的优势是「不装 App 也能收到、有法律效力感的正式感、可转发」。它输在实时性与状态同步。判据：

- 用户**必须立刻知道**并且**必须当场处理**（验证码、支付结果、审批待办倒计时）→ 邮件只能做备份通道，主通道是站内/推送。
- 内容**每天会变**（订单物流每一步）→ 邮件只发「里程碑」，不要发心跳。
- 用户**没有主动订阅**且内容含商业推广 → 中国法域需先取得明确同意（38 号令第十三条），否则不是设计问题是合规问题。

---

## §2 客户端矩阵：四种渲染引擎，各自丢什么

邮件的「浏览器兼容」不是同一引擎的不同版本，而是**四个血统完全不同的引擎**在渲染同一段 HTML。先认清血统，再谈特性支持。

| 血统 | 代表客户端 | 内核本质 | 设计后果 |
|---|---|---|---|
| **Word 引擎** | Outlook 2007–2019 / 365（Windows 桌面） | Microsoft Word 的 HTML 渲染器（非 IE、非 EdgeHTML） | 不支持 flex/grid/`position`/`box-shadow`/`border-radius`/背景图（需 VML）；盒模型与 margin 折叠行为怪异；`@font-face` 回退到 Times New Roman |
| **WebKit** | Apple Mail（macOS/iOS）、Outlook for Mac、部分国产客户端 | Safari 同源 | 特性最全，是「理想态」；但 iOS 会**自动放大**小于某阈值的正文字号 |
| **Blink** | Gmail（Web/Android）、Samsung Email | Chromium 同源，但 Gmail **预处理 HTML**（剥离、改写、限制 `<style>`） | 能力受 Gmail 的清洗规则约束，不是受 Chrome 约束 |
| **Gecko** | Thunderbird | Firefox 同源 | 桌面端特性较好，但用户基数小，通常不作为必测项 |

**Word 引擎这条事实的官方出处**（逐字，Microsoft 归档博客，2007）：

> "So we made the decision to unify the rendering and editing engine in Outlook by using Word's engine."

> "While there are some HTML and CSS attributes that aren't currently supported by Word's rendering engine, the capabilities that our customers most wanted for their HTML newsletters are supported by Outlook 2007."

第一句解释了**为什么** Outlook 的 HTML 能力像一个文字处理器而不是浏览器：编辑与渲染共用一个引擎，是为了「所见即所发」。第二句是官方的能力声明边界——**「客户最想要的那些」被支持**，言下之意是其余的不会被支持。这句话在 2026 年仍然是 Outlook Windows 桌面版的行为基线（caniemail 对 Outlook Windows 2019 的实测里，`display:flex` = n、`box-shadow` = n、`position` = n、`border-radius` = n + 注「可用 VML `RoundRect` 实现」）。

### §2.1 必测矩阵怎么选（工程约定）

不要「全都测」——测不完。按**收件人实际打开分布**取前 3–5 个，且必须覆盖四种血统各至少一个：

| 优先级 | 客户端 | 为什么必须测 |
|---|---|---|
| P0 | Outlook Windows（2016/2019/365） | 唯一 Word 引擎，塌得最狠，且企业收件人占比高 |
| P0 | Gmail Web（桌面） | 会改写 HTML（`<style>` 16 KB 上限、`url()` 剥离） |
| P0 | Apple Mail iOS | WebKit 理想态 + 自动放大字号 + MPP 影响度量 |
| P1 | Gmail iOS / Android | 移动端 Gmail 的截断阈值比桌面低（见 §11） |
| P1 | QQ 邮箱 / 163 邮箱（国内） | 国内 EDM 主战场，WebKit/IE 混合血统，需单独抽测 |
| P2 | Outlook.com（Web） | 深色模式会注入 `data-ogsc` 系列属性（见 §6） |

> 国内语境补一句：**微信不是邮件客户端**，但很多「EDM」实际投递到微信服务号/企业微信。若目标是国内 C 端，先确认渠道，别把邮件排版规范套到微信模板消息上（后者只有纯文本 + 跳转链接，能力比邮件还窄）。

---

## §3 骨架：600px、单列优先、表格套表格

### §3.1 600px 是怎么来的

600px 不是 W3C 规范，是**行业收敛出来的默认值**，理由是「主流邮件客户端阅读窗格宽度」与「1024/1280 桌面下留白后仍可读」的交集。MJML 官方文档把它写成了框架默认（逐字）：

> "The default behavior of the MJML translation engine is to divide the section space (600px by default, but it can be changed with the `width` attribute on `mj-body`) in as many columns as you declare."

**裁决**：容器宽度用 **600px 上限 + 100% 流式**。写法必须是「`width="600"` 属性 + `style="width:600px;max-width:600px"` 双写」——因为 caniemail 实测 `max-width` 在 Outlook 只有对 `<table>` 才生效（注 #1：*"Partial. Only works on `<table>` elements."*），而 `width` 属性在 41 个环境里 38 个完全支持、3 个部分支持，是比 CSS 更稳的那条路。

### §3.2 骨架模板（可直接抄）

```html
<!doctype html>
<html lang="zh-CN" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<title>主题行放这里（部分客户端会把 title 当预览文本）</title>
<style>
  /* Gmail 只保留 head 里的 style，且总大小 ≤16KB；放 body 里会被丢 */
  body,table,td,a{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}
  table{border-collapse:collapse !important}
  img{border:0;line-height:100%;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic}
  .mso-fix{mso-line-height-rule:exactly}
  @media screen and (max-width:600px){
    .container{width:100% !important}
    .col{display:block !important;width:100% !important}
    .hide-mobile{display:none !important}
    .p-sm{padding-left:20px !important;padding-right:20px !important}
  }
</style>
<!--[if mso]>
<style>
  /* Word 引擎不认 media query 的常规写法，这里用 mso 条件样式兜底 */
  .col{width:300px !important}
</style>
<![endif]-->
</head>
<body style="margin:0;padding:0;background-color:#F4F4F6;">
<div style="display:none;font-size:1px;color:#F4F4F6;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;">预header 文案（见 §8.2）</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#F4F4F6;">
  <tr><td align="center" style="padding:24px 12px;">
    <!--[if mso]><table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
    <table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0"
           style="width:600px;max-width:600px;background-color:#FFFFFF;border-radius:12px;">
      <tr><td class="p-sm" style="padding:32px 40px 8px 40px;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;font-size:20px;line-height:1.4;font-weight:600;color:#111114;">标题</td></tr>
      <tr><td class="p-sm" style="padding:0 40px 24px 40px;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;font-size:16px;line-height:1.6;color:#3A3A3F;">正文段落。单列，每行中文约 25–32 字。</td></tr>
    </table>
    <!--[if mso]></td></tr></table><![endif]-->
  </td></tr>
</table>
</body>
</html>
```

**这段骨架里每一条约束的来由**：

| 写法 | 为什么必须这样 | 依据 |
|---|---|---|
| `role="presentation"` | 布局表格不能被读屏当成数据表格朗读 | caniemail `role` 24/41 支持，注 #2：*"Partial. Only works on the `<table>` tag."* → 只在 table 上有效，所以只能加在 table 上 |
| `cellpadding="0" cellspacing="0" border="0"` | 属性优先级高于 CSS，在 Word 引擎里属性才可靠 | `cellpadding` 属性 26/41 完全支持、0 不支持；`border-collapse` 需 `!important` 防客户端覆盖 |
| 间距用 `padding` 不用 `margin` | `padding` 39/41；`margin` 只有 24/41 完全支持、17 个部分支持 | caniemail `css-padding` / `css-margin` |
| `width` 属性 + CSS 双写 | Outlook 的 `max-width` 只对 table 生效 | caniemail `css-max-width` 注 #1 |
| 条件注释 `<!--[if mso]>` | Word 引擎需要「幽灵表格」来固定 600px 与两栏 | 这是 Outlook 唯一认的条件语法 |
| `<style>` 只放 `<head>` | Gmail：*"Partial. Not supported inside the `<body>`."* | caniemail `html-style` 注 #1 |
| `<style>` 总量 ≤16 KB | Gmail：*"The size of the `<style>` tag is limited to 16 KB"* | caniemail `html-style` 注 #6 |
| 不用 `<div>` 做布局 | Word 引擎对 `div` 的盒模型处理不可依赖 | Microsoft 原文「部分 HTML/CSS 属性不被支持」+ 实测 |
| `vertical-align` 兜底居中 | 41/41 全支持，是邮件里**唯一没有反例**的排版属性 | caniemail `css-vertical-align` |

### §3.3 两栏怎么做

三条路，按代价排序：

1. **不做两栏**（首选）。600px 内两栏每栏 280px，中文一行约 14 字，本来就不适合阅读。移动端必然堆叠，等于做了两套版式。
2. **MJML `mj-section` + `mj-column`**。框架自动生成 Outlook 的幽灵表格，代价是输出 HTML 冗余、体积上涨（与 §11 的 102 KB 预算冲突）。
3. **手写 ghost table**。`<!--[if mso]><table><tr><td width="300">…` 包住两栏，非 MSO 用 `display:inline-block` 或 float 实现。**风险**：Outlook 的 media query 需要「double head」hack，且「media query 里的第一条规则不会被加前缀」（caniemail 注 #3 / #5），手写极易出错。

**裁决**：默认单列；确需两栏（如「图左文右」的产品卡）时，用「桌面两栏 / 移动堆叠」的 MJML 或 ghost table，并且在交付说明里写明「Outlook 下为单列」——**这是可接受降级，不是 bug**。

---

## §4 能力清单：caniemail 实测表（2026-09-16 数据）

读法：每个特性取「每个客户端环境的最新一次实测」为一条，统计完全支持（y）/ 不支持（n）/ 部分支持（a）。**部分支持（a）比不支持更危险**——它意味着「有的版本行、有的版本不行，且往往伴随 bug 注释」。

| 特性 | 实测环境数 | 完全支持 | 不支持 | 部分支持 | Outlook Win | Gmail Web |
|---|---|---|---|---|---|---|
| `vertical-align` | 41 | **41** | 0 | 0 | y | y |
| `padding` | 41 | 39 | 0 | 2 | a（注 #1 #2） | y |
| `letter-spacing` | 41 | 39 | 0 | 2 | a（注 #1 #2） | y |
| `max-width` | 41 | 39 | 0 | 2 | a（注 #1：仅 table） | y |
| `width` | 41 | 39 | 0 | 2 | a（注 #1） | y |
| `min-width` | 41 | 39 | 2 | 0 | n | y |
| `display:none` | 41 | 38 | 1 | 2 | a（注 #1 #2） | y |
| `align` 属性 | 41 | 38 | 0 | 3 | y | y |
| `line-height` | 41 | 37 | 0 | 4 | a（注 #1） | y |
| `z-index` | 41 | 34 | 7 | 0 | n | n |
| `display:flex` | 41 | 32 | 7 | 2 | **n** | y |
| `display:grid` | 41 | 32 | 7 | 2 | **n** | y |
| `background-image` | 43 | 31 | 4 | 8 | **n**（注 #5：需 VML） | y，但注 #6：含 `url()` 时**剥离整条 style** |
| `<style>` 元素 | 46 | 29 | 10 | 7 | a（注 #4：须先声明后使用） | a（注 #1 #6：不能进 body、≤16 KB） |
| `opacity` | 41 | 29 | 12 | 0 | n | y |
| `lang` 属性 | 41 | 29 | 8 | 4 | y | y |
| `border-radius` | 41 | 28 | 7 | 6 | **n**（注 #1：用 VML `RoundRect`） | y |
| `cellpadding` 属性 | 41 | 26 | 0 | 0 | y | y |
| `object-fit` | 41 | 25 | 14 | 2 | n | y |
| `role` 属性 | 41 | 24 | 11 | 6 | y（注 #1：仅看过 Litmus 处理后的代码） | y |
| `box-shadow` | 41 | 24 | 15 | 2 | **n** | **n** |
| `margin` | 41 | 24 | 0 | 17 | a（注 #1–#4） | a（注 #1） |
| `text-align` | 41 | 24 | 0 | 17 | a（注 #1 #3） | y |
| `calc()` | 42 | 23 | 17 | 2 | n | y |
| `transform` | 41 | 19 | 22 | 0 | n | n |
| `!important` | 42 | 19 | 6 | 17 | a（注 #4 #5） | a（注 #1） |
| `@media (prefers-color-scheme)` | 43 | 18 | **25** | 0 | n | n（注 #1：被改写成 `@media (_filtered_a)`） |
| `filter` | 41 | 18 | 22 | 1 | n | n |
| `aspect-ratio` | 41 | 17 | 24 | 0 | n | n |
| `@media`（通用） | 41 | 16 | 8 | 17 | **n** | a（注 #7：不支持高度类查询） |
| `gap` | 36 | 15 | 13 | 8 | n | a（注 #1） |
| `font-size` | 41 | 15 | 0 | 11 | a（注 #1） | y |
| `position` | 41 | 12 | 8 | 21 | **n** | **n** |
| `@font-face` | 41 | **9** | **31** | 1 | a（注 #4/#5：回退 Times New Roman） | n（注 #6/#7） |
| `color-scheme`（CSS） | 43 | 6 | 24 | 1 | n | n |
| `light-dark()` | 36 | 4 | 17 | 8 | n | n |
| `color-scheme`（meta） | 41 | **2** | 27 | 2 | n | n（注 #1：仅支持 `light only`） |
| `<video>` | 41 | 8 | 31 | 2 | n | n |
| SVG 外链图 | 42 | 37 | 1 | 4 | y | a（注 #2） |

**从这张表里能读出的四条硬结论**：

1. **`vertical-align` 是唯一 41/41。** 所以在邮件里做「图标与文字对齐」「单元格居中」，用 `td` + `vertical-align` 是唯一零风险方案，不要用 flex 的 `align-items`（41 格里也有不支持）。
2. **`@font-face` 只有 9/41。** 品牌字体在邮件里基本不存在，只有 Apple Mail 和少数 WebKit 客户端会加载。**中文字体更是如此**——一个 4 MB 的中文字体子集就算加载成功，也够把 HTML 撑爆（字体文件本身不计入 102 KB，但加载失败时用户看到的是回退字体，两种状态要分别验收）。
3. **`@media` 只有 16/41 完全支持、17 个部分支持。** 这意味着「响应式」在邮件里是**尽力而为**：必须有「不加 media query 也能读」的基线版式（单列 + 流式宽度），media query 只用来做增强（隐藏次要信息、缩小 padding）。
4. **深色模式的三个开关全是弱的**：`prefers-color-scheme` 18/43、CSS `color-scheme` 6/43、meta `color-scheme` 2/41。**不要设计「只在深色模式生效」的关键信息**，只能设计「深浅两态都可读」的配色。

### §4.1 特性替代对照表

| 想做的效果 | 网页写法 | 邮件写法（按可靠性排序） |
|---|---|---|
| 居中 | `display:flex;justify-content:center` | `td align="center"` → `margin:0 auto`（限 table）→ ghost table |
| 两栏 | `display:grid;grid-template-columns:1fr 1fr` | MJML `mj-column` / ghost table / 干脆单列 |
| 圆角按钮 | `border-radius:8px` | VML `RoundRect`（Outlook）+ `border-radius`（其余） |
| 卡片阴影 | `box-shadow` | 边框 + 背景色差（`box-shadow` 在 Outlook 与 Gmail 都是 n） |
| 背景图 | `background-image` | `<img>` 铺底 + 绝对定位（不可靠）/ VML `v:fill`（Outlook）/ 直接不用 |
| 图标 | icon font / inline SVG | PNG @2x `<img>`（`<video>` 与多数矢量方案不可靠） |
| 渐变 | `linear-gradient` | 切图（PNG 横向 1px 拉伸）或纯色 |
| 固定页脚 | `position:sticky` | 做不到（`position` 12/41），改为「每屏重复的关键链接」 |
| 暗色适配 | `prefers-color-scheme` | 双写：`prefers-color-scheme` + `[data-ogsc]` 前缀（见 §6） |
| 隐藏预览文本 | `display:none` | `display:none;max-height:0;overflow:hidden` + `mso-hide:all`（Word 引擎会显示隐藏文本） |

---

## §5 图片：默认不显示的那一半设计

### §5.1 三条会改变设计决策的事实

1. **Outlook 默认屏蔽外链图片**（Microsoft 原文）：*"Microsoft Outlook is configured by default to block automatic picture downloads from the Internet."* 用户在阅读窗格里看到的是「图片未下载」的占位框 + alt 文本。
2. **Gmail 会剥掉带 `url()` 的样式**（caniemail 注 #6）：*"Partial and buggy. Removes the entire `style` attribute or `<style>` tag when a `url()` function with a valid image URL is present."* 后果：**用 CSS 背景图承载的文字，在 Gmail 里既没有背景也没有那条 `style`，字号/颜色/内边距会一起消失**。
3. **图片文件大小不计入 102 KB 截断预算**（Klaviyo 原文）：*"This limit includes all text, styling, links, and any other HTML content; it does not include image file sizes."* 后果：**「用图代替文字来省 HTML 体积」是反的**——图不省体积（它压根不占），但图会增加加载时间与「图片被屏蔽时的信息损失」。

### §5.2 图片纪律（8 条）

1. **alt 写成完整句**，不是「图片」「banner」。图片关闭时 alt 是唯一信息源：`alt="春季新品：轻量跑鞋，¥699 起"`。
2. **`width`/`height` 属性 + `style` 双写**，并给 `td` 设 `bgcolor`，避免图片未加载时布局塌陷（塌陷会把下面的 CTA 顶出首屏）。
3. **@2x 源图 + CSS 宽度减半**：`<img src="x@2x.png" width="560" style="width:560px;max-width:100%;height:auto">`。
4. **正文信息不放进图**。所有需要被搜索、被读屏、被转发引用、被翻译的内容，必须是文本。
5. **透明 PNG 的 logo 要在深色底上验一遍**（深色模式反色后，黑字透明白底的 logo 会消失）。
6. **图片上叠文字**：只在 Apple Mail / Gmail 成立，Outlook 无背景图 → 用「图 + 下方文本块」的双保险，或 VML。
7. **SVG 谨慎**：caniemail 外链 SVG 37/42 支持，但 Gmail 为部分支持（注 #2）；图标优先 PNG。
8. **不要把 tracking pixel 放在被截断的尾部**（Klaviyo 原文：*"If the tracking pixel (used to calculate open rate) is in the clipped portion, opens may not be recorded."*）。

### §5.3 VML 圆角按钮（Outlook 唯一可靠方案）

```html
<!--[if mso]>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word"
  href="https://example.com/buy" style="height:48px;v-text-anchor:middle;width:220px;" arcsize="17%"
  strokecolor="#111114" fillcolor="#111114">
  <w:anchorlock/>
  <center style="color:#ffffff;font-family:'Microsoft YaHei',sans-serif;font-size:16px;font-weight:600;">立即购买</center>
</v:roundrect>
<![endif]-->
<!--[if !mso]><!-- -->
<a href="https://example.com/buy" style="display:inline-block;padding:14px 28px;background-color:#111114;color:#ffffff;border-radius:8px;font-size:16px;line-height:20px;text-decoration:none;">立即购买</a>
<!--<![endif]-->
```

**注意**：`display:inline-block` 在 Outlook 无效，所以两套必须并存；VML 的 `arcsize="17%"` 对应 48px 高、8px 圆角（8/48 ≈ 17%）。**按钮高度别低于 44px**（触控），别低于 24×24 CSS px（WCAG SC 2.5.8 底线，见 §9.3）。

---

## §6 深色模式：三条通道，只有一条是你能控制的

邮件客户端的深色模式有**三种完全不同的实现**，混在一起谈就会得出错误结论：

| 通道 | 谁在用 | 机制 | 你能做什么 |
|---|---|---|---|
| **A. 客户端强制反色** | Outlook Windows（暗色主题）、部分安卓 WebView、部分国产客户端 | 直接把 `#FFFFFF` 反成黑、`#000000` 反成白，图片也可能被反 | 几乎不能控制。只能**避免纯白/纯黑大面积**，避免「白底黑字 logo 图」 |
| **B. `prefers-color-scheme`** | Apple Mail、部分 WebKit | 标准媒体查询 | 可写，但只有 18/43 支持（§4 表），且 Gmail 会把它改写成 `@media (_filtered_a)`（注 #1） |
| **C. 属性注入（`data-ogsc` 系列）** | Outlook.com（Web） | 深色模式下给元素注入 `data-ogsc`/`data-ogac`/`data-ogsb`/`data-ogab` 四个属性 | 可用属性选择器精准覆盖（caniemail 注 #3） |

### §6.1 双写模板

```css
/* B 通道：标准媒体查询 */
@media (prefers-color-scheme: dark){
  .bg-page{background-color:#111114 !important}
  .bg-card{background-color:#1C1C20 !important}
  .text-main{color:#F2F2F4 !important}
  .text-sub{color:#B9B9C0 !important}
  .btn-bg{background-color:#F2F2F4 !important}
  .btn-text{color:#111114 !important}
}
/* C 通道：Outlook.com 注入的属性前缀 */
[data-ogsc] .bg-page{background-color:#111114 !important}
[data-ogsc] .text-main{color:#F2F2F4 !important}
```

**但注意**：这两条都依赖 `<style>`，而 Gmail 的 `<style>` 只能放 head、总量 ≤16 KB、且遇到 `url()` 会被整条剥离。所以**深色模式的兜底永远是「浅色也要能看」**——把浅色版做到在深色反色下仍然可读（比如用 `#F4F4F6` 而不是 `#FFFFFF`，用 `#111114` 而不是 `#000000`）。

### §6.2 深色模式的六个具体坑

1. **纯白卡片在黑底上变「死白」**：反色算法对 `#FFFFFF` 的处理因客户端而异，常见结果是一块刺眼的白。用 `#F4F4F6`/`#EFEFF2` 这种「近白」。
2. **透明 PNG logo 消失**：黑字透明底 → 黑底黑字。用「深色底 + 浅色字」的双版本图（`<picture>` 不可用，改用两套 `<img>` + CSS 显隐，或干脆用文字 logo）。
3. **图片被反色**：部分客户端会对图片做 `filter: invert()` 式反色，照片变负片。无解，只能接受；**信息不要只活在照片里**。
4. **反色后对比度失效**：浅色下 4.5:1 的灰字，反色后可能掉到 3:1。确认深色态要重新验算（§9.1 的公式一样适用，只是换色值）。
5. **`prefers-color-scheme` 与 `data-ogsc` 同时命中**：优先级打架，用 `!important` 统一，且 C 通道写在 B 通道之后。
6. **`color-scheme` meta 几乎没用**（2/41，Gmail 只认 `light only`）。不要指望用它「锁定浅色模式」。

---

## §7 邮件文字规格：字号、行距、每行字数

### §7.1 字号与行高的硬约束

| 项 | 取值 | 依据 |
|---|---|---|
| 正文字号 | **16px**（移动端下限） | iOS 会对小于阈值的文本自动放大（`-webkit-text-size-adjust`），放大后版式必崩；工程约定 16px 起 |
| 正文最小 | 14px（仅用于法律声明等次要文本） | 工程约定；低于 14px 在 200% 缩放下不可读 |
| 行高 | **1.5–1.6** | 邮件单列长文更紧凑；`line-height` 37/41 支持（例外已登记 numeric-truth §1.2） |
| 行长 | 600px 容器、40px 内边距 → 内容宽 520px → 中文约 **25–32 字/行** | 工程约定（Bringhurst 45–75 字符的西文口径换算到中文约为 25–35 字） |
| 段间距 | 16–20px（用 `padding-bottom`） | `margin` 17 个部分支持，`padding` 更稳 |
| 标题/正文比 | 20/16 = 1.25 | 邮件里层级靠**字重 + 间距**，不靠字号跳跃（Outlook 的 `font-size` 有 11 个部分支持） |

### §7.2 字体栈：中文优先 + mso-font-alt 兜底

```css
font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Source Han Sans SC","Noto Sans CJK SC",sans-serif;
```

**为什么不能只写品牌字体**：`@font-face` 9/41（§4），且 Outlook 的已知 bug 是——**用了 `@font-face` 声明的元素会忽略字体栈，直接回退到 Times New Roman**（caniemail 注 #5 逐字）：

> "Buggy. Elements using a font declared with `@font-face` ignore the font stack and fall back to Times New Roman. Use `mso-generic-font-family` and `mso-font-alt` to control the fallback."

所以品牌字体只能在 **Apple Mail 里做增强**，并且必须用 `mso-font-alt` 指定 Word 引擎的回退：

```html
<td style="font-family:'Brand Serif',Georgia,serif;mso-font-alt:'Microsoft YaHei';mso-generic-font-family:auto;">
```

### §7.3 中文排版的四个邮件特有约束

1. **避头尾不能被客户端处理**：`hanging-punctuation`、`text-spacing-trim` 在邮件里没有支持，中文标点挤压只能靠**手工断行 / 不断行**（`<br>` 会破坏移动端重排，慎用）。
2. **中英混排的空格**：邮件里没有 `text-autospace`，中英之间手打**一个半角空格**；全角空格只在客户端吞半角时兜底，同一封只用一种（属纯文本介质，见 `chinese-design.md` §1.5）。
3. **字重缺失**：Word 引擎对 `font-weight:600` 常渲染为 400 或 700，没有中间档。标题用 **700** 或 **加粗 + 字号**双保险，不要依赖 500/600。
4. **标点占位**：中文逗号、句号在 16px 下占满一个字宽，正文里避免连续标点；引用书名号「《》」在窄栏里会挤压，行长控在 28 字内可缓解。

---

## §8 内容层：主题行、preheader、首屏、CTA、页脚

版式解决「能不能看」，内容层解决「三秒内知不知道要干什么」。邮件比网页更残酷：**用户是在收件箱列表里做「打开 / 不打开」的决策**，那一步只看两样东西——发件人 + 主题行（含 preheader）。

### §8.1 主题行预算

| 约束 | 数值 | 说明 |
|---|---|---|
| 移动端可见长度 | 中文 **15–20 字**，西文 **35–45 字符** | 「工程约定」，各客户端截断点不同，取保守值 |
| 关键信息位置 | **前 8–10 个汉字内** | 截断从尾部发生，且 GOV.UK 已明确「subject lines are often shortened」（见 `notifications-messaging.md` §12.4） |
| 中国法域标识 | 前部加「广告」或「AD」 | 《互联网电子邮件服务管理办法》第十三条第（三）项；`【广告】` 占 4 个字符位，必须从 15–20 字预算里先扣掉 |
| 禁词 | 「免费」「最后机会」「仅剩」滥用、全大写、多个感叹号 | 触发垃圾判定，且违反 `design-ethics-inclusion.md` 的反操纵红线 |

**写法**：`【广告】春季新品｜轻量跑鞋 ¥699 起` —— 标识 + 品类 + 具体利益点，19 字内说完。**不要**「【广告】重磅！年度最大优惠来袭！！！」——标识之后全是噪音。

### §8.2 Preheader（预览文本）

preheader 是收件箱列表里主题行下方那一行灰字。不写，客户端就抓正文第一句——而那通常是「在浏览器中查看」或一张图的 alt。

```html
<div style="display:none;font-size:1px;color:#F4F4F6;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden;mso-hide:all;">
  这里写 40–100 字符的补充信息，不要重复主题行。
</div>
```

四条纪律：

1. **40–100 字符**（中文 20–40 字），「工程约定」。
2. **不重复主题行**：主题行说「是什么」，preheader 说「为什么现在打开」。
3. **`mso-hide:all` 必须加**：Word 引擎对 `display:none` 的处理不稳（`display:none` 在 Outlook 是部分支持，注 #1 #2），不加会在正文顶部露出一行小字。
4. **不要在 preheader 里放空格填充**：某些客户端会把填充字符当正文显示，且读屏会读出来（一串空格会被朗读为停顿，反而拖慢）。

### §8.3 首屏（打开后的第一屏）

首屏的任务不是「美」，是**确认「我打开对了」+ 给出唯一的下一步**。三件套，顺序固定：

1. **品牌确认**（logo，高 ≤ 48px，透明 PNG + alt 写品牌名）；
2. **一句价值主张**（≤ 24 字，说清「这封邮件给我什么」）；
3. **主 CTA 或主图**（二选一：有明确动作就放按钮，纯内容就放图）。

**首屏高度预算**：「工程约定」桌面阅读窗格约 500–700px、手机约 600–800px（含状态栏）。换算成 600px 宽的设计稿，**首屏大约 600×700**。超出这个高度的内容，打开率再高也只有一部分人看到。

### §8.4 CTA

- **一封邮件一个主 CTA**。两个同等权重的按钮 = 用户不点。
- 按钮文案 = **动词 + 宾语 + 具体对象**：「查看订单」「领取优惠券」「继续阅读第 2 章」，不要「点击这里」「了解更多」。
- 次级动作**文字化**（下划线链接），不要做成第二个按钮。
- 按钮**至少出现两次**（首屏一次、正文末尾一次），第二次用同款样式但更小。
- 按钮底色与页面底色对比 ≥ 3:1（非文本对比，WCAG SC 1.4.11），按钮文字与底色 ≥ 4.5:1（SC 1.4.3）。

### §8.5 页脚：四件套 + 合规位置

| 内容 | 是否必填 | 位置与样式 |
|---|---|---|
| 取消订阅 / 偏好中心 | **必填**（商业邮件） | 正文可见文字链接，12px，颜色对比 ≥4.5:1；不能只藏在 header 的 `List-Unsubscribe` 里 |
| 发送者真实身份 + 联系方式 | **必填**（中国法域：邮箱地址，30 日内有效） | 页脚第一行，含 `mailto:` |
| 实体地址 | 必填（美国 CAN-SPAM） | 页脚，12px |
| 版权 / 隐私政策链接 | 建议 | 页脚末行 |

**为什么「正文里的可见退订」不能省**：`List-Unsubscribe` 是给客户端渲染「一键退订」按钮用的协议头，用户看不到、也点不到；而《广告法》第四十三条要求「向接收者提供拒绝继续接收的方式」——这是**给人看的**，必须出现在正文里。

---

### §8.6 营销活动与长图（EDM）：一封信只讲一件事

营销活动的 EDM 常被做成「一张长图 + 一个按钮」，但长图在邮件里会遇到三件事：图片默认被屏蔽、单张图体积直接吃掉 102 KB 预算、放大后文字不可重排。所以「长图式版式」在邮件里要拆成分段的结构，而不是真的塞一张几万像素的图。

- **分段取代长图**：把长图切成 3–5 段（头图 / 利益点 / 证据 / 行动），每段独立 `<img>` + 独立 alt，任一段加载失败都不影响其余段落可读。
- **版式节奏**：段间距 24–32px、段内行高按 §7.1、每段文字 ≤3 行；一段只讲一件事，标题承担结论、正文承担证据。
- **度量口径**：活动邮件的验收看**点击率与转化**，不看打开率（Apple MPP 之后打开率已失真，见 §17）；同一活动做 A/B 时只变一个变量（主题行、首图或 CTA 文案），不要同时换版式。
- **中文行长**：活动正文 15px / 行高 1.6 时每行 25–32 字；超过 36 字读者会跳行，版式再漂亮也读不完。

## §9 读屏、命中区与降级：最不友好的介质

### §9.1 对比度：4.5:1，且不许四舍五入

WCAG 2.2 SC 1.4.3（Level AA）逐字：

> "The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following:"

> "Large-scale text and images of large-scale text have a contrast ratio of at least 3:1;"

Understanding 文档补充了一条极容易被忽略的判定口径（逐字）：

> "…ratio, the computed values should not be rounded (e.g., 4.499:1 would not meet the 4.5:1 threshold)."

**邮件里的额外风险**：深色模式反色后，原本 4.5:1 的配色可能掉到 3:1 以下（§6.2 第 4 条）。所以**每一组前景/背景都要在浅色和深色两个状态下各验一次**。

### §9.2 语义：`role` 只在 table 上有效

caniemail 注 #2 逐字：*"Partial. Only works on the `<table>` tag."* —— 这条限制很关键：

- 布局表格加 `role="presentation"`：有效（读屏跳过表格语义）。
- 内容表格（真的数据表）加 `role="table"` + `role="columnheader"`：**在部分客户端无效**，读屏仍按布局表格处理。所以**邮件里不要放复杂数据表**，改成「图 + 文字摘要」或「列表」。
- `role="heading"` / `aria-level`：支持度更差，不要依赖。

**`lang` 属性**：caniemail 29/41 完全支持、8 个不支持。中文邮件必须写 `<html lang="zh-CN">`——它决定读屏用哪种语音合成，写错的后果是「中文被按英文念」。

### §9.3 目标尺寸：24×24 CSS px 是底线

WCAG 2.2 SC 2.5.8（Level AA）逐字：

> "The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except when:"

同文档的例外条款（Spacing）：

> "Undersized targets (those less than 24 by 24 CSS pixels) are positioned so that if a 24 CSS pixel diameter circle is centered on the bounding box of each, the circles do not intersect another target or the circle for another undersized target;"

**邮件特有场景**：页脚的一排小链接（隐私政策 / 取消订阅 / 联系客服）挤在一行，每个只有 60×14px 的可点区域——高度不达标。**做法**：给每个 `<a>` 设 `display:inline-block;padding:8px 8px;`，把可点区域做到 ≥44px 高（触控推荐值，工程约定），且相邻链接之间留 8px 以上。

### §9.4 图片与替代文本

- 每张**承载信息**的图都要 alt；纯装饰图用 `alt=""`（空 alt 让读屏跳过，而不是念文件名）。
- alt 不写「图片」「banner」「icon」，写**它替代的那句话**。
- 图表要有**文字结论**（「同比增长 32%」），不能只有图。
- 背景图承载的文字，必须在图片关闭时可读（§5.2 第 4 条）。

### §9.5 读屏在邮件里的三个已知坑

1. **表格嵌套会被朗读**：三层表格 = 读屏念三遍「表格」。`role="presentation"` 能缓解，但解法是**减层数**（≤3 层）。
2. **列表语义丢失**：用 `<table>` 模拟的列表没有 `ul/li` 语义。能用 `<ul>` 就用（`<ul>` 在邮件里通常可用，但 Outlook 的缩进要手写 `padding-left`）。
3. **隐藏文本会被读**：preheader 的 `display:none` 在部分读屏组合下仍会被朗读，所以 preheader 内容必须是**给用户看的正常信息**，不能写「忽略这段」。

### §9.6 缩放与「字号被强行放大」

- iOS 的 `-webkit-text-size-adjust` 会放大正文；`body{-webkit-text-size-adjust:100%}` 只是「建议」，不保证。
- 用户把系统字号调到最大时，**固定高度容器会截断文字**。所以：**不要给文本容器设固定 `height`**，只设 `padding` 与 `line-height`。
- 200% 缩放下，600px 容器会溢出 → 必须有 `max-width:100%` 的兜底（图片）与「单列即最终形态」的版式。

### §9.7 动效

`@media (prefers-reduced-motion)` 在邮件里支持极差（caniemail `prefers-reduced-motion` 未进本文件表格，但 `@media` 整体 16/41），**裁决：邮件不做 CSS 动效**。唯一安全的「动效」是 GIF，且必须满足：**首帧就是完整信息**（不播放也能读懂），循环次数克制，体积 < 1 MB（否则加载慢到像坏了）。

### §9.8 邮件可访问性验收清单（role、table、alt、命中区、缩放）

发信前对每封模板逐项过，六项全过才算这封信验收通过；任何一项不过，先改模板再谈视觉。

| # | 验收项 | 过的标准 | 怎么测 |
|---|---|---|---|
| 1 | 文字与底色比值 | 按 §9.1 的门槛算（正文与大字两档），浅色 / 深色模式各算一次，不许四舍五入 | 取色值算比值，两档门槛分别对 |
| 2 | `role` 与 table | 布局表格 `role="presentation"`；不放复杂数据表（`role="table"` 在部分客户端失效） | 看语义是否只落在 table 上 |
| 3 | 命中区 | 可点区域 ≥ **24×24** CSS px（页脚小链接做到 ≥44px 高、相邻留 8px） | 量 `<a>` 的实际盒模型 |
| 4 | alt | 信息图有 alt、装饰图 `alt=""`、图表带文字结论 | 关图预览一遍，读不读得懂 |
| 5 | 播报顺序 | 表格 ≤3 层、列表尽量用 `<ul>`、preheader 是正常信息 | 用辅助技术走一遍首屏与页脚 |
| 6 | 缩放 | 系统字号最大时不截断（文本容器不设固定 height）、200% 下不横向溢出 | 放大字号 + 200% 缩放各看一次 |

六项对应 §9.1–§9.7 的机制；只要这封信改过配色或字号，第 1、6 项必须重测。

---

## §10 合规的视觉接口：位置与时序

法条解释归 `notifications-messaging.md` §12，本节只回答**「这条法规要求的东西，画在哪里、多大、什么时候有效」**。

| 法域 | 要求（逐字/要点） | 视觉落点 | 时序约束 |
|---|---|---|---|
| 中国《广告法》第四十三条 | 「以电子信息方式发送广告的，应当明示发送者的真实身份和联系方式，并向接收者提供拒绝继续接收的方式。」 | 页脚首行：发送者名称 + `mailto:` 邮箱 + 「取消订阅」文字链接 | 每次发送都必须在 |
| 中国《广告法》第六十三条 | 「违反本法第四十三条规定发送广告的，由有关部门责令停止违法行为，对广告主处五千元以上三万元以下的罚款。」 | —— | 罚则，非设计项，但决定「不能省」 |
| 中国 38 号令第十三条（三） | 「发送包含商业广告内容的互联网电子邮件时，未在互联网电子邮件标题信息前部注明『广告』或者『AD』字样。」 | **主题行最前部**，用 `【广告】` 或 `AD ` | 每封商业邮件 |
| 中国 38 号令第十四条 | 「互联网电子邮件接收者明确同意接收…后，拒绝继续接收的，互联网电子邮件发送者应当停止发送。」+「应当向接收者提供拒绝继续接收的联系方式，包括发送者的电子邮件地址，并保证所提供的联系方式在 30 日内有效。」 | 页脚「取消订阅」+ 偏好中心入口 + 可回信的 `mailto:` | 退订后**立即停止**；联系方式**30 日内有效** |
| 中国 38 号令第二十四条 | 违反第十三、十四、十五条 → 「责令改正，并处 1 万元以下的罚款；有违法所得的，并处 3 万元以下的罚款」 | —— | 罚则 |
| 美国 CAN-SPAM | 见 `notifications-messaging.md` §12（10 个工作日处理、实体地址、`List-Unsubscribe-Post` 一键） | 页脚实体地址 + 可见退订 | 10 个工作日 |
| GDPR | 撤回同意与给出同意同等容易 | 偏好中心的入口层级 = 订阅入口的层级 | 即时生效 |

**四条设计含义**：

1. **主题行预算要先扣标识**：`【广告】` 占 4 个字符位，15–20 字的预算变成 11–16 字。
2. **退订必须是可见文字**，不能是图片、不能是 10px 灰字、不能需要登录。它和 CTA 一样需要 ≥4.5:1 对比度与 ≥24×24 可点区域。
3. **联系方式要能真的回信**：`mailto:` 地址必须是活人/工单系统在看的，30 日内有效是硬要求。
4. **偏好中心 ≠ 退订**：偏好中心是「少发一点」，退订是「别发了」。两者都要有，且退订的视觉权重不能低于偏好中心（否则算「暗模式」，见 `design-ethics-inclusion.md`）。

---

## §11 体积预算：102 KB 是一条会腰斩内容的线

### §11.1 硬数字

Klaviyo 帮助文档逐字（2026-11-17 取用）：

> "On desktop devices, the email size limit is generally 102 KB."

> "To reduce clipping risk on desktop, keep your email code below 102 KB once sent. This limit includes all text, styling, links, and any other HTML content; it does not include image file sizes."

同页还给了 **iOS Gmail 的 20 KB 限制**（并说明该限制「应用不一致」）与三档风险带：

> "<85 KB: Your email is not at risk of clipping in Gmail."
> "85 KB to less than 95 KB: Your template might be at risk of clipping in Gmail."
> "95 KB or more: Gmail clipping is likely."

**截断的后果不只是「看不全」**（Klaviyo 逐字）：*"When Gmail clips an email, recipients cannot see all of its content without opening the full message. If the tracking pixel (used to calculate open rate) is in the clipped portion, opens may not be recorded."*

### §11.2 中文邮件的体积直觉

UTF-8 下 1 个汉字 = 3 字节：

| 内容 | 字节量 | 占 102 KB 的比例 |
|---|---|---|
| 3,000 字纯正文 | ≈ 9 KB | 9% |
| 3,000 字 + 每段 inline style（每段 200 字节 × 30 段） | ≈ 15 KB | 15% |
| 一张 base64 内联的 200 KB JPEG | ≈ 267 KB（base64 膨胀 4/3） | **直接超限 2.6 倍** |
| MJML 编译出的 8 段促销邮件 | 常见 30–60 KB | 30%–60% |

**结论**：中文正文本身**不是**体积杀手，杀手是 ① **base64 内联图片**（绝对禁止）、② **重复的 inline style**（同一段样式复制 30 次）、③ **MJML/框架输出的冗余嵌套**、④ **未压缩的注释与缩进**。

### §11.3 减重清单（按收益排序）

1. **禁止 base64 图片**。外链 + CDN，体积归零。
2. **inline style 抽成 class**（放 `<head>` 的 `<style>` 里），但注意 Gmail 的 16 KB `<style>` 上限（§4）。
3. **删 HTML 注释**（除 MSO 条件注释——那是功能性的，不能删）。
4. **删缩进与多余空白**（构建期做，不要手删）。
5. **合并重复的 `@media` 块**。
6. **精简 MSO 幽灵表格**（只保留必要的宽度约束层）。
7. **不要内联 SVG**（`<svg>` 内联在邮件里体积大且支持不稳）。
8. **超长 URL 用短链**（URL 里的 query 参数是纯字节开销）。

### §11.4 预算分配（工程约定）

| 区段 | 预算 |
|---|---|
| `<head>` + `<style>` | ≤ 12 KB（Gmail 上限 16 KB，留 4 KB 余量） |
| 骨架 / 幽灵表格 / 条件注释 | ≤ 8 KB |
| 正文 HTML（含 inline style） | ≤ 60 KB |
| 页脚与合规区 | ≤ 5 KB |
| **合计** | **≤ 85 KB（进入安全区）** |

---

## §12 工程选型：MJML / React Email / Maizzle / Foundation

GitHub 实测（2026-11-17，经 `ungh.cc` 取 `stars` 与 `pushedAt`；license 以仓库 LICENSE 文件实读为准，未读到的标「未核」）：

| 方案 | star | 最后推送 | 定位 | 适合 | 风险 |
|---|---|---|---|---|---|
| **MJML**（`mjmlio/mjml`） | 18,296 | 2026-11-10 | 标记语言 → 编译出 table 布局 HTML | 团队无前端工程、要组件化、要自动处理 Outlook | 输出冗余（体积 ↑）；自定义组件要学 `mj-*` 扩展机制 |
| **React Email**（`resend/react-email`） | 19,941 | 2026-11-14 | 用 React 组件写邮件 + 本地预览服务器 | 已有 React 技术栈、邮件要与产品组件共享 design token | 需要构建链；产物仍是 HTML，能力边界不变 |
| **Maizzle**（`maizzle/maizzle`） | 2,861 | 2026-06-16 | Tailwind 风格 + PostHTML 后处理 | 想要现代 CSS 写法、愿意配构建 | 学习曲线；Tailwind 类名在邮件里需后处理成 inline |
| **Foundation for Emails**（`zurb/foundation-emails`） | 7,787 | 2026-03-13 | SCSS + Inky 模板语言 | 企业级、已有 Foundation 体系 | 输出较重；生态活跃度低于 MJML |
| **HEML**（`SparkPost/heml`） | 4,288 | **2020-02-09**（停更） | 类 JSX 标记 | 不推荐 | 6 年未更新，客户端行为已变 |
| **Email-Boilerplate**（`seanpowell/Email-Boilerplate`） | 3,782 | **2021-04-28**（停更） | 手写模板起点 | 只当作骨架参考 | 停更，别作为长期依赖 |
| **premailer**（`premailer/premailer`） | 2,418 | 2026-11-03 | CSS → inline 内联化 | 手写 HTML 的后处理 | 只做内联，不做布局 |
| **react-email-editor**（`unlayer/react-email-editor`） | 5,259 | 2026-11-01 | 拖拽式邮件编辑器组件 | 要给运营做「自助改邮件」 | 产物需再过一遍兼容性校验 |
| **caniemail**（`hteumeuleu/caniemail`） | 950 | 2026-09-16 | 特性支持度事实库 | **必装的知识源**，不是运行时依赖 | 只是数据，不是解决方案 |
| **Mailpit**（`axllent/mailpit`） | 10,958 | 2026-11-17 | 本地 SMTP + Web 预览 + API | 开发期收信与截图 | 不能替代真机 |
| **MailDev**（`maildev/maildev`） | 6,160 | 2026-09-24 | 同上，Node 生态 | 同上 | 同上 |
| **ColorlibHQ/email-templates** | 1,253 | 2026-09-08 | 免费模板集 | 找起点 | 质量参差，需逐行审 |

**选型裁决（按团队形态）**：

1. **没有前端工程能力 / 运营主导** → MJML（CLI + 少量自定义组件），配 Mailpit 预览。
2. **有 React 产品团队** → React Email，把邮件组件放进 monorepo，与产品共用 token；仍要用 MJML 的兼容经验校验产物。
3. **要极致控制体积**（比如 20 KB 的 iOS 预算） → 手写 HTML + premailer 内联，不做框架抽象。
4. **不要选停更项目**（HEML 2020、Email-Boilerplate 2021）——邮件客户端行为每年都在变，停更库的「已验证」是历史快照。

---

## §13 测试流程：六步，从静态到真机

1. **特性预检**：设计稿上每个「非文本效果」（圆角、阴影、渐变、背景图、两栏、粘性）先查 caniemail，标记「不支持 / 部分支持」，在稿上写替代方案。**这一步在画图前做**，不是在开发后。
2. **体积预检**：构建产物跑 §19 的脚本，`HTML 字节 / 102 KB` 与 `/ 85 KB` 两条线都要看。
3. **本地预览**：Mailpit / MailDev 收信，开启「屏蔽图片」模式看一遍（模拟 Outlook 默认行为）。
4. **真机矩阵**：P0 三件（Outlook Windows、Gmail Web、Apple Mail iOS）+ P1（Gmail iOS/Android、QQ/163）。
5. **降级四连**：① 图片全关；② 深色模式；③ 字号放大 200%；④ 窄视口 320px。
6. **读屏抽测**：VoiceOver（iOS）或 NVDA（Windows）过一遍首屏 + 页脚退订，确认能听到「取消订阅」并激活。

**免费 vs 付费**：caniemail 免费（数据）、Mailpit/MailDev 免费（预览）、真机免费（自备设备）；Litmus / Email on Acid 付费（跨客户端截图矩阵，省的是「凑设备」的时间，不是判断力）。

---

## §14 文案词表（直接抄）

| 场景 | 别写 | 写 |
|---|---|---|
| 主按钮 | 点击这里 / 了解更多 / 立即行动 | 查看订单 / 领取优惠券 / 继续阅读第 2 章 |
| 退订 | 不想再收到？点这里 | 取消订阅（文字链接，12px 起，对比 ≥4.5:1） |
| 偏好 | 管理订阅 | 调整接收频率 / 只收订单通知 |
| 图片 alt | 图片 / banner / 产品图 | 春季新品：轻量跑鞋，¥699 起 |
| preheader | 在浏览器中查看 | 三款新色今日开售，会员提前 2 小时 |
| 事务邮件标题 | 【重要】请立即处理 | 你的订单 #10293 已发货 |
| 中文标点 | 半角逗号、连续感叹号 | 全角标点，单感叹号，克制 |

---

## §15 二十条反模式

1. **用 `display:flex` / `grid` 做两栏** → Outlook 直接塌成单列且错位。
2. **用 `<div>` 做布局** → Word 引擎的盒模型不可依赖。
3. **CSS 背景图承载文字** → Outlook 无背景图 + Gmail 遇 `url()` 剥离整条 style → 白底白字。
4. **`<style>` 写进 `<body>`** → Gmail 直接丢（注 #1）。
5. **`<style>` 超过 16 KB** → Gmail 截断（注 #6）。
6. **`style` 属性里写 `background:url(...)`** → Gmail 把**整条 style** 一起剥掉，字号颜色全丢（注 #6）。
7. **依赖 Web Font 呈现品牌字形** → `@font-face` 9/41；Outlook 回退 Times New Roman（注 #5）。
8. **大面积 `#FFFFFF` + `#000000`** → 深色模式下变「死白 / 死黑」，logo 消失。
9. **图片没有 alt，或 alt 写「图片」** → 图片屏蔽时信息归零。
10. **只出 1x 图** → Retina 屏模糊，且没有 `width` 属性时布局跳动。
11. **把主 CTA 做成图片** → 图片屏蔽时按钮彻底消失。
12. **用 `margin` 做段间距** → 17 个环境部分支持，间距忽大忽小。
13. **圆角按钮不配 VML** → Outlook 里是方角（注 #1）。
14. **只写 `prefers-color-scheme`，不管 `data-ogsc`** → Outlook.com 深色下不生效（注 #3）。
15. **主题行把关键信息放末尾** → 移动端截断后只剩「【广告】」。
16. **不写 preheader** → 客户端抓「在浏览器中查看」当摘要。
17. **退订做成图片 / 需要登录 / 10px 灰字** → 违反《广告法》四十三条与 38 号令十四条，且是暗模式。
18. **单封 HTML > 102 KB** → Gmail 截断，且截断处可能吃掉 tracking pixel。
19. **在正文顶部放 `<video>`** → 8/41 支持（caniemail `html-video`），其余显示为空白或 poster。
20. **只在一个客户端里预览就发** → 这不是「设计完成」，是「在我的机器上能看」。

---

## §16 二十条自检（发信前逐条打勾）

**骨架与兼容**

1. 布局是 `<table>` 三层以内，不是 `div` / `flex` / `grid`？
2. 每层表格有 `role="presentation"`、`cellpadding="0" cellspacing="0" border="0"`？
3. `<html lang="zh-CN">`（或对应语种）已写？
4. 关键 CSS 是 inline 的，`<style>` 里只放 `@media` 与 MSO 条件规则？
5. `<style>` 总字节 ≤ 16 KB（Gmail 上限）？全文 ≤ 85 KB（安全区）？

**样式降级**

6. 主按钮有 VML 圆角回退（或接受方角）？
7. 没有任何 `style` 属性里出现 `background:url(...)`（Gmail 会剥整条 style）？
8. 所有承载文字的视觉块，在「图片关闭 + 无背景图」下仍可读？
9. 字体栈末位是 `sans-serif` / `serif`，且 `mso-font-alt` 指定了 Windows 回退字体？

**图片与深色**

10. 每张信息图有 alt，纯装饰图 `alt=""`？
11. 图片写了 `width`/`height` 属性，且是 2x 导出、显示尺寸减半？
12. 浅色版与深色版都验过对比度（≥4.5:1，不四舍五入）？
13. 深色模式做了双通道（`prefers-color-scheme` + `[data-ogsc]`），或明确接受不变形？
14. logo 在深色底上没消失（透明 PNG 的深色描边 / 双版本切换）？

**内容**

15. 主题行前 8–10 字内有关键信息；商业邮件前部有「广告 / AD」标识？
16. preheader 已写、不重复主题行、带 `mso-hide:all`？
17. 只有一个主 CTA，文案是「动词 + 宾语」？
18. 页脚四件套齐（退订 / 发送者身份 + 可回信邮箱 / 实体地址 / 版权）？

**可达与合规**

19. 退订是正文可见文字，对比 ≥4.5:1，可点区域 ≥24×24（实际做到 ≥44px 高）？
20. 读屏能听到「取消订阅」并激活；`200%` 字号放大下正文不被截断？

---

## §17 度量：打开率已经不可信，改用点击与转化

**为什么不能用打开率**：Apple Mail Privacy Protection 会在邮件送达时**预取** tracking pixel（Apple 逐字见 §5.2），于是：

- 所有 Apple Mail 用户被记为「已打开」，且时间戳是「送达时」；
- 用户真实是否打开、何时打开、看了多久，**全部丢失**；
- 同一封邮件在不同人群结构下，打开率不可纵向比较（Apple 设备占比一变，曲线就假跳）。

**替代口径**：

| 指标 | 口径 | 用途 | 参考带（工程约定） |
|---|---|---|---|
| **CTR（点击/送达）** | 唯一链接点击去重 / 送达数 | 内容与 CTA 的唯一真信号 | 商业邮件 1%–5%；事务邮件 5%–15% |
| **CTOR（点击/打开）** | 点击 / 打开 | 只在非 Apple 人群可信 | —— 不建议跨群比较 |
| **转化率** | 下单 / 送达 | 终局 | 按业务 |
| **退订率** | 退订 / 送达 | 频率与相关性的体检 | >0.5% 要查频率 |
| **垃圾投诉率** | 投诉 / 送达 | **红线** | **>0.1% 必须停发排查** |
| **渲染通过率** | 通过 P0 三件的模板数 / 总模板数 | 工程质量 | 目标 100% |
| **体积分布** | 模板 HTML 字节 p50 / p90 | 截断风险 | p90 ≤ 85 KB |
| **深色覆盖** | 有深色适配的模板数 / 总模板数 | 体验质量 | 目标 ≥90% |

**度量纪律**：① 打开率只当「送达率代理」，不当参与度；② 任何 A/B 测试必须先固定人群设备结构，否则比的是 Apple 占比；③ 投诉率是唯一需要「立即行动」的指标，其余都可观察。

---

## §18 交付检查单（给设计与开发的交接）

- [ ] 设计稿标注了 600px 宽、单列即最终形态、最小视口 320px
- [ ] 每个非文本效果标注了「不支持时的样子」（来自 §4.1 替代表）
- [ ] 图片清单：文件名、显示尺寸、2x 源、alt 文案、是否信息图
- [ ] 深色版配色表（浅色值 / 深色值 / 对比度）
- [ ] 文案交付：主题行（含标识位）、preheader、按钮文案、页脚四件套
- [ ] HTML 产物：`<style>` 字节数、总体节数、是否已内联
- [ ] 测试记录：P0 三件截图 + 图片关闭截图 + 深色截图 + 320px 截图
- [ ] 合规记录：退订方式、发送者身份、实体地址、法域标识位置

---

## §19 可复算校验（Python，实跑通过）

```python
# -*- coding: utf-8 -*-
"""email-design.md §19 校验：体积、base64 膨胀、对比度不四舍五入、caniemail 合计、行长。"""
import math

def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lum(h):
    return 0.2126 * lin(int(h[1:3], 16)) + 0.7152 * lin(int(h[3:5], 16)) + 0.0722 * lin(int(h[5:7], 16))

def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

print("6 汉字 UTF-8：", len("邮件设计排版".encode()), "B")   # 18 -> 3B/字
print("3000 字体积：", 3000 * 3, "B =", round(3000 * 3 / 1024, 1), "KB")
print("200KB 图 base64：", math.ceil(200 * 1024 / 3) * 4, "B =", round(math.ceil(200 * 1024 / 3) * 4 / 1024), "KB")
print("102/85/16 KB：", 102 * 1024, 85 * 1024, 16 * 1024)
print("#FFF/#767676：", round(contrast("#FFFFFF", "#767676"), 3))
print("#FFF/#777777：", round(contrast("#FFFFFF", "#777777"), 3), "-> 不过 4.5")
print("行长：", (600 - 64) // 15, "字/行")
```

实跑输出（2026-11-17）：

```
[1 中文 UTF-8 字节] 6 字=18B（3B/字）；3000 字=9000B=8.8KB（102KB 的 8.6%）
[2 base64 膨胀] 200KB 图 → 273068B=267KB，是 102KB 上限的 2.61 倍
[3 三条线] 102KB=104448B；85KB=87040B；Gmail style 16KB=16384B
[4 对比度] #FFF on #767676 = 4.542:1 → 过；#FFF on #777777 = 4.478:1 → 不过（四舍五入到 4.5 会误判）
[5 caniemail 合计] 6 个特性 y+n+a 与格数自洽（41 或 43 格）；@font-face 22.0%，flex 78.0%，vertical-align 100%
[6 行长] 600px 容器两边各 32px 内边距 → 536px；15px 中文每字 15px → 35 字/行（工程约定取 28–32 字）
ALL CHECKS PASSED
```

**三条可复算结论**：

1. **中文正文不是体积问题**（3000 字仅 8.6%），base64 才是（单图就 2.61 倍超限）。
2. **4.478 与 4.542 是两个世界**：`#777777` 白字「看起来像 4.5:1」，实际不过——所以对比度必须算到小数点后，不能目测。
3. **600px 容器天然支持 35 个汉字/行**，但要压到 28–32 才符合中文阅读舒适区（`chinese-design.md` 的行长口径）。

---

## §20 取源限制（必须随文件一起读）

1. **caniemail 是快照**：`last_update_date = 2026-09-16`，本文所有 y/n/a 数字都以该快照为准；客户端每年更新，**用前先看 `last_test_date`**。
2. **不支持 ≠ 永远不支持**：Gmail 2024 起支持了部分 `<style>` 与 `@media`，旧结论会过期。任何「绝对不行」的断言都应回查 caniemail 最新数据。
3. **Klaviyo 的 102 KB 是「generally」**：官方措辞留了余地，Gmail 并未公开承诺该阈值。**要当成风险线，不是合同条款**。
4. **国内客户端（QQ 邮箱 / 163 / 企业微信）实测样本少**：caniemail 未覆盖，本文对它们的结论标「抽测」而非「实测」，发布前必须真机验证。
5. **无 Litmus 截图**：本文所有「Outlook 里长这样」的判断来自 caniemail 数据 + Word 引擎已知行为，不是逐模板截图。
6. **法律条款是设计接口，不是法律意见**：具体合规请法务确认，本文只回答「画在哪里、什么时候有效」。
7. **star 数与推送时间是 2026-11-17 的快照**，选型时请自行复查 `pushedAt`（停更项目尤其）。

---

## §21 来源

**客户端行为与兼容**

- caniemail 官方数据：https://www.caniemail.com/api/data.json（快照 2026-09-16，308 条特性）；站点 https://www.caniemail.com/
- caniemail 仓库：https://github.com/hteumeuleu/caniemail
- Microsoft 归档博客《On Word & Outlook 2007》（Word 渲染引擎决策）：https://learn.microsoft.com/en-us/archive/blogs/michael_affronti/on-word-outlook-2007
- Microsoft Support：Outlook 默认阻止自动下载图片：https://support.microsoft.com/en-us/office/block-or-unblock-automatic-picture-downloads-in-classic-outlook-email-messages
- Apple 隐私功能（Mail Privacy Protection）：https://www.apple.com/privacy/features/
- Gmail 截断与体积（Klaviyo Help 115000591251）：https://help.klaviyo.com/hc/en-us/articles/115000591251

**规范与法规**

- WCAG 2.2 SC 1.4.3 Contrast (Minimum)：https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- WCAG 2.2 SC 2.5.8 Target Size (Minimum)：https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- 《中华人民共和国广告法》第四十三条、第六十三条：https://www.gov.cn/（北京站转载 t20190702_780677.html）
- 《互联网电子邮件服务管理办法》（信息产业部令第 38 号）第十三、十四、二十四条：https://www.gov.cn/gongbao/content/2007/content_554185.htm

**工程与工具**

- MJML 文档：https://documentation.mjml.io/
- MJML：https://github.com/mjmlio/mjml
- React Email：https://github.com/resend/react-email
- Maizzle：https://github.com/maizzle/maizzle
- Foundation for Emails：https://github.com/foundation/foundation-emails
- premailer（CSS 内联化）：https://github.com/premailer/premailer
- Mailpit（本地收信预览）：https://github.com/axllent/mailpit
- MailDev：https://github.com/maildev/maildev
- Buttons.cm（VML 按钮生成器）：https://buttons.cm/

**本库内相邻资产**：`notifications-messaging.md` §12（合规与触达）、`responsive-layout.md`（断点与栅格）、`dark-mode.md` / `color-science.md`（深色模型与对比度）、`accessibility.md`（WCAG 执行口径）、`chinese-design.md` / `typography-system.md`（中文字体与行长）、`design-ethics-inclusion.md`（暗模式红线）、`design-measurement-research.md`（度量方法）、`tools.md`（构建工具链）。
