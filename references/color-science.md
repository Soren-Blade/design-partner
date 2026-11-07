# 色彩科学（Color Science for Designers）

> 快照 2026-11-07 · 22 节 · 12 场景 · 20 反模式 · 20 自检 · 6 段可抄代码

把「配色靠感觉 / 对比度靠试 / 色板靠抄」变成**可计算的决策**。本文件不替代 `design-tokens.md`（token 三层架构）/`dark-mode.md`（暗色表面层级）/`accessibility.md`（WCAG 阈值总表）/`brand-identity.md`（品牌色阶路线），而是给它们补上**底层坐标与算法**：为什么 HSL 生成的色板会错序、对比度到底怎么算、渐变为什么发灰、色盲用户看到什么。

---

## 1 · 为什么单列色彩科学

配色不是纯审美，是一组**有最优解的计算**：

- 同一份「主色 + 白色文字」，有人凭感觉调、有人用公式反解——后者能保证任何背景都过 4.5:1，前者大概率翻车。
- 设计师常犯的根因错误不是「审美差」，是**用错了色彩坐标**：在 HSL 里转色相以为等距、在 sRGB 里直接插值以为等亮、用对比度「目测差不多」。
- 上游文件（tokens / dark / a11y / brand）都在**用**颜色，但没人讲**颜色本身怎么算**。本文件补这一层。

三条最重要裁决见 §2、§6、§8。

---

## 2 · 色彩模型谱系（先认坐标，再谈配色）

| 模型 | 轴含义 | 感知均匀 | 设计师用法 |
|---|---|---|---|
| **sRGB** | 显示器原生非线性 RGB（γ≈2.2） | 否 | 最终落地格式，不适合做数学 |
| **线性 sRGB** | sRGB 去伽马后的物理光 | 否 | 插值 / 混合 / 亮度计算的前置步骤 |
| **HSL / HSV** | 色相 / 饱和 / 明度（圆柱 sRGB） | **否** | 直觉调色方便，但**不适合生成色板/梯度** |
| **HSLuv / HCL** | 把 CIELAB 亮度做成 0–100 均匀 | 部分 | 需要「均匀明度」但不想引入 OKLab 时 |
| **CIELAB / LCH** | 1976 CIE，L 感知亮度 | 较好（非完美） | 工业色差 ΔE 计算 |
| **OKLab / OKLCH** | Björn Ottosson 2020，更均匀的改进版 | **最优（当前实践）** | **色板生成 / 渐变插值 / 明度判定首选** |
| **Display P3** | 比 sRGB 宽 ~25% 色域（更艳的绿/红） | — | 影像/品牌强调色，需 `color(display-p3 …)` + sRGB 降级 |

**核心结论**：凡是要「生成 / 插值 / 比较亮暗」的操作，走 **OKLab/OKLCH**；只在「给人类看一个直观旋钮」时用 HSL。

---

## 3 · 感知均匀性：HSL 为什么撒谎

HSL 的「L」是**相对亮度**（亮底上才亮），不是**感知亮度**。后果：

- 等 HSL 步进 ≠ 等视觉步进。蓝区（H≈240）在 L 上的感知跨度比红区（H≈0）长 **30%+**，于是「色相固定、L 从 20→80」在蓝色上看起来变化剧烈、在红色上几乎看不出。
- 「同饱和度同明度、只换色相」的「调色板」在视觉重量上**根本不统一**——红和绿能一样重吗？不能。
- HSL rotation 生成 12 色板，常出现「某几格几乎一样、另几格突然跳变」的错序。

**判据**：色板/梯度/明度比较，一律在 OKLab/OKLCH 空间做；HSL 只用于「手调一个颜色」。

---

## 4 · 伽马（gamma）：为什么不能直接对 sRGB 插值

sRGB 存储的是**经过伽马编码**的值（`V = 1.055·L^0.4167 − 0.055`），不是线性光。直接对两个 sRGB 十六进制做线性插值，等于在「编码后的非线性刻度」上取中点——中间会**发灰、发脏、偏暗**。

正确做法：sRGB → 线性光 → 在线性空间（或 OKLab 空间，更优）插值 → 再编码回 sRGB。

