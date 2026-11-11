# AI / 生成式设计工具链：工作流、提示词、质量验收与合规边界

> 快照 2026-11-06 ｜ 22 节 ｜ 全部法规条款、日期、数值取自官方原文；仓库 star / 许可取自 GitHub REST API 实测（2026-11-06）。
>
> **一句话立场**：AI 是设计流程里的**产能层**，不是**判断层**。它能把 5 个方案变成 50 个，但不能替你决定哪个对；它能生成一张图，但不能替你承担这张图的版权与标识责任。本文件给的是**何时用、怎么验收、出事谁负责**的可执行口径，不是工具清单。

---

## 0. 与既有资产的分层（先判该读哪份）

| 你手上是什么问题 | 去哪份 | 本文件补什么 |
|---|---|---|
| 要一份给 AI 编码 agent 读的**风格约束文件** | `design-md-format.md`（DESIGN.md 九章骨架 + 54 品牌 DNA） | §7 把 DESIGN.md 定位成"一致性契约"，§8/§9 给生成它之前的 brief→prompt 转换 |
| 要把设计稿**交给开发** | `handoff-collaboration.md`（spec 9 字段 / 走查 / SemVer） | §14 生成→代码的衔接层、§15 prompt 版本化与 SemVer 对照 |
| 想找**有哪些 AI 工具** | `tools.md`（153 条链接清单）、`resources.md` | §13 五层地图 + **选型判据** + 实测维护状态 |
| 生成结果**不好看 / 有 AI 味** | 本文件 §11（AI Slop Test + 8 维 DO/DON'T） | 第 5 步原则、`impeccable` 风格判据 |
| 生成的界面**过不了无障碍 / 性能 / 文案 / 图表关** | 各自专项文件 | §12 把 12 类 AI 固有缺陷**逐条接回**既有专项，不重复抄规则 |
| 素材**能不能商用、要不要打标** | 本文件 §2–§6（全新，既有资产空白） | `brand-identity.md` §17 讲的是字体/商标授权，不覆盖 AI 生成物 |
| 要设计**AI 功能本身的界面**（生成按钮、置信度、纠错、反馈） | 本文件 §10（HAX 18 条**原则层**）+ `feedback-states.md`；**流式输出 / 聊天日志 / 生成式组件 / 混合界面 / 四档纠错链路** → `references/conversational-generative-ui.md`（链路层） | 原则层看 18 条，链路层看新资产；两处不重讲彼此内容，路由优先级不变 |

> **边界纪律**：本文件不重讲 WCAG 阈值、不断点数值、不 toast 时长、不色板 hex。需要数值去对应专项文件读，§12 是**索引**不是副本。副本必然漂移。

---

## 1. 判层：AI 在设计流程的五个位置，以及哪些活不该交出去

### 1.1 五层地图（每层都要有人工闸门）

| 层 | AI 做什么 | 人做什么（闸门） | 验收口径 |
|---|---|---|---|
| **L1 探索** | 扩写关键词、找类比、列风格候选、反例枚举 | 选定**一个**方向并写清理由 | 有没有出现"都对但没立场"的清单？有 = 无效 |
| **L2 生成** | 出变体（配色/构型/插画/文案/布局） | 按第 5 步原则**筛**，不是挑好看的 | 见 §11 AI Slop Test；每轮至少砍掉一半 |
| **L3 编辑** | 局部重绘、抠图、扩图、超分、去噪、改字 | 检查边缘/文字/手指/透视/品牌一致性 | 见 §12 缺陷表 + 印刷/长图的裁切检查 |
| **L4 代码化** | 截图→HTML、设计稿→组件、token 提取 | 语义 HTML、焦点态、状态覆盖、token 对齐 | 见 §14，落地后必须跑 §21.4 自动验收 |
| **L5 验收** | 跑脚本查对比度/alt/标识/空态、批量截图回归 | 判 P0–P3、签字 | 见 §20 自检 20 项 + `handoff-collaboration.md` §11 |

### 1.2 三类活**不要**交给 AI（给立场，不和稀泥）

1. **合规判断**：能不能商用、要不要打标、是否侵权、是不是 deepfake —— AI 会 confidently 编造法条。只认 §2–§5 的官方原文，并让法务复核。
2. **最终取舍**：两个方案在冲突约束下选哪个（L4 品味），需要知道业务目标、品牌上下文和用户；模型不知道，且**不能通过读代码库推断上下文**（`impeccable` 设计上下文纪律：Target audience / Use cases / Brand personality 必须由人给）。
3. **事实性内容**：真实数据、价格、人名、法条、引用、案例编号。AI 生成界面里最容易埋雷的是**编造的假数据被当成真数据上线**（§12.5）。

### 1.3 一条效率判据

> **AI 适合"生成可丢弃的选项"，不适合"生成不可回退的结论"。**
> 变体越多越好（可丢）；法规结论、品牌定位、上线签字、版权归属只能有一个（不可回退）。

---

## 2. 合规地基（一）：中国 AI 生成内容标识，是**法定义务**不是设计建议

### 2.1 三层法规栈（日期必须记准）

| 层级 | 文件 | 发布 / 施行 | 对设计的硬约束 |
|---|---|---|---|
| 部门规章 | 《生成式人工智能服务管理暂行办法》（七部门**令第 15 号**） | 2023-07-10 公布 / **2023-08-15 施行** | 第 4 条内容要求、第 7 条训练数据合法来源、第 12 条标识、第 11 条输入与用记录保护 |
| 部门规章 | 《人工智能生成合成内容标识办法》（**国信办通字〔2025〕2 号**，网信办/工信部/公安部/广电总局） | 2025-03-07 印发 / **2025-09-01 施行** | **显式 + 隐式双标识**、传播平台核验、用户主动声明、分发平台上架审核 |
| 强制性国标 | **GB 45438-2025**《网络安全技术 人工智能生成合成内容标识方法》 | 2025-02-28 发布（2025 年第 3 号国标公告）/ **2025-09-01 与办法同步实施** | 把标识做成可执行的**技术方法**：显式标识的时长/尺寸/位置、隐式标识的包含要素 |

> ⚠️ **口径纪律**：GB 45438-2025 的具体像素、字号、音频时长等数值，**本文件不臆造**。国标全文未逐字取得时，只写"标准规定了显式标识的时长、尺寸与隐式标识要素"（此结论来自网信办 2025-09-05 专家解读原文），落地时以国标全文 / 自评估检测平台为准。**拿不到原文的数值不写进资产**，这是本技能一贯纪律。

### 2.2 《标识办法》逐条翻译成设计动作（14 条，原文口径）

| 条 | 原文要点 |  designer 要做什么 |
|---|---|---|
| 第 2 条 | 适用于符合《算法推荐规定》《深度合成规定》《暂行办法》情形的**网络信息服务提供者** | 先判自己在不在适用范围；内部研发、未向境内公众提供服务的不适用（见《暂行办法》第 2 条第 3 款） |
| 第 3 条 | 生成合成内容 = 文本/图片/音频/视频/虚拟场景；标识分**显式**（可被用户明显感知）与**隐式**（文件数据中、不易感知） | 两套都要做，只放一行"AI 生成"角标 ≠ 合规 |
| 第 4 条 | 六类显式标识位置：文本起始/末尾/中间或交互界面；音频起始/末尾/中间或界面；**图片适当位置**；**视频起始画面 + 播放周边**（可加末尾/中间）；虚拟场景起始画面；其他场景按特点。**提供下载/复制/导出功能时，必须确保文件中含显式标识** | 这是最容易被设计漏掉的一条：**导出件也要带标识**。做"去水印/无标版"导出按钮前先看第 9 条 |
| 第 5 条 | 隐式标识写在**文件元数据**：生成合成内容属性信息、服务提供者名称或编码、内容编号等制作要素；**鼓励**加数字水印 | 元数据字段进导出管线；别让图片压缩/CDN 转码把元数据洗掉（§21.5 有检查脚本） |
| 第 6 条 | 传播平台四档处置：① 元数据有隐式标识 → 周边加显著提示"属于"；② 无标识但**用户声明** → "可能为"；③ 无标识无声明但检测到显式标识或生成痕迹 → **"疑似"**；④ 提供必要标识功能并提醒用户主动声明。前三档还要在元数据补传播要素（属性、传播平台名称/编码、内容编号） | 三档文案**不能混用**：属于 / 可能为 / 疑似，是法律语义差异，不是文案润色（`ux-writing.md` §2 的"说结果不说状态"在这里要让位于准确性） |
| 第 7 条 | **应用分发平台**在上架/上线审核时，要求 App 说明是否提供生成合成服务，并核验标识材料 | 做 App 上架材料的设计/产品，要准备标识方案说明与截图 |
| 第 8 条 | 服务提供者应在**用户服务协议**中明确标识方法、样式等规范，并提示用户阅读 | 标识样式要写进协议，不是藏在帮助中心 |
| 第 9 条 | 用户申请**不含显式标识**的内容时，可在协议明确用户标识义务与责任后提供，并**依法留存提供对象信息等日志不少于六个月** | "无标版"不是默认选项；要有协议 + 6 个月日志能力 |
| 第 10 条 | 用户发布时应**主动声明并使用标识功能**；**任何组织和个人不得恶意删除、篡改、伪造、隐匿标识**，不得提供此类工具/服务 | 设计师不能给用户提供"一键抹掉 AI 角标"的工具；裁剪导出把标识切掉同理 |
| 第 11 条 | 还应符合强制性国标 | 见 2.1 |
| 第 12 条 | 算法备案、安全评估时须提供标识相关材料 | 材料归档 |
| 第 14 条 | **2025-09-01 施行** | — |

