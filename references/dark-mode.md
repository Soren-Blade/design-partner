# 暗色模式体系（Dark Mode System）

> **一句话**：暗色模式不是"把颜色反过来"，而是**换一套表面层级逻辑**——亮色用阴影表达高度，暗色用**表面变亮**表达高度；亮色文字越黑越清楚，暗色文字**不能用纯白**。
>
> 本文件解决六个问题：**该不该做**（证据与边界）、**表面怎么排**（三体系精确 tone/lighten 值与实测对比度）、**文字怎么给**（四档透明度与纯白陷阱）、**品牌色怎么降**（色阶重映射而非反相）、**怎么切**（CSS/小程序/iOS/Android 四端实现与防闪白）、**怎么验**（22 项自检 + 20 条反模式）。

**读法**：先看 §1 判断要不要做 → §2 拿到层级数值 → §3–§5 拿到文字/边框/阴影规则 → §6 处理品牌与语义色 → §9–§10 落地实现 → §12 验收。只想抄代码直接跳 §14。

> 快照 2026-11-01。文中所有 tone / alpha / hex 均取自官方源码或官方文档原文；所有对比度数值由 WCAG 相对亮度公式与 CIELAB L\*→Y 换算**实测计算**，非引用二手结论。

---

## 1. 先决定：该不该做暗色（含反面证据）

### 1.1 NN/g 的证据链（与直觉相反，必须先知道）

NN/g 的 Raluca Budiu 综述了学界研究，结论**不利于"暗色默认"**：

| 结论 | 出处与条件 |
|---|---|
| **正常视力用户，浅色模式在多数情况下表现更好** | Piepenbrock 等 2013（*Ergonomics*）：视力正常年轻组（18–33）与老年组（60–85），Landolt C 缺口识别 + 校对找错，**浅色在全部维度胜出** |
| **字号越小，浅色优势越明显** | Piepenbrock 等（*Human Factors*）："the smaller the font, the better it is for users to see the text in light mode" |
| **夜间浅色仍优于暗色**；白天两者无显著差异 | Dobres 等 2017（MIT AgeLab，*Applied Ergonomics*）：词汇判断任务，白天无极性差异，夜间浅色更快 |
| **两种模式的疲劳感无显著差异** | Piepenbrock：暗色并不更省眼，浅色也不更累眼 |
| **用户主观感受不到差异** | Piepenbrock：受试者报告的可读性感受无差别——所以**别用"用户说喜欢暗色"当证据** |

**机理**（NN/g 引用的解释）：正极性（浅底深字）下整体进光更多 → 瞳孔收缩更小 → 球面像差更小、景深更大 → 细节聚焦更轻松。

### 1.2 但暗色确实有不可替代的场景

| 场景 | 依据 |
|---|---|
| **低视力/白内障等屈光介质混浊** | Legge 等（明尼苏达）：7 名介质混浊受试者**全部**在暗色下阅读更快；中心视力受损者则不受极性影响。原因：混浊介质散射光，屏幕发光越少失真越少 |
| **暗环境使用** | Apple HIG：Dark Mode 面向 low-light environments |
| **省电** | Android 官方：暗色"reduces power usage by a significant amount, depending on the device's screen technology"（OLED 才明显） |
| **沉浸式媒体** | Apple HIG：媒体浏览类可用**永久暗色**让 UI 退后（如 Stocks） |
| **长文阅读类应用** | NN/g 明确建议：book readers / magazines / news sites **应提供**暗色开关 |
| **长期用眼的潜在风险** | Aleman 等 2018（*Scientific Reports*）：浅色阅读 1 小时后脉络膜变薄（与近视相关），暗色则增厚。样本仅 7 人，**只能作为"提供选项"的理由，不能作为"暗色更健康"的结论** |

### 1.3 决策树

```
目标用户是普通大众 / 办公 / 数据录入 / 长文阅读？
├─ 是 → 【默认浅色 + 提供暗色开关】（不要默认暗色）
└─ 否 ↓
目标场景是媒体浏览 / 开发者工具 / 监控大屏 / 夜间驾驶 / 影院？
├─ 是 → 可以【默认暗色】，但仍需浅色逃生口（大屏除外）
└─ 否 → 【跟随系统】是最安全的默认值（Android 官方推荐 MODE_NIGHT_FOLLOW_SYSTEM）
```

**三条硬规矩**：
1. **不提供"仅本应用"的独立外观开关作为唯一入口**。Apple HIG：应用级外观设置会让用户以为应用坏了（不响应系统设置）。正确做法是**三态**：浅色 / 深色 / 跟随系统，默认跟随系统。
2. **做了就必须全站做完**。NN/g：选项应贯穿所有界面。半套暗色（登录页还是白的）比没有更糟。
3. **中后台/表单密集系统不要默认暗色**——§1.1 的字号结论直接命中（12–14px 正文是暗色最吃亏的区间）。

---

## 2. 表面层级：暗色的核心是"重排"，不是"反相"

### 2.1 为什么不能反相（一句话原理）

亮色模式里，`#fff` 背景 + 阴影 = 高度。暗色模式里，阴影在深底上**几乎不可见**，所以必须换一种信号：**表面越靠前，颜色越亮**。这就是 M2 的 elevation overlay、M3 的 surface container tone、Ant 的 `lighten(brightness)`、Carbon 的 layer 阶梯——四家做法不同，**方向一致**。

> Apple HIG 的原话最准确：暗色"uses two sets of background colors — called *base* and *elevated*… The base colors are dimmer, making background interfaces appear to recede, and the elevated colors are brighter, making foreground interfaces appear to advance."
> 并且明确警告：暗色"aren't necessarily inversions of their light counterparts: while many colors are inverted, some are not."

