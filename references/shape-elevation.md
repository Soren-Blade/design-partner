# 形状与深度系统（Shape & Elevation）

> 快照 2026-11-08 · 24 节 · 12 场景 · 20 反模式 · 20 自检 · 6 段可抄代码（3 段 Python 已实跑）

把「圆角调几像素、卡片加个阴影、弹窗往上抬一点」变成**有约束、可计算、能验收的决策**。本文件不替代 `color-science.md`（表面色怎么算）/`typography-system.md`（文字契约）/`dark-mode.md`（暗色下表面层级重排）/`visual-style-taxonomy.md`（Shape & Material 作为风格信号）/`performance-design.md`（玻璃拟态与模糊的性能价格）/`design-tokens.md`（三层 token 架构）/`accessibility.md`（WCAG 全档阈值），而是补上它们都在**用**、却没人讲清楚底层机制的第三根基础支柱：**几何（半径怎么被盒尺寸约束）、高度（elevation 到底是语义还是数值）、表面（深度用哪种信号表达）、材质（blur 与 vibrancy 的边界）、层叠（z-index 为什么不该写魔法数）**。

**一句话立场**：形状不是装饰数字，是**几何契约**；深度不是阴影，是**语义层级**。圆角会被盒尺寸按比例压缩、嵌套时受 padding 约束；elevation 是「谁在谁上面」的顺序，不是一段可以直接粘进 `box-shadow` 的 CSS；阴影只是表达深度的三种语言之一，而且在无障碍验收里**不算边界**。

**本轮三条最重要裁决**（后文逐条给官方原文、实跑计算与验收动作）：

1. **elevation 是语义 z-height，不是可直接抄写的阴影值**。M3 官方 *Component elevation* 原文：*"Elevation has no shadow or value of its own by default."* 而 `material-foundation/material-tokens` 的 `css/elevation.css` 里又写着 `box-shadow: var(--md-sys-elevation-level1)`（展开即 `box-shadow: 1px`）——MDN `box-shadow` 正式语法要求 **two, three, or four `<length>`**，单长度不是合法值。所以 `--md-sys-elevation-level*` 是**高度元数据**，把它当 CSS 阴影整段抄进项目是误读。
2. **阴影不能充当 WCAG 2.2 SC 1.4.11 的 3:1 识别边界**。官方要求识别 UI 组件/状态所必需的图形对象对 adjacent color(s) 至少 **3:1**。本轮实跑合成计算：白底上常用 `5%–12%` 黑色阴影分别只有 **1.119:1 / 1.192:1 / 1.248:1 / 1.320:1**，全部远低于 3:1；要凑到 3:1 需 `alpha ≈ 0.4176`（≈`#949494`），那已经不是"轻微投影"而是脏灰块。Understanding 文档同时给了 **3D drop-shadow 例外**（若不影响识别组件可忽略）。正解是给边界线 / focus ring / 状态形状实打实的 3:1，阴影只做附加线索。
3. **圆角是几何契约，不是"看着舒服"的常数**。`border-radius` 的百分比水平轴参照 box `width`、垂直轴参照 `height`；相邻角半径之和超过边长时规范按 `f = min(L_i/S_i)` **整体等比缩减**（`100×40` 写 `radius: 30px` 实际只生效 `20px`）；嵌套卡片要维持同心须 `r = R − p`，`r ≤ 0` 时这个公式失效而不是硬套负数。忽略这三条，设计稿与浏览器永远对不上。

---

## 1 · 为什么单列形状与深度系统

圆角 阴影 高度 材质 形状 elevation 是和色彩、排印并列的基础支柱，但此前 37 份参考里零独立文件；缺口用 `dp_search.py` 与词频统计判定为结构性空白而非覆盖不足。

**缺口实测**（本轮 `dp_search.py "圆角 阴影 高度 材质 形状 elevation"` 与 `grep -ric` 统计）：全局词频 `圆角=18`、`radius=10`、`阴影=15`、`shadow=11`、`elevation=5`，而 `高度层级=0`、`格式塔=0`、`Gestalt=0`、`视觉层级=1`、`hierarchy=3`。命中集中在三处边角：`dark-mode.md §2/§5`（表面层级与暗色阴影两派）、`design-tokens.md §2.4`（"圆角与阴影"一小节，给过 `sm/md/lg` 三层建议）、`visual-style-taxonomy.md §2.3`（Shape & Material 作为风格四维信号之一）。`performance-design.md §10` 只给玻璃拟态的性能价格，不讲几何。

上游文件都在**用**形状和深度，没人讲**它们本身怎么被浏览器计算、怎么被 WCAG 判、怎么在亮暗两套主题里保持一致**。缺了这一层，"卡片圆角 8px、阴影 0 2px 8px rgba(0,0,0,.1)"就永远是一条没有理由的口诀——换个尺寸就溢出、换个主题就看不见、过验收才发现输入框没有边界。

**与两大支柱的对照**：配色有 OKLCH 这套可计算坐标，排印有一组不可协商的可访问性边界；形状与深度同样没有"唯一正确的 8px"，但有**一组几何硬约束 + 一组语义分层契约 + 一条无障碍红线**。越界是缺陷，不是品味差异。

**边界声明**：本文件管「形与层」的机制与数值；风格取向（玻璃拟态/新拟态要不要用、算不算 AI slop）归 `visual-style-taxonomy.md §3.8/§3.9` 与 `ai-design-toolchain.md §11`；暗色下具体 tone 值归 `dark-mode.md §2`；对比度算法归 `color-science.md §6`；焦点样式归 `accessibility.md §3`。

---

## 2 · 五层模型：先判层，再谈审美

需求里出现「圆角 阴影 高度 材质 形状 elevation」时先定位是哪一层坏了；层叠与边界问题往往在 L5/L3，换圆角半径根本修不了。

| 层 | 问的问题 | 硬判据 | 主要落点 |
|---|---|---|---|
| L1 **几何** | 半径合法吗？会不会被压缩？ | `border-radius` 语法 / corner overlap `f` / concentric `r = R − p` | §10 §11 §12 §13 §14 |
| L2 **高度** | 谁在谁上面？用哪种深度语言？ | elevation 语义 / 六级刻度 / 三种语言选一 | §3 §4 §19 |
| L3 **表面** | 边界看得见吗？对比度够吗？ | 3:1 非文本 / 边界线而非阴影 / 亮暗重排 | §5 §6 §15 |
| L4 **材质** | 需不需要 blur？性能与可读性代价？ | Liquid Glass 分层 / backdrop-filter / 降级 | §16 §17 |
| L5 **层叠** | 浮层顺序对吗？会不会被父级困住？ | 语义 z-index 刻度 / stacking context / portal | §18 |

**裁决顺序**：L5 先过（层叠顺序错了，阴影再漂亮也出不来）→ L2/L3（选一种深度语言 + 边界必须 3:1，这是无障碍硬边界）→ L1（几何约束，半径不许溢出）→ L4（材质最后加，且有性能与对比度红线）→ **最后**才谈"圆润一点还是硬朗一点"。气质判断归 `visual-style-taxonomy.md §2`，本文件不越界。

---

## 3 · 裁决一：elevation 是语义 z-height，不是可直接抄写的阴影值

M3 官方 elevation 原文与 `elevation.css` 的单长度 `box-shadow` 存在误读风险；把高度 token 当 CSS 阴影抄进项目会产出无效声明。

**官方原文**（M3 *Component elevation*，2026-11-08 核验）：

> *"Elevation has no shadow or value of its own by default."*

同页明确 elevation 表达的是 **z-axis 上的相对距离 / surface order**，并给出 6 级 `dp` 刻度；另有 *"Surface tint color is deprecated."* —— 旧 M3 里"用表面染色表达高度"的做法已废弃，不要再照抄二手教程里的 `surface tint` 方案。

**源码侧的陷阱**（`material-foundation/material-tokens/css/elevation.css`，GitHub raw 实测）：

```css
--md-sys-elevation-level0: 0px;
--md-sys-elevation-level1: 1px;
--md-sys-elevation-level2: 3px;
--md-sys-elevation-level3: 6px;
--md-sys-elevation-level4: 8px;
--md-sys-elevation-level5: 12px;

.elevation-1 { box-shadow: var(--md-sys-elevation-level1); }
```