### 2.3 设计交付清单（可直接贴进 spec）

- [ ] 生成结果在界面上有**显式标识**（文字/声音/图形，位置按第 4 条按载体分）
- [ ] **下载 / 复制 / 导出**三条路径都保留显式标识（第 4 条末款）
- [ ] 导出文件元数据含：生成合成内容属性、服务提供者名称或编码、内容编号（第 5 条）
- [ ] 转码/压缩/CDN 后抽检元数据仍在（§21.5）
- [ ] 用户发布流程有**主动声明**开关与标识功能（第 6 条第 4 项、第 10 条）
- [ ] 传播侧三档提示文案按"属于 / 可能为 / 疑似"分支（第 6 条）
- [ ] 标识样式写入用户协议（第 8 条）
- [ ] 若提供无标版：协议明确义务 + 日志留存 ≥6 个月（第 9 条）
- [ ] 不存在"抹除标识"的工具或快捷操作（第 10 条）

---

## 3. 合规地基（二）：中 / 欧 / 美三法域矩阵（出海产品必读）

| 维度 | 🇨🇳 中国 | 🇪🇺 欧盟 AI Act Art. 50 | 🇺🇸 美国 |
|---|---|---|---|
| 强制标识 | **显式 + 隐式双强制**（办法第 4/5 条 + GB 45438-2025） | 输出以**机器可读格式**标记、可被检测为人工生成或操纵（Art. 50(2)） | 无联邦通用强制内容标识；有**登记披露**义务 |
| 生效 | 2025-09-01 | **2026-08-02**（依 Art. 113） | USCO 登记指南 2023-03-16；Part 2 报告 2025-01-29 |
| 谁担责 | 生成服务提供者（源头）/ 应用分发平台（入口）/ 传播平台（流通）/ 用户（声明）——四段责任链 | **Provider** 做机器可读标记；**Deployer** 对 deepfake / 公共利益相关文本做披露 | 申请人在版权登记时披露 AI 生成部分 |
| 对交互界面 | 交互场景界面可承载显著提示（第 4 条） | Art. 50(1)：与人直接交互的 AI 系统须**告知对方在与 AI 交互**（除非对合理知情者显而易见）；Art. 50(5)：信息须在**最迟首次交互/首次暴露时**以清晰可区分方式提供，且**符合适用无障碍要求** | — |
| 豁免 | 未向境内公众提供服务的内部研发不适用（暂行办法第 2 条第 3 款） | ① **辅助性标准编辑**、或**不实质改变输入数据及其语义**（Art. 50(2) 末句）；② 执法用途；③ 艺术/创作/讽刺/虚构作品：披露限于"以不妨碍作品展示或欣赏的适当方式"；④ 公共利益相关文本若经**人工审校或编辑控制**且由自然人/法人承担编辑责任，可免披露（Art. 50(4)） | — |
| deepfake | 落入生成合成内容统一标识 | Art. 50(4) 部署者须披露内容经人工生成或操纵；deepfake 定义见 Art. 3(60) | USCO Part 1（2024-07-31）专门处理数字复制品，建议联邦立法 |
| 版权 | 尊重知识产权（暂行办法第 4(三)、第 7(二) 条） | 标识义务不解决版权归属 | **纯 AI 输出不可版权**（§4） |

### 3.1 三条落地判据

1. **按最严法域做一套，不要做三套**：中国要求显式（人读）+ 隐式（机读）双轨，欧盟要求机器可读标记，二者可共用同一份元数据管线；"符合中国双轨"是**充分条件**里的较强者。欧盟额外多的是"告知在与 AI 交互"与"deepfake 披露"，这是**界面层**要求，别只做文件层。
2. **Art. 50(5) 的"最迟首次交互"是设计时序硬约束**：把 AI 身份说明放在首次对话/首次生成之前，不能藏在设置页或帮助中心；且必须**满足无障碍要求**（回到 `accessibility.md`：读屏可读、对比度、焦点可达）。
3. **"辅助性标准编辑"豁免别乱用**：裁切、调色、压缩这类不实质改变输入语义的操作可豁免；**用生成模型重绘、扩图、换脸、改写文案**不是辅助编辑，是生成/实质改变。判不准时按不豁免处理。

> ⚠️ **本矩阵是工程判据不是法律意见**；具体产品上线前由法务确认适用主体与行业特别规定（《暂行办法》第 2 条第 2 款：新闻出版、影视制作、文艺创作另有规定的从其规定）。

---

## 4. 裁决一：**提示词写得再细，也不构成作者身份**（本轮最重要的一条）

### 4.1 权威口径

美国版权局《Copyright and Artificial Intelligence, Part 2: Copyrightability》于 **2025-01-29** 发布。其官方解读（U.S. Copyright Office / Library of Congress 博客，2025-02-06）原文结论：

> "the outputs of generative AI can be protected by copyright **only where a human author has determined sufficient expressive elements**. This can include situations where a human-authored work is perceptible in an AI output or a human makes creative arrangements or modifications of the output, **but not the mere provision of prompts**."

配套事实：
- 2023-08-30 发出 Notice of Inquiry，收到 **超过 10,000 条**意见，其中约**一半**讨论可版权性；绝大多数认为现行法足够、完全由 AI 生成的材料不可版权。
- 官方立场："existing principles of copyright law are flexible enough"；**不建议为 AI 输出额外立法保护**。
- **用 AI 辅助创作 / 在人类作品中含 AI 生成材料，不因此丧失可版权性**。
- 报告分三部分：Part 1 Digital Replicas（2024-07-31）、Part 2 Copyrightability（2025-01-29）、Part 3 Generative AI Training（**2025-05-09 预发布版**，最终版无实质结论变化预期）。
- 另有一份独立的 **Copyright Registration Guidance for Works Containing AI-Generated Materials**（88 Fed. Reg. 16,190，2023-03-16）：登记含 AI 生成材料的作品须**披露并排除（disclaim）** AI 生成部分。

### 4.2 被纠正的常见说法

| ❌ 常见说法 | ✅ 正确口径 |
|---|---|
| "我写了 500 字提示词，这张图的版权归我" | **not the mere provision of prompts**。提示词是**指令**，不是表达；投入工时 ≠ 作者身份 |
| "用 AI 做的东西一律没有版权" | 错在另一头：人类作品在输出中**可感知**，或人类做了**创造性编排/修改**，该部分可保护；AI 只是工具时整作仍可版权 |
| "AI 生成物加进我的设计里，整张图就不能登记了" | 可登记，但须**披露并 disclaim** AI 生成部分；人类贡献部分仍受保护 |
| "买了会员/订阅 = 拿到版权" | 订阅给的是**服务使用条款**，不是著作权转让。看服务商 ToS 的 license 字段，与版权归属是两件事 |

### 4.3 设计侧的可执行结论：**留下可举证的创作链**

既然"人类决定了足够的表达元素"是保护门槛，交付时就要把这件事**留痕**：

1. **分层源文件**：保留 PSD / Figma / AI 工程文件，把 AI 输出放在独立图层并命名（如 `AI_bg_v3`），人类重绘/编排层单独可见。
2. **素材台账**：每个 AI 素材记录 ①生成工具与版本 ②提示词 ③生成日期 ④种子/参数 ⑤后续人工修改清单 ⑥使用位置。
3. **人工贡献写清**：不是"我用 AI 做了张图"，而是"AI 生成背景底纹 → 我裁切并重构构图、替换 3 处元素、重绘文字层、按品牌色阶重映射"。
4. **登记/维权材料包**：分层文件 + 台账 + 修改前后对照，才是能拿出手的证据；只有一张 PNG 和一段提示词，等于没有证据。
5. **商用别只看版权**：还要过肖像权、商标、字体授权（`brand-identity.md` §17）、素材库许可，以及 §2 的标识义务。

> **立场**：把 AI 输出当"素材"而不是"作品"。素材要能被追溯、被替换、被证明经过人的判断；作品才有资格谈保护。

---

## 5. 裁决二：**Content Credentials / 打了 AI 标 ≠ 版权清晰 ≠ 内容为真**

