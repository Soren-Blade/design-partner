# 视频播放器与字幕（Video Player UX & Captions / Subtitles / WebVTT）

> 快照 2026-11-17 · 每日升级 #44（v47→v48）· 主题：Video Player UX / Control Bar / Timeline & Scrub / WebVTT / Captions & Subtitles / Autoplay Policy / Fullscreen & PiP
> 取源：Netflix Timed Text Style Guide（General Requirements 2022-10-07 / Subtitle Timing Guidelines 2025-07-04 / English (USA) 2026 现行版）· W3C WCAG 2.2 Understanding（SC 1.2.2 / 1.4.3 / 2.2.2 / 2.5.8）· WebKit 官方博客 *New &lt;video&gt; Policies for iOS*（Jer Noble，2016-07-25）· GitHub API 实测 5 个播放器仓库（2026-11-17）。规范数值逐字引原文；无官方来源的尺寸与时长一律标「工程约定」。
>
> **边界纪律（先读这段，避免误路由）**：本文件只管「视频怎么被播放、被拖动、被配字幕、被无障碍地看完」。**视频文件怎么选/怎么传/怎么校验**归 `file-upload-media-input.md` §5.4；**播放/暂停这类过渡动画的曲线与时长**归 `motion-orchestration.md` §10.2（WAAPI 播放控制）；**提示音与触觉**归 `sound-haptics-feedback.md`（含 §5.2「短音效不要自建播放器」）；**字幕文案怎么翻译、复数与截断**归 `i18n-localization.md`；**WCAG 全量 86 条口径与焦点样式**归 `accessibility.md`（本文件只补 1.2.2 / 2.2.2 / 2.5.8 / 1.4.3 在播放器里的落地）；**手势与拖拽的通用命中区规则**归 `direct-manipulation.md`；**播放页的加载/缓冲五态**归 `feedback-states.md`；**首帧体积与媒体性能预算**归 `performance-design.md`。

---

## §0 一句话立场

**播放器不是「把一个视频塞进页面」，是一份关于时间的契约：任何时刻用户都要能回答「现在播到哪、我能不能倒回去、听不见或看不见时怎么补上」。**

三条裁决：

1. **控件层是契约层，`<video controls>` 不是设计。** 原生控件不能改顺序、不能加字幕菜单与画质菜单，静音/全屏按钮的语义还各浏览器不同；一旦要「字幕可选、倍速可选、章节可跳」，就必须自建控件层（或 media-chrome 这类 web components 控件层）并把原生控件关掉——**只保留 `playsinline`、`preload`、`muted` 这类策略属性**，其余表现全部自己负责。
2. **字幕是内容，不是样式。** 42 字符/行、每屏 2 行、成人 20 CPS / 儿童 17 CPS、最短 5/6 秒、最长 7 秒、相邻间隙 2 帧——这是硬约束，设计师不能凭美感突破。用户投诉「字幕看不清 / 跟不上 / 一闪就没」，九成是数值违规，不是字体丑。
3. **默认不自动播放有声视频。** 允许自动播放的只有两种形态：**静音**或**源本身无音轨**，且必须「可见才播、不可见就暂停」（WebKit 原文），并同时提供暂停机制（WCAG 2.2.2 的五秒门槛）。为了「页面有动感」而自动播放带声音的视频，是把留存赌在用户的忍耐上。

判层先答三问（§1），再选架构（§2），最后才调控件与字幕样式（§3–§9）。**顺序不能换**：先把控制栏画漂亮，再回头问「字幕数据从哪来、CPS 超没超」，一定会给已经画好的界面找理由。

---

## §1 七层判层：从「怎么装」到「看没看完」

播放器是一条会失败的链路。先把问题定位到层，再决定改编码、改控件、改时间轴、改字幕还是改策略。

| 层 | 这一层回答 | 典型失败 | 主要归属 |
|---|---|---|---|
| **L1 媒体层** | 字节怎么变成可播的流？起播多快？ | 首帧 3 秒以上；HLS 在 Safari 播、Chrome 黑屏；总时长显示了但拖不动 | §2 / §4 |
| **L2 控件层** | 谁能操作、操作入口在哪、触摸够不够大？ | 只用原生控件导致无法加字幕菜单；按钮 32×32，手机上点不中 | §3 |
| **L3 时间层** | 现在在哪、能倒回多少、拖动时看到什么？ | 拖动无反馈；缓冲期显示的黑屏；直播没有 DVR 窗 | §4 |
| **L4 文本层** | 说的是什么：字幕、章节、转录？ | 有字幕没说怎么开；字幕被控制栏挡住；CPS 超标跟不上 | §5–§7 |
| **L5 策略层** | 什么时候它自己动：自动播、画中画、全屏？ | 有声自动播被浏览器拦成静音黑屏；iOS 不进全屏就播不了 | §8 |
| **L6 无障碍层** | 不用鼠标、不用耳朵，能不能看完？ | 键盘按空格滚页面而不是暂停；无 caption 只有音轨；对比度不足 | §9 |
| **L7 度量层** | 看完没、在哪掉？ | 用「播放次数」当完成率；不看 quartile 与 seek 分布 | §9 结尾 |

**判层三问**：

1. 用户抱怨的是「找不到按钮」还是「时间对不上」？——前者在 L2，后者在 L3/L4，修法相反：一个改构型，一个改数据。
2. **关掉声音、只用键盘**，能不能完成「找到某一句并重看」？答不上来，说明 L4 与 L6 都没设计完。
3. 首屏会自动播放吗？会 → 必须同时过 L5 的三条硬条件（静音/无音轨、可见、可暂停），否则直接降级为「点击播放 + 海报图」。

---

## §2 架构选型：三种路线与它们能承诺的话