`.elevation-1` 展开是 `box-shadow: 1px`。而 MDN `box-shadow` 正式语法要求 **two, three, or four `<length>`**：两个值是 `offset-x offset-y`，第三个是 `blur-radius`，第四个是 `spread-radius`。**单长度不构成合法 `box-shadow`**，浏览器会丢弃整条声明。这份 CSS 里的 `level*` 是**高度元数据 / 供上层生成器消费的 dp 值**，不是可直接用于生产的样式片段。

**这条例外为什么重要**：网上大量"M3 elevation token"文章把 `level1=1dp / level3=6dp` 直接写成 `box-shadow: 0 6px 6px`，属于把语义高度误当模糊半径。正确的映射是：**先定这个组件在第几层（语义）→ 再按本项目的深度语言选阴影层/表面色/材质（表现）**，两者之间是一次显式设计决策，不是数值拷贝。

**验收动作**：搜项目里所有 `box-shadow:` 声明，凡只有一个 `<length>` 的一律判无效；凡 `--*-elevation-level*` 变量被直接塞进 `box-shadow` 的，改为语义类名或一层完整的阴影 token。见 §23.5 静态扫描。

---

## 4 · M3 Elevation 六级精确表与组件映射

M3 component elevation 官方表给出 6 级高度 `level0–level5` / `dp`：`0 / 1 / 3 / 6 / 8 / 12`；这是层级顺序不是阴影参数。

| Level | 高度（dp） | 语义 | 典型落点（设计侧） |
|---|---|---|---|
| level0 | 0 | 贴在页面基底上 | 正文区、表格行、无边界内容块 |
| level1 | 1 | 轻微可辨的独立面 | 卡片静态态、分组容器、App bar（滚动前） |
| level2 | 3 | 明确的浮起 | 悬浮按钮静态态、被拖起前的卡片、sticky 元素 |
| level3 | 6 | 交互抬起 | hover / focus / drag 态、dropdown 菜单 |
| level4 | 8 | 覆盖内容 | modal / dialog、侧滑抽屉 |
| level5 | 12 | 最高临时层 | toast / snackbar、tooltip、全局浮层 |

**三条纪律**：

1. **dp 不进 `box-shadow`**。上表是"第几层"，不是 `offset-y` 或 `blur`。要转成 CSS，必须走 §8 里某一套完整阴影配方。
2. **高度差要能解释**。level1 的卡片 hover 到 level3 是一次**有语义的抬起**（用户操作引起），不是"顺手把阴影调浓"。同一组件在亮/暗两套主题里应保持**同一 level**，只换表达语言（亮色阴影 / 暗色表面提亮 + 轻阴影），见 `dark-mode.md §5`。
3. **层级数不要超过 6**。超过 6 档人眼分辨不出，只会让 token 表膨胀；`impeccable` 的 `spatial-design.md` 给的是更克制的 `sm → md → lg → xl` 四档一致 elevation scale，本项目若无 Material 兼容要求，四档更实用。该文档原话：*"Shadows should be subtle—if you can clearly see it, it's probably too strong."*

---

## 5 · 裁决二：阴影不能充当 WCAG 1.4.11 的 3:1 识别边界

WCAG 2.2 SC 1.4.11 非文本对比度要求组件边界对相邻色至少 3:1；本轮用 WCAG 相对亮度公式实跑证明常用半透明阴影只到 1.1–1.3:1，不能算边界。

**官方口径**（W3C WCAG 2.2 Understanding SC 1.4.11 Non-text Contrast）：识别 UI 组件及其状态、或理解内容所必需的图形对象，对 **adjacent color(s)** 至少 **3:1**。对比度**不四舍五入**（`2.999:1` 依然不通过，这是对比度判定的通用纪律）。Understanding 同时给出 **3D drop-shadow 例外**：若投影只是立体装饰、去掉后仍不影响识别组件，则这类阴影可被忽略——反过来说明"靠阴影当边界"根本不在条款的保护范围内。焦点指示器另需足够对比度，不能因为"有阴影"就免检。

**实跑合成计算**：白底 `#FFFFFF`，阴影为纯黑 `rgb(0,0,0)` 以 alpha 叠加，合成色 `c = 255 × (1 − α)`；用 WCAG 相对亮度 `L = 0.2126R + 0.7152G + 0.0722B`（sRGB 线性化）算 `ratio = (L_light + 0.05) / (L_dark + 0.05)`。

| alpha | 合成色 | 对白底对比度 | 判定 |
|---|---|---|---|
| 0.05 | `#F2F2F2` | **1.119:1** | 远不足 3:1 |
| 0.08 | `#EBEBEB` | **1.192:1** | 远不足 3:1 |
| 0.10 | `#E6E6E6` | **1.248:1** | 远不足 3:1 |
| 0.12 | `#E0E0E0` | **1.320:1** | 远不足 3:1 |
| 0.20 | `#CCCCCC` | **1.606:1** | 不足 3:1 |
| 0.25 | `#BFBFBF` | **1.839:1** | 不足 3:1 |
| 0.42 | `#949494` | **3.033:1** | 刚过，但已不是轻投影 |

**反解**：白底上要靠纯黑半透明达到 3:1，需 **`alpha ≈ 0.4176`**，合成色约 `#949494`。也就是说：想让阴影同时满足"轻微悬浮感"和"3:1 边界"，在这套坐标系里**不可能**。这两个目标必须拆成两个元素：边界线负责合规，阴影负责氛围。

**为什么这条经常被漏**：Tailwind v4 的 `shadow-sm` 是 `0 1px 3px 0 rgb(0 0 0 / 0.1)`，MUI 的 umbra 是 `rgba(0,0,0,0.2)`，TDesign `--td-shadow-1` 三层里最低 5%、最高 12%——**所有主流体系的"轻阴影"都在 5%–20% 区间**，对应 1.1–1.6:1。一个纯白卡片放在纯白背景上、只靠阴影区分，在 WCAG 口径下等于**没有边界**。设计评审里"这个卡片浮起来了"与"这个卡片可识别"是两件事。

**结论**：阴影是**附加线索（supplementary cue）**，不是唯一线索。任何需要被识别的组件/状态，必须有独立满足 3:1 的边界信号。

---

## 6 · 非文本 3:1 的正确落点（边界 / 焦点 / 状态）

输入框 按钮 开关 边界线 焦点框 阴影 对比度 3:1 的合规信号必须是独立元素；阴影只做叠加氛围，不承担识别责任。

| 需要识别的对象 | 合规做法 | 常见错法 |
|---|---|---|
| 输入框边界 | `1px solid` 且对背景 ≥3:1（暗色下 `#424242` 仅 2.09:1 是已知陷阱，见 `dark-mode.md §4`） | 只给 `box-shadow: 0 1px 3px rgba(0,0,0,.1)` |
| 按钮边界（次要/描边按钮） | 描边色 ≥3:1；填充按钮靠填充色与背景 ≥3:1 | 白底白按钮 + 轻微投影 |
| 开关 / 复选框 / 单选 | 轨道或外框 ≥3:1，且状态不只靠颜色 | 只换填充色、外框 1.2:1 |
| 焦点指示器 | 独立 focus ring ≥3:1；Carbon 通常用 `2px border` | `outline: none` + 用阴影代替焦点 |
| 图表 / 状态图形 | 图形对象与相邻色 ≥3:1 | 细灰线 + 投影 |
| 卡片与页面基底的**可区分性** | 用表面色阶差（≥3:1 只在需要识别时强制）或**真实描边** | 同色 + 阴影 |

**两条判据**：① 关掉 CSS 里的 `box-shadow` 与 `filter`，组件还认得出来吗？认不出 → 违规。② 把组件截图转灰度、降对比到 50%，边界还在吗？不在 → 违规。这两步是比"看设计稿"更可靠的验收。

**与既有文件的分工**：完整 WCAG 阈值档位、焦点三层标准、24px 圆间距例外在 `accessibility.md §2/§3`；暗色下的边界实测值在 `dark-mode.md §4`；APCA 与 WCAG 双算法在 `color-science.md §6`。本文件只负责裁定"阴影不算边界"这一条。

---

## 7 · `box-shadow` 正式语法（MDN 逐条核验）

