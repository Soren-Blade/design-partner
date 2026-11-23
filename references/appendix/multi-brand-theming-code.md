# 多品牌与多主题 · 配置文件与可抄代码（附录）

> 2026-11-23 自 `references/multi-brand-theming.md` §十一、§二十 迁出（v72「越界内容拆附录」）。主文件保留判据、四轴、四层、色阶路线、护栏、矩阵策略、切换取舍、治理与自检。
>
> 迁移时删掉两段与正文同构的重复：原 20.1（主题矩阵骨架，见 §6.1/§6.2）与原 20.4（首屏注入，见 §十四）；原 11.3 的 SD 片段与 20.6 重复，只留 20.6 完整版。以正文为准。

## 段 A · 目录结构（core 与 brand 分离）

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

## 段 B · DTCG 组继承（published 2025.10 原文口径）

**版本更正（2026-11-23 实测）**：`$extends` 与 `$root` **不是**早期草案才有的写法。[Design Tokens Format Module 2025.10](https://www.designtokens.org/TR/2025.10/format/)（Final Community Group Report，28 October 2025）§6.2 定义 `$root`，§6.3 的 Group Properties 表收录 `$extends`，§6.4 给出完整继承语义。主文件「附：来源」里「属早期草案表述」的旧注记已删。

原文硬规则（逐条可判定）：

- `$extends` 只能指向**组**，指向 token 无效；语义等价于 JSON Schema `$ref`，实现可自选，但**对外行为必须是深合并**。
- 深合并：同路径 → 本地**完整替换**整个 token 定义（不是逐属性合并）；不同路径 → 并存；新增路径 → 并入。
- 循环继承必须报错（工具 MUST 检测）。
- 含 `$value` 是 token，不含是组；**同时含 `$value` 与子节点 = 无效结构，工具 MUST 报错**。
- 名字 MUST NOT 以 `$` 开头，MUST NOT 含 `{` `}` `.`。
- `$type` 解析：自身 → 被引用组（扩展解析后）→ 最近父组 → 都无则**无效，工具 MUST NOT 猜**。
- `$root` 是保留 token 名：`{color.accent.$root}` 有效；`{color.accent}` 指向组本身 → 无效。
- 组属性表只有：`$description` / `$type` / `$extends` / `$deprecated` / `$extensions`。

旧正文的继承示例仍成立（深合并 + 同路径完整替换）：

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

## 段 C · Style Dictionary 多品牌构建（已验证的配置模式）

SD 的多品牌不靠"主题插件"，靠两条机制的**组合**：

1. **`include` 放共享基座，`source` 放品牌覆盖**。加载顺序是 `include`（按数组序）→ `source`（按数组序），**后者覆盖前者**。
2. **关键规则**：`source` 覆盖 `include` **不告警**（因为这是设计意图）；但 `source` **内部**两个文件冲突**会告警**。所以品牌覆盖必须全放 `source`，共享基座全放 `include`——这样"意外的覆盖"才会被报出来。

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

## 段 D · 品牌色护栏（生成色阶后、写 token 前必跑）

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

## 段 E · 品牌色阶生成骨架（HCT tone，路线 A）

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

## 段 F · 主题切换（禁用过渡，只改属性）

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