| 路线 | 承诺什么 | 不承诺什么 | 何时选 |
|---|---|---|---|
| **A 原生 `<video controls>`** | 零代码、平台一致的系统控件、iOS 上唯一完全可控的方案 | 控件顺序/图标/菜单（字幕、画质、倍速）一律不可改；各浏览器外观与键盘行为不一致 | 单视频内容页（博客、落地页、说明书内嵌）、原型、移动端为主且不需要字幕菜单 |
| **B 自建控件层**（HTML/CSS + 少量 JS，如 media-chrome 的 web components） | 完全可控的构型、命中区、字幕菜单、章节、品牌化 | 需要自己做状态机、键盘、ARIA、缓冲态与移动端手势 | **大多数产品界面**：需要品牌一致、需要字幕/画质/倍速菜单 |
| **C 完整播放器框架**（video.js / shaka-player） | 插件生态、广告、DRM、HLS/DASH 适配、成熟键盘与 ARIA | 样式侵入强、升级成本高、体积大 | 有 DRM 或广告需求、需要 DASH/HLS 多协议、团队没有媒体工程能力 |

GitHub API 实测（`api.github.com/repos/*`，2026-11-17 取，全部 `archived: false`）：

| 仓库 | star | forks | license | pushed_at | 关键事实 |
|---|---|---|---|---|---|
| `videojs/video.js` | 40,211 | 7,503 | `NOASSERTION`（API name "Other"） | 2026-11-17 | v10 起明确面向 HTML + React，生态最全，**license 需人工核对**（不是标准 SPDX 标识） |
| `sampotts/plyr` | 29,985 | 3,097 | MIT | 2026-10-21 | 官方 description 逐字含 *"Deprecated in favour of Video.js 10; security updates only."* → **新项目不要选**，老项目只做安全升级 |
| `muxinc/media-chrome` | 2,772 | 130 | MIT | 2026-11-12 | web components 控件层，最贴「设计可控」这条路；不管流协议 |
| `shaka-project/shaka-player` | 8,283 | 1,626 | Apache-2.0 | 2026-11-17 | DRM / DASH 强项，许可最干净 |
| `video-dev/hls.js` | 17,058 | 2,782 | `NOASSERTION`（API name "Other"） | 2026-11-17 | HLS 在 MSE 浏览器上的事实标准；只管流不管 UI |

**选型结论（可直接抄）**：

- 需要「字幕菜单 + 品牌控件 + 无 DRM」→ **路线 B**：`<video>` + media-chrome（或自写控件层）+ hls.js 按需。
- 需要 DRM / 多协议 / 广告 → **路线 C**：shaka-player（许可证最干净）或 video.js v10（生态最全，但先核对 license）。
- 只要展示一个视频、不需要任何菜单 → **路线 A**，但必须补 `playsinline`（§8），否则 iPhone 上点播即强制全屏。
- **plyr 不进入任何新方案**：description 里已写明弃用，抄它的样式可以，选它当依赖不行。

---

## §3 控制栏构型：控件顺序、隐藏时机与命中区

### 3.1 控件顺序（从左到右，桌面）

`播放/暂停 → 音量 → 已播/总时长 → 进度条（弹性占满）→ 字幕 → 设置（倍速/画质）→ 画中画 → 全屏`

理由：**高频动作在外侧、低频动作在右侧收拢**——「播放/暂停」与「进度条」是唯一两个每次观看都要用的控件，其余都是「设置一次就不动」的。

窄屏（< 480 CSS px）合并规则：

- 音量按钮收进「设置」，只留播放、进度、字幕、全屏；
- 时间显示二选一：`当前` 或 `剩余`（不并排显示 `00:12 / 03:40`，会挤掉进度条）；
- 字幕按钮必须仍在**一级控件**上（不能收进设置菜单）——听障用户找不到字幕开关等于没有字幕。

### 3.2 自动隐藏状态机

| 状态 | 进入条件 | 退出条件 | 表现 |
|---|---|---|---|
| `visible` | 指针移动 / 触摸 / 键盘聚焦控件 / 暂停 / 打开菜单 | 播放中 2.5–3 s 无上述事件 | 控制栏 + 进度条完全显示 |
| `hidden` | 播放中且无交互 | 任一交互 | 淡出（≤150 ms），视频不缩放 |
| `pinned` | 暂停 / 焦点在控件内 / 菜单打开 / 指针停在控制栏上 | 恢复播放且失焦 | 永不隐藏 |

三条硬规则：

1. **暂停时永不自动隐藏**——用户暂停就是为了找东西，把控件藏起来是最常见的播放器缺陷。
2. **键盘焦点在控件内时永不隐藏**（否则 Tab 到一半控件消失，焦点丢失）。
3. **隐藏时不改变视频布局**（用透明度，不要用 `display:none` 顶掉高度），否则画面会跳一下。

### 3.3 尺寸与命中区

| 元素 | 工程约定（非规范值） | 规范下限（可引用） |
|---|---|---|
| 控件条高度 | 桌面 44–48 px；触摸设备 48–56 px | 控件命中区 ≥ 24×24 CSS px（WCAG 2.5.8 AA），推荐 44×44（WCAG 2.5.5 AAA） |
| 进度条视觉轨道 | 4–6 px，悬停加粗到 6–8 px | 同上，实际可点区域高 ≥ 24 px（用上下 padding 扩，不靠加粗轨道） |
| 进度条滑块 | 直径 12–14 px（仅悬停/拖动时显示） | 同上 |
| 图标按钮 | 图标 20–24 px，按钮 40–44 px | 同上 |
| 控件与画面间距 | 底部内边距 8–12 px | — |

> 引用依据：SC 2.5.8 原文 *"The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except when:"*；Understanding 文档 Intent 段明确 *"2.5.5 Target Size (Enhanced) uses the larger 44 by 44 CSS pixel measure"*，且 *"The requirement is independent of the zoom factor of the page"*。**不要把 44 写成 AA 要求**，AA 是 24。

### 3.4 缓冲与加载反馈

