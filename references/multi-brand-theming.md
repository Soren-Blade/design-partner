# 多品牌与多主题 Token 架构 — Multi-brand & Multi-theme

> 本文件解决「**一套产品要服务 N 个品牌 / N 种外观，怎么不失控**」。
> 蒸馏自：Material 3 `dynamic_scheme.ts` 源码（2021 与 2025 两版 spec 的色度常量全表）、Fluent UI `packages/tokens/src/types.ts`、GitHub Primer 主题文件结构、Carbon 四主题 token 对照、TDesign 中文色板规范、Radix 12 步与 Lc 保证、Ant Design Seed/Map/Alias 三级推导、DTCG 2025.10 格式草案、Style Dictionary 多品牌构建、CSS `@layer` 层叠规则。
> 对比度数值**全部由本技能自算**（WCAG 相对亮度公式，见 §5），不是抄二手结论。
> 快照 2026-11-01
> 使用时机：白标 / 私有化部署 / 多子品牌 / 换肤 / 主题切换 / 客户自带品牌色 / 设计系统对外售卖。

---

## 一、判据：什么时候真的需要多品牌架构

先判「要不要」，再判「怎么做」。多数团队在只需要 **1 个品牌 × 2 个模式** 时上了四层品牌架构，结果是维护成本翻倍、收益为零。

| 场景 | 真实需求 | 该做什么 | 不该做什么 |
|---|---|---|---|
| **白标 SaaS**（一套产品卖给 N 个客户） | 客户要自己的主色 + logo | 品牌层运行时注入 + 对比度护栏 | 给每个客户 fork 一份代码 |
| **集团多子品牌**（A 品牌 / B 品牌共用组件库） | 两套色阶、可能两套字体 | 品牌层 + L1 色阶双套 | 两套语义层（组件行为会分叉） |
| **私有化部署**（客户机房，要求"换成我们的颜色"） | 单客户单品牌，构建期确定 | 构建期编译一份即可 | 为一次交付引入运行时主题引擎 |
| **同一产品的多外观**（明/暗/高对比/色盲友好/紧凑） | 同一品牌，多个**正交轴** | 只改 L2 映射，不动 L1 | 把"暗色"当成"另一个品牌" |
| **设计系统对外售卖** | 客户自带品牌，你只提供骨架 | 品牌输入契约 + 自动色阶 + 护栏 | 允许客户直接改语义 token |
| **营销站多活动页** | 每个活动一套配色 | 局部作用域变量，不建主题体系 | 建一套"活动品牌"架构 |

**判据一句话**：**品牌数是「1 还是 N」，模式数是「1 还是 2+」。两个都 >1 才需要完整架构；只有模式 >1 是 `dark-mode.md` 的活，不是本文件的活。**

---

## 二、主题不是"换色"，是四个正交轴

把主题理解成"一套配色"是最常见的架构错误。真实系统里主题是**多个独立轴的笛卡尔积**，每根轴改动的东西完全不同：

| 轴 | 取值 | 改哪一层 | 是否动 L1 色阶 | 典型来源 |
|---|---|---|---|---|
| **A 品牌 brand** | 品牌 1 / 品牌 2 / … | L0 输入 + L1 全量 | **是**（整套换） | 客户配置 |
| **B 模式 mode** | light / dark | L2 映射 | 否（同一色阶换档位） | 系统偏好 / 用户 |
| **C 对比度 contrast** | normal / high | L2 映射 + 少量 L3 | 否（往色阶两端跳档） | 系统无障碍设置 |
| **D 密度 density** | compact / default / comfortable | 只改 dimension token | 否（完全不碰色） | 用户偏好 / 设备 |
| E 方向 direction | LTR / RTL | 布局 token + 逻辑属性 | 否 | 语言 |
| F 色觉 color vision | normal / protanopia / deuteranopia / tritanopia | 语义色重映射 | 否（同层换色相） | 用户设置 / 系统 |

**组合爆炸必须先算**：4 轴 × 3 值 = 81 种组合。如果每组合手写一份 CSS，等于 81 份需要同步维护的色板——这是所有"主题系统后期崩掉"的根因。

**收敛三原则**：
1. **只有品牌轴允许全量重映射**（它换的是 L1）。其余轴都是**同一 L1 上的不同指针**。
2. **密度轴完全不碰颜色**，所以它永远不参与颜色组合爆炸（`compact × dark × brand-B` 只是把 spacing 变量换一套，与色无关）。
3. **轴之间不许有交叉规则**。一旦出现"品牌 A 的暗色要用特殊的 X"，说明 L1 设计有问题——回去修色阶，不要加 `[data-brand="a"][data-mode="dark"]` 的特例块。**出现第 3 个交叉特例就是架构失败信号。**

**实证：GitHub Primer 用 2 根轴装下 9 个主题**——`data-color-mode`（auto/light/dark）× `data-light-theme` / `data-dark-theme`（light / light_tritanopia / light_high_contrast / light_colorblind / dark / dark_colorblind / dark_dimmed / dark_high_contrast / dark_tritanopia）。不是 9 份独立主题，是 **2 模式 × 5 变体** 的组合。这就是正确做法。

---

## 三、四层架构：在原有三层上加一层"品牌输入"

`design-tokens.md` 里的三层（Base / Semantic / Component）是**单品牌**模型。多品牌必须再加一层，否则品牌值会渗透进语义层：

| 层 | 名称 | 存什么 | 示例 | 谁改 | 跨品牌共享？ |
|---|---|---|---|---|---|
| **L0** | Brand Input | **种子**：1 个品牌色 + 可选字体族 + 圆角基数 + logo | `seed: #0052D9` | 客户填表 | ❌ 每品牌一套 |
| **L1** | Primitive | 由 L0 **算出**的全量色阶（10–14 档 × 若干色相） | `--blue-7: #0052D9`<br>`--gray-3: #E8E8E8` | 生成器 | ❌ 每品牌一套 |
| **L2** | Semantic | 角色 → 指向 L1 的**某个档位** | `--color-brand: var(--blue-7)`<br>`--color-text-primary: var(--gray-1)` | 系统维护者 | ✅ **全部共享** |
| **L3** | Component | 单组件局部覆盖 | `--button-height: 40px` | 组件作者 | ✅ 全部共享 |

**四条铁律**：

1. **品牌只允许注入 L0 与 L1**。L2/L3 由系统统一维护，客户一个字都不能改。
2. **L2 的"映射关系"跨品牌一致**。品牌 A 的 `--color-brand` 指 `blue-7`，品牌 B 指 `green-7`——**指的都是"第 7 档"**，不是"各自的品牌色"这种模糊说法。档位一致才能保证对比度行为一致。
3. **L1 的档位数量必须跨品牌相同**。品牌 A 给 10 档、品牌 B 给 8 档 → L2 映射立刻断裂。这是自动色阶生成器存在的唯一理由。
4. **L2 只允许引用 L1，不允许写字面值**。一旦语义层出现 `#0052D9`，这个品牌就再也换不掉了。

**为什么必须这样分**：品牌换的是"哪种蓝"，不是"哪里用蓝"。前者是值，后者是决策。把决策也交给客户，等于把设计系统交给客户。

**反例（真实高频）**：客户要求"我们的品牌色要出现在主按钮、链接、选中态、图表第一色、进度条"，于是每个品牌各写一套 semantic。三个月后加了新组件，5 个品牌漏了 3 个 → 组件在品牌 C 下是默认蓝。**这是 L2 分叉的必然结局，不是执行不力。**

---

## 四、从 1 个品牌色算出整套色阶：四条路线与精确参数

