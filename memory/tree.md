# 记忆树 · Knowledge Tree

> 自动生成于 2026-10-31 22:07 ｜ 14 个文件 · 179 个章节 · 143,097 字符
> 由 `scripts/mindmap.py` 重建，**不要手改**（手改会被下次覆盖；要改就改源文件或脚本）。

## 怎么用（三条命令）

```bash
python scripts/dp_search.py "缓动曲线"      # 关键词检索：命中章节 + 行号 + 摘要
python scripts/dp_search.py --topic          # 列出所有主题（章节标题一览）
python scripts/mindmap.py                    # 资产变更后重建本树与 index.json
```

**检索纪律**：先用 `dp_search` 定位到「文件 §章节」，再只读那一段。不要整份读 references——11 份文件全读一遍会吃掉大量上下文，而命中往往只在一节。

## 一、意图 → 位置（快捷路由）

| 用户这么说 | 去哪儿 |
|---|---|
| 从零做视觉 | 第 5 步原则 + patterns.md 取构型 + design-tokens.md 取数值 |
| 改进现有设计 | 按第 5 步逐条诊断；动效问题查 motion-system.md §10 验收清单 |
| 要灵感 / 参考 | patterns.md（元素级）→ inspiration.md（风格级）→ portfolios.md（校准） |
| 要设计规范 / 系统 | design-tokens.md（三层 token）→ design-md-format.md（九章骨架） |
| 对标某品牌 | design-md-format.md §3 品牌 DNA + design-tokens.md 取精确值 |
| 中文项目 | chinese-design.md（排版/生态）→ motion-system.md §9（小程序） |
| 动效 / 微交互 / 动画 | motion-system.md：§2 曲线 · §3 时长 · §4 场景表 · §7 代码 · §10 验收 |
| 滚动动画 / 页面转场 | motion-system.md §7.3 View Transitions · §7.4 scroll-driven |
| 无障碍 / reduced-motion | motion-system.md §8.1 三档降级 |
| 找工具 / 资产 | tools.md（工具）· resources.md（图标/字体/3D）· component-libraries.md（代码） |
| 想提升自己 / 学习路径 | knowledge-map.md L0→L4 + 20 条自测 |
| 不确定知识在哪 | python scripts/dp_search.py "关键词" |

## 二、知识树（按文件）

### `SKILL.md` · Design Partner 设计伙伴
_262 行 · 快照 — · 12 节_

- **工作流：接到任何设计任务时按此执行** `L39`
  - **第 0 步 · 先检索，别整份读** `L41` — 资产已超 12 份、约 12 万字符。整份读完等于浪费上下文，而答案通常只在一节。动手前：
  - **第 1 步 · 识别设计意图** `L52`
  - **第 2 步 · 完善需求（设计 brief 澄清）** `L72` — 动手前检查以下要素。只问缺失且影响方向的项（一次最多 3 个，给选项不给开放题）；要素齐全就直接进第 3 步。用户不在场时选合理默认值并注明假设。
  - **第 3 步 · 可行性 × 美观性预判（自我判断，反馈给用户）** `L87` — 执行前对需求本身给出结构化评审——这一步的产出是给用户的反馈，不是自我怀疑。用户在线时先给评审再动手；不在线时把评审作为交付说明的开头。
  - **第 4 步 · 匹配灵感（三级精准匹配）** `L113` — 先读 memory/design-log.md 的「当前画像」：用户既定偏好优先于通用推荐（画像说不要渐变，就不出现渐变变体）。
  - **第 5 步 · 按设计原则执行** `L144` — 从策展标准（craft / utility / clarity / relevance）展开，适用于任何视觉产出：
  - **第 6 步 · 产出前自检 + 交付评审** `L201` — 交付前逐条检查，不达标先修再交：
- **自我成长机制（用得越多越准）** `L220` — 记忆档案 memory/design-log.md 分两层，协议如下：
- **自我进化机制（知识保鲜）** `L233` — - 自动刷新：references 头部标注快照日期。快照 30 天、或用户说"更新知识库/刷新灵感库"时，执行 python <技能目录/scripts/refreshcatalog.py——它重抓 designeer.xyz 目录 AP
  - **每日升级协议（Deep Distillation Loop）** `L240` — 定时任务按此五步跑，每次只深挖一个主题，不做广度摊平：
- **边界与习惯** `L254` — - 给立场：评审和对比都先给明确结论和理由，再列备选；不和稀泥。

### `references/chinese-design.md` · 中文设计场景 — Chinese Design（排版规范 + 生态地图）
_195 行 · 快照 2026-10-29 · 14 节_