### 2.2 Material 3：tone 全表（源码逐字，非二手）

来源：`material-color-utilities/typescript/dynamiccolor/color_spec_2021.ts` + `scheme/scheme.ts`。

| 表面角色 | 亮色 tone | 暗色 tone | 暗色 vs surface 实测对比 |
|---|---|---|---|
| `surfaceContainerLowest` | 100 | **4** | 1.04 |
| `surface` / `surfaceDim` | 98 / 87 | **6** | 1.00 |
| `surfaceContainerLow` | 96 | **10** | 1.08 |
| `surfaceContainer` | 94 | **12** | 1.13 |
| `surfaceContainerHigh` | 92 | **17** | 1.29 |
| `surfaceContainerHighest` | 90 | **22** | 1.50 |
| `surfaceBright` | 98 | **24** | 1.61 |

**关键读法（三点，都是算出来的）**：
1. **亮色是"往下压"，暗色是"往上提"**：亮色 surface 98 → 最高层 90（越前越深）；暗色 surface 6 → 最高层 22（越前越亮）。
2. **暗色的层级跨度比亮色大**：亮色 98→90 总跨度对比 **1.23**；暗色 6→22 总跨度 **1.50**。暗底上深度更难感知，所以必须给更大的 tone 差。**直接照抄亮色的层级差是最常见的错误。**
3. **相邻层之间只有 1.04–1.17**。所以**永远不要只靠一层 tone 差表达层级**——必须配边框、阴影或留白（见 §5）。

**M3 还给了对比度等级（ContrastLevel）**，这是很多人漏掉的能力：`ContrastCurve(low, normal, medium, high)` 对应 contrastLevel **-1.0 / 0.0 / 0.5 / 1.0**（源码注释逐字："The four values correspond to values for contrast levels -1.0, 0.0, 0.5, and 1.0"）。例如暗色 `surfaceContainerHighest` 在四级下分别是 tone **22 / 22 / 26 / 30**——**同一套 token 可以出"标准/中/高对比"三个无障碍档位**，不用手调颜色。

### 2.3 Ant Design：暗色是"黑底 + 白 alpha 提亮"

来源：`components/theme/themes/dark/colors.ts`，`colorBgBase='#000'`，`getSolidColor = lighten(brightness)`。

| 语义 | 亮色 | 暗色 | 暗色实际 hex（黑底） | 与底色对比 |
|---|---|---|---|---|
| `colorBgLayout` | lighten(4) | **lighten(0)** | `#000000` | 1.00 |
| `colorBgContainer` | lighten(0) | **lighten(8)** | `#141414` | 1.14 |
| `colorBgElevated` | lighten(0) | **lighten(12)** | `#1f1f1f` | 1.27 |
| `colorBgSpotlight` | 85% 黑 alpha | **lighten(26)** | `#424242` | 2.09 |

**注意这个反转**：亮色里 Layout 比 Container **深**（+4），Container 和 Elevated 都是 **0**（靠阴影区分）；暗色里 Layout 是 **0**（最底），Container **+8**、Elevated **+12**、Spotlight **+26**。**"阴影消失，靠亮度补"** 在这一行代码里体现得最干净。

> 实用换算：`lighten(n)` 对纯黑等于 `rgb(255n/100)`。所以 `+8 → #141414`、`+12 → #1f1f1f`、`+26 → #424242`。**如果你的底色不是纯黑，必须重新算，不能套用这三个 hex。**

### 2.4 Carbon：g100 的 layer 阶梯（hex 全部来自 `@carbon/colors` 11.61.0 包内源码）

Carbon 灰阶（实测取值）：`gray10 #f4f4f4` · `gray20 #e0e0e0` · `gray30 #c6c6c6` · `gray40 #a8a8a8` · `gray50 #8d8d8d` · `gray60 #6f6f6f` · `gray70 #525252` · `gray80 #393939` · `gray90 #262626` · `gray100 #161616`

g100（暗色主题）映射（`packages/themes/src/v10/g100.ts`）：

| Token | 值 | hex | 实测 |
|---|---|---|---|
| `uiBackground` | gray100 | `#161616` | 底色 |
| `ui01`（layer 1） | gray90 | `#262626` | vs 底色 1.22 |
| `ui02` / `ui03`（layer 2/3） | gray80 | `#393939` | vs 底色 1.74 |
| `ui04` | gray60 | `#6f6f6f` | vs 底色 3.60 |
| `ui05` | gray10 | `#f4f4f4` | — |
| `text01` | gray10 | `#f4f4f4` | **16.45** on 底色 |
| `text02` | gray30 | `#c6c6c6` | **10.59** |
| `text03`（禁用） | gray60 | `#6f6f6f` | **3.60** |
| `textError` | red40 | — | — |
| `field01` / `field02` | gray90 / gray80 | — | — |

**Carbon 的特点：底色不是纯黑，是 `#161616`**（16,16,16 ≈ tone 6），和 M3 的 `surface=6` 巧合一致。**两家独立体系都收敛到"tone 6 附近"，这是暗色底色的经验值。**

### 2.5 选底色的三种做法与取舍

| 做法 | 值 | 优点 | 代价 |
|---|---|---|---|
| **纯黑** | `#000000` | OLED 省电最多；对比度最高（白字 21:1） | 阴影/层级全失效；白色文字晕光最重；滚动时 OLED 像素开关有拖影（M2 明确警告）；M2 与 Apple 都不推荐 |
| **深灰（推荐默认）** | `#121212`（M2）/ `#161616`（Carbon）/ tone 6（M3） | 保留层级与阴影空间；晕光可控 | 省电不如纯黑 |
| **带主色倾向的深色** | `#121212` + 8% 主色 → `#1F1B24`（M2 官方示例） | 品牌感强、不"死黑" | 主色一变就要重算；饱和度易过头 |