- 起播/seek 后**延迟 200 ms** 再显示 spinner（低于 200 ms 的等待直接给内容，避免闪烁）；spinner 一旦显示，最短停留 300 ms（避免闪一下就消失）。
- `waiting` 事件 → 显示；`playing` 事件 → 隐藏；`seeking` 期间进度条滑块跟随指针而不是跟随播放头。
- 缓冲态必须保留**当前帧**（`poster` 或用最后一帧），不要黑屏——黑屏会让用户以为坏了。

### 3.5 封面（poster）、首帧与加载策略

- `poster` 是**加载前的第一屏**，不是占位色块：默认 `preload="metadata"`，不要首屏就下整条视频；`poster` 与视频首帧的构图要一致，否则开播的瞬间画面会「跳一下」。
- 首帧取法：服务端截 `00:00:00.000` 多半是黑场或渐入，取 **T+0.5 s～1 s** 的帧做海报；16:9 与 9:16 各出一套，不要用一个横版海报到处 `object-fit: cover` 硬裁主体。
- 性能口径（工程约定）：进视口才把 `src` 从 `data-src` 换上（lazy）；`poster` 体积 ≤ 视频本身时长的 1/10 档位；LCP 元素应该是 poster 图或标题文本——**不要给 `<video>` 加 `autoplay` 还让它抢 LCP**。
- 组件契约：`poster` / `aspectRatio` / `fallbackImage` 三个 prop 的默认值写清；无 `poster` 时用 `background-color` + 居中播放键兜底，禁止「黑框 + 无按钮」的加载态。

---

## §4 时间轴语义：点按、拖拽、帧步进

| 交互 | 语义 | 工程约定 |
|---|---|---|
| 点按进度条 | 跳到该位置并继续当前播放状态 | 命中区 ≥24 px 高；点按后不暂停 |
| 拖拽（scrub） | 持续预览目标位置 | 拖动中显示目标时间气泡（`00:42 / 03:40`），松手才 commit |
| 键盘 ← / → | ±5 s | 与系统视频播放器对齐 |
| 键盘 J / L | ±10 s | YouTube 惯例，可选 |
| 帧步进（`,` / `.`） | ±1 帧 | 只在「逐帧校对」类产品做（字幕/剪辑），普通播放器不做 |
| 倍速 | 0.5 / 0.75 / 1 / 1.25 / 1.5 / 2 | 超过 2× 必须重新核字幕 CPS（见 §6），因为 2× 下 20 CPS 变成 40 CPS 的阅读压力 |

**拖拽三态**：`idle → dragging → committed`。dragging 期间必须

1. 暂停 `timeupdate` 驱动的字幕更新（否则字幕会疯狂闪烁），改由指针位置计算应显示哪条字幕；
2. 不触发 `seeking` 的网络请求风暴（节流到 100–200 ms 一次，或松手才 seek）；
3. 松手后一次 commit，并在 `seeked` 后恢复字幕更新。

**直播**：进度条变成 DVR 窗（可回看区间），右端固定为「LIVE」；点击「LIVE」回到实时边缘；不允许把 DVR 窗画成「整条可拖」——用户会以为能拖到未来。

### 4.1 竖屏短视频：双击点赞、上滑切换与进度条

| 手势 | 语义 | 判定阈值（工程约定） | 冲突处理 |
|---|---|---|---|
| 单击 | 播放 / 暂停 | 抬起前位移 < 10 px、时长 < 250 ms | 250 ms 内再落第二击 → 判双击，撤销这次暂停 |
| 双击 | 点赞 | 两击间隔 ≤ 300 ms，落点距离 ≤ 40 px | 点赞动画 200 ms 内不响应播放切换 |
| 长按 | 2× 倍速（松手回 1×） | 按住 ≥ 500 ms | 长按期间不触发单击 / 双击 |
| 上滑 | 下一条 | 纵向位移 ≥ 60 px 且 |dy| > |dx| × 1.5 | 拖动进度条时禁用 |
| 横滑 | 切 tab（关注 / 推荐） | 同上，方向阈值 1.5 倍 | 与系统返回手势留 ≥ 20 px 边缘安全区 |

- **进度条不能被手势吃掉**：底部进度条命中区 ≥ 24 px 高，`pointerdown` 时立刻 `stopPropagation()`；否则用户想拖进度，结果上滑换了视频。
- **点赞幂等且可撤销**：双击点赞后 5 s 内可再点取消；按钮状态与手势状态共用一个 store，不要各写一份。
- 安全区：底部进度条与文案避开 **Home Indicator 34 px** 区与顶部刘海，竖屏内容左右内缩 **10%**（工程约定）。
- 双击点赞动画只做 `transform` / `opacity`，不要 `filter: blur()` 全屏动画——低端机必掉帧。

---

## §5 字幕数据模型（WebVTT / `<track>`）

### 5.1 三种文本轨道，别混

| 类型 | `kind` | 内容 | 谁需要 |
|---|---|---|---|
| **隐藏式字幕（captions）** | `captions` | 对白 + **非语音信息**（音效、音乐、笑声、说话人、位置） | 听障用户；静音观看者 |
| **字幕（subtitles）** | `subtitles` | 只翻对白（面向听不懂该语言的人） | 跨语言观众 |
| 章节 / 描述 | `chapters` / `descriptions` | 章节标记 / 画面描述 | 导航 / 视障 |

> 引用依据：WCAG 2.2 SC 1.2.2 Key Terms 对 captions 的定义含 *"sound effects, music, laughter, speaker identification and location"*——所以**「只有对白的字幕」不能宣称满足 1.2.2**；面向听障用户的轨道必须是 captions，把 `[门砰地关上]`、`[笑声]` 写进去。

### 5.2 `<track>` 与 TextTrack 状态