- **一、中文排版：为什么不是"英文换字"** `L10`
  - **1.1 三个根本差异** `L12`
  - **1.2 字号与行高（关键差异表）** `L20` — 对照英文：英文正文 16px / 1.5 就够；中文同样 16px 需要 1.7–1.8 才不压抑。直接沿用英文行高是中文排版最常见的错误。
  - **1.3 中文字体族栈（可直接用）** `L32` — css
  - **1.4 字重陷阱（中文特有）** `L57` — - 中文字体普遍缺 500（Medium）档，font-weight: 500 会被渲染成 400 或伪粗体（faux bold）——笔画糊、边缘脏。
  - **1.5 标点与避头尾（clreq 核心规则）** `L64` — 全角标点：中文标点占一个汉字宽（全角）。，。；：？！「」『』（）《》 等。
  - **1.6 行长（中文按字数算）** `L102` — 换算：中文 1 字 ≈ 2 个西文字符宽，所以 max-width: 36em（英文标准）对中文约等于 36 字，在舒适区间内。但中文正文用 max-width: 40em 时行长约 40 字，已接近上限。
  - **1.7 竖排（了解即可）** `L112` — writing-mode: vertical-rl 支持中文竖排，但：
- **二、中文设计生态地图（平台怎么用、哪里有坑）** `L121`
  - **2.1 六个核心平台（用户指定清单）** `L123`
  - **2.2 补充平台（按需扩展）** `L134`
  - **2.3 检索策略（按需求类型直接跳）** `L146` — Dribbble 使用纪律（重要）：看到喜欢的 shot，问三个问题再决定要不要借鉴——
- **三、中文产品形态的四个特征（影响设计决策）** `L167` — 中后台 vs 消费级的分野：
- **四、中文排版自检清单（交付前逐条过）** `L182` — - [ ] 正文字号 ≥14px（内容页 ≥16px），行高 ≥1.6

### `references/component-libraries.md` · 组件库与设计 GitHub 地图 — Component Libraries
_37 行 · 快照 2026-10-29 · 3 节_

- **元素覆盖矩阵** `L5`
- **选型规则** `L24` — - 要"复制类名就用"（无 JS 依赖）：HyperUI TailGrids daisyUI Meraki UI
- **维护协议** `L34` — - 快照：2026-10-29。任何条目链接失效或用户报告质量下降时：先 GitHub API 复核该库（star/推送/许可），再决定降级或替换，并在本文件更新快照日期。

### `references/dataviz.md` · 数据可视化规范 · Data Visualization
_376 行 · 快照 2026-10-31 · 26 节_

- **0. 四条总原则（AntV 官方，可直接引用）** `L8` — 交互三层（AntV）：数据获取 → 信息加工 → 知识流转；口诀「概览第一，聚焦过滤，再按需查看详情」。做仪表盘时按这个顺序设计，不要一上来就给明细表。
- **1. 先判关系，再选图形（FT Visual Vocabulary 九类）** `L21` — FT 的核心主张：按"你要表达什么关系"组织，而不是按"你会画什么图"组织。选图前先回答"我想让读者看到什么关系"。
- **2. 图表选型决策树（30 秒版）** `L43` — 数据里有几个变量？
- **3. 色板：三类用途，不许混用** `L76` — 这是数据可视化里最容易翻车的一环。 三类色板解决三个不同问题，混用等于撒谎：
  - **3.1 分类色板 · Carbon 14 色（IBM，精确值，必须按序取用）** `L86` — 原文规定："The colors of this palette should be applied in sequence strictly as described below." —— 顺序经专门编排以最大化相邻色对比度。不要自己挑颜
  - **3.2 分类色板 · AntV 默认 10 色（中文项目常用，G2 v5 源码实测）** `L102` — #5B8FF9 #5AD8A6 #5D7092 #F6BD16 #6F5EF9
  - **3.3 顺序色板（连续值 / 热力 / 地图）** `L114` — 规则（Carbon 原文）：浅色主题下最深 = 最大；深色主题下最浅 = 最大。这条搞反是热力图最常见的错误。
  - **3.4 发散色板（同比增减、偏离基准）** `L126` — 铁律：中点必须是中性色或极浅色，两侧必须阶数对称、明度对称。中点不对称 = 暗示偏移不存在。
  - **3.5 状态色（警报）** `L135` — #da1e28 错误/危险 ｜ #ff832b 严重警告 ｜ #f1c21b 常规警告 ｜ #198038 正常/成功（Carbon 精确值）
  - **3.6 选色纪律（六条）** `L141` — 1. 先问有几个类别，再决定用哪种色板；不要先选好看的颜色再套数据。
- **4. 坐标轴铁律（含 G2 精确数值）** `L152`
  - **4.1 三条不可违反的** `L154` — 1. 柱状图 / 面积图 / 堆叠图必须从 0 开始。截断基线等于用长度撒谎。折线图可以截断（趋势比绝对值重要），但必须在轴上留截断符号或直接标注首末值。
  - **4.2 数值规格（AntV G2 v5 light 主题，源码实测，可直接抄）** `L160`
  - **4.3 布局规则** `L173` — - 网格线只保留横向（柱状/折线）。纵向网格线删掉——它和柱子重复。
