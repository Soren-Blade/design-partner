# 对话式与生成式界面：流式输出、混合界面与可纠错契约

> 快照 2026-11-11 · 每日升级 #32（v35→v36）· 主题：Conversational & Generative UI / AI 产品交互
> 取源：`Design-related websites.txt` 二十一区 + W3C / MDN / Microsoft HAX / Ant Design X / Vercel AI SDK / AG-UI / arXiv / GitHub API 实测。凡规范数值与条文均引官方原文，凡工程建议均标注「工程约定」。
>
> **边界纪律（先读这段，避免误路由）**：本文件只回答「**AI 功能本身作为一个界面，怎么把一段不确定的、边生成边变化的输出，做成可等待、可阅读、可纠错、可撤销的交互链路**」。Microsoft HAX G1–G18 18 条人机交互准则的完整表在 `ai-design-toolchain.md §10`，本文件**不重列 18 条**；反馈五层决策树 / toast 时长 / 空态在 `feedback-states.md`；WCAG 阈值与焦点三层在 `accessibility.md`；loading 骨架与性能预算在 `performance-design.md`；文案语气在 `ux-writing.md`。这里只写这些资产都没覆盖的**流式链路、事件协议、混合界面、状态归位、纠错恢复**。

---

## 0. 一句话立场与三条裁决

对话式与生成式界面（Conversational & Generative UI）不是「把聊天气泡套个皮」，而是**一条五段并存且每一段都会失败的链路**：发得出 → 等得住 → 读得动 → 改得动 → 收得回；任何一段没建模，界面就会在「模型正在输出」这个真实状态下崩掉。

**三条最重要裁决**（本轮要求 agent 不再含糊的地方）：

1. **流式回答正文不是状态消息，状态边界才播报一次**。WCAG 2.2 SC 4.1.3 逐字只管 *status messages*，且官方明确「搜索结果列表不是 status update」——回答正文与搜索结果同类，**逐 chunk 塞进 `aria-live="assertive"` 属于失败族**；`role="log"`（隐性 `aria-live="polite"` / `aria-atomic="false"`）负责追加的新消息，`role="status"` 只在 submitted / streaming / ready / error 与「已停止」「已重新生成」这些**边界**播报一句短文本。详见 §3 §4 §5 §12。
2. **生成式 UI 是「模型在受控组件目录里做路由」，不是「模型返回任意组件」**。Vercel 官方原文 *"you provide tools that return React components"*、*"the model is akin to a dynamic router"*；每个 tool 必须有 `inputSchema`（Zod）且 `generate` 必须返回 React component。模型只能输出**组件名 + 参数**，组件名必须查白名单表，绝不能把模型字符串当组件/HTML 执行。详见 §6 §7 §8。
3. **纠错是四档恢复链，不是一个「重新生成」按钮**。HAX G9 逐字 *"Make it easy to edit, refine, or recover when the AI system is wrong."*，其官方模式含 G9-C *Undo automated actions*、G9-B *Rich and detailed edits*。四档为：停止 → 重试/重生成 → 编辑原消息重放 → 撤销自动化动作；每档都必须**状态归位 + 一次播报**。详见 §11 §12 §13。

**质量门槛**：读完本文件，agent 应能对「逐 token 播报对不对」「RSC 能不能上生产」「答错了只能重生成吗」给出带官方条文或代码契约的明确结论，而不是「视情况而定」。

---

## 1. 为什么这是结构性空白（缺口实测）

结构性空白是指：不是覆盖不足，而是**全域没有独立资产**，检索会把问题路由到完全不相干的文件。本轮用 `scripts/dp_search.py` 与全域词频实测（v35 基线，41 份参考）判定。

| 探测词 | v35 全域命中 | 判定 |
|---|---|---|
| `Chatbot` / `streaming` / `生成式界面` / `GenUI` | 0 | 零命中 |
| `role=log` / `ARIA23` / `aria-busy` / `message.parts` / `streamUI` | 0 | 零命中 |
| `流式` | 6（均为 `流式排版`/`clamp` 语境） | 语义错配 |
| `对话式` / `聊天` | 1 / 6（散在 `ai-design-toolchain.md` 与 UX 文案里） | 无独立体系 |
| `prompt` | 67（几乎全是提示词工程，不是界面） | 语义错配 |
| `HAX` | 20（全在 `ai-design-toolchain.md §10`） | 已有原则层，缺界面链路层 |

`dp_search.py "对话式界面 聊天 UI 流式输出"` 在 v35 首位返回 `ai-design-toolchain.md`（提示词 / HAX 原则）与 `feedback-states.md`（加载态），**没有任何一份资产回答「流式 chunk 期间状态怎么算、读屏怎么播报、答错了怎么回滚」**。

**与既有资产的邻接关系**：`content-findability.md`（能不能找到）→ `visual-hierarchy-gestalt.md`（目光先看哪）→ `direct-manipulation.md`（按下指针之后）→ 本文件（**输出是不确定的、边生成边变化的**）。前三份都假设「内容是确定的」，本轮补的是「内容本身在流动」这一支。

---

## 2. 五段链路判层模型（L1 发得出 → L5 收得回）

先判问题落在哪一段，再动手改界面；**一上来改气泡样式是典型的判层失败**。

| 层 | 问题 | 典型症状 | 主判据 | 去哪节 |
|---|---|---|---|---|
| L1 发得出 | 意图表达 | 用户只会打字、不会给约束；Enter 与换行打架；提交后不知道发出去了没 | 输入框 / 发送契约 / `submitted` 可见 | §15 |
| L2 等得住 | 等待与进度 | 首 token 前空白、没有「停止」、进度假、取消后还在扣费 | 四态状态机 + 生命周期事件 | §8 §9 §13 |
| L3 读得动 | 流式呈现与播报 | 逐 chunk 读屏刷屏、代码块闪成正文、自动滚动抢焦点、组件越权 | `role=log` / `message.parts` / 白名单 | §3–§7 §14 |
| L4 改得动 | 纠错与恢复 | 只有「重新生成」、不能编辑原消息、工具副作用撤不回 | HAX G9 四档恢复链 | §11 §12 |
| L5 收得回 | 收口与归位 | `ready` 了按钮还禁用、`aria-busy` 没复位、错误被吞、队列没清 | 状态归位表 + 错误契约 | §13 §12 |

**判层口诀**：用户说「卡住了 / 一直在转」先查 L2；说「读屏一直在念 / 页面乱跳」查 L3；说「答错了只能重来」查 L4；说「停止之后还能发但状态不对」查 L5。**禁止跨层改样式**。

---

## 3. 裁决一：流式文本不是状态消息，状态边界才播报（SC 4.1.3 逐字）

WCAG 2.2 SC 4.1.3 Status Messages (Level AA) 规范条文逐字：

> In content implemented using markup languages, status messages can be programmatically determined through role or properties such that they can be presented to the user by assistive technologies without receiving focus.

`status message` 的官方定义逐字：

> change in content that is not a change of context, and that provides information to the user on the success or results of an action, on the waiting state of an application, on the progress of a process, or on the existence of errors

W3C Understanding 页明确把「内容结果」排除在外，逐字：

> the list of results obtained from a search are not considered a status update and thus are not covered by this success criterion. However, brief text messages displayed *about* the completion or status of the search, such as "Searching...", "18 results returned" or "No results returned" would be status updates if they do not take focus or cause a page refresh.