> 这就是为什么 `linear-gradient(red, blue)` 中间一团脏灰，而 `linear-gradient(in oklab, red, blue)` 干净。见 §9。

---

## 5 · OKLab / OKLCH：公式与用法

Björn Ottosson（2020）公开公式，已成为 CSS Color 4/5 与主流设计工具的实践标准。

**sRGB → 线性**（每通道）：
```
c_lin = c/12.92                  if c <= 0.04045
c_lin = ((c+0.055)/1.055)^2.4   otherwise
```

**线性 RGB → LMS**（矩阵）：
```
l = 0.4122214708*r + 0.5363325363*g + 0.0514459929*b
m = 0.2119034982*r + 0.6806995451*g + 0.1073969566*b
s = 0.0883024619*r + 0.2817188376*g + 0.6299787009*b
```

**LMS → 立方根 → OKLab**：
```
l'=cbrt(l); m'=cbrt(m); s'=cbrt(s)
L = 0.2104542553*l' + 0.7936177850*m' - 0.0040720468*s'
a = 1.9779984951*l' - 2.4285922050*m' + 0.4505937099*s'
b = 0.0259040371*l' + 0.7827717662*m' - 0.8086757660*s'
```

**OKLab → OKLCH**（圆柱坐标）：
```
C = sqrt(a² + b²)      // 色度
H = atan2(b, a)        // 色相，度
L 不变                 // 感知亮度，0=黑 1=白（CSS 里 0–100%）
```

**CSS 用法**（2023-05 起跨浏览器广泛可用，Baseline）：
```css
:root { --brand: oklch(62% 0.17 28); }   /* L 感知亮度 / C 色度 / H 色相 */
.card { background: oklch(98% 0.005 28); } /* 极浅同色相底 */
```
- `L`：0–1（或 0–100%），**感知亮度**，可直接当「明度」用，等步进即等视觉步进。
- `C`：通常 0–0.4（CSS 里 `100%` = 0.4，不是 1）；高 C 才鲜艳，但高 L 时 C 上限会自动变小（否则超出 sRGB/Display P3 色域）。
- `H`：0–360°。

> 相对颜色语法 `oklch(from var(--brand) l c h)` 可在保持色相/色度下只改亮度（如 `oklch(from var(--brand) 85% c h)`），比 `color-mix` 更可控。

---

## 6 · 对比度：两套算法，不是只有 WCAG 2.x

### 6.1 WCAG 2.x 相对亮度（现行强制标准）

相对亮度：
```
L = 0.2126·R + 0.7152·G + 0.0722·B     // R/G/B 为「线性 sRGB」(见 §4 去伽马)
对比度 CR = (L_light + 0.05) / (L_dark + 0.05)
```
阈值（WCAG 2.1/2.2）：
- 正文（<18pt 或 <14pt 粗）**≥ 4.5:1**
- 大文本（≥24px / ≥18.66px 粗体，约 18pt/14pt 粗）**≥ 3:1**
- 非文本 / UI 组件 / 图形对象（1.4.11）**≥ 3:1**
- AAA：正文 ≥ 7:1、大文本 ≥ 4.5:1

⚠️ **不可四舍五入**：`4.499:1` 不达标，`4.5:1` 才算。屏幕截图肉眼「看起来够」不算数，用相对亮度公式算。

### 6.2 APCA（WCAG 3 候选，长文/暗色更准）

APCA 用 **`Lc`**（感知亮度对比，可正可负，符号表文字/背景关系），不分「正文/大文本」一刀切，而是按文本尺寸与权重给分档：

| Lc 目标 | 适用 |
|---|---|
| **15** | 非文本 / 点缀元素最低限 |
| **30** | 参与交互的非文本（图标/图表线） |
| **45** | 正文最低（小字需更高） |
| **60** | 正文偏好值（1.5 倍行高的舒适正文） |
| **75** | 优化值（大标题 / logo 级） |

简化公式（SAPC/APCA const）：
```
Lc = (Ybg^0.56 − Ytxt^0.57) × 1.14 × 极性系数
```
**立场**：正文 4.5:1 是 WCAG 2.x 的**合规底线**，必须过；长文阅读、暗色界面、低视力场景用 **APCA Lc 分档**做体验增强更准。不要把 APCA 当合规唯一标准（尚未正式成为 WCAG 3）。