```html
<video id="v" src="clip.mp4" poster="poster.jpg" preload="metadata" playsinline>
  <track kind="captions" src="zh-Hans.vtt" srclang="zh-Hans" label="中文（隐藏式字幕）" default>
  <track kind="captions" src="en.vtt" srclang="en" label="English (CC)">
  <track kind="chapters" src="chapters.vtt" srclang="zh-Hans" label="章节">
</video>
```

- `default` 只该给**一个**轨道；给多个会让浏览器的默认选择变得不可预测。
- `label` 必须是给人看的语言名（`中文（隐藏式字幕）`），不要写 `zh-Hans.vtt` 这种文件名。
- TextTrack 的 `mode` 有三值：`disabled`（不加载、不显示）、`hidden`（加载并触发 `cuechange`，但不显示——**自绘字幕层就用这个**）、`showing`（浏览器原生渲染）。**同一时间只能有一个字幕轨道是 `showing`**，否则两套字幕会叠在一起。
- `src` 跨域时 VTT 需要 CORS 头，否则 Chrome 静默不显示（`<track>` 的失败通常不抛错，只在控制台出现 CORS 提示）——这是「字幕文件明明在却不显示」的第一号原因。

### 5.3 cue 的四个定位设置

```vtt
WEBVTT

00:00:01.000 --> 00:00:04.500 line:85% align:center position:50%
<c.yellow>这一句是黄色高亮</c>

00:00:05.000 --> 00:00:07.000 line:0% align:center
<v Kimmy>Are you coming?</v>
```

- `line`：字幕基线位置（百分比或行号，负值表示从底部数）。
- `align`：行内对齐（`start` / `center` / `end` / `left` / `right`）。
- `position`：水平位置（配合 `align` 使用）。
- `region`：把多条 cue 绑到同一个矩形区域（需要 `REGION` 定义），适合「固定两行窗口」的样式。

**建议**：普通播放器不要依赖 cue 里的 `line` 做底部安全区，交给容器 CSS（§7.2）统一控制；cue 设置一旦被写死，用户放大字号时就会撞到控制栏。

---

## §6 字幕规范数值表：字号、行长（42 字符）与 20 CPS 定生死

全部来自 Netflix Timed Text Style Guide 原文（English (USA) 与 General / Timing 三份），**逐字引号处即原文**。

| 判据 | 值 | 原文/依据 |
|---|---|---|
| 每行字符上限 | **42 characters per line** | EN (USA) I.2 / II.3 |
| 每屏行数 | **Maximum two lines.** | EN (USA) I.10 / General *"2 lines maximum"* |
| 阅读速度（成人） | **Up to 20 characters per second** | EN (USA) I.14 |
| 阅读速度（儿童） | **Up to 17 characters per second** | EN (USA) I.14 |
| 最短时长 | **5/6 (five-sixths) of a second per subtitle event**（24fps = 20 帧） | General Requirements |
| 最短时长（帧口径） | **not be any shorter in duration than 20 frames (or 4/5 sec)** | Timing Guidelines |
| 最长时长 | **7 seconds per subtitle event** | General Requirements |
| 相邻最小间隙 | **minimum of 2 frames between them**（适用任何帧率） | Timing Guidelines |
| 24fps 的 3–11 帧间隙 | **must be closed to 2 frames** | Timing Guidelines |
| 允许的间隙档位 | **either 2 frames or half a second or more** | Timing Guidelines |
| 入场时间 | 落在音频第一帧，**within 1-2 frames** 可接受 | Timing Guidelines |
| 出场时间 | 至少比音频结束晚 **half a second**（24fps = 12 帧） | Timing Guidelines |
| 对齐 | center justified，**top or bottom**（日语可竖排） | General Requirements |
| 字体 | **White**，Arial 类比例无衬线占位，尺寸「相对视频分辨率、能放下 42 字符」 | EN (USA) I.7 |
| 双人对话 | **hyphen without a space** 开头，每行最多一个说话人 | EN (USA) |
| TTML 尺寸 | **`tts:fontSize` shall be defined as 100%. Do not use pixel values.** 只用百分比 | General Requirements |

### 6.1 两个必须会解释的矛盾

1. **5/6 s 与 4/5 s**：24fps 下 5/6 s = 20 帧；4/5 s = 0.8 s = 19.2 帧，是个**取整近似**。取严：`min_duration = max(5/6, 20/fps)`。在 25fps 下 20 帧 = 0.8 s，此时 4/5 s 反而更严——所以**不能把 4/5 当成更低的上限**，两条都要过。
2. **「42 字符 × 2 行」与「20 CPS」是联合约束**：一屏最多 84 字符，按 20 CPS 至少要 4.2 秒；而最长 7 秒意味着**单屏最多 140 字符**。所以「两行长句」在 4.2 秒以内出现时，要么拆成两条 cue，要么提速——不能既保留长句又保留短时长。

### 6.2 中文与 CJK 的换算（工程约定，非 Netflix 原文）

Netflix 数值是为拉丁字符定的；中文不能直接照抄「42 字符」：

- 中文**全角字符 ≈ 2 个拉丁字符宽**，一行 42 个拉丁字符的横向空间 ≈ **21 个汉字**；
- 实践取值：**每行 ≤ 20–22 个汉字，每屏 ≤ 2 行（≤ 44 字）**；
- CPS 换算：成人 20 CPS（拉丁）≈ **9–10 汉字/秒**；儿童 17 CPS ≈ **8 汉字/秒**。超出这个速度，中文观众会「看到但来不及读」；
- 断行遵守标点（中文避头尾规则见 `chinese-design.md`），**不在词中间断**，不把数量词与量词拆开。

---

## §7 字幕样式实现：从 `::cue` 到自绘层

### 7.1 原生渲染（`::cue`）与能力边界