`box-shadow` 需要 2/3/4 个 `<length>`：`offset-x offset-y [blur-radius [spread-radius]]`；多阴影逗号分隔且第一个在最上，不占布局空间，跟随圆角。

| 长度个数 | 依次含义 | 例子 |
|---|---|---|
| 2 | `offset-x` `offset-y` | `0 2px` |
| 3 | + `blur-radius` | `0 2px 8px` |
| 4 | + `spread-radius` | `0 2px 8px -1px` |
| 1 | **非法** | `1px`（§3 的 M3 token 陷阱） |

**其余规则**：

- `color` 可选，可写在长度之前或之后；省略时用 `currentColor`（各 UA 措辞略有差异，生产显式写颜色）。
- `inset` 把外阴影变内阴影；可与其他层混用，但同一组件不要内外同时用（视觉语义打架）。
- 多个阴影用逗号分隔，**书写顺序里第一个绘制在最上层**（不是最后）。三层配方里通常把最紧、最暗的 umbra 放第一层。
- `blur-radius` 不能为负；`spread-radius` 可负（内收）。
- **不影响 box model**：阴影不占空间、不触发布局、不改变元素尺寸；因此它天然不能承担"边界"职责（边界必须占一个可测的视觉位置）。
- 元素有 `border-radius` 时，外阴影**跟随圆角**；内阴影同样受圆角裁剪。所以圆角与阴影必须成套定义，改一个要复核另一个。
- 阴影会被 `overflow: hidden` 的祖先、`filter`/`opacity`/`transform` 创建的 stacking context 裁剪或改变合成顺序，见 §18。

---

## 8 · 七体系阴影 token 精确对照（源码 / 官方文档实测）

真实说法：「Tailwind shadow-md 默认值到底是多少」「Ant Design 圆角和阴影默认值抄哪」——下表把 Tailwind v4 / MUI / Ant Design 5 / TDesign / Arco / Carbon / M3 的阴影默认值与结构逐项对照；数值均为官方原文或 GitHub 源码实测，不抄二手表格。

### 8.1 Tailwind CSS v4（`box-shadow` 官方文档逐字）

| 类 | 精确值 |
|---|---|
| `shadow-2xs` | `0 1px rgb(0 0 0 / 0.05)` |
| `shadow-xs` | `0 1px 2px 0 rgb(0 0 0 / 0.05)` |
| `shadow-sm` | `0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)` |
| `shadow-md` | `0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)` |
| `shadow-lg` | `0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)` |
| `shadow-xl` | `0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)` |
| `shadow-2xl` | `0 25px 50px -12px rgb(0 0 0 / 0.25)` |
| `shadow-none` | `0 0 #0000` |

v4 把这些值放在 `--shadow-*` 自定义属性里，可用 `shadow-(<custom-property>)` 直接接自己的变量——这是把深度 token 化的最低成本路径。注意 `shadow-2xl` 的 alpha 跳到 `0.25`，跨档不是线性递增，别自己按等差补档。

### 8.2 MUI（`packages/mui-material/src/styles/shadows.js` 源码实测）

```javascript
const shadowKeyUmbraOpacity = 0.2;
const shadowKeyPenumbraOpacity = 0.14;
const shadowAmbientShadowOpacity = 0.12;
// createShadow(...px) → 3 层：umbra / penumbra / ambient
// shadows[1] = createShadow(0, 2, 1, -1, 0, 1, 1, 0, 0, 1, 3, 0)
```

共 **25 档**（`shadows[0] = 'none'`，其后 24 档）。三个固定 alpha 对应物理分解：**umbra**（本影，最紧最暗 0.20）、**penumbra**（半影 0.14）、**ambient**（环境光 0.12）。这解释了"为什么专业体系都是三层阴影"——不是审美偏好，是在模拟一个光源产生的三种遮挡。25 档过密，产品里实际只用 3–5 档。

### 8.3 Ant Design 5（`customize-theme` 官方表逐字）

| Token | 默认值 |
|---|---|
| `boxShadow` | `0 6px 16px 0 rgba(0,0,0,0.08), 0 3px 6px -4px rgba(0,0,0,0.12), 0 9px 28px 8px rgba(0,0,0,0.05)` |
| `boxShadowSecondary` | 与 `boxShadow` **完全相同** |

同为三层，alpha 分别 `0.08 / 0.12 / 0.05`，比 MUI 更淡。注意 `spread` 一负一正（`-4px` / `8px`）：第三层用正 spread 做大范围柔光，这是"淡但不糊"的关键。

### 8.4 TDesign（`Tencent/tdesign-common/style/web/theme/_light.less` 源码实测）

```less
--td-shadow-1: 0 1px 10px rgba(0, 0, 0, 5%), 0 4px 5px rgba(0, 0, 0, 8%), 0 2px 4px -1px rgba(0, 0, 0, 12%);
--td-shadow-2: 0 3px 14px 2px rgba(0, 0, 0, 5%), 0 8px 10px 1px rgba(0, 0, 0, 6%), 0 5px 5px -3px rgba(0, 0, 0, 10%);
--td-shadow-3: 0 6px 30px 5px rgba(0, 0, 0, 5%), 0 16px 24px 2px rgba(0, 0, 0, 4%), 0 8px 10px -5px rgba(0, 0, 0, 8%);
```

**TDesign 只有 3 档**，且档位越高 alpha 反而越淡（5%→4%）——靠更大的 blur / spread 拉开距离感，而不是把阴影加黑。这是与 MUI/Tailwind 不同的思路，直接混用两套会打架。官方设计 token 页原文把 system token 分为 5 类：*"color、font、border-radius、box-shadow and size"*。

### 8.5 Arco Design（官方 token 页）

阴影 token 名为 `shadow-special`、`shadow1-center`、`shadow2-center`、`shadow3-center`（"center" 表示无 y 偏移的四周扩散型）。**取源限制**：本轮抓取返回的是变量名与分类，未取得逐字完整字符串，因此此处只登记结构与命名，不臆造数值；需要精确值时以项目内 `@arco-design/web-react` 的 token 文件为准。

### 8.6 Carbon（不用阴影表达层级）

Carbon *Layering* 明确用 **neutral gray palette 的 layered colors** 表达 depth / spatial association，而非投影：light themes 在 `White ↔ Gray 10` 之间交替，dark themes 每加一层变浅一个 step。focus 通常是 `2px border` 且需 3:1。这意味着 Carbon 系项目里"卡片浮起来"是**表面色阶差**，不是阴影强度差。

### 8.7 M3（语义高度 + 已废弃的 surface tint）

见 §3 §4。M3 现代表达是"语义 level + 表面色角色"，`Surface tint color is deprecated.`。

### 8.8 横向结论

| 体系 | 档数 | 层数 | alpha 区间 | 深度语言 |
|---|---|---|---|---|
| Tailwind v4 | 7 + none | 1–2 | 0.05–0.25 | 阴影 |
| MUI | 25 | 3 | 0.12–0.20 | 阴影（物理三层） |
| Ant Design 5 | 2（值相同） | 3 | 0.05–0.12 | 阴影 |
| TDesign | 3 | 3 | 0.04–0.12 | 阴影（高等级更淡更大） |
| Arco | 4 名 | — | 本轮未取 | 阴影（center 型） |
| Carbon | 层次色阶 | 0 | — | **表面色** |
| Apple | materials | 0 | — | **材质 + 分层** |

**没有一套是"通用正确"的**。选型先定语言（§19），再从这一套里取完整值；把 Tailwind 的 `shadow-sm` 和 TDesign 的 `--td-shadow-3` 混在同一页面，等于两套光源模型打架。

---

## 9 · 三层阴影为什么够：物理分解与克制原则

三层阴影 umbra penumbra ambient 对应一个光源的三种遮挡；阴影应当 subtle，看得清就说明太重——这是 `impeccable/spatial-design.md` 的原文立场。

一个不透明物体在单一光源下产生：紧贴合的**本影**（锐利、暗、偏移小）、过渡的**半影**（较柔、稍大）、以及整体环境光被遮挡形成的**环境阴影**（最扩散、最淡）。MUI 的 `0.2 / 0.14 / 0.12` 就是这三者的固定权重；Ant 的 `0.08 / 0.12 / 0.05` 与 TDesign 的 `5% / 8% / 12%` 只是同一模型的不同调参。