**这条是裁决一的规范支点**：模型回答正文等同于「结果列表」——是内容，不是状态；而「正在生成 / 已生成完毕 / 生成失败 / 已停止」是 *about* 结果的状态，才是 SC 4.1.3 的对象。把每个 token 当 status message 播报，既不符合定义，也踩中官方点名的 chatty 风险：

> However, there is a risk of making an application too "chatty" for a screen reader user. User testing should be carried out to ensure the appropriate level of feedback is achieved.

> The purpose of this success criterion is not to force authors to generate new status messages. Its intent is to ensure that when status messages *are* displayed, they are programmatically identified in a way that allows assistive technologies to present them to the user.

**失败族（W3C 官方 Failures 逐字）**：

> - F103: Failure of Success Criterion 4.1.3 due to providing status messages that cannot be programmatically determined through role or properties
> - Using `role="alert"` or `aria-live="assertive"` on content which is not important and time-sensitive

**充分技术按情境分（不要一律上 role=alert）**：Situation A（成功/结果/应用状态）→ ARIA22 `role=status` + G199；Situation B（建议或错误警告）→ ARIA19 `role=alert` / Live Regions + G83/G84/G85/G177/G194；Situation C（流程进度）→ **ARIA23 `role=log`**、ARIA25、ARIA22+G193、ARIA27 `ariaNotify`。官方 Note 逐字：

> A role of "alert" is only necessary where a change of context does *not* take place.

**可验收结论**：`role="alert"` / `assertive` 只留给「生成失败且用户必须立刻知道」这类重要且时间敏感的错误；「正在生成」「已完成」「已停止」用 `role="status"`（隐性 polite）。**流式正文永不进 assertive 区**。

---

## 4. ARIA23 role=log 与隐性 aria-live=polite / aria-atomic=false

W3C Technique ARIA23《Using `role=log` to identify sequential information updates》是 SC 4.1.3 Situation C 的**充分技术**（*Techniques are examples ... not required*），其官方示例 1 直接就是聊天记录，逐字：

> The ARIA live region role of `log` has an implicit `aria-live` value of `polite` and `aria-atomic` value of `false`, which allows a user to be notified via AT (such as a screen reader) when log messages are added. The new content within the live region is automatically read by the AT, without the AT having to focus on the place where the text is displayed.

> #### Example 1: Updating the contents of a chat conversation
> Comments that users type into a chat input field are appended to the end of the chat history region. The region is marked with `role="log"` so that new additions are announced by ATs. When each new chat message appears, a screen reader should announce its content (depending on AT/browser compatibility).

```html
<div id="chatRegion" role="log" aria-labelledby="chatHeading">
  <h4 id="chatHeading">Chat History</h4>
  <ul id="conversation">
    <li>The latest chat message</li>
  </ul>
</div>
```

ARIA23 的 Tests 只要求一件事：*Check that the container for the information is given a role of `log`*。**它没要求逐 chunk 播报，也没要求自己再声明 aria-live**——隐性值已生效。

**为什么 `aria-atomic="false"` 是关键**：只播报新增节点，不重读整个对话。若错误设成 `true`，每来一个 token 就会把整段历史重念一遍，正是 §3 的 chatty 风险。W3C Understanding 也给了同构的购物车例子：只更新 `"0 items"` 里的数字会只念 "three"，此时应把整串 `"3 items"` 标为状态文本或用 `aria-atomic` 补足上下文；但**流式正文不是状态文本**，别把这个技巧套到回答气泡上。

**MDN 补充口径**（W3C TR 页本轮被 Cloudflare 拦截，取源限制见 §23）：`role=log` 隐性 `aria-relevant` 默认 `additions text`；`role=log` 应有 accessible name（`aria-label` / `aria-labelledby`）；`role=alert` 有隐性 `aria-live="assertive"`，部分读屏会双播，故不要同时写 `aria-live="assertive"` + `role="alert"`。

---

## 5. 聊天界面播报工程契约：chatbot 流式输出的状态边界（空容器、aria-busy、aria-relevant、assertive 双播）

以下为**工程约定**（规范未强制逐条），但每条都能追溯到官方机制，验收时按此清单过：

| 契约 | 做法 | 官方依据 / 踩坑 |
|---|---|---|
| 空 live region 必须**提前存在** | 页面加载时就有 `<div role="status" id="gen-status"></div>`；不要等要播报才 `createElement` | MDN Live regions：AT 只会监视已存在的 live region，动态新建常常不播报 |
| 对话容器用 `role="log"` | 追加整条消息节点，不追加 token 节点 | ARIA23 Example 1；隐性 polite + atomic=false |
| 状态边界播报一次 | submitted / streaming / ready / error / 已停止 / 已重新生成，各播一句 ≤20 字短句 | SC 4.1.3 Situation A/C；chatty 风险 |
| `aria-busy` 挂在**正在生成的气泡**上 | 开始 `true`，收口 `false`；别挂整个 `role=log` 容器，否则历史追加也被抑制 | MDN `aria-busy`：多段更新期间设 true，完成后置 false |
| `aria-relevant` 不滥用 removals | 默认 `additions text` 足够；加 `removals` 会让「停止/删除消息」也念一遍 | MDN Live regions |
| 不写 `role="alert"` + `aria-live="assertive"` 双份 | 只保留其一 | 部分 AT 双播 |
| 焦点不抢 | 生成完成**不**把焦点移到回答末尾；需要跳转给一个可聚焦的「跳到最新回答」按钮 | SC 4.1.3 的前提就是 *without receiving focus* |
| 中文短句不带技术词 | 「正在生成」「已生成完毕」「生成失败，可重试」「已停止」 | `ux-writing.md` 错误文案三层；不写 "stream aborted" |

**反例（必须能一眼判错）**：把 `<div aria-live="assertive">` 绑定 `delta`，模型每吐一个字就播报一次；把 `aria-busy="true"` 留在页面上永不复位；生成完成自动 `focus()` 到回答，导致用户正在输入框打字时被拽走。

---

## 6. 裁决二：生成式界面 streamUI 是组件白名单里的路由，不是任意组件

Vercel AI SDK RSC《Streaming React Components》官方原文逐字：

> With the `streamUI` function, **you provide tools that return React components**. With the ability to stream components, the model is akin to a dynamic router that is able to understand the user's intention and display relevant UI.

> If the model decides, based on the context of the conversation, to call a tool, it will generate a tool call. The `streamUI` function will then run the respective tool, returning a React component. If the model doesn't have a relevant tool to use, it will return a text generation, which will be passed to the `text` function, for you to handle.

> Remember, the `streamUI` function must return a React component.

A tool 的三字段契约逐字：`description`（a string telling the model what the tool does and when to use it）、`inputSchema`（a Zod schema describing what the tool needs in order to run）、`generate`（an asynchronous function ... **This must return a React component**）。

```tsx
const result = await streamUI({
  model: openai('gpt-6-astra'),
  prompt: 'Get the weather for San Francisco',
  text: ({ content }) => <div>{content}</div>,
  tools: {
    getWeather: {
      description: 'Get the weather for a location',
      inputSchema: z.object({ location: z.string() }),
      generate: async function* ({ location }) {
        yield <LoadingComponent />;
        const weather = await getWeather(location);
        return <WeatherComponent weather={weather} location={location} />;
      },
    },
  },
});
```