**M2 的原话立场**：默认用深灰 `#121212` 而非纯黑，因为"深灰能表达更丰富的色彩、高度和深度，因为阴影在灰色上比在黑色上更易看见"；**纯黑只留给"需要高效省电的产品"**。

**决策**：
- 移动端 OLED 为主、内容型 → 可用纯黑，但**必须**把文字从纯白降到 tone 90 档（§3），并用边框替代阴影。
- 中后台 / 桌面 / 长时间阅读 → 深灰 `#161616`~`#1a1a1a`。
- 大屏监控 → 纯黑（避免环境光反射），但要接受"层级别只能靠边框"。

---

## 3. 文字：暗色下不能用纯白（暗色对比度与文字层级）

### 3.1 四家体系的"不用纯白"是共识（可验证）

| 体系 | 暗色主文本实际值 | 相对纯白的降幅 |
|---|---|---|
| M3 | `onSurface` = **tone 90**（`#e6e6e6` 附近） | 降 10 tone |
| Ant Design | `colorText` = `rgba(255,255,255,0.85)` | 合成 `#d9d9d9`（黑底） |
| Carbon g100 | `text01` = **gray10 `#f4f4f4`** | 降 11/255 |
| Radix | 第 11 步（低对比）/ 第 12 步（高对比），均非纯白 | — |

**原因**：亮色文字在深底上会因**光渗（halation）**在视觉上"发胖"、边缘扩散，纯白尤其明显；同时纯白 + 纯黑是 21:1 的极端对比，长时间阅读反而更累。降到 tone 90 档既保住可读性，又削掉晕光。

### 3.2 Ant Design 四档文本透明度 + 实测对比度（重点看第三档）

| 档位 | alpha | 黑底合成 | vs `#000` | vs `#141414` | vs `#1f1f1f` |
|---|---|---|---|---|---|
| 主文本 `colorText` | 85% | `#d9d9d9` | **14.88** | 13.43 | 12.14 |
| 次文本 `colorTextSecondary` | 65% | `#a6a6a6` | **8.63** | 8.21 | 7.69 |
| 三级 `colorTextTertiary` | 45% | `#737373` | **4.43** ⚠️ | 4.54 | 4.41 ⚠️ |
| 四级 `colorTextQuaternary` | 25% | `#404040` | **2.03** ❌ | 2.25 | 2.28 |

**这张表暴露了两个真实陷阱**：
1. **三级文本 45% 只有 4.43–4.54**，正好压在 WCAG AA 4.5:1 的线上——**在纯黑底上直接不达标（4.43 < 4.5）**。如果你的设计系统抄了 Ant 的 45%，又在纯黑底上放辅助说明文字，**已经不合规**。修法：把三级提到 **50%–52%**，或底色调到 `#141414` 以上。
2. **四级 25% 只有 2.03**，只能用于**装饰性**（图标底纹、分隔装饰），**绝不能承载文字**。

> 对照：亮色的对应值是 88% / 65% / 45% / 25%（`colorText` 亮色是 **88%**，暗色是 **85%**——暗色反而更低，正是为了削晕光）。

### 3.3 文字层级推荐表（可直接抄）

| 用途 | 暗色值 | 说明 |
|---|---|---|
| 正文/标题（主） | `#e6e6e6`（tone 90）或 `rgba(255,255,255,0.85)` | 不用 `#fff` |
| 次要说明 | `#a6a6a6`（tone 70 附近） | 8.6:1，安全 |
| 辅助/占位 | `#8d8d8d`（gray50） | 5.45:1 on `#161616`，刚好过 AA |
| 禁用 | `#6f6f6f`（gray60） | 3.60:1，**仅用于禁用态**，且必须配 `cursor: not-allowed` + 其他信号 |
| 链接 | 主色 tone 80（M3）/ `blue40`（Carbon） | 见 §6 |

**中文字体的额外注意**：中文笔画细密，暗底上光渗更明显。同一字号下，中文在暗色里的可读性下降比拉丁文更快。**暗色下中文正文建议：行高 +0.05~0.1、字重不降、字号不小于 14px**；12px 中文在暗色里几乎不可读（NN/g 的"字号越小浅色优势越大"直接命中）。

---

## 4. 边框与分隔线：暗色下不可依赖

### 4.1 实测：主流暗色的边框都不达 3:1

| 值 | 来源 | 与底色对比 |
|---|---|---|
| `#424242`（Ant `colorBorder`，lighten 26%） | Ant dark | **2.09** |
| `#303030`（Ant `colorBorderSecondary`，lighten 19%） | Ant dark | **1.59** |
| gray60 `#6f6f6f`（Carbon `ui04`） | Carbon g100 | **3.60** ✅ |

**这意味着**：抄 Ant 的暗色边框（`#424242`）做输入框描边，**不满足 WCAG 2.2 SC 1.4.11（非文本对比 3:1）**——因为输入框边界是"识别控件所必需"的。Carbon 用 `ui04`（gray60）就达标。

### 4.2 三条规则

1. **表单控件边界必须 ≥3:1**。用 `#6f6f6f` 起步，不要用 `#424242`。
2. **装饰性分隔线可以低于 3:1**（1.4.11 只要求"识别控件与状态所必需"的边界）。表格横线、卡片分隔用 1.5–2.1 即可，太亮会"抢戏"。
3. **暗色下"线"比"面"更可靠**。因为相邻 surface 只有 1.04–1.17 的差，纯靠 tone 分层在低亮度屏/差显示器上会完全糊掉。**暗色的卡片建议：surface 提亮 + 1px 边框（≥1.5:1）双保险**。