### 5.1 C2PA 到底断言什么

C2PA（Coalition for Content Provenance and Authenticity，Joint Development Foundation 项目）现行规范门户为 **2.5**（含 Content Credentials 规范、crJSON；Attestations 1.4、Soft Binding API 2.4、Explainer / Guidance / UX Recommendations 2.2、AI/ML 指南 2.3、Security 2.4）。核心概念：

- **Assertion**：*"A data structure which represents a statement about the asset"* —— 是**陈述**，不是已被证明的事实。
- **C2PA Manifest / Content Credential**：*"The set of information about the provenance of an asset consisting of one or more assertions that are digitally signed to ensure their authenticity and integrity."*
- **Hard binding** = cryptographic hashing（SHA2-256 + Merkle-tree-like 结构 + X.509 凭证签名），把 asset 与 Manifest 绑定 → **tamper-evident**。
- **Soft binding** = 隐形水印 / fingerprint lookup，用于 Manifest 被移除或未嵌入时仍能在云端找回。
- **Claim** 里只有 `created_assertions` 归属于 signer，`gathered_assertions` 不归属。
- 不依赖区块链。

### 5.2 它**不**断言什么（原文边界）

> "Content Credentials do not provide value judgments about whether a given set of provenance data is 'true', but instead merely whether the provenance information is well-formed and free from tampering, valid and trusted..."

> "provenance information alone cannot tell you whether the digital content is true, accurate or factual."

> "no assumption should be made about the trustworthiness of a particular asset purely based on its usage of Content Credentials."

其他明确限制：不是 misinformation 的万能解；**Unlike DRM, Content Credentials does not restrict user access or impose usage limitations**；核心规范不直接处理人或组织身份（身份是 extension，且有隐私影响）；规范全文未出现 `copyright` 一词；Authenticity 在 C2PA 里是**技术含义**——"a set of facts that can be cryptographically verified as not having been tampered with"，不是现实世界为真。

### 5.3 三个必须分开的概念（最容易混）

| 概念 | 回答的问题 | 谁给 |
|---|---|---|
| **内容标识**（中国 §2 / 欧盟 Art.50(2)） | 这是不是 AI 生成的？ | **法定义务**，由服务提供者/平台加 |
| **内容凭证 / 溯源**（C2PA Content Credentials） | 这份文件从哪来、被谁改过、有没有被篡改？ | **技术机制**，密码学完整性，不作真伪/权属判断 |
| **版权归属 / 商用授权** | 我能不能用、能不能独占、能不能维权？ | **法律 + 合同**，见 §4 与服务商 ToS |

> ⚠️ **三者互不替代**：一个文件可以**有**合规标识、**有** Content Credentials，却**没有**可用版权（纯 AI 输出）；也可以**有**人类充分创作（可版权）但**没打**法定标识（违规）。把"打了标"当成"可以商用"是本轮要消灭的误解。

### 5.4 中国隐式标识与 C2PA 的关系

- 中国第 5 条要求的是**文件元数据**中的生成合成内容属性信息 + 服务提供者名称/编码 + 内容编号；并**鼓励**数字水印。
- C2PA Manifest 可作承载这些字段的一种技术实现（它还定义了与 IPTC / XMP / EXIF 的 mapping），但**满足 C2PA ≠ 自动满足 GB 45438-2025**：字段口径、编码格式、显式标识位置与时长由国标规定，须按国标自评估。
- C2PA 的 soft binding（隐形水印）与中国"鼓励数字水印"方向一致，可一并设计，但**显式标识不能省**（第 4 条）。

---

## 6. AI 素材的来源与授权链

### 6.1 训练数据侧的法定要求（《暂行办法》第 7 条，原文五款）

提供者应当依法开展预训练、优化训练等训练数据处理活动：①使用**具有合法来源的数据和基础模型**；②涉及知识产权的**不得侵害他人依法享有的知识产权**；③涉及个人信息的取得同意或符合法定情形；④提高训练数据质量，增强真实性、准确性、客观性、多样性；⑤遵守《网安法》《数安法》《个保法》等。第 4 条另要求**尊重知识产权、商业道德**，提升透明度与生成内容准确性、可靠性，并不得侵害肖像权、名誉权、隐私权与个人信息权益。

> 设计师能做的不是审模型，而是**问供应商**：训练数据来源说明、是否有授权链、ToS 里的赔偿（indemnity）条款、是否保留输入用于训练。Four questions，没有答案就别进商业项目。

### 6.2 输入侧：别把客户的资产贴进外部模型

《暂行办法》第 11 条要求提供者**不收集非必要个人信息、不非法留存可识别使用者身份的输入信息和使用记录、不非法向他人提供**。对应到设计侧：

- 未公开的品牌 VI、未发布产品图、含真实用户数据的截图、合同/身份证/后台数据，**不进公共模型**（企业私有部署或明确不留存、不训练的条款下另议）。
- 上传前做脱敏：换假数据、换占位图、去掉人名与订单号。§12.5 的"编造数据"与这里是**两个方向**的风险：一个怕假数据上线，一个怕真数据外泄。
- 《暂行办法》第 2 条第 3 款明确：**行业组织、企业、教育和科研机构研发应用 AI 但未向境内公众提供服务的，不适用本办法** —— 内部工具与对外服务要分开评估，别一刀切。

### 6.3 授权四查（与 `brand-identity.md` §17 串联）

1. **模型/服务 ToS**：商用是否允许、是否要求署名、是否有赔偿条款、输出权利归谁（注意 §4：ToS 给的是 license，不是著作权转让）。
2. **素材库许可**：参考图、字体、图标、纹理的授权范围 —— 桌面 / 网页 / 嵌入 App / 商标图样是**不同授权**（`brand-identity.md` §12/§17）。
3. **人格与第三方权利**：肖像、声音、可识别建筑/艺术品、他人 logo；AI 仿声与换脸同时触发 deepfake 披露（欧盟 Art. 50(4)）与中国标识义务。
4. **标识与元数据**：导出后仍在（§2.3、§21.5）。

---

## 7. DESIGN.md：把"风格一致性"变成 AI 可读的契约

`design-md-format.md` 已给九章骨架；本节补的是**为什么它是 AI 工具链的关键节点**，而不是抄一遍骨架。

Google Stitch 提出的 DESIGN.md 是放在项目根目录的纯文本设计系统文档，AI 编码 agent 读了就能生成风格一致的 UI。其格式含 9 章：① Visual Theme & Atmosphere ② Color Palette & Roles ③ Typography Rules ④ Component Stylings ⑤ Layout Principles ⑥ Depth & Elevation ⑦ Do's and Don'ts ⑧ Responsive Behavior ⑨ **Agent Prompt Guide**。

### 7.1 三条纪律

1. **第 9 章最常被漏，但它是"可执行"的关键**：给 agent 的 3–5 条生成指令 + 一段可直接用的 prompt 模板。没有它，前 8 章只是给人看的说明书。
2. **它是给机器读的约束，不是给人读的系统**：设计系统站点/组件文档页是另一回事（见 `design-system-docs.md` 的 Diátaxis 判层与 GOV.UK 九段式），别把两者混写。
3. **风格要有出处**：`awesome-design-md` 收录 54 个真实产品的 DESIGN.md（Vercel / Linear / Stripe / Notion / Figma / Apple / IBM…），并给出项目类型→推荐风格映射（SaaS 官网→Stripe/Vercel/Linear；AI 产品→Claude/Mistral AI/ElevenLabs；开发者工具→Vercel/Cursor/Raycast/Supabase；内部后台→Sentry/PostHog/ClickHouse 等）。用户没指定风格时**主动推荐 3–5 个并让用户选**，别默认套一个；用户说"随便"才给安全默认值并说明可换。

### 7.2 与 token 体系对齐

DESIGN.md 里的色值/字号/间距必须与 `design-tokens.md` 的三层架构和 `multi-brand-theming.md` 的 L0–L3 一致。**AI 生成 UI 最常见的系统性故障不是"不好看"，而是每次生成的十六进制值都不一样**（§12.12）。写进 DESIGN.md 的是 token 名，不是散落的 hex。

---

## 8. 提示词工程：把设计 brief 变成可复用、可评估的 prompt

### 8.1 官方结构（OpenAI Prompt Engineering 指南口径）

`developer` message 推荐按 **Identity → Instructions → Examples → Context** 组织：

| 区块 | 作用 | 设计场景填什么 |
|---|---|---|
| **Identity** | 模型扮演谁 | "你是一位 B 端中后台设计总监，给立场不和稀泥" |
| **Instructions** | 规则、约束、输出格式 | 设计原则、禁用项、token 表引用、产出结构 |
| **Examples** | 输入/期望输出配对（few-shot） | 1 好 1 坏的界面描述 + 判定理由 |
| **Context** | 训练数据外的专有/相关信息 | 品牌 VI、真实组件库、用户画像、DESIGN.md 片段 |