官方对 generator function 的说明逐字：*`function*`* ... *"By yielding values one at a time, generator functions enable efficient processing of streaming data without blocking the main thread."* 这给出一个被低估的界面契约：**`generate` 可以先 yield 一个 loading 组件，再 return 结果组件**——加载态属于组件流的一部分，不是另加的 spinner。

**裁决二的可执行形式（工程约定，强制）**：

1. 维护一张 `COMPONENT_REGISTRY` 白名单：`{ name → ReactComponent, schema → Zod }`。模型只输出 `{ name, props }`。
2. `name` 必须 `Object.hasOwn(registry, name)` 通过；未命中一律降级为纯文本，不抛给用户。
3. `props` 必须过 `schema.safeParse`，失败同样降级。**绝不 `dangerouslySetInnerHTML`、绝不 `eval`、绝不把模型字符串当组件名动态 import**。
4. 组件自带可访问名称与键盘可达性（生成出来的卡片也要能 Tab 到、能读屏念出来）——生成式 UI 不豁免 WCAG。
5. 组件流必须能被**停止 / 重生成 / 撤销**（§11），否则不要生成有副作用的组件。

**边界**：模型是 router，不是 designer。它选「显示天气卡」，不决定这张卡的对比度、圆角、字号；那些仍归 `design-tokens.md` / `accessibility.md` / `shape-elevation.md`。

---

## 7. AI SDK RSC experimental 与生产推荐路径（口径不张冠李戴）

RSC 文档页首逐字（**这句话只在这一页**）：

> AI SDK RSC is currently experimental. We recommend using AI SDK UI for production. For guidance on migrating from RSC to UI, see our migration guide.

**取源纪律**：`ai-sdk.dev/docs/ai-sdk-ui/chatbot` 页面里**没有**任何 "production" / "AI SDK RSC" / 推荐对比句。本轮实测该页的 `Recommended` 分别指「渲染 `parts` 而非 `content`」「显示泛化错误消息」「request-level options 优先于 hook-level」。**不得把 RSC 页的推荐句写成「chatbot 页说生产别用 RSC」**——写成「RSC 文档自述 experimental 并推荐 AI SDK UI 用于生产」才准确。

Next.js 接入形态（官方两步）：① `app/actions.tsx` 写 `'use server'` 的 Server Action，调 `streamUI` 并 `return result.value`；② `app/page.tsx` 写 `'use client'`，用 `useState<React.ReactNode>()` 接收并渲染。

```tsx
'use server';
import { streamUI } from '@ai-sdk/rsc';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';
export async function streamComponent() {
  const result = await streamUI({ /* model, prompt, text, tools */ });
  return result.value;
}
```

**选型结论（给立场）**：新项目默认走 AI SDK UI（`useChat` + `message.parts` + 组件白名单）；只有当「组件本身必须服务端流式、且接受 experimental + 迁移成本」时才上 RSC。别因为 `streamUI` 看起来酷就把整站搬过去。

---

## 8. useChat 四态状态机与 message.parts（parts 不是 content）

AI SDK UI Chatbot 官方对 `useChat` 的定位逐字：

> The `useChat` hook makes it effortless to create a conversational user interface for your chatbot application. It enables the streaming of chat messages from your AI provider, manages the chat state, and updates the UI automatically as new messages arrive.

三特性逐字：**Message Streaming**（real-time）、**Managed States**（input, messages, status, error and more）、**Seamless Integration**。

**`status` 四态（官方逐字释义，别自造第五态）**：

| `status` | 官方释义 | 界面落点（工程约定） |
|---|---|---|
| `submitted` | "The message has been sent to the API and we're awaiting the start of the response stream." | 用户消息已上屏；显示等待态；`role=status` 播「已提交，正在等待」 |
| `streaming` | "The response is actively streaming in from the API, receiving chunks of data." | 显示「停止」；禁用提交；`aria-busy=true` 挂在气泡 |
| `ready` | "The full response has been received and processed; a new user message can be submitted." | 恢复输入；`aria-busy=false`；播「已生成完毕」 |
| `error` | "An error occurred during the API request, preventing successful completion." | 泛化文案 + 重试；**不自动 focus** |

官方用途逐字：show a loading spinner / show a "Stop" button / disable the submit button。示例用 `status !== 'ready'` 禁用输入与提交。

**渲染必须走 `parts`，不是 `content`（官方逐字）**：

> The UI messages have a new `parts` property that contains the message parts. We recommend rendering the messages using the `parts` property instead of the `content` property. The parts property supports different message types, including text, tool invocation, and tool result, and allows for more flexible and complex chat UIs.

这一句是「生成式 UI 走 UI 路径」的技术支点：**文本、工具调用、工具结果统一是 message parts**，界面按 part 类型分派到白名单组件，而不是把整段回答当字符串渲染。TypeScript 侧用 `InferUITool` / `InferUITools` 把 tool 输入输出类型接到 `UIMessage`，保证 client/server 类型安全（官方原文：*"This provides full type safety for tool inputs and outputs on the client and server."*）。

**默认更新与节流**：官方 *"By default, `useChat` publishes message updates as each chunk is processed. React may batch multiple updates into a single render."*，React/Vue 可用 `throttle` 选项节流；但 *"Stream processing and event callbacks remain immediate, and the latest messages are published before the chat enters a terminal `ready` or `error` status."* → **节流可以，但终态前必须刷出最后一帧**，否则会出现「状态说已完成，界面停在半句」。

**Plain text 流的代价**：`streamProtocol: 'text'` / `TextStreamChatTransport` 下官方明确 *"tool calls, usage information and finish reasons are not available."* → 只要产品需要工具调用或生成式组件，就不能用纯文本流。

**错误文案口径**：官方 *"We recommend showing a generic error message to the user, such as 'Something went wrong.' This is a good practice to avoid leaking information from the server."*，默认遮蔽为 `"An error occurred."`；`providerExecuted: true` 的工具执行错误会**绕过 UI stream 的 `onError`**，官方警告 *"Do not rely on this callback to redact provider-executed tool execution errors before they reach the client."* → 脱敏必须做在服务端，不能指望前端回调。

---

## 9. AG-UI 对话状态机：RunStarted / RunError / TextMessageStart 与 messageId 归属

AG-UI（Agent-User Interaction Protocol）官方逐字：

> The Agent User Interaction Protocol uses a streaming event-based architecture. Events are the fundamental units of communication between agents and frontends, enabling real-time, structured interaction.

**生命周期边界逐字**：

> A typical agent run follows a predictable pattern: it begins with a `RunStarted` event, may contain multiple optional `StepStarted`/`StepFinished` pairs, and concludes with either a `RunFinished` event (success) or a `RunError` event (failure). ... The `RunStarted` and either `RunFinished` or `RunError` events are mandatory, forming the boundaries of an agent run.

> After a `RunError` event, no further processing will occur in this run.

**三种通用流模式逐字**：

> 1. **Start-Content-End Pattern**: Used for streaming content (text messages, tool calls) — Start initiates / Content delivers chunks / End signals completion
> 2. **Snapshot-Delta Pattern**: Used for state synchronization — Snapshot provides complete state / Delta events provide incremental updates
> 3. **Lifecycle Pattern**: Used for monitoring agent runs — Started signal beginnings / Finished·Error signal endings

文本流官方说明逐字：*"A message begins with a `TextMessageStart` event, followed by one or more `TextMessageContent` events ... and concludes with a `TextMessageEnd` event."*；*"The `TextMessageContent` events each contain a `delta` field ... Frontends should concatenate these deltas in the order received"*；*"The `messageId` property links all related events"*。工具调用同构：`ToolCallStart → ToolCallArgs → ToolCallEnd`，`ToolCallResult` 作为**完整单元**单独返回。