客户只会给你**一个色值**。你必须用它生成 10–16 档可用的色阶，且每档的对比度行为要可预测。四条成熟路线，各有适用面。

### 4.1 路线 A · M3 HCT 色度常量法（最通用，Android/跨端首选）

做法：把种子色转成 **HCT**（色相 H、色度 C、明度 tone T），**色相继承种子，色度按变体常量固定，明度按需取 0–100 的 tone**。关键在于"色度固定"——这样不同品牌色生成的色阶**饱和度观感一致**，不会一个品牌很灰一个很艳。

**2021 spec 色度常量全表**（`dynamic_scheme.ts`，直接可抄）：

| 变体 Variant | primary C | secondary C | tertiary C | neutral C | neutralVariant C |
|---|---|---|---|---|---|
| **TONAL_SPOT**（Android 12/13 默认） | **36.0** | **16.0** | **24.0**（hue+60） | **6.0** | **8.0** |
| FIDELITY（保真，贴原色） | 种子的 C | `max(C−32, C×0.5)` | 补色（无固定 C） | `C/8` | `C/8 + 4` |
| CONTENT（内容优先） | 种子的 C | `max(C−32, C×0.5)` | 类比色（无固定 C） | `C/8` | `C/8 + 4` |
| VIBRANT（高饱和） | **200.0** | 24.0（旋转色相） | 32.0（旋转色相） | 10 | 12 |
| EXPRESSIVE（表现力） | **40**（hue+240） | 24.0 | 32.0 | 8（hue+15） | 12（hue+15） |
| NEUTRAL（近无彩） | **12.0** | 8.0 | 16.0 | **2.0** | **2.0** |
| MONOCHROME（单色） | **0.0** | 0.0 | 0.0 | 0.0 | 0.0 |
| RAINBOW | 48.0 | 16.0 | 24.0 | 0.0 | 0.0 |
| FRUIT_SALAD | 48.0（hue−50） | 36.0（hue−50） | 36.0 | 10.0 | 16.0 |

**2025 spec 改了五个变体**（其余 fall through 到 2021，且新增 `platform: phone | watch` 维度）：

| 变体 | phone primary C | phone neutral C | 备注 |
|---|---|---|---|
| TONAL_SPOT | **26（dark）/ 32（light）** | **5** | 比 2021 的 36 更收敛；neutralVariant = neutral × **1.7** |
| VIBRANT | **74**（2021 是 200，降幅极大） | **28** | neutralVariant = neutral × **1.29** |
| EXPRESSIVE | **36（dark）/ 48（light）** | 黄相环境 6 / 其余 14（dark），light 18 | — |
| NEUTRAL | 蓝相 12 / 非蓝 8 | **1.4** | neutralVariant = neutral × **2.2** |
| CONTENT | 种子 C | `clamp(6, 20, C×0.333)`（watch） | phone 沿用 2021 |

**怎么选**：白标产品用 **TONAL_SPOT**（2021 常量 36/16/24/6/8）——观感统一、饱和度克制，且几乎所有 M3 工具链默认它。客户明确要求"要跟我们 logo 一模一样的颜色"时用 **FIDELITY**，但要知道它的代价：**色阶的饱和度会跟着种子走**，一个很艳的品牌色会生成很艳的整套灰。

**为什么不能只调 HSL 的 L**：HSL 的 L 不是感知明度。同一个 L=50%，黄的观感比蓝亮得多。用 HSL 生成 10 档，结果是"黄色三档和蓝色三档看起来不是同一档"。**HCT 的 tone 是感知等距的**，这是它存在的理由。

### 4.2 路线 B · Fluent BrandRamp 16 档（需要"最细颗粒"时）

Fluent UI 把品牌色阶写成了**强制 16 档**的类型：

```ts
export type Brands = 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90
                  | 100 | 110 | 120 | 130 | 140 | 150 | 160;
export type BrandVariants = Record<Brands, string>;
```

**16 档、步长固定 10、从 10 到 160**。另外它还有：

- `ColorVariants` = **13 档**：`shade50 / shade40 / shade30 / shade20 / shade10 / primary / tint10 / tint20 / … / tint60`（6 深 + 1 原 + 6 浅）
- `Greys` = **50 档**：偶数 2–98 共 49 个 + `99`
- `AlphaColors` = **10 档**：5/10/20/30/40/50/60/70/80/90

**什么时候用**：需要极细的 hover/pressed 差异（大屏、精细交互），或需要"品牌色在任意档位都能取出一个"。代价是**16 档必须全部填满**，缺一档类型就不成立——这反而是它的优点：**用类型系统强制生成器输出完整色阶**，人不可能漏。

### 4.3 路线 C · Radix 12 步语义步进（最省心，Web 首选）

Radix 把 12 个档位**按用途定死**，不是按明度：

| 档位 | 用途 | 档位 | 用途 |
|---|---|---|---|
| 1 | App 背景 | 7 | 交互元素边框 / 焦点环 |
| 2 | 微弱背景 | 8 | 悬停态边框（**也是焦点环可用档**） |
| 3 | 组件背景（常态） | 9 | **实心底色**（全色阶最高色度，最"纯"） |
| 4 | 组件背景（hover） | 10 | 实心底色 hover |
| 5 | 组件背景（active/selected） | 11 | **低对比文本** |
| 6 | 微弱边框 / 分隔线 | 12 | **高对比文本** |

**两条硬保证（这是它最值钱的地方）**：
- **第 11 与 12 档在同色阶第 2 档背景上，保证 Lc 60 与 Lc 90**（APCA 对比度）。
- **第 9 档色度最高**，所以适合做 logo / 图形 / 实心按钮；**第 9 档多数色系配白字**，但 `Sky / Mint / Lime / Yellow / Amber` 五个色系是**配深色字**的——这正好对上 §5 的亮度边界。

**12 步的意义**：它把"我该用第几档"这个每次都要想的问题，变成了查表。多品牌场景下这是巨大优势——**N 个品牌共用同一张用途表**，不会因为品牌色不同而改变档位语义。

### 4.4 路线 D · 中文体系（HCT + 插值拟合 + 品牌倾向中性色）

TDesign 的做法值得单独记，因为它解决了"品牌氛围"这个中文 B 端常见诉求：

- **主题色取第 7 档**：腾讯蓝 `#0052D9` 落在 `blue-7`，**对比度 6.54:1**（不是取第 6 档）。
- **每个功能色 10 档**，色阶用 **HCT 色彩空间 + 按色相插值拟合曲线**生成，目标是"变化均匀、多色之间亮度均等"。
- **中性色 14 档**，按 **CIELab 的 L 值**切：White + `L96 / L94 / L92 / L88 / L80 / L68 / L58 / L50 / L40 / L32 / L24 / L18 / L14 / L8`。用 CIELab L 而不是随意取灰，是因为**暗色模式要靠中性色分层**（呼应 `dark-mode.md`）。
- **带品牌倾向的中性色 = RGB 线性混色 12%**：`Average(r,g,b) = 0.12 × 品牌色 + 0.88 × 灰`。文档给出的确定区间是 **8%–12%**。这条规则极实用——它让"品牌氛围"变成一个可调参数而不是"凭感觉加点蓝"。
- 常用文字对比度**全部 > 4.5**（WCAG 2.0）。

**中文项目默认建议**：路线 C（Radix 用途表）做结构 + 路线 D 的"12% 品牌倾向中性色"做氛围。前者给档位语义，后者给中文客户想要的"整体偏品牌色"。

### 4.5 路线选择决策表