```css
video::cue {
  color: #fff;
  background: rgba(0, 0, 0, 0.72);
  font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
  font-size: 100%;          /* 相对浏览器的默认 cue 尺寸 */
  line-height: 1.35;
  padding: 0 0.25em;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.85);
}
video::cue(v[voice="Kimmy"]) { color: #ffd166; }   /* 按说话人着色 */
```

限制（决定你该不该自绘）：

- `::cue` 支持的属性集**有限且各浏览器不一致**，`font-size` 用百分比/相对单位，写 px 在部分浏览器被忽略；
- 无法控制**容器位置与换行**（`line` 只能写在 cue 里），无法做「两行固定窗口」；
- 无法在字幕里放图标/按钮，无法做逐字高亮（卡拉 OK）；
- **用户浏览器的字幕字号设置优先级高于你的 CSS**（这是特性不是 bug，别对抗）。

### 7.2 自绘字幕层（需要完全控制时）

结构：`<div class="dp-caption" role="region" aria-live="off">` 绝对定位在视频容器上。

三条硬规则：

1. **位置**：底部安全区 = 容器高度的 **5%–8%**（1080p → 54–86 px），且必须在控制栏**之上**（控制栏显示时字幕上移 8–12 px，或控制栏本身做半透明渐变，不与字幕重叠）。WCAG 2.2 SC 1.2.2 Key Terms Note 4 原文：*"Captions should not obscure or obstruct relevant information in the video."*——这既约束视频内容，也约束你自己的控件：**字幕被进度条盖住就是遮挡**。
2. **同步**：不要用 `timeupdate`（约 4 Hz，会明显滞后）。用 `requestAnimationFrame` 轮询 `video.currentTime`，按 `TextTrack.mode = "hidden"` + `cuechange` 兜底；拖动期间（§4 的 dragging 态）改用指针位置推算，避免字幕狂闪。
3. **不重复**：自绘时必须把原生轨道切成 `hidden`（不是 `showing`），否则两套字幕叠字。**同一时刻只允许一条渲染路径。**

### 7.3 字号与可调性

- 基准：**容器高度的 2.5%–3%**（1080p → 27–32 px；720p → 18–22 px），与 Netflix「按分辨率、能放下 42 字符」的口径一致；
- 提供 **50% / 100% / 150% / 200%** 四档用户缩放，并把选择**持久化**（localStorage）——这是听障与低视力用户的高频需求，不是「高级设置」；
- 缩放后必须重新跑 §6 的行数检查（字号变大 → 每行字符变少 → 可能变三行，撞 2 行上限）。

---

## §8 媒体策略：iOS 门控与静音开播

### 8.1 浏览器允许什么（WebKit 原文）

> *"`<video autoplay>` elements will now honor the `autoplay` attribute, for elements which meet the following conditions: `<video>` elements will be allowed to `autoplay` without a user gesture if their source media contains no audio tracks. `<video muted>` elements will also be allowed to autoplay without a user gesture. If a `<video>` element gains an audio track or becomes un-muted without a user gesture, playback will pause."*

> *"`<video autoplay>` elements will only begin playing when visible on-screen such as when they are scrolled into the viewport, made visible through CSS, and inserted into the DOM."*；*"will pause if they become non-visible, such as by being scrolled out of the viewport."*

> *"On iPhone, `<video playsinline>` elements will now be allowed to play inline, and will not automatically enter fullscreen mode when playback begins. `<video>` elements without `playsinline` attributes will continue to require fullscreen mode for playback on iPhone."*

推论（可直接写成验收项）：

| 场景 | 能不能自动播 | 必须怎么做 |
|---|---|---|
| 无声背景视频 / 动图替代 | ✅ 可以（`muted` 或源无音轨），可见才播 | `muted playsinline loop autoplay` + 提供暂停按钮（WCAG 2.2.2） |
| 带声音的营销视频 | ❌ 默认不行 | 给 `preload="metadata"` + 醒目播放按钮 + 海报图；用户点击后再 `play()` |
| 用户已交互过的页面内 | 仍按上面两条，不要赌「已经点过一次」 | 不要用「首次点击页面任意处就播有声视频」绕过策略 |
| iOS 内嵌播放 | 必须 `playsinline` | 否则一播就强制全屏，页面上下文全丢 |

`video.play()` 在不符合条件时返回 **rejected Promise**——必须 `.catch()` 并把 UI 退回「点击播放」态，不要留下一个永远转圈的播放按钮。

### 8.2 为什么值得用视频替代 GIF（官方数据）

WebKit 同一篇原文：*"GIFs can be up to twelve times as expensive in bandwidth and twice as expensive in energy use"*（相对 H.264）。落地口径：动图超过 **约 500 KB / 5 秒**时改用 `<video muted loop playsinline autoplay>` + `poster` 兜底，并保留 `<img>` 作为 no-JS fallback。

### 8.3 全屏与画中画

- 全屏用 `requestFullscreen()`；iOS Safari 上 `<video>` 的原生全屏由 `webkitEnterFullscreen()` 提供，自定义容器全屏在 iPhone 上不可用——**不要承诺「iPhone 上也能自定义全屏控件」**。
- PiP（画中画）在桌面 Chrome/Safari/Firefox 可用，移动端多为系统级；提供入口但不承诺能力，`document.pictureInPictureEnabled` 为 false 时隐藏按钮。
- 全屏状态下**键盘映射不变**（Space/←/→/M/F），且 Esc 退出后焦点必须回到进入全屏前的元素。

### 8.4 iOS 内联播放与静音开播：落地清单

- **内联**：`<video playsinline webkit-playsinline>` 两个属性都写；iOS Safari 缺 `playsinline` 就一播全屏，页面上下文全丢。
- **静音开播**：只有 `muted`（或源无音轨）才够格静音起播；`muted` 要写进 HTML 属性，别只在 `play()` 前用 JS 设——部分 iOS 版本上设得太晚，照样被拦。
- **切声**：用户取消静音是一次手势，`video.muted = false` 与 `play()` 必须同在手势回调里，否则 Promise 直接 rejected；失败就退回「点击播放」态，别留转圈。
- **移动端控件**：按钮取 WCAG 24×24 CSS px 与 Apple HIG 44×44 的**大者**；竖屏内联时控制栏做半透明渐变，不能压住字幕（§7.2）。
- 验收四步：iPhone Safari / Android Chrome 各跑「进页面不自播 → 点一下播 → 切后台暂停 → 回前台不自动续播」。