---

## 5. 阴影与高度：两派做法与正确用法

### 5.1 两派（存在真实分歧，不要以为只有一种对）

| 派别 | 立场 | 代表 |
|---|---|---|
| **A：阴影保持深色** | "不要用浅色光晕替代深色阴影表达高度——光晕无法准确表现投射阴影"；暗色靠**表面颜色**表达高度 | M2 官方 |
| **B：阴影用白色 alpha** | `colorShadow` 默认 `rgba(255,255,255,0.2)`，所有 `boxShadow` 由它派生 | Ant Design dark |

**怎么选**：
- **有明确层级体系（M3/Ant/Carbon 式 surface 阶梯）→ 用 A**。阴影只做极轻的补充（0–8% 黑），主力是 surface 提亮。
- **只有一层底色、组件必须"浮起来"（弹窗/下拉/气泡）→ 用 B 的变体**：`0 6px 16px rgba(0,0,0,.48), 0 0 0 1px rgba(255,255,255,.06)`——**黑色投影做体积 + 极淡白色描边做分离**。纯白 glow 单独用会显得"发霉"。

### 5.2 高度与表面值的对照（把两套合成一张表）

| 层级 | 典型组件 | 亮色信号 | 暗色信号 |
|---|---|---|---|
| 0 · 背景 | 页面底 | `#f5f5f5` | `#000` / `#161616` |
| 1 · 卡片 | Card、Panel | 白底 + 阴影 | surface +8（`#141414`）+ 1px 边框 |
| 2 · 浮层 | Dropdown、Popover、Tooltip | 白底 + 中阴影 | surface +12（`#1f1f1f`）+ 深阴影 |
| 3 · 模态 | Dialog、Drawer | 白底 + 大阴影 + scrim | surface +26（`#424242`）+ scrim 60–80% |
| 4 · 最前 | Toast、Spotlight | 高对比反色 | 亮底深字（反相）或 `#424242` |

**注意 §3 的连带影响**：表面越亮，白字对比越低。`#424242` 上的白字只有 **10.05**、85% 白只有 **7.83**——仍达标，但如果再往上提（比如 `#525252`，白字 7.81），就要检查正文 4.5:1 是否还成立。**M2 的原始约束就是这个**：底色必须深到"最亮的那层表面上的正文仍满足 4.5:1"。

---

## 6. 品牌色与语义色：降饱和，不是反相

### 6.1 M2 的精确规则（可直接执行）

- **不要用高饱和色做暗色主题的主色**。原因两条：过不了 AA 4.5:1；在深底上产生**光学振动（optical vibration）**，加剧眼疲劳。
- **主色取 200 色阶**（"在所有高度表面上，普通文字至少满足 4.5:1"）。整体建议区间 **200–50 浅色调**，而不是亮色主题惯用的 900–500 饱和档。
- **品牌色可以全饱和，但只给 1–2 个元素**（logo、品牌按钮）。
- **错误色**：M2 基线暗色 `#CF6679`（= 亮色 `#B00020` 叠 40% 白提亮）。
- 状态叠加层：用主色的容器，状态叠加用**白色**；禁用态容器 12% 白、内容 38% 白。

### 6.2 M3 的做法：不是"取 200 阶"，是"tone 重映射"

| 角色 | 亮色 tone | 暗色 tone | 规律 |
|---|---|---|---|
| `primary` | 40 | **80** | 深色档 → 浅色档 |
| `onPrimary` | 100 | **20** | 反相 |
| `primaryContainer` | 90 | **30** | 浅容器 → 深容器 |
| `onPrimaryContainer` | 10 | **90** | 反相 |
| `outline` | 50 | **60** | **变亮**（不是反相！） |
| `outlineVariant` | 80 | **30** | 反相 |
| `inverseSurface` | 20 | **90** | 反相 |
| `error` | 40 | **80** | 同 primary |
| `onErrorContainer` | 10 | **80** | ⚠️ 不对称 |

> **两处易错点**（源码实测，别自作聪明"对称化"）：
> 1. `outline` 暗色 **50→60 是变亮**——暗底上"边界"需要更强分离度。
> 2. `onErrorContainer` 暗色是 **80 而非 90**，与 `onPrimaryContainer`(90) 不一致，这是官方实现的真实差异。
>
> 完整品牌色阶生成方法（HCT / Radix 12 步 / 对比度优先三条路线）见 `brand-identity.md §10`，此处不重复。

### 6.3 中国特色：涨跌色在暗色下必须重调

A 股/中文金融场景的红涨绿跌在暗色下有两个坑：

| 问题 | 现象 | 修法 |
|---|---|---|
| **红色在深底上振动** | `#F5222D`（Ant red-6）on `#141414` 对比仅约 4.1，且高饱和红在暗底上"跳" | 暗色改用 red-5 或提亮降饱和（如 `#FF7875` / `#E86E6E`），并实测 ≥4.5 |
| **绿色过暗** | `#52C41A` 在深底上亮度不足，与背景区分弱 | 暗色改用 green-4/5（`#95DE64` / `#73D13D`），并检查与红色的**色盲可辨**（不要只靠色相，配 ↑↓ 箭头或 +/− 符号） |

**规矩**：涨跌色**必须两套值**（亮/暗各一套），且暗色那套要重新跑对比度与色盲模拟——直接复用亮色 hex 是最常见的翻车点。色盲安全色板见 `accessibility.md` 的 Okabe–Ito 8 色。

---

## 7. 图像、插画、图标

### 7.1 Apple 的明确要求