| 你的情况 | 选 | 理由 |
|---|---|---|
| 白标 SaaS，客户随便给色 | **A（TONAL_SPOT 2021）** | 观感统一，工具链成熟 |
| 客户坚持"必须一模一样" | **A（FIDELITY）** | 保真，但要接受整套饱和度跟着走 |
| Web 产品，要最快落地 | **C（Radix 12 步）** | 用途定死，档位不用想 |
| 需要极细 hover 层次 / 大屏 | **B（Fluent 16 档）** | 颗粒最细，且类型强制完整 |
| 中文 B 端，要"品牌氛围" | **C + D 的 12% 混色** | 结构清晰 + 氛围可控 |
| 只需要明暗两套，不换品牌 | **不用本文件** → `dark-mode.md` | 别过度设计 |

---

## 五、品牌色护栏：把"客户给什么用什么"变成"算过才用"

**这是多品牌系统最容易出事、也最少被写进规范的一节。** 客户给你一个品牌色，你直接拿去做主按钮底 + 白字——**10 个里 7 个不达 AA**。这不是审美问题，是可计算的合规问题。

### 5.1 亮度边界：一条公式定生死

WCAG 相对亮度 `L`，白字对比度 = `1.05 / (L + 0.05)`，黑字对比度 = `(L + 0.05) / 0.05`。反解出两条**绝对边界**：

| 条件 | 推导 | 结论 |
|---|---|---|
| 白字达 AA 4.5:1 | `1.05/(L+0.05) ≥ 4.5` | **L ≤ 0.1833** |
| 黑字达 AA 4.5:1 | `(L+0.05)/0.05 ≥ 4.5` | **L ≥ 0.1750** |
| 白字达 3:1（大字/图形） | `1.05/(L+0.05) ≥ 3` | **L ≤ 0.3000** |
| 黑字达 3:1 | `(L+0.05)/0.05 ≥ 3` | **L ≥ 0.1000** |

**这张表就是品牌色护栏的全部数学。** 记住三个数：**0.1833 / 0.1750 / 0.3000**。

- `L ≤ 0.1750`：只能用白字（深色品牌）
- `L ≥ 0.1833`：只能用黑字（浅色品牌）
- `0.1750 < L < 0.1833`：极窄重叠区，两向都能过 AA（经典 `#767676` 就在这，L=0.180，白字 4.54 / 黑字 4.62）

### 5.2 九个真实品牌色的实测（本技能自算）

| 品牌色 | 色值 | L | 白字对比 | 判定 | 黑字对比 | 该配什么字 |
|---|---|---|---|---|---|---|
| 腾讯蓝（TDesign） | `#0052D9` | 0.1104 | **6.54** | ✅ AA | 3.03 | 白字 |
| Ant 蓝 | `#1677FF` | 0.2058 | **4.10** | ❌ **不达 AA** | 4.82 | **黑字** |
| 成功绿 | `#00B96B` | 0.3576 | 2.58 | ❌ | 7.69 | 黑字 |
| 警示橙 | `#FA8C16` | 0.3914 | 2.38 | ❌ | 8.32 | 黑字 |
| 危险红 | `#FF4D4F` | 0.2713 | 3.27 | ❌ | 6.06 | 黑字 |
| 品牌黄 | `#FADB14` | 0.7104 | **1.38** | ❌ 差得远 | 14.34 | 黑字 |
| 紫 | `#722ED1` | 0.0826 | 6.94 | ✅ AAA | 2.55 | 白字 |
| 青 | `#13C2C2` | 0.4262 | 2.21 | ❌ | 8.98 | 黑字 |
| 粉 | `#EB2F96` | 0.2179 | 3.90 | ❌ | 5.79 | 黑字 |

**三个必须传达的结论**：

1. **Ant 自己的品牌色 `#1677FF` 配白字只有 4.10:1，不达 AA**。这不是黑 Ant——它说明"业界最成熟的系统也在这一点上妥协"。你的系统没有理由继续抄。
2. **浅色系品牌色（黄/青/绿/橙）根本不该走"实心按钮 + 白字"**。品牌黄要压暗 **45.9%** 才能承载白字，压完已经不是品牌色了。正确做法是**改形态**：实心底 + 深色字，或描边按钮 + 品牌色文字，或浅色底 + 品牌色深字。这正是 Radix 对 `Sky/Mint/Lime/Yellow/Amber` 的处理。
3. **"品牌色 = 主按钮底色"是伪需求**。品牌识别靠的是**出现频率与一致性**，不是"最大面积最饱和"。改成"品牌色出现在链接、选中态、图标、边框、进度条，主按钮用品牌色的第 9 档并配深色字"，识别度不掉，合规过。

### 5.3 三档修正策略（护栏不达标时怎么改）

| 策略 | 做法 | 代价 | 什么时候用 |
|---|---|---|---|
| **① 换档位**（首选） | 用色阶的第 8/9/10 档替代原始品牌色 | 几乎无损，观感仍属同色系 | 默认策略。**80% 的情况够用** |
| **② 调明度** | 朝黑/白混色直到过阈值（本技能实测：Ant 蓝压 **5.3%** 即达 4.50；危险红压 **16.3%**；警示橙压 **29.0%**） | 色相不变、饱和度略降 | 客户坚持"就要这个色"时 |
| **③ 换前景色** | 不改底色，改文字色（白 → 深灰/黑） | 需同时改按钮的字色 token | 浅色品牌（L > 0.1833）**唯一正确解** |
| ④ 降面积 | 品牌色不用于大面积实心，改描边/文字/图标 | 需重做视觉稿 | 品牌色极浅（黄 L=0.71）时 |
| ⑤ 拒绝 | 客户品牌色与语义色冲突（品牌绿 + 成功绿） | 商务成本 | 只在冲突到无法区分时 |

**护栏的正确位置**：**在生成色阶之后、写入 token 之前**，作为生成管线的一道自动校验。人不可能每次手算，所以它必须是代码。

### 5.4 护栏还要管三件事（不只是按钮）

| 用途 | 阈值 | 判据 | 失败后果 |
|---|---|---|---|
| 品牌色上的文字 | 4.5:1（正文）/ 3:1（≥24px 或 ≥18.5px bold） | §5.1 亮度边界 | 按钮文字看不清 |
| 品牌色**作为文字**放在白/浅底上 | 4.5:1 | 同上（反向） | 链接、错误提示看不清 |
| 品牌色**作为边框/图标/焦点环** | 3:1 | `L ≤ 0.30`（白底） | WCAG 1.4.11 不过 |
| 品牌色作为**图表分类色** | 相邻色 ΔE 可辨 + 不靠颜色单编码 | 见 `dataviz.md` §3 | 色盲读不出 |

**注意最后一条的陷阱**：品牌色**不应该**直接当图表第一分类色。品牌色是"一个色"，图表需要"一组可辨色"。把品牌色塞进分类色板，会导致"第一类特别突出、其余类失衡"，且品牌色一换图表全变。**图表分类色板应独立维护，品牌色最多取一个衍生档做强调。**

---

## 六、主题矩阵的落地：选择器与层叠策略

### 6.1 不要写 2^N 个选择器块

错误写法（组合爆炸）：

```css
[data-brand="a"][data-mode="light"] { --color-brand: #0052D9; }
[data-brand="a"][data-mode="dark"]  { --color-brand: #4B8BFF; }
[data-brand="b"][data-mode="light"] { --color-brand: #E1251B; }
[data-brand="b"][data-mode="dark"]  { --color-brand: #FF6B5E; }
/* … 品牌数 × 模式数，还要乘对比度与密度 */
```

正确写法（**轴独立，层叠叠加**）：