- **5. 图例、标签、注释** `L184` — 信息优先级：直接标注 图例 Tooltip。每往下一级，读者多一次视线跳跃。
- **6. 中文数字与单位（中文项目必做）** `L204` — 中文图表字号比英文 +1px：轴标签 12px 在中文里偏小，建议 12–13px，下限 11px；数据标签 13–14px。中文字宽等宽，同样的 12px 中文比英文"重"，行高需 1.4–1.5（英文 1.2 即可）。
- **7. 仪表盘布局** `L223` — 结构顺序按读者的决策路径，不按数据表顺序：结论（KPI）→ 趋势（折线）→ 结构（占比/排名）→ 明细（表格）。
- **8. 图表动效（与 motion-system.md 的关系）** `L242` — 图表是唯一被允许突破 400ms 上限的场景——因为它不阻塞用户输入，且数据过渡需要可读时间。但这条豁免仅限"图表入场与数据更新"。
- **9. 可访问性（图表最容易漏的一节）** `L265` — WCAG 2.2 SC 1.4.11 非文本对比度：理解内容所必需的图形对象，与相邻颜色对比 ≥ 3:1。原文强调 3:1 是阈值，2.999:1 不通过，不可四舍五入。
- **10. 反模式清单（逐条给改法）** `L289`
  - **10.1 图形与比例** `L291` — 1. 柱状图不从 0 开始 → 改回 0 基线；若差异确实小，改用点图/棒棒糖图（可不从 0）。
  - **10.2 双 Y 轴（有立场，但要说清条件）** `L299` — 默认禁用。Datawrapper 2018 原文的核心论证仍然成立：两个轴的比例是任意的，读者会默认按单轴折线图去读，从而得出"两条线同速增长"这类错误结论（研究：Isenberg et al. 2011 对 15 人的实验显示双轴图在准确
  - **10.3 表达与标注** `L315` — 7. Y 轴刻度不整或跳变（0、3、6、9）→ 改 0、25、50、75、100。
- **11. 实现选型（GitHub API 实测 2026-10-31）** `L325` — 选型规则：
- **12. 自检 12 项（图表交付前逐条过）** `L349` — 1. 关系对了吗：图形是否匹配 §1 的关系类型？（不是"我觉得好看"）
- **13. 素材与出处** `L366` — - FT Visual Vocabulary — 九类数据关系与图形选型（本文件 §1 骨架，多语言版含简体中文）

### `references/design-md-format.md` · DESIGN.md 规范与品牌 DNA — Design Spec
_190 行 · 快照 2026-10-29 · 13 节_

- **一、DESIGN.md 是什么，为什么值得作为交付物** `L10` — 定义：一份纯 Markdown 的设计系统文档，放在项目根目录，AI 编码 agent 读了就能生成风格一致的 UI。
- **二、九章骨架（照此结构写，不增不减）** `L26` — 篇幅参考：一份合格 DESIGN.md 约 230–370 行（本地 54 份实测区间）。低于 150 行通常不够具体。
- **三、54 品牌 DNA 速查** `L44` — 用途：用户说"做成 XX 那种感觉"时，先在此定位气质，再读对应文件取精确数值。
  - **3.1 AI 与机器学习（12）** `L49`
  - **3.2 开发者工具与平台（14）** `L66`
  - **3.3 基础设施与 API（6）** `L85`
  - **3.4 生产力与协作（10）** `L96`
  - **3.5 金融科技（4）** `L111`
  - **3.6 消费品牌与巨头（8）** `L120` — ---
- **四、项目类型 → 风格推荐（选风格先看场景）** `L135` — 兜底规则：用户说"随便/你决定"→ 默认 Vercel（干净、现代、专业，最不易出错），并明确告知"我先用 Vercel 风格（简约黑白），不喜欢随时换"。
- **五、何时把 DESIGN.md 作为交付物** `L153` — 产出流程：
- **六、写 DESIGN.md 的四条纪律** `L173` — 1. 数值优先于形容词。"圆角 10px，全站统一" 优于 "圆角柔和"。
- **七、与本技能其他文件的衔接** `L182`

### `references/design-tokens.md` · 设计 Token 体系 — Design Tokens（深度蒸馏）
_231 行 · 快照 2026-10-29 · 13 节_

- **一、三层架构（唯一正确的组织方式）** `L9` — 铁律：
- **二、Ant Design 数值体系（中文语境最完整的一套）** `L26` — Ant Design 的字体方案基于「动态秩序」原则，结合自然对数与音律规则推导；布局基于柯布西耶模度思想。以下是可直接抄用的数值。
  - **2.1 色彩** `L30` — 中性色的透明度实现（浅色 / 深色双值）：
  - **2.2 字体** `L56` — 字体族栈（直接可用）：
  - **2.3 布局与间距** `L83` — 两种适配范式：
  - **2.4 圆角与阴影（跨体系通用建议）** `L99` — 阴影三层足够：sm 悬停微起 / md 卡片默认 / lg 弹层浮起。阴影与边框二选一，同时用会显脏。
- **三、三大体系对比（选哪套取决于产品语境）** `L112` — 选择规则：
- **四、中文设计系统矩阵（GitHub 验证 · 2026-10-29）** `L133` — 选型规则：
- **五、Token 输出格式（三种落地形态）** `L156`
  - **5.1 CSS 变量（推荐，最通用）** `L158` — css
  - **5.2 Tailwind 配置（工程侧）** `L183` — js
  - **5.3 JSON（给设计工具 / agent 用）** `L199` — json