官方三条容易被忽略的细节：
- **Context 通常放 prompt 靠后**（不同请求换不同 context）；而**反复复用的稳定内容应放最前面**以命中 prompt caching，省成本与延迟。
- Markdown 标题/列表划分区块，**XML 标签**标出内容边界与属性（`<design_spec>` / `<examples>`），让模型分清"指令"与"参考资料"。
- 角色优先级：`instructions` 参数 > `developer` > `user` > `assistant`；`instructions` **只作用于当前响应**，用 `previous_response_id` 串会话时不会保留。

### 8.2 输出与评估的工程化（不是"多试几次"）

- **指定输出格式**：JSON Schema / Structured Outputs、严格单值输出、"不要 Markdown 只返回代码"；前端场景明确 Markdown standards（inline code / fences / 表格 / 路径与类名用反引号）。
- **Few-shot 要多样**：*"show a diverse range of possible inputs with the desired outputs"*，示例通常放 `developer` message；工具调用要给具体调用示例。
- **Prompt 当代码管**：*"Store production prompts in your application code"* —— 类型化输入、code review、测试、正常发布流程；改生产 prompt 前加 representative fixtures 与 evaluation checks，用 feature flag / 配置做灰度。
- **固定模型快照**：官方举例 `gpt-4.1-2025-04-14`；模型升级会改变输出，非确定性内容必须有 eval suite。
- **Rubric 自检**：官方 zero-to-one web app 示例要求先建 5–7 类内部 rubric、再据此迭代；agentic 任务用 TODO / rubric 并在每次 tool call 后反思完整性。
- **别假设输出位置**：文本不一定在 `output[0].content[0].text`，用 SDK 的 `output_text` 聚合。

> ⚠️ **对设计的直接含义**：同一段 prompt、同一模型、同一快照，在不同时间也可能产出不同界面。所以 **prompt 要进版本库、进 code review、进 CI**，不能存在聊天记录里。`handoff-collaboration.md` §12 的 SemVer 规则同样适用：**改默认 prompt = 改默认值 = MAJOR**，见 §15。

### 8.3 设计 brief → prompt 转换表（本技能第 2 步的落地）

| brief 字段 | 写进 prompt 的哪块 | 反面例子 |
|---|---|---|
| Target audience（谁用） | Identity + Context | "做一个高大上的页面" |
| Use cases（完成什么任务） | Instructions（任务与成功标准） | "做个 dashboard" |
| Brand personality / tone | Context（引用 DESIGN.md / 品牌 DNA） | "科技感、有质感" |
| 约束（框架/性能/无障碍） | Instructions（硬约束，不可协商） | 事后才说"要过 WCAG" |
| 参考与反例 | Examples（成对给，含理由） | 只给一张好看的图 |
| 交付格式 | Instructions（结构化输出） | "随便给点方案" |

> **设计上下文不能靠读代码库推断**（`impeccable` 纪律）：代码只说明"构建了什么"，不说明"为谁构建 / 应该有什么感觉"。目标受众、用例、品牌调性必须由人给，或读项目根 `.impeccable.md` / Design Context 段。

### 8.4 一段可复用模板

见 §21.2。核心是 **四区块 + 硬约束清单 + 输出 schema + 自检 rubric**，且把"给立场、列反例、标不确定"写成指令，而不是期望模型自发做到。

---

## 9. AI 辅助设计的工作流（可直接落地的 8 步）

1. **写 brief**（人）：受众 / 用例 / 品牌调性 / 硬约束 / 成功标准，最多 3 个澄清问题、给选项不给开放题（本技能第 2 步）。
2. **判可行性 × 美观性**（人）：技术/范围/资源/性能四查 + 审美风险预判，**执行前给明确立场**（第 3 步）。
3. **定风格契约**：选 DESIGN.md 参考风格或填九章 → 写进 Context。
4. **生成变体**（AI）：一次要 4–6 个**方向不同**的构型，不要 20 个同款换色。
5. **筛**（人）：按第 5 步原则 + §11 AI Slop Test 砍掉一半，写清每个被砍的理由。
6. **深化与对齐**：把选中的方案拆成 token / 组件 / 状态，回写 DESIGN.md；数值一律从 `design-tokens.md`、`form-table.md` 等专项取，**不让模型自己编 px**。
7. **代码化 + 自动验收**（AI + 脚本）：§21.4 脚本先跑，再人工读语义与状态。
8. **合规与交付**：§2.3 标识清单、§4 创作链台账、§20 自检、走查三遍法、P0–P3 门禁。

> **每步都要留人工闸门**。跳过第 2/5/6/8 步，得到的是"看起来完成了"的产出，而不是可交付的设计。

---

## 10. AI 功能界面：微软人机交互 18 条准则（HAX G1–G18）

来源：Microsoft HAX Toolkit《Guidelines for Human-AI Interaction》，综合 20+ 年研究，2019 CHI 获奖论文；官方说明其设计模式贯穿 **Initial / During interaction / When wrong / Over time** 四阶段。下表按官方设计库 **G1–G18 编号顺序**逐条给**界面落点**（界面落点是本技能自己的映射，准则编号、标题与说明为官方原文口径）。

> **口径纪律**：官方设计库页面给出 18 条编号与四阶段名称，但**未逐条标注编号与阶段的归属**；因此下表只按编号分四组便于阅读，**不臆造「G× 属于某阶段」的边界**。四阶段名称本身来自 HAX 官方页面。

### 准则 1–6
| # | 准则（官方标题） | 说明 | 界面落点 |
|---|---|---|---|
| G1 | Make clear what the system can do | 让用户理解 AI 能做什么 | 首次使用说明能力边界；**不得暗示全能** |
| G2 | Make clear how well the system can do what it can do | 让用户理解出错频率 | 给置信度/准确率口径，不只给"智能"标签 |
| G3 | Time services based on context | 按当前任务与环境决定何时行动/打断 | 不在用户填表到一半弹 AI 建议 |
| G4 | Show contextually relevant information | 显示与当前任务环境相关的信息 | 侧栏建议绑定当前选区，不给通用灵感 |
| G5 | Match relevant social norms | 符合社交与文化预期 | 不用拟人化到让用户误以为是真人（叠加欧盟 Art. 50(1) 告知义务） |
| G6 | Mitigate social biases | 不强化刻板印象与不公平偏见 | 生成人像/职业/姓名样例做多样性抽检 |

### 准则 7–11
| # | 准则 | 说明 | 界面落点 |
|---|---|---|---|
| G7 | Support efficient invocation | 需要时容易唤起 | 快捷入口 / 快捷键，别藏在三级菜单 |
| G8 | Support efficient dismissal | 容易忽略或关闭不想要的服务 | 一键关闭且**记住关闭状态** |
| G9 | Support efficient correction | 出错时容易编辑、细化、恢复 | 保留原始输入、可回退、可局部重生成 |
| G10 | Scope services when in doubt | 目标不确定时澄清或优雅降级 | 给选项式追问，别自作主张生成一大版 |
| G11 | Make clear why the system did what it did | 可访问"为什么这么做"的解释 | "为什么推荐这个"入口；解释要能读懂 |

### 准则 12–13
| # | 准则 | 说明 | 界面落点 |
|---|---|---|---|
| G12 | Remember recent interactions | 保持短期记忆，便于高效引用 | "沿用上一步的风格"这类引用 |
| G13 | Learn from user behavior | 随时间从行为中个性化 | 个性化要**可见、可重置**（见 G17） |

### 准则 14–18
| # | 准则 | 说明 | 界面落点 |
|---|---|---|---|
| G14 | Update and adapt cautiously | 更新行为时限制破坏性变化 | 模型升级不静默改变输出风格；发版前跑 eval |
| G15 | Encourage granular feedback | 常规交互中收集细粒度偏好 | 针对单个结果给"太花/太挤/不是这个语气"，别只给 👍👎 |
| G16 | Convey the consequences of user actions | 立即说明用户动作将如何影响未来行为 | "点赞后同类建议会更多"要当下可见 |
| G17 | Provide global controls | 允许全局自定义监控内容与行为方式 | 设置页总开关：是否记录、是否个性化、是否用于改进 |
| G18 | Notify users about changes | 新增或更新能力时通知用户 | 变更提示 + changelog；与 §15 SemVer 对齐 |

### 接线：18 条准则接回本技能既有资产

- **G2 / G11（不确定性披露）** ↔ `feedback-states.md` §1 五层决策树：AI 建议属于低风险可撤销反馈，别用模态打断；但"生成失败/内容被拦截"属于错误，要按 §6 三级错误文案写清**发生了什么 + 为什么 + 怎么修**。
- **G9（纠错）** ↔ `ux-writing.md` §2：按钮写具体动作（"重新生成背景"），禁 "重试 / OK"。
- **G3（时机）** ↔ `feedback-states.md` §2 的 0.1 / 1 / 10s 阈值：长生成任务必须有进度，>10s 要给可取消与后台继续。
- **G5 / G6** ↔ `accessibility.md` + `i18n-localization.md`：告知信息要读屏可读，且 RTL 下不能因镜像丢失标识。
- **G17（全局控制）** ↔ 《暂行办法》第 11 条：输入与使用记录的保护义务落在设置页具体开关上，不是一句隐私政策。

