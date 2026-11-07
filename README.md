# Design Partner · 设计伙伴

> 一个会**自我进化**的设计 Skill：把模糊的想法变成有品味的设计决策，并在每次使用与每日迭代中变得更准。

![version](https://img.shields.io/badge/version-v31-1677ff)
![assets](https://img.shields.io/badge/reference_files-37-2ea44f)
![entries](https://img.shields.io/badge/curated_entries-657-e60023)
![updated](https://img.shields.io/badge/updated-2026-11-07-6e7781)

---

## 它解决什么问题

| 问题 | 表现 | 本 Skill 的解法 |
|---|---|---|
| **需求不清** | "做个好看点的页面" | 第 2 步：设计 brief 澄清（给选项，不问开放题） |
| **不知可行与否** | 做完才发现做不出来 | 第 3 步：可行性 × 美观性预判，执行前先给评审 |
| **没有参照** | 只会一种做法，遇到新场景就硬套 | 第 4 步：三级精准匹配（元素级 / 风格级 / 实现级） |
| **系统不统一** | 第 5 个页面和第 1 个不像同一产品 | 三层 token + DESIGN.md 契约 |
| **动效凭感觉** | 时长随手写 500ms、入场出场一样慢 | `motion-system.md` 语义曲线 + 时长刻度 + 场景表 |
| **图表不像专业出品** | 饼图切 8 片、柱状图截断轴、配色靠感觉 | `dataviz.md` 九类关系选型 + 精确色板 + 坐标轴铁律 |
| **表单难填、表格难读** | 一进来就全红、错误只说"格式不正确"、表格全列居中 | `form-table.md` 校验三档 + 错误文案模板 + 行高与列对齐铁律 |
| **无障碍过不了验收** | 焦点框被 `outline:none` 杀掉、只靠颜色表状态、读屏念不出、适老化尺寸不够 | `accessibility.md` 四档阈值 + 焦点三层 + 24/44/60 三档 + 25 条自检 |
| **反馈要么吵要么没** | 保存成功弹一堆 toast、严重错误 3 秒就消失、加载转圈 15 秒没进度、空态只放插画 | `feedback-states.md` 五层决策树 + toast 精确时长 + 五种空态 + 五级错误 |
| **多端就散架** | 手机上横向滚动、`100vh` 被地址栏挡住、8 列表格硬变卡片、大屏只是把手机版放大 | `responsive-layout.md` 六体系断点对照 + 五动词降级 + 窄屏表格四策略 + 版心阶梯 |
| **导航让人迷路** | 找不到入口、汉堡藏了关键功能、当前页不知道在哪、tab 放太多、面包屑末级还能点 | `navigation-ia.md` 四类职责 + 形态决策 + 项数铁律 + 当前位置指示 + 面包屑 + 可访问性 |
| **评审会变成挑刺或拍板** | 反馈模糊没法改、领导一句话就改、当场改稿、决策两周后被推翻、委员会改出平庸方案 | `design-critique.md` 两种评审分清 + 给反馈七铁律 + 接收四步 + 评判框架（NN/g 10 启发式 + 严重度 0–4）+ 反模式（design by committee/HiPPO）+ 决策记录 ADR |
| **版式全靠感觉** | 一行 130 字读不下去、海报裁切露白边、长图字小到看不清、印出来颜色发暗 | `editorial-layout.md` 行长行距联动表 + 出血与安全区 + 长图字号换算 + 印刷五查 |
| **品牌立不住** | logo 好看但说不清为什么、缩小就糊、品牌色一进暗色模式就脏、交付缺图标尺寸、没注册商标 | `brand-identity.md` 三词定位 + 七型决策树 + 24 网格构造 + 清space 与最小尺寸 + 色阶三路线 + tone 映射 + 交付清单 + 商标合规 |
| **暗色模式一开就脏** | 把亮色反一下就当暗色、纯白字刺眼、卡片和背景分不开、切换闪白、辅助文字看不清 | `dark-mode.md` 该不该做的证据链 + 三套表面层级精确值 + 不用纯白 + 实测对比度陷阱 + 四端实现与防闪白 |
| **配色凭感觉** | 配出来脏、对比度不达标、渐变发灰、色板错序、色盲分不清 | `color-science.md` 色彩空间谱系 + OKLCH 生成 + APCA 对比度 + OKLab 渐变插值 + 色盲 Okabe–Ito 8 色 |
| **风格说不清** | "做成 XX 那种感觉""要高级感"却拆不出做法、潮流叠满、前后页不像一个产品 | `visual-style-taxonomy.md` 四维信号拆解 + 17 条编年谱系 + 混搭纪律 + 风格→token 映射 |
| **字号行距全凭感觉** | 正文写死 px 用户改不了字号、放大到 200% 按钮被切、WCAG 文本间距一覆盖表单就重叠、表格数字每秒抖一次、中文出现方框乱码、字体不敢自托管 | `typography-system.md` 六层契约 + rem 阶梯 + 1.4.12 注入验收 + 200% 缩放 + `tabular-nums` + 逐字符回退与 `unicode-range` 分片 + `size-adjust` 压 CLS + clreq 中文排版 + OFL 1.1 授权 |
| **交付就翻车** | 标注全凭感觉、开发反复问"这里多少 px"、上线后走查一堆 P0、组件库发版没人敢升、改了默认值全站变样 | `handoff-collaboration.md` spec 9 字段 + 只标例外 + 9 态矩阵 + 命名四套 + P0–P3 门禁 + SemVer 与迁移表 + 走查三遍法 |
| **中文场景翻车** | 直接套英文规范，字号小、行距挤、标点乱 | `chinese-design.md` 中文排版修正 |
| **产出平庸** | 说不上哪不好，但就是不对 | 第 5 步原则执行 + 第 6 步 35 项自检 |
| **知识找不到** | 37 份参考、85 万字符，不知读哪节 | `memory/tree.md` 记忆树 + `dp_search.py` 章节级检索 |
| **不记得用户偏好** | 每次都从零猜 | `memory/design-log.md` 持续蒸馏偏好画像 |

---

## 知识资产（自动统计，随迭代更新）

| 资产 | 内容 | 条目 | 快照 |
|---|---|---|---|
| [知识路线图](references/knowledge-map.md) | L0→L4 分级目标 / 必读 / 练习 / 验收 + 136 条自测 | 规则型 | 2026-11-05 |
| [元素设计模式](references/patterns.md) | 12 类高频元素的构型谱系、参数区间、速配规则 | 规则型 | 2026-10-29 |
| [设计 Token 体系](references/design-tokens.md) | 三层架构 / Ant Design 数值全量 / 三大体系对比 / 中文设计系统矩阵 | 规则型 | 2026-10-29 |
| [动效与微交互系统](references/motion-system.md) | 曲线语义表（M3/Carbon/Ant 精确值）/ 时长刻度 / 20 场景速查 / 转场代码 / 降级与验收 | 规则型 | 2026-10-30 |
| [动效进阶·编排 / 状态机 / 共享元素转场](references/motion-orchestration.md) | 三层分工判层 / 四种时间结构与 T≤400ms 总时长公式 / 两代 stagger API / FLIP 四步与 100ms 窗口 / 列表增删重排四策略 / View Transitions 伪元素树与 UA 默认 0.25s·ease·三 promise·单例中断 / Motion layoutId 与 scale correction / 四态状态机与 XState / 中断三策略与 WAAPI 全默认值 / @starting-style 四件套 / WCAG 2.3.3 与 JS 层降级 / 跨框架矩阵 / 16 场景 / 20 反模式 / 20 自检 / 8 段代码 | 规则型 | 2026-11-05 |
| [数据可视化规范](references/dataviz.md) | FT 九类关系选型 / Carbon·AntV 精确色板 / 坐标轴与图例数值 / 仪表盘布局 / 12 条反模式 | 规则型 | 2026-10-31 |
| [表单与表格规范](references/form-table.md) | 标签对齐决策 / 字段定宽 / 校验三档与 12 条错误文案模板 / 行高三档 / 列对齐 / 分页·批量·空态 / 18 条反模式 | 规则型 | 2026-10-31 |
| [可访问性实操](references/accessibility.md) | WCAG 2.2 四档阈值 / 焦点三层标准与可抄样式 / 24px 圆间距例外 / ARIA 纪律 / aria-live / 读屏实测 / GB/T 37668 与适老化 / 25 条自检 | 规则型 | 2026-11-01 |
| [反馈与状态设计](references/feedback-states.md) | 五层反馈决策树 / 0.1·1·10s 阈值 / 四体系 toast 时长与宽度 / 加载三形态 / 进度六铁律 / 五种空态 / 五级错误 / 确认框八条 / 五态模型 / WCAG 4.1.3 / 15 项自检 | 规则型 | 2026-11-01 |
| [响应式与断点体系](references/responsive-layout.md) | 六体系断点精确值对照 / 断点按内容定 / 跨断点五动词 / gutter 固定 column 流体 / 版心阶梯 / 容器查询 / clamp 无障碍公式 / 视口单位陷阱 / 窄屏表格四策略 / 中后台 1440 适配 / 20 条反模式 | 规则型 | 2026-11-01 |
| [版式与网格（Editorial）](references/editorial-layout.md) | 五类载体决策 / 网格五型 / 12 栏与基线 / Van de Graaf 页边距 2:3:4:6 / 模数阶梯七档 / 行长 45–90 字符与行距 120–145% / 孤寡行与断行 / 海报出血 3mm 与安全区 / 长图字号换算 / 九平台社媒尺寸 / 印刷 CMYK 与总墨量 300% / 竖排与避头尾 / 18 项自检 | 规则型 | 2026-11-01 |
| [品牌视觉与 Logo 逻辑](references/brand-identity.md) | 四层结构 / 三词定位与六维翻译 / 七型标志决策树 / 24dp 网格与四基形 / 光学修正四条 / 清space 三口径 / 最小尺寸 40px·10mm / 响应式标志四档 / 种子色四问 / 三条色阶路线（HCT·Radix 12 步·对比度优先）/ M3 亮暗 tone 全表 / 图标网格两体系 / 插画五参数 / 品牌语气四维 / 资产交付清单 / 商标与授权合规 / 18 项自检 | 规则型 | 2026-11-01 |
| [性能与设计的关系](references/performance-design.md) | CWV 七指标阈值与 p75 口径 / Lighthouse 10 权重 / LCP 四分解 40·10·40·10 / INP 三阶段与长任务 50ms / CLS 公式与 500ms 免责窗口 / 关键路径 170KB 与六类页面预算 / 图片格式矩阵与 25 倍像素浪费 / font-display 五档与中文字集化 / 视觉手法性能价格表 / 帧预算 16.67ms 与图层内存算术 / 三档决策分级 / 弱网三层降级 / 小程序单包 2MB / 18 项自检 | 规则型 | 2026-11-01 |
| [暗色模式体系](references/dark-mode.md) | 该不该做的 NN/g 证据链 / 三态切换决策树 / 表面层级三套精确值（M3 tone 4·6·10·12·17·22 / Ant lighten 0·8·12·26 / Carbon g100 阶梯）/ 实测对比度陷阱（45% 白仅 4.43、边框仅 2.09:1）/ 不用纯白的四体系共识 / 阴影两派与合成方案 / 品牌色 tone 重映射 / 涨跌色双套 / 图像四死法 / 四端实现与防闪白 / 暗色专属八陷阱 / 22 项自检 | 规则型 | 2026-11-01 |
| [多品牌与多主题 Token 架构](references/multi-brand-theming.md) | 四根正交轴 / 四层架构 L0–L3 / 品牌色阶四条生成路线 / 对比度护栏（亮度边界 0.1833·0.1750·0.3000 与九色实测）/ 轴独立选择器与 @layer / 多品牌同页共存 / 四套真实主题矩阵 / DTCG 与 Style Dictionary / Figma 变量模式 / 注入六步管线 / 18 项自检 | 规则型 | 2026-11-01 |
| [设计交付与协作](references/handoff-collaboration.md) | 交付链六关卡与 intent·rule·value 三层 / spec 9 字段与 Carbon 规格六类 / 标注只标四类（8px mini unit·padding 16·gutter 32·spacing 13 档）/ 9 态矩阵 / 命名四套与默认变体规则 / 组件属性四类与 3–5 上限 / Given-When-Then 3–5 步 / 评审 30 分钟与 2 正 1 改 / 走查三遍法与 9 字段表 / P0–P3 门禁 / SemVer 11 条与 MAJOR 迁移表 / DTCG 与 Style Dictionary 管线 / 回归四层（80%·VRT·AVT·三读屏器）/ 六个交付指标 / 20 项自检 + 4 套模板 | 规则型 | 2026-11-01 |
| [内容设计与 UX 文案](references/ux-writing.md) | 三级文案尺寸 / 五条不可商量原则（禁 OK）/ 按钮·错误·空态文案模板 / 语气四维 / 表单与对话框文案 / 术语管理 / sentence case 四体系共识 / 中文标点与数字日期 / 国际化写文案速记（短串膨胀口径见 i18n-localization.md）/ 文案 token / 18 项自检 | 规则型 | 2026-11-05 |
| [国际化与本地化设计（i18n / L10n / RTL）](references/i18n-localization.md) | 三层判层（标记层 lang·dir / 布局层弹性·逻辑属性·镜像 / 数据层复数·日期·数字·姓名·排序）/ W3C-IBM 膨胀表（≤10 字符 200–300% → microcopy 2–3×）/ 裁决 ux-writing §13「+40%」对短串错误 / WCAG 3.1.1 A·3.1.2 AA 与 H57·H58 / W3C 硬禁令 Never use CSS to apply the base direction / CSS logical properties 全映射 / Material 镜像白黑名单 / CLDR 复数六类（one≠1·中文仅 other）/ ICU MessageFormat 禁拼接 / Intl API 与 Node v22.22.2 实测（DurationFormat 需能力检测）/ 日期·数字·货币·列表·排序 / 姓名单一 Full name / 伪本地化五变换 / 12 场景 / 20 反模式 / 20 自检 | 规则型 | 2026-11-05 |
| [演示文稿与幻灯片版式](references/presentation-design.md) | 16:9=1920×1080 / 标题 5%·动作 3% 安全区 / 字号阶梯（最小 24pt 线上 28pt）/ 文字密度四规则 / 母版 6–8 版式 / 动画与转场区分三档 / 投影对比度高 50% / 线上与中文演示 / 三分法与 Z 模式 / 12 场景 / 18 自检 | 规则型 | 2026-11-05 |
| [DESIGN.md 规范](references/design-md-format.md) | 九章骨架 + 54 品牌 DNA 速查 + 项目类型选型 | 规则型 | 2026-10-29 |
| [设计系统文档写作](references/design-system-docs.md) | Diátaxis 四象限判层 / GOV.UK 组件页九段式与活文档四件套 / 文档信息架构四条地基与 Google 写作规范 / 完整填充范例 / 组件成熟度（USWDS 三阶段·Carbon semver）/ Docusaurus 3.10.2 版本化（<10·preview 2–3·patch 不切）/ Keep a Changelog 1.1.0 七原则六类 / MAJOR 迁移文档 / DTCG published 2025.10 与 preview draft 裁决 / Storybook Autodocs·MDX·Doc Blocks·Figma Code Connect / GOV.UK 贡献与治理 / 新鲜度与漂移自举 / 12 场景 / 20 反模式 / 20 自检 | 规则型 | 2026-11-05 |
| [AI / 生成式设计工具链](references/ai-design-toolchain.md) | 中国《标识办法》14 条设计动作与中欧美三法域矩阵 / USCO「提示词不构成作者身份」与可举证创作链 / C2PA 三概念分离 / DESIGN.md 给 AI 读的契约 / 提示词四区块与 prompt SemVer / HAX G1–G18 界面落点 / AI Slop Test 与 8 维 DO-DON'T / 12 类固有缺陷 / 5 层工具链 18 仓库 API 实测与选型三问 / 12 场景 / 20 反模式 / 20 自检 / 6 段可抄代码（3 段已实跑） | 规则型 | 2026-11-06 |
| [中文设计场景](references/chinese-design.md) | 中文排版规范 + 中文设计生态地图 + 产品形态特征 | 规则型 | 2026-10-29 |
| [灵感与阅读](references/inspiration.md) | 策展画廊与设计阅读 | 137 | 2026-10-29 |
| [设计资源](references/resources.md) | 组件 / 图标 / 动效 3D / 字体配色 | 201 | 2026-10-29 |
| [设计伦理与包容性](references/design-ethics-inclusion.md) | CPPA §7004 对称选择与步数测量 / §7003 可读性与 WCAG 2.1 引用 / EDPB 03-2022 v2.0 六类机制 / PIPL 14·15·16·17·24 五条 UI 底线 / 广告办法第 10 条一键关闭三数值 / 网络交易办法第 18 条 2025 修正与「前五日」反陈旧裁决 / 未成年人条例令第 766 号 42-45·47 / deceptive.design 现行 18 类 / 成瘾机制四红线 / Inclusive Design 七原则与 COGA 八目标 / 合规×包容四象限 / 18 场景决策矩阵 / 20 反模式 / 22 自检 / 4 段可抄代码（3 段 Python 已实跑，含陈旧法条守卫） | 规则型 | 2026-11-06 |
| [组件 API 设计与组合模式](references/component-api-design.md) | 三份所有权（状态 / 渲染 / 契约与演进）/ Radix `prop !== undefined` 与受控生命周期告警 / React `<input>` 受控契约 / 五种换元素 API（asChild mergeProps · Ariakit render · MUI slots/slotProps · Vue slots · children） / 开放扩展四条与合并优先级 / **React 19 forwardRef 反陈旧裁决**与命令式 ref 红线 / APG 键盘契约与单 tab stop / data-* 状态暴露 / **API SemVer 六冻结面 = MAJOR + codemod** / Storybook argTypes / TypeScript 可辨识联合 / 16 场景 / 20 反模式 / 22 自检 / 4 段代码（3 段 Python 实跑全 PASS） | 规则型 | 2026-11-07 |
| [设计度量与用户研究](references/design-measurement-research.md) | ISO 9241-11 可用性三要素（有效性/效率/满意度）/ 任务级指标（成功率·错误率·时长·SE）/ SUS·UMUX-Lite·SEQ·SUPR-Q·NPS 计分与基准（SUS 68 基准·一致作答恒 50）/ Google HEART 五维三层落地 / 样本量公式（定性 5 人≈84%·定量 n≈Z²p(1−p)/E²）/ 研究方法 2×2 与卡片分类·树测试 / 可用性测试（主持·非主持·出声思考）/ 问卷偏差避坑 / A/B 统计（双比例 z 检验·MDE·95% CI 跨 0 即无 winner·护栏指标·序贯检验）/ 行为分析与漏斗 / 证据分级与三角验证 / 研究 ops 与工具矩阵 / 12 场景 / 20 反模式 / 20 自检 / 4 段可抄代码（Python 全实跑） | 规则型 | 2026-11-07 |
| [图标设计系统](references/iconography.md) | 24×24 网格与 keyline（圆⌀20·方18·矩20×16）+ 描边（Lucide stroke=2 / Heroicons 1.5 / Carbon 1.5 / Material wght 100–700·GRAD −50..200·FILL 0–1）+ 尺寸阶梯 12/16/20/24/32/48 + 图标-文字间距 8px（最小 4px）+ 填充/描边/双色 + 光学对齐与过冲 + spinner 1–1.4s linear + 交付格式（内联 SVG/Sprite/字体子集/组件）+ 可访问性（aria-hidden+focusable=false / role=img+aria-label / ≥3:1 / 不靠颜色）+ 动画降级 + kebab-case 命名 + 库选型矩阵（Lucide 25.6k★/Tabler 22.6k★/Fluent 11k★/Radix 2.7k★ GitHub API 实测）+ 12 场景 + 20 反模式 + 20 自检 + 4 段可抄代码 | 规则型 | — |
| [设计评审与反馈](references/design-critique.md) | 评审是暴露盲点/对齐决策（非挑错非批准）+ 两种评审分清（standalone critique / design review）+ 三前提（范围/目标/对话）+ 给反馈七铁律（具体/挂目标/品味vs工艺/I like·I wish·I wonder/行为化/2正1改/给观察不给方案跳转）+ 接收反馈四步（不辩护/追问/归类/记录决策）+ RACI 与远程异步（48h 窗口）+ 评判框架（NN/g 10 启发式 + 严重度 0–4 + DFV 三问 + 重要性×确定性 + 可取性测试）+ 15 反模式（设计by committee/HiPPO/审美化争论/方案跳转/模糊反馈/现场改稿…）+ 决策记录（ADR / critique notes 模板）+ 工具（Figma comment/Figjam/Notion/PR review 类比/Loom）+ 20 自检 + 4 段可抄模板 | 规则型 | 2026-11-07 |
| [导航与信息架构](references/navigation-ia.md) | 四类职责谱系（全局/局部/上下文/辅助）+ 形态决策矩阵（tab/侧栏/汉堡/rail/drawer）+ 项数铁律（米勒 7±2·全局 5–9·底部 ≤5）+ 深度 vs 广度（3-click 迷思/信息气味/卡片分类·树测试）+ 面包屑三型 + ARIA Tabs 键盘契约 + 移动端降级（Apple ≤5·Material bar/rail/drawer）+ 当前位置指示（aria-current）+ WCAG 2.4.x 导航口径 + 搜索协同 + 20 反模式 + 20 自检 + 5 段可抄代码 | 规则型 | — |
| [组件库地图](references/component-libraries.md) | 14 库元素覆盖矩阵（GitHub API 验证） | 规则型 | 2026-10-29 |
| [制作工具](references/tools.md) | 开发 / AI / 截取 / 效率工具 | 153 | 2026-10-29 |
| [作品集](references/portfolios.md) | 一线从业者站点，用于审美校准 | 166 | 2026-10-29 |
| [色彩科学](references/color-science.md) | 色彩空间谱系 sRGB/HSL/HSV/Lab/LCH/OKLab/OKLCH/Display P3 / 感知均匀性与 HSL 为何撒谎 / OKLab 公式与 CSS oklch() / 对比度双算法（WCAG 2.x 相对亮度 + APCA Lc 分档）/ 色盲与 Okabe–Ito 8 色 / 色板生成四路线（OKLCH 旋转·Radix 12 步·M3 tonal·Leonardo 对比度优先·HCT）/ 渐变 OKLab 插值 / 色彩无障碍 beyond 1.4.11 / 工程实现 color()·color-mix·相对颜色语法·culori·colorjs.io·Figma 变量 / 12 场景 / 20 反模式 / 20 自检 / 6 段可抄代码 | 规则型 | 2026-11-07 |
| [视觉风格谱系与设计运动](references/visual-style-taxonomy.md) | 立场：风格不是名词贴标签，是四维信号的组合签名 / 四维信号表（Typography·Color·Shape&Material·Motion&Space 逐维标注）/ 17 条编年谱系（Swiss 1950s→Bauhaus→Brutalism→Memphis 1981→Skeuomorphism→Flat 2013→Material 2014→Neumorphism 2019→Glassmorphism 2020→Y2K→Vaporwave→Cyberpunk→Bento 2022→Claymorphism→企业中性，各给何时用/何时不用）/ 匹配决策（参考站四步拆解·形容词先确认语境）/ 风格 vs 品牌三词定位 / 混搭纪律（depth language 只一种主导·装饰密度只一个极端·趋势叠加上限=1）/ 趋势生命周期（技术驱动 vs 纯视觉潮流 12–24 个月）/ 中文与出海 / 风格→token 映射与 DTCG / 新拟态与玻璃拟态硬红线 / 12 场景 / 20 反模式 / 20 自检 / 3 段可抄清单或代码 | 规则型 | 2026-11-07 |
| [字体排印系统](references/typography-system.md) | 立场：排印不是选一款字体，是六层契约（覆盖·尺度·节奏·字形·加载·授权）/ 三条裁决（px 写正文不可访问·MDN 原文与 rem 阶梯 / WCAG 2.2 SC 1.4.12 文本间距是用户覆盖抗压测试非默认样式表 / font-family 逐字符回退 + unicode-range 命中一字即整片下载）/ 字体选型三前置 / 行高两档（M3 大字号 1.2×·小正文标签 1.5×）与 SC 1.4.8 行宽·禁 justify·200% 无横向滚动 / 注入式 1.4.12 验收五步与两种 200% 缩放 / 可变字体五注册轴与 GRAD / OpenType 数字特性 8 值全表与 tabular-nums / 高位 font-variant-* 优先与低位 API 纪律 / font-display 三阶段五档 / size-adjust 度量对齐压 CLS / W3C clreq 中文排版（1/4 汉字宽·1:1 正方形·全角 ASCII·UAX #29 字素丛）/ M3 五角色×三尺寸与 --md-sys-typescale-* token 化 / OFL 1.1 五条件 / 9 仓库 GitHub API 实测 / 12 场景 / 20 反模式 / 20 自检 / 6 段可抄代码（含可实跑的排印可访问性静态扫描） | 规则型 | 2026-11-07 |

> 条目数与快照日期由 `scripts/build_readme.py` 从文件实时统计，不手写。
> 快照 > 30 天时执行 `python scripts/refresh_catalog.py` 自动重抓。

---

## 七步工作流

```
第 0 步  先检索        →  dp_search.py 定位到「文件 §章节」，只读那一段
第 1 步  识别设计意图  →  180 类意图路由（全表见 SKILL.md 第 1 步）
第 2 步  完善需求      →  brief 澄清，最多 3 个问题，给选项不给开放题；主动提示盲区
第 3 步  可行性×美观性 →  技术/范围/资源/性能 四查 + 审美风险预判，给明确立场
第 4 步  匹配灵感      →  L1 元素级（出可视化设计板）/ L2 风格级（品牌 DNA）/ L3 实现级（组件库）
第 5 步  按原则执行    →  层级 / 排版 / 色彩 / 间距 / 动效 / 图表 / 表单 / 表格 / 反馈与状态 / 响应式 / 版式与网格 / 交付与协作 / 一致性 / 系统化 / 中文修正
第 6 步  自检与交付    →  35 项自检（含中文关、系统关、动效关、图表关、表单关、表格关、无障碍关、反馈关、响应式关、版式关、品牌关、暗色关、性能关、交付关、文案关、演示关、编排关、国际化关、文档关、AI 关、伦理关、组件 API 关、度量关、图标关、导航关、色彩科学关、评审关、风格关、字体排印关）+ 交付说明三段式
```

**核心主张：给立场，不和稀泥。** 评审先给结论再列备选；⚠️ 时给"满足什么条件就可行"，❌ 时给最接近意图的替代方案。

---

## 记忆树与快捷检索

资产过千行后，"知识在哪"本身成了问题。本技能自带一层索引：

```bash
python scripts/dp_search.py "缓动曲线"    # → references/motion-system.md §2 (L30) + 摘要
python scripts/dp_search.py --topic       # 全部主题总览
python scripts/mindmap.py                 # 重建 memory/tree.md + index.json，并做接线体检
python scripts/regression.py --baseline   # 收口门槛：新主题可发现性 + HEAD 基线 top3 零退化
```

| 文件 | 作用 |
|---|---|
| [`memory/tree.md`](memory/tree.md) | 意图→位置路由表 + 别名映射 + 全资产章节树 + 接线体检（谁写了但没被路由） |
| `memory/index.json` | 机器索引：文件 → 章节 → 行号 → 摘要（检索数据源） |
| `memory/aliases.json` | **检索层别名映射**：198 组口语/术语/中英对应，只提升召回、不改路由优先级；单组 ≤12 词、成员不与既有组重复 |
| `scripts/dp_search.py` | 中文按二元组拆词、英文按词拆，标题/摘要/正文加权打分；别名以 0.45 权重补充召回 |
| `scripts/mindmap.py` | 扫描全部 Markdown 重建索引；`--check` 只跑体检 |
| `scripts/regression.py` | 固化新主题门槛 + `git archive HEAD` 基线 top3 对比；路由边界与登记演进各按硬校验判定 |

**接线体检**是自我进化的自检项：新增参考文件却忘了在 `SKILL.md` 加路由时，`mindmap.py` 会直接报「未接线」——避免"写了等于没写"。

---

## 知识路线图 L0→L4

| 级别 | 目标 | 可交付物 |
|---|---|---|
| **L0** 视觉感知 | 能**看出**两个设计的高低 | 一份"好在哪/差在哪"的书面判断 |
| **L1** 界面语汇 | 知道每个元素**有几种做法** | 元素级设计板（4–6 变体） |
| **L2** 系统秩序 | 用**一套 token** 统管全站 | token 表 + DESIGN.md |
| **L3** 工程落地 | 把设计**变成可运行代码** | 组件代码 / 可交互页面 |
| **L4** 判断与品味 | 在**冲突约束**下做取舍 | 设计评审报告、方案对比结论 |

含 25 条专题支线（中文场景 / 数据可视化 / 动效 / 可访问性 / 反馈与状态 / 版式与网格 / 品牌视觉与 Logo / 暗色模式 / 性能与设计 / 设计交付与协作 / 内容设计与 UX 文案 / 演示文稿与幻灯片版式 / 动效编排与状态机 / 国际化与本地化 / 设计系统文档写作 / AI / 生成式设计工具链 / 设计伦理与包容性 / 组件 API 设计与组合模式 / 设计度量与用户研究 / 图标设计系统 / 导航与信息架构 / 设计评审与反馈 / 色彩科学 / 视觉风格谱系与设计运动 / 字体排印系统）、学习节奏表、136 条能力自测 → 见 [`references/knowledge-map.md`](references/knowledge-map.md)

---

## 自我进化机制

```
每日  ┌─ 取源：Design-related websites.txt + 上轮待挖项 + 知识缺口
      ├─ 验证：GitHub API 实测 star/许可；规范数值读官方原文
      ├─ 蒸馏：产出可执行判断规则（数值/构型/验收），不是链接清单
      ├─ 接线：更新 SKILL.md 路由 + 补 memory/aliases.json 别名（单组 ≤12 词）+ mindmap 重建记忆树（含接线体检）
      ├─ 回归：regression.py --baseline，新主题门槛全过 + 历史 top3 零退化，退出码 0 才继续
      └─ 归档：design-log 追加 → build_readme 重算 → git commit → REST API 推送 → 双份全局安装
```

**质量门槛**：一轮升级至少要让某类问题**不再含糊**（能给具体数值或明确立场）。只多了几条链接 = 无效升级，重做。

**检索门槛**：新知识必须能被 `dp_search.py "关键词"` 命中前 3 条，否则说明标题不像索引。测试集含「主题词 + 通用跨域词」组合；泛化跨域查询按 **路由边界** 单列（不计通过率但仍校验与 HEAD 一致），新权威资产上位按 **登记演进** 判定（须过 top1 不变 / 原答案仍在 top5 / `--no-alias` 仍在前 3 三条硬校验），别名抢词则拆组修掉——三类例外由 `regression.py` 统一裁定，不许拿来凑数。

**记忆协议**：偏好信号出现 ≥2 次即升级为画像规则；画像优先于通用推荐；记录只增不改，保持可审计。

---

## 升级记录

| 日期 | 内容 |
|---|---|
| 2026-11-07 | 每日升级 #27：字体排印系统（Typography System） |
| 2026-11-07 | 每日升级 #26：视觉风格谱系与设计运动（Visual Style Taxonomy） |
| 2026-11-07 | 每日升级 #25：色彩科学（Color Science） |
| 2026-11-07 | 设计评审与反馈（Design Critique & Feedback，每日升级 #24） |
| 2026-11-07 | 导航与信息架构（Navigation & IA，每日升级 #23） |
| 2026-11-07 | 图标设计系统（Iconography，每日升级 #22） |
| 2026-11-07 | 设计度量与用户研究：可用性指标、研究方法与统计验收（每日升级 #21） |
| 2026-11-07 | 组件 API 设计与组合模式：状态所有权、渲染所有权、契约可演进（每日升级 #20） |

---

## 数据来源

- [designeer.xyz](https://designeer.xyz/) — 按 craft / utility / clarity / relevance 人工策展的 657 条资源
- [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — 54 个真实产品 DESIGN.md
- [Ant Design 设计规范](https://ant.design/docs/spec/introduce-cn) — 价值观 / 色彩 / 字体 / 布局 / 动效原文
- [Material 3 · Easing & duration tokens](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs) — 曲线与时长 token 全表
- [Carbon Design System · Motion](https://www.carbondesignsystem.com/elements/motion/overview/) — productive/expressive 二分与评估清单
- [Fluent 2 · Motion](https://fluent2.microsoft.design/motion) — 四种转场模式与编排原则
- [MDN](https://developer.mozilla.org/) — View Transition API / scroll-driven animations / prefers-reduced-motion
- [FT Visual Vocabulary](https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary) — 九类数据关系与图形选型（含简体中文版）
- [IBM Carbon · Data visualization color palettes](https://carbondesignsystem.com/data-visualization/color-palettes/) — 分类/顺序/发散色板精确 hex 与取用顺序
- [AntV G2](https://github.com/antvis/G2) — 色板、坐标轴、图例、Tooltip 默认值（源码实测）
- [W3C WCAG 2.2 SC 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) — 图形对象 3:1 非文本对比度
- [Datawrapper](https://www.datawrapper.de/blog/dual-axis-charts-guide) — 双轴图的适用条件与误导机制
- [W3C clreq](https://www.w3.org/TR/clreq/) — 中文排版需求
- [Apple HIG](https://developer.apple.com/design/human-interface-guidelines)
- [Björn Ottosson · OKLab](https://bottosson.github.io/posts/oklab/) — OKLab/OKLCH 感知均匀色彩空间原始定义与公式
- [Evil Martians · OKLCH in CSS](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl) — OKLCH 生产可用性、浏览器支持与 `oklch()` 实战
- [MDN · oklch()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch) — `oklch()` 语法、色域与降级
- [APCA · W3C Community Group](https://www.w3.org/TR/apa/) — 下一代对比度算法 Lc 等级与可读性阈值
- [color.js](https://colorjs.io/) — 现代色彩空间计算库（OKLab/OKLCH/Display P3）教学站点
- [culori](https://github.com/EvilMartians/culori) — 轻量色彩计算库（OKLab/OKLCH 插值、色板生成）
- [Okabe–Ito 8 色](https://jfly.uni-koeln.de/tools/colorblind/ColorUniversalDesign.pdf) — 色盲安全 8 色 hex 表（学术原版）
- [W3C WCAG 2.1 · Contrast (Minimum)](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) — 4.5:1 文本对比度定义
- [Radix Colors](https://www.radix-ui.com/colors) — 感知均匀、可访问的色阶生成器
- [Material 3 · Tonal Palette](https://m3.material.io/styles/color/the-color-system/tonal-palettes) — HCT 色阶与品牌色派生
- [Adobe Leonardo](https://leonardo.cc/) — 基于对比度的可访问色板生成工具
- [Michal Malewicz · Neumorphism in user interfaces](https://uxdesign.cc/neumorphism-in-user-interfaces-b47cef3bf3a6) — 2019-12-17 原文：New Skeuomorphism 由 Jason Kelley 在评论区命名，Malewicz 去掉 "o" 定型
- [UX Collective / UX Planet · Neumorphism](https://uxplanet.org/neumorphism-design-the-future-of-ui-ux-design-d4dc01c6a382) — Plyuto 2019 原作与低对比可见性缺陷
- [Interaction Design Foundation · Design History](https://www.interaction-design.org/literature/topics/design-history) — Bauhaus 1919–1933 / De Stijl 1917–1931 / Swiss style / Skeuomorphic→Flat 编年
- [MDN · font-size](https://developer.mozilla.org/en-US/docs/Web/CSS/font-size) — 相对单位可访问性建议 / px not accessible / em compounding / rem 消除 compounding
- [W3C WCAG 2.2 · Understanding SC 1.4.12 Text Spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html) — 四项门槛 / Exception / Note 1「非默认样式表」/ Author Responsibility
- [W3C WCAG 2.2 · SC 1.4.4 / 1.4.8](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html) — Resize Text 200% / Visual Presentation 行宽与禁 justify
- [Material 3 · Applying type](https://m3.material.io/styles/typography/applying-type) — 五角色×三尺寸 / 行高 1.2×·1.5× / tabular figures / 3:1·4.5:1 / 链接下划线 / half-leading
- [W3C clreq](https://www.w3.org/TR/clreq/) — §2.1.3 ≤1/4 汉字宽 / §1.2 1:1 正方形 / §4.1 全角 ASCII / §4.2.1 UAX #29 字素丛
- [SIL Open Font License 1.1](https://openfontlicense.org/open-font-license-official-text/) — 官方英文原文：五条件 / RFN / 文档不受字体 license 约束
- [MDN · font-display / unicode-range / font-variant-numeric / font-feature-settings](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display) — 字体加载三阶段五档 / 子集化 / OpenType 数字特性 / 低位 API 纪律
- [Google Fonts](https://github.com/google/fonts) · [rsms/inter](https://github.com/rsms/inter) · [fonttools](https://github.com/fonttools/fonttools) — 字体源与子集化工具链（star / 许可 GitHub API 实测）
- [Calinou/awesome-design](https://github.com/Calinou/awesome-design) — UI/UX 高质量资源策展（GitHub API 实测 10★）
- [bradtraversy/design-resources-for-developers](https://github.com/bradtraversy/design-resources-for-developers) — 设计资源合集（GitHub API 实测 67,340★ · MIT）

## 目录结构

```
design-partner/
├── SKILL.md                  # 主文件：七步工作流 + 资产索引 + 进化协议
├── README.md                 # 本文件（自动生成）
├── references/               # 知识库（37 份，见上表）
├── memory/
│   ├── tree.md               # 记忆树（自动生成）
│   ├── index.json            # 检索索引（自动生成）
│   ├── aliases.json          # 检索层别名映射（手维护）
│   └── design-log.md         # 偏好画像 + 匹配日志（只增不改）
└── scripts/
    ├── dp_search.py          # 章节级快捷检索
    ├── regression.py         # 检索回归门槛（门槛 + HEAD 基线对比）
    ├── mindmap.py            # 重建记忆树 + 接线体检
    ├── refresh_catalog.py    # 重抓目录 API，重建 references
    ├── build_readme.py       # 统计并重建 README
    └── publish_github.py     # REST API 发布（git push 被网络策略拦截时用）
```

## License

MIT