- **六、常见错误（逐条对照）** `L218`

### `references/inspiration.md` · 灵感与阅读 — Inspiration
_153 行 · 快照 2026-10-29 · 4 节_

- **用法** `L5` — 按需求关键词定位：做 Web/UI 视觉调研 找 Galleries 里对应领域的站点；想 系统提升审美与方法论 读 Reading 里的小节。
- **Galleries (103)** `L9` — - 60fps — Recordings of interfaces that move well.
- **Reading (33)** `L115` — - Interface Craft — Articles exploring modern digital interface craftsmanship.
- **Other (1)** `L151` — - gaki — GAKI 的个人空间：想法、实验、与 AI 一起动手的过程，以及逐渐成形的作品。

### `references/knowledge-map.md` · 设计能力知识路线图 — Knowledge Map（L0→L4）
_222 行 · 快照 2026-10-29 · 32 节_

- **全景：五级台阶与对应产出** `L9` — 级别不是资历，是任务类型。 同一份工作里会反复上下：做落地页是 L0→L1→L2→L3 直落；被问"这版好不好"是 L4 单点。
- **L0 · 视觉感知：先治"看不出来"** `L23` — 为什么排第一：绝大多数"设计不好"不是技法问题，是看不出问题。没有分辨力，学再多规范也只是套模板。
  - **核心概念（4 个）** `L27` — 1. 层级（Hierarchy）——一屏只有一个主角。判断法：眯眼看，还能分清主次吗？
  - **必读材料** `L33` — - 本技能 portfolios.md：选 5 个作品集，逐站回答"它的主角是谁、靠什么手法突出"
  - **练习（必须落成文字）** `L40` — 取任意两个同类站点（如两个 SaaS 首页），写 300 字对比：
  - **验收标准** `L45` — 能对任何界面在 60 秒内说出：主角、视觉路径、最弱的一环。做不到就还在 L0。
- **L1 · 界面语汇：从"感觉"到"构型"** `L50` — 为什么：设计师和普通人的差别不是审美，是知道有几种做法。只会一种做法的人，遇到不合适的场景就只能硬套。
  - **核心概念** `L54` — 1. 构型谱系——每个元素有 4–6 种主流构型，各有适用场景（见 patterns.md）
  - **必读材料** `L60` — - 本技能 patterns.md：12 类元素，每类「构型 → 参数 → 变体 → 速配 → 常见错误」
  - **练习** `L67` — 任选一个元素（导航栏/定价表/表单），产出 4–6 个构型变体的真实渲染设计板（不是截图、不是链接）。
  - **验收标准** `L70` — 给一个元素 + 场景（"文档站导航"），能直接说出该选哪种构型、为什么、参数取多少。答"看情况"就是没学会。
- **L2 · 系统秩序：从"页面"到"系统"** `L75` — 为什么：单个页面好看靠手艺，一整套产品好看只能靠系统。这一步是从"做图"跨到"做设计"。
  - **核心概念** `L79` — 1. 三层 token 架构：base（原始值）→ semantic（语义角色）→ component（组件专用）
  - **必读材料** `L86` — - 本技能 design-tokens.md：Ant Design 数值体系全量蒸馏 + 三大体系对比 + 中文设计系统矩阵
  - **练习** `L94` — 给一个虚构产品写出完整 token 表：12 个语义色 + 5 档字阶 + 8 档间距 + 3 档圆角 + 3 层阴影，并注明每项使用场景。
  - **验收标准** `L97` — token 表能直接翻译成 CSS 变量且无歧义；同一份表能同时生成浅色与深色两套。
- **L3 · 工程落地：从"稿"到"跑起来"** `L102` — 为什么：设计的最终形态是运行中的界面。不懂实现的约束，就会设计出做不出来的东西（或成本高 10 倍的东西）。
  - **核心概念** `L106` — 1. 技术栈匹配：React/Vue/纯 HTML，选库先看栈再看元素覆盖
  - **必读材料** `L113` — - 本技能 component-libraries.md：14 库元素覆盖矩阵 + 选型规则 + 维护协议
  - **练习** `L120` — 把一个 L1 设计板里的变体，用选定组件库实现为可运行页面，并跑一次 Lighthouse。
  - **验收标准** `L123` — 交付物能跑、能响应式、Lighthouse 可访问性 ≥ 90。
- **L4 · 判断与品味：在冲突约束下取舍** `L128` — 为什么：真实项目里需求永远自相矛盾（"要高级又要热闹""信息多又要留白"）。L4 的能力是给立场，不是列选项。
  - **核心概念** `L132` — 1. 约束识别：分清"硬约束"（品牌色、法务文案、性能）与"软偏好"（个人喜好）
  - **必读材料** `L139` — - Ant Design 设计价值观：自然/确定性/意义感/生长性——评价设计的内在标准
  - **练习** `L145` — 拿一个真实需求，写一份可行性 × 美观性预判：3 条风险、每条给缓解方案、最后给"做什么/不做什么/先做什么"。
  - **验收标准** `L148` — 结论有立场、有理由、有代价说明；被反驳时能说清"我为什么仍这样判断"。