**实现纪律逐字**：

> - Events should be processed in the order they are received
> - Events with the same ID (e.g., `messageId`, `toolCallId`) belong to the same logical stream
> - Implementations should be resilient to out-of-order delivery

`StateSnapshot` 要**替换**而非合并本地状态（官方 *"Frontends should replace their existing state model with the contents of this snapshot rather than trying to merge it with previous state."*），`StateDelta` 是 RFC 6902 JSON Patch，按序 apply，发现分歧可请求新 snapshot。

**状态机映射（工程约定，把两套官方状态对齐）**：

| AG-UI 事件 | `useChat.status` | 播报（`role=status`） | UI 动作 |
|---|---|---|---|
| `RunStarted` / `TextMessageStart` | `submitted`→`streaming` | 「正在生成」 | 建气泡、置 `aria-busy=true`、显示停止 |
| `TextMessageContent` / `ToolCallArgs` | `streaming` | **不播报** | 追加 part，节流刷新 |
| `TextMessageEnd` / `ToolCallEnd` | `streaming` | **不播报** | 结束该 part |
| `RunFinished` | `ready` | 「已生成完毕」 | `aria-busy=false`、恢复输入 |
| `RunError` | `error` | 「生成失败，可重试」 | 泛化错误 + 重试；此后不再处理该 run 事件 |

**推理可见性边界**：AG-UI 的 `Reasoning*` 事件支持展示「可见部分」，而 `ReasoningEncryptedValue` 官方明确 *"without exposing raw chain-of-thought"*、*"The client stores and forwards these encrypted values opaquely"*。界面可展示进度摘要，**不要**假装展示完整思维链。`THINKING_*` 已弃用（"will be removed in version 1.0.0"），迁到 `REASONING_*`。

---

## 10. Hybrid UI 混合界面与 RICH 范式（WIMP 不是唯一解）

Ant Design X 官方 RICH 设计范式四要素：**Intention（意图）**、**Role（角色）**、**Conversation（会话）**、**Hybrid UI（混合界面）**。其官方立场是：AI 对话不是要取代 WIMP（Window / Icon / Menu / Pointer），而是与图形界面**混合**——自然语言负责表达模糊意图，图形控件负责精确操作、确认与批量编辑。

**判型决策表（工程约定）**：

| 用户任务 | 纯对话够吗 | 应补的图形控件 | 理由 |
|---|---|---|---|
| 开放式探索、写作、解释 | 够 | 复制 / 引用 / 重生成 | 输出是文本，无精确参数 |
| 筛选、比价、订票、填表 | **不够** | 表单 / 表格 / 日期选择 / 滑块 | 参数必须可枚举、可校验、可回改 |
| 有副作用的动作（下单、删除、发邮件） | **绝不够** | 确认卡片 + 可见参数 + 撤销 | HAX G9-C / `feedback-states.md §7` |
| 长任务 / 多步执行 | 不够 | ThoughtChain / 步骤进度 / Activity 区 | AG-UI `StepStarted/StepFinished`、`ActivitySnapshot/Delta` |
| 引用型答案（RAG） | 不够 | Sources / 引用角标 / 原文跳转 | 可举证性归 `ai-design-toolchain.md`，界面要有入口 |

Ant Design X 组件分组（官方 overview）：Bubble（消息气泡）、Sender（输入发送）、ThoughtChain（思维链可视化）、Prompts（快捷提示）、Sources（引用来源）等——**这正是「对话 + 图形件」的零件表**，不是一堆气泡皮肤。

**一条硬裁决**：凡是「用户点一下就能改准」的字段，就不要让用户「再说一遍自然语言」。让模型把不确定的意图翻成结构化表单，再由人确认——这是 Hybrid UI 相对纯 chat 的核心增益。

---

## 11. 裁决三：AI 答错了要高效纠错（HAX G9）——四档恢复链，不是重新生成按钮

Microsoft HAX Design Library G9 逐字：

> Guideline 9: Support efficient correction
> Make it easy to edit, refine, or recover when the AI system is wrong.
> Sometimes AI systems will be only partially correct. To ensure people can still achieve their goals when this happens, make it easy for the user to edit the AI system's outputs.

官方 G9 模式：G9-A *Switch classification decisions*、G9-B *Rich and detailed edits*、G9-C *Undo automated actions*、G9-D *Do G9 through G15*（把纠错能力贯穿到后续准则）、G9-E *Batch-editing data*。

**注意边界**：HAX 18 条完整表在 `ai-design-toolchain.md §10`；这里只把 G9 落成**界面动作清单**，不重复 18 条。arXiv `2010.11761`（Google PAIR 6 章 113 条 / Microsoft 18 条 / Apple 59 条比较）指出微软体系尤其强调**错误与心智模型**；这也是本轮把纠错独立成裁决的原因。

**四档恢复链（工程约定，按代价递增）**：

| 档 | 动作 | 用户成本 | 必须的状态归位 | 播报 |
|---|---|---|---|---|
| ① 停止 | `stop()` | 最低 | 中断 fetch、把气泡标「已停止（不完整）」、`ready` 可再发、`aria-busy=false` | 「已停止」 |
| ② 重试 / 重生成 | `regenerate()` | 低 | 替换最后一条回答、保留原提问、错误态清除 | 「已重新生成」 |
| ③ 编辑原消息重放 | `setMessages()` + 重新提交 | 中 | **停止进行中的响应并清空队列**、截断被编辑消息之后的对话分支、重放 | 「已按修改重放」 |
| ④ 撤销自动化动作 | 显式 Undo | 高但必要 | 回滚副作用、记录可举证日志、把结果标为「已撤销」 | 「已撤销：××」 |

官方对 `stop` 逐字：*"When the user clicks the 'Stop' button, the fetch request will be aborted. This avoids consuming unnecessary resources and improves the UX of your chatbot application."*；对 `regenerate` 逐字：*"the AI provider will regenerate the last message and replace the current one correspondingly."*

**队列的硬口径（官方逐字，最易被写错）**：

> "Editing a message or regenerating stops the response in progress and clears the queue, since the queued messages were sent after the part of the conversation that changes."
> "Stopping, an error or an interrupted response pauses the queue."
> "The queue lives in memory in the chat, so it is not saved and is lost on reload."

→ 所以「编辑第 3 条」不能只改那一条文本就重发；必须**砍掉第 3 条之后的所有分支**，否则界面会把基于旧上下文生成的回答留在屏上。队列功能官方标注 *"Message queueing is experimental."*，不要把它当持久化能力写进验收。

**HAX G9-C 的界面落点**：模型若执行了写操作（改字段、发消息、下单），必须在结果旁提供**同级可见**的「撤销」，且撤销后状态回到操作前；只有「重新生成」不算纠错——重新生成只改文本，改不回已发生的副作用。

---

## 12. stop / regenerate / setMessages 与状态边界播报一次（含清空队列）

把 §11 落成事件-动作对照，供实现直接抄：