```css
/* 每根轴只写自己的那一段，互不知道对方存在 */
[data-brand="a"] { --blue-7: #0052D9; /* L1 全量 */ }
[data-brand="b"] { --blue-7: #E1251B; /* L1 全量 */ }

[data-mode="light"] { --color-bg: var(--gray-1); --color-text: var(--gray-13); }
[data-mode="dark"]  { --color-bg: var(--gray-14); --color-text: var(--gray-2); }

[data-contrast="high"] { --color-text: var(--gray-14); --color-border: var(--gray-11); }
```

**原理**：CSS 自定义属性是**就近覆盖**的，不同选择器改**不同变量**时天然叠加，不需要穷举组合。**只有当两根轴要改同一个变量时才需要交叉**——而 §2 的原则要求你不许制造这种交叉。

### 6.2 用 `@layer` 锁死优先级（关键）

主题系统"覆盖不掉"的头号原因是：**未分层的样式永远赢过分层样式**，而第三方库（组件库 reset）通常是不分层的。

```css
/* 第一行：只声明顺序，不写规则。先声明者优先级最低 */
@layer tokens.base, tokens.brand, tokens.mode, tokens.contrast,
       components, utilities, overrides;

@layer tokens.base    { :root { --blue-7: #1677FF; --gray-1: #FFF; } }
@layer tokens.brand   { [data-brand="b"] { --blue-7: #E1251B; } }
@layer tokens.mode    { [data-mode="dark"] { --color-bg: var(--gray-14); } }
@layer tokens.contrast{ [data-contrast="high"] { --color-border: var(--gray-11); } }
@layer overrides      { /* 客户最后一公里的临时补丁，永远赢 */ }
```

**`@layer` 的三条硬规则**（MDN）：
1. **先声明的层优先级最低，后声明的最高**；层顺序一旦确定，**特异性与出现顺序都被忽略**——所以层内可以用最简单的选择器。
2. **未分层的样式永远赢过任何命名层与匿名层**（`!important` 反向：层内的 `!important` 赢过层外）。
3. 嵌套层用点号追加：`@layer framework.layout`。

**推论**：把主题层放在 `components` **之前**，组件层就能用 `var(--color-brand)` 且不需要 `!important`；把 `overrides` 放最后，客户的临时补丁才能生效。

### 6.3 作用域三选

| 作用域 | 写法 | 适用 | 风险 |
|---|---|---|---|
| 全局 | `:root` | 单品牌整站 | 无法多品牌同页 |
| 属性作用域 | `[data-brand="x"]` | **多品牌推荐** | `position: fixed` 弹层会逃出 |
| 类作用域 | `.theme-brand-x` | 组件级预览 | 类名污染、易漏 |
| 容器样式查询 | `@container style(--density: compact)` | 组件自适应所在容器 | 兼容性较新，**不要用于主题主路径** |

**逃逸陷阱（必记）**：`position: fixed` 的弹层 / `dialog` / `popover` 如果 portal 到 `body`，会**离开 `[data-brand]` 作用域**，于是弹层用的是 `:root` 的默认品牌。**解法：portal 目标必须是同作用域的容器，而不是 `body`。** 这个 bug 在多品牌系统里几乎必然出现一次，且极难定位（"只有弹窗颜色不对"）。

---

## 七、运行时切换 vs 构建期编译

这是多品牌架构的**第一个分叉决策**，选错后面全错。

| 维度 | 运行时（CSS 变量） | 构建期（Sass/Less `modifyVars`） |
|---|---|---|
| 一套 CSS 服务 N 品牌 | ✅ 是 | ❌ 否，N 份产物 |
| 切换是否重载 | ✅ 零重载 | ❌ 需重新构建/加载 |
| 首屏 CSS 体积 | 较大（含全部 L1） | 较小（只含该品牌） |
| 客户自助改色 | ✅ 可行 | ❌ 需重新发版 |
| 变量数量上限 | 有实际压力（见 §16） | 无 |
| 典型实现 | `[data-brand]` + `var()` | Arco 的 `modifyVars: { 'arcoblue-6': '#f85959' }` |

**判据表**：

| 条件 | 选 |
|---|---|
| 品牌数 ≥ 3，或客户可自助配置 | **运行时** |
| 品牌数 = 1，只是私有化交付 | **构建期**（更简单、首屏更小） |
| 品牌数 = 2–3 且固定，首屏预算极紧 | **构建期 + 独立入口** |
| 品牌数多 + 首屏极紧 | **混合**：品牌层运行时（只注入 L1 的 20–30 个关键变量），密度层构建期 |

**Ant Design 的两档正好是这个取舍的显式化**：`cssVar` 开启后走 CSS 变量（可运行时切、可嵌套作用域）；`zeroRuntime`（6.0.0+）则关闭运行时样式生成，改为预编译 CSS——**用构建期换首屏**。

**Arco 的代价要记**：它基于 Less `modifyVars` + CSS Custom Properties，**官方明确不兼容 IE**。选它就意味着放弃 IE（2026 年这通常可接受，但要写进交付说明）。

---

## 八、多品牌同页共存（最容易被忽略的场景）

以下四种场景**必须**支持同页多品牌，而多数主题系统做不到：

1. 设计系统官网的"品牌切换预览"
2. 嵌入式 SDK / 白标组件被嵌进客户的页面
3. 微前端：主应用品牌 A，子应用品牌 B
4. 白标后台里嵌第三方（如支付、客服）组件

**四条实现纪律**：

1. **变量必须作用域化**，`:root` 只放"默认品牌 + 跨品牌共享的 L2/L3"。
2. **不要用全局单例 theme context**。React 用嵌套 Provider（Ant 的 `ConfigProvider` 支持嵌套，**子主题未修改的 token 继承父主题**，`inherit` 默认 `true`）。
3. **Ant 多品牌同页要开 `cssVar` 并给不同 `key`**，否则多个 `ConfigProvider` 会共用同一套变量名互相覆盖。
4. **`position: fixed` 弹层 portal 到同作用域容器**（见 §6.3）。

**已知坑（Ant 官方文档明写）**：`ConfigProvider` 对 `message.xxx` / `Modal.xxx` / `notification.xxx` **静态方法不生效**——因为这些方法通过 `ReactDOM.render` 动态创建实体，拿不到 context。解法是用 `Modal.useModal()` 的 `contextHolder`，或改用 `App` 组件包裹。**在多品牌场景下这个坑会表现为"弹窗永远用默认品牌色"。**

---

## 九、四套真实主题矩阵对照（可直接抄结构）

| 体系 | 主题数 | 轴怎么分 | 分档方式 | 可抄的点 |
|---|---|---|---|---|
| **GitHub Primer** | **9** | 2 模式 × 5 变体（含 2 色盲 + 2 高对比 + dimmed） | 中性色阶 **0–13**（14 档） | **亮暗色阶方向反向**（亮从白起、暗从黑起）→ 同一 functional token 无需覆写；3 个 data 属性 |
| **IBM Carbon** | **4** | white / g10 / g90 / g100（两组亮两组暗） | token 名不变、值变 | 明确区分 **Theme / Token / Role / Value** 四个词；`$text-secondary` 白主题 Gray70、g100 主题 Gray30 |
| **Microsoft Fluent 2** | 1 套 × N 品牌 | 品牌 ramp 独立于主题 | BrandRamp **16 档**（10–160）；Theme 含 **16 类 token** | **用类型强制色阶完整**（`Record<Brands, string>` 缺档即报错） |
| **Ant Design** | 3 算法可组合 | Seed → Map → Alias 三级 | 品牌色 → 自动派生 10 个 map token | **只改 1 个 seed 就得到整套**；算法可数组组合（`[darkAlgorithm, compactAlgorithm]`） |
| **TDesign（中文）** | 明/暗 + 品牌 | 全局语义 token → 组件 token 两级 | 功能色 **10 档**、中性 **14 档** | 品牌倾向中性色 **12% 混色**；主题色取**第 7 档** |
| **Arco（中文）** | 明/暗 + 品牌 | 粒子变量（Less） | `arcoblue-6` 单点替换 | 单变量即可换肤；**不兼容 IE** |