---

## §9 可访问性：四条 SC + 一套键位

### 9.1 必须逐字过的条文

- **SC 1.2.2 Captions (Prerecorded)**（AA）：*"Captions are provided for all prerecorded audio content in synchronized media, except when the media is a media alternative for text and is clearly labeled as such."* → 有音轨就必须有 captions；「视频本身就是文字内容的替代」是唯一豁免，且必须**明确标注**。
- **SC 2.2.2 Pause, Stop, Hide**（A）：*"For any moving, blinking or scrolling information that (1) starts automatically, (2) lasts more than five seconds, and (3) is presented in parallel with other content, there is a mechanism for the user to pause, stop, or hide it unless the movement, blinking, or scrolling is part of an activity where it is essential"*。→ **自动播放且超过 5 秒**的动效/视频必须能暂停；且 Understanding 明确，*"an animation stop only so long as a user has focus on it … would not be considered a 'mechanism for the user to pause'"*——**hover 暂停不算暂停机制**。
- **SC 2.5.8 Target Size (Minimum)**（AA，2.2 新增）：控件 ≥ **24×24 CSS px**；例外仅当存在等价的另一条路径，或间距满足「24 px 直径圆互不相交」的 Spacing 例外。音频/视频控件**不在** inline 例外范围内。
- **SC 1.4.3 Contrast (Minimum)**：字幕文字与背景 ≥ **4.5:1**；大字（≥18pt 或 ≥14pt 粗体，Understanding 注明 1pt = 1.333px，即约 24px / 18.5px）≥ **3:1**。注意原文 *"4.499:1 would not meet the 4.5:1 threshold"*——**不许四舍五入**。

> 字幕的黑色半透明底 + 白字是最稳的组合（纯黑底白字 21:1）；**白字直接压在视频画面上不可接受**，因为背景亮度随画面变化，最亮帧处会掉到 2:1 以下。用 `background: rgba(0,0,0,.72)` 加 `text-shadow` 作为双保险。

### 9.2 键位映射（工程约定，与 YouTube / 系统播放器对齐）

| 键 | 动作 | 备注 |
|---|---|---|
| `Space` / `K` | 播放 / 暂停 | 焦点在按钮上时，Space 触发按钮本身，不要双触发 |
| `←` / `→` | −5 s / +5 s | |
| `J` / `L` | −10 s / +10 s | 可选 |
| `↑` / `↓` | 音量 ±5% | |
| `M` | 静音切换 | 按钮 `aria-label` 同步为「取消静音 / 静音」 |
| `F` | 全屏切换 | |
| `C` | 字幕开关 | 一级控件里必须有等价按钮 |
| `0`–`9` | 跳到 0%–90% | 可选 |

**焦点管理**：控制栏用 `role="toolbar"` 或一组原生 `<button>`；Tab 顺序 = 视觉顺序；**不要给进度条 `tabindex="-1"` 后只靠方向键**——滑块必须是可聚焦的 `<input type="range">` 或带 `role="slider"` 的元素，并有 `aria-valuemin/valuemax/valuetext`（`aria-valuetext` 用「1 分 23 秒，共 3 分 40 秒」这类人话）。

### 9.3 播报与状态

- 播放/暂停按钮的 `aria-label` 必须随状态变化（不要固定写「播放」）。
- **不要**给字幕容器加 `aria-live="assertive"`——字幕会每两秒打断读屏；需要朗读字幕时用 `aria-live="off"` 并让用户主动请求转录文本（§L4）。
- 加载/缓冲用 `role="status"` 播报「正在缓冲」，不要用 `aria-live="assertive"`。

### 9.4 度量（L7）

别用「播放次数」当完成率。看四件事：**起播率**（点击播放 → `playing` 的比例）、**25/50/75/100% 四分位到达率**、**seek 分布**（大量回拖 = 内容难懂或缺字幕）、**字幕开启率**（低得异常说明开关找不到或默认没开）。

### 9.5 读屏与隐藏式字幕的交付验收

- 读屏软件（NVDA / VoiceOver / TalkBack）**读不到 `<video>` 里渲染出来的字幕**——原生 `::cue` 与自绘层都不进无障碍树。要让读屏用户拿到字幕内容，必须提供**同一内容的文字稿（transcript）**，或给字幕容器 `role="region" aria-label="字幕"` 并把当前 cue 以静态节点暴露。
- 「隐藏式字幕」的「隐藏」是**视觉隐藏**，不是对读屏隐藏：`kind="captions"` 在 `mode="hidden"` 时仍触发 `cuechange`，这正是自绘层的数据源；为了「不显示」而设 `disabled` 会把数据源一起关掉。
- 验收三条（工程约定）：① 不开字幕也能用读屏完成「播放 / 暂停 / 调音量 / 开字幕」；② 开字幕时读屏不会把整屏字幕反复念（`aria-live` 用 `off`，绝不用 `assertive`）；③ 字幕开关按钮的 `aria-pressed` 与视觉状态同步。

---

## §10 反模式（出现即返工）