**克制原则**（`impeccable` `spatial-design.md` 原文）：

> *"Create semantic z-index scales (dropdown → sticky → modal-backdrop → modal → toast → tooltip) instead of arbitrary numbers. For shadows, create a consistent elevation scale (sm → md → lg → xl). **Key insight**: Shadows should be subtle—if you can clearly see it, it's probably too strong."*

**三条落地纪律**：① 一个项目只用**一套**三层配方，档位差靠 `offset-y / blur / spread` 缩放，不靠改 alpha 或换色相。② 阴影颜色用**中性黑/深灰**，不要用品牌色投影（会脏，且在暗色下偏色）。③ 层级差 ≥2 档才需要动阴影；相邻两档（level1 ↔ level2）用户几乎看不出，别为它加一档 token。

---

## 10 · 裁决三：圆角是几何契约，不是装饰常数

`border-radius` 正式语法是 `<length-percentage[0,∞]>{1,4} [ / <length-percentage[0,∞]>{1,4} ]?`；百分比水平轴参照 width、垂直轴参照 height，负值无效。

**语法拆解**：

- 斜杠前 1–4 个值 = 四角的**水平半径**，按 CSS 常规顺序（TL / TR / BR / BL）展开；斜杠后 1–4 个值 = **垂直半径**。
- 有斜杠可形成**椭圆角（elliptical corners）**：`border-radius: 40px / 20px` 的角是横向 40、纵向 20 的椭圆，不是圆。
- `<length-percentage>` 的 `[0,∞]` 约束意味着**负值无效**，整条声明会被丢弃。
- 百分比：水平半径参照 box 的 **width**，垂直半径参照 **height**。所以 `border-radius: 50%` 在 `200×100` 的盒子上不是"半径 100px 的圆角"，而是水平 100px、垂直 50px 的椭圆角；要得到正圆胶囊得用足够大的长度值（如 `999px`，由 §11 的 overlap 规则兜底）或 `50%` 配合正方形。
- `border-radius: 50%` 写在正方形上是圆，写在矩形上是椭圆——这是 `avatar` 必须锁 1:1 宽高比的根本原因。

**设计后果**：圆角值不能脱离盒尺寸讨论。"这套卡片统一 16px 圆角"在 `320×64` 的横幅和 `100×40` 的小标签上视觉完全不同（后者已接近全圆）。设计交付应同时给出**半径 token 与适用尺寸带**，而不是一个全局常数。

---

## 11 · Corner overlap：半径按比例缩减的规范公式

圆角重叠 corner overlap 的规范处理是 `f = min(L_i / S_i)`，`f < 1` 时所有角半径乘 `f` 等比缩减；实跑验证 `100×40` 写 `30px` 只生效 `20px`。

当同一条边上相邻两角的半径之和超过该边长度时，浏览器不会裁掉某个角，而是**把所有角的半径整体乘一个系数 `f`**：

```
f = min( L_i / S_i )     # L_i = 第 i 条边长；S_i = 该边两端角半径之和
若 f < 1：所有 radius *= f
```

**本轮 Python 实跑结果**（统一四角半径）：

| box 尺寸 | 声明 radius | f | 实际生效 |
|---|---|---|---|
| `100×40` | 30px | 0.6667 | **20.00px** |
| `100×40` | 50px | 0.4000 | **20.00px** |
| `320×64` | 40px | 0.8000 | **32.00px** |
| `120×120` | 80px | 0.7500 | **60.00px** |

注意前两行：声明 30 和声明 50 得到**完全相同**的 20px。也就是说超过临界值后继续加大圆角**毫无效果**，只会在设计稿与实现之间制造"我明明写了 50"的争执。

**临界值速算**：四角同半径 `r` 的盒子，`min(w,h)/2` 就是有效上限。`100×40` → 20px；`320×64` → 32px；`120×120` → 60px。想要更大的圆角，只能改盒子尺寸或改成胶囊（用 `999px` 让 overlap 自己收敛到 `min(w,h)/2`）。

**取源限制（诚实记录）**：本轮 `https://www.w3.org/TR/css-backgrounds-3/#corner-overlap` 抓取被 Cloudflare 挑战页拦截（*"Just a moment..."*），`drafts.csswg.org` 的抓取片段也未包含 §4.5 正文。因此 `f = min(L_i/S_i)` 是随附规范说明给出的常见原文公式，本轮**已用本地 Python 实跑验证其数值行为**，但**未从 W3C TR 页面逐字核验**。写入时按"公式 + 实跑验证"标注，不声称逐字引自 TR 正文。

---

## 12 · 嵌套同心圆角 `r = R − p` 与失效条件

嵌套圆角 同心圆角 concentric radius 的规则是内圆角 `r = R − p`；`r ≤ 0` 时公式失效，不能硬套负数。

当卡片里再嵌一个带内边距的容器（输入框、图片、次级卡片），两层弧线要**同心**才不别扭：

```
R = 外层圆角，p = 外容器 padding（内边距）
r = R − p
```

**本轮实跑校验**：

| 外层 R | padding | 内层 r | 判定 |
|---|---|---|---|
| 16 | 8 | 8 | OK 同心 |
| 28 | 12 | 16 | OK 同心 |
| 8 | 4 | 4 | OK 同心 |
| 12 | 16 | **−4** | **INVALID** |

最后一行是最常见的真实事故：外层 `12px` 圆角、内边距 `16px`，按公式内层应为 −4px（不存在）。此时正确处置不是写 `0` 硬凑，而是**三选一**：① 减小 padding 到 ≤ R；② 增大外层 R；③ 去掉内层圆角，让内容区直接以直边收口并靠 padding 留白。写成 `0` 会让两层弧线在视觉上"错位"，是卡片套卡片显得廉价的典型来源。

**与 §11 联动**：内层盒子尺寸更小，`min(w,h)/2` 上限也更低；算完 `r` 还要再过一次 overlap 检查。嵌套越深，可用半径越小——这也是 `impeccable` 把「卡片套卡片」列为 DON'T 的几何理由，不只是审美判断。

---

## 13 · 七体系圆角 token 精确对照与 M3 Expressive 更新

真实说法：「定一套圆角 token 该有几档」「形状尺度怎么定」——圆角 token 对照：M3 `4/8/12/16/28`、TDesign `2/3/6/9/12/999`、Ant `2/4/6/8`、Arco `0/2/4/8`；M3 Expressive 2025-05 新增 35 shapes 并改用 `full`。

### 13.1 精确值（官方原文 / 源码实测）

| 体系 | token 与值 | 来源 |
|---|---|---|
| **M3** | `corner-none 0` · `extra-small 4px` · `small 8px` · `medium 12px` · `large 16px` · `extra-large 28px` · `corner-full-family 3px` | `material-foundation/material-tokens/css/shape.css` GitHub raw 实测 |
| **TDesign** | `small 2px` · `default 3px` · `medium 6px` · `large 9px` · `extraLarge 12px` · `round 999px` · `circle 50%` | `Tencent/tdesign-common/style/web/theme/_radius.less` 实测 |
| **Ant Design 5** | `borderRadiusXS 2` · `SM 4` · `borderRadius 6` · `LG 8` · `Outer 4` · `controlHeight 32` | 官方 `customize-theme` Seed/Map Token 表逐字 |
| **Arco** | `none 0` · `small 2px` · `medium 4px` · `large 8px` · `circle 50%` | 官方 token 页「边框圆角」段 |
| **Material Web** | 支持 `corner-extra-large / extra-small / full / large / medium / none / small`，并派生 `*-top` 等 shorthand | `tokens/_md-sys-shape.scss` `$supported-tokens` 实测 |
| **Carbon** | 以 `0` 直角为基调（sharp corners 是品牌识别信号） | Carbon 视觉语言；不用圆角表达层级 |
| **Tailwind v4** | `rounded-xs/sm/md/lg/xl/2xl/3xl/full` 等，值由 `--radius-*` 变量驱动 | 官方 radius 文档（本轮未逐字抄全表） |

**观察**：国内体系（Ant 6 / TDesign 3 / Arco 4）的默认圆角明显**小于** M3（medium 12 / large 16）。这不是"谁更现代"，是信息密度不同：中后台表格、表单密集，大圆角会吞掉可用空间并让相邻控件看起来松散。跨体系抄值前先确认信息密度。