- **"Soften the color of white backgrounds"**：内容图里带白底的，暗色下要**轻微压暗**，否则白底在深色界面里"发光"。
- **插画**：同一张插画在暗底上"contrast 差、细节丢失"——需要**单独调过对比的暗色版本**，不是简单反相。
- **图标**：必要时做两套。Apple 举的例子很具体：**满月图标在亮底上要加细描边，在暗底上不需要；一滴油图标在暗底上要加边才看得见边缘**。
- 能用动态色/SF Symbols 就别自己做两套。

### 7.2 Web 落地规则

| 资产 | 亮色 | 暗色 | 做法 |
|---|---|---|---|
| 照片 | 原图 | **轻微压暗**（`filter: brightness(.85)` 或叠 8–12% 黑） | 别用 `invert()`，肤色会变鬼 |
| 白底截图 | 原图 | **加 1px 边框 + 压暗** | 边框是必需的，否则白块直接"爆"在深色里 |
| 线稿插画 | 深色线 | **反相 + 降饱和**，或单独出图 | `filter: invert(1) hue-rotate(180deg)` 只适合纯黑白线稿 |
| Logo（深色版） | 彩色/深色 | 用**单色白版**或浅色版 | 品牌手册里应有；没有就让设计师补，别用滤镜凑 |
| 图标 | `currentColor` | 同 | **一律 `currentColor`**，暗色自动跟随文字色 |
| 透明 PNG 深色内容 | 原图 | 会"消失" | 必须换浅色版 |

### 7.3 一张必查清单（图片在暗色里的四个死法）

1. 白底图 → 发光（压暗 + 边框）
2. 深色透明图 → 消失（换浅色版）
3. 半透明遮罩 → 在暗色里"糊成一片"（遮罩透明度要降，暗色用 60–80% 黑而非 40%）
4. 渐变图 → 与背景"接不上"（渐变两端要延伸到背景色）

---

## 8. 状态与交互反馈在暗色下的差异

| 状态 | 亮色 | 暗色 | 陷阱 |
|---|---|---|---|
| Hover | 加深（`darken`） | **提亮**（`lighten`） | 直接复用亮色 hover 值 → hover 后"消失" |
| Active/Pressed | 更深 | 更亮 | 同上 |
| Focus 环 | 深色环 | **亮色环**，且需 3:1 | 深色环在暗底上不可见 |
| Disabled | 灰化（降透明） | 降透明 + **降亮度** | 暗色下 `opacity:.4` 会让元素"沉进背景"，需同时加 1px 边框 |
| Selected | 主色浅底 + 主色字 | **主色深容器 + 主色浅字**（tone 30 + tone 90） | 用 `primaryContainer` 而非 `primary` 做选中底 |
| Scrim | 黑 40–60% | **黑 60–80%** | 暗色下 40% 遮罩压不住，前景不够"前" |
| Skeleton | 灰 `#f0f0f0` | `#1f1f1f`~`#262626`，**且必须比卡片底亮一档** | 用比背景暗的骨架色 → 骨架"看不见" |

**Focus 环在暗色的具体值**：GOV.UK 的 `#FFDD00` 焦点黄在深底上依然可用（黄在暗色里对比极高），但**内圈必须配深色**（`#0B0C0C`）形成双色环。或者用主色 tone 80 的 2px 环 + 2px offset。完整焦点三件套见 `accessibility.md §5`。

---

## 9. 切换实现：四端与防闪白

### 9.1 Web：三件事必须一起做

```html
<!-- ① 提前告知 UA，防首屏白闪（必须放在任何 CSS 之前） -->
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#161616" media="(prefers-color-scheme: dark)">
```

```css
/* ② 声明支持，让滚动条/表单控件/系统色跟随 */
:root { color-scheme: light dark; }
```

```css
/* ③ 变量换层，不换结构 */
:root {
  --bg: #ffffff;
  --bg-elevated: #ffffff;
  --text: #1f1f1f;
  --border: #d9d9d9;
}
:root[data-theme="dark"] {
  --bg: #161616;
  --bg-elevated: #1f1f1f;   /* 提亮，不是变白 */
  --text: #e6e6e6;          /* 不用 #fff */
  --border: #424242;
}
```

**MDN 明确的三点**：
1. `color-scheme` 影响**画布背景色、滚动条、表单控件默认样式、拼写检查下划线**——不设它，暗色下滚动条还是白的。
2. `color-scheme: only light` 可以**关掉 Chrome 的 Auto Dark Theme 强制反色**（对已有暗色的站点很有用，避免被浏览器二次处理）。
3. `light-dark()` 函数可以替代双份声明：`color: light-dark(#1f1f1f, #e6e6e6)`——**前提是祖先设了 `color-scheme`**。

### 9.2 防闪白（FOUC）：唯一正确顺序

```
1. <head> 里 meta color-scheme（浏览器绘制前生效）
2. <head> 里内联 <script> 读 localStorage → 立刻设 documentElement.dataset.theme
3. 之后才是 CSS 与 JS 包
```

内联脚本必须在 CSS 之前、且不能 defer。Tailwind 官方示例也是这个思路（"best to add inline in `head` to avoid FOUC"）：

```js
document.documentElement.classList.toggle(
  "dark",
  localStorage.theme === "dark" ||
  (!("theme" in localStorage) && matchMedia("(prefers-color-scheme: dark)").matches)
);
```

### 9.3 三态切换的存储约定

| 用户选择 | 存储 | 渲染 |
|---|---|---|
| 浅色 | `theme=light` | 强制 light |
| 深色 | `theme=dark` | 强制 dark |
| 跟随系统 | **删除键**（不是存 `"system"`） | 读 `prefers-color-scheme` |