---

## 11. AI 味验收：AI Slop Test 与 8 维 DO/DON'T

来源：`impeccable`（基于 Anthropic frontend-design 技能，Apache-2.0，仓库 `pbakaus/impeccable` 实测 **104380★ / Apache-2.0 / 2026-11-05**）。

### 11.1 一句话测试

> **"如果你把这个界面展示给某人并说'这是 AI 做的'，他们会立刻相信吗？如果是，那就是问题所在。"**
> 独特的界面应该让人问"这是怎么做出来的？"，而不是"哪个 AI 做的？"

把它变成可执行判据：**找 3 个不知道需求的人，展示界面并只问"你猜这是怎么做的"**。若 2 人以上直接答"AI 生成"，本轮不算通过，回到 §9 第 5 步重筛。

### 11.2 8 维 DO / DON'T 速查

| 维度 | ✅ DO | ❌ DON'T |
|---|---|---|
| 字体 | 独特展示字体 + 精致正文字体；模块化比例；`clamp()` 流体尺寸 | Inter / Roboto / Arial / Open Sans；等宽字体当"技术感"；标题上方大图标 + 圆角 |
| 色彩 | `oklch` / `color-mix` / `light-dark()`；中性色调偏向品牌色 | 纯黑 `#000` / 纯白 `#fff`；**AI 配色**（青+深色、紫蓝渐变、霓虹点缀）；默认深色+发光 |
| 空间 | 变化间距创造节奏；`clamp()` 流式间距 | 万物皆卡片 / 卡片套卡片；英雄指标模板；居中一切 |
| 动效 | 状态变化动效；指数缓动（ease-out-quart / expo） | 动画化布局属性；回弹 / 弹性缓动 |
| 交互 | 渐进式披露；有教育意义的空状态 | 重复信息；所有按钮都设为主要 |
| 响应 | 容器查询 `@container` | 移动端隐藏关键功能 |
| 文案 | 每个词都有存在价值 | 重复用户已能看到的信息 |
| 细节 | 有意图的装饰强化品牌 | 毛玻璃滥用；圆角 + 通用阴影；无意义火花线 |

> 与既有资产一致性：色彩/字体的"不用纯黑纯白"与 `dark-mode.md` §3「不用纯白」同源；动效的"不动画化布局属性"与 `performance-design.md` §11「只动 transform/opacity」同源；响应式的容器查询与 `responsive-layout.md` §1 同源。**这些不是新规则，是 AI 生成时最常违反的既有规则**——把它们前置成筛选项，比事后逐条返工便宜。

### 11.3 生成前的三个必答问题（Design Context）

1. **Target audience**：谁用？在什么情境下？
2. **Use cases**：他们要完成什么任务？
3. **Brand personality / tone**：界面应该给人什么感觉？

三个里缺任何一个，**先补再生成**。这是 `impeccable` 的硬纪律，也是本文件 §1.2 第 2 条"不交给 AI"的具体化。

---

## 12. AI 生成界面的 12 类固有缺陷 → 接回既有专项

> 本节是**索引**，不复制规则。每条给出「症状 → 去哪份读 → 自动检查」。

| # | 症状 | 根因 | 去哪读 | 自动检查 |
|---|---|---|---|---|
| 1 | 生成页好看但 Tab 走不动、`outline:none` | 模型只学了视觉，没学语义 | `accessibility.md` §3/§4 | §21.4 脚本 |
| 2 | 对比度不够，浅灰字/浅色边框 | 模型偏好低对比"高级感" | `accessibility.md` §2（4.5:1 / 3:1 不四舍五入） | 计算脚本（同 `multi-brand-theming.md` 亮度边界） |
| 3 | 只有 happy path，缺空/错/加载/禁用态 | 一次生成只画一个状态 | `feedback-states.md` §4/§5/§6、`handoff-collaboration.md` §5 九态矩阵 | 状态清单比对 |
| 4 | 文字是编造的假数据、假人名、假价格、假法条 | 模型补白 | `ux-writing.md` §2/§4 + §1.2 第 3 条 | 上线前逐字段核对真实数据源 |
| 5 | 真实客户数据被贴进外部模型 | 输入侧无脱敏 | §6.2、《暂行办法》第 11 条 | 上传前 checklist |
| 6 | 按钮写 OK / Submit / "点击这里" | 训练语料惯性 | `ux-writing.md` §2（动词 2–4 词、中文 2–4 字、禁 OK） | 禁词表扫描 |
| 7 | 图表截断轴、饼图切 8 片、色板靠感觉 | 图表规范未进 prompt | `dataviz.md` §2/§3 | 图表选型核对 |
| 8 | 表单一进来全红、表格全列居中 | 校验与对齐规则未进 prompt | `form-table.md` §6/§13 | 视觉走查 |
| 9 | 手机上横向滚动、`100vh` 被地址栏挡 | 只生成桌面视图 | `responsive-layout.md` §7/§9 | 8 档宽度截图 |
| 10 | 动效乱加、回弹、500ms 起步 | 把"有动效"当"有质感" | `motion-system.md` §2/§3、`motion-orchestration.md` | 时长/曲线核对 |
| 11 | 首屏大图 + 玻璃拟态 + 粒子，加载很慢 | 效果没定价 | `performance-design.md` §10 视觉手法性能价格表 | Lighthouse / 预算表 |
| 12 | 每次生成的 hex / 间距都不同，多页不像同一产品 | 没写 token 名只写色值 | `design-tokens.md`、`design-md-format.md`、§7.2 | token 名 vs 字面值扫描 |

---

## 13. AI 设计工具链五层地图与选型（GitHub REST API 实测 2026-11-06）

> 数据由 `api.github.com/repos/{owner}/{repo}` 实测（凭据经 `GET /user` 验证）；star 为快照值，许可取 `license.spdx_id`，`NOASSERTION` 表示非标准/自定义许可，**商用前必须自己读 LICENSE**。拿不到原文的线索一律不写入。

| 层 | 仓库 | star | 许可 | 最近推送 | 选型备注 |
|---|---|---|---|---|---|
| L2 生成 | `comfyanonymous/ComfyUI` | 145350 | **GPL-3.0** | 2026-11-06 | 节点式工作流；**GPL-3.0 有传染性**，商业集成先评估 |
| L2 生成 | `AUTOMATIC1111/stable-diffusion-webui` | 165264 | **AGPL-3.0** | 2026-03-02 | 推送已趋缓（约 8 个月） |
| L3 编辑 | `lllyasviel/ControlNet` | 34151 | Apache-2.0 | 2024-02-25 | 结构控制；**已近 3 年未推送**，别当活源 |
| L3 编辑 | `facebookresearch/segment-anything` | 55103 | Apache-2.0 | 2024-09-18 | 分割/抠图基础模型，同样趋缓 |
| L3 编辑 | `xinntao/Real-ESRGAN` | 37387 | BSD-3-Clause | 2024-08-06 | 超分；BSD 友好 |
| L3 编辑 | `upscayl/upscayl` | 51827 | **AGPL-3.0** | 2026-10-05 | 桌面超分应用 |
| L4 代码化 | `abi/screenshot-to-code` | 81058 | MIT | 2026-11-05 | 截图→代码，最活跃；产出必须过 §21.4 验收 |
| L4 代码化 | `GLips/Figma-Context-MCP` | 16173 | MIT | 2026-10-27 | Figma → MCP 上下文；与 `handoff-collaboration.md` §7.4 Code Connect 是不同层（这里给模型喂设计数据，Code Connect 给开发者看真实组件） |
| L4 代码化 | `builderio/builder` | 8884 | MIT | 2026-11-06 | 可视化搭建 |
| 画布/协作 | `tldraw/tldraw` | 51299 | **NOASSERTION** | 2026-11-06 | 无限画布 SDK；许可需单独确认 |
| 规范/风格 | `VoltAgent/awesome-design-md` | 125854 | MIT | 2026-10-28 | 54 个真实产品 DESIGN.md（§7） |
| 质量/反 AI 味 | `pbakaus/impeccable` | 104380 | Apache-2.0 | 2026-11-05 | §11 的判据来源 |
| 提示词 | `f/awesome-chatgpt-prompts` | 175985 | **NOASSERTION** | 2026-11-06 | 提示词合集；**许可不明，别整段复制进商业代码** |
| 提示词 | `openai/openai-cookbook` | 76977 | MIT | 2026-11-06 | §8 官方指南配套示例 |
| 提示词 | `anthropics/prompt-eng-interactive-tutorial` | 39094 | 无 license 字段 | 2026-08-28 | 交互式教程；无明确许可声明 |
| 提示词 | `google-gemini/cookbook` | 17907 | Apache-2.0 | 2026-11-05 | Gemini 官方示例 |
| 编辑器 | `cursor/cursor` | 33324 | 无 license 字段 | 2026-05-12 | 该仓库为 issue 跟踪用途，非源码 |
| — | `microsoft/TypeScript` | 111782 | Apache-2.0 | 2026-11-06 | 对照组：§21.4 类型化 prompt 的基础 |

