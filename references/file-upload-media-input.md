# 文件上传与媒体输入（File Upload & Media Input）：把「选个文件传上去」做成可失败、可恢复、可验收的五段链路

## §0 一句话立场与三条裁决

**一句话立场**：上传不是一个按钮，是**五段并存且每段都会失败的链路**——选（pick）→ 验（validate）→ 传（transfer）→ 处理（process）→ 存下或失败（commit / fail）。只做了一个「选择文件」按钮和一根进度条，等于只做了第一段和第三段的一半；用户真正会遇到的「传不上去 / 传上去是横的 / 传一半断了 / 传完说格式不对」全在第 2、4、5 段。

**三条最重要裁决**（每条都能直接改需求）：

1. **`accept` 是提示，不是校验，更不是安全边界。** MDN 逐字：*"The `accept` attribute doesn't validate the types of the selected files; it provides hints for browsers to guide users towards selecting the correct file types."* 以及 *"It is still possible (in most cases) for users to toggle an option in the file chooser that makes it possible to override this and select any file they wish, and then choose incorrect file types."* 结论写死：**前端 accept 只负责「少让人选错」，真正的类型判定必须在服务端**（OWASP 逐字：*"Validate the file type, don't trust the Content-Type header as it can be spoofed"*）。
2. **拖放是增强，不是通道；上传的每一条路径都必须能用单指针完成。** W3C SC 2.5.7（AA）逐字：*"All functionality that uses a dragging movement for operation can be achieved by a single pointer without dragging, unless dragging is essential or the functionality is determined by the user agent and not modified by the author."* 上传属于「非 essential」的典型：必须同时有「选择文件」按钮（本库 `accessibility.md:281` 已写死*「同时提供"选择文件"按钮（必须，不是可选）」*），拖放区只是第二条路。
3. **失败态是主设计对象，成功态只是它的一种。** 每个文件要有**独立的七态**（排队 / 校验中 / 上传中 / 处理中 / 成功 / 失败 / 已取消），且**一个文件失败不阻塞同批其他文件**；错误必须能回答「差多少、怎么办」——SC 3.3.1 逐字：*"If an input error is automatically detected, the item that is in error is identified and the error is described to the user in text."*、SC 3.3.3 逐字：*"If an input error is automatically detected and suggestions for correction are known, then the suggestions are provided to the user, unless it would jeopardize the security or purpose of the content."*

**与既有资产的边界**：`form-table.md` 管字段与校验时机；`feedback-states.md` 管全局反馈层级与 toast/进度条分工；`ux-writing.md §12.3` 管「文件大小」文案口径；`direct-manipulation.md` 管指针与拖拽机制；本资产只管**从「用户手里有一份文件」到「系统确认收到并可用」这条链路的设计决定**。不重复抄它们的表，只在需要时交叉引用。

---

## §1 判层：五问定「做不做、做哪一类、放哪里」

上传是**成本最高**的输入控件之一（要拍照/翻相册/找文件/等网络/可能失败）。先问五个问题，每一个都会改变做法：

| # | 五问 | 答案怎么改变方案 |
|---|---|---|
| Q1 | **文件从哪来？** 相册 / 拍照 / 本机 / 粘贴 / 拖放 / 扫码 / 第三方（云盘、微信） | 决定要不要 `capture`、要不要拖放区、要不要「从其他应用导入」入口 |
| Q2 | **用户能不能先看到结果？**（头像、封面、证件照、附件预览） | 能预览 → 必须有裁剪/旋转/重拍三段；不能预览 → 至少给文件名 + 类型图标 + 大小 |
| Q3 | **文件多大、网络多差？**（<2 MB / 2–20 MB / >20 MB；Wi-Fi/4G/弱网） | 决定进度形态、是否要断点续传、是否要客户端压缩 |
| Q4 | **失败的代价多大？**（重传一次 3 秒 vs 重填整张表） | 代价大 → 断点续传 + 后台队列 + 离开页面警告；代价小 → 就地重试即可 |
| Q5 | **有没有合规/隐私要求？**（证件、病历、合同、未成年人照片） | 决定是否本地处理不上传原图、是否水印、留存期与删除入口、EXIF 脱敏 |

### §1.1 判层表：12 个真实场景（直接对号入座）

| 场景 | 关键约束 | 必做 | 最常见错法 |
|---|---|---|---|
| 头像 / 个人资料图 | 1:1 裁切、尺寸小、要能重拍 | 相册+拍照两入口、圆形预览、拖动缩放、最小像素校验 | 只收原图不裁 → 头像被拉扁；裁完才发现太小 |
| 封面 / 头图 | 宽幅比例（16:9 或 1.91:1）、文字安全区 | 比例框 + 安全区提示 + 桌面/移动双预览 | 让用户自己记「1200×630」，不给框 |
| 证件照 / 身份证 | 比例固定、背景规范、极敏感 | 边框对齐引导、本地裁切、明确「仅用于实名，不公开」 | 原图直传 CDN、可被遍历 URL 访问 |
| 聊天 / 评论附件 | 高频、小文件、允许粘贴 | `paste` 事件直接收图、缩略图先上、原图后台传 | 每次都要点「+」→「文件」→ 找路径 |
| 后台批量导入（CSV/Excel） | 列映射、部分成功、可重下失败行 | 模板下载 + 预览前 5 行 + 失败行可导出（§6.5 四段与四条硬规则） | 传完只说「导入失败」，不说第几行、哪一列 |
| 多图商品 / 作品集 | 排序、批量、每张独立状态 | 网格缩略图 + 拖动排序 + 逐张进度 + 单张重试 | 一张失败整批回滚 |
| 视频上传 | 大文件、转码、封面帧 | 时长/大小上限前置、转码中占位、封面帧选择 | 转码中显示「完成」→ 用户马上分享空链接 |
| 音频 / 录音 | 权限、波形、时长 | 录制 → 波形 → 试听 → 上传三段 | 一按就开始传，用户没机会重录 |
| 合同 / 发票 PDF | 页数、清晰度、不可编辑 | 首页缩略图 + 页数 + 「是否清晰」自检 | 只校验扩展名 `.pdf`，收到 0 页文件 |
| 简历上传 | 解析、格式兼容、隐私 | 接受 pdf/docx + 解析预览 + 可替换 | 只收 `.doc`（用户现在都用 docx/pdf） |
| 素材/品牌资源（SVG/字体） | 安全（XSS）、许可 | SVG sanitize、字体白名单、许可勾选 | 直接把用户 SVG 内联进页面 |
| 弱网上传（现场/外勤） | 断线、切网、息屏 | 断点续传 + 「已保留进度」+ 重连自动续 | 一断就从头传，且不告诉用户 |

### §1.2 三条拒绝条件（满足任一就不该做「上传」这个交互）

1. **能用选项解决的，不要用上传**：金额、日期、归属部门这类结构化信息，让用户上传一张截图等于把解析成本转嫁给用户。
2. **必需文件说不清「传了给谁、用来干什么」**：GOV.UK 逐字 *"You should only ask users to upload something if it's critical to the delivery of your service."* 说不清就不是 critical。
3. **同一份文件可以用已有数据替代**（订单号、身份证后四位、发票代码）时，别要文件。

---

## §2 选文件：控件契约

### §2.1 `<input type="file">` 的四个属性（逐字口径）