删除键 vs 存 `"system"`：删键能让"用户从未选择过"和"用户主动选了跟随系统"在逻辑上合并，少一个分支。若要支持"系统主题变化时实时跟随"，监听 `matchMedia('(prefers-color-scheme: dark)').addEventListener('change', ...)`，但**只在无存储值时生效**。

### 9.4 Tailwind v4 的两种写法

```css
/* 默认：跟随系统（media 策略） */
@import "tailwindcss";

/* 手动切换：class 策略 */
@custom-variant dark (&:where(.dark, .dark *));

/* 或用 data 属性 */
@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));
```

**推荐 `data-theme`**：和 CSS 变量方案统一，且不会和第三方库的 `.dark` class 打架。

### 9.5 微信小程序暗色适配（`theme.json` 官方配置逐字）

```json
// app.json
{ "darkmode": true, "themeLocation": "theme.json" }
```

```json
// theme.json —— light / dark 两个对象都是必填
{
  "light": { "navBgColor": "#f6f6f6", "navTxtStyle": "black" },
  "dark":  { "navBgColor": "#191919", "navTxtStyle": "white" }
}
```

- 用 `@变量名` 引用：`"navigationBarBackgroundColor": "@navBgColor"`。
- 支持变量化的属性：`navigationBarBackgroundColor`、`navigationBarTextStyle`、`backgroundColor`、`backgroundTextStyle`、`backgroundColorTop`、`backgroundColorBottom`；tabBar 的 `color`、`selectedColor`、`backgroundColor`、`borderStyle`、`list[].iconPath`、`list[].selectedIconPath`。
- **只有配置 `"darkmode": true` 才拿得到 `theme`**（`wx.getSystemInfoSync().theme`），**主题切换事件也才触发**（`App({ onThemeChange })` 或 `wx.onThemeChange`）。
- **但 WXSS 的 `@media (prefers-color-scheme: dark)` 不受该开关影响**——只要微信客户端支持（iOS 7.0.12 / Android 7.0.13+），媒体查询就生效。**这是最容易踩的坑**：以为没开 darkmode 就不会变，结果样式被媒体查询改了、配置却没变。
- 官方已知 bug：iOS 7.0.12 在 light 模式下把 tabBar `borderStyle` 设为 `white` 可能出现黑底。

### 9.6 iOS / Android

| 平台 | 要点 |
|---|---|
| iOS | 用 **base / elevated 两套系统背景色**，别自定义；`UIColor.labelColor` 等语义色自动适配；`UIUserInterfaceStyle` 不要硬设；Increase Contrast + Reduce Transparency 组合下要复测（Apple 明确警告可能出现"深字压深底"） |
| Android | 主题继承 `Theme.MaterialComponents.DayNight` 或 `Theme.AppCompat.DayNight`；三态用 `MODE_NIGHT_NO` / `MODE_NIGHT_YES` / `MODE_NIGHT_FOLLOW_SYSTEM`；API 31+ 用 `UiModeManager#setApplicationNightMode`（可让启动屏也对齐），API 30- 用 `AppCompatDelegate.setDefaultNightMode()` |
| Android Force Dark | `android:forceDarkAllowed="true"` 可自动反色，但**必须逐屏复测**，且可用 `android:forceDarkAllowed="false"` 对单个 View 关闭。**继承 DayNight 主题时 Force Dark 不生效**（自动切换已接管） |
| 鸿蒙 | 用 `$r('app.color.xxx')` 资源 + `dark` 限定词目录，不要硬编码 hex |

### 9.7 切换动画

- 全局 `transition: background-color .2s, color .2s` **只加在容器与文字上**，不要 `* { transition: all }`（会把布局属性也带上，卡顿）。
- 切换瞬间**不要**做 `filter` 过渡（整页滤镜极贵）。
- 尊重 `prefers-reduced-motion`：`@media (prefers-reduced-motion: reduce) { * { transition-duration: 0s !important } }`。

---

## 10. 暗色专属的无障碍陷阱

| 陷阱 | 说明 | 修法 |
|---|---|---|
| **纯白晕光** | `#fff` on `#000` = 21:1，光渗导致文字"发胖"、边缘发虚 | 文字降到 tone 90 / 85% 白（§3） |
| **细字重在暗底上消失** | 中文 300 字重 + 12px + 暗底 = 不可读 | 暗色下**不要降字重**；中文正文 ≥14px |
| **对比度"看着够"其实不够** | 暗色的高对比容易让人误判；4.499 仍不达标（不可四舍五入） | 用工具实测，不靠眼睛 |
| **禁用态完全不可辨** | `opacity:.4` 后与背景差 <1.5 | 加 1px 边框 + 保留形状 |
| **焦点环消失** | 深色焦点环在深底上不可见 | 亮色环 ≥3:1，或双色环 |
| **OLED 纯黑拖影** | M2 明确警告：OLED 上像素开关会造成滚动延迟/模糊 | 内容滚动区避免纯黑底，用 `#0a0a0a`~`#121212` |
| **色盲在暗色下更差** | 暗色降低了色相区分度 | 不只靠颜色，配形状/符号/文字（涨跌加箭头） |
| **系统高对比模式叠加** | iOS Increase Contrast 下暗色可能"深字压深底" | 必须实测该组合 |

---

## 11. 场景速查（12 个高频问题 → 直接答案）