- **三条专题支线（可与主线并行）** `L153`
  - **支线 A · 中文场景（中文项目必走）** `L155` — 中文不是"英文换字"。字号要 +1~2px、行高要 1.6–1.8、标点全角、避头尾、中英混排要间距。
  - **支线 B · 数据可视化** `L159` — - 原则：准确 / 有效 / 清晰 / 美（AntV 四原则）；Data-ink Ratio 最大化
  - **支线 C · 动效（界面"活"起来的那一层）** `L168` — - 三种合法用途：反馈 / 引导（空间关系、过程）/ 个性（每页 ≤1 处）
- **学习节奏（可持续，不靠意志力）** `L178` — 最后一条最重要：能看出自己旧作的毛病，是能力增长唯一可靠的证据。
- **能力自测（20 条，做到 ≥15 条即达 L2+）** `L192` — L0

### `references/motion-system.md` · 动效与微交互系统 — Motion System（深度蒸馏）
_348 行 · 快照 2026-10-30 · 21 节_

- **1. 决策三问：先判该不该动** `L10` — 动效只有三种合法用途（说不出属于哪一种，就删掉）：
- **2. 曲线：语义决定曲线，不是审美决定** `L30` — 核心规则（90% 的人搞反的一条）：
  - **2.1 四体系精确值对照（可直接抄进 CSS）** `L39` — Ant 的反向曲线：motionEaseInBack cubic-bezier(0.71, -0.46, 0.88, 0.6)（先回撤再走），慎用，仅适合"取消/撤销"的语义。
  - **2.2 立场：项目默认用哪套** `L53` — 给一个 3 曲线最小集就够，不要引入 12 档：
- **3. 时长：按距离和面积取，不按心情取** `L69` — 原理：位移距离越长、面积越大，人眼需要的追踪时间越长，时长必须递增（Carbon 原话：the larger the change in distance or size, the longer the animation）。但上限 400
  - **3.1 四体系时长刻度** `L73` — M3 的 700–1000ms 只用于不涉及用户输入的环境型转场。任何由点击触发的动画超过 400ms 都是错的。
  - **3.2 距离 → 时长（经验法则，按 Carbon 的非线性刻度换算）** `L87` — 微交互的硬指标（Carbon 评估清单原文）：用户输入触发的微交互应落在 90–120ms，且用 ease-out。
- **4. 场景速查表（直接取值，不用再算）** `L101` — 覆盖场景：hover / 按钮按压 / 焦点环 / 开关 Toggle / 复选框 / Tooltip / 下拉菜单 Popover / 弹层（Modal、Dialog）/ 抽屉 Drawer / Toast 提示 / 手风琴 / Tab 
- **5. 编排：多个元素一起动时的顺序** `L131` — 1. 层级优先：重要元素先动、动得更久；次要元素合并成一组同时动（Fluent：次要元素同步可避免注意力分散）。
- **6. 物理感：什么时候用弹簧，什么时候用曲线** `L141` — 建议参数（建议值，非官方）：UI 常规 stiffness 300–500 / damping 30–40 / mass 1；需要弹性时降 damping 到 20–26；永远设置最大时长兜底（如 restDelta 0.01 + 超时 6
- **7. 实现：可直接抄的四段代码** `L155`
  - **7.1 动效 token（贴进 :root）** `L157` — css
  - **7.2 从 display:none 进入的弹层（@starting-style）** `L179` — 原生 dialog / popover 从 display:none 变可见时，直接写 transition 不会触发动画，必须配 @starting-style + transition-behavior: allow-discrete：
  - **7.3 共享元素过渡（View Transitions）** `L200` — 同一元素在 A 视图与 B 视图都标同一个名字，浏览器自动做"从旧位置尺寸平滑过渡到新位置尺寸"：
  - **7.4 滚动驱动动画（无 JS）** `L221` — css
- **8. 性能与降级** `L238` — 只动这两个属性：transform（含 translate / scale / rotate）与 opacity——它们走合成层，不触发布局与重绘。
  - **8.1 prefers-reduced-motion 三档降级（必须做）** `L257` — WCAG 依据：2.3.3 Animation from Interactions（AAA）——交互触发的动效必须可关闭（除非是功能必需）；2.2.2 Pause, Stop, Hide（A）——超过 5 秒的自动运动内容必须可暂停；2.3
- **9. 中文场景与小程序** `L285` — ---
- **10. 验收清单（10 条，交付前逐条过）** `L298` — 1. 每个动效都能说出属于反馈 / 引导 / 个性中的哪一种？说不出的删了没？
- **11. 反模式（命中即扣分）** `L313` — - 从 scale(0) 弹窗、从 opacity:0 + scale(0.5) 做卡片——真实物体不会从无到有地放大。
- **12. 素材与出处** `L326` — 规范原文（本轮实测）

### `references/patterns.md` · 元素设计模式图鉴 — Patterns（深度蒸馏）
_120 行 · 快照 2026-10-29 · 13 节_