**Primer 的"反向色阶"值得单独说**：它的中性色阶在亮色下从白开始、暗色下从黑开始，**方向相反**。这样 `bgColor-default` 这类 functional token 在两个模式下**指向同一个档位号**，不需要为暗色重写一遍映射。代价是：**你必须接受"档位号不表示明度，只表示层级"**。这是多主题架构里最优雅的一个技巧，也是最反直觉的一个。

**Carbon 的四主题对照（直接抄）**：

| Token | Role | White 主题 | Gray 100 主题 |
|---|---|---|---|
| `$text-secondary` | 标签色 | Gray 70 | **Gray 30** |
| `$text-primary` | 主文本 | Gray 100 | **Gray 10** |
| `$border-strong` | 底边框 | Gray 50 | **Gray 60** |
| `$icon-primary` | 主图标 | Gray 100 | **Gray 10** |
| `$field-01` | 输入框底 | Gray 10 | **Gray 90** |
| `$background` | 页面底 | White | **Gray 100** |

**注意 `$border-strong` 是 50 → 60（变亮而非变暗）**——这和 `dark-mode.md` 里"outline 50→60 变亮"是同一个规律：**边框在暗色下要提亮，不是加深**。

---

## 十、语义层分叉的边界：什么时候允许"每个品牌一套 L2"

**默认禁止。** 允许的例外只有三种，且每种都要写书面理由：

| 例外 | 判据 | 代价 | 替代方案 |
|---|---|---|---|
| **品牌色与语义色撞车** | 客户品牌是绿，而成功态也是绿 → 无法区分 | 该品牌的状态色需另选色相 | 优先改**状态色**（语义色的色相本就可协商），而非改 L2 结构 |
| **合规要求独立色板** | 金融/医疗客户要求"错误色必须是 XX 标准色" | 一套额外色板 | 只分叉 `support-error-*` 一族，不是整个 L2 |
| **品牌需要完全不同密度** | 品牌 A 是消费级、品牌 B 是专业工具 | 两套 dimension token | 用**密度轴**（D）解决，不要放进品牌轴 |

**分叉的代价可以量化**：`组件数 × 状态数`。20 个组件 × 9 态 = 180 个映射点。分叉 3 个品牌 = 540 个点要同步。**这就是为什么"L2 共享"不是洁癖，是算术。**

**如果非分叉不可，正确姿势是"条件映射"而不是"复制结构"**：

```css
/* 结构只有一份；不同品牌让同一语义指向不同档位 */
:root { --color-brand-solid: var(--blue-9); --color-on-brand: #FFFFFF; }

[data-brand="yellow-brand"] {
  /* 不改结构，只改指针 + 前景字色 */
  --color-brand-solid: var(--yellow-9);
  --color-on-brand: var(--gray-14);   /* 浅色品牌必须换深色字 */
}
```

这样组件里永远只写 `var(--color-brand-solid)` / `var(--color-on-brand)`，**组件代码零分叉**。

---

## 十一、配置文件结构：DTCG 多品牌写法

### 11.1 目录结构（core 与 brand 分离）

```
tokens/
  core/                 # 跨品牌共享：L2 语义 + L3 组件 + dimension
    semantic.tokens.json
    component.tokens.json
    dimension.tokens.json
  brands/
    brand-a/            # 只放 L0 + L1
      seed.tokens.json
      palette.tokens.json
    brand-b/
      seed.tokens.json
      palette.tokens.json
  themes/
    light.tokens.json   # 只改 L2 的指针
    dark.tokens.json
    high-contrast.tokens.json
```

**铁律**：`core/` 里**不许出现任何品牌色值**。`brands/*/` 里**不许出现任何语义名**（`--color-text` 这种词只属于 core）。

### 11.2 DTCG 的 `$extends` 做品牌继承

DTCG（2025.10 草案）的组级 `$extends` 是**深合并**语义：复制被继承组 → 本地同路径**完整替换**（不是逐属性合并）→ 新增路径并入 → **禁止循环引用**。

```json
{
  "brand": {
    "$extends": "{core.semantic}",
    "color": {
      "brand": { "$value": "{palette.blue.7}", "$type": "color" }
    }
  }
}
```

**注意 DTCG 的几条硬约束（踩过就知道）**：
- 含 `$value` 才是 token，不含才是组；**两者同时出现是无效结构，必须报错**。
- token 名与组名**不得以 `$` 开头**，**不得含 `{ } .`**（点号是路径分隔符）。
- 别名两种语法都要支持：`{group.token}`（只能指向完整 token）与 `$ref`（RFC 6901 JSON Pointer，可指向任意位置与属性级子值）。
- `$type` 解析优先级：自身 → 被引用 token → 最近父组 → 无则**无效，工具不得猜**。
- 组可用保留名 `$root` 提供基础值；`{color.accent.$root}` 有效，`{color.accent}` 指向组本身 → **无效**。
- **这是 preview draft，官方明写"不要实现此版本，不要作为权威引用"**——用于内部管线可以，写进对外规范要注明。

### 11.3 Style Dictionary 多品牌构建（已验证的配置模式）

SD 的多品牌不靠"主题插件"，靠两条机制的**组合**：

1. **`include` 放共享基座，`source` 放品牌覆盖**。加载顺序是 `include`（按数组序）→ `source`（按数组序），**后者覆盖前者**。
2. **关键规则**：`source` 覆盖 `include` **不告警**（因为这是设计意图）；但 `source` **内部**两个文件冲突**会告警**。所以品牌覆盖必须全放 `source`，共享基座全放 `include`——这样"意外的覆盖"才会被报出来。

```js
import StyleDictionary from 'style-dictionary';

const brands = ['brand-a', 'brand-b', 'brand-c'];

for (const brand of brands) {
  const sd = new StyleDictionary({
    include: ['tokens/core/**/*.json'],          // 基座：语义 + 组件 + 尺寸
    source:  [`tokens/brands/${brand}/**/*.json`], // 覆盖：只有 L0 + L1
    platforms: {
      css: {
        transformGroup: 'css',
        buildPath: `build/${brand}/css/`,        // 每品牌独立输出目录
        files: [{ destination: 'tokens.css', format: 'css/variables',
                  options: { outputReferences: true } }],
      },
    },
  });
  await sd.buildAllPlatforms();
}
```

**四条纪律**：
1. **每个品牌独立 `buildPath`**，不要试图把多品牌塞进一个文件（后面必然要拆）。
2. **DTCG 与原格式不能在同一实例混用**（SD v4 明写）。
3. `options.outputReferences: true` 让输出保留 `var(--blue-7)` 引用链——**这是运行时换肤的前提**，关掉就变成硬编码值。
4. token 元数据里 `isSource: true/false` 可用来判断"这个值来自品牌覆盖还是基座"，做审计时有用。

---

## 十二、Figma 侧：变量模式必须与代码轴一一对应

| 规则 | 做法 | 为什么 |
|---|---|---|
| **一个 collection = 一根轴** | `Brand` collection、`Mode` collection、`Density` collection | 一个 collection 装所有轴 → 模式数爆炸且无法组合 |
| **模式数有硬上限** | **Professional / Organization：每 collection 4 个模式；Enterprise：40 个** | 超过就要拆 collection 或升级计划 |
| **变量名 = 代码 token 名** | Figma `color/brand/solid` ↔ CSS `--color-brand-solid` | 名字不一致 → 交付断链，每次靠人对 |
| **只让设计师碰 L2/L3** | L1 色阶由生成器写入，标为只读 | 设计师改 L1 会破坏护栏 |
| **品牌切换用模式，不用多文件** | 一个文件切模式看 5 个品牌 | 多文件必然漂移 |