| 问题 | 答案 |
|---|---|
| 底色用纯黑还是深灰？ | 默认深灰 `#161616`；移动 OLED 内容型可纯黑但文字必须降档 |
| 卡片怎么浮起来？ | surface 提亮一档（+8~12）+ 1px 边框；别指望阴影 |
| 正文用什么白？ | `#e6e6e6` / 85% 白，**不用 `#fff`** |
| 辅助文字多少对比？ | ≥4.5:1；Ant 的 45% 在纯黑上只有 4.43，要提到 50%+ |
| 边框多亮？ | 表单控件 ≥3:1（`#6f6f6f`）；装饰线 1.5–2.1 |
| 阴影怎么做？ | 黑投影做体积 + 极淡白描边做分离；别单用白 glow |
| 主色直接用亮色那套？ | 不行。取 tone 80 / 200 色阶；容器用 tone 30 + 字 tone 90 |
| 图片白底怎么办？ | 压暗 8–12% + 1px 边框 |
| 怎么防首屏白闪？ | `<meta name="color-scheme">` + head 内联脚本，顺序不能错 |
| 小程序要不要开 darkmode？ | 要，否则拿不到 `theme`、收不到切换事件（但媒体查询仍会生效） |
| 半套暗色能不能先上？ | 不能。要么全做，要么不做 |
| 怎么验？ | §12 自检 + 真机低亮度 + 灰度屏 + 色盲模拟三件套 |

---

## 12. 上线自检（22 项，逐条打勾）

**决策层**
1. [ ] 目标用户/场景已确认，暗色是"提供选项"而非"默认强制"（除非媒体/大屏场景）
2. [ ] 三态切换（浅/深/跟随系统），默认跟随系统
3. [ ] 全站覆盖：登录页、错误页、邮件模板、空态、弹窗、第三方嵌入

**表面层**
4. [ ] 底色不是"亮色背景直接反相"，是独立选定的深色值
5. [ ] 有 ≥4 档 surface 层级，且暗色层级跨度 **大于** 亮色（不是照抄亮色差值）
6. [ ] 相邻层之间不只有 tone 差，还配了边框或阴影
7. [ ] 最亮那层表面上的正文仍 ≥4.5:1

**文字层**
8. [ ] 主文本不是 `#fff`（tone 90 / 85% 白）
9. [ ] 三级/辅助文字实测 ≥4.5:1（不是照抄 45% alpha）
10. [ ] 禁用态有边框或形状信号，不只靠透明度
11. [ ] 中文正文 ≥14px，暗色下未降字重

**色彩层**
12. [ ] 品牌主色重映射（tone 80 / 200 阶），不是反相
13. [ ] 语义色（成功/警告/错误/涨跌）各有一套暗色值，且实测过对比度
14. [ ] 涨跌/状态色做过色盲模拟，不只靠色相

**组件层**
15. [ ] Hover/Active 在暗色是"提亮"，不是"加深"
16. [ ] Focus 环在暗底 ≥3:1
17. [ ] Scrim 透明度 ≥60%
18. [ ] Skeleton 比卡片底**亮**一档
19. [ ] 表单控件边界 ≥3:1

**资产层**
20. [ ] 白底图已压暗 + 加边框；深色透明图已换浅色版；图标用 `currentColor`
21. [ ] Logo 有浅色/单色版

**工程层**
22. [ ] `meta color-scheme` + head 内联脚本（无 FOUC）；`color-scheme` 已设（滚动条/表单跟随）；真机低亮度 + 灰度 + 系统高对比三种条件复测

---

## 13. 反模式（20 条，看到就是错）

1. **`filter: invert(1)` 整页反相**——图片、品牌色、肤色全毁
2. **`#fff` 文字 + `#000` 底**——21:1 晕光，长时间阅读最累
3. **照抄亮色的层级差值**——暗色需要更大跨度（1.50 vs 1.23）
4. **只靠阴影表达高度**——暗底上阴影不可见，等于没有层级
5. **只靠白 glow 表达高度**——像"发霉"，M2 明确反对
6. **主色直接复用亮色 hex**——高饱和在深底上光学振动
7. **涨跌色只做一套**——亮色红在暗底上"跳"
8. **表单边框用 `#424242`**——2.09:1，不过 1.4.11
9. **三级文字抄 45% alpha**——纯黑底 4.43，不达标
10. **`opacity: .4` 做禁用**——暗色下沉进背景，完全不可辨
11. **Focus 环用深色**——在暗底上不可见
12. **半套暗色**——登录页/错误页漏掉
13. **应用内独立外观开关**（不给"跟随系统"）——Apple 明确反对
14. **没有 `meta color-scheme`**——首屏白闪 + 滚动条仍是亮色
15. **`color-scheme` 没设**——原生表单控件（select/date/checkbox）仍是白底
16. **`* { transition: all .3s }`**——切换主题时整页卡顿
17. **暗色下把图片直接反相**——白底截图变黑底但文字也反了
18. **深色透明 PNG 直接用**——在暗色里"消失"
19. **Scrim 仍用 40%**——前景不够前，层级失效
20. **只在设计稿里验收**——真机低亮度 + 灰度屏 + 系统高对比三件套必须过

---

## 14. 可抄代码（4 段）

### 14.1 完整变量骨架（亮/暗双套，含层级与文字四档）