**实测中 404 的线索（已剔除，不臆造）**：`soma-shah/Figma-Context-MCP`、`Motiff/motiff`。

### 13.1 选型三问（比 star 更重要）

1. **许可能不能进商业项目？** GPL-3.0 / AGPL-3.0 / NOASSERTION 三个红灯，尤其 AGPL 对 SaaS 有网络交互条款；Apache-2.0 / MIT / BSD-3-Clause 相对安全。
2. **是活源吗？** `pushed_at` 超过 12 个月的模型/规范仓库只能当参考，不能当会持续更新的依赖（ControlNet、segment-anything、Real-ESRGAN 均已趋缓）。
3. **输出能不能被验收？** 能不能导出分层/元数据、能不能跑自动化检查、失败能不能回退。不能验收的工具不进生产链。

---

## 14. 生成 → 代码：衔接层与三个陷阱

| 路径 | 工具/机制 | 交付物 | 必须补的人工动作 |
|---|---|---|---|
| 截图/设计稿 → HTML | screenshot-to-code 类 | HTML/CSS/JS | 语义标签、焦点态、九态矩阵、token 替换（§12.1/3/12） |
| Figma → 模型上下文 | Figma-Context-MCP | 设计数据结构 | 命名一致性、变体属性、隐藏图层清理 |
| Figma → 开发者视图 | **Code Connect**（`handoff-collaboration.md` §7.4） | 真实组件代码片段 | 组件映射维护、版本同步 |
| 风格约束 → 全项目 | DESIGN.md（`design-md-format.md`） | 根目录 Markdown | 九章填充 + 第 9 章 Agent Prompt Guide |

**三个陷阱**：
1. **Dev Mode 的自动生成代码 ≠ 你的组件**：默认给的是自动生成的 div；接 Code Connect 才能让开发者看到真实组件。AI 截图转码同理，产出的是"长得像"的 DOM，不是设计系统组件。
2. **生成代码不带状态**：截图里只有一个状态，九态矩阵里的 hover / focus / selected / disabled / read-only / error / warning 全靠补（`handoff-collaboration.md` §3/§5）。
3. **token 字面值漂移**：生成代码里出现 `#1677FF`、`16px` 这类散落字面值而不是 `var(--color-primary)`，见 §12.12 与 §7.2。

---

## 15. Prompt 版本化、eval 与 SemVer

| 变更 | 级别（类比 `handoff-collaboration.md` §12 SemVer） | 理由 |
|---|---|---|
| 改默认 prompt 的措辞 / 增删硬约束 | **MAJOR** | 等价于"改默认值"，全站输出风格会变 |
| 新增一个可选 prompt 模板 | MINOR | 向后兼容 |
| 修提示词里的错别字、修 XML 标签闭合 | PATCH | 不改变行为 |
| 换模型 / 换模型快照 | **MAJOR + 全量 eval** | 官方明确要求固定快照；非确定性输出必须回归 |
| 改输出 schema | MAJOR | 下游解析器会崩 |

**官方 eval 纪律**（§8.2）：prompt 存代码库 → 类型化输入 → representative fixtures + evaluation checks → feature flag 灰度 → 固定模型快照 → 升级前跑全量 eval。把它接到 `handoff-collaboration.md` §14 的回归四层（80% 覆盖 / VRT ≥1 默认 story / AVT 全复杂态 / 三读屏器），AI 生成界面额外加一层：**输出一致性 eval**（同一 prompt 多次生成的 token 名、结构、状态覆盖是否稳定）。

---

## 16. 不确定性与披露：把"可能错"设计出来

1. **AI 身份告知**（欧盟 Art. 50(1)）：与人直接交互的系统须告知对方在与 AI 交互，除非对合理知情、观察、审慎的人而言显而易见；Art. 50(5) 要求**最迟在首次交互/首次暴露时**以清晰可区分方式提供，并**符合适用无障碍要求**。
2. **能力边界与出错率**（HAX G1/G2）：首次使用说明能做什么、多久会错；别用"智能""精准"这类无信息量的词。
3. **解释入口**（HAX G11）："为什么推荐这个"要能点开，且解释用用户语言。
4. **标识三档语义**（中国第 6 条）：属于 / 可能为 / 疑似，**不可混用**。
5. **低置信度时收敛而非硬生成**（HAX G10）：给选项式追问或优雅降级，别自作主张铺满一屏。
6. **错误与拦截文案**：按 `feedback-states.md` §6 三段式（发生了什么 + 为什么 + 怎么修），禁俏皮话，禁把责任推给用户。

---

## 17. 隐私、输入与组织边界

- 《暂行办法》第 11 条：不收集非必要个人信息、不非法留存可识别身份的输入与使用记录、不非法向他人提供；须及时受理查阅/复制/更正/补充/删除请求。
- 第 17 条：具有**舆论属性或社会动员能力**的服务须开展安全评估并履行算法备案；第 12 条：算法备案、安全评估时提供标识材料。
- 第 2 条第 3 款：内部研发应用、未向境内公众提供服务**不适用本办法**——但**不适用 ≠ 无风险**，客户数据仍受合同与《个保法》约束。
- HAX G17 全局控制：把"是否记录、是否个性化、是否用于改进"做成用户可见开关，不要只写在隐私政策里。
- 设计侧最小动作：上传素材前脱敏；建立"可上传 / 需审批 / 禁止上传"三级素材分类；把这条写进团队 AI 使用规范。

---

## 18. 12 场景速查

| # | 场景 | 直接结论 |
|---|---|---|
| 1 | 用 AI 生成官网主视觉并上线（境内） | 显式标识 + 隐式元数据；导出件也带；记录创作链（§2/§4） |
| 2 | 做出海产品，同一素材投中/欧/美 | 按中国双轨做一套元数据 + 欧盟界面告知与 deepfake 披露；美国备登记披露材料（§3） |
| 3 | 客户问"这图版权归我们吗" | 不因提示词归客户；给出人类贡献台账与分层源文件，让法务判断（§4） |
| 4 | 供应商说"我们有 Content Credentials，所以可商用" | 不成立；C2PA 不作权属/真伪判断，看 ToS 与人类贡献（§5） |
| 5 | 想做"一键去 AI 角标"功能 | 不做（第 10 条禁止恶意删除/隐匿标识、不得提供工具）；无标版走第 9 条协议 + 6 个月日志 |
| 6 | AI 生成 20 个落地页方案 | 先按 §11 AI Slop Test 砍一半，再按第 5 步原则筛到 1–2 个 |
| 7 | 同一 prompt 每次生成颜色都不一样 | 把 token 名写进 DESIGN.md 与 Instructions，散落 hex 一律判 FAIL（§7.2/§12.12） |
| 8 | 截图转代码后要上线 | 过 §21.4 自动验收 + 九态矩阵 + 走查三遍法，别直接发 |
| 9 | 产品里加"AI 生成"按钮 | HAX G7/G8/G9 三件套（易唤起 / 易关闭 / 易纠错）+ 首次告知 + 进度可取消（§10/§16） |
| 10 | 模型升级后界面风格变了 | 固定快照、全量 eval、G18 通知用户、SemVer MAJOR（§15） |
| 11 | 要把未发布产品图贴进公共模型找灵感 | 脱敏或走私有部署；先查第 11 条与合同（§6.2/§17） |
| 12 | 用 AI 生成的字体/logo 做品牌 | 叠加商标检索、字体授权、最小尺寸与清space 检查（`brand-identity.md` §17/§6/§7），并留人类修改证据 |

---

## 19. 20 条反模式