- **导航栏 Navbar** `L7` — 构型谱系（选 1 种，不混用）：
- **首屏 Hero** `L25` — 构型谱系：
- **功能特性区 Features** `L41` — 构型谱系：3 列网格（最常用）｜2×2 大卡｜左右交替图文｜密集列表（每行 icon+标题+一句话）。
- **CTA 区块** `L49` — 构型谱系：通栏色块（强调色底+白字居中）｜描边卡片（浅底+边框+左右布局）｜全宽渐变（每页 ≤1 处）。
- **页脚 Footer** `L57` — 构型谱系：4 列链接 + 底条（产品/资源/公司/法务）｜精简单行（logo+少量链接+版权，作品集）｜大字标语式（品牌宣言压底）｜站点地图式（SaaS 大站）。
- **定价表 Pricing** `L65` — 构型谱系：3 档横排（推荐档抬高/描边强调）｜2 档对照+企业档横条｜月/年切换（年付标 -20% 类折扣）。
- **登录/注册 Auth** `L73` — 构型谱系：居中卡片（≤400px，logo+标题+表单+社交登录+切换链接）｜左品牌右表单分屏（品牌侧放图/标语）｜全屏极简（只有表单）。
- **仪表盘 Dashboard** `L81` — 构型谱系：侧边导航 F + 顶栏 + 内容区（默认）｜顶部导航 + 卡片网格（轻量工具）｜三栏（列表+详情+属性面板，管理类）。
- **卡片 Card** `L89` — 构型谱系：竖版图文（封面 16:9 + 标题 + 摘要）｜横版列表行（缩略图 48–64px + 双行文字）｜数据卡（数值+标签+趋势）｜可交互卡（hover 抬升 2px + 阴影加深）。
- **表单 Form** `L97` — 关键参数：标签在输入框上方 14px；输入框高 44–48px；字段间距 24px；帮助文字 12–13px 灰字在框下方；提交按钮右上或底部全宽。
- **移动端底部导航 Tab Bar** `L104` — 关键参数：高度 56–64px + 安全区内嵌；3–5 项，图标 24px + 10–11px 标签；当前项用强调色，其余灰；点击目标 ≥44×44px。
- **落地页版式骨架（整页组装）** `L111` — 标准顺序（SaaS，可裁剪）：导航(A) → Hero(A/B) → 社会证明 logo 墙 → Features(3 列) → 用法演示/截图 → 定价(3 档) → 常见问题(手风琴) → CTA(通栏) → Footer(4 列)。
- **反模式速查（任何元素通用）** `L118` — 纯灰 #808080 大面积使用｜字号不用阶梯｜间距非 4/8 倍数｜同页两种圆角语言｜标题靠彩色而不是字号字重分层｜动效无反馈/引导/个性用途｜一行放不下还想塞｜对比度 <4.5:1 的正文。

### `references/portfolios.md` · 作品集 — Portfolios
_194 行 · 快照 2026-10-29 · 8 节_

- **用法** `L5` — 这是审美校准素材：当 agent 需要判断「什么是好的界面」时，参考这些一线从业者的作品构成方式；也用于给用户推荐可对标的作品集风格。
- **Founders & Makers (17)** `L9` — - Emil Kowalski — Creator of Sonner, Vaul, and animations.
- **Design (41)** `L29` — - Rauno Freiberg — Author of Interaction Guidelines at Vercel.
- **Development (30)** `L73` — - Sarah Drasner — Engineering leader and web animation author.
- **Creative Development (13)** `L106` — - Jhey Tompkins — Creative developer building playful CSS experiments.
- **Design Engineering (55)** `L122` — - Arlan Marat — Design engineer from Waymo and Yandex.
- **Studios (4)** `L180` — - Unlimited Studio — Independent studio crafting bespoke digital identities.
- **Other (6)** `L187` — - Krutik Raut — Creative portfolio of Krutik - Designer and Developer who makes pixels behave

### `references/resources.md` · 设计资源 — Resources
_225 行 · 快照 2026-10-29 · 5 节_

- **用法** `L5` — - Components：找可复用 UI 组件库与设计系统参考
- **Type & Colour (14)** `L14` — - Fontshare（免费） — High-quality professional fonts free for commercial use.
- **Components (128)** `L31` — - ForgeUI（免费+付费） — Animated React and Tailwind components and templates.
- **Motion & 3D (26)** `L162` — - Three.js（免费） — JavaScript 3D library rendering WebGL scenes.
- **Icons (33)** `L191` — - Lucide（免费） — Community-maintained Feather Icons fork with thousands of glyphs.

### `references/tools.md` · 制作工具 — Tools
_182 行 · 快照 2026-10-29 · 7 节_

- **用法** `L5` — - Development：前端/开发工具
- **Development (40)** `L13` — - SVGOMG（免费） — Web GUI to optimize and clean SVG files.
- **Capture & Media (33)** `L56` — - Squoosh — Browser image compression with visual comparisons.
- **Design & Canvas (17)** `L92` — - Vessa — Publish brand guidelines as live pages.
- **Productivity & Desktop (24)** `L112` — - Butterfly — Team building the Pond Linux operating system.
- **AI & Agents (38)** `L139` — - Dray（免费） — Unified desktop workspace managing coding agents.
- **Other (1)** `L180` — - ASCII Magic — Free ASCII art generator and image & video effects studio: ASCII, pixel art, voxel, mosaic, halftone,…