| 属性 | 作用 | 逐字依据 | 设计含义 |
|---|---|---|---|
| `accept` | 逗号分隔的**唯一文件类型说明符**列表 | MDN：*"The `accept` attribute takes as its value a comma-separated list of one or more file types, or unique file type specifiers, describing which file types to allow."* | 只影响选择器过滤，不做校验 |
| `multiple` | 允许多选 | MDN：*"When the `multiple` Boolean attribute is specified, the file input allows the user to select more than one file."* | 多选必须配「逐文件状态」，否则一个失败无法定位 |
| `capture` | 直接调摄像头/麦克风 | MDN：*"A value of `user` indicates that the user-facing camera and/or microphone should be used. A value of `environment` specifies that the outward-facing camera and/or microphone should be used."* | `user` 自拍/证件，`environment` 拍实物/单据；桌面浏览器通常忽略 |
| `type="file"` 本身 | 系统文件选择器 | MDN：*"the file input provides a button that opens up a file picker dialog"* | 浏览器原生控件不可样式化，必须用 `<label for>` 或隐藏 input + 自定义按钮 |

**`accept` 的合法写法只有五种**（MDN 逐字列举）：

- 扩展名：*"A valid case-insensitive filename extension, starting with a period (".") character. For example: `.jpg`, `.pdf`, or `.doc`."*
- MIME 类型：*"A valid MIME type string, with no extensions."*
- `audio/*`：*"meaning 'any audio file'"*
- `video/*`：*"meaning 'any video file'"*
- `image/*`：*"meaning 'any image file'"*

**为什么扩展名和 MIME 要同时写**：同一类文件有多种标识方式。MDN 的 Word 例子逐字给出写法 `<input type="file" accept=".doc,.docx,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document">`，并说明 *"there are a number of ways Microsoft Word files can be identified"*。只写 MIME，部分系统会找不到文件；只写扩展名，macOS 的「其他格式」可能仍可选。**双写 + 服务端白名单三件套**才是完整方案（见 §3.2、§8.1）。

### §2.2 按钮与可访问标签（三条硬规则）

1. **可见文本必须是一个动宾短语**：「选择文件」「上传照片」「拍照上传」；不要「浏览…」「Upload」，更不要在按钮里写文件类型（类型写在提示里）。
2. **原生 input 的 `label` 不能省**：用 `<label for>` 关联，或把 input 设为视觉隐藏（`position:absolute; opacity:0` 之类，**不要 `display:none`**，那会让部分读屏与键盘路径失效），再把自定义按钮做成 label 的兄弟并用 `aria-describedby` 关联提示文本。
3. **提示文本写在控件上方、永久可见**：类型、大小上限、数量上限、是否有模板。USWDS 逐字：*"Use hint text to highlight input restrictions. Create an element with the `usa-hint` class to explain any file restrictions, such as document types or file size."* —— 这条比任何错误文案都重要，因为它把「选择后失败」变成「选择前就不选错」。

### §2.3 拖放区：四件事缺一不可

| 必须 | 做法 | 依据/说明 |
|---|---|---|
| ① 有「选择文件」按钮 | 拖放区下方或区内一个真按钮 | SC 2.5.7 + 本库 `accessibility.md:281` |
| ② 整页拦截 `dragover` | 否则文件在拖放区外松手时浏览器直接打开该文件，页面被替换，用户丢上下文 | 工程约定（`dragover` 必须 `preventDefault()` 才能触发 `drop`） |
| ③ `drop` 后走**同一套**校验 | 拖入和点选必须复用同一个 `validate(files)`，否则两条路径行为不一致 | 本库 `direct-manipulation.md` 的「同一件事只有一条实现」 |
| ④ 拖入态与键盘焦点态都要有视觉变化 | `:focus-visible` 与拖入 hover 同等对待，且对比度 ≥3:1 | SC 2.4.7 / 1.4.11 |

**拖放区不要做的事**：不要只写「把文件拖到这里」；不要用 `position:fixed` 全屏遮罩接管整页拖放（会干扰页面内其他拖拽，如排序、富文本）；不要在 `dragenter` 就开始上传。

### §2.4 粘贴上传（聊天/评论/工单的高频路径）

`paste` 事件里 `event.clipboardData.files` 可能直接有图片（截图粘贴）。规则：
- **只在用户已聚焦的输入区域内监听**，不要全页监听（否则用户粘贴文字也会触发上传）。
- 粘贴后先给**缩略图 + 可撤销**（避免误粘敏感截图），再开始传。
- 同时保留「选择文件」入口：不是所有平台粘贴都带 `files`（有的只带 HTML/文本），粘贴失败要静默回退到按钮路径，不弹错。

### §2.5 数量上限

- 上限要**写在提示里**：「最多 10 个文件，单个不超过 20 MB」。GOV.UK 的错误文案示例逐字给了数量口径：*"For example, 'You can only select up to 10 files at the same time'."*（这是**示例措辞**，不是法定上限，见 §14）。
- 超限的处理分两派，**必须选一派并写清**：**截断并提示**（保留前 N 个）或 **整批拒绝**。Ant Design `maxCount` 属第一派且行为特殊：官方文档逐字 *"Limit the number of uploaded files. Will replace current one when `maxCount` is `1`"*，源码对超限文件的处理是从 `fileList` 里**静默丢弃**（`// We should ignore event if current file is exceed maxCount`），组件本身不渲染错误提示 —— 用它就必须自己补提示，否则用户拖了 5 个只进去 3 个且不知道为什么。
- **单文件场景优先用「替换」语义**（头像、封面）：选新图直接替换旧图，不要累积成列表。

---

## §3 校验：三档分工与文案

### §3.1 三档校验，各管一段

| 档位 | 时机 | 管什么 | 不管什么 |
|---|---|---|---|
| **即时（客户端）** | `change` / `drop` 后立刻 | 数量、扩展名/MIME、大小、像素/时长、文件名长度 | **不能**作为安全边界（可绕过） |
| **提交前（客户端）** | 点「上传/保存」时 | 必填、许可勾选、总量汇总 | 不能替代服务端 |
| **服务端（权威）** | 收到字节后 | 真实类型（文件头/魔数）、大小、病毒扫描、内容合法性、权限 | 不该等它才发现「类型选错了」 |

