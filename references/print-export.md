# 打印与导出（Print & PDF Export）：纸张、分页、去色可读、页眉页脚

> 适用：网页「打印 / 导出 PDF」、报表与对账单、发票与合同、简历、报价单存档、后台批量打印
> 不适用：印刷工艺（专色、出血、模切 → `editorial-layout.md` §10）；屏幕内阅读顺序（→ `accessibility.md`）

## §0 一句话立场

**打印稿是第二载体，不是屏幕的截图**：凡是靠颜色、悬停、滚动位置、分页脚本才成立的信息，在纸上都必须改由文字与位置承载；验收方式只有一个——黑白打印出来后，不看屏幕也能读懂每一页。

## §1 判层：先问五个问题，再动手

| # | 问题 | 答「是」→ 去哪一节 | 答「否」→ |
|---|---|---|---|
| 1 | 会被黑白复印或传真吗 | §4 去色可读优先，语义一律补文字 | §4 仍要过灰度测试 |
| 2 | 会分页装订（≥2 页）吗 | §3 分页与表头重复、§5 页码与续页 | 单页：§2 纸张与边距 |
| 3 | 是归档件（合同、发票、审批单）吗 | §2 纸张固定 A4、§5 留导出时间与版本 | 随手打印：可接受浏览器默认页眉页脚 |
| 4 | 内容来自表单/交互控件吗 | §5 把值渲染成文本，不印输入框与按钮 | 静态内容：§6 反模式自查 |
| 5 | 同页还有导航、工具栏、筛选器吗 | §5 隐藏非正文（nav / toolbar / pager） | — |

四类构型：**报表类**（表头重复 + 页脚页码）、**凭证类**（固定 A4、不可编辑、留导出时间）、**长文类**（不分栏、标题不与正文分离）、**卡片类**（每卡 `break-inside: avoid`，宁留白不切断）。

## §2 纸张与页边距：先定页面盒，再谈排版

官方原文（MDN `@page`）：*"The **`@page`** at-rule is a CSS at-rule used to modify different aspects of printed pages. It targets and modifies the page's dimensions, orientation, and margins."*

MDN `size` 描述符原文：*"defines the size and orientation of the box which is used to represent a page. Most of the time, this size corresponds to the target size of the printed page if applicable."*

精确值（MDN `size` 页逐字给出）：

| 关键字 | 官方尺寸 | 用途 |
|---|---|---|
| `A4` | **210mm × 297mm**（"most frequently used dimensions for personal printing"） | 中国 / 欧洲默认，归档件基准 |
| `letter` | **8.5in × 11in** | 北美默认 |
| `A5` | 148mm × 210mm | 单据小票、手册 |
| `A3` | 297mm × 420mm | 报表附页、图纸 |
| `portrait` | 默认方向（最长边竖直） | 正文 |
| `landscape` | 最长边水平 | 宽表、看板 |

两条硬约束：

1. **`@page` 里只能写页面描述符与 margin at-rules**（MDN 原文：*"The `@page` at-rule can contain only page descriptors and margin at-rules."*）。
2. **不要在 `@page` 里用 `vh / vw / vmin / vmax`**（MDN 原注：*"Meanwhile do not use them within a `@page` at-rule."*）。

设计后果，逐条可执行：
- 内容边距 **≥12mm**；装订侧（奇偶页）再加 **≥8mm**，即左侧 20mm。打印机不可打印区通常 ≤6.4mm，12mm 是留安全余量后的经验下限，不是规范值。
- A4 正文版心宽 = 210 − 12 − 12 = **186mm**；三栏表按 6:3:1 分，最窄列 <28mm 就改两栏或转纵向。
- `size: A4` 不等于"一定按 A4 出"：打印对话框的"适应页面"能推翻它，行长与列宽用 `mm`/`ch`，别写死 `px`。
- 页眉页脚优先用浏览器自带；`@top-right` 一类 margin at-rule 支持面窄，**不作唯一页码通道**，正文底部另给「第 x / 共 y 页」由脚本填数。

## §3 分页：不切断语义块，不丢表头