### 13.2 M3 Expressive（2025-05）更新要点

- 新增 **35 个 shapes** 与 **shape morphing**（形状在状态间平滑变形）。
- 尺寸档上调：`Large increased (20dp)`、`Extra large increased (32dp)`、`Extra extra large (48dp)`。
- `full` **取代**旧的 `50%` fully rounded 定义。
- 官方页面明确 **"Web is not currently available"** —— shape library 与 morphing 目前没有 Web 端实现，**不要在 Web 项目里假装已经能用**。

**取源限制**：M3 `styles/shape/shape-scale-tokens` 页面本轮返回的是 Shape / Shape morph / Shape library 说明，**未返回期望的精确 shape scale token 表**；上表 M3 精确值来自静态 `material-tokens/css/shape.css`，与 Expressive 的动态 scale 不是同一套，不要混为一谈。

---

## 14 · `corner-shape` 与 squircle：实验特性，不进生产

`corner-shape` 是 MDN 标记为 Experimental 的属性，依赖 `border-radius`；没有有效 `border-radius` 或解析为 `0` 时完全不生效。

| 值 | 效果 |
|---|---|
| `round` | 默认圆弧 |
| `squircle` | 超椭圆，介于圆与方之间（Apple 图标常用轮廓） |
| `superellipse()` | 可指定参数化超椭圆 |
| `scoop` | 内凹 |
| `bevel` | 斜切 |
| `notch` | 缺口 |
| `square` | 直角 |

**三条纪律**：① Experimental 意味着浏览器支持不完整且语法可能变，**生产必须能力检测 + 回退到 `round`**。② 它依赖 `border-radius` 提供尺寸，`border-radius: 0` 时 `corner-shape: squircle` 什么也不会发生——这是最常见的"我写了怎么没效果"。③ 设计稿里若出现 squircle，交付时要同时给 `border-radius` 数值与 `@supports (corner-shape: squircle)` 的渐进增强路径，别让开发以为是普通圆角。

---

## 15 · 表面层级：不用阴影也能表达深度（Carbon 与暗色重排）

表面层级 surface layering 的第二条路线是用中性灰色阶交替，而非投影；亮色 `White ↔ Gray 10` 交替、暗色每加一层变浅一个 step。

**Carbon Layering** 的立场是：depth 与 spatial association 应由 **layered colors** 表达。具体做法：

- Light themes：基础层 `White`，上一层次 `Gray 10`，再上一层回到 `White`，**交替**而非单调变深。
- Dark themes：每加一层，表面色变浅一个 step（暗色下"更亮 = 更靠前"）。
- 好处：不依赖光源方向、在任意背景上都稳定、不受 `overflow: hidden` 裁剪、天然带可测的色差（比 1.2:1 的阴影更能支撑边界识别）。

**暗色模式的重排**（与 `dark-mode.md §2/§5` 对齐）：亮色靠阴影、暗色靠**提亮表面**。直接把亮色阴影搬到暗底几乎不可见（黑上黑），所以暗色必须"重排"而不是"反相"：把 level1→level5 映射为逐级变亮的表面色，阴影只保留极轻的一层作辅助。`dark-mode.md §5.2` 给过高度与表面值的对照表，本文件不重复数值。

**三种语言只能选一种主导**（§19）：一个界面里同时出现"阴影深度的卡片""表面色深度的侧栏""毛玻璃深度的顶栏"，用户读到的是三套互相矛盾的物理规则。`visual-style-taxonomy.md §5` 的「材质语言只一种主导、装饰密度只一个极端、趋势叠加上限 = 1」在这里同样成立。

---

## 16 · 材质与玻璃：Apple HIG Materials / Liquid Glass 的分层边界

材质 毛玻璃 Liquid Glass 只用于 controls / navigation 的 functional layer，不要用于 content layer；`clear` 变体在明亮背景上建议加 35% 暗色 dimming layer。

**Apple HIG Materials 官方要点**（2026-11-08 核验）：

- 材质分两类：**Liquid Glass**（动态、带折射与高光）与 **standard materials**（`ultra-thin / thin / regular / thick` 四档静态模糊）。
- 两者都有 `regular` 与 `clear` variant。
- **Liquid Glass 属于 functional layer**：用于控件、导航栏、工具栏等浮在内容之上的功能层；**不要用在 content layer**（正文、卡片主体、图像内容）。把内容本身做成玻璃，可读性和性能都会崩。
- `clear` 变体在明亮背景上对比不足，官方建议在材质下加一层约 **35% opacity 的 dark dimming layer** 保证内容可读。
- 避免 `quaternary` 标签色配 `thin` / `ultraThin` 材质的低对比组合。

**设计侧翻译**：玻璃是**"层和内容的隔离膜"**，不是"卡片样式"。判定句式：这个元素是不是**覆盖在滚动内容之上、且需要让人隐约看到底下有什么**？是 → 可考虑材质；否（它本身就是内容）→ 用实色表面。

**与 `visual-style-taxonomy.md §3.9` 的硬红线一致**：玻璃拟态文字 ≥4.5:1、正文密集区禁用、`backdrop-filter` 须测低端机成本。本文件补的是**分层位置**（functional vs content），两者叠加才是完整判据。

---

## 17 · 玻璃拟态的合成开销与降级顺序

玻璃拟态的真实代价在每帧对背景区域重采样；降级顺序是「减层数与半径 → 加暗色遮罩 → 换实色表面」，不是只去掉透明度。

| 风险 | 机制 | 检查点 |
|---|---|---|
| 合成成本 | 每帧对背景区域重采样 + 模糊，滚动时持续触发；多层叠加成本近似叠加 | 低端机实测帧时间；`performance-design.md §10` 把玻璃拟态列为高价手法 |
| 文字可读 | 半透明材质让文字与背景同时透过，`4.5:1` 失去稳定参照 | 取材质合成后的**实际像素**算对比度，不拿设计稿的纯色算 |
| 层数失控 | 每个浮层都加 blur，视觉糊成一团 | 一个视图内材质层 ≤1（顶栏或侧栏二选一） |
| 降级缺失 | 不支持 `backdrop-filter` 时变成纯透明 → 文字消失 | `@supports not (backdrop-filter: blur(1px))` 给实色回退 |
| 系统偏好 | 用户开启降低透明度时仍强推玻璃 | 尊重系统 reduce transparency / 高对比模式 |

**降级顺序**：性能或可读性出问题 → ① 降低 blur 半径与层数 → ② 提高材质不透明度 / 加 dimming layer → ③ 换回实色表面（保留同一层级语义，见 §15）。**不要**直接去掉 `backdrop-filter` 而保留半透明背景，那是最糟的中间态。

---

## 18 · z-index 语义刻度与 stacking context

z-index 不该写魔法数；用 `dropdown → sticky → modal-backdrop → modal → toast → tooltip` 的语义刻度，并检查父级 stacking context。

**语义刻度**（`impeccable` `spatial-design.md` 原文给出的顺序）：

```
0        base / 页面内容
100      dropdown · popover
200      sticky header · sticky column
300      modal-backdrop（遮罩）
400      modal · dialog · drawer
500      toast · snackbar
600      tooltip
```

命名成 token（`--z-dropdown` 等）而非散落的 `z-index: 9999`。判据：**任何一个 `z-index` 数值都应能在刻度表里查到出处**；出现 `9999` / `100000` 说明层级已经失控。

**stacking context 三条常踩的坑**：① 父元素上的 `transform` / `opacity < 1` / `filter` / `will-change` / `isolation: isolate` 会创建新的层叠上下文，子元素的 `z-index` **只在父上下文内比较**，再大也盖不过父级之外的兄弟。② `position` 非 `static` 且 `z-index` 非 `auto` 才参与；flex/grid item 即使 `position: static` 也可因 `z-index` 生效。③ Portal / 浮层渲染到 `document.body` 就是为了逃出父上下文——`multi-brand-theming.md` 记录过 "portal 逃逸" 的主题变量问题，两者要一起查。

**与阴影联动**：`overflow: hidden` 的祖先会裁掉外阴影，所以"卡片 hover 抬起"若父级是滚动容器，阴影会被切一半。这不是阴影参数问题，是层叠与布局结构问题（§2 的 L5 优先）。