1. **把合规判断交给模型**——AI 会编法条；只认官方原文。
2. **只做显式角标，不做元数据**——第 5 条是独立义务。
3. **导出/下载时把标识洗掉**——第 4 条末款明确要求文件中含显式标识。
4. **把"属于 / 可能为 / 疑似"三档文案混用**——第 6 条法律语义不同。
5. **提供"一键抹除 AI 标识"**——第 10 条禁止。
6. **认为提示词 = 作者身份**——USCO：not the mere provision of prompts。
7. **认为打了 Content Credentials 就有版权**——C2PA 只断言完整性。
8. **把订阅会员当版权转让**——ToS 给的是 license。
9. **只留一张 PNG 当交付物**——无可举证创作链。
10. **没拿到国标全文就编造像素/秒数**——本技能纪律：拿不到原文不写入资产。
11. **把客户未公开素材贴进公共模型**——输入侧泄露。
12. **上线 AI 编造的假数据**——逐字段核对真实数据源。
13. **让模型自己编 px / hex / 时长**——数值一律从专项文件取。
14. **DESIGN.md 漏第 9 章 Agent Prompt Guide**——前 8 章不可执行。
15. **把 DESIGN.md 当设计系统文档站写**——机器读的约束 ≠ 给人读的系统。
16. **prompt 存在聊天记录里**——要进版本库、review、CI。
17. **不固定模型快照**——非确定性输出无法回归。
18. **AI 功能没有关闭/纠错/解释入口**——违反 G8/G9/G11。
19. **首次交互后才告知在与 AI 交互**——Art. 50(5) 要求最迟首次交互/暴露。
20. **把 AI 生成界面直接当终稿发布**——没过 §20 自检与走查三遍法。

---

## 20. AI 关 20 项自检（第 6 步新增，逐条可判 PASS/FAIL）

1. **判层**：五个位置都标了人工闸门，最终取舍由人做（§1）。
2. **适用范围**：判明是否"向境内公众提供生成式 AI 服务"（《暂行办法》第 2 条）。
3. **显式标识**：按载体落在规定位置，界面/图片/视频/音频/虚拟场景逐项过（第 4 条）。
4. **导出保留**：下载 / 复制 / 导出三条路径抽检均含显式标识（第 4 条末款）。
5. **隐式标识**：元数据含生成合成属性 + 服务提供者名称或编码 + 内容编号（第 5 条）。
6. **转码存活**：压缩 / CDN / 格式转换后元数据仍在（§21.5）。
7. **传播三档**：属于 / 可能为 / 疑似分支文案正确，且补传播要素（第 6 条）。
8. **用户声明**：发布流程有主动声明开关与标识功能（第 6/10 条）。
9. **协议与日志**：标识样式写入用户协议；无标版留存日志 ≥6 个月（第 8/9 条）。
10. **无抹除工具**：全产品无"删除/篡改/伪造/隐匿标识"的工具或快捷方式（第 10 条）。
11. **欧盟界面告知**：首次交互前清晰告知 + 满足无障碍（Art. 50(1)/(5)）。
12. **deepfake / 公共利益文本披露**：适用时已披露，或确认命中豁免（Art. 50(4)）。
13. **创作链**：分层源文件 + 素材台账 + 人工修改清单齐备（§4.3）。
14. **授权四查**：ToS / 素材许可 / 人格权 / 标识均通过（§6.3）。
15. **Design Context**：受众 / 用例 / 品牌调性三项齐全才生成（§11.3）。
16. **AI Slop Test**：3 人盲测未出现 2 人以上直接答"AI 生成"（§11.1）。
17. **DESIGN.md**：九章齐全含第 9 章；token 名而非散落 hex（§7/§12.12）。
18. **prompt 工程化**：入版本库、类型化、有 eval fixtures、固定模型快照（§8/§15）。
19. **HAX 三件套**：易唤起 / 易关闭 / 易纠错 + 解释入口 + 全局控制（§10）。
20. **生成代码验收**：§21.4 脚本零阻断 + 九态矩阵 + 12 类缺陷逐条销项（§12/§14）。

---

## 21. 6 段可抄代码

### 21.1 标识合规 checklist（放进 CI，纯 Python 无依赖）

```python
# ai_label_check.py —— 按《标识办法》第 4/5/6/9/10 条核对交付物
from pathlib import Path
import sys

# 第 5 条要求元数据含「内容属性 / 服务提供者 / 内容编号」等制作要素。
# 下面右侧是工程侧常见字段别名，**不是法定字段名**；法定口径以办法原文为准，
# 具体字段名/取值以适用标准与平台规范为准（拿不到原文不硬编码）。
REQUIRED_ELEMENTS = {
    "生成合成内容属性信息": ("Label", "AIGC", "生成合成内容属性信息"),
    "服务提供者名称或编码": ("ContentProducer", "ServiceProvider", "服务提供者名称或编码"),
    "内容编号": ("ProduceID", "ContentID", "内容编号"),
}
BANNED_UI = ("去除AI标识", "抹掉水印", "隐藏标识", "remove ai label")

def _keys(meta: dict) -> set:
    """递归取扁平字段名：兼容 {"AIGC": {"Label": "1"}} 这类嵌套结构。"""
    out = set()
    for k, v in meta.items():
        out.add(str(k).lower())
        if isinstance(v, dict):
            out |= _keys(v)
    return out

def check_export(path: Path, label_visible: bool, meta: dict, ui_strings: list):
    problems = []
    if not label_visible:
        problems.append("第4条：导出文件缺少显式标识")
    keys = _keys(meta)
    for element, aliases in REQUIRED_ELEMENTS.items():
        if not any(a.lower() in keys for a in aliases):
            problems.append(f"第5条：元数据缺要素 {element}")
    for s in ui_strings:
        if any(b.lower() in s.lower() for b in BANNED_UI):
            problems.append(f"第10条：疑似抹除标识功能「{s}」")
    return problems

if __name__ == "__main__":
    good = {"AIGC": {"Label": "1", "ContentProducer": "corp-042",
                     "ContentPropagator": "platform-7", "ProduceID": "20261106-0001"}}
    cases = [
        ("合规件",     True,  good, ["导出", "下载", "保存"], 0),
        ("缺显式标识", False, good, ["导出"],                1),
        ("缺内容编号", True,  {"AIGC": {"Label": "1", "ContentProducer": "corp-042"}}, ["导出"], 1),
        ("含抹除功能", True,  good, ["去除AI标识"],           1),
    ]
    results = []
    for name, visible, meta, ui, want in cases:
        got = len(check_export(Path("hero.png"), visible, meta, ui))
        results.append((name, got == want, got))
    for name, passed, got in results:
        print(f"{'PASS' if passed else 'FAIL'} {name}（检出 {got} 项）")
    sys.exit(0 if all(p for _, p, _ in results) else 1)
```

> `path` 保留在签名里是为了接 §21.5 的「导出后元数据存活」抽检；本段只校验要素齐全与 UI 红线，不假装能判断标识是否「显著」——显著性需人工复核（对应 GB 45438-2025 的尺寸/时长要求，本资产不臆造数值）。

### 21.2 设计 prompt 四区块模板（OpenAI 指南结构）

```xml
<!-- developer message：Identity → Instructions → Examples → Context -->
<identity>
你是 B 端中后台设计总监。给立场，不和稀泥；评审先给结论再列备选。
</identity>

<instructions>
任务：为「{{use_case}}」生成 4 个方向不同的布局构型，不要 4 个换色同款。
硬约束（不可协商）：
  - 只用 <design_spec> 里的 token 名，禁止出现裸 hex / 裸 px 数值
  - 每个方案必须列出 9 态（default/hover/focus/selected/disabled/read-only/error/warning/loading）的覆盖情况
  - 禁止：纯黑 #000 / 纯白 #fff、紫蓝渐变、万物皆卡片、OK/Submit 按钮文案
  - 输出严格 JSON，schema 见 <output_schema>
成功标准：3 人盲测中不得有 2 人以上直接判断为「AI 生成」。
</instructions>

<examples>
<input>「数据看板 KPI 怎么排」</input>
<good>一页一主指标 + 两张趋势图，指标卡不做立体阴影；理由：降低噪声、对齐阅读动线</good>
<bad>四张等大渐变卡片 + 霓虹描边 + 装饰性火花线；理由：英雄指标模板 + AI 配色</bad>
</examples>

<output_schema>
{"schemes":[{"name":"","layout":"","token_refs":[],"states_covered":[],
             "anti_slop_check":[],"reject_reason":""}],"verdict":""}
</output_schema>

<context>
目标受众：{{target_audience}}
品牌调性：{{brand_tone}}
<design_spec>{{DESIGN_md_excerpt}}</design_spec>
</context>
```

### 21.3 DESIGN.md 最小可用骨架（九章，第 9 章不可省）

```markdown
# DESIGN.md
## 1. Visual Theme & Atmosphere   <!-- 一句话气质 + 一句反气质 -->
## 2. Color Palette & Roles       <!-- 语义名 → token 名，不写散落 hex -->
## 3. Typography Rules            <!-- 字族/层级表/中文回退栈 -->
## 4. Component Stylings          <!-- 按钮/卡片/输入 + 9 态 -->
## 5. Layout Principles           <!-- spacing scale / grid / 留白 -->
## 6. Depth & Elevation           <!-- 阴影层级，暗色靠提亮不靠阴影 -->
## 7. Do's and Don'ts             <!-- 至少 5 条 DON'T -->
## 8. Responsive Behavior         <!-- 断点 / 折叠 / 触摸目标 -->
## 9. Agent Prompt Guide          <!-- 3–5 条生成指令 + 可直接用的 prompt -->
> 生成前必读 references/design-md-format.md；数值一律取自 design-tokens.md。
```