官方原文（MDN `break-inside`）：*"The **`break-inside`** CSS property sets how page, column, or region breaks should behave inside a generated box. If there is no generated box, the property is ignored."*

取值语义（MDN 逐字）：`avoid` = *"Avoids any break (page, column, or region) from being inserted within the principal box."*；`avoid-page` 只管分页。优先级：强制断点 > `avoid`，而 `avoid` 只在"该元素边界"上生效——**它不保证内容一定不跨页，只保证浏览器优先寻找别处断点**。

可照抄的分页规则：

```css
@media print {
  h1, h2, h3 { break-after: avoid; }        /* 标题不留在页尾 */
  table       { break-inside: auto; }        /* 大表允许跨页 */
  tr, figure, blockquote, .signature { break-inside: avoid; }
  thead { display: table-header-group; }     /* 每页重复表头 */
  tfoot { display: table-footer-group; }
  .keep-with-next { break-after: avoid; }
}
```

验收：打印预览里逐页看 **① 有没有一行被切成上下两半 ② 第 2 页起表头是否还在 ③ 标题是否单独留在页尾**。三项任一失败，就在对应块加 `break-inside: avoid`，不要靠缩字号硬塞。

## §4 颜色与背景：浏览器默认会"帮你"删色

官方原文（MDN `print-color-adjust`）：*"By default, the browser is allowed to make any adjustments to the element's appearance it determines to be necessary and prudent given the type and capabilities of the output device."*

`economy`（默认）：*"when printing, a browser might opt to leave out all background images and to adjust text colors to be sure the contrast is optimized for reading on white paper. This is the default."*

`exact`：*"The element's content has been specifically and carefully crafted to use colors, images, and styles in a thoughtful and/or important way, such that being altered by the browser might actually make things worse rather than better."*

关键警告（MDN 逐字）：*"there isn't any guarantee that `print-color-adjust` will do anything. Not only can the user override the behavior, but each user agent is allowed to decide for itself how to handle `print-color-adjust` in any given situation."*

设计后果，逐条可执行：
- **语义不许只靠底色**：状态徽标（成功 / 失败 / 待审）必须有文字或图形，底色删掉后仍可判读——这一条与 J10「空态靠出口判型」同源。
- 深色主题页面**必须单独出打印稿**：`filter: invert()` 类的暗色在纸上等于黑底，`economy` 又会把背景剥成白底浅灰字，最坏结果是**白底白字**。打印样式里显式覆盖 `background: #fff; color: #000;`。
- 报表的斑马纹、热力块、图例色块，全部补**灰度差 ≥ 可辨**的第二通道（数字、符号、线型）；只靠色相的浅底在灰度里同值。
- 必留底色时：`.badge{print-color-adjust:exact}`，但仍按"可能失效"设计。

## §5 链接、表单与页脚：把"可点"翻译成"可读"

- 外链在纸上失去可点性：`a[href^="http"]::after { content: " (" attr(href) ")"; }` + `word-break: break-all`，**只在 print 媒体里加**。
- 表单控件必须"值化"：边框、按钮、下拉箭头、`placeholder` 全不印（`input,select{border:0;appearance:none}`），值另用文本渲染，或导出前切只读视图。
- 每页页脚三件：**文档名 + 导出时间 + 第 x / y 页**；凭证类再加"本页金额合计"，防抽页拼错。
- 隐藏非正文：`nav, .toolbar, .pagination, .cookie-bar { display: none !important; }`——打印样式优先级低于组件库内联样式，此处 `!important` 正当。

## §6 反模式（10 条）

1. 只加 `@media print { body { zoom: .8 } }` —— 缩放不解决断页与表头。
2. `position: fixed` 做每页页眉 —— 部分引擎不重复，且盖正文。
3. 表格不设 `display: table-header-group` —— 第 2 页起无列名。
4. 深色主题直接出纸 —— 黑底耗墨、剥色后白底浅字。
5. 状态只用底色 —— 黑白复印后四类全同。
6. 分页落在卡片、签名、图注中间 —— 一份合同被切成两半。
7. 纸上仍留"筛选 / 排序 / 共 128 条" —— 把界面状态当文档内容。
8. 链接只印文字 —— 纸质读者无法回源。
9. A4 按 1440px 屏宽等缩 —— 行长 120 字，读两行就串行。
10. 把 `window.print()` 当"导出 PDF" —— 得到带浏览器页眉页脚的稿，文件名与元数据不可控。