---

## 19 · 深度语言三选一：阴影 / 表面色 / 材质

深度语言 阴影 表面色 材质 必须三选一做主导；混用三套等于给界面三套互相矛盾的光源与物理规则。

| 语言 | 表达机制 | 适用 | 不适用 | 代表体系 |
|---|---|---|---|---|
| **阴影** | 投影的偏移/模糊/透明 | 浅色、有明确光源隐喻、浮层少的消费级产品 | 暗色主界面、密集表格 | Tailwind / MUI / Ant / TDesign |
| **表面色阶** | 中性灰阶交替、暗色逐级提亮 | 中后台、信息密集、需要稳定可测边界、双主题 | 需要强烈"浮起"动效的场景 | Carbon / M3（现代） |
| **材质** | blur / vibrancy / 折射 | 覆盖在滚动内容上的功能层（顶栏、工具栏） | 内容层、正文密集区、低端机 | Apple HIG |

**决策顺序**：① 先看明暗与信息密度（暗色 / 高密度 → 表面色阶）；② 再看是否有"覆盖在内容之上"的功能层（有 → 仅该层可加材质，且 ≤1 处）；③ 最后决定要不要用阴影做交互抬起的**动效线索**（可以，但它是第四层辅助，不是深度语言本身）。

**一致性验收**：把界面截图转灰度并关掉 `box-shadow`，层级还读得出来 → 用的是表面色阶（稳）；读不出来 → 全靠阴影（脆）。后者在暗色模式、高对比模式、低端机降级时都会失效。

---

## 20 · 场景速查（12）

| # | 场景 | 先判层 | 动作 | 验收 |
|---|---|---|---|---|
| 1 | 白底白卡片"浮起来"但看不出边界 | L3 | 加 3:1 描边或表面色阶差，阴影保留为氛围 | 关 `box-shadow` 后仍可识别 |
| 2 | 卡片圆角写了 24px，小尺寸下像全圆 | L1 | 按 `min(w,h)/2` 复核 overlap，按尺寸带分档 | 实跑 `f` 计算器 |
| 3 | 卡片里嵌输入框，两层弧线错位 | L1 | `r = R − p`，`r ≤ 0` 时减 padding / 增 R / 去内圆角 | 同心校验器 PASS |
| 4 | 暗色下弹窗"不够前" | L2/L3 | 重排为表面提亮 + 极轻阴影，不照搬亮色阴影 | 亮暗两套同 level |
| 5 | 输入框只靠浅阴影，无障碍验收挂了 | L3 | 补 ≥3:1 描边；阴影不算边界 | 灰度 + 去阴影双测 |
| 6 | 焦点框被 `outline:none` 杀掉，改用阴影 | L3 | 独立 focus ring ≥3:1，Carbon 用 `2px border` | 键盘 Tab 全路径 |
| 7 | 顶栏想上毛玻璃 | L4 | 确认它是 functional layer；≤1 处；文字按合成像素验 4.5:1 | 低端机帧时间 + 降级路径 |
| 8 | 玻璃上文字发虚 / 背景太亮 | L4 | 加 35% dark dimming layer 或换 `regular` 变体 | 合成后实测对比度 |
| 9 | 项目里出现 `z-index: 99999` | L5 | 收回语义刻度表，用 token 命名 | 全量 `z-index` 可查出处 |
| 10 | 弹窗阴影被父容器切掉一半 | L5 | 检查 `overflow:hidden` 与 stacking context，必要时 portal | 滚动容器内 hover 抬起 |
| 11 | 从 M3 抄 `level3 = 6dp` 写成 `box-shadow: 0 6px 6px` | L2 | 区分语义高度与阴影参数，取完整三层配方 | 无单长度 `box-shadow` |
| 12 | 同一页面混 Tailwind `shadow-sm` 与 TDesign `--td-shadow-3` | L2 | 选一套深度语言并重定档 | 一套配方、3–5 档 |

---

## 21 · 反模式（20）

1. **把阴影当 3:1 边界**——白底白卡只加 `rgba(0,0,0,.1)`，实测 1.248:1，验收必挂。
2. **单长度 `box-shadow`**——`box-shadow: 1px` 是非法声明，浏览器直接丢弃。
3. **把 elevation 的 dp 数值当 `blur` / `offset-y` 抄**——语义高度不是 CSS 参数。
4. **照抄已废弃的 `surface tint`**——M3 官方 *"Surface tint color is deprecated."*。
5. **`border-radius` 用负值**——`[0,∞]` 约束下整条声明无效。
6. **矩形上写 `50%` 以为是正圆**——水平参照 width、垂直参照 height，得到的是椭圆。
7. **无视 corner overlap 继续加大半径**——`100×40` 写 30px 与 50px 结果都是 20px。
8. **嵌套圆角硬套 `r = R − p` 得到负数还写进代码**——CSS 无负半径，视觉必然错位。
9. **卡片套卡片层层加圆角**——既是 `impeccable` 的 DON'T，也是几何上半径逐层失效。
10. **一个项目混两套阴影体系**——两套光源模型、两套 alpha 调参，档位无法互译。
11. **阴影用品牌色**——亮色下发脏、暗色下偏色，且污染对比度计算。
12. **阴影加到"一眼能清楚看见"**——`impeccable` 原文：看得清通常就是太重。
13. **层级分 10 档以上**——人眼分辨不出，只让 token 表膨胀；3–5 档足够。
14. **暗色模式把亮色阴影原样搬过去**——黑上黑几乎不可见，正确做法是表面提亮重排。
15. **内容层用 Liquid Glass**——官方明确材质属 functional layer，内容层用了可读性与性能双崩。
16. **多处叠加 `backdrop-filter`**——一个视图内材质层 >1，滚动时帧时间线性上升。
17. **不支持 `backdrop-filter` 时留半透明背景**——降级最糟中间态，文字直接消失。
18. **`z-index` 写魔法数**——`9999` 之后只能继续加 9，层级最终失控。
19. **忽略父级 stacking context**——父元素 `transform` / `opacity` 让子元素再大的 z 也出不去。
20. **`corner-shape: squircle` 配 `border-radius: 0`**——实验属性依赖有效半径，写了等于没写。

---

## 22 · 自检（20）

1. 项目里所有 `box-shadow` 都至少含 2 个 `<length>` 吗？
2. 有没有把 `--*-elevation-level*` 直接塞进 `box-shadow`？
3. elevation 是作为语义 level 定义、而非 CSS 数值拷贝的吗？
4. 每个需要识别的组件，关掉阴影后仍 ≥3:1 可辨吗？
5. 输入框 / 开关 / 次要按钮的边界有独立 ≥3:1 信号吗？
6. 焦点指示器是独立 focus ring、且 ≥3:1 吗？
7. 圆角 token 是否标注了适用尺寸带（而非全局一个常数）？
8. 所有 `border-radius` 都过了 `min(w,h)/2` 上限检查吗？
9. 百分比圆角是否确认了水平参照 width / 垂直参照 height？
10. 嵌套容器是否按 `r = R − p` 校验，且没有 `r ≤ 0` 的硬套？
11. 全站只用一套深度语言（阴影 / 表面色 / 材质）作主导吗？
12. 阴影是否成套定义（层数、alpha、颜色、档位）且不混体系？
13. 档位是否 ≤6（建议 3–5），且每个档位有语义解释？
14. 亮暗两套主题是否保持同一 level、只换表达语言？
15. 材质是否只出现在 functional layer，且一个视图内 ≤1 处？
16. 玻璃上文字是否按**合成后像素**验过 4.5:1，并有 35% dimming 或 `regular` 方案？
17. `backdrop-filter` 是否有 `@supports` 实色回退与降低透明度偏好处理？
18. 所有 `z-index` 都能在语义刻度表里查到出处吗？
19. 浮层是否检查过父级 `overflow` / `transform` / `opacity` 造成的裁剪与新 stacking context？
20. hover 抬起的阴影不会被滚动容器切掉，且 `prefers-reduced-motion` 下不强制动效吗？

---

## 23 · 可抄代码（6 段）

### 23.1 CSS · 形状与深度 token 系统（可直接落项目）