| 用户动作 | 调用 | status 变化 | 队列 | 播报一次 | 禁止 |
|---|---|---|---|---|---|
| 发送 | `sendMessage({ text })` | →`submitted` | 默认响应中禁用输入 | 「已提交，正在等待」 | 连点产生两个 run |
| 首 chunk 到 | （流事件） | →`streaming` | — | 「正在生成」 | 每个 chunk 都播 |
| 完成 | `TextMessageEnd` + `RunFinished` | →`ready` | 恢复 | 「已生成完毕」 | 自动 focus 到回答 |
| 停止 | `stop()` | →`ready` | **暂停** | 「已停止」 | 把半截回答标成成功 |
| 失败 | `RunError` / `error` | →`error` | **暂停** | 「生成失败，可重试」 | 展示服务端原始报错 |
| 重生成 | `regenerate()` | →`submitted` | **清空** | 「已重新生成」 | 保留旧回答造成两条并存 |
| 编辑 | `setMessages()` + 重发 | →`submitted` | **清空 + 截断后续分支** | 「已按修改重放」 | 只改文本不截断 |
| 撤销副作用 | 自定义 Undo | 视业务 | 不变 | 「已撤销：××」 | 只写日志不给入口 |

**`aria-busy` 配对纪律**：进入 `streaming` 置 `true`；`ready` / `error` / `stop` 三个出口**都必须**置回 `false`。漏一个出口，读屏会永久静音该区域——这是静态扫描器（§20 代码 2）能直接查出的缺陷。

**回调口径**：`onFinish`（完成，含 abort / disconnect / errors 标志）、`onError`、`onData`；官方提示 *"you can abort the processing by throwing an error in the `onData` callback"*，可用于拦截异常响应，但不要拿它做脱敏（见 §8 `providerExecuted` 警告）。

---

## 13. 状态归位表：每个动作后哪些状态必须复位

收口（L5）是「模型输出不确定」带来的特有缺陷域：传统界面状态由用户操作驱动，AI 界面状态由**远端事件**驱动，事件丢失就永久错位。

| 状态位 | 进入 | 必须复位的出口 | 漏复位的症状 |
|---|---|---|---|
| `status` | submitted / streaming | ready / error / stop / regenerate / edit | 按钮永久禁用、输入框打不开 |
| `aria-busy` | streaming | ready / error / stop | 该区域读屏再不播报 |
| 提交按钮 disabled | 发送 | ready / error / stop | 明明结束了还发不出去 |
| 「停止」按钮可见 | streaming | ready / error / stop | 停止按钮悬空，点了没反应 |
| 气泡 loading 组件 | `generate` 的 `yield` | `return` 结果组件 / RunError | 永远转圈（RSC 生成器路径） |
| 队列 `experimental_queuedMessages` | 响应中排队 | 编辑 / 重生成 / stop / error 按 §11 规则 | 旧上下文的消息被发出去 |
| 错误展示 | error | 重试 / 新消息 | 错误条一直挂在屏上 |
| 自动滚动锁定 | 用户上滚 | 用户回到底部 | 用户读旧内容时被拖到最新 |
| 工具副作用 | 有写操作 | ④ 撤销 | 改了数据却没有回退路径 |

**验收方法**：拿一张表逐行做「进入 → 走每个出口 → 看界面」，任一出口没复位即 P1。这比跑一遍 happy path 有用得多。

---

## 14. 流式渲染工程：增量 Markdown、未闭合块、节流、自动滚动纪律

流式 Markdown 不是「把字符串拼起来交给 renderer」——**任意切分点都可能落在代码块、表格、链接、加粗标记中间**。§20 代码 3 实跑证明：同一段含代码围栏的 Markdown，按 7 / 13 / 29 字符切分，处于未闭合围栏期间的分片分别是 3 / 2 / 1 个。

**四条工程约定**：

1. **未闭合结构先 hold**：围栏代码块、表格、未闭合的 `**` / `[` 不要按原样渲染；补一个「渲染中」占位或临时闭合，等 End 事件再定型。Vercel `streamdown` 的仓库描述即为 *"A drop-in replacement for react-markdown, designed for AI-powered streaming."*（GitHub API 实测见 §21）。
2. **节流不等于丢帧**：`useChat` 的 `throttle` 只削渲染频率；官方保证终态前刷出最新消息，实现时仍要在 `ready` / `error` 前 flush 一次。
3. **自动滚动要能被用户否决**：用户向上滚动后停止跟随，显示「回到底部」按钮；生成完成不自动 focus（§5）。这是 `direct-manipulation.md` 的「用户控制权」在流式场景的延伸。
4. **防 CLS**：气泡高度用占位骨架锁定，组件白名单里的卡片给固定最小高度；图片/图表尺寸归 `responsive-layout.md §8` 与 `performance-design.md §5`，别让流式插入把页面顶跳。

---

## 15. L1 输入与发送：Enter / Shift+Enter、禁用提交、队列、中文场景

| 决策 | 约定 | 依据 |
|---|---|---|
| Enter 发送 / Shift+Enter 换行 | 多行输入默认此组合，并在输入框 `aria-describedby` 写明 | APG 键盘契约 + `ux-writing.md` 帮助文案 ≤16 字（工程约定） |
| 单行输入 | Enter 直接发送，不提供换行 | 同上 |
| 响应中禁用提交 | `status !== 'ready'`；官方示例即如此 | §8 `useChat` 官方用途 |
| 想允许边生成边打字 | `experimental_queue`（官方标注 experimental）；须知队列在内存、刷新即丢 | §11 官方逐字 |
| 停止按钮优先级 | 与发送按钮同位置同尺寸切换，不要藏在菜单里 | `feedback-states.md §4.5` 乐观更新三态 + 本文件 §12 |
| 中文提示词 | 不限制输入长度到「英文字符数」；中文按字计，别用 `maxLength=140` 卡中文 | `chinese-design.md` 中文排版口径（工程约定） |
| 附件 / 工具入口 | 图形按钮，别要求用户用自然语言描述「请读取我上传的文件」 | Hybrid UI（§10） |

---

## 16. 来源、引用与置信度呈现（与 HAX 18 条的边界）

本文件不重列 HAX G1–G18，但要把三条**界面落点**说清，避免与 `ai-design-toolchain.md §10` 互相抢路由：

- **能力边界（G1/G2）**属于「首次使用告知」，是产品说明层；本文件只在输入框附近留一个「能做什么 / 可能出错」入口，不写完整 18 条。
- **解释入口（G11）**属于回答旁的可展开说明；本文件要求它作为 `message.parts` 的一种 part 渲染，且展开不抢焦点。
- **低置信度收敛（G10）**属于模型策略；界面侧要把「给选项式追问」做成**可点的 Prompts 组件**，而不是又一段让用户自己组织的文本。

RAG / 引用型答案必须有 Sources 区与原文跳转（Ant Design X 官方组件分组含 Sources）；引用角标要可键盘聚焦、有 accessible name。可举证创作链的完整规则归 `ai-design-toolchain.md`，不在这里重复。

---

## 17. 12 个高频场景速查