**顺序纪律**：客户端拦截必须给出**与最终结果一致**的判定。若服务端更严（如只接受真实 JPEG，不接受改扩展名的 PNG），前端提示里要写清「仅支持 JPG/PNG 原始文件」，不要写「支持 image/*」。

### §3.2 类型白名单：双写 + 服务端再判

```
<input type="file" accept=".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp">
```

- **扩展名**决定选择器过滤（大小写不敏感，必须以 `.` 开头，MDN 逐字）。
- **MIME** 决定部分系统的「文件类型」下拉项。
- **服务端**按文件头判定真实类型（OWASP：*"Validate the file type, don't trust the Content-Type header as it can be spoofed"*），并**只允许业务必需的类型**（OWASP：*"List allowed extensions. Only allow safe and critical extensions for business functionality"*）。
- **HEIC/HEIF 的现实**：iPhone 默认拍 HEIC，很多浏览器 `accept="image/*"` 仍能选到但无法解码。三种做法选一：① 服务端转码；② 前端提示「iPhone 请在 设置→相机→格式 选『兼容性最佳』」（体验差，不推荐）；③ 接受 HEIC 并在上传后异步转码，界面先显示占位。**不要在 JS 里用扩展名判断能否解码**。

### §3.3 大小上限：先告知、给单位、给差额

- 上限值由业务定，但**必须在选择前可见**（§2.2 第 3 条）。
- 单位口径要固定（详见 §13.1 的代码）：`File.size` 是**字节**（MDN 逐字：*"returns the size of the `Blob` or `File` in bytes"*），但界面上用户看的是 MB。**全站统一一套换算**（十进制 MB = 10⁶ B 或二进制 MiB = 2²⁰ B），不要一处 1000 一处 1024。
- 错误文案要给「差多少」而不是只说超了：GOV.UK 示例逐字 *"For example, 'The selected file must be smaller than 2MB'."*；服务端拒绝时标准状态码是 **413**，MDN 的示例响应体逐字给了可抄的结构：`{"error": "Upload failed", "message": "Maximum allowed upload size is 4MB"}`。
- **压缩后可过关的文件，必须给出口**：「这张图片 12.4 MB，超过 8 MB 上限 → [自动压缩到 7.2 MB] [重新选择]」。只给「重新选择」等于让用户自己去装压缩工具。

### §3.4 文件名：三个必判项

OWASP 的三条逐字要求：*"Change the filename to something generated by the application"*、*"Set a filename length limit. Restrict the allowed characters if possible"*、*"Restrict use of leading periods (hidden files) and sequential periods (directory traversal)"*。

**已知绕过形态**（OWASP 逐字列举，前端校验也要拦）：
- 双扩展名 `.jpg.php`（*"where it circumvents easily the regex `\.jpg`"*）
- 空字节 `.php%00.jpg`（*"where `.jpg` gets truncated and `.php` becomes the new extension"*）
- 大小写 `.pHp` / `.phP`
- Windows NTFS 备用数据流 `shell.asp:.jpg` / `shell.php::$DATA` —— OWASP 明确 *"reject any filename containing a colon (`:`)"*

**设计侧结论**：界面上**展示用户原文件名**（让他确认传对了），但**存储名一律服务端生成**（UUID）；原文件名只作为元数据保存并做长度/字符净化。展示时截断中段（`很长的文件名…最终版.pdf`），保留扩展名。

### §3.5 图片尺寸/比例/DPI 的验收（业务规则，但要算得清）

- **像素是硬约束，DPI 是打印才需要的换算**。公式：`像素 = 英寸 × DPI`。例：要印 35×45 mm 证件照、300 DPI → 宽 35/25.4×300 ≈ 413 px、高 45/25.4×300 ≈ 531 px。**屏幕上只说像素**，说 DPI 只会让用户困惑。
- 头像最小像素建议按「显示尺寸 × 2」定（1× 显示 96 px → 至少 192 px，建议 512 px），并**在裁剪框里直接限制缩放下限**，不要等上传后报「太小」。
- 比例用**固定框 + 遮罩**表达，不要用文案写「请上传 16:9 图片」——用户不会算。
- 证件类「清晰度」无法用像素保证：给**实时预览 + 「能看清文字吗」自检勾选**，比自动判定可靠。

### §3.6 上传文案矩阵（中英对照，可直接抄）

| 场景 | ❌ 别写 | ✅ 写 |
|---|---|---|
| 类型不符 | 文件格式错误 | 仅支持 JPG、PNG，当前是 PDF。换一个文件或先导出为 JPG |
| 超大小 | 文件过大 | 这张图 12.4 MB，超过 8 MB 上限。[压缩后上传] [重选] |
| 超数量 | 数量超出限制 | 最多 10 个文件，已选 12 个。已保留前 10 个 (3/10) |
| 上传中断 | 上传失败 | 网络中断，已保留 6.2 MB / 12.4 MB。[继续上传] |
| 服务端处理失败 | 系统错误 | 文件已收到，但无法读取（可能是加密 PDF）。请另存为未加密版本再试 |
| 病毒/违规 | 非法文件 | 这个文件未通过安全检查，无法上传。如有疑问请联系 support@… |
| 等待转码 | 上传成功 | 已上传，正在生成预览（约 30 秒），完成后会通知你 |
| 权限不足 | 没有权限 | 你的账号不能上传到「财务」空间。请联系空间管理员开通 |

---

## §4 传输与进度

### §4.1 三档反馈阈值（NN/g 口径，与 `feedback-states.md` 一致）

| 时长 | 界面该给什么 | 不该给什么 |
|---|---|---|
| **< 0.1 s** | 按下态（按钮立即变化） | 任何加载指示 |
| **0.1–1 s** | 不需要额外指示器 | spinner |
| **1–10 s** | 「正在上传」明确信号（进度条或不确定型） | 静态文字「Loading…」 |
| **> 10 s** | **百分比 + 已传/总量 + 剩余时间（粗略）+ 可取消** | 无限转圈（分不清在跑还是死了） |

### §4.2 进度条规格（逐项可验收）

1. **确定性进度优先**：已知 `total`（`File.size`）就必须给百分比；未知总量（服务端先收后处理）用不确定型 + 阶段文案（「正在上传」→「正在处理」）。
2. **数值要有意义**：`3.2 MB / 8.0 MB`，不要只给 `40%`（大文件时用户更关心还剩多少）。
3. **剩余时间只给粗粒度**：`约 1 分钟`。精确到秒的倒计时必然跳变且不准，会降低可信度。
4. **必须可取消**：取消不是「隐藏」——要中止请求（`xhr.abort()` / `AbortController`）并清理服务端已收分片（若有）。
5. **多文件时逐文件进度 + 总进度**：总进度按**字节加权**，不是「已完成文件数 / 总数」。
6. **完成态不要立刻消失**：给「已上传」+ 缩略图/文件名，让用户能确认传的是哪份；批量场景给「3 个成功，1 个失败」汇总。

### §4.3 状态机：七态与播报

```
queued → validating → uploading → processing → done
                ↘ rejected（校验不过，可重选）
        uploading ↘ failed（网络/服务端，可重试） ↘ canceled（用户取消，可重试）
```

- **`rejected` 与 `failed` 必须分开文案**：前者是「你的文件不合规，改文件」，后者是「系统/网络问题，重试」。混成一个「上传失败」是这一行最常见的可用性事故。
- **`processing` 必须存在**：大图转码、视频转码、病毒扫描、PDF 解析都可能在上传完成后还要等几秒到几十秒。此时给「已上传，正在处理」并**禁止**把状态显示成完成。
- **播报**：容器 `role="status"`（隐式 `aria-live=polite`），**节流**（进度文本变化 ≤ 每 5 秒一次，否则读屏被刷屏）；完成/失败各播报一次；失败用 `aria-live="assertive"` 或 `role="alert"` 需谨慎（打断用户）。WCAG 4.1.3 逐字：*"In content implemented using markup languages, status messages can be programmatically determined through role or properties such that they can be presented to the user by assistive technologies without receiving focus."* 其示例逐字描述了进度的播报方式：*"An application displays a dynamic progress bar to indicate the status of an upgrade. The screen reader provides intermittent announcements of the progress."* —— **intermittent（间歇）** 是规范给的口径，不是「每次变化都念」。
- 进度条本体用 `role="progressbar"` + `aria-valuenow/min/max`（有确定值时），并配可见百分比文本。

### §4.4 并发与队列

- **并发数**：浏览器对同域连接数有限制，且并发上传会互相抢带宽导致每个都慢。**工程建议值：普通场景 3 个并发，弱网 1–2 个**（这不是规范值，见 §14；写进实现约定即可）。
- **串行并不更好**：一个 200 MB 视频阻塞后面 5 张小图，用户会以为坏了。**按文件大小排序并发**或**小文件优先**。
- **重试不占用并发槽位**：重试进队尾，避免一个坏文件反复卡住队列。

### §4.5 断点续传：什么时候值得，以及协议长什么样

**判断**：满足任一才做——单文件 > 10 MB、移动端/弱网为主、失败重传代价高（表单长、需重新授权）。小于 10 MB 的文件做续传是过度工程。

**tus 可恢复上传协议 1.0.0 的关键语义**（逐字，来自协议原文）：

| 要素 | 逐字/精确值 |
|---|---|
| 版本头 | *"The `Tus-Resumable` header MUST be included in every request and response except for `OPTIONS` requests. The value MUST be the version of the protocol used by the Client or the Server."*（如 `Tus-Resumable: 1.0.0`） |
| 偏移量 | *"The `Upload-Offset` request and response header indicates a byte offset within a resource. The value MUST be a non-negative integer."* |
| 总长度 | *"The `Upload-Length` request and response header indicates the size of the entire upload in bytes. The value MUST be a non-negative integer."* |
| PATCH 媒体类型 | *"All `PATCH` requests MUST use `Content-Type: application/offset+octet-stream`, otherwise the server SHOULD return a `415 Unsupported Media Type` status."* |
| 偏移不匹配 | *"If the offsets do not match, the Server MUST respond with the `409 Conflict` status without modifying the upload resource."* |
| 成功 | *"The Server MUST acknowledge successful `PATCH` requests with the `204 No Content` status."* |
| 分片大小 | 协议**没有规定字节数**：*"The Client SHOULD send all the remaining bytes of an upload in a single `PATCH` request, but MAY also use multiple small requests successively for scenarios where this is desirable."* → 分片大小是**服务端/实现**决定，不要在网上抄一个「必须 5 MB」。 |
| 上限 | *"The `Tus-Max-Size` response header MUST be a non-negative integer indicating the maximum allowed size of an entire upload in bytes."* → 上限是**服务端播报**的，前端应读取它并据此提示，而不是硬编码。 |
| 校验和扩展 | 失败三态逐字：*"1) `400 Bad Request` if the checksum algorithm is not supported by the server, 2) `460 Checksum Mismatch` if the checksums mismatch or 3) `204 No Content` if the checksums match and the processing of the data succeeded."*；服务端至少支持 SHA1（`sha1`） |
| 状态码族 | `200`（HEAD）/ `201`（POST 创建）/ `204`（PATCH、HEAD、OPTIONS、DELETE）/ `400` / `403` / `404` / `409` / `410`（过期）/ `412`（版本不支持）/ `413`（超 `Tus-Max-Size`）/ `415` / `460` |

**设计侧要落的三句话**：① 断线后重进页面要能**自动列出未完成上传**并「继续」；② 续传时必须显示「已保留 6.2 MB / 12.4 MB」，而不是从 0 开始；③ 服务端 410 过期时要明确告知「上传已过期，需重新选择文件」，不能静默重传。

---

## §5 媒体输入特化

### §5.1 图片方向：竖拍照片为什么躺倒

- 浏览器默认**已按 EXIF 转正**。MDN `image-orientation` 逐字：*"`from-image`: Default initial value. The EXIF information contained in the image is used to rotate the image appropriately."*
- 但一旦你自己解码（canvas、`drawImage`、服务端处理）就可能拿到**未转正的原始像素**，于是「预览是正的、传上去是躺的」。修法：`createImageBitmap(file, { imageOrientation: 'from-image' })` —— MDN 逐字：*"`from-image`: Image oriented according to EXIF orientation metadata, if present (default)."*；对照值 `none` 逐字是 *"Image oriented according to image encoding, ignoring any metadata about the orientation (such as EXIF metadata, that might be added to an image to indicate that the camera was turned sideways to capture the image in portrait mode)."*
- 还有一个安全细节：MDN 对 `image-orientation: none` 的警告逐字：*"**Warning:** `image-orientation: none;` **does not** override the orientation of non-secure-origin images as encoded by their EXIF information, due to security concerns."* → 别指望用 `none` 统一「不转」，跨源图片行为不一致。
- **验收动作**：准备一张 iPhone 竖拍、一张安卓竖拍、一张扫描件（可能带镜像标签），三张都要在「预览 / 裁剪 / 最终存储」三处方向一致。

### §5.2 压缩与转码：客户端还是服务端

| 方案 | 适用 | 代价 |
|---|---|---|
| 客户端 canvas/`ImageBitmap` 压缩 | 图片、单张 < 20 MP、能接受有损 | 占主线程（放 Worker）、色彩管理差异、可能丢 EXIF（这通常是好事） |
| 服务端（sharp/ImageMagick 等） | 任意尺寸、需要统一质量、需要多尺寸派生 | 带宽与算力成本、需要排队态 |
| 两者都做 | 大图先客户端降到 2560 px 长边，服务端再出多档 | 复杂度最高，但移动端体验最好 |

- **OWASP 逐字**：图片类应 *"decode and re-encode to an allowed image format, explicitly removing unnecessary metadata"*，且 *"Rewriting does not guarantee that all malicious content is removed, and the image processor itself handles untrusted input."* → 重编码 + 元数据剥离是**隐私与安全**动作，不只是省流量。
- **EXIF GPS 必须默认剥离**：用户传一张在家拍的照片，GPS 会泄露住址。剥离发生在**服务端**（客户端剥离不可信）。
- 格式选择回 `performance-design.md` 的格式矩阵，这里只定一条：**上传入口接受的面要宽（jpg/png/webp/heic），存储面要窄（webp/avif + jpg 回退）**，不要把「存储格式」当成「上传限制」。

### §5.3 裁剪：比例、安全区与重拍

| 用途 | 比例 | 额外要求 |
|---|---|---|
| 头像 | 1:1 | 圆形遮罩预览、最小像素、脸部居中提示 |
| 封面 / 头图 | 16:9 或 1.91:1 | 标题/文字安全区、桌面与移动两版预览 |
| 竖版海报 / 社媒图 | 4:5 或 9:16 | 上下留白提示（平台 UI 会压） |
| OG / 分享图 | 1.91:1 | 缩略图在信息流里的可读性（字号大） |
| 证件 | 固定 mm 比例 | 边框对齐、背景纯色、不可滤镜美化 |

**裁剪器五条验收**：① 只允许缩放/平移，**不允许把图放大到超过原图像素**（否则出马赛克）；② 裁剪结果的最小像素在框内实时校验；③ 支持旋转 90°（手机横拍）；④ 键盘/读屏可用（回 `direct-manipulation.md` 的四条路径）；⑤ **「恢复原图」入口**（裁坏了能退回）。

### §5.4 视频 / 音频

- **前置披露**：时长上限、大小上限、转码时间量级（「10 分钟视频约需 2 分钟处理」）。用户最怕的是传完才被告知超时长。
- **上传完成 ≠ 可用**：必须有 `processing` 态 + 完成通知（回 `notifications-messaging.md`）。
- **封面帧**：默认取第 1 秒（不是第 0 帧，常是黑帧），允许用户拖到任意帧。
- **录音**：录 → 波形 → 试听 → 确认上传，四段分开；权限被拒时给「去设置」与「改用上传已有文件」两条路（回 `onboarding-first-run.md` 的权限时机）。

### §5.5 预览的可访问性

- 图片预览的 `alt` 由**用户提供**（头像场景可默认「头像预览」）；纯装饰性缩略图 `alt=""`。
- 文件名是文本，不要用图片代替；类型用「PDF / 图片 / 视频」文字 + 图标（图标 `aria-hidden="true"`）。
- 删除/重试/旋转这些小图标按钮，每个都要 `aria-label`（「移除 简历.pdf」「重试上传 产品图 2」），且**带上文件名**，否则读屏用户听到 8 个「移除」。

---

## §6 失败与重试

### §6.1 十种失败，十种处理

| 失败 | 用户看到 | 可做动作 | 不要做 |
|---|---|---|---|
| 网络断开 | 「网络中断，已保留 6.2/12.4 MB」 | 自动重连续传 | 弹「上传失败」并清空列表 |
| 请求超时 | 「服务器响应超时」 | 重试（同一文件） | 无限自动重试 |
| 413 超限 | 「超过 8 MB 上限（实际 12.4 MB）」 | 压缩/重选 | 只说「失败」 |
| 415 类型不支持 | 「不支持 HEIC，请转 JPG」 | 重选/转换 | 把服务端 MIME 报文原样丢给用户 |
| 422 内容不合法 | 指出具体问题（页数/清晰度/加密） | 按提示改 | 「系统错误」 |
| 病毒/违规 | 「未通过安全检查」 | 换文件 + 申诉入口 | 暴露内部扫描引擎名 |
| 处理失败（转码/解析） | 「文件已收到，但无法读取」 | 换格式重传 + 保留原文件 | 静默把状态置成功 |
| 存储满/服务降级 | 「暂时无法接收，请稍后再试」 | 定时重试 | 让用户反复点 |
| 登录过期 | 「登录已过期，进度已保留」 | 重新登录后自动续 | 跳登录页丢上传状态 |
| 用户取消 | 「已取消」 | 重试 | 保留半截文件占位 |

### §6.2 重试策略（工程建议值，非规范）

- **指数退避**：1 s → 2 s → 4 s → 8 s，最多 3–4 次，之后转手动。
- **只对可重试错误自动重试**：网络/超时/5xx/429；**不要**对 413/415/422 自动重试（永远不会成功）。
- **幂等键**：同一文件重试要带同一个 `uploadId`，避免服务端出现两份。
- **重试时保留进度**（有续传）或**明确从头开始**（无续传），不能默默从 0 开始还显示旧进度。

### §6.3 「部分成功」的界面

多文件必须给**汇总 + 逐项**：
- 汇总：「4 个文件：3 个已上传，1 个失败」。
- 逐项：失败项有「为什么 + 重试 + 移除」，成功项有缩略图与「移除」。
- **不要整批回滚**（用户会丢掉已成功的 3 个），除非业务要求原子性（如发票批量核验）——那就必须在**开始前**说明「全部成功才生效」。

### §6.5 批量导入（CSV / Excel）：模板、预览、失败行导出

「传一个 CSV 进来」最容易做错的地方，是把「上传文件」当成了整件事。批量导入是**四段**，每段都要有出口：

| 段 | 必须给的东西 | 反例 |
|---|---|---|
| 1. 准备 | **可下载的模板**（含列名、示例行、必填标记、编码说明） | 只说「按格式上传」，用户自己猜列名 |
| 2. 上传前 | 前置提示写在控件上方：允许的扩展名（`.csv` / `.xlsx`）、大小上限、**行数上限**、有无模板 | 传完才说「超过 500 行」 |
| 3. 解析预览 | 解析后**先预览前 5 行**（映射后的字段名 + 值），让用户确认列映射再落库 | 直接入库，错列了要回滚 |
| 4. 结果 | **逐行失败清单**：行号 + 列名 + 原因；**失败行可导出**成同格式 CSV（能改完再传） | 「导入失败」，不说第几行、不说哪列 |

四条硬规则：

1. **行号从数据行起算并在导出里保留**（含表头时明确「第 1 行是表头」），否则用户对不上 Excel 行号。
2. **部分成功是默认，不是例外**：成功行照常生效，失败行单独重传；要原子性就必须在上传前声明「全部成功才生效」。
3. **失败行导出的 CSV 必须能原样再导入**（同一列顺序、同一编码），这是「重试」在批量场景的唯一可用形态。
4. **编码显式声明**：给 Excel 用户的模板写 UTF-8 with BOM，并在提示里写清「请保持 UTF-8」；GBK 文件要能识别并给「请另存为 UTF-8」的具体动作。

Excel 与 CSV 的分工：`.xlsx` 适合有多 sheet 或需要格式说明；`.csv` 适合系统导出/再导入的往返（本库 §3.2 的类型校验对两者都要在**服务端**重做，客户端只做「能不能打开 + 行数估读」）。

### §6.4 离开页面的三种处理

| 情况 | 处理 |
|---|---|
| 上传中关闭/刷新 | `beforeunload` 提示（有未完成上传时）；有续传则提示「进度已保留」 |
| 上传中切换步骤 | 后台继续 + 全局进度条（回 `feedback-states.md` 的全局反馈层） |
| 上传完成但未保存表单 | 明确「文件已上传，别忘了点保存」 |

---

## §7 无障碍：上传是最容易漏键盘的一条链路

### §7.1 键盘全链路（逐段验收）

1. `Tab` 能到「选择文件」按钮，`Enter`/`Space` 打开系统选择器。
2. 选择器关闭后焦点回到按钮（不要丢到 body）。
3. 文件列表可 `Tab` 遍历，每项的可操作按钮可聚焦。
4. 「取消上传」「重试」「移除」都能键盘触发。
5. **拖放区不是唯一入口**（SC 2.5.7）。
6. 没有键盘陷阱；`Escape` 不关闭整个上传（除非在弹窗内）。

### §7.2 读屏播报清单

| 时机 | 播报 | 方式 |
|---|---|---|
| 选择完成 | 「已选择 2 个文件：简历.pdf，2.1 MB；作品集.png，8.4 MB」 | `role="status"` |
| 进度 | 「正在上传，45%」每 5 秒最多一次 | `role="progressbar"` + 节流 |
| 单个完成 | 「简历.pdf 上传完成」 | `role="status"` |
| 失败 | 「简历.pdf 上传失败：超过 2 MB 上限」 | `role="alert"`（一次） |
| 全部完成 | 「4 个文件已上传，1 个失败」 | `role="status"` |

**错误关联**：错误文本用 `aria-describedby` 绑到对应输入/文件项，且**把焦点移到第一个错误项**（多文件时移到失败项，不要移到页面顶部）。

### §7.3 目标尺寸

SC 2.5.8（AA）逐字：*"The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except when:"*，例外之一是间距：*"Undersized targets (those less than 24 by 24 CSS pixels) are positioned so that if a 24 CSS pixel diameter circle is centered on the bounding box of each, the circles do not intersect another target or the circle for another undersized target;"*。同一文档还说明：*"the Working Group settled on the smaller measure of 24 by 24 CSS pixels for the \"(Minimum)\" version of this criterion, while 2.5.5 Target Size (Enhanced) uses the larger 44 by 44 CSS pixel measure as its threshold size."*

→ 上传行里的 `×` 删除、`↻` 重试、`✎` 编辑**至少 24×24**，移动端按 **44×44** 设计（`direct-manipulation.md` 的目标尺寸三口径一致）。

### §7.4 对比度与动效

- 进度条已完成段与轨道 ≥ **3:1**（SC 1.4.11 非文本对比）；进度百分比文字 ≥ **4.5:1**。
- 上传中的呼吸/流光动画要能 `prefers-reduced-motion` 降级为静态进度。
- 不要用颜色单独区分成败（成功绿 / 失败红 + 图标 + 文字，SC 1.4.1）。

---

## §8 安全与隐私：客户端做体验，服务端做边界

### §8.1 服务端六条（OWASP File Upload Cheat Sheet 原文口径）

1. **白名单扩展名**，只留业务必需：*"List allowed extensions. Only allow safe and critical extensions for business functionality"*
2. **不信任 `Content-Type`**：*"Validate the file type, don't trust the Content-Type header as it can be spoofed"*
3. **文件名由系统生成**：*"Change the filename to something generated by the application"*
4. **有大小上限**：*"Set a file size limit"*
5. **存在 webroot 外或另一台机器**：*"Store the files on a different server. If that's not possible, store them outside of the webroot"*
6. **过一遍杀毒/沙箱**：*"Run the file through an antivirus or a sandbox if available to validate that it doesn't contain malicious data"*

补充两条工程要求：解压后再算大小（防 ZIP 炸弹，OWASP 明确 *"the file size limit should be considered after file decompression is conducted"*）；上传目录禁用逐目录配置覆盖（防 `.htaccess` / `web.config` 注入）。

### §8.2 客户端三条

1. **SVG 必须 sanitize**（`<script>`、`on*`、`<foreignObject>`、外部引用），否则等于让用户往你页面里注入脚本；能栅格化就别内联。
2. **不把原图原样公开**：文件名随机化 + 私有桶 + 签名 URL（有效期最短），禁止「按自增 ID 遍历」的公开 URL。
3. **上传前告知**：用途、保存多久、谁能看到、怎么删。敏感证件类附「仅用于实名核验，30 天后自动删除」这类具体承诺，而不是「我们会保护您的隐私」。

### §8.3 直传（前端直传对象存储）的最小权限模型

- 服务端签发**一次性、限大小、限类型、限路径前缀、限有效期**的凭证（预签名 POST/PUT）。
- 前端不持有长期密钥；上传完成后由服务端**回调确认**再落库（否则用户可伪造「已完成」）。
- 直传失败的重试与续传由客户端负责，**但最终是否可用以服务端校验为准**。

---

## §9 库选型：GitHub API 实测（2026-11-16）

数字全部来自 `GET https://api.github.com/repos/{owner}/{repo}` 实时返回（`stargazers_count` / `license.spdx_id` / `pushed_at` / `archived`）：

| 库 | Star | 许可 | 最近推送 | 定位 |
|---|---|---|---|---|
| transloadit/uppy | 31,075 | MIT | 2026-11-16 | 全家桶：多源（相机/云盘/URL）、断点续传（tus）、仪表盘 UI |
| react-dropzone/react-dropzone | 11,024 | MIT | 2026-11-15 | 只要 dropzone 行为 + 键盘可达的 React 钩子 |
| pqina/filepond | 16,396 | MIT | 2026-11-11 | 自带精美 UI、图片裁剪/滤镜、异步上传 |
| fengyuanchen/cropperjs | 13,918 | MIT | 2026-11-15 | 纯裁剪器（旋转/缩放/比例框） |
| dropzone/dropzone | 18,408 | NOASSERTION（API 返回 "Other"） | 2026-11-01 | 经典拖放上传组件；注意 API 的 `full_name` 已解析为 `enyo/dropzone` |
| tus/tus-js-client | 2,640 | MIT | 2026-11-15 | tus 1.0.0 客户端，只管续传协议 |
| GoogleChromeLabs/squoosh | 26,195 | Apache-2.0 | 2026-10-22 | 图片压缩（含 WASM 编解码），可学其参数 |
| lovell/sharp | 32,855 | Apache-2.0 | 2026-11-16 | 服务端图像处理（多尺寸派生、剥离 EXIF） |

**选型决策树**：
1. 需要「从 Google Drive / Dropbox / 相机 / URL 取文件」→ **uppy**。
2. 只要拖放行为且自己画 UI → **react-dropzone**（React）或原生 `dragover/drop` 自己写。
3. 要开箱即用的漂亮上传 + 图片编辑 → **filepond**（注意打包体积与许可）。
4. 只要裁剪 → **cropperjs**。
5. 文件 > 10 MB 且要续传 → **tus-js-client**（配 tus 服务端；不要自己发明 offset 协议）。
6. 图片压缩/多尺寸 → 服务端 **sharp**；浏览器内 → **squoosh** 的编解码思路。

**Ant Design `Upload` 的精确 props**（文档原文，写契约前必须知道）：

| prop | 类型/默认 | 关键语义（逐字） |
|---|---|---|
| `accept` | string | 同原生；v6 起支持 `AcceptObject {format, filter}` |
| `multiple` | boolean，默认 `false` | — |
| `maxCount` | number | *"Limit the number of uploaded files. Will replace current one when `maxCount` is `1`"*；超限**静默丢弃**且不渲染提示（实现注释：`// We should ignore event if current file is exceed maxCount`） |
| `beforeUpload` | 返回 `boolean \| Promise<File> \| Upload.LIST_IGNORE` | *"Uploading will be stopped with `false` or a rejected Promise returned. When returned value is `Upload.LIST_IGNORE`, the list of files that have been uploaded will ignore it."* |
| `listType` | `text`（默认）/ `picture` / `picture-card` / `picture-circle` | 决定列表形态 |
| `progress` | `{ strokeWidth: 2, showInfo: false }` | 想显示百分比必须显式开 |
| `customRequest` | `(options, info) => void \| { abort }` | 接直传/续传的入口 |

⚠️ **该组件没有「大小上限」prop**：必须在 `beforeUpload` 里自己判 `file.size`（本库实测，属使用注意，不是规范）。

---

## §10 场景速查（12 行，直接查表）

| 需求说法 | 先判什么 | 落点 |
|---|---|---|
| 「加个上传按钮」 | Q1 来源 + Q2 预览 | §2.1 属性三件套 + §2.2 标签与提示 |
| 「支持拖拽上传」 | 有没有单指针替代 | §2.3 四件事 + SC 2.5.7 |
| 「只让传图片」 | 前端提示 vs 服务端判定 | §3.2 accept 双写 + §8.1 |
| 「限制 10 MB」 | 提示位置 + 单位 + 差额文案 | §3.3 + §13.1 |
| 「大文件传一半断了」 | 是否 > 10 MB / 弱网 | §4.5 tus + §6.2 |
| 「进度条怎么画」 | 时长分档 | §4.1 + §4.2 |
| 「传完是横的」 | EXIF | §5.1 |
| 「头像怎么裁」 | 比例 + 最小像素 | §5.3 + §13.6 |
| 「多图怎么显示」 | 逐文件状态 | §4.3 + §6.3 |
| 「用户传了病毒/违规文件」 | 服务端边界 | §8.1 + §8.2 |
| 「读屏用户能不能上传」 | 播报与替代路径 | §7.1 + §7.2 |
| 「该用哪个库」 | 需求面 | §9 决策树 |

---

## §11 反模式（20 条，评审直接对照）

1. 只有拖放区，没有「选择文件」按钮。
2. `accept` 写了就当做了校验，服务端不复核。
3. 大小上限写在错误文案里，提示区不写。
4. 只说「文件太大」，不说实际大小和上限。
5. 多文件共用一个进度条，不知道哪个失败了。
6. 一个文件失败，整批回滚并清空。
7. 把「上传完成」当「可以使用」（缺 `processing` 态）。
8. 上传中不允许取消，或取消只是隐藏。
9. 断线后进度归零且不告知。
10. 用无限转圈展示 200 MB 上传。
11. 进度百分比用「已完成文件数 / 总数」（大小差 100 倍时严重失真）。
12. 竖拍照片存成躺倒（未处理 EXIF）。
13. 头像不裁剪，直接拉伸成正方形。
14. 裁剪器允许放大超过原图像素。
15. 只接受 `.doc` 或只接受旧的 `.xls`。
16. 存储名直接用用户文件名（路径穿越 / 覆盖 / XSS）。
17. 上传目录可执行脚本、或在 webroot 内直读。
18. 公开 URL 可被遍历（自增 ID / 原始文件名）。
19. SVG 原样内联或原样当图片返回。
20. 保留 EXIF GPS 与设备信息。

---

## §12 自检清单（20 项，交付前逐条打勾）

- [ ] 1 提示区写清了类型、大小、数量、模板（若需）？
- [ ] 2 有「选择文件」按钮，且拖放不是唯一路径？
- [ ] 3 `accept` 同时写了扩展名与 MIME，且与服务端白名单一致？
- [ ] 4 服务端按文件头判定类型，不只信 `Content-Type`？
- [ ] 5 大小上限在**选择前**可见，错误文案含实际值与上限？
- [ ] 6 有「压缩后上传」这类补救出口（图片场景）？
- [ ] 7 多文件逐项状态，失败项可单独重试？
- [ ] 8 七态状态机齐全，`rejected` 与 `failed` 文案分开？
- [ ] 9 1 s / 10 s 两档反馈阈值落实（<1 s 不加 spinner；>10 s 有百分比+取消）？
- [ ] 10 进度用 `role="progressbar"` + `aria-valuenow`，且文本节流 ≤5 s 一次？
- [ ] 11 完成/失败有 `role="status"` / `role="alert"` 播报？
- [ ] 12 上传中可取消，且真的中止请求与清理分片？
- [ ] 13 大文件（>10 MB）有续传或至少「已保留进度」提示？
- [ ] 14 竖拍/横拍/扫描件三种图片来源方向都正确？
- [ ] 15 预览 `alt` 合理，图标按钮 `aria-label` 带文件名？
- [ ] 16 删除/重试按钮 ≥24×24（移动端 44×44），键盘可达？
- [ ] 17 上传中离开页面有提示，或后台继续 + 全局进度？
- [ ] 18 SVG 已 sanitize，EXIF GPS 已剥离，存储 URL 不可遍历？
- [ ] 19 敏感文件有用途/留存/删除说明？
- [ ] 20 弱网下重试退避生效，且不会自动重试 413/415/422？

---

## §13 可跑代码（`python -I -X utf8` 实跑通过）

### §13.1 大小上限判定与单位格式化

```python
UNITS = [("GB", 10**9), ("MB", 10**6), ("KB", 10**3)]

def human_size(nbytes, binary=False, digits=1):
    base = 1024 if binary else 1000
    names = ["B", "KiB", "MiB", "GiB"] if binary else ["B", "kB", "MB", "GB"]
    v = float(nbytes)
    i = 0
    while v >= base and i < len(names) - 1:
        v /= base
        i += 1
    return ("%d B" % nbytes) if i == 0 else ("%.*f %s" % (digits, v, names[i]))

def check_size(nbytes, limit_bytes):
    """返回 (ok, 用户可读的实际值, 差额)。差额只在超限时有值。"""
    ok = nbytes <= limit_bytes
    return ok, human_size(nbytes), (None if ok else human_size(nbytes - limit_bytes))

# iPhone 竖拍原图约 3.4 MB；上限 2 MB
ok, actual, over = check_size(3_400_000, 2_000_000)
assert ok is False and actual == "3.4 MB" and over == "1.4 MB"
assert check_size(1_999_999, 2_000_000)[0] is True
# 同一份 12,400,000 B 的两种口径：十进制 12.4 MB / 二进制 11.8 MiB（差 4.86%）
assert human_size(12_400_000) == "12.4 MB"
assert human_size(12_400_000, binary=True) == "11.8 MiB"
print("13.1 PASS", actual, over, human_size(12_400_000, binary=True))
```

### §13.2 `accept` 解析 + 前后端白名单一致性检查

```python
WILDCARDS = {"audio/*", "video/*", "image/*"}

def parse_accept(value):
    """按 MDN 的 5 种唯一文件类型说明符解析；返回 (exts, mimes, wildcards)。"""
    exts, mimes, wild = set(), set(), set()
    for raw in value.split(","):
        tok = raw.strip()
        if not tok:
            continue
        low = tok.lower()
        if low in WILDCARDS:
            wild.add(low)
        elif low.startswith("."):
            if len(low) < 2 or "/" in low or " " in low:
                raise ValueError("非法扩展名: %r" % tok)
            exts.add(low)
        elif "/" in low:
            mimes.add(low)
        else:
            raise ValueError("既不是扩展名也不是 MIME: %r" % tok)
    return exts, mimes, wild

def audit_accept(accept, server_allowed):
    """服务端只认 server_allowed（扩展名集合）。返回需要人工确认的问题列表。"""
    exts, mimes, wild = parse_accept(accept)
    problems = []
    if wild:
        problems.append("通配 %s 会让用户选到无法解码的格式" % sorted(wild))
    if exts - server_allowed:
        problems.append("前端允许但服务端不接受: %s" % sorted(exts - server_allowed))
    if not exts and mimes:
        problems.append("只写了 MIME：部分系统按扩展名过滤，会看不到可选文件")
    if exts and not mimes:
        problems.append("只写了扩展名：macOS『所有文件』仍可能选中错误类型")
    return problems

p = audit_accept(".jpg,.jpeg,.png,image/*", {".jpg", ".jpeg", ".png"})
assert any("通配" in x for x in p) and any("只写了扩展名" in x for x in p)
p2 = audit_accept(".jpg,.pdf,application/pdf", {".jpg"})
assert any("服务端不接受" in x for x in p2) and any(".pdf" in x for x in p2)
assert audit_accept(".jpg,.png,image/jpeg,image/png", {".jpg", ".png"}) == []
print("13.2 PASS", p2)
```

### §13.3 三档反馈阈值判定（给 elapsed 输出该显示什么）

```python
def feedback_for(elapsed_s, known_total=True, can_cancel=True):
    if elapsed_s < 0.1:
        return "pressed-only"
    if elapsed_s < 1.0:
        return "no-indicator"
    if elapsed_s <= 10.0:
        return "spinner-or-progress"
    if not known_total:
        return "indeterminate+cancel"
    return "percent+cancel" if can_cancel else "percent+WARN-no-cancel"

assert feedback_for(0.05) == "pressed-only"
assert feedback_for(0.5) == "no-indicator"
assert feedback_for(3) == "spinner-or-progress"
assert feedback_for(45) == "percent+cancel"
assert feedback_for(45, can_cancel=False) == "percent+WARN-no-cancel"   # SC 2.2.1 风险
print("13.3 PASS")
```

### §13.4 文件名净化（OWASP 规则的最小实现）

```python
import re, unicodedata

RESERVED = {"CON", "PRN", "AUX", "NUL"} | {"COM%d" % i for i in range(1, 10)} | {"LPT%d" % i for i in range(1, 10)}

def sanitize_name(name, max_len=80):
    """只用于『展示 + 元数据』；存储名必须由服务端生成 UUID。"""
    n = unicodedata.normalize("NFKC", name).strip()
    n = n.replace("\\", "/").split("/")[-1]        # 去路径
    n = n.replace(":", "")                          # NTFS 备用数据流 shell.asp:.jpg
    n = "".join(ch for ch in n if ch.isprintable())  # 控制字符 / 空字节
    n = re.sub(r"[<>\"'`|?*\x00-\x1f]", "", n)       # Windows 非法字符
    stem, dot, ext = n.rpartition(".")
    if not dot:
        stem, ext = n, ""
    stem = stem.lstrip(". ").rstrip(" .")            # 隐藏文件 / 尾随点
    if stem.upper() in RESERVED:
        stem = "_" + stem
    if len(stem) + len(ext) + 1 > max_len:
        keep = max_len - len(ext) - 2
        stem = stem[:keep] + "…"
    return (stem + ("." + ext if ext else "")) or "file"

assert sanitize_name("../../etc/passwd") == "passwd"
assert sanitize_name("report.jpg.php") == "report.jpg.php"     # 双扩展名：服务端白名单再拦
assert sanitize_name("shell.asp:.jpg") == "shell.asp.jpg"      # 冒号已去
assert sanitize_name("CON.txt").startswith("_CON")
assert len(sanitize_name("长" * 200 + ".pdf", 20)) <= 20
print("13.4 PASS")
```

### §13.5 重试退避 + 是否值得续传

```python
RETRYABLE = {408, 429, 500, 502, 503, 504}

def backoff_delays(attempts=4, base=1.0, cap=30.0):
    out, d = [], base
    for _ in range(attempts):
        out.append(round(d, 1))
        d = min(d * 2, cap)
    return out

def should_retry(status):
    return status in RETRYABLE

def needs_resumable(size_bytes, mobile_share=0.5, threshold_bytes=10 * 1024 * 1024):
    return size_bytes > threshold_bytes or (mobile_share >= 0.5 and size_bytes > 2 * 1024 * 1024)

assert backoff_delays() == [1.0, 2.0, 4.0, 8.0]
assert should_retry(503) and should_retry(429)
assert not should_retry(413) and not should_retry(415) and not should_retry(422)
assert needs_resumable(200 * 1024 * 1024) is True
assert needs_resumable(1 * 1024 * 1024) is False
print("13.5 PASS", backoff_delays())
```

### §13.6 裁剪比例 / 最小像素验收

```python
def crop_check(src_w, src_h, ratio_w, ratio_h, min_output_px):
    """返回 (是否可裁, 最大可用输出宽, 提示)。只允许缩小，不允许放大。"""
    if src_w <= 0 or src_h <= 0:
        return False, 0, "图片尺寸无效"
    target = ratio_w / ratio_h
    if src_w / src_h > target:
        out_w = int(src_h * target)          # 高度受限
    else:
        out_w = src_w                        # 宽度受限
    if out_w < min_output_px:
        return False, out_w, "原图太小：最多能裁出 %d px，需要至少 %d px" % (out_w, min_output_px)
    return True, out_w, "可裁切，最大输出宽 %d px" % out_w

ok, w, msg = crop_check(1200, 1600, 1, 1, 512)
assert ok and w == 1200
ok2, w2, msg2 = crop_check(400, 400, 1, 1, 512)
assert not ok2 and w2 == 400 and "原图太小" in msg2
print("13.6 PASS", msg, "/", msg2)
```

---

## §14 取源限制（本轮实测，逐条登记）

1. **WHATWG HTML 规范 `file-upload-state-(type=file)` 无法机读**：`https://html.spec.whatwg.org/multipage/input.html#file-upload-state-(type=file)` 与 `https://html.spec.whatwg.org/dev/input.html` 均 HTTP 200 但正文被取源工具丢弃（"HTML content omitted: unable to convert safely"）。因此 `accept` 的规范级语法（unique file type specifiers 的 MUST 措辞）本轮**未取到逐字原文**，只用了 MDN 的等价表述；不臆造规范级措辞。
2. **WHATWG MIME Sniffing 标准同样不可读**（同上症状，`raw.githubusercontent.com/whatwg/mimesniff/main/mimesniff.bs` 也 fetch failed）。「不信任 `Content-Type`」改用 OWASP Cheat Sheet 的逐字表述承载，未引用 mimesniff 文本。
3. **EXIF 8 值方向表未取到官方原文**：CIPA DC-008 为 PDF/需人工下载，`developer.android.com` 的 `ExifInterface` 页 fetch failed。因此本资产**不给 1–8 数值映射表**，只写「浏览器默认按 EXIF 转正、自解码会丢」这一被 MDN `image-orientation` 与 `createImageBitmap` 双重证实的机制；旋转角度数值属未取到项，不编造。
4. **IEC 二进制前缀官方页 202 空正文**：`https://www.iec.ch/si/binary.htm` 返回 HTTP 202 且无正文。因此 §13.1 只用**算术**给出两种口径（10³ / 2¹⁰）与其差异，不声称「法定必须用 KiB」。
5. **GOV.UK 的 2 MB / 10 个是错误文案示例**，不是强制上限（原文用法是 *"For example, …"*）。要写进自家规范前必须用业务上限替换。
6. **USWDS File input 的分数**（15 tests / 13 passed / 2 exceptions、WCAG 2.1 AA）来自其组件页的状态徽标，取源时页面已渲染，但该分数会随版本变动，引用时须注明日期。
7. **Material 3 无文件上传专用组件页**（`m3.material.io/components` 只渲染出 shell），本轮未引用 M3 上传规范。
8. **`tus` 协议没有规定分片字节数**：网传「必须 5 MB / 必须 256 KiB」等说法在协议原文中不存在，本资产已按原文写明「SHOULD 一次传完剩余字节，MAY 分多次」，分片值交服务端与实现决定。
9. **并发数 3、退避 1/2/4/8 s、最小头像 512 px、>10 MB 才续传**均标注为**工程建议值**，无官方来源，不得当成规范引用。
10. **Ant Design 版本口径**：`upload` 文档页为 JS-only 空正文，props 取自其仓库 `components/upload/index.en-US.md`（master = v6 线），`AcceptObject` 为 6.4.0 起；接老版本前须回对应版本文档核对。
11. **dropzone 仓库已迁移**：`api.github.com/repos/dropzone/dropzone` 返回 301 后解析为 `enyo/dropzone`，许可字段为 `NOASSERTION`（页面写 "Other"），选型时按实际仓库与许可页复核。
12. **本条为边界声明**：本资产不覆盖「上传后的内容审核流程」「CDN 与存储成本」「服务端队列架构」，只到「系统确认收到且可用」为止；这些内容不在本库任何资产内，属实现侧。