```css
:root {
  /* L1 几何：半径按尺寸带分档，避免 overlap 静默压缩 */
  --radius-none: 0px;
  --radius-xs: 2px;      /* 小标签 / chip，盒高 ≤24 */
  --radius-sm: 4px;      /* 输入框 / 按钮，盒高 24–40 */
  --radius-md: 8px;      /* 常规卡片，盒高 ≥64 */
  --radius-lg: 16px;     /* 大卡片 / 弹窗，盒高 ≥120 */
  --radius-pill: 999px;  /* 由 overlap 自动收敛到 min(w,h)/2 */

  /* L2 高度：语义 level，不是 CSS 参数 */
  --elevation-0: 0;   --elevation-1: 1;
  --elevation-2: 2;   --elevation-3: 3;
  --elevation-4: 4;   --elevation-5: 5;

  /* 三层阴影配方（umbra / penumbra / ambient），一项目只用这一套 */
  --shadow-1: 0 1px 2px 0 rgb(0 0 0 / 0.10), 0 1px 3px -1px rgb(0 0 0 / 0.08);
  --shadow-2: 0 3px 6px -2px rgb(0 0 0 / 0.12), 0 6px 16px 0 rgb(0 0 0 / 0.08);
  --shadow-3: 0 9px 28px 8px rgb(0 0 0 / 0.05), 0 6px 16px 0 rgb(0 0 0 / 0.08),
              0 3px 6px -4px rgb(0 0 0 / 0.12);

  /* L3 表面：边界信号独立满足 3:1，不靠阴影 */
  --surface-base: #ffffff;
  --surface-raised: #ffffff;
  --border-identifiable: #767676;  /* 对白底 ≈4.54:1，过 3:1 */

  /* L5 层叠：语义刻度，不写魔法数 */
  --z-dropdown: 100;  --z-sticky: 200;  --z-backdrop: 300;
  --z-modal: 400;     --z-toast: 500;   --z-tooltip: 600;
}

.card {
  border-radius: var(--radius-md);
  /* 阴影与边界各司其职：前者氛围，后者合规 */
  box-shadow: var(--shadow-1);
  border: 1px solid var(--border-identifiable);
}
.card:hover { box-shadow: var(--shadow-2); }  /* level1 → level3 的语义抬起 */

/* 嵌套同心：r = R − p，用 calc 让契约显式 */
.card--nested { --outer-r: var(--radius-lg); --pad: 8px; padding: var(--pad); }
.card--nested > .inner { border-radius: calc(var(--outer-r) - var(--pad)); }

/* 材质：仅 functional layer，带完整降级 */
.topbar { background: rgb(255 255 255 / 0.72); }
@supports (backdrop-filter: blur(1px)) {
  .topbar { backdrop-filter: blur(20px); }
}
@supports not (backdrop-filter: blur(1px)) {
  .topbar { background: var(--surface-base); }  /* 实色回退，不留半透明 */
}
```

### 23.2 Python · 阴影 alpha → WCAG 对比度计算器（实跑 PASS）

```python
def rel_lum(rgb):
    c = [x / 255 for x in rgb]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]

def contrast(a, b):
    x, y = sorted([rel_lum(a), rel_lum(b)], reverse=True)
    return (x + .05) / (y + .05)

def shadow_on_white(alpha):
    """纯黑半透明阴影叠在白底上的合成色与对比度。"""
    c = tuple(round(255 * (1 - alpha)) for _ in range(3))
    return c, contrast((255, 255, 255), c)

def alpha_for_ratio(target=3.0, bg=(255, 255, 255)):
    """与 shadow_on_white 同口径：先取整成真实 8bit 像素，再判 3:1。
    连续解约 0.4162，但 8bit 取整后 c=149 只有 2.995:1 不过线，
    故生产阈值取能真正通过的 0.4176（c=148 / #949494）。"""
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        composited = tuple(round(v * (1 - mid)) for v in bg)
        if contrast(bg, composited) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

if __name__ == "__main__":
    for a in (0.05, 0.08, 0.10, 0.12, 0.20, 0.25, 0.42):
        c, r = shadow_on_white(a)
        print(f"alpha {a:.2f} -> rgb{c}  {r:.3f}:1  "
              f"{'PASS' if r >= 3 else 'FAIL'}")
    print("alpha needed for 3:1 on white =", round(alpha_for_ratio(), 4))
```

实跑输出：

```
alpha 0.05 -> rgb(242, 242, 242)  1.119:1  FAIL
alpha 0.08 -> rgb(235, 235, 235)  1.192:1  FAIL
alpha 0.10 -> rgb(230, 230, 230)  1.248:1  FAIL
alpha 0.12 -> rgb(224, 224, 224)  1.320:1  FAIL
alpha 0.20 -> rgb(204, 204, 204)  1.606:1  FAIL
alpha 0.25 -> rgb(191, 191, 191)  1.839:1  FAIL
alpha 0.42 -> rgb(148, 148, 148)  3.033:1  PASS
alpha needed for 3:1 on white = 0.4176
```

### 23.3 Python · corner overlap 与同心圆角校验器（实跑 PASS）

```python
def effective_radius(w, h, r):
    """规范 f = min(L_i/S_i)：四角同半径时上限为 min(w,h)/2。"""
    f = min(w / (2 * r), h / (2 * r)) if r > 0 else float("inf")
    return (min(f, 1.0), r * min(f, 1.0))

def concentric(R, p):
    """嵌套同心圆角 r = R - p；r <= 0 视为契约失效。"""
    r = R - p
    return ("OK concentric", r) if r > 0 else ("INVALID (r<=0, reduce p or raise R)", r)

if __name__ == "__main__":
    for w, h, r in ((100, 40, 30), (100, 40, 50), (320, 64, 40), (120, 120, 80)):
        f, used = effective_radius(w, h, r)
        print(f"box {w}x{h} radius {r} -> f={f:.4f} used={used:.2f}px")
    for R, p in ((16, 8), (28, 12), (8, 4), (12, 16)):
        verdict, r = concentric(R, p)
        print(f"outer R={R:2d} padding={p:2d} -> inner r={r:3d} {verdict}")
```

实跑输出：

```
box 100x40 radius 30 -> f=0.6667 used=20.00px
box 100x40 radius 50 -> f=0.4000 used=20.00px
box 320x64 radius 40 -> f=0.8000 used=32.00px
box 120x120 radius 80 -> f=0.7500 used=60.00px
outer R=16 padding= 8 -> inner r=  8 OK concentric
outer R=28 padding=12 -> inner r= 16 OK concentric
outer R= 8 padding= 4 -> inner r=  4 OK concentric
outer R=12 padding=16 -> inner r= -4 INVALID (r<=0, reduce p or raise R)
```

### 23.4 Python · 深度系统静态扫描器（实跑 PASS）

```python
import re
from pathlib import Path

LEN = r"-?[\d.]+(?:px|rem|em|%)?"

def scan(css_text):
    issues = []
    for m in re.finditer(r"box-shadow\s*:\s*([^;]+);", css_text):
        val = m.group(1).strip()
        # elevation 语义 token 误用必须在 var() 短路之前判，否则会被漏掉
        if re.search(r"elevation-level\d+", val):
            issues.append("elevation token used as box-shadow: " + val[:60])
            continue
        if val.startswith("var("):
            continue  # 普通 token 引用由 token 定义处单独校验
        for layer in val.split(","):
            lens = re.findall(LEN, layer.strip())
            if len(lens) == 1:
                issues.append("single-length box-shadow (invalid): " + layer.strip())
            if re.search(r"-\d+(?:\.\d+)?px", layer) and "spread" not in layer:
                pass  # 负 spread 合法
    for m in re.finditer(r"border-radius\s*:\s*([^;]+);", css_text):
        if re.search(r"-\s*\d", m.group(1)):
            issues.append("negative border-radius (invalid): " + m.group(1))
    for m in re.finditer(r"z-index\s*:\s*(\d{4,})", css_text):
        issues.append("magic z-index: " + m.group(1))
    for m in re.finditer(r"corner-shape\s*:\s*(\w+)", css_text):
        if "border-radius" not in css_text:
            issues.append("corner-shape without border-radius: " + m.group(1))
    return issues

if __name__ == "__main__":
    bad = """
    .a { box-shadow: 1px; }
    .b { box-shadow: var(--md-sys-elevation-level1); }
    .c { border-radius: -4px; }
    .d { z-index: 9999; }
    """
    good = """
    .card { border-radius: 8px;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
            z-index: var(--z-dropdown); }
    """
    b, g = scan(bad), scan(good)
    print("bad issues:", len(b)); [print("  -", x) for x in b]
    print("good issues:", len(g))
    assert len(b) >= 4 and len(g) == 0
    print("self-test PASS")
```