```css
:root {
  color-scheme: light dark;

  /* 表面层级：亮色往下压 */
  --surface-0: #f5f5f5;   /* 页面底 */
  --surface-1: #ffffff;   /* 卡片 */
  --surface-2: #ffffff;   /* 浮层（靠阴影区分） */
  --surface-3: #ffffff;   /* 模态 */

  /* 文字四档（亮色 88/65/45/25） */
  --text-1: rgba(0,0,0,.88);
  --text-2: rgba(0,0,0,.65);
  --text-3: rgba(0,0,0,.45);
  --text-4: rgba(0,0,0,.25);

  --border-strong: #8c8c8c;  /* 控件边界，≥3:1 */
  --border-subtle: #e8e8e8;  /* 装饰分隔 */
  --shadow-2: 0 6px 16px rgba(0,0,0,.08), 0 3px 6px rgba(0,0,0,.12);
}

:root[data-theme="dark"] {
  /* 表面层级：暗色往上提（跨度更大） */
  --surface-0: #0d0d0d;   /* 页面底 */
  --surface-1: #161616;   /* 卡片  +8 档 */
  --surface-2: #1f1f1f;   /* 浮层  +12 档 */
  --surface-3: #2b2b2b;   /* 模态  +20 档 */

  /* 文字四档（暗色 85/65/52/32 —— 三档从 45% 提到 52%） */
  --text-1: rgba(255,255,255,.85);
  --text-2: rgba(255,255,255,.65);
  --text-3: rgba(255,255,255,.52);
  --text-4: rgba(255,255,255,.32);

  --border-strong: #6f6f6f;  /* 3.6:1，过 1.4.11 */
  --border-subtle: #2e2e2e;  /* 1.5:1，装饰用 */
  --shadow-2: 0 6px 16px rgba(0,0,0,.48), 0 0 0 1px rgba(255,255,255,.06);
}

/* 只给颜色加过渡，别用 * */
body, .card, .btn { transition: background-color .2s ease, color .2s ease, border-color .2s ease; }
@media (prefers-reduced-motion: reduce) { * { transition-duration: 0s !important; } }
```

### 14.2 防 FOUC 的三行脚本（放 `<head>` 最前，不 defer）

```html
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#161616" media="(prefers-color-scheme: dark)">
<script>
  (function () {
    var t = localStorage.getItem('theme');
    var d = t === 'dark' || (!t && matchMedia('(prefers-color-scheme: dark)').matches);
    document.documentElement.dataset.theme = d ? 'dark' : 'light';
  })();
</script>
```

### 14.3 三态切换组件逻辑

```js
const mq = matchMedia('(prefers-color-scheme: dark)');

function apply(mode) {            // mode: 'light' | 'dark' | 'system'
  const dark = mode === 'dark' || (mode === 'system' && mq.matches);
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
}

function setMode(mode) {
  if (mode === 'system') localStorage.removeItem('theme');
  else localStorage.setItem('theme', mode);
  apply(mode);
}

// 仅当用户选了"跟随系统"时，才响应系统切换
mq.addEventListener('change', () => {
  if (!localStorage.getItem('theme')) apply('system');
});
```

### 14.4 暗色图片处理

```css
/* 照片：轻微压暗，不反相 */
:root[data-theme="dark"] img.photo { filter: brightness(.88) contrast(1.02); }

/* 白底截图：压暗 + 边框，避免"发光白块" */
:root[data-theme="dark"] img.screenshot {
  filter: brightness(.9);
  outline: 1px solid rgba(255,255,255,.12);
  border-radius: 6px;
}

/* 纯黑白线稿：可以反相（仅限真·纯黑白） */
:root[data-theme="dark"] img.lineart { filter: invert(1) hue-rotate(180deg); }

/* 图标一律跟随文字 */
.icon { color: currentColor; }
```

---

## 15. 参考来源

- **Material Design 3 · Color roles / 源码**：`material-color-utilities` 的 `dynamiccolor/color_spec_2021.ts`（surface 与容器 tone、ContrastCurve 四级）、`scheme/scheme.ts`（亮/暗角色 tone 全表）、`dynamiccolor/contrast_curve.ts`（-1.0/0.0/0.5/1.0 语义）
- **Material Design 2 · Dark theme**：`m2.material.io/design/color/dark-theme.html`（`#121212`、elevation overlay 0–16% 全表、200 色阶规则、文字 87/60/38、`#CF6679`、纯黑仅限省电场景）
- **Ant Design · 暗色算法源码**：`components/theme/themes/dark/colors.ts`（85/65/45/25 文本 alpha、18/12/8/4 填充、lighten 0/8/12/26）、`dark/index.ts`、`dark/colorAlgorithm.ts`（`getSolidColor=lighten`）、`default/colors.ts`（亮色 88/65/45/25 对照）、`util/alias.ts`（boxShadow 由 `colorShadow` 派生）
- **Carbon Design System**：`packages/themes/src/v10/g100.ts`（layer 阶梯与 text01-03）、`@carbon/colors@11.61.0` 包内 `es/index.js`（gray10–gray100 全 hex）
- **Apple HIG · Dark Mode**：base/elevated 两套背景、4.5:1 下限与 7:1 建议、非反相声明、白底图压暗、双套图标案例
- **Radix Colors · Understanding the scale**：12 步语义、步骤 11/12 在步骤 2 背景上保证 Lc 60 / Lc 90（APCA）
- **Nielsen Norman Group · Dark Mode**：正极性优势、Piepenbrock 2013 / *Human Factors*、Dobres 2017、Aleman 2018、低视力（Legge）与"不建议默认暗色"立场
- **Android Developers · Implement dark theme**：DayNight、`MODE_NIGHT_*`、`forceDarkAllowed`、API 31 `UiModeManager`
- **微信开放文档 · DarkMode 适配指南**：`darkmode`/`themeLocation`/`theme.json` 变量清单、`onThemeChange`、媒体查询不受开关影响、iOS 7.0.12 tabBar bug
- **MDN · `color-scheme` / `light-dark()` / `prefers-color-scheme`**：影响范围、`only light` 关闭 Auto Dark Theme、FOUC 防法
- **Tailwind CSS v4 · Dark mode**：`@custom-variant` 两种写法、class/data 策略、FOUC 内联脚本示例
- **WCAG 2.2**：SC 1.4.3（4.5:1，不可四舍五入）、SC 1.4.11（非文本 3:1）——完整口径见 `accessibility.md`
- 本文所有对比度数值由 WCAG 相对亮度公式与 CIELAB L*→Y 换算**实测计算**，非引用