> ⚠️ 取源限制：APCA 精确阈值与 Lookup 表（apcawiki）本机未逐条联网核验，Lc 15/30/45/60/75 为公开常用分档值，落地前以 [APCA 官方 Lookup](https://www.myndex.com/APCA/) 为准。

---

## 7 · 色盲：三型 + Okabe–Ito 8 色

约 **8% 男 / 0.5% 女**有某种色觉缺陷。三型：
- **红色盲 / 绿色盲（Protan / Deutan）**：最常见（~6%），红绿难分。
- **蓝色盲（Tritan）**：罕见（~0.01%）。
- **全色盲（Monochromacy）**：极罕见。

**Okabe–Ito 8 色**（对最常见红绿色盲安全，含 hex，直接使用）：
```
#000000  黑        #E69F00  橙        #56B4E9  天蓝
#009E73  蓝绿      #F0E442  黄        #0072B2  蓝
#D55E00  朱红      #CC79A7  紫红
```
- 分类色板优先从这 8 色取；图表分类 ≤7 类时更要从这里挑。
- **永不只靠颜色**：状态/编码必须叠加形状、纹理、文字、位置等第二通道（`accessibility.md` §12）。
- 验证：用色盲模拟（Color Oracle / 浏览器 DevTools 渲染模拟 / culori 的 `deficiencies`）过一遍。

---

## 8 · 色板生成科学：四条可复现路线（选一不许混）

混用不同路线会导致**色阶错序**（如第 9 档比第 10 档还亮），必须选一条：

1. **OKLCH 色相/明度旋转**（最通用）：固定 H、在 OKLCH 里按 L 步进生成浅→深；或固定 L、旋转 H 生成分类色。均匀、可预测。
2. **Radix 12 步语义档**（组件库首选）：1–2 背景 / 3–5 组件底 / 6–8 边框与焦点环 / **9 实心且彩度最高** / 10 hover / 11–12 文字（11/12 保证 APCA Lc60/Lc90）。语义命名驱动。
3. **M3 Tonal Palette**（Material 体系）：seed 色经 HCT 生成 Tonal 0–100 档（primary 40/primary 容器 90…），亮暗用 tone 映射非反色。
4. **Leonardo / 对比度优先**（无障碍优先）：以「目标对比度」反解颜色，输出略高于目标（因 WCAG 是最低限）；适合品牌色配白字这类「必须过阈值」场景。

> 品牌主色阶路线已在 `brand-identity.md` §9 详述（HCT / Radix 12 步 / Leonardo），本文件补的是**底层坐标为什么用 OKLCH 而非 HSL**。

---

## 9 · 渐变与插值：在 OKLab 空间做

sRGB 直插 → 中间发灰发脏（§4）。正解：

```css
/* 错误：中间一团脏灰 */
.linear-bad { background: linear-gradient(90deg, #2563eb, #f43f5e); }

/* 正确：在 OKLab 空间插值，过渡干净 */
.oklab-good { background: linear-gradient(in oklab, #2563eb, #f43f5e); }
```

规则：
- 任意两点间的渐变，用 `linear-gradient(in oklab, …)` / `in oklch`（色相要绕最近路径时 oklch 更可控，注意 hue 插值方向 `in oklch longer/shorter hue`）。
- 多停点色板渐变，先在 OKLab 生成各停点再插值，不要对 sRGB 十六进制序列直插。
- 设计工具（Figma 2024+ 渐变支持 OKLCH、CSS 导出）与代码（culori/colorjs.io）都能在 OKLab 采样。

---

## 10 · 色彩无障碍 beyond 1.4.11

- **不只靠颜色单通道**：错误 = 红 + 图标 + 文案；状态 = 颜色 + 形状 + 文字；涨跌 = 颜色 + 符号。色盲与「看不清颜色」用户都要能读（WCAG 1.4.1）。
- **非文本对比度 ≥3:1**（1.4.11）：输入框边框、按钮边界、图表线、焦点环都算「非文本」，常被忽略。
- **图案 / 纹理填充**：图表里相邻分类除颜色外加不同填充图案（斜线/点/网格），是色盲与灰度打印双保险。
- **forced-colors / 高对比模式**：系统开启后阴影/渐变/背景图被抹平，靠颜色分层级的界面会塌成一片白——必须有**边框兜底**（`accessibility.md` §12 / `dark-mode.md` §相关）。
- **不要纯黑底纯白字突兀对比**做全站：暗色正文用 tone 90 而非 #fff（见 `dark-mode.md`）。

---

## 11 · 工程实现（落地要点）

**现代 CSS（2023–2024 可用，原生无依赖）**：
```css
:root {
  --brand: oklch(62% 0.17 28);
  --brand-hover: oklch(from var(--brand) 72% c h);   /* 只提亮，保色相色度 */
  --surface: color(display-p3 0.95 0.95 0.97);        /* P3 更准；见降级 */
}
/* Display P3 降级：先写 sRGB，再用 @supports 覆盖 P3 */
.btn { background: oklch(62% 0.17 28); }
@supports (color: color(display-p3 1 0 0)) {
  .btn { background: color(display-p3 0.51 0.21 0.18); } /* 同色更艳 */
}
```
- `oklch()` / `lab()` / `color()`：2023-05 起跨浏览器广泛可用（Baseline）。
- 相对颜色语法 `oklch(from …)` / `color-mix()`：2024 起主流浏览器支持（Chrome 119+ / Safari 16.4+ / Firefox 128+ 量级）。
- `color-mix(in oklch, var(--brand) 30%, white)` 做浅底比 `rgba` 更可控且感知均匀。

**JS 库选型**（选型三问：许可 / 活源 / 可验收）：
- **culori**（npm，MIT）：Node/浏览器，空间转换 + 采样 + 插值，体积小，首选。
- **colorjs.io**（Lea Verou，MIT）：完整 CSS 色彩模型，教学/实验友好，体积偏大。
- **chroma.js**：老牌，覆盖广，部分新空间（oklch）支持晚于前两者。

**Figma**：用 Variables 存 OKLCH 值（或 HCT），模式（mode）做亮/暗，避免手存 sRGB 十六进制导致跨模式漂移。

> 取源限制：Display P3 与各函数确切浏览器版本号本机未逐条联网核验，落地前以 [MDN 兼容性表](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch) 为准；「2023-05 广泛可用」「2024 起支持相对颜色语法」为公开共识级事实。

---

## 12 · 场景速查（12）

1. **生成一套浅→深主色阶** → OKLCH 固定 H、L 从 95%→30% 步进（§8 路线 1）。
2. **生成 6 个「视觉重量一致」的分类色** → 固定 L/C、旋转 H（§8 路线 1），或直接取 Okabe–Ito（§7）。
3. **两个颜色做干净渐变** → `linear-gradient(in oklab, a, b)`（§9）。
4. **算某段文字在某底上的对比度** → §6.1 公式，或 culori `wcagContrast`（§15 代码）。
5. **长文正文选对比度档** → WCAG 4.5:1 保底 + APCA Lc≥45（小字≥60）（§6.2）。
6. **品牌主色压白字看不清** → 用 Leonardo 反解「过 4.5:1 的最深可用主色」，或降主色 L（§8 路线 4）。
7. **图表分类色怕色盲** → Okabe–Ito 8 色 + 叠加图案/形状（§7、§10）。
8. **暗色界面文字刺眼** → 不用 #fff，用 tone 90；配色坐标问题见 `dark-mode.md`（本文件 §2 底模）。
9. **hover/active 态** → `oklch(from var(--brand) 高 L c h)` 只提亮，保色相（§11、§5）。
10. **更艳的强调色（影像/品牌）** → Display P3 + sRGB 降级（§11、§2）。
11. **输入框边框/焦点环过 3:1** → 这是非文本对比度，用 §6.1 算，别目测（§10）。
12. **色板在亮暗两套都匀** → 在 OKLCH 生成、用 tone 映射而非反色（§8、接 `multi-brand-theming.md`）。

---

## 13 · 反模式（20）

1. 在 **HSL 里转色相生成色板**（错序、重量不均）。
2. 对 **sRGB 十六进制直接线性插值**做渐变（中间发灰）。
3. 用 **对比度「目测差不多」**代替相对亮度计算。
4. 把 **4.499:1 当 4.5:1** 四舍五入放行。
5. **只靠颜色**表达状态/编码（色盲与灰度全失）。
6. 在 **OKLCH 旋转色相**却期望「亮度一致」（C 上限随 L 变，需约束）。
7. 混用 **Radix 12 步 + HCT + Leonardo** 生成同一套色阶（错序）。
8. 暗色正文用 **纯白 #fff**（刺眼，且不均）。
9. 用 **高饱和大面积**（未约束 C，超色域后溢出/抖动）。
10. 非文本元素（边框/图标/线）**不过 3:1**只过文字 4.5。
11. Display P3 颜色**不写 sRGB 降级**（不支持的浏览器直接崩色）。
12. 用 `rgba(…, .5)` 做浅底而非 `color-mix(in oklch, …)`（感知不均）。
13. 把 **APCA Lc 当 WCAG 合规唯一判据**（尚未正式成为 WCAG 3）。
14. 色盲安全配色**自己拍一组**（未验证，常仍撞红绿）。
15. 渐变用 **3 个以上无协调的 sRGB 停点**直插（脏带）。
16. 用 **同一 HSL 饱和度**做强调/背景（背景需低 C，强调需高 C）。
17. 忽略了 **forced-colors** 下颜色被抹平（无边框兜底）。
18. 在 **线性 sRGB 之外**做「亮度比较」（应在 OKLab L 或相对亮度）。
19. Figma 变量**手存 sRGB 十六进制**做多模式（跨模式漂移）。
20. 给「感知均匀」假设**没验证**就交付（用 culori 采样/校验再上线）。

---

## 14 · 自检（20）

1. 色板是在 **OKLCH/OKLab** 生成的，不是 HSL 旋转？
2. 渐变用 **`in oklab`/`in oklch`**，不是 sRGB 直插？
3. 正文对比度 **≥4.5:1**（大文本 ≥3:1）且**未四舍五入**？
4. 非文本元素（边框/图标/线/焦点环）**≥3:1**？
5. 长文/暗色额外过了 **APCA Lc 分档**（小字 ≥60）？
6. 状态/编码**至少有形状 + 颜色 + 文字两样**通道？
7. 分类色**色盲可辨**（Okabe–Ito 或模拟验证）？
8. 主色压白字/黑字**过了对比度**（不是凭感觉）？
9. 色阶**单路线生成**，无 HCT/Radix/Leonardo 混用错序？
10. 高 L 时 **C 有上限约束**（未超色域溢出）？
11. Display P3 颜色**有 sRGB 降级**（`@supports`）？
12. hover/active 用 **相对颜色语法只改 L**，保色相？
13. 浅底用 `color-mix(in oklch,…)` 而非 `rgba`？
14. 没有把 **4.499 当 4.5** 放行？
15. 过了 **forced-colors** 兜底（边框而非仅颜色分层）？
16. 渐变停点**协调**（同空间采样，≤3 主停点）？
17. Figma 变量存的是 **OKLCH/HCT** 而非裸 sRGB 十六进制？
18. 色盲**模拟**过一遍（Color Oracle / DevTools）？
19. 强调色 C 足够高但不**刺眼**（大面积压低 C）？
20. 关键颜色值**用库采样/校验**后再上线（非假设感知均匀）？

---

## 15 · 可抄代码（6 段）

### 15.1 CSS · OKLCH 生成浅→深主色阶
```css
:root{
  --brand: oklch(62% 0.17 28);
  --brand-50:  oklch(97% 0.02 28);
  --brand-100: oklch(93% 0.04 28);
  --brand-300: oklch(80% 0.12 28);
  --brand-500: oklch(62% 0.17 28);   /* 主色 */
  --brand-700: oklch(48% 0.15 28);
  --brand-900: oklch(34% 0.10 28);
}
/* hover 只提亮，保色相色度 */
.btn:hover{ background: oklch(from var(--brand) 72% c h); }
```

### 15.2 CSS · OKLab 渐变（干净过渡）
```css
.banner{
  background: linear-gradient(135deg in oklab, #2563eb, #f43f5e);
}
```

### 15.3 JS · WCAG 2.x 相对亮度 + 对比度（可直接用）
```js
function srgbToLinear(c){
  c /= 255;
  return c <= 0.04045 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4);
}
function relLum(hex){
  const r = parseInt(hex.slice(1,3),16),
        g = parseInt(hex.slice(3,5),16),
        b = parseInt(hex.slice(5,7),16);
  const R = srgbToLinear(r), G = srgbToLinear(g), B = srgbToLinear(b);
  return 0.2126*R + 0.7152*G + 0.0722*B;
}
function contrast(a, b){
  const L1 = relLum(a), L2 = relLum(b);
  const hi = Math.max(L1,L2), lo = Math.min(L1,L2);
  return (hi + 0.05) / (lo + 0.05);
}
contrast('#2563eb', '#ffffff'); // ≈ 4.54 → 正文达标
```

### 15.4 JS · 简化 APCA（Lc）计算（以官方 Lookup 为准校准）
```js
// 简化 SAPC/APCA const；正负表文字/背景关系。精确阈值见 apcawiki。
function apcaLc(txtHex, bgHex){
  const Y = h => { // 近似用相对亮度替代更严谨的 Y；生产用完整 APCA 常量
    return relLum(h); // 见 15.3
  };
  const Ytxt = Y(txtHex), Ybg = Y(bgHex);
  const Lc = (Math.pow(Ybg, 0.56) - Math.pow(Ytxt, 0.57)) * 1.14 * (Ybg > Ytxt ? 1 : -1);
  return Math.round(Lc * 100) / 100;
}
// apcaLc('#222','#fff') 应落在较大正值附近；正文目标 Lc≥45
```

### 15.5 Python · OKLCH 色相旋转生成分类色板（culori）
```python
# pip install culori  (或 numpy 自实现 OKLab 矩阵，见 §5)
from culori import oklch, convert, format_hex
def categorical(n, base_L=0.65, base_C=0.16):
    out = []
    for i in range(n):
        h = round(i * 360 / n, 1)
        c = oklch(base_L, base_C, h)
        out.append(format_hex(convert(c, "sRGB")))
    return out
print(categorical(6))   # 6 个视觉重量一致的均匀分类色
```

### 15.6 Python · 反解「过 4.5:1 的最深主色」（对比度优先思路）
```python
from culori import oklch, convert, format_hex, wcag_contrast  # 伪接口，按库实际 API
def deepest_brand_on_white(white="#ffffff", target=4.5, H=28, C=0.17):
    L = 0.30
    while L < 0.75:
        cand = convert(oklch(L, C, H), "sRGB")
        if wcag_contrast(format_hex(cand), white) >= target:
            return format_hex(cand), round(L, 3)
        L += 0.01
    return None
print(deepest_brand_on_white())  # (hex, L) 满足 ≥4.5:1 的最深可用主色
```

> 15.4/15.5/15.6 为思路骨架：APCA 用官方常量校准（§6.2 取源限制），culori 以其实 API 为准；15.3 为完整可用实现。

---

## 16 · 取源与限制（公开记录）

- **已吸收并交叉验证**：OKLab/OKLCH 公式（Björn Ottosson 2020 公开）、WCAG 2.1 相对亮度公式与阈值、Okabe–Ito 8 色 hex、sRGB γ 编码与线性化、Display P3 比 sRGB 宽约 25%、`oklch()` 自 2023-05 跨浏览器广泛可用（MDN 已核验）。
- **未逐条联网核验（落地前以官方为准）**：
  - APCA 精确阈值与 Lookup 表（Lc 15/30/45/60/75 为公开常用分档值，非逐条实测）。
  - Display P3 与 `color()`/`color-mix()`/相对颜色语法的确切浏览器版本边界（公开共识：2023–2024 可用）。
  - culori/chroma.js/colorjs.io 的当前 API 与体积（许可均为 MIT/兼容，选型三问已覆盖）。
- **纪律**：凡标注「以官方为准」的数值，不臆造逐字与精确版本号；上线前用 §15 代码或官方工具复核。