**4 个模式的现实约束**：如果你有 3 个品牌 × 2 个模式 = 6 个组合，**装不进一个 collection**。正确解法是拆成 `Brand`（3 模式）+ `Mode`（2 模式）两个 collection——组合由 Figma 自动做笛卡尔积，**不需要 6 个模式**。这条能省掉大量"要不要升级 Enterprise"的纠结。

---

## 十三、品牌注入管线：从客户填表到 CSS 生效

```
① 客户输入        ② 校验                ③ 生成           ④ 编译        ⑤ 分发        ⑥ 注入
品牌色/字体/      对比度护栏(§5)          L1 全量色阶       变量文件       CDN +        首屏内联
圆角/logo         色域/字体授权/白名单     (路线 A/C)       hash 命名     immutable    + 运行时切换
```

**六步各自的关键决策**：

| 步 | 关键点 | 失败模式 |
|---|---|---|
| ① 输入 | 只收 **1 个色值 + 1 个字体族 + 1 个圆角基数**。不收"整套色板" | 收整套 → 客户给 40 个不协调的色 |
| ② 校验 | 护栏必须**自动修正并告知**，不是拒绝 | 直接拒绝 → 客户觉得产品不专业 |
| ③ 生成 | 色阶档数**固定**（10 或 12 或 16），不随品牌变 | 档数变 → L2 映射断裂 |
| ④ 编译 | 输出 `brand-{hash}.css`，**hash 由品牌配置算出** | 用客户 ID 命名 → 改了配置但缓存不失效 |
| ⑤ 分发 | `Cache-Control: public, max-age=31536000, immutable` | 不设长缓存 → 每次请求回源 |
| ⑥ 注入 | **首屏变量内联在 `<head>`**，其余走外链 | 全靠外链 → FOUC 闪一下默认品牌色 |

**安全（必做，最常被漏）**：客户输入是**不可信输入**。

| 攻击面 | 防护 |
|---|---|
| CSS 注入（`}` 逃逸、`url()` 外链） | 色值只接受 `#RRGGBB` / `rgb()` 正则；**严禁字符串拼接进 `<style>`** |
| 字体 URL 指向恶意资源 | 字体只允许**预置白名单**，不接受任意 URL |
| 圆角/尺寸注入超范围值 | 数值 `clamp()` 到允许区间 |
| 客户上传 logo 的 SVG | **必须 sanitize**（`<script>`、`on*`、`<foreignObject>`） |

---

## 十四、防闪烁：多品牌特有的 FOUC

`dark-mode.md` §9 讲的是"模式闪白"。多品牌多一个更严重的问题：**品牌未知时先渲染了默认品牌，然后跳到客户品牌**——用户会以为进错了网站。

**三件套（顺序不能变）**：

1. **`data-brand` 必须在 HTML 首字节就带上**，由服务端渲染写入，**不能等 JS**。
   ```html
   <html lang="zh-CN" data-brand="acme" data-mode="light">
   ```
2. **首屏关键变量内联在 `<head>`**（只放 L1 的 20–30 个关键档位 + L2 的 10 来个语义），其余外链。
3. **CSS 必须在变量之后**，且变量块放在 `@layer tokens.brand` 里（否则被组件层覆盖）。

**"品牌未知"的决策**：如果服务端拿不到品牌（如 CDN 静态页 + 客户端识别租户），**先渲染中性骨架（无品牌色），品牌到达后一次性套用**。不要"先默认品牌再换"——那是两次视觉跳变，比一次延迟更糟。

**字体是第二个闪烁源**：品牌字体按需加载必然有 swap。三档处理：
- 品牌字体是**装饰性**（标题）→ `font-display: swap` + 尺寸接近的回退字体 + `size-adjust` 校正（见 `performance-design.md` §8）
- 品牌字体是**功能性**（正文）→ **不要用品牌字体做正文**，用系统字体栈，品牌字体只上标题
- 品牌字体**未授权**（客户只给了 logo 没给字体授权）→ 回退到系统栈，**并在交付说明里写明**

---

## 十五、性能成本：变量数量与切换代价

| 成本项 | 量级 | 控制手段 |
|---|---|---|
| L1 色阶变量 | 12 色相 × 10 档 = **120 个**（或 4 色相 × 10 = 40） | **只生成用到的色相**，不要 12 色全量 |
| L2 语义变量 | 40–80 个 | 合并同值；不要给每个组件建语义 |
| L3 组件变量 | 组件数 × 2–5 | **L3 越少越好**，多数组件不该有 L3 |
| 单品牌 CSS 变量总条数 | 建议 **≤ 300 条** | 超过说明 L3 泛滥 |
| 5 品牌 × 全量 | 变量定义体积 × 5 | 品牌层只注入 L1（约 40–120 条），L2/L3 共用 |

**切换主题的代价**：
- **只改变量值 → 不重排（no reflow），但会重绘（repaint）**。`color` / `background-color` / `border-color` 都在绘制阶段。
- **切换时不要同时改布局**。如果密度轴与模式轴一起变，会触发重排 + CLS。**密度切换应当是独立的用户动作**，不要与明暗切换绑在一个按钮上。
- **避免在切换瞬间触发 `transition`**：给 `*` 加 `transition: background-color .3s` 会让整页 300ms 内持续重绘。正确做法是切换时给 `html` 加一个 `no-transition` 类，下一帧移除。

**缓存策略**：
- 品牌 CSS：`brand-{hash}.css` + `immutable`（hash 变了 URL 就变）
- 不要在运行时用 JS 逐个 `setProperty` 设置几十个变量（会触发多次样式重算）——**改一个 `data-brand` 属性，让 CSS 一次性完成**。

---

## 十六、治理：品牌准入与变更管理

| 治理项 | 规则 |
|---|---|
| **品牌注册表** | 每个品牌一条记录：`brandId / 显示名 / 种子色 / 字体 / 圆角基数 / 色阶算法版本 / 护栏修正记录 / 负责人 / 生效时间` |
| **准入白名单** | 新品牌必须过 §5 护栏 + 生成色阶 + 视觉走查，才进 `brands/` 目录 |
| **禁止项** | 客户不得直接改 L2/L3；不得上传任意 CSS；不得指定"第 3 档用什么色" |
| **SemVer** | **改语义映射（L2 指向变了）= MAJOR**（所有品牌视觉全变）；新增品牌 = MINOR；修某品牌色阶错误 = PATCH（但要写影响面） |
| **审计** | 每次品牌配置变更留 diff：谁、何时、改了哪个 token、护栏是否重新校验 |
| **下线** | 品牌下线前至少保留一个 MINOR 周期，且要能回答"存量页面怎么办" |

**"改默认值 = MAJOR"在多品牌下更严重**：单品牌改默认色影响一个产品，多品牌改 L2 映射影响**所有品牌的所有页面**。所以 L2 的任何改动都要按 MAJOR 走迁移流程（见 `handoff-collaboration.md` §12）。

---

## 十七、12 个场景速查