## §7 自检清单（交付前逐条打勾）

- [ ] 黑白打印一次：所有状态、图例、强调仍可判读
- [ ] 第 2 页起表头在、页码在、续页有标识
- [ ] 没有任何一行 / 卡片 / 签名块被切断
- [ ] 标题没有单独留在页尾
- [ ] 页面盒 `@page { size; margin }` 显式声明，且 `@page` 内无 `vh/vw`
- [ ] 导航、工具栏、筛选器、分页控件在纸上全部消失
- [ ] 表单值已值化，没有输入框与按钮残影
- [ ] 外链带 URL（仅 print 媒体）
- [ ] 深色主题有独立打印覆盖，不靠浏览器剥色
- [ ] 导出文件名与页脚文档名一致（可追溯）

## §8 可跑校验：打印稿体检

```python
# 用法：python -I -X utf8 print_audit.py   （把 HTML 片段换成你的导出模板）
import re

CSS = """
@media print {
  @page { size: A4; margin: 12mm 12mm 16mm 20mm; }
  thead { display: table-header-group; }
  tr, figure { break-inside: avoid; }
  h2 { break-after: avoid; }
}
"""
HTML = "<table><thead><tr><th>项目</th></tr></thead><tbody><tr><td>1</td></tr></tbody></table>"


def audit(css: str, html: str) -> list[str]:
    problems = []
    block = re.search(r"@media\s+print\s*\{(.*)\}", css, re.S)
    if not block:
        return ["缺少 @media print 块"]
    body = block.group(1)
    if "@page" not in body:
        problems.append("未声明页面盒（@page size / margin）")
    if re.search(r"@page[^{]*\{[^}]*\d(vh|vw|vmin|vmax)\b", body):
        problems.append("@page 内使用了视口单位")
    if "<thead" in html and "table-header-group" not in body:
        problems.append("表格缺表头重复（display: table-header-group）")
    if "<tr" in html and "break-inside" not in body:
        problems.append("行块未设 break-inside: avoid")
    return problems


issues = audit(CSS, HTML)
print("PASS" if not issues else "FAIL: " + "; ".join(issues))
assert not issues, issues
print("段 A OK")
```

```python
# 段 B：颜色对比可读性（不打印也能预判"剥掉底色"后的最坏情况）
def lum(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(a: str, b: str) -> float:
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# 深色徽标打印时底色被剥 → 只剩文字色对白纸
cases = {"成功 #16A34A": "#16A34A", "警告 #B45309": "#B45309", "失败 #DC2626": "#DC2626"}
worst = {k: round(ratio(v, "#FFFFFF"), 2) for k, v in cases.items()}
print("对白纸最坏对比：", worst)
weak = sorted(k for k, v in worst.items() if v < 4.5)
print("需补第二通道：", weak)
assert weak == ["成功 #16A34A"], "预期仅成功绿跌到 4.5:1 以下"
print("段 B OK")
```

实跑（`python -I -X utf8`，2026-11-21）：段 A `PASS`；段 B 输出成功绿 **3.3:1**、警告 5.02:1、失败 4.83:1，`需补第二通道： ['成功 #16A34A']` —— 3.3 连正文 4.5 都不到，故 §4 要求把语义搬到文字/图形，而不是把绿字调深了事。

## §9 取源限制

| 目标 | 状态 | 处理 |
|---|---|---|
| MDN `@page` / `size` / `print-color-adjust` / `break-inside` | 2026-11-21 逐字取到 | 直接引用，见 §2–§4 |
| CSS Paged Media L3（margin boxes） | 未逐字取到 | §2 只给"支持面窄"，不给原文 |
| 打印机不可打印区 | 无统一官方值 | §2 的 12mm 标经验下限，注明"非规范值" |
| `counter(pages)` 总页数在浏览器里的支持 | 未逐字验证 | §5 要求脚本填数，不把 `@top-right` 当唯一通道 |