### 21.4 AI 生成界面自动验收（HTML 静态扫描，零依赖）

```python
# ai_ui_audit.py —— AI 生成 HTML 上线的第一道闸门（§12.1/2/3/6/12）
import re, sys
from pathlib import Path

# 英文用词边界，避免把 B**OK** / TOKEN 之类的子串误判成按钮文案；中文直接子串匹配
BANNED_COPY = [r"\bOK\b", r"\bSubmit\b", r"\bClick here\b", r"\bOops\b", "点击这里", "格式不正确"]
RAW_VALUE = re.compile(r"#[0-9a-fA-F]{3,8}\b|(?<![\w-])\d{2,3}px\b")

def audit(html: str):
    fail = []
    if re.search(r"outline\s*:\s*(none|0)", html, re.I): fail.append("焦点框被杀（§12.1）")
    if re.search(r"<div[^>]*onclick", html, re.I): fail.append("可点击 div 缺语义（§12.1）")
    for m in re.finditer(r"<img\b[^>]*>", html, re.I):
        if "alt=" not in m.group(0): fail.append("img 缺 alt（§12.1）")
    for w in BANNED_COPY:
        if re.search(w, html, re.I): fail.append(f"禁用文案「{w.replace(chr(92) + 'b', '')}」（§12.6）")
    if len(RAW_VALUE.findall(html)) > 8: fail.append("散落字面值过多，疑似未用 token（§12.12）")
    for kw in ("aria-", "focus", "disabled", "error", "loading", "empty"):
        if kw not in html.lower(): fail.append(f"缺状态覆盖线索：{kw}（§12.3）")
    return fail

if __name__ == "__main__":
    html = Path(sys.argv[1]).read_text(encoding="utf-8")
    errs = audit(html)
    print("PASS" if not errs else "FAIL\n - " + "\n - ".join(errs))
    sys.exit(1 if errs else 0)
```

> 这是**第一道**闸门，不替代 axe-core / Lighthouse / 读屏实测；对比度与真实焦点顺序仍需专项检查（`accessibility.md` §2/§3/§14）。

### 21.5 元数据存活检查（导出 → 压缩 → CDN 后抽检）

```python
# meta_survival.py —— 第 5 条「文件元数据隐式标识」在管线末端的存活校验
from pathlib import Path
import sys

def inspect(path: Path):
    b = path.read_bytes()
    # JPEG APP1/EXIF/XMP、PNG tEXt/iTXt、WebP RIFF 均可能承载元数据
    marks = {
        "XMP": b.find(b"http://ns.adobe.com/xap/1.0/") >= 0,
        "EXIF": b"Exif\x00\x00" in b,
        "C2PA": b"c2pa" in b.lower(),
        "AIGC": b"AIGC" in b or "生成合成".encode("utf-8") in b,
    }
    return marks

if __name__ == "__main__":
    before, after = Path(sys.argv[1]), Path(sys.argv[2])
    m0, m1 = inspect(before), inspect(after)
    lost = [k for k in m0 if m0[k] and not m1[k]]
    print("元数据存活 PASS" if not lost else "FAIL 丢失：" + ", ".join(lost))
    sys.exit(1 if lost else 0)
```

### 21.6 AI 输出 eval 清单（YAML，换模型快照时全量跑）

```yaml
# ai_eval.yaml —— 与 §15 的 SemVer 规则配套，进 CI
model_snapshot: "pinned-model-2026-11-06"   # 官方要求固定快照
prompt_version: "design-brief@3.0.0"        # 改默认措辞 = MAJOR
fixtures:
  - id: landing-b2b
    context: references/design-md-format.md
    expect_tokens: ["--color-primary", "--space-4"]
    forbid: ["#000", "#fff", "紫蓝渐变", "Click here"]
    must_cover_states: 9
    must_have_alt: true
    must_have_focus: true
    must_keep_ai_label: true               # 第 4 条：导出件含显式标识
checks:
  - token_name_only          # 禁止散落 hex / px（§12.12）
  - ai_slop_test             # §11.1 三人盲测人工判定
  - label_survival           # §21.5
  - ui_audit                 # §21.4
  - a11y_contrast            # accessibility.md §2，4.5:1 / 3:1 不四舍五入
  - nine_states              # handoff-collaboration.md §5
  - i18n_expansion           # i18n-localization.md §2，microcopy 2–3× 弹性
```

---

## 22. 数据来源（全部官方原文 / 上游源码 / API 实测）

**法规与官方解读**
- 国家互联网信息办公室等四部门《人工智能生成合成内容标识办法》（国信办通字〔2025〕2 号，2025-09-01 施行）：https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm
- 中国网信网《给人工智能生成合成内容贴上数字标识》（2025-09-05 专家解读，确认 GB 45438-2025 与办法同步施行、责任四段链）：https://www.cac.gov.cn/2025-09/05/c_1758792061408012.htm
- 七部门《生成式人工智能服务管理暂行办法》（令第 15 号，2023-08-15 施行）：https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm
- EU AI Act Article 50 Transparency Obligations（依 Art. 113 于 2026-08-02 适用）：https://artificialintelligenceact.eu/article/50/
- U.S. Copyright Office · Copyright and Artificial Intelligence（Part 1 2024-07-31 / Part 2 2025-01-29 / Part 3 预发布 2025-05-09）：https://copyright.gov/ai/
- U.S. Copyright Office 官方解读《Inside the Report, Part 2: Copyrightability》（2025-02-06，含 "but not the mere provision of prompts"）：https://blogs.loc.gov/copyright/2025/02/inside-the-copyright-offices-report-copyright-and-artificial-intelligence-part-2-copyrightability/
- USCO Registration Guidance（88 Fed. Reg. 16,190，2023-03-16）：https://www.govinfo.gov/content/pkg/FR-2023-03-16/pdf/2023-05321.pdf

**技术规范与人机交互准则**
- C2PA Specifications（现行门户 2.5；Explainer 2.2 / UX Recommendations 2.2 / AI-ML 2.3 / Security 2.4 / Attestations 1.4 / Soft Binding 2.4）：https://c2pa.org/specifications/
- C2PA Explainer（"do not provide value judgments about … 'true'" / "not a cure-all for misinformation" / "Unlike DRM…"）：https://spec.c2pa.org/specifications/specifications/2.2/explainer/Explainer.html
- Microsoft HAX Toolkit · Guidelines for Human-AI Interaction（18 条 / 2019 CHI 论文）：https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/
- Microsoft HAX Design Library（G1–G18 逐条标题与说明）：https://www.microsoft.com/en-us/haxtoolkit/library/
- OpenAI · Prompt engineering 官方指南（Identity/Instructions/Examples/Context、few-shot、Structured Outputs、model snapshots、eval）：https://platform.openai.com/docs/guides/prompt-engineering

**本会话加载的技能（作为一手素材蒸馏）**
- `impeccable`（AI Slop Test、DO/DON'T 8 维、Design Context 纪律）→ 仓库：https://github.com/pbakaus/impeccable （Apache-2.0）
- `awesome-design-md`（54 个 DESIGN.md、九章格式、项目类型→风格映射）→ https://github.com/VoltAgent/awesome-design-md （MIT）
- Google Stitch DESIGN.md format：https://stitch.withgoogle.com/docs/design-md/format/ —— **本轮该页抓取失败，九章结构以 `references/design-md-format.md` 与本技能既有资产为准，未从该 URL 引入新数值**。

**GitHub REST API 实测（2026-11-06）**：见 §13 表格，18 个仓库逐条 `GET /repos/{owner}/{repo}` 取 `stargazers_count` / `license.spdx_id` / `pushed_at` / `archived`；`soma-shah/Figma-Context-MCP`、`Motiff/motiff` 返回 404 已剔除。

**取源纪律**：Adobe Firefly 商业安全页（本轮 404）与 Google Stitch format 页（本轮 fetch failed）**未取得原文，其具体承诺与数值一律不写入本资产**；GB 45438-2025 的显式标识时长/尺寸等具体数值同样未逐字取得，只保留网信办专家解读中可验证的"标准规定了显式标识的时长、尺寸与隐式标识要素"这一结论，落地以国标全文为准。

---

> **本轮让哪类问题不再含糊**：①「AI 生成素材能不能商用、要不要打标」→ 中国 14 条逐条设计动作清单 + 中欧美三法域矩阵；②「提示词算不算作者」→ USCO 原文裁决 + 可举证创作链五步；③「打了标/C2PA 是不是就安全」→ 三概念分离表；④「AI 生成界面怎么验收」→ AI Slop Test + 12 类缺陷索引 + 20 项自检 + 4 段可运行脚本。**只多了几条链接不算升级，这四条都给了可判 PASS/FAIL 的口径。**