| 用户说 | 先做什么 | 关键数值 / 位置 |
|---|---|---|
| "客户要换成他们的品牌色" | 走 §5 护栏 → §4 生成色阶 | 亮度边界 **0.1833 / 0.1750** |
| "我们有 5 个客户，各要自己的主题" | §3 四层 + §7 运行时 | L2/L3 共享，只有 L0/L1 分品牌 |
| "客户品牌色很浅（黄/青），按钮白字看不清" | §5.3 策略 ③ 换前景色 | L > 0.1833 必须黑字；黄 L=0.71 |
| "一个页面要同时显示两个品牌" | §8 作用域化 + portal | 弹层必须 portal 到同作用域 |
| "加了暗色后主题组合爆炸" | §2 轴独立 + §6.1 不要穷举 | 每轴只改自己的变量 |
| "客户自定义的颜色覆盖不掉组件库" | §6.2 `@layer` | 未分层样式永远赢 |
| "换肤时页面闪一下默认色" | §14 三件套 | `data-brand` 服务端写入首屏 |
| "要不要给每个品牌写一套语义 token" | §10 默认禁止 | 代价 = 组件数 × 状态数 |
| "色阶生成用 HSL 调明度行不行" | §4.1 不行，用 HCT | HSL 的 L 不是感知明度 |
| "品牌色能直接当图表第一色吗" | §5.4 不行 | 图表色板独立维护 |
| "设计稿变量和代码 token 对不上" | §12 一 collection 一轴 | 模式上限 4 / 40 |
| "客户上传 logo 有风险吗" | §13 安全 | SVG 必须 sanitize |

---

## 十八、20 条反模式

1. **每个品牌 fork 一份代码** —— 半年后无法合并，任何 bug 要修 N 次。
2. **把品牌色硬编码进组件** —— 换品牌要全局搜索替换。
3. **给每个品牌各写一套 L2 语义** —— 组件行为分叉，新组件必然漏。
4. **品牌色阶档数不一致**（A 品牌 10 档、B 品牌 8 档）—— L2 映射断裂。
5. **用 HSL 调 L 生成色阶** —— 各色相观感不等距，黄色三档和蓝色三档不同高。
6. **品牌色直接做按钮底 + 白字，不校验** —— 10 个里 7 个不过 AA。
7. **浅色品牌色（黄/青）也配白字** —— 品牌黄只有 1.38:1，等于没有对比。
8. **为了"保住品牌色"把黄压暗 46%** —— 压完已经不是品牌色，应改形态。
9. **品牌色当图表第一分类色** —— 一类突出、其余失衡，换品牌图表全变。
10. **写 2^N 个组合选择器** —— 加一根轴就翻倍，必然漏。
11. **主题变量放 `:root` 却要做多品牌同页** —— 互相覆盖。
12. **弹层 portal 到 `body`** —— 弹窗永远是默认品牌色。
13. **用 `!important` 修主题覆盖问题** —— 说明 `@layer` 顺序错了。
14. **切换主题时同时切密度** —— 重排 + CLS。
15. **给 `*` 加全局 `transition` 做主题过渡** —— 切换时整页 300ms 持续重绘。
16. **运行时用 JS 逐个 `setProperty` 设几十个变量** —— 多次样式重算，改一个属性就够。
17. **品牌 CSS 用客户 ID 命名缓存** —— 改了配置缓存不失效。
18. **接受客户任意 CSS / 字体 URL / 未消毒 SVG** —— CSS 注入 + XSS。
19. **Figma 一个 collection 装所有轴** —— 模式数撞上限（4/40），且无法组合。
20. **把"品牌数 × 模式数"当主题数手写** —— 忘了密度与对比度两根轴，后面全返工。

---

## 十九、18 项自检（多品牌/多主题关）

1. **判过要不要做**？品牌数 >1 或模式数 >1 才上架构，否则用 `dark-mode.md`。
2. **轴分开了**？品牌/模式/对比度/密度是四根独立轴，**没有交叉特例块**（≤2 个可接受，第 3 个就是架构失败）。
3. **只有品牌轴动 L1**？其余轴只改 L2 指针或 dimension。
4. **L2/L3 跨品牌共享**？组件代码里没有任何品牌判断分支。
5. **L1 档数跨品牌一致**？10 / 12 / 16 之一，固定不变。
6. **色阶算法说得出名字与参数**？（TONAL_SPOT 36/16/24/6/8 / Radix 12 步 / Fluent 16 档 / TDesign HCT+10 档）
7. **品牌色过了亮度护栏**？`L ≤ 0.1833` 用白字，`L ≥ 0.1750` 用黑字，中间区两向都验过。
8. **不达标时用了正确策略**？换档位（首选）/ 调明度 / 换前景字色（浅色品牌唯一解）。
9. **浅色品牌改的是形态不是硬压**？黄/青/绿没有"压暗 40% 后还叫品牌色"。
10. **品牌色没当图表分类色**？图表色板独立。
11. **选择器不是 2^N 穷举**？每轴只写自己那段。
12. **`@layer` 顺序正确**？`tokens.base → brand → mode → contrast → components → overrides`，主题层在组件层**之前**。
13. **弹层 portal 到同作用域**？`position: fixed` 弹窗颜色正确。
14. **多品牌同页能共存**？变量作用域化 + 嵌套 Provider + `cssVar` 独立 key。
15. **首屏不闪**？`data-brand` 在 HTML 首字节、关键变量内联在 `<head>`、CSS 在变量之后。
16. **运行时 vs 构建期选对了**？品牌数 ≥3 或客户自助 → 运行时；单客户私有化 → 构建期。
17. **切换代价可控**？只改变量不重排；密度切换独立；切换瞬间禁用全局 transition。
18. **治理齐了**？品牌注册表、准入白名单、L2 改动按 MAJOR、变更审计、客户输入白名单校验（含 SVG sanitize）。

---

## 二十、可抄代码（6 段）

### 20.1 主题矩阵骨架（轴独立 + `@layer`）

```css
/* 1) 先声明层顺序，不写规则 —— 先声明者优先级最低 */
@layer tokens.base, tokens.brand, tokens.mode, tokens.contrast,
       components, overrides;

/* 2) L1 基座（默认品牌） */
@layer tokens.base {
  :root {
    --blue-9: #1677FF; --blue-8: #4096FF; --blue-10: #0958D9;
    --gray-1: #FFFFFF; --gray-2: #F5F5F5; --gray-13: #141414; --gray-14: #0A0A0A;
    --color-brand-solid: var(--blue-9);
    --color-on-brand: #FFFFFF;          /* 深色品牌：白字 */
    --color-bg: var(--gray-1);
    --color-text: var(--gray-13);
  }
}

/* 3) 品牌轴：只改 L1 与"前景字色"这一个指针 */
@layer tokens.brand {
  [data-brand="acme"]   { --blue-9: #0052D9; --blue-8: #366EF4; --blue-10: #003CAB; }
  [data-brand="sunny"]  {
    --blue-9: #FADB14; --blue-8: #FFE58F; --blue-10: #D4B106;
    --color-on-brand: var(--gray-13);   /* 浅色品牌：必须换深色字 */
  }
}

/* 4) 模式轴：只改 L2 指针 */
@layer tokens.mode {
  [data-mode="dark"] {
    --color-bg: var(--gray-14);
    --color-text: var(--gray-2);
  }
}

/* 5) 对比度轴：只往色阶两端跳档 */
@layer tokens.contrast {
  [data-contrast="high"] {
    --color-text: var(--gray-14);
    --color-border-strong: var(--gray-11);
  }
}

/* 6) 组件层：只引用 L2，永不写品牌判断 */
@layer components {
  .btn-primary {
    background: var(--color-brand-solid);
    color: var(--color-on-brand);
  }
}
```

### 20.2 品牌色护栏（生成色阶后、写 token 前必跑）