| # | 场景 | 先判层 | 直接答案 |
|---|---|---|---|
| 1 | 做个聊天机器人 / chatbot UI | L1–L5 | §2 五段链路逐层过；先定状态机再画气泡 |
| 2 | 回答一个字一个字蹦出来，读屏一直念 | L3 | 正文进 `role=log`，状态边界才用 `role=status`；禁 assertive（§3 §4） |
| 3 | 生成中途用户想打断 | L2/L5 | `stop()` + 标「已停止（不完整）」+ 三个出口复位 `aria-busy`（§12 §13） |
| 4 | 答错了只能点重新生成 | L4 | 补四档恢复链，尤其编辑原消息与撤销副作用（§11） |
| 5 | 想让模型直接吐出一个卡片/图表 | L3 | 组件白名单 + `inputSchema`，模型只选 name+props（§6） |
| 6 | 要不要上 `streamUI` / RSC | L3 | RSC 自述 experimental 且推荐 UI 用于生产，默认 `useChat`+`parts`（§7） |
| 7 | 工具调用过程要不要给用户看 | L2/L3 | 看，但用 ThoughtChain / Activity 区展示摘要，不暴露原始思维链（§9 §10） |
| 8 | 筛选、填表、下单也用对话 | L3 | 不够；补表单 / 表格 / 确认卡片，Hybrid UI（§10） |
| 9 | 首 token 前白屏好几秒 | L2 | `submitted` 与 `streaming` 分开建模，别把等待当「没反应」（§8 §9） |
| 10 | 代码块 / 表格流式时闪成乱码 | L3 | 未闭合结构 hold 渲染，终态定型（§14 + 代码 3） |
| 11 | 生成完成页面自动跳到回答 | L3/L5 | 不抢焦点；给「跳到最新回答」按钮（§5） |
| 12 | 断线重连后对话历史错乱 | L2/L5 | `MessagesSnapshot` 替换而非合并；`StateDelta` 按序 apply（§9） |

---

## 18. 反模式 20 条

1. 把每个 token 塞进 `aria-live="assertive"` —— 官方 Failure 族 + chatty 风险。
2. 整个 `role=log` 容器挂 `aria-busy="true"` 且永不复位 —— 历史追加被抑制，读屏永久静音。
3. 生成完成自动 `focus()` 到回答 —— SC 4.1.3 前提是 *without receiving focus*。
4. 把 `role="alert"` 和 `aria-live="assertive"` 同时写上 —— 部分 AT 双播。
5. 用 `role=status` 播报整段回答 —— 状态容器只放一句话，正文进 log。
6. 动态创建 live region 后才写文本 —— AT 往往不播报；容器必须提前存在。
7. 生成式 UI 直接把模型返回字符串 `dangerouslySetInnerHTML` —— 越权 + 注入。
8. 组件名由模型自由生成、前端动态 import —— 必须查 `COMPONENT_REGISTRY` 白名单。
9. tool 不写 `inputSchema`，props 直接透传组件 —— 类型与边界双失守。
10. 因为 `streamUI` 看起来新就把新项目搬去 RSC —— 官方自述 experimental。
11. 把「生产推荐 AI SDK UI」这句安到 chatbot 文档头上 —— 该句只在 RSC 页（§7）。
12. 渲染 `message.content` 而不是 `message.parts` —— 丢掉 tool invocation / tool result。
13. 用 `TextStreamChatTransport` 还想要工具调用 —— 官方明说不可用。
14. 自造第五个 `status`（如 "thinking"）—— 状态归位表会漏出口；要展示进度用 `StepStarted`。
15. 编辑第 N 条消息只改文本、不截断后续分支 —— 官方要求清空队列。
16. 把 `experimental_queue` 当持久化队列写进验收 —— 内存态，刷新即丢。
17. 停止后把半截回答标成「已生成」—— 状态归位失败。
18. 有写操作的生成结果只给「重新生成」不给「撤销」—— 违反 G9-C。
19. 用户上滚看旧内容时仍强制自动滚到底 —— 抢走阅读控制权。
20. 流式 Markdown 未闭合围栏直接渲染 —— 代码块闪成正文（代码 3 实测）。

---

## 19. 自检 20 项（交付前逐条过）

1. [ ] 对话容器是 `role="log"` 且有 accessible name？隐性 polite / atomic=false 有没有被手动改坏？
2. [ ] 状态容器 `role="status"` 是否在页面加载时就存在（不是动态新建）？
3. [ ] 是否存在任何 `aria-live="assertive"` 绑定流式 `delta`？有即 P0。
4. [ ] `aria-busy` 的 ready / error / stop 三个出口是否都置回 false？
5. [ ] 状态边界播报是否各只一次、短句 ≤20 字、中文无技术词？
6. [ ] 生成完成是否**没有**自动移动焦点？
7. [ ] `status` 是否只用官方四态、每个出口都复位了提交按钮与停止按钮？
8. [ ] 是否渲染 `message.parts` 而非 `content`？三种 part 都有落点？
9. [ ] 组件白名单是否存在，未命中 name 是否降级为纯文本？
10. [ ] 每个 tool 是否都有 `inputSchema` 并过 `safeParse`？
11. [ ] 是否避免了 `dangerouslySetInnerHTML` / eval / 动态 import 模型字符串？
12. [ ] 若用了 RSC，是否记录 experimental 与迁移成本？选型结论是否写进交付说明？
13. [ ] 四档恢复链是否齐：停止 / 重试 / 编辑原消息 / 撤销自动化动作？
14. [ ] 编辑与重生成是否清空队列并截断后续对话分支？
15. [ ] 有副作用的生成结果是否提供同级可见的撤销？
16. [ ] 错误文案是否泛化、脱敏是否做在服务端（不依赖 `onError` 遮蔽）？
17. [ ] 未闭合代码块 / 表格在流式期间是否 hold 或临时闭合？
18. [ ] 终态前是否 flush 最后一次渲染（节流不丢最后一帧）？
19. [ ] 用户上滚后是否停止自动跟随并提供「回到底部」？
20. [ ] 键盘能否完成发送 / 停止 / 重生成 / 撤销全流程，焦点顺序是否不被生成事件打乱？

---

## 20. 可抄代码 5 段（3 段 Python 实跑，输出为本轮实测）

### 代码 1 · AG-UI 事件流校验器（Python，实跑）

校验 RunStarted / RunError 生命周期边界、Start-Content-End 三元组闭合、messageId 归属。

```python
events = [
    {"type": "RunStarted", "runId": "r1", "threadId": "t1"},
    {"type": "TextMessageStart", "messageId": "m1", "role": "assistant"},
    {"type": "TextMessageContent", "messageId": "m1", "delta": "已"},
    {"type": "TextMessageContent", "messageId": "m1", "delta": "查到 3 条"},
    {"type": "ToolCallStart", "toolCallId": "c1", "toolCallName": "search"},
    {"type": "ToolCallArgs", "toolCallId": "c1", "delta": "{\"q\":"},
    {"type": "ToolCallEnd", "toolCallId": "c1"},
    {"type": "TextMessageEnd", "messageId": "m1"},
    {"type": "RunFinished", "runId": "r1"},
]

def audit(seq):
    errs = []
    if not seq or seq[0]["type"] != "RunStarted":
        errs.append("首事件不是 RunStarted")
    if not seq or seq[-1]["type"] not in ("RunFinished", "RunError"):
        errs.append("末事件不是 RunFinished / RunError")
    for i, e in enumerate(seq[:-1]):
        if e["type"] in ("RunFinished", "RunError"):
            errs.append("L%d 终止边界之后仍有事件" % (i + 1))
    opening = {}
    for e in seq:
        t = e["type"]
        if t in ("ToolCallResult", "TextMessageChunk", "ToolCallChunk"):
            continue  # 完整单元 / 自动展开的便利事件，不走三元组
        if t.startswith("TextMessage") or t.startswith("ToolCall"):
            k = e.get("messageId") or e.get("toolCallId")
            if t.endswith("Start"):
                if k in opening: errs.append("%s 重复 Start" % k)
                opening[k] = t
            elif t.endswith("End"):
                if k not in opening: errs.append("%s End 无 Start" % k)
                else: opening.pop(k)
            else:
                if k not in opening: errs.append("%s %s 无 Start" % (k, t))
    for k, t in opening.items():
        errs.append("%s %s 未闭合（缺 End）" % (k, t))
    return errs

print("合法流:", audit(events) or "PASS · 0 处违规")
bad = [e for e in events if e["type"] != "ToolCallEnd"] + [
    {"type": "TextMessageContent", "messageId": "m9", "delta": "迟到的 chunk"}]
print("注入违规:", audit(bad))
```