1. **只用 `<video controls>` 却又被要求「加个字幕菜单」**——原生控件无法扩展，最后只能叠一堆浮层，键盘顺序必乱。
2. **自动播放有声视频**——被浏览器拦成静音后仍显示「正在播放」，用户以为没声音是设备坏了。
3. **没有 `playsinline`**——iPhone 上点播放直接全屏，页面上下文全丢。
4. **控制栏 32×32 的图标按钮**——低于 AA 的 24×24 命中区只是勉强，触摸设备上实际点不中。
5. **暂停时隐藏控制栏**——用户暂停就是为了找按钮。
6. **拖动进度条时字幕疯狂闪烁**——`timeupdate` 与 scrub 抢更新，必须进 dragging 态。
7. **缓冲时黑屏**——用户判定「视频坏了」；保留最后一帧或海报图。
8. **字幕被控制栏遮住**——直接违反 SC 1.2.2 Note 4。
9. **两套字幕同时渲染**（自绘层 + 原生 `showing`）——文字叠字，几乎无法阅读。
10. **「42 字符」直接套到中文**——中文一行 42 字会宽到出画，应按 20–22 汉字。
11. **字幕字号写 px 且不提供用户缩放**——低视力用户无法放大，且各浏览器会覆盖。
12. **用 hover 暂停当「暂停机制」**——SC 2.2.2 明确不认。
13. **进度条不可键盘操作**——只剩鼠标能 seek，等于听障用户回看某句的路径被切断。
14. **倍速到 2× 却没有重新核 CPS**——字幕阅读压力翻倍，`20 CPS → 40 CPS`。

---

## §11 交付前自检（18 条，逐条打勾）

- [ ] 1. 有一个 `<video>`，同时具备 `playsinline` 与显式 `preload`（默认 `metadata`）；首帧有 `poster`。
- [ ] 2. 自动播放仅出现在「`muted` 或源无音轨」的视频上，且 `play()` 的 rejected Promise 有 `.catch()` 回退。
- [ ] 3. 自动播放/循环动效超过 5 秒时，有**真实可见的暂停按钮**（不是 hover 暂停）。
- [ ] 4. 控件命中区 ≥24×24 CSS px（桌面与移动端都实测过），触摸设备 ≥44×44。
- [ ] 5. 播放中控件 2.5–3 s 自动隐藏；暂停 / 焦点在控件内 / 菜单打开时**不隐藏**。
- [ ] 6. 进度条可键盘聚焦，`role="slider"` + `aria-valuetext` 为「X 分 Y 秒，共 Z 分 W 秒」。
- [ ] 7. 拖动进度条进入 dragging 态：字幕/时间不闪、seek 节流、松手才 commit。
- [ ] 8. 起播与 seek 的 spinner 延迟 200 ms、最短 300 ms；缓冲时保留当前帧。
- [ ] 9. 有 captions 轨道（不只是 subtitles），且含非语音信息（`[笑声]`、`[门响]`）。
- [ ] 10. 字幕可通过一级控件开关，按钮 `aria-label` 随状态变化；快捷键 `C` 等价。
- [ ] 11. 字幕行数 ≤2、每行 ≤42 拉丁字符或 ≤22 汉字、CPS ≤20（儿童 ≤17）、时长 5/6–7 s、间隙 2 帧或 ≥0.5 s——用 §12.1 脚本跑过。
- [ ] 12. 字幕底部安全区在控制栏之上，底部留白 ≥5% 容器高度；不遮挡画面关键信息。
- [ ] 13. 字幕对比度 ≥4.5:1（用 §12.3 脚本算，不四舍五入），有半透明底或描边。
- [ ] 14. 提供字幕字号 50%–200% 四档并持久化；放大后仍是 ≤2 行。
- [ ] 15. 全键盘可完成「播放 → 跳转 → 开字幕 → 全屏 → 退出」，Esc 后焦点回到原点。
- [ ] 16. 数据侧已埋点：起播率、四分位到达率、seek 分布、字幕开启率。

- [ ] 17. 竖屏短视频：单击 250 ms / 双击 300 ms / 长按 500 ms / 上滑 60 px 的判定写死在代码里，且进度条 `pointerdown` 阻止冒泡——不会「想拖进度却换了视频」。
- [ ] 18. 读屏路径：页面上有文字稿，或字幕区可被读屏访问；读屏能独立完成「播放 / 暂停 / 开字幕」三件事。

---

## §12 可执行校验（代码围栏均以 `python -I -X utf8` 实跑通过）

### 12.1 字幕合规校验器（Netflix 数值 + 帧间隙规则）