```js
const s2l = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
const lum = hex => {
  const h = hex.replace('#', '');
  return 0.2126 * s2l(parseInt(h.slice(0,2),16))
       + 0.7152 * s2l(parseInt(h.slice(2,4),16))
       + 0.0722 * s2l(parseInt(h.slice(4,6),16));
};
const cr = (a, b) => {
  const [hi, lo] = [lum(a), lum(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
};

// 边界（由公式反解，不要凭经验改）
const WHITE_AA_MAX = 0.1833;   // L <= 此值 → 白字可达 4.5:1
const BLACK_AA_MIN = 0.1750;   // L >= 此值 → 黑字可达 4.5:1
const WHITE_3_MAX  = 0.3000;   // L <= 此值 → 白字可达 3:1（大字/图形）

/**
 * 给定品牌色，返回合规的前景字色与告警。
 * 注意：优先"换档位"，其次"调明度"，浅色品牌必须"换前景字色"。
 */
function guardOnBrand(brandHex) {
  const L = lum(brandHex);
  if (L <= WHITE_AA_MAX) return { onColor: '#FFFFFF', ratio: cr(brandHex, '#FFFFFF'), ok: true };
  if (L >= BLACK_AA_MIN) {
    const on = '#0A0A0A';
    return { onColor: on, ratio: cr(brandHex, on), ok: cr(brandHex, on) >= 4.5 };
  }
  return { onColor: '#FFFFFF', ratio: cr(brandHex, '#FFFFFF'), ok: true, note: '重叠区，两向均需复测' };
}
```

### 20.3 品牌色阶生成骨架（HCT tone，路线 A）

```js
// 伪代码：色相继承种子、色度取变体常量、明度取 tone 列表
// 依赖 @material/material-color-utilities
import { Hct, TonalPalette } from '@material/material-color-utilities';

const seed = Hct.fromInt(0xFF0052D9);          // 客户品牌色

// TONAL_SPOT 2021 常量：primary 36 / secondary 16 / tertiary 24 / neutral 6 / nv 8
const primary   = TonalPalette.fromHueAndChroma(seed.hue, 36);
const secondary = TonalPalette.fromHueAndChroma(seed.hue, 16);
const tertiary  = TonalPalette.fromHueAndChroma(seed.hue + 60, 24);
const neutral   = TonalPalette.fromHueAndChroma(seed.hue, 6);
const nv        = TonalPalette.fromHueAndChroma(seed.hue, 8);

// 取档：亮色 surface 98/96/94/92/90，暗色 4/6/10/12/17/22（见 dark-mode.md）
const steps = [98, 96, 94, 92, 90, 80, 70, 60, 50, 40, 30, 20, 10];
const palette = Object.fromEntries(steps.map(t => [`blue-${t}`, primary.tone(t)]));
```

### 20.4 首屏防闪烁注入

```html
<!doctype html>
<html lang="zh-CN" data-brand="acme" data-mode="light">
<head>
  <meta charset="utf-8">
  <!-- 1) 关键变量内联，必须早于任何 CSS -->
  <style>
    [data-brand="acme"]  { --blue-9:#0052D9; --color-brand-solid:var(--blue-9); --color-on-brand:#fff; }
    [data-brand="sunny"] { --blue-9:#FADB14; --color-brand-solid:var(--blue-9); --color-on-brand:#141414; }
    [data-mode="dark"]   { --color-bg:#0A0A0A; --color-text:#F5F5F5; }
  </style>
  <!-- 2) 其余 token 外链 -->
  <link rel="stylesheet" href="/tokens/brand-acme.9f2c1a.css">
  <link rel="stylesheet" href="/app.css">
</head>
```

### 20.5 主题切换（禁用过渡，只改属性）

```js
// 错误：切主题时给 * 加 transition，会整页重绘 300ms
// 正确：切换瞬间禁用过渡，下一帧恢复
function switchTheme({ brand, mode }) {
  const root = document.documentElement;
  root.classList.add('no-transition');
  if (brand) root.dataset.brand = brand;
  if (mode)  root.dataset.mode  = mode;
  requestAnimationFrame(() => requestAnimationFrame(() => {
    root.classList.remove('no-transition');
  }));
}
```

```css
.no-transition, .no-transition * { transition: none !important; }
```

### 20.6 Style Dictionary 多品牌（完整可跑）

```js
// sd.config.js —— 每品牌独立实例 + 独立输出目录
import StyleDictionary from 'style-dictionary';

const brands = ['acme', 'sunny', 'nova'];

export default async function build() {
  for (const brand of brands) {
    const sd = new StyleDictionary({
      include: ['tokens/core/**/*.json'],            // L2 + L3 + dimension，跨品牌共享
      source:  [`tokens/brands/${brand}/**/*.json`], // 只含 L0 种子 + L1 色阶
      platforms: {
        css: {
          transformGroup: 'css',
          buildPath: `build/${brand}/`,
          files: [{
            destination: 'tokens.css',
            format: 'css/variables',
            options: { outputReferences: true },     // 保留 var() 引用链，否则无法运行时换肤
          }],
        },
      },
    });
    await sd.buildAllPlatforms();
    console.log(`✓ ${brand}`);
  }
}
```

---

## 附：来源

| 结论 | 来源 |
|---|---|
| 色度常量全表（2021/2025）、变体定义 | `material-color-utilities` `typescript/dynamiccolor/dynamic_scheme.ts` 源码 |
| BrandRamp 16 档、ColorVariants 13 档、Greys 50 档 | `microsoft/fluentui` `packages/tokens/src/types.ts` |
| 9 主题与 3 个 data 属性、中性阶 0–13、亮暗反向 | [Primer Primitives](https://primer.style/product/primitives/) · [Color usage](https://primer.style/product/getting-started/foundations/color-usage/) |
| 四主题、Theme/Token/Role/Value 定义、跨主题 token 对照 | [Carbon Themes](https://carbondesignsystem.com/elements/themes/overview/) · `packages/themes/src/v10/white.ts` |
| 12 步用途表、Lc 60/90 保证、第 9 档最高色度 | [Radix Understanding the scale](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale) |
| mutable aliases / 语义别名 / 重命名色阶 | [Radix Aliasing](https://www.radix-ui.com/colors/docs/overview/aliasing) |
| Seed/Map/Alias 三级、三算法、嵌套 Provider、`cssVar`/`zeroRuntime` | [Ant Design 定制主题](https://ant.design/docs/react/customize-theme) |
| 腾讯蓝第 7 档、10 档功能色、14 档中性色、12% 品牌混色 | [TDesign 色彩](https://tdesign.tencent.com/design/color) |
| Less `modifyVars` 换肤、CSS Custom Properties、不兼容 IE | [Arco 定制主题](https://arco.design/react/docs/theme) |
| `$value`/`$type`/`$description`/`$deprecated`/`$extensions`/别名与 reference（**published 2025.10 权威口径**；原 `$extends`/`$root` 属早期草案表述） | [DTCG published 2025.10](https://www.designtokens.org/TR/2025.10/format/) · [preview drafts 仅作辨析](https://tr.designtokens.org/format/) |
| `include`→`source` 覆盖顺序、source 内部冲突告警、`.extend()`、DTCG 不可混用 | [Style Dictionary Config](https://styledictionary.com/reference/config/) · [Tokens](https://styledictionary.com/info/tokens/) |
| 层顺序、未分层样式优先、`!important` 反向 | [MDN @layer](https://developer.mozilla.org/en-US/docs/Web/CSS/@layer) |
| 模式数上限 4 / 40 | Figma 官方插件说明（Professional + Organization 4 个，Enterprise 40 个） |
| 对比度边界 0.1833 / 0.1750 / 0.3000 与九色实测 | **本技能按 WCAG 相对亮度公式自算**（§5） |