实跑输出：

```text
合法流: PASS · 0 处违规
注入违规: ['末事件不是 RunFinished / RunError', 'L8 终止边界之后仍有事件', 'm9 TextMessageContent 无 Start', 'c1 ToolCallStart 未闭合（缺 End）']
```

### 代码 2 · live region 契约扫描器（Python，实跑）

静态扫描 `role=log` / `role=status` / assertive 滥用 / `aria-busy` 未复位。

```python
import re

html_bad = '''<div role="log" aria-label="对话记录"><ul id="conversation"></ul></div>
<div aria-live="assertive" id="token-feed"></div>
<div aria-busy="true" id="bubble"></div>'''
html_ok = '''<div role="log" aria-label="对话记录"><ul id="conversation"></ul></div>
<div role="status" id="gen-status">准备就绪</div>
<div aria-busy="false" id="bubble"></div>'''

def scan(src):
    issues = []
    if 'role="log"' not in src:
        issues.append("缺 role=log 对话容器（ARIA23）")
    if re.search(r'aria-live="assertive"', src):
        issues.append("assertive live region 用于非紧急内容（F103 失败族）")
    if 'role="status"' not in src:
        issues.append("缺状态边界播报容器 role=status")
    busy = len(re.findall(r'aria-busy="true"', src))
    if busy:
        issues.append("%d 处 aria-busy=true 未在收口时置回 false" % busy)
    return issues or ["PASS · 0 处违规"]

print("坏例:", scan(html_bad))
print("修正:", scan(html_ok))
```

实跑输出：

```text
坏例: ['assertive live region 用于非紧急内容（F103 失败族）', '缺状态边界播报容器 role=status', '1 处 aria-busy=true 未在收口时置回 false']
修正: ['PASS · 0 处违规']
```

### 代码 3 · 流式 Markdown 分片鲁棒性（Python，实跑）

证明任意切分点会落在未闭合围栏内，必须 hold。

```python
FENCE = "`" * 3  # 用变量拼围栏，避免文档源码里出现额外的三反引号破坏 Markdown 配对
md = ("结果如下：\n\n" + FENCE + "python\nprint('ok')\n" + FENCE +
      "\n\n| 项 | 值 |\n|---|---|\n| A | 1 |\n")
def chunks(s, n): return [s[i:i+n] for i in range(0, len(s), n)]
for n in (7, 13, 29):
    buf, held = "", 0
    for c in chunks(md, n):
        buf += c
        if buf.count(FENCE) % 2 == 1:
            held += 1
    print("chunk=%2d 分片数=%2d 未闭合围栏期间收到分片=%2d" % (n, len(chunks(md, n)), held))
```

实跑输出：

```text
chunk= 7 分片数=10 未闭合围栏期间收到分片= 3
chunk=13 分片数= 5 未闭合围栏期间收到分片= 2
chunk=29 分片数= 3 未闭合围栏期间收到分片= 1
```

### 代码 4 · 生成式 UI 组件白名单分派（TypeScript / React）

```tsx
import { z } from 'zod';

const WeatherCard = (p: { location: string; weather: string }) => (
  <section aria-label={`${p.location}天气`}>
    {p.location}：{p.weather}
  </section>
);

const REGISTRY = {
  WeatherCard: { component: WeatherCard, schema: z.object({ location: z.string(), weather: z.string() }) },
} as const;

type GenPart = { name: string; props: unknown };

export function renderGenerated(part: GenPart): React.ReactNode {
  const entry = Object.prototype.hasOwnProperty.call(REGISTRY, part.name)
    ? REGISTRY[part.name as keyof typeof REGISTRY]
    : null;
  if (!entry) return <p>暂不支持展示该内容</p>;          // 未命中降级为纯文本
  const parsed = entry.schema.safeParse(part.props);
  if (!parsed.success) return <p>内容格式异常，已按文本显示</p>;
  const Component = entry.component as React.ComponentType<typeof parsed.data>;
  return <Component {...parsed.data} />;
}
```

### 代码 5 · 对话容器的无障碍骨架（HTML）

```html
<!-- 容器必须提前存在；role=log 隐性 polite / atomic=false，只播新增整条消息 -->
<section role="log" aria-label="对话记录" id="conversation">
  <ol id="messages"><!-- 每条消息作为一个 li 追加，不追加 token --></ol>
</section>

<!-- 状态边界独立容器；只写一句短文本，每个边界一次 -->
<div role="status" id="gen-status">准备就绪</div>

<!-- aria-busy 挂「正在生成的气泡」，不是整个 log；三个出口都要置回 false -->
<div id="bubble-streaming" aria-busy="false"></div>

<form id="composer">
  <label for="prompt">输入消息</label>
  <textarea id="prompt" aria-describedby="composer-hint"></textarea>
  <p id="composer-hint">Enter 发送，Shift+Enter 换行</p>
  <button type="submit" id="send">发送</button>
  <button type="button" id="stop" hidden>停止</button>
  <button type="button" id="regenerate" hidden>重新生成</button>
  <button type="button" id="undo" hidden>撤销</button>