```python
# caption_lint.py — 逐条落地 §6 的数值，输入 VTT 文本，输出违规清单
import re

FPS_DEFAULT = 24.0
MIN_DUR = 5 / 6          # General: "5/6 (five-sixths) of a second"
MIN_DUR_FRAMES = 20      # Timing: "no shorter than 20 frames"
MAX_DUR = 7.0            # General: "Maximum duration: 7 seconds"
MAX_LINE_CHARS = 42      # EN (USA) I.2: "42 characters per line"
MAX_LINES = 2            # EN (USA) I.10: "Maximum two lines."
CPS = {"adult": 20.0, "child": 17.0}   # EN (USA) I.14
MIN_GAP_FRAMES = 2       # Timing: "minimum of 2 frames between them"
BIG_GAP_S = 0.5          # Timing: "either 2 frames or half a second or more"


def _sec(ts):
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def parse_vtt(vtt):
    """按空行切块：块首可能是 WEBVTT 头或 cue id，真正的正文在 '-->' 之后。"""
    cues = []
    for block in re.split(r"\n\s*\n", vtt.strip()):
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if not lines or lines[0].startswith("WEBVTT"):
            continue
        idx = next((k for k, ln in enumerate(lines) if "-->" in ln), None)
        if idx is None:
            continue
        a, b = [x.strip() for x in lines[idx].split("-->")[:2]]
        cues.append({"start": _sec(a), "end": _sec(b), "lines": lines[idx + 1:]})
    return cues


def lint(vtt, fps=FPS_DEFAULT, audience="adult"):
    cues = parse_vtt(vtt)
    bad = []
    min_dur = max(MIN_DUR, MIN_DUR_FRAMES / fps)
    for i, c in enumerate(cues, 1):
        dur = c["end"] - c["start"]
        plain = re.sub(r"<[^>]+>", "", " ".join(c["lines"]))
        if dur + 1e-9 < min_dur:
            bad.append("cue #%d: %.3fs < min %.3fs" % (i, dur, min_dur))
        if dur - 1e-9 > MAX_DUR:
            bad.append("cue #%d: %.3fs > max %.1fs" % (i, dur, MAX_DUR))
        if dur > 0 and len(plain) / dur > CPS[audience] + 1e-9:
            bad.append("cue #%d: %.1f CPS > %.0f" % (i, len(plain) / dur, CPS[audience]))
        if len(c["lines"]) > MAX_LINES:
            bad.append("cue #%d: %d lines > %d" % (i, len(c["lines"]), MAX_LINES))
        for ln in c["lines"]:
            n = len(re.sub(r"<[^>]+>", "", ln))
            if n > MAX_LINE_CHARS:
                bad.append("cue #%d: line %d chars > %d" % (i, n, MAX_LINE_CHARS))
        if i < len(cues):
            gap_frames = (cues[i]["start"] - c["end"]) * fps
            if gap_frames < -1e-6:
                bad.append("cue #%d: overlaps next cue" % i)
            elif 1e-6 < gap_frames < BIG_GAP_S * fps - 1e-6:
                if abs(gap_frames - MIN_GAP_FRAMES) > 0.5:
                    bad.append("cue #%d: gap %.1f frames is neither 2f nor >=0.5s"
                               % (i, gap_frames))
    return bad


SAMPLE = """WEBVTT

1
00:00:01.000 --> 00:00:01.400
太短的一句字幕

2
00:00:02.000 --> 00:00:09.500
这一句持续时间超过七秒，而且字符数也远远超过两行四十二字符的上限，所以必然被校验器报出多处问题
"""
problems = lint(SAMPLE)
assert len(problems) >= 3, problems
assert lint("WEBVTT\n\n00:00:01.000 --> 00:00:03.000\n你好，世界。\n") == []
print("caption_lint OK ->", problems)
```

### 12.2 双行断行器（底部更宽的金字塔形，对应 EN (USA) I.10）

```python
# cap_break.py — 在 <=42 字符的前提下把一条 cue 断成两行，且下行不短于上行
def break_caption(text, limit=42):
    words = text.split()
    if not words:
        return [""]
    best = None
    for k in range(1, len(words)):
        top, bottom = " ".join(words[:k]), " ".join(words[k:])
        if len(top) > limit or len(bottom) > limit:
            continue
        if len(top) > len(bottom):      # 金字塔：下行 >= 上行
            continue
        score = (max(len(top), len(bottom)), len(bottom) - len(top))
        if best is None or score < best[0]:
            best = (score, [top, bottom])
    if best:
        return best[1]
    out, cur = [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if len(cand) <= limit:
            cur = cand
        else:
            out.append(cur)
            cur = w
    out.append(cur)
    return out


S = "Breaking the line should happen after punctuation marks and before conjunctions"
lines = break_caption(S)
assert " ".join(lines) == S, lines
assert len(lines) == 2 and all(len(x) <= 42 for x in lines), lines
assert len(lines[0]) <= len(lines[1]), lines      # 底部更宽
print("cap_break OK ->", [len(x) for x in lines], lines)
```

### 12.3 字号与对比度（把「看不见」变成可算的数）

```python
# cap_style.py — 字号基准 2.5%–3% 容器高；对比度按 WCAG 定义算，不四舍五入
def caption_font_px(video_height, ratio=0.026, lo=14, hi=72):
    return int(round(min(hi, max(lo, video_height * ratio))))


def _lin(c8):
    c = c8 / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def contrast(hex1, hex2):
    def lum(h):
        h = h.lstrip("#")
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)
    a, b = sorted((lum(hex1), lum(hex2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


assert caption_font_px(1080) == 28
assert caption_font_px(480) == 14                 # 触底到最小值
assert round(contrast("#FFFFFF", "#000000"), 2) == 21.0
assert contrast("#FFFFFF", "#767676") >= 4.5      # 恰好达标的深灰
assert contrast("#FFFFFF", "#787878") < 4.5       # 再浅一点就不达标
print("cap_style OK -> 1080p=%dpx, 720p=%dpx, 黑底白字=%.2f:1"
      % (caption_font_px(1080), caption_font_px(720), contrast("#FFFFFF", "#000000")))
```

---

## §13 取源限制（本轮实测，绝不臆造）

- **BBC Subtitle Guidelines 取不到**：`https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/` 连续 2 次 `fetch failed`（TypeError）；`https://bbc.github.io/subtitle-guidelines/` 返回 HTTP 404，页面只剩一句 *"The BBC Subtitle Guidelines have moved!"*。因此本轮**不引用**任何 BBC 数值（常见的「37 字符/行」「160–180 wpm」等数字未经原文核对，一律不写）。
- **Chrome 自动播放策略原文取不到**：`https://developer.chrome.com/blog/autoplay` 返回 `fetch failed`。因此自动播放这一节只引 WebKit 官方博客（已逐字核对），**不引 Chrome 的具体策略阈值**。
- **dcmp Captioning Key 只取到目录页**：`https://dcmp.org/learn/captioningkey` 返回的是索引页，子页正文未展开且无可引数值，故不引用。
- Netflix 三份指南的**出版日期各版本有差异**（General 2022-10-07、Timing 2025-07-04、EN (USA) 为 2026 现行版），引用时已分别标注；数值若与更新版本冲突，以被引原文为准并重核。
- `videojs/video.js` 与 `video-dev/hls.js` 的 license 在 GitHub API 返回 `NOASSERTION`（name 显示 "Other"），**商用前必须人工读 LICENSE 文件**，不能当成 MIT/Apache 直接放进合规清单。