实跑输出：`bad issues: 4`（单长度 / elevation token / 负半径 / 魔法 z-index）· `good issues: 0` · `self-test PASS`。

### 23.5 CSS · 亮暗双主题的同 level 表达（不照搬阴影）

```css
:root { color-scheme: light dark; }
:root {
  --surface-0: #ffffff; --surface-1: #ffffff; --surface-2: #f7f7f7;
  --edge: #767676;                 /* 亮色：3:1 边界 */
  --lift: var(--shadow-1);
}
@media (prefers-color-scheme: dark) {
  :root {
    /* 暗色：同一 level 改为表面逐级提亮，阴影只作极轻辅助 */
    --surface-0: #121212; --surface-1: #1e1e1e; --surface-2: #272727;
    --edge: #9a9a9a;              /* 对 #1e1e1e 仍 ≥3:1 */
    --lift: 0 1px 2px rgb(0 0 0 / 0.4);
  }
}
.surface-1 { background: var(--surface-1); border: 1px solid transparent; }
.surface-1.is-identifiable { border-color: var(--edge); }
.surface-1.is-raised { box-shadow: var(--lift); }
.surface-2 { background: var(--surface-2); }   /* level 再上一层，不靠加黑阴影 */
```

### 23.6 CSS · 材质层的渐进增强与可访问性降级

```css
.functional-layer {
  background: rgb(255 255 255 / 0.72);   /* 默认：不透明兜底 */
  color: #1a1a1a;
}
@supports (backdrop-filter: blur(1px)) {
  .functional-layer { backdrop-filter: blur(20px) saturate(1.2); }
  /* clear 变体在亮背景上补 35% 暗色 dimming，保文字可读 */
  .functional-layer.is-clear::before {
    content: ""; position: absolute; inset: 0;
    background: rgb(0 0 0 / 0.35); pointer-events: none;
  }
  .functional-layer > * { position: relative; }
}
/* 降低透明度 / 强制对比：一律回实色 */
@media (prefers-contrast: more), (prefers-reduced-transparency: reduce) {
  .functional-layer { background: #fff; backdrop-filter: none; }
  .functional-layer.is-clear::before { display: none; }
}
```

---

## 24 · 取源与限制（公开记录）

本轮 shape elevation 取源均标注了可核验位置与不可核验处；以下限制**不臆造、不补齐**，供后续轮次继续深挖。

**一手官方原文 / 源码实测（2026-11-08）**：

| 来源 | 取得内容 |
|---|---|
| M3 *Component elevation* | 6 级 `0/1/3/6/8/12 dp`；*"Elevation has no shadow or value of its own by default."*；*"Surface tint color is deprecated."* |
| M3 *Shape overview*（2025-05 Expressive） | 35 shapes / shape morphing / `Large increased (20dp)` / `Extra large increased (32dp)` / `Extra extra large (48dp)` / `full` 取代 `50%` / *"Web is not currently available"* |
| `material-foundation/material-tokens` `css/shape.css` | `0 / 4 / 8 / 12 / 16 / 28px` + `corner-full-family: 3px` |
| `material-foundation/material-tokens` `css/elevation.css` | `level0–5 = 0/1/3/6/8/12px` 与 `.elevation-1 { box-shadow: var(...) }` |
| MDN `box-shadow` / `border-radius` / `corner-shape` | 2/3/4 `<length>` 规则、不影响 box model、逗号顺序、跟随圆角；`<length-percentage[0,∞]>{1,4} [ / ... ]?`、百分比参照 width/height、负值无效；`corner-shape` Experimental 且依赖有效半径 |
| W3C WCAG 2.2 Understanding SC 1.4.11 | 3:1 adjacent color(s)、3D drop-shadow 例外、focus 仍需对比度、不四舍五入口径 |
| Tailwind CSS v4 `box-shadow` 文档 | 8 个工具类完整逐字值 |
| Ant Design 5 `customize-theme` | 6 个圆角/高度 token + 2 个 `boxShadow` 逐字字符串 |
| `mui/material-ui` `shadows.js` | `0.2 / 0.14 / 0.12` 与 `createShadow` 三层结构、25 档 |
| `Tencent/tdesign-common` `_radius.less` / `_light.less` | 7 个圆角 token + 3 条阴影逐字值 |
| Arco Design token 页 | 5 个圆角值 + 4 个阴影 token **名称**（未取逐字字符串） |
| `material-components/material-web` `_md-sys-shape.scss` | `$supported-tokens` 7 项与 `*-top` shorthand |
| Carbon *Color / Layering* | `White ↔ Gray 10` 交替、暗色逐级变浅、`2px border` focus 与 3:1 |
| Apple HIG *Materials* | Liquid Glass vs standard materials、`regular`/`clear`、functional layer 边界、35% dimming、`quaternary` on thin 禁配 |
| `impeccable` `spatial-design.md` | semantic z-index scale 与 `sm→md→lg→xl`、*"if you can clearly see it, it's probably too strong"* |
| `awesome-design-md` `SKILL.md` | 54 个真实产品 DESIGN.md 的 9 sections，第 6 节即 *Depth & Elevation — Shadow system, surface hierarchy* |

**GitHub API 实测（12 仓库 star / license）**：`mui/material-ui` 99,301★ MIT · `ant-design/ant-design` 100,108★ MIT · `carbon-design-system/carbon` 9,609★ Apache-2.0 · `material-components/material-web` 11,417★ Apache-2.0 · `radix-ui/themes` 8,825★ MIT · `shadcn-ui/ui` 127,614★ MIT · `tailwindlabs/tailwindcss` 98,645★ MIT · `primer/primitives` 417★ MIT · `microsoft/fluentui` 20,391★ NOASSERTION · `chakra-ui/chakra-ui` 40,716★ MIT · `VoltAgent/awesome-design-md` 126,096★ MIT · `pbakaus/impeccable` 105,892★ Apache-2.0。（`NOASSERTION` ≠ 无许可，需逐目录读 LICENSE。）

**明确未证实 / 已排除（不写入结论）**：

1. W3C TR `css-backgrounds-3/#corner-overlap` 本轮被 Cloudflare 挑战页拦截，`drafts.csswg.org` 抓取片段也不含 §4.5 正文。`f = min(L_i/S_i)` 按随附规范说明记录，并**已用 §23.3 Python 实跑验证数值行为**，不声称逐字引自 TR。
2. **Fluent 2 `/depth` 返回 404**，未取得任何 Fluent 2 深度数值，本文件不含 Fluent 2 elevation 表；`Design-related websites.txt` 里已有的 Fluent 2 Motion 条目保持不动。
3. M3 `styles/shape/shape-scale-tokens` 页面未返回精确 shape scale token 表；本文件 M3 精确值来自静态 `shape.css`，与 Expressive 动态 scale 不同源，不可混用。
4. Arco 阴影 token 只取到名称，未取逐字字符串；§8.5 只登记命名与结构。
5. `ant-design` 的 `components/theme/themes/default/seed.ts` 与 `radix-ui/themes` 的 `tokens` 目录均 404，精确默认值改由官方 `customize-theme` 表与已验证源码取得；Radix 圆角/阴影 token 本轮**未纳入**（列为下轮候选）。
6. `corner-shape` 为 Experimental，浏览器支持矩阵本轮未实测，只按 MDN 标记给出纪律。
7. 本文件所有对比度数值基于 **sRGB / WCAG 2.x 相对亮度**；APCA Lc 口径见 `color-science.md §6`，两者不可混判。

**下轮候选缺口**：① 格式塔 / 视觉层级 / 眼动与认知负荷（`格式塔=0`、`Gestalt=0`、`视觉层级=1`，全域空白）；② Radix / Primer / Chakra 的 shape·elevation token 源码精确定位；③ Fluent 2 depth 现行文档路径复核；④ W3C corner-overlap §4.5 逐字核验（换可访问镜像）。