</form>
```

---

## 21. GitHub API 实测仓库（2026-11-11 经 GitHub API）

star / license / pushed_at / archived 均为本轮 `api.github.com/repos/...` 实测，不凭记忆写数字；`NOASSERTION` 表示 GitHub 未检出明确 SPDX，不代表「无许可」。

| 仓库 | ★ | License (SPDX) | pushed_at | archived | 官方 description（节选） |
|---|---:|---|---|---|---|
| `vercel/ai` | 27,865 | NOASSERTION | 2026-11-11 | false | The AI Toolkit for TypeScript ... free open-source library for building AI-powered applications and agents |
| `ant-design/x` | 4,844 | 未检出 | 2026-10-29 | false | Craft AI-driven interface effortlessly |
| `assistant-ui/assistant-ui` | 13,060 | MIT | 2026-11-11 | false | Typescript/React Library for AI Chat |
| `CopilotKit/CopilotKit` | 38,631 | MIT | 2026-11-11 | false | The Frontend Stack for Agents & Generative UI ... Makers of the AG-UI Protocol |
| `open-webui/open-webui` | 158,371 | NOASSERTION | 2026-11-11 | false | User-friendly AI Interface (Supports Ollama, OpenAI API, ...) |
| `ag-ui-protocol/ag-ui` | 17,110 | MIT | 2026-11-11 | false | AG-UI: the Agent-User Interaction Protocol. Bring Agents into Frontend Applications. |
| `vercel/streamdown` | 5,754 | NOASSERTION | 2026-11-10 | false | A drop-in replacement for react-markdown, designed for AI-powered streaming. |

**选型读法（工程约定）**：要协议级事件流看 AG-UI；要 React 聊天零件看 assistant-ui / Ant Design X（中文生态友好）；要 agent 与生成式 UI 全栈看 CopilotKit；要流式 Markdown 渲染看 streamdown；要底层模型流看 vercel/ai。`NOASSERTION` 的库进商业项目前必须自行核对 LICENSE 文件。

---

## 22. 与其他资产的边界（避免重复与抢路由）

| 邻域 | 归谁 | 本文件只做什么 |
|---|---|---|
| HAX G1–G18 人机交互 18 条 | `ai-design-toolchain.md §10` | 只把 G9 落成四档恢复链；不重列 18 条 |
| AI 生成内容标识 / 版权 / AI 味 | `ai-design-toolchain.md §2 §4 §11` | 不碰 |
| 加载态 / 骨架 / toast 时长 / 空态 / 乐观更新 | `feedback-states.md` | 只处理「流式期间」这一新形态与状态归位 |
| WCAG 阈值 / 焦点三层 / 读屏实测脚本 | `accessibility.md` | 只用 SC 4.1.3 / ARIA23 的流式语义，不重讲 4.5:1 |
| 性能预算 / CLS / 字体加载 | `performance-design.md` | 只提流式插入的 CLS 与节流 |
| 响应式 / 图片尺寸 | `responsive-layout.md` | 不碰 |
| 按钮与错误文案 | `ux-writing.md` | 只给状态边界短句口径 |
| 拖拽 / 指针 / 目标尺寸 | `direct-manipulation.md` | 不碰；自动滚动控制权是其「用户控制权」的延伸 |
| 组件 API / 受控非受控 | `component-api-design.md` | 不碰；白名单是安全边界不是 API 设计 |

`ai-design-toolchain.md` 的分流表已同步修正：原则层（HAX 18 条）仍归该文件，链路层（流式 / 混合界面 / 纠错）归本文件。

---

## 23. 取源限制（公开记录，不臆造）

1. **W3C WAI-ARIA 1.2 TR `#log` 被 Cloudflare 拦截**：只返回 `Just a moment...`，未取得 normative definition / Superclass Role / Implicit Value。`w3c.github.io/aria/#log`（ED）内容被截断，只见 role 名在列表中。→ 本文件 `role=log` 隐性值以 **W3C ARIA23 技术页逐字**为准，`aria-relevant` 等以 MDN 为准，并标注来源；不引用未取得的 TR 原文。
2. **Google PAIR 原站 cookie wall**：`pair.withgoogle.com/guidebook/` 与 `/guidebook/patterns` 只返回 cookie notice，未取得章节与 patterns 逐字正文。→ Google 6 章 / 113 条、Microsoft 18 条、Apple 59 条、统一分类体系与差异，改用 arXiv `2010.11761` **HTML 版**交叉核验；arXiv PDF 为 `application/pdf` 非文本资源，本机 curl 亦失败，故不用 PDF。
3. **`x.ant.design/docs/spec/conversation` 404**：Conversation 子页未取得。→ RICH 范式与 Hybrid UI 取自 `x.ant.design/docs/spec/introduce`，组件分组取自 `x.ant.design/components/overview/`。
4. **Vercel `ai-sdk.dev/docs/ai-sdk-ui/streaming-ui` 与 `generative-ui` 404**：→ 改用 `sdk.vercel.ai/docs/ai-sdk-rsc/streaming-react-components` 与 `ai-sdk.dev/docs/ai-sdk-ui/chatbot`。
5. **`nngroup.com/articles/ai-ux/` 404**（页面自带 *AI chat may hallucinate nonexistent NN/G articles* 提示）：→ 未引用任何 NN/g AI/UX 具体文章结论；本轮 NN/g 相关内容全部沿用既有资产已验证的口径。
6. **本机 `curl` / `urllib` 到 `api.github.com` 被阻断**（`http=000` / exit 35 / WinError 10061）：→ 仓库字段改走 WebFetch 的 GitHub API 通道实测，7 个仓库逐个取回。
7. **口径不张冠李戴**：`ai-sdk.dev/docs/ai-sdk-ui/chatbot` 页**没有**「生产推荐 AI SDK UI 而非 RSC」这句话；该句只出现在 RSC 页。本文件 §7 明确区分，不把两页内容合并引用。
8. **未量化项不编数值**：本文件所有「≤20 字短句」「8 档验收」类建议均标注为工程约定；规范数值只引 SC 4.1.3 条文、ARIA23 隐性值与 `status` 四态原文。HAX 18 条未逐条标注阶段归属（官方设计库未给），本文件不臆造。

---

## 24. 数据来源清单

- W3C WCAG 2.2 Understanding SC 4.1.3 Status Messages — https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
- W3C Technique ARIA23 `role=log` — https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA23
- W3C Techniques ARIA22 / ARIA19 / ARIA25 / ARIA27 / G199 / G193 / F103 — https://www.w3.org/WAI/WCAG22/Techniques/
- MDN ARIA: log role / ARIA live regions / `aria-busy` — https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA
- Microsoft HAX Design Library G9 Support efficient correction — https://www.microsoft.com/en-us/haxtoolkit/guideline/support-efficient-correction/
- Microsoft HAX Toolkit G1–G18 — https://www.microsoft.com/en-us/haxtoolkit/library/
- arXiv 2010.11761（HTML 版，三套 AI 指南比较） — https://arxiv.org/html/2010.11761v1
- Ant Design X RICH 范式 / 组件总览 — https://x.ant.design/docs/spec/introduce · https://x.ant.design/components/overview/
- Vercel AI SDK RSC Streaming React Components — https://sdk.vercel.ai/docs/ai-sdk-rsc/streaming-react-components
- Vercel AI SDK UI Chatbot / `useChat` — https://ai-sdk.dev/docs/ai-sdk-ui/chatbot
- AG-UI Events / 协议文档 — https://docs.ag-ui.com/concepts/events · https://ag-ui.com
- GitHub API 实测仓库：`vercel/ai`、`ant-design/x`、`assistant-ui/assistant-ui`、`CopilotKit/CopilotKit`、`open-webui/open-webui`、`ag-ui-protocol/ag-ui`、`vercel/streamdown`

---

## 25. 术语与口径速记

| 词 | 本文件口径 | 常见误用 |
|---|---|---|
| 状态消息 status message | SC 4.1.3 定义的内容变更，**不含焦点变化** | 把回答正文当状态消息逐 chunk 播报 |
| `role=log` | 顺序追加信息的 live region，隐性 polite / atomic=false | 拿它当进度条、或再挂 assertive |
| `aria-busy` | 多段更新期间抑制播报，**完成必须置回 false** | 挂在容器上且漏复位 |
| Generative UI / GenUI | 模型在**组件白名单**里路由，返回 name + props | 模型直接返回 JSX / HTML |
| `message.parts` | text / tool invocation / tool result 的统一分派单元 | 继续渲染 `content` 字符串 |
| Hybrid UI | 自然语言表达意图 + 图形控件精确操作 | 用纯对话做筛选 / 下单 / 填表 |
| 四档恢复链 | 停止 / 重试 / 编辑原消息 / 撤销自动化动作 | 只给「重新生成」 |
| 五段链路 | 发得出·等得住·读得动·改得动·收得回 | 一上来改气泡样式 |

---

**接线**：SKILL.md 资产表 / 意图路由 / 第 5 步 / 第 40 条自检 · mindmap INTENTS · regression NEW_QUERIES · knowledge-map 支线 AD · memory/aliases.json 检索层别名（不改路由优先级）· README 统计重算。