### `memory/design-log.md` · 设计记忆（自我成长档案）
_77 行 · 快照 — · 8 节_

- **当前画像（规则层，命中 ≥2 次的稳定偏好）** `L6` — （暂无——随使用积累）
- **匹配与反馈日志（追加层，只增不改）** `L11`
- **YYYY-MM-DD · 需求一句话** `L14` — - 需求：载体/调性/明暗
- **2026-10-28 · 开发者工具深色落地页（自测）** `L21` — - 需求：落地页 / 深色 / 开发者工具；调性默认 极简+专业+冷静
- **2026-10-29 · 元素级精准匹配升级（v3）** `L27` — - 需求：导航栏等元素提示词应返回设计图本体而非设计网站链接
- **2026-10-29 · v4 系统化与中文场景补齐（每日升级 #1）** `L33` — - 需求：每日深蒸馏 Design-related websites.txt + 补充设计站/GitHub 仓库，产出知识路线与资料，自动推 GitHub 并更新 README
- **2026-10-30 · 动效系统 + 记忆树与检索（每日升级 #2）** `L46` — - 需求：每日深蒸馏（本轮按用户补充要求：记忆树、快捷搜索查询、自我进化、自动推送）
- **2026-10-31 · 数据可视化规范（每日升级 #3）** `L61` — - 需求：每日深蒸馏（记忆树 / 快捷检索 / 自我进化 / 自动推送 + 更新 README）

## 三、主题索引（章节标题 → 位置）

- **0. 四条总原则（AntV 官方，可直接引用）** → `references/dataviz.md` L8
- **1. 先判关系，再选图形（FT Visual Vocabulary 九类）** → `references/dataviz.md` L21
- **1. 决策三问：先判该不该动** → `references/motion-system.md` L10
- **10. 反模式清单（逐条给改法）** → `references/dataviz.md` L289
- **10. 验收清单（10 条，交付前逐条过）** → `references/motion-system.md` L298
- **11. 反模式（命中即扣分）** → `references/motion-system.md` L313
- **11. 实现选型（GitHub API 实测 2026-10-31）** → `references/dataviz.md` L325
- **12. 素材与出处** → `references/motion-system.md` L326
- **12. 自检 12 项（图表交付前逐条过）** → `references/dataviz.md` L349
- **13. 素材与出处** → `references/dataviz.md` L366
- **2. 图表选型决策树（30 秒版）** → `references/dataviz.md` L43
- **2. 曲线：语义决定曲线，不是审美决定** → `references/motion-system.md` L30
- **2026-10-28 · 开发者工具深色落地页（自测）** → `memory/design-log.md` L21
- **2026-10-29 · v4 系统化与中文场景补齐（每日升级 #1）** → `memory/design-log.md` L33
- **2026-10-29 · 元素级精准匹配升级（v3）** → `memory/design-log.md` L27
- **2026-10-30 · 动效系统 + 记忆树与检索（每日升级 #2）** → `memory/design-log.md` L46
- **2026-10-31 · 数据可视化规范（每日升级 #3）** → `memory/design-log.md` L61
- **3. 时长：按距离和面积取，不按心情取** → `references/motion-system.md` L69
- **3. 色板：三类用途，不许混用** → `references/dataviz.md` L76
- **4. 场景速查表（直接取值，不用再算）** → `references/motion-system.md` L101
- **4. 坐标轴铁律（含 G2 精确数值）** → `references/dataviz.md` L152
- **5. 图例、标签、注释** → `references/dataviz.md` L184
- **5. 编排：多个元素一起动时的顺序** → `references/motion-system.md` L131
- **6. 中文数字与单位（中文项目必做）** → `references/dataviz.md` L204
- **6. 物理感：什么时候用弹簧，什么时候用曲线** → `references/motion-system.md` L141
- **7. 仪表盘布局** → `references/dataviz.md` L223
- **7. 实现：可直接抄的四段代码** → `references/motion-system.md` L155
- **8. 图表动效（与 motion-system.md 的关系）** → `references/dataviz.md` L242
- **8. 性能与降级** → `references/motion-system.md` L238
- **9. 中文场景与小程序** → `references/motion-system.md` L285
- **9. 可访问性（图表最容易漏的一节）** → `references/dataviz.md` L265
- **AI & Agents (38)** → `references/tools.md` L139
- **CTA 区块** → `references/patterns.md` L49
- **Capture & Media (33)** → `references/tools.md` L56
- **Components (128)** → `references/resources.md` L31
- **Creative Development (13)** → `references/portfolios.md` L106
- **Design & Canvas (17)** → `references/tools.md` L92
- **Design (41)** → `references/portfolios.md` L29
- **Design Engineering (55)** → `references/portfolios.md` L122
- **Development (30)** → `references/portfolios.md` L73
- **Development (40)** → `references/tools.md` L13
- **Founders & Makers (17)** → `references/portfolios.md` L9
- **Galleries (103)** → `references/inspiration.md` L9
- **Icons (33)** → `references/resources.md` L191
- **L0 · 视觉感知：先治"看不出来"** → `references/knowledge-map.md` L23
- **L1 · 界面语汇：从"感觉"到"构型"** → `references/knowledge-map.md` L50
- **L2 · 系统秩序：从"页面"到"系统"** → `references/knowledge-map.md` L75
- **L3 · 工程落地：从"稿"到"跑起来"** → `references/knowledge-map.md` L102
- **L4 · 判断与品味：在冲突约束下取舍** → `references/knowledge-map.md` L128
- **Motion & 3D (26)** → `references/resources.md` L162
- **Other (1)** → `references/inspiration.md` L151 · `references/tools.md` L180
- **Other (6)** → `references/portfolios.md` L187
- **Productivity & Desktop (24)** → `references/tools.md` L112
- **Reading (33)** → `references/inspiration.md` L115
- **Studios (4)** → `references/portfolios.md` L180
- **Type & Colour (14)** → `references/resources.md` L14
- **YYYY-MM-DD · 需求一句话** → `memory/design-log.md` L14
- **一、DESIGN.md 是什么，为什么值得作为交付物** → `references/design-md-format.md` L10
- **一、三层架构（唯一正确的组织方式）** → `references/design-tokens.md` L9
- **一、中文排版：为什么不是"英文换字"** → `references/chinese-design.md` L10
- **七、与本技能其他文件的衔接** → `references/design-md-format.md` L182
- **三、54 品牌 DNA 速查** → `references/design-md-format.md` L44
- **三、三大体系对比（选哪套取决于产品语境）** → `references/design-tokens.md` L112
- **三、中文产品形态的四个特征（影响设计决策）** → `references/chinese-design.md` L167
- **三条专题支线（可与主线并行）** → `references/knowledge-map.md` L153
- **二、Ant Design 数值体系（中文语境最完整的一套）** → `references/design-tokens.md` L26
- **二、中文设计生态地图（平台怎么用、哪里有坑）** → `references/chinese-design.md` L121
- **二、九章骨架（照此结构写，不增不减）** → `references/design-md-format.md` L26
- **五、Token 输出格式（三种落地形态）** → `references/design-tokens.md` L156
- **五、何时把 DESIGN.md 作为交付物** → `references/design-md-format.md` L153
- **仪表盘 Dashboard** → `references/patterns.md` L81
- **元素覆盖矩阵** → `references/component-libraries.md` L5
- **全景：五级台阶与对应产出** → `references/knowledge-map.md` L9
- **六、写 DESIGN.md 的四条纪律** → `references/design-md-format.md` L173
- **六、常见错误（逐条对照）** → `references/design-tokens.md` L218
- **功能特性区 Features** → `references/patterns.md` L41
- **匹配与反馈日志（追加层，只增不改）** → `memory/design-log.md` L11
- **卡片 Card** → `references/patterns.md` L89
- **反模式速查（任何元素通用）** → `references/patterns.md` L118
- **四、中文排版自检清单（交付前逐条过）** → `references/chinese-design.md` L182
- **四、中文设计系统矩阵（GitHub 验证 · 2026-10-29）** → `references/design-tokens.md` L133
- **四、项目类型 → 风格推荐（选风格先看场景）** → `references/design-md-format.md` L135
- **学习节奏（可持续，不靠意志力）** → `references/knowledge-map.md` L178
- **定价表 Pricing** → `references/patterns.md` L65
- **导航栏 Navbar** → `references/patterns.md` L7
- **工作流：接到任何设计任务时按此执行** → `SKILL.md` L39
- **当前画像（规则层，命中 ≥2 次的稳定偏好）** → `memory/design-log.md` L6
- **用法** → `references/inspiration.md` L5 · `references/portfolios.md` L5 · `references/resources.md` L5 · `references/tools.md` L5
- **登录/注册 Auth** → `references/patterns.md` L73
- **移动端底部导航 Tab Bar** → `references/patterns.md` L104
- **维护协议** → `references/component-libraries.md` L34
- **能力自测（20 条，做到 ≥15 条即达 L2+）** → `references/knowledge-map.md` L192
- **自我成长机制（用得越多越准）** → `SKILL.md` L220
- **自我进化机制（知识保鲜）** → `SKILL.md` L233
- **落地页版式骨架（整页组装）** → `references/patterns.md` L111
- **表单 Form** → `references/patterns.md` L97
- **边界与习惯** → `SKILL.md` L254
- **选型规则** → `references/component-libraries.md` L24
- **页脚 Footer** → `references/patterns.md` L57
- **首屏 Hero** → `references/patterns.md` L25

## 四、接线体检（自我进化的自检项）

✅ 所有 references 均已在 SKILL.md 接线。

> 每次升级新增参考文件后，必须同步在 SKILL.md 资产表 + 意图路由里加一行，否则等于没写。
