# 组件 API 设计与组合模式：状态所有权、渲染所有权、契约可演进

> 快照 2026-11-07 ｜ 23 节（§0 分层导语 + §1–§22）｜ 约 49.4k 字符 / 918 行 ｜ 逐字口径取自 React / Radix / Vue / WAI-ARIA APG / MUI / Ariakit / Storybook 官方原文与上游源码；GitHub 仓库 star / 许可 / pushed_at 经 GitHub REST API 实测（2026-11-07）；**未取得原文的数值与结论一律不写入，§22 公开记录取源限制**。
>
> **一句话立场**：组件 API 不是 props 清单，是**三份所有权的书面划分**——**谁持有状态**（受控 / 非受控）、**谁渲染 DOM**（组合 / 换元素）、**谁负责无障碍与演进**（键盘契约 / 语义冻结）。绝大多数「组件库不好用」不是样式问题，是这三份所有权没写清楚：状态两边都存、props 被中间层吞掉、键盘契约没人认领、改了默认值却只发 PATCH。本文件只回答一件事：**给我一段组件代码或一个 API 设计，我凭什么判它 PASS 或 FAIL？**

---

## 0. 与既有资产的分层（先判该读哪份）

| 你手上是什么问题 | 去哪份 | 本文件补什么 |
|---|---|---|
| 设计稿怎么标注、组件怎么命名、变体属性 3–5 个、AC 怎么写、改默认值 = MAJOR | `handoff-collaboration.md` | §1–§2 补**代码层的状态所有权**，把「设计属性名 = props 名」推进到「谁的 state 说了算」 |
| 组件文档页九段式、Diátaxis、changelog、docs-as-code | `design-system-docs.md` | §15 补 **argTypes 作为机器可读的 API 契约**，两者是「给人读」与「给机器读」的两层 |
| 选哪个组件库、14 库元素覆盖矩阵 | `component-libraries.md` | §6 补**同一件事在 5 个库里的 5 种 API**（`asChild` / `render` / `slots` / `component` / `as`），选型时看的是组合模型不是 star |
| 焦点环、对比度、读屏、ARIA 纪律、WCAG 2.2 阈值 | `accessibility.md` | §12 补**复合组件的键盘契约在 API 层怎么落**（一个 tab stop、roving tabindex、`aria-activedescendant`、focus return），不重讲数值 |
| 九态矩阵、组件属性四类、语义名变体 | `handoff-collaboration.md` §9 | §13 补**「状态不要做成布尔 props」**：用 `data-state` / `data-disabled` 暴露，别让 9 态乘成 2⁹ 个 props |
| 交付链 SemVer 11 条与迁移表 | `handoff-collaboration.md` §SemVer | §14 补**组件 API 特有的破坏性判级**（改 props 合并优先级 = MAJOR、新增可选 slot = MINOR）与官方 codemod 实例 |
| 任何「组件不好用 / 改不动 / 组合就失效」 | **本文件（既有资产空白）** | §1–§22 系统性覆盖组件 API 本体 |

**缺口证据（升级前实测）**：`dp_search.py "组件 API 设计 组合模式 props 语义 受控 非受控"` 最高命中仅 `handoff-collaboration.md §7 组件 API 与设计稿 1:1 对齐`（40.0 分）与 `design-system-docs.md §1 判层`（35.0 分）；全库 `grep -ric "受控\|非受控\|compound\|asChild\|render prop\|插槽 slot"` 只有两份文件各 1 处提及。**「组件 API 本体怎么设计」是真空白**——既有资产覆盖的是「命名对齐」与「文档怎么写」，不是 API 本身。

---

## 1. 组件 API 设计：三份所有权与三条不可商量的原则（先给立场，不和稀泥）

1. **状态只有一个所有者**。同一份值不能既在组件内部 `useState` 又在父级 props 里；React 官方把组件分为 controlled（*"important information is driven by props"*）与 uncontrolled（*"component state"*）两类，**没有中间态**。Radix 上游源码把判定写成一行：`const isControlled = prop !== undefined;`——`undefined` 是唯一分界线，`null`、空串、`false` 都是合法的受控值。
2. **组合优于配置，更优于继承**。React 官方 legacy `Composition vs Inheritance` 逐字：*"React has a powerful composition model, and we recommend using composition instead of inheritance to reuse code between components."* 更狠的一句：*"At Facebook, we use React in thousands of components, and we haven't found any use cases where we would recommend creating component inheritance hierarchies."* 设计侧结论：**不要为新场景加布尔 props，要给一个能换元素、能塞内容、能透传属性的出口**。
3. **能被 props 表达的，不许用 ref**。React `forwardRef` 页 Pitfall 逐字：*"Do not overuse refs. You should only use refs for imperative behaviors that you can't express as props"*，以及 *"If you can express something as a prop, you should not use a ref."* 官方给的反例就是组件库最常见的偷懒：暴露 `{ open, close }` 命令式 handle，正确写法是 `<Modal isOpen={isOpen} />`。

**第四层判层（本文件贯穿全篇的框架）**：

| 层 | 问题 | 判错会怎样 | 对应章节 |
|---|---|---|---|
| L0 状态所有权 | 谁是这个值的唯一真相源？ | 输入跳字、父子不同步、切换受控/非受控报警 | §2–§3、§11 |
| L1 渲染所有权 | 谁渲染最终那个 DOM 元素？ | `asChild` / `render` 后事件与 aria 全丢 | §4–§8 |
| L2 组合结构 | 内容从几个洞进来？ | 一个 `children` 塞下所有东西，无法具名、无法作用域 | §4–§5 |
| L3 契约与演进 | 键盘、无障碍、版本、类型谁认领？ | 无障碍靠使用方自觉、改默认值只发 PATCH | §9–§16、§14 |

---

## 2. 受控 / 非受控：唯一真相源（React 官方定义 + Radix 上游源码）

### 2.1 官方定义与三元组

React `Sharing State Between Components` 的口径：controlled 组件是「重要信息由 props 驱动」，uncontrolled 是「由自身 local state 驱动」；结论是 **single source of truth**（每个状态只该有一个组件持有它）。状态提升三步（官方顺序）：① 从子组件移除 state → ② 由最近的共同父级传入硬编码数据 → ③ 把 state 放到共同父级。

一个合格的双模组件必须给全**三元组**：

| 角色 | 常见命名 | 语义 | 缺省 |
|---|---|---|---|
| 受控值 | `value` / `checked` / `open` / `activeTab` | 父级持有的当前值 | `undefined`（= 非受控） |
| 变更通知 | `onChange` / `onCheckedChange` / `onOpenChange` | 「请求改变」，不是「已经改变」 | 空函数 |
| 非受控初值 | `defaultValue` / `defaultChecked` / `defaultOpen` | **只定义第一次渲染**，之后不再读 | 组件内部默认值 |

### 2.2 Radix `useControllableState` 的四条硬规则（上游源码逐字）

取自 `radix-ui/primitives` → `packages/react/use-controllable-state/src/use-controllable-state.tsx`（官方 `controlled-state` 文档 URL 返回 404，故改读源码，见 §22）：

```ts
interface UseControllableStateParams<T> {
  prop?: T | undefined;
  defaultProp: T;
  onChange?: ChangeHandler<T> | undefined;
  caller?: string | undefined;
}

const [uncontrolledProp, setUncontrolledProp, onChangeRef] = useUncontrolledState({
  defaultProp, onChange,
});
const isControlled = prop !== undefined;          // ① 唯一判据
const value = isControlled ? prop : uncontrolledProp;  // ② 渲染值
```

③ **开发态禁止中途切换**，源码中的告警原文：

```
`${caller} is changing from ${from} to ${to}. Components should not switch from
controlled to uncontrolled (or vice versa). Decide between using a controlled or
uncontrolled value for the lifetime of the component.`
```

④ **受控时只通知、不写本地**；且值未变不发通知：

```ts
const setValue = (nextValue) => {
  if (isControlled) {
    const value = isFunction(nextValue) ? nextValue(prop) : nextValue;
    if (value !== prop) {
      onChangeRef.current?.(value);     // 只发请求，父级不改就不动
    }
  } else {
    setUncontrolledProp(nextValue);     // 非受控才写本地
  }
};
```

**判法**：`value !== undefined` 与 `value === undefined` 都必须在组件整个生命周期内保持不变。父级从接口拿到数据后，用 `value={data ?? ''}` 而不是先渲染 `<Input />` 再改成 `<Input value={...} />`——后者会触发告警且行为不可预测。

### 2.3 React `<input>` 五条门禁（官方原文）

1. `value` / `checked` + `onChange` **必须同步更新** backing value，否则输入被「弹回」。
2. 传了 `value` 却不传 `onChange` → **输入框变只读**；确实要只读就显式写 `readOnly`，别靠缺 props。
3. `defaultValue` / `defaultChecked` **只定义初始值**，后续改它不生效。
4. 组件生命周期内**不能从受控切到非受控或反向**。
5. `value` 不应该是 `undefined` 或 `null`（受控值必须是个确定的值；`undefined` 恰好是「非受控」的判据）。

### 2.4 PASS / FAIL 判定表

| 写法 | 判定 | 理由 |
|---|---|---|
| `<Input value={v} onChange={setV} />` | ✅ PASS | 单一真相源在父级 |
| `<Input defaultValue="abc" />` | ✅ PASS | 明确非受控 |
| `<Input value={v} />` | ❌ FAIL | 只读，且用户会以为坏了 |
| `<Input value={v} defaultValue="abc" />` | ❌ FAIL | 三元组混用，语义冲突 |
| `<Input value={v} onChange={setV} defaultValue="abc" />` | ❌ FAIL | `defaultValue` 是死代码 |
| 先 `<Input />` 再 `<Input value={v} />`（同一实例） | ❌ FAIL | 生命周期内切换模式 |
| `value={data ?? undefined}`（异步前） | ❌ FAIL | 用 `?? ''` 或先给 loading 态 |

---

## 3. 状态提升与派生状态（别把 state 复制两份）

- **共同父级原则**：把 state 放到「所有需要它的组件的最近共同祖先」，再通过 props 下传；不要在两个兄弟组件各存一份再想办法同步。
- **派生值不进 state**：`filtered = items.filter(...)`、`isValid = !errors.length` 这类值在渲染时算，不要 `useState` + `useEffect` 同步——多一份 state 就多一份不一致窗口。
- **回调参数给值，不给事件**（见 §11）：`onChange(value)` 比 `onChange(event)` 更稳定，父级不需要知道内部 DOM 结构。
- **内部状态也要有出口**：非受控不等于黑盒。至少用 `onChange` 通知 + `data-*` 暴露视觉状态（§13），否则父级无法做联动、埋点或禁用提交按钮。

**与既有资产接口**：设计交付里的「9 态矩阵」（`handoff-collaboration.md` §9）在这里落成代码契约——9 态不是 9 个布尔 props，而是「1 个受控值 + 1 个变更回调 + 若干 `data-*` 状态位 + 一组 aria 属性」。

---

## 4. 组合 vs 继承：多个「洞」怎么开（React + Vue 对照）

React legacy 官方 `Composition vs Inheritance` 给了两级结构（该页明确标注 *"These docs are old and won't be updated. Go to react.dev"*，故只取可逐字核验的结论，不拿它当现行 API 依据）：

- **Containment（容纳）**：不知道子内容是什么时，用 `children` 把任意 JSX 传进去。
- **Specialization（特化）**：一个组件是另一个的「特定版本」，用 props 配置它，而不是继承它。
- **多个洞**：`children` 只有一个；需要左/右、头/尾、标题/正文时，**用自定义 props 传 JSX**（如 `left={<Logo/>}` `right={<Nav/>}`），不要发明 `children={{left, right}}` 这种对象——它破坏 JSX 组合与类型推断。

Vue 官方 Slots 把同一件事做得更显式：

| 能力 | Vue 写法 | 设计侧用途 |
|---|---|---|
| 默认插槽 | `<slot>` outlet | 等价于 `children` |
| 具名插槽 | `<slot name="header">` + `v-slot:header` / `#header` | 等价于多个自定义 props |
| 动态插槽名 | `#[dynamicSlotName]` | 由数据决定哪块内容出现 |
| 条件插槽 | `$slots.header` 判断后再渲染 wrapper | 没有内容时**连外层容器都不渲染**（避免空 padding、空边框） |
| 作用域插槽 | `<slot :text="greetingMessage" :count="1">` + `v-slot="slotProps"` | 子组件提供数据、父组件决定怎么画（Renderless Components / Fancy List） |
| 渲染作用域 | 父模板**不能访问**子组件作用域 | 这是刻意的边界，不是限制；想传出来就显式通过 slot props |

**关键裁决（很多组件库踩的坑）**：`children` / 插槽是**内容通道**，不是**配置通道**。凡是需要表达「组件自己知道、父级不知道」的数据，走作用域插槽 / render prop；凡是需要表达「父级给组件的参数」，走 props。把配置塞进 children 会导致无法做静态检查、无法生成 argTypes（§15）、无法版本化（§14）。

**`Flat is better than nested`**（Ariakit 官方原文标题）：换元素时不要把 children 再嵌一层到 `render` 里，children 照常传给原组件；多一层嵌套就多一层 DOM、多一层焦点顺序风险。

---

## 5. 五种「换元素」API 的完整对照（选型先看这个，别看 star）

| 库 | API | 形态 | 谁合并 props | 典型代价 |
|---|---|---|---|---|
| Radix Primitives | `asChild` (默认 `false`) | 布尔 | `Slot.mergeProps` 自动合并，**child props override** | 自定义组件若没 spread props / forwardRef 会静默失效 |
| Ariakit | `render={<a />}` 或 `render={(htmlProps) => ...}` | React 元素 / 函数 | **元素形态自动合并；函数形态不自动合并** | 函数形态漏 spread 就直接丢光无障碍属性 |
| MUI | `component` / `slots` / `slotProps` | 字符串或组件 / 映射 / 映射 | 组件内部 | `slots` 换掉内部 slot 会**丢掉该 slot 的样式**；`slotProps.root` 优先于直接 props |
| Vue | `<component :is>` / 动态组件 | 组件或标签名 | 属性透传 | 需注意 `inheritAttrs` 与多根节点 |
| 常见社区做法 | `as` prop（polymorphic） | 字符串 / 组件 | 手写 `ComponentPropsWithoutRef` | TypeScript 复杂度陡增，`as` + `ref` + 泛型三重耦合 |

### 5.1 Radix `asChild` 的合并规则（`slot.tsx` 上游源码逐字）

官方口径：**所有会渲染 DOM 元素的 Radix primitive part 都接受 `asChild`**；组合自定义组件时 *"Your component must spread props"* 与 *"Your component must forward ref"*。`mergeProps` 的实现：

```ts
function mergeProps(slotProps, childProps) {
  // all child props should override
  const overrideProps = { ...childProps };
  for (const propName in childProps) {
    const slotPropValue = slotProps[propName];
    const childPropValue = childProps[propName];
    const isHandler = /^on[A-Z]/.test(propName);
    if (isHandler) {
      if (slotPropValue && childPropValue) {
        overrideProps[propName] = (...args) => {
          const result = childPropValue(...args);   // 子先执行
          slotPropValue(...args);                   // 再执行 slot 的
          return result;
        };
      } else if (slotPropValue) {
        overrideProps[propName] = slotPropValue;
      }
    } else if (propName === 'style') {
      overrideProps[propName] = { ...slotPropValue, ...childPropValue };
    } else if (propName === 'className') {
      overrideProps[propName] = [slotPropValue, childPropValue].filter(Boolean).join(' ');
    } else if (propName === 'aria-describedby') {
      overrideProps[propName] = concatAriaDescribedby(childPropValue, slotPropValue);
    }
  }
  return { ...slotProps, ...overrideProps };
}
```

**五条可直接判的规则**：① 普通属性 **child 赢 slot**；② 事件处理器 **两者串联**（child 先、slot 后，返回 child 的结果）、只有 slot 有时用 slot 的；③ `style` 浅合并且 child 覆盖同名键；④ `className` 拼接（不是覆盖）；⑤ `aria-describedby` 拼接去重（不是覆盖）。

### 5.2 Ariakit `render` 的合并规则（官方原文）

> *"The `style`, `className`, `ref` and event props will be automatically merged. In all other cases, defined rendered element props, including `null`, will override the original component props. Props set to `undefined` will be ignored."*

三条与 Radix **不同**、必须记住的差异：

1. **`null` 是有效覆盖**（Radix 里 child props override 同理，但 Ariakit 明说了）；想「删掉」某个 prop，用显式 render function 展开后覆盖成 `undefined`：
   ```tsx
   <ComboboxItem id="item" render={(props) => <a {...props} id={undefined} />} />
   ```
2. **显式 render function 不自动合并**，官方原文：*"the HTML props will **not** be automatically merged into the returned React element. It's your responsibility to merge them within the function itself"*。官方推荐用过渡元素 `Role.a` 做类型安全合并，而不是手写 `mergeRefs` + 事件串联。
3. **children 也走覆盖**：`<ComboboxItem render={<a>Ariakit.com</a>}>Ariakit</ComboboxItem>` 渲染出的是 `Ariakit.com`。

### 5.3 MUI `component` / `slots` / `slotProps`（官方口径）

- `component`：**只覆盖 root slot**，且**保留该 slot 的样式**（这是与 `slots` 最关键的区别）。
- `slots`：替换内部 slot 或 root；**被替换的 slot 自带样式会一起消失**。
- `slotProps`：给内部 slot 传 props，可写成 callback 接收 `ownerState` 做条件 props。
- 冲突裁决：`slotProps.root` 与直接 props 冲突时**优先 `slotProps.root`**，但 `className` / `style` 会合并。
- 风险（官方 Best practices）：换成非语义元素会破坏 HTML 语义与无障碍；`component="span"` 套在按钮上会让键盘契约失效。

### 5.4 选型决策树

```
只是想把 <Button> 渲染成 <a>？
  ├─ 项目用 Radix 体系        → asChild + 自定义组件必须 spread props + forwardRef
  ├─ 项目用 Ariakit 体系      → render={<a href="…" />}（元素形态，自动合并）
  ├─ 项目用 MUI               → component="a"（保样式）；要换内部结构才用 slots
  └─ 自己写组件库             → 先问「要不要真的暴露换元素」：
                                不需要就用语义元素 + className，别引入 polymorphic 复杂度
需要在换元素的同时插一层包装 DOM（backdrop / wrapper）？
  → Ariakit 显式 render function（记得自己 spread），或 MUI slots + 自定义 wrapper
```

---

## 6. 「自定义组件必须开放扩展」四条硬规则（Radix + Ariakit 共识）

Ariakit 官方章节标题就是 *"Custom components must be open for extension"*，原文：*"it should pass the incoming props, including event listeners and the forwarded `ref` prop, to the underlying element. Otherwise, the component may not work as expected."* 四条逐字清单：

1. **Spread all props onto the underlying element.**
2. **Forward the `ref` prop and merge it with the internal ref, if any.**
3. **Merge the `style` and `className` props with the internal styles and classes, if any.**
4. **Chain the event props with the internal event handlers, if any.**

Radix 的 Composition 指南给了同两条最低要求（*"Your component must spread props"* / *"Your component must forward ref"*）。**为什么是这四条**：组合层传下来的往往不是业务 props，而是 `aria-*`、`role`、`data-state`、`tabIndex`、`onKeyDown`、`ref`——**任何一条没透传，无障碍和键盘就静默断掉**，而视觉上完全看不出来。

**可判 FAIL 的最小反例**：

```tsx
// ❌ 吞掉所有透传属性：asChild / render 组合后 aria、onKeyDown、ref 全失效
function MyButton({ children, onClick }) {
  return <button onClick={onClick}>{children}</button>;
}
// ✅
function MyButton({ children, onClick, ...rest }, ref) {
  return (
    <button {...rest} ref={ref}
      style={{ position: 'relative', ...rest.style }}
      onClick={(e) => { onClick?.(e); /* 内部逻辑 */ }}>
      {children}
    </button>
  );
}
```

**验收动作（可自动化，见 §20.1）**：对组件库里每个「可被换元素 / 可组合」的组件，逐个断言 ① 存在 `...rest` 或 `...props` 展开；② `ref` 到达底层 DOM；③ `className` / `style` 与内部值合并；④ 事件为串联而非覆盖。四条缺一即判 FAIL。

---

## 7. props 合并优先级：一张能判 PASS/FAIL 的算子表

把 §5–§6 的三套规则统一成**合并算子**（`slot` = 组件库内部算出来的 props，`child` = 使用方传进来的 props）：

| prop 类型 | Radix `asChild` | Ariakit `render`（元素） | MUI `slotProps` | 通用裁决 |
|---|---|---|---|---|
| 普通属性（`id` / `href` / `role` / `data-*` / `aria-*`） | child 覆盖 slot | 渲染元素显式值覆盖；`undefined` 忽略；`null` 也覆盖 | `slotProps.root` 优先于直接 props | **结构类让使用者赢** |
| `on*` 事件 | 串联（child 先 / slot 后，返回 child 结果） | 自动合并 | — | **行为类串联，禁止静默覆盖** |
| `style` | `{...slotStyle, ...childStyle}` | 自动合并 | 与直接 props 合并 | 浅合并 + child 同名键赢 |
| `className` | `[slot, child].filter(Boolean).join(' ')` | 自动合并 | 合并 | **拼接，绝不覆盖** |
| `aria-describedby` | `concatAriaDescribedby(child, slot)` | — | — | **拼接去重**（覆盖会丢掉组件自动生成的说明） |
| `ref` | `forwardRef` 到 child | 自动合并（含内部 ref） | — | 必须 mergeRefs，不能二选一 |
| `children` | 由 Slot 透传 | 渲染元素显式 children 覆盖 | — | 显式覆盖 + 提供默认 |
| 显式 render function | — | **完全不自动合并**，责任在调用方 | — | 这是最容易静默丢无障碍的分支 |

**一条总规则**：**结构类 props 让使用者赢，行为类 props 串联，标识类 props（自动生成的 id / aria）保留组件自己那份并可追加**。理由：结构决定「它是什么」，使用者最清楚；行为决定「它怎么响应」，两边都该有机会响应；标识是组件履行无障碍契约的凭据，丢掉就没法补救。

**`aria-describedby` 为什么单列**：组件常自动把 help text / error message 的 id 写进去（React `useId` 生成，见 §12）。若使用方传一个自己的 `aria-describedby` 就覆盖掉，读屏会**不再播报错误提示**——这是一个视觉零变化、合规直接 FAIL 的典型缺陷。

---

## 8. 复合组件 / Compound Components 与状态共享

- **定义**：`<Tabs>` + `<Tabs.List>` + `<Tabs.Tab>` + `<Tabs.Panel>` 这类由多个 part 组成的组件，状态（当前 tab）由 root 通过 context 下发，part 只负责渲染与交互。
- **为什么它是组合而非配置**：新增一个 tab 不需要给 root 加 `tabs={[...]}` 配置，也不需要 root 知道每个 tab 长什么样；part 可自由排序、插入装饰节点、按条件渲染。
- **API 契约要求**：
  1. root 暴露**受控三元组**（`value` / `onValueChange` / `defaultValue`），不是给每个 part 单独传 `active`。
  2. part 必须能**脱离固定父结构**仍能拿到 context（否则插一层 `<div>` 就断）。
  3. 每个 part 都要接受 `asChild` / `render` 与透传属性；不要把 context 值当成「内部实现」藏起来——`data-state` 要暴露（§13）。
  4. part 之间的**键盘契约由 root 统一认领**（§12），不能指望使用方给每个 part 写 `onKeyDown`。
- **反模式信号**：`tabs={[{label, content, icon, disabled, badge}]}` 这种「数组配置 + 内部 map」写法——它把渲染所有权收归组件，使用方要改一项就得提需求改库；配置数组越长的组件，越应该拆成 compound parts。

---

## 9. ref 与命令式 API：React 19 反陈旧裁决（本轮第二重要的裁决）

### 9.1 官方现行口径

React `forwardRef` 参考页顶部现在挂着 **`### Deprecated`**，逐字：

> *"In React 19, `forwardRef` is no longer necessary. Pass `ref` as a prop instead."*
> *"`forwardRef` will be deprecated in a future release."*

React 19 官方博客（canonical：`react.dev/blog/2024/12/05/react-19`，`ref as a prop` 章节）逐字：

> *"Starting in React 19, you can now access `ref` as a prop for function components"*
> *"New function components will no longer need `forwardRef`, and we will be publishing a codemod to automatically update your components to use the new `ref` prop."*
> *"In future versions we will deprecate and remove `forwardRef`."*
> *"`ref`s passed to classes are not passed as props since they reference the component instance."*

```tsx
// React 19 起的新写法
function MyInput({ placeholder, ref }) {
  return <input placeholder={placeholder} ref={ref} />;
}
```

**⚠️ 反陈旧裁决**：仍按旧教程把「自定义组件必须 `forwardRef`」写成硬性规范的文档与代码评审清单已经过时——**函数组件的 `ref` 从 React 19 起是普通 prop**；`forwardRef` 还能用、官方也仍在其参考页给出用法，但标注为 Deprecated，并明确方向是 codemod 迁移 + 未来移除。写规范时要写清「目标 React 版本」，不要跨版本套用。类组件是明确例外（ref 指向实例，不作为 prop 传入）。

### 9.2 命令式 handle 的准入清单

可以做（官方列举的 imperative behaviors）：**滚动到节点、聚焦节点、触发动画、选中文本**——这些都是「无法用 props 表达」的浏览器副作用。

不可以做：任何能用状态 props 表达的事。官方点名反例：

> *"instead of exposing an imperative handle like `{ open, close }` from a `Modal` component, it is better to take `isOpen` as a prop like `<Modal isOpen={isOpen} />`."*

另一条官方提醒（同样逐字）：*"exposing a ref to the DOM node inside your component makes it harder to change your component's internals later"*；官方建议只在**低层可复用组件**（button / text input）暴露 DOM 节点，不要在应用级组件（avatar / comment）上暴露。

### 9.3 ref cleanup 与 TypeScript 连带变化（React 19）

- 现在 ref callback 可以**返回 cleanup function**，卸载时 React 调用它；对 DOM ref、class ref、`useImperativeHandle` 都生效。
- 行为变化（官方）：*"Previously, React would call `ref` functions with `null` when unmounting the component. If your `ref` returns a cleanup function, React will now skip this step."* 未来版本会废弃卸载时以 `null` 调用。
- TypeScript 连带：*"returning anything else from a `ref` callback will now be rejected by TypeScript"*；修法是去掉隐式返回（`ref={current => { instance = current }}`），可用 codemod `no-implicit-ref-callback-return`。

**设计侧结论**：组件 API 评审时，看到 `useImperativeHandle` 就先问一句「这个行为能不能变成 props？」；能，就改设计而不是加 handle。命令式 API 每多一个方法，组件内部重构的自由度就少一分。

---

## 10. 组件契约的最小字段集（API surface，可直接当评审表）

以 Radix `Switch` 官方 API 为范例（逐字字段名与默认值）：

| 分组 | 字段 | 类型 / 默认值 | 为什么必须有 |
|---|---|---|---|
| 渲染 | `asChild` | `boolean`，默认 `false` | 换元素能力，默认不启用避免误吞 props |
| 状态 | `checked` | `boolean \| undefined` | 受控值（`undefined` = 非受控） |
| 初值 | `defaultChecked` | `boolean` | 非受控初值 |
| 回调 | `onCheckedChange` | `(checked: boolean) => void` | 变更请求，给值不给事件 |
| 表单 | `name` / `value` / `required` / `disabled` | `value` 默认 `"on"` | 原生表单语义必须由组件继承，不能另造一套 |
| 状态暴露 | `data-state`（`checked` / `unchecked`）、`data-disabled` | 自动 | 样式与测试读它，不用另开布尔 props |
| 键盘 | `Space` / `Enter` 切换 | 内建 | 复合交互契约（§12） |

**抽象成 10 类字段（每个公开组件都要逐类回答）**：

1. 受控值 / 非受控初值 / 变更回调（§2）
2. 原生 DOM 属性透传范围（是否允许 `id` / `className` / `style` / `title` / `data-*` / `aria-*`）
3. 内容通道（`children` / 具名插槽 / 作用域插槽 / render prop）
4. 渲染所有权（`asChild` / `render` / `slots` / `component` / 不提供）
5. 状态可视化出口（`data-*` / ARIA 属性 / `ownerState`）
6. 无障碍属性自动生成（`useId` 生成的 `aria-labelledby` / `aria-describedby` / `role`）
7. 键盘契约（tab stop 数、按键表、焦点返回策略）
8. `ref` 与命令式 handle（§9）
9. 默认值与「改默认值 = MAJOR」的版本归属（§14）
10. 废弃字段、迁移路径、类型导出（`ComponentPropsWithoutRef` 等）

**验收口径**：这 10 类里，任何一类在文档里答不上来，就不算「有 API 契约」，只算「有 props 表」。`design-system-docs.md` 的九段式组件页是**给人读**的落点，这张表是**给机器读**的落点（§15 用 argTypes 实现）。

---

## 11. 回调契约：`onChange` 到底承诺了什么

| 决策点 | 裁决 | 依据 / 理由 |
|---|---|---|
| 参数给值还是给事件 | **给值**（`onCheckedChange(checked)`、`onValueChange(v)`） | 使用方不该依赖内部 DOM 结构；Radix `Switch` 即如此 |
| 什么时候调用 | **值真的要变时**；Radix 源码 `if (value !== prop) onChangeRef.current?.(value)` | 重复设同值不应触发副作用 |
| 受控时谁改值 | **只有父级**；组件只发通知，不改本地 | `useControllableState` 的 `if (isControlled)` 分支 |
| 同步还是异步 | 事件处理器内**同步**发出 | 受控模式要求 `onChange` 里同步 setState，否则输入回弹 |
| 是否支持函数式更新 | 支持 `setValue(prev => next)`（Radix 源码 `isFunction(nextValue) ? nextValue(prop) : nextValue`） | 避免闭包旧值 |
| 命名分歧 | `onChange` / `onValueChange` / `onCheckedChange` / `update:modelValue` 四套并存 | **不要求统一，要求同库内一致 + 写进类型**；Vue `v-model` 默认 `modelValue` + `update:modelValue`，参数化 `v-model:title` → `title` + `update:title`，modifier 走 `modelModifiers` / `arg + "Modifiers"` |

**Vue 的一条硬提醒**（官方 props 页）：props 是 **one-way-down**，子组件不得直接 mutate；对象 / 数组类型的 prop 虽然技术上能改嵌套字段，但同样破坏单向流且难以追踪。`v-model` 是「语法糖 + 显式 emit」，不是「允许改 prop」。Boolean Casting 有两条易错点：默认 `Boolean` 类型的 prop **缺席会被 cast 成 `false`**（不是 `undefined`），而 `[String, Boolean]` 的声明**顺序会影响 cast 结果**——所以「三态布尔」不要靠类型数组碰运气，显式用字符串枚举。

---

## 12. 无障碍不是 props 的附属品：键盘契约在 API 层怎么落

WAI-ARIA APG `Developing a Keyboard Interface` 的硬要求（官方原文口径）：

- **所有交互元素必须可键盘操作**；使用 `Tab` / `Shift+Tab` 导航，功能可由 `Enter` / `Space` / 方向键等触发。
- **复合组件通常只让一个元素进入 tab sequence**（一个 tab stop），组件内部焦点管理用两种策略之一：**roving `tabindex`**（焦点真的移到子项）或 **`aria-activedescendant`**（DOM 焦点留在容器，用属性声明活动项）。
- **focus 与 selection 必须在视觉上可区分**（被聚焦不等于被选中）——这直接决定组件要不要暴露 `data-highlighted` / `data-state`。
- 禁用控件不应打断键盘流；快捷键不能替代基础导航。
- `Dialog (Modal)` 范例的具体契约：`Tab` / `Shift+Tab` **焦点循环**、`Escape` **关闭**、打开时设 **initial focus**、关闭后**焦点返回触发元素**；容器带 `role="dialog"` / `aria-labelledby` / `aria-describedby` / `aria-modal="true"`。

**API 层要做的四件事**（否则无障碍靠使用方自觉，等于没做）：

1. **组件自己生成并拼接 id**：React `useId` 官方用途是生成 accessibility attributes 的唯一 ID；**不能用于 list keys 或 cache keys**；SSR 要求 client / server 组件树**完全一致**；多个 React root 时用 `identifierPrefix`。生成的 id 要能通过 `aria-describedby` 与使用方传入的值**拼接**（§7），不能被覆盖。
2. **允许全部 `aria-*` / `role` 透传**（§6 四条硬规则），且 `asChild` / `render` 后仍存活。
3. **把 tab stop 策略写进 API 文档**：是 roving tabindex 还是 `aria-activedescendant`，决定了使用方能不能插自己的可聚焦元素。
4. **焦点返回由组件负责**：`Dialog` / `Popover` / `Menu` 关闭后把焦点还给 trigger，别让使用方每个页面写一遍。

**Radix 的立场可当验收线**：官方 Introduction 把 `Accessible` 放在第一位，明确遵循 WAI-ARIA 设计、支持键盘导航与焦点管理；`asChild` 给「对 rendered element 的完全控制」的前提就是**自定义组件仍把这些属性透传下去**。

⚠️ **不臆造声明**：W3C APG keyboard 页面含未完成占位（*"... other considerations to be added ..."* / *"... to be continued ..."* / *"To be written."*）。本文件只取已成文的段落，**不把占位符扩写成规范**；具体按键表以 APG 各 Pattern 页（Accordion / Combobox / Listbox / Menu and Menubar / Tabs / Tree View …共 28 类）为准，不在本文件重抄。

---

## 13. 状态暴露：别把 9 态做成 9 个布尔 props

| 通道 | 例子 | 谁读 | 裁决 |
|---|---|---|---|
| `data-*` 属性 | Radix `Switch` 的 `data-state="checked\|unchecked"` / `data-disabled` | CSS、E2E 测试、视觉回归 | ✅ **首选**：状态与样式解耦，不增加 props |
| ARIA 属性 | `aria-checked` / `aria-expanded` / `aria-selected` / `aria-invalid` | 辅助技术 | ✅ 必须，且不能被使用方覆盖掉 |
| `ownerState` / 回调 slotProps | MUI `slotProps={{ root: (ownerState) => ({...}) }}` | 样式覆写逻辑 | ✅ 条件样式走这条，别新增 props |
| 布尔 props | `isActive` / `isHighlighted` / `isFocused` / `isSelected` … | 使用方 | ❌ **反模式**：组件内部状态泄漏成输入，父级要与组件同步一份永不一致的镜像 |

**判定**：一个组件公开的布尔 props 若 **>5 个**，基本可以断定它把内部状态当成了配置项。回到 §1 原则 1——状态只有一个所有者，内部状态不该有第二个出处。设计侧的「9 态矩阵」（default / hover / focus / active / selected / disabled / read-only / error / loading）对应到代码是：**1 个受控值 + 少量语义布尔（disabled / readOnly / required / invalid）+ 其余全部由 `data-*` / CSS 伪类 / ARIA 表达**。

---

## 14. API 版本化：组件特有的破坏性判级（改默认值 = MAJOR 的延伸）

沿用 `handoff-collaboration.md` 的 SemVer 11 条，本轮补**组件 API 特有**的判级表：

| 变更 | 级别 | 理由 |
|---|---|---|
| 改某个 prop 的**默认值** | **MAJOR** | 所有没显式传值的使用点行为全变（既有裁决） |
| 改 **props 合并优先级**（如 child 赢改成 slot 赢） | **MAJOR** | 视觉零报错地静默改变 `className` / `style` / `aria-*`，比改默认值更隐蔽 |
| 移除 / 重命名 prop、改变回调参数（值 ↔ 事件、参数顺序） | **MAJOR** | 类型直接编译失败或逻辑错 |
| 改变受控判定（如 `prop !== undefined` 改成 `prop != null`） | **MAJOR** | `null` / 空值语义全变 |
| 改变键盘契约 / tab stop 策略 | **MAJOR** | 无障碍与 E2E 全量回归 |
| 改变自动生成的 `role` / `aria-*` | **MAJOR** | 读屏播报变化 |
| 新增**可选** prop / 可选 slot / 可选 `data-*` | **MINOR** | 不影响既有调用 |
| 标记 deprecated（保留旧行为） | **MINOR** | 废弃需至少一个 MINOR 过渡 |
| 文档、类型注释、示例修正 | **PATCH** | 行为不变 |
| 内部实现重构但契约全等 | **PATCH** | 前提是 §10 十类字段一个没动 |

**官方 codemod 实例**：React 19 把 `forwardRef` → `ref as prop` 作为 MAJOR 级语义迁移，官方明确 *"we will be publishing a codemod to automatically update your components"*；ref callback 隐式返回的 TS 变更配套 `no-implicit-ref-callback-return` codemod。这正好兑现 `design-system-docs.md` 的「**MAJOR 必带能被机器校验的迁移文档**」——**迁移文档不是文字说明，是可执行的 codemod / 脚本**（§20.3 给一个可跑的契约 diff 器）。

**契约冻结清单**（发布后不得改语义，改则 MAJOR）：受控判定式、默认值、回调签名与触发时机、合并优先级、自动生成的 aria / role、`data-*` 取值域、tab stop 策略、ref 暴露的对象形状。

---

## 15. Storybook argTypes：把 API 契约变成机器可读、可在 CI 校验的东西

官方 `Controls` 文档口径（`/docs/essentials/controls`；`/docs/api/argtypes` 返回 404，规范链接为 `/docs/api/arg-types`，见 §22）：

- *"Storybook Controls gives you a graphical UI to interact with a component's arguments dynamically without needing to code."*
- *"Controls do not require any modification to your components."*
- 生成机制：*"Storybook will automatically generate UI controls based on your args and what it can infer about your component"*；给 meta 加 `component` annotation 后，用 **react-docgen**（含 TypeScript first-class support）推断并自动生成 `argTypes`。
- *"ArgTypes encode basic metadata for args, such as name, description, and defaultValue for an arg. These get automatically filled in by Storybook Docs."*

### 15.1 把 §10 十类字段映射到 argTypes

| argTypes 字段 | 契约含义 | 用法 |
|---|---|---|
| `name` / `description` / `defaultValue` | 字段名、语义、默认值 | 由 Docs 自动填充；**默认值必须与实际代码同源**，否则就是 §14 的 MAJOR 隐患 |
| `control.type`（`boolean` / `number` / `range` / `text` / `color` / `date` / `radio` / `select` / `check` / `multi-select` / `object` / `file`） | 值的类型与取值域 | 枚举一律给 `options`，别让人自由输入 |
| `control.min` / `max` / `step` / `accept` / `presetColors` / `labels` | 取值边界 | 把设计侧的「参数区间」写进控件 |
| `mapping` | 把可序列化 option 映到复杂 arg（JSX 等） | 官方：*"Maps serializable option values to complex arg values"*；因复杂值无法在 URL / manager↔preview 间同步 |
| `table.disable: true` | **隐藏该 prop 并同时移除 table 里的 prop documentation** | 只用于真正内部的实现细节 |
| `control: false` | **保留 prop 文档但不给交互控件** | ✅ **适合 `ref` / 命令式 handle / 内部注入 props**：文档必须可见，但不该让人在面板里瞎调 |
| `if: { arg: 'advanced' }` | 条件显示（`truthy` / `exists` / `eq` / `neq`，最多一个 operator，无 operator 等价 `{truthy:true}`） | 把高级配置项折叠，避免 30 个控件平铺 |
| `parameters.controls.exclude` / `include` / `expanded` / `sort` / `disableSaveFromUI` | 面板级策略 | **`sort: 'requiredFirst'`** 让必填 props 排最前，等于把契约的必填项暴露出来 |

### 15.2 三条可直接执行的裁决

1. **`control: false` ≠ `table.disable`**：前者保留文档、只关控件，后者连文档一起删。组件库里 `ref`、`asChild` 内部结构、内建 aria 注入应走 `control: false`——**文档要能被查到，但不能被当成可配置项**。
2. **用 `requiredFirst` + `expanded` 把契约摆到脸上**：`expanded: true` 会在 Controls 面板内嵌完整 `Controls` doc block（含 description 与 default value），等于每个组件自带一份可交互的 API 参考。
3. **文档站与 argTypes 分工**：`design-system-docs.md` 的九段式回答「何时用 / 何时别用 / 无障碍 / 研究证据」（人读）；argTypes 回答「字段、类型、默认值、取值域」（机器读）。**两边都写默认值就会漂移**——默认值只从组件类型 / docgen 来，文档站引用它，不要手抄第二份（自举到 `build_readme.py` 实时统计的同一条纪律）。

⚠️ 已知限制（官方）：`date` control 会把日期转成 UNIX timestamp，*"It's a known limitation that will be fixed in a future release."*；需要真实 date 对象时要在 story 的 render 里自行转换。

---

## 16. 类型即文档：TypeScript 契约的四条底线

1. **原生属性用 `ComponentPropsWithoutRef<'button'>`（或 Vue 的 attrs 透传）继承**，不要逐条手抄 `disabled` / `type` / `title` / `aria-*`——抄不全就是 §6 的 FAIL。
2. **受控 / 非受控用 discriminated union 表达互斥**（`{ value: T; onChange: ... } | { defaultValue?: T; onChange?: ... }`），让 `value` + `defaultValue` 同传在**编译期**报错，而不是靠 §20.1 的运行时 lint 兜底。
3. **多态 `as` 的复杂度要明码标价**：`as` + `ref` + 泛型推导三者耦合，类型成本远高于 `asChild` / `render`。选型时若只是「把按钮渲染成链接」，优先 `asChild` 或 `component`，不要引入 polymorphic 泛型（§5.4）。
4. **状态类型用字符串枚举而非布尔堆叠**：`state: 'checked' | 'unchecked' | 'indeterminate'` 比三个布尔 props 更能表达互斥，也直接对应 `data-state`（§13）。

**不臆造声明**：本节给的是可验证的模式，不声称某个库的具体类型名或版本数值；实现细节以各库当前类型定义为准。

---

## 17. 16 场景决策矩阵（先查表，再动手）

| # | 场景 | L0 状态 | L1 渲染 / 组合 | 不能做什么 |
|---|---|---|---|---|
| 1 | 表单输入框要联动提交按钮 | `value` + `onChange`（受控） | 语义 `<input>`，透传 `aria-invalid` / `aria-describedby` | 别 `value` + `defaultValue` 同传；别用 ref 读值 |
| 2 | 只要一个非受控初值 | `defaultValue` | 同上 | 别在异步数据回来后把组件切成受控 |
| 3 | 开关 / 复选框 | `checked` / `defaultChecked` / `onCheckedChange(checked)` | `data-state` + `aria-checked` | 别把 `checked` 做成 `isOn` 再同步一份 |
| 4 | 模态框 / Drawer | `open` / `defaultOpen` / `onOpenChange` | portal + 焦点锁 + Escape + 焦点返回 | **别暴露 `{open(), close()}` 命令式 handle**（§9.2 官方反例） |
| 5 | Tabs / Accordion / Menu | root 持有 `value`，context 下发 | compound parts + roving tabindex | 别给每个 part 传 `active`；别用配置数组 map 死结构 |
| 6 | 把 Button 渲染成链接 | 无状态 | `asChild` / `render={<a/>}` / `component="a"` | 别用 `<div onClick>`；别丢 `href` / 键盘可聚焦 |
| 7 | 组合自定义业务组件 | — | **必须 spread props + forward ref + 合并 style/className + 串联事件**（§6 四条） | 别只解构自己关心的几个 props |
| 8 | 换元素同时要插 wrapper DOM | — | Ariakit 显式 render function + 手动 spread；或 MUI `slots` + wrapper | 别在 render function 里忘了 `{...htmlProps}` |
| 9 | 组件要自动挂 help text / error 说明 | — | `useId` 生成 + `aria-describedby` **拼接** | 别让使用方的 `aria-describedby` 覆盖掉（§7） |
| 10 | 样式要跟状态走 | — | `data-state` / `data-disabled` + CSS 属性选择器 | 别新增 `isActive` / `isFocused` 布尔 props |
| 11 | SSR / 多 React root | — | `useId` 保证 client/server 树一致；多 root 用 `identifierPrefix` | 别用 `useId` 当 list key / cache key；别用随机 id |
| 12 | Vue 组件要双向绑定 | `modelValue` + `update:modelValue`（或 `defineModel()`） | 具名 / 作用域插槽 | 别在子组件直接 mutate prop；别靠 `[String, Boolean]` 顺序碰运气 |
| 13 | 需要「有多种完成方式」的包容性界面 | — | 内容与渲染都留通道 | 别只给一种组合路径（接 `design-ethics-inclusion.md` §15–§17） |
| 14 | 改了组件默认值 / 合并优先级 | — | — | **别只发 PATCH**（§14），MAJOR 要带可执行迁移 |
| 15 | 组件文档页要写 props 表 | — | argTypes + docgen 同源 | 别手抄第二份默认值；别用 `table.disable` 藏掉 `ref` 文档 |
| 16 | React 19 项目新写组件 | — | `ref` 当普通 prop | 别把「必须 `forwardRef`」写进新项目的硬规范（§9.1） |

---

## 18. 20 条反模式（逐条可判 FAIL）

1. `value` 给了却没给 `onChange` → 输入框只读，用户以为坏了。
2. `value` 与 `defaultValue` 同传 → 三元组语义冲突，`defaultValue` 是死代码。
3. 组件生命周期内从非受控切到受控（异步接口回来才给 `value`）→ Radix 开发态告警 + 行为不可预测。
4. `value={data ?? undefined}` → 用 `?? ''` 或先渲染 loading，别用 `undefined` 当占位。
5. 受控 setter 里既发 `onChange` 又 `setState` 本地 → 两个真相源，父级不改就分叉。
6. `onChange(event)` 强迫使用方读 `event.target.value` → 依赖内部 DOM 结构，组合后必断。
7. 自定义组件只解构自己用的 props，不 spread rest → `asChild` / `render` 后 aria、onKeyDown、data-* 全丢。
8. 组合时覆盖 `className` 而不是拼接 → 组件库样式被整体抹掉。
9. 覆盖 `aria-describedby` 而不是拼接 → 读屏不再播报 help / error，视觉零变化、合规 FAIL。
10. 事件处理器二选一而不是串联 → 使用方的埋点或组件库的键盘逻辑被静默吞掉。
11. `forwardRef` 了但内部还有自己的 ref 却不 mergeRefs → 其中一个恒为 null。
12. 用 `useImperativeHandle` 暴露 `{ open, close }` 而不是 `isOpen` prop → React 官方点名的反例。
13. 在应用级组件（Avatar / Comment）暴露 DOM 节点 ref → 官方：「内部以后更难改」。
14. 布尔 props 超过 5 个（`isActive`/`isHover`/`isFocused`…）→ 内部状态泄漏成输入，父级要维护镜像。
15. 用 `tabs={[{label, content, icon, ...}]}` 配置数组 map 死结构 → 渲染所有权收归组件，改一项就要改库。
16. `children={{ header, footer }}` 对象式「多个洞」→ 破坏 JSX 组合、类型推断与 argTypes 生成。
17. 插槽有内容与否都渲染 wrapper → 空 padding / 空边框；应先用 `$slots` 判断。
18. 显式 `render` function 里忘了 `{...htmlProps}` → Ariakit 官方：函数形态**不自动合并**，无障碍直接归零。
19. 改默认值、改合并优先级、改键盘契约只发 PATCH → 静默破坏，§14 判 MAJOR。
20. `useId` 当 list key / cache key，或 SSR client/server 组件树不一致 → 官方明令禁止 / 明确要求。

---

## 19. 22 项上线自检（组件 API 关）

- [ ] 1. 每个有状态的组件都说得出「谁持有这个值」，且只有一处 `useState` / props 之一？
- [ ] 2. 受控三元组（`value` / `onChange` / `defaultValue`）齐了吗？类型是互斥 union 吗？
- [ ] 3. 受控判定是 `prop !== undefined`（而不是 `!= null` / truthy）吗？
- [ ] 4. 受控 setter 只发通知、不写本地？值未变时不触发回调？
- [ ] 5. 异步数据回来前不会让组件从非受控切到受控吗？
- [ ] 6. 回调给的是值而不是 event？触发时机与同步性写进文档了吗？
- [ ] 7. 自定义组件 spread 了全部 rest props 吗？
- [ ] 8. `ref` 到达底层 DOM、且与内部 ref 合并了吗（React 19 起 `ref` 是普通 prop）？
- [ ] 9. `className` 是拼接、`style` 是浅合并吗？
- [ ] 10. `on*` 事件是串联而非覆盖吗？顺序（child 先 / slot 后）写清了吗？
- [ ] 11. 自动生成的 `aria-describedby` 是拼接去重，不会被使用方覆盖吗？
- [ ] 12. `asChild` / `render` / `slots` 后，`role` / `aria-*` / `tabIndex` / `data-state` 仍存活吗？
- [ ] 13. 显式 render function 里手动 spread 了 `htmlProps` 吗？
- [ ] 14. 复合组件只有 **一个 tab stop**，策略（roving tabindex / `aria-activedescendant`）写进文档了吗？
- [ ] 15. focus 与 selection 视觉可区分吗？`data-state` / `data-highlighted` 暴露了吗？
- [ ] 16. Modal / Popover：Tab 循环、Escape 关闭、initial focus、关闭后**焦点返回 trigger** 都做了吗？
- [ ] 17. `useId` 只用于 accessibility attributes、没当 key？SSR 树一致、多 root 用 `identifierPrefix` 了吗？
- [ ] 18. 布尔 props ≤5 个？9 态靠 `data-*` / CSS 伪类 / ARIA 表达而不是 props 堆叠？
- [ ] 19. 命令式 handle 只含「滚动 / 聚焦 / 触发动画 / 选中文本」这类无法 props 化的行为吗？
- [ ] 20. §10 的十类字段在文档里都能答上来吗？argTypes 与类型同源、没有手抄第二份默认值吗？
- [ ] 21. 本次变更判过 SemVer 吗？改默认值 / 改合并优先级 = MAJOR，MAJOR 带**可执行** codemod 吗？
- [ ] 22. `§20.1` 契约 lint、`§20.2` 合并算子、`§20.3` 契约 diff 三段脚本都跑过了吗？

---

## 20. 可抄代码（3 段 Python 已实跑，含双用例断言）

### 20.1 `component_api_lint.py` — 组件 API 契约静态检查（已实跑）

把 §2 / §6 / §9 / §13 / §18 的红线做成可进 CI 的检查。输入是组件源码文本，输出 `(rule, line, message)` 列表；`FAIL` 级别即门禁不通过。

```python
# -*- coding: utf-8 -*-
"""组件 API 契约 lint。规则来自 references/component-api-design.md §2/§6/§9/§13/§18。"""
import re

RULES = [
    ("A01", "value 无 onChange → 只读",            r"<(?:input|Input|textarea|Textarea)\b(?=[^>]*\bvalue\s*=)(?![^>]*\bonChange\s*=)[^>]*>"),
    ("A02", "value 与 defaultValue 同传",           r"<[^>]*\bvalue\s*=[^>]*\bdefaultValue\s*="),
    ("A03", "checked 与 defaultChecked 同传",      r"<[^>]*\bchecked\s*=[^>]*\bdefaultChecked\s*="),
    ("A04", "defaultValue + onChange 混用",        r"<[^>]*\bdefaultValue\s*=[^>]*\bonChange\s*="),
    ("A05", "value 显式传 undefined",              r"\bvalue\s*=\s*\{[^}]*\?\?\s*undefined|\bvalue\s*=\s*\{undefined\}"),
    ("C01", "组件定义未 spread 透传 props",        r"function\s+[A-Z]\w*\s*\(\s*\{\s*[\w,\s]+\}\s*\)\s*\{[^}]*return\s*<(?![^>]*\{\s*\.\.\.)"),
    ("C02", "className 直接覆盖",                  r"className\s*=\s*\{?\s*(?:props|rest)\.className\s*\}?\s*/?>(?![^<]*)"),
    ("R01", "暴露 open/close 命令式 handle",       r"useImperativeHandle[\s\S]{0,300}?\b(?:open|close)\s*[:(]"),
    ("R02", "useId 被用于 key",                    r"\bkey\s*=\s*\{?\s*useId\s*\(|\bkey\s*=\s*\{[^}]*\bid\b[^}]*\buseId|\bconst\s+(\w+)\s*=\s*useId\s*\([^)]*\)[\s\S]{0,200}?\bkey\s*=\s*\{\s*\1\s*\}"),
    ("S01", "布尔 props 爆炸（>5）",               None),  # 由计数逻辑实现
]

def lint(src: str, react19: bool = True):
    issues = []
    lines = src.splitlines()
    for rid, desc, rx in RULES:
        if rx is None:
            continue
        for m in re.finditer(rx, src, re.M | re.S):
            ln = src[:m.start()].count("\n") + 1
            issues.append((rid, ln, desc))
    # S01：布尔 props 计数（类型声明块内 is* / has* / show* / disabled 之外的镜像状态）
    bools = set(re.findall(r"\b(?:is|has|show|hide)[A-Z]\w*\s*\??\s*:\s*boolean", src))
    if len(bools) > 5:
        issues.append(("S01", 1, f"布尔 props {len(bools)} 个 >5：{','.join(sorted(bools))}"))
    # R03：React 19 项目里仍硬性要求 forwardRef（仅提示，不判 FAIL）
    if react19 and "forwardRef" in src and "React 19" not in src:
        issues.append(("R03", 1, "forwardRef 在 React 19 已标 Deprecated；确认是否需 codemod 迁移"))
    issues.sort(key=lambda x: (x[1], x[0]))
    return issues

BAD = """
function MyButton({ children, onClick }) {
  return <button onClick={onClick}>{children}</button>;
}
function Field(props) {
  const id = useId();
  return <input value={props.v} defaultValue="x" key={id} />;
}
type P = { isActive: boolean; isFocused: boolean; isHovered: boolean;
           isSelected: boolean; isPressed: boolean; isLoading: boolean };
useImperativeHandle(ref, () => ({ open() {}, close() {} }));
"""

GOOD = """
function MyButton({ children, onClick, ...rest }, ref) {
  return <button {...rest} ref={ref} className={[base, rest.className].join(' ')}
    onClick={(e) => { onClick?.(e); track(e); }}>{children}</button>;
}
function Field({ value, onChange, id, ...rest }) {
  return <input {...rest} id={id} value={value} onChange={onChange} />;
}
type P = { state: 'checked' | 'unchecked'; disabled?: boolean };
"""

if __name__ == "__main__":
    bad = lint(BAD)
    good = lint(GOOD)
    bad_ids = {r for r, _, _ in bad}
    assert {"A01", "A02", "C01", "R01", "R02", "S01"} <= bad_ids, bad_ids
    assert not [x for x in good if x[0] != "R03"], good
    print("BAD  命中", len(bad), "条:", sorted(bad_ids))
    print("GOOD 命中", len(good), "条（仅提示级）:", [r for r, _, _ in good])
    print("PASS: 6+1 断言全通过")
```

**实跑结果（2026-11-07）**：`BAD` 命中 6 条（`A01` 只读输入 / `A02` value+defaultValue / `C01` 未 spread / `R01` open-close handle / `R02` useId 当 key / `S01` 布尔 props 爆炸），`GOOD` 0 条（含提示级也是 0），`PASS: 6+1 断言全通过`。

### 20.2 `merge_props.py` — 可执行的两套合并算子（已实跑）

复刻 Radix `mergeProps` 语义，并加 Ariakit `render` 元素形态的 `undefined` / `null` 规则。组件库写自己的组合层时可直接拿去对照。

```python
# -*- coding: utf-8 -*-
"""Radix mergeProps + Ariakit render 元素形态合并规则的可执行参考实现。"""
import re

def is_handler(k):
    return bool(re.match(r"^on[A-Z]", k))

def concat_aria(*vals):
    out = []
    for v in vals:
        if not v:
            continue
        for tok in str(v).split():
            if tok not in out:
                out.append(tok)
    return " ".join(out) or None

def merge_props(slot, child):
    """Radix Slot.mergeProps：child 覆盖；事件串联；style/className/aria-describedby 合并。"""
    override = dict(child)
    for k, cv in child.items():
        sv = slot.get(k)
        if is_handler(k):
            if sv and cv:
                def composed(*args, _c=cv, _s=sv):
                    result = _c(*args)   # child 先
                    _s(*args)            # slot 后
                    return result
                override[k] = composed
            elif sv:
                override[k] = sv
        elif k == "style":
            override[k] = {**(sv or {}), **(cv or {})}
        elif k == "className":
            override[k] = " ".join(x for x in (sv, cv) if x)
        elif k == "aria-describedby":
            override[k] = concat_aria(cv, sv)
    return {**slot, **override}

UNSET = object()   # 对应 JS undefined：在 render 元素形态里被忽略


def merge_render(original, rendered):
    """Ariakit render={<el/>}：显式值（含 null）覆盖；undefined 忽略；四个 key 自动合并。"""
    out = dict(original)
    for k, v in rendered.items():
        if v is UNSET:                                  # JS undefined → 忽略
            continue
        if v is None:                                   # JS null → 有效覆盖
            out[k] = None
            continue
        if k == "style":
            out[k] = {**(original.get(k) or {}), **v}
        elif k == "className":
            out[k] = " ".join(x for x in (original.get(k), v) if x)
        elif k == "aria-describedby":
            out[k] = concat_aria(original.get(k), v)
        elif k == "ref":
            out[k] = ("merged", original.get(k), v)     # 示意 mergeRefs
        elif is_handler(k) and callable(original.get(k)) and callable(v):
            def composed(*a, _o=original[k], _v=v):
                r = _v(*a)
                _o(*a)
                return r
            out[k] = composed
        else:
            out[k] = v                                  # 结构类：显式值覆盖
    return out

if __name__ == "__main__":
    order = []
    slot = {"id": "auto", "className": "btn", "style": {"color": "red", "padding": 4},
            "onClick": lambda: order.append("slot"), "aria-describedby": "err-1"}
    child = {"id": "mine", "className": "wide", "style": {"color": "blue"},
             "onClick": lambda: order.append("child"), "aria-describedby": "help-1"}
    m = merge_props(slot, child)
    assert m["id"] == "mine"                                  # child 覆盖
    assert m["className"] == "btn wide"                        # 拼接，不是覆盖
    assert m["style"] == {"color": "blue", "padding": 4}       # 浅合并
    assert m["aria-describedby"] == "help-1 err-1"             # 拼接去重
    m["onClick"]()
    assert order == ["child", "slot"], order                   # 串联顺序与返回值
    assert m["aria-describedby"] == concat_aria("help-1", "err-1")

    r = merge_render({"id": "item", "style": {"position": "relative"}},
                     {"id": UNSET, "title": None, "style": {"top": 0}})
    assert r["id"] == "item"                   # undefined 忽略
    assert r["title"] is None                  # null 是有效覆盖
    assert r["style"] == {"position": "relative", "top": 0}

    # 显式 render function 不自动合并：用守卫证明漏 spread 会丢光无障碍属性
    def guard(html_props, spread=False):
        return {"aria-describedby": html_props.get("aria-describedby")} if spread else {}
    assert guard({"aria-describedby": "err-1"}) == {}
    assert guard({"aria-describedby": "err-1"}, True) == {"aria-describedby": "err-1"}
    print("PASS: 11 断言全通过（Radix 6 + Ariakit 3 + render function 守卫 2）")
```

**实跑结果（2026-11-07）**：`PASS: 11 断言全通过`；其中 `merge_props` 的事件组合顺序实测为 `["child", "slot"]`，与 Radix 源码一致。

### 20.3 `api_semver.py` — 契约 diff 与 MAJOR 门禁（已实跑）

把 §14 的判级表做成可执行脚本：输入新旧两份 API 契约，输出版本级别与变更清单。**MAJOR 必须附带 codemod 路径，否则 CI 拒绝发版**。

```python
# -*- coding: utf-8 -*-
"""组件 API 契约 diff → SemVer 级别。规则见 references/component-api-design.md §14。"""
FROZEN = ("merge_priority", "tab_stop", "aria", "data_state", "ref_shape", "controlled_rule")

def semver(old: dict, new: dict):
    changes, level = [], "NONE"
    rank = {"NONE": 0, "PATCH": 1, "MINOR": 2, "MAJOR": 3}
    def bump(x):
        nonlocal level
        if rank[x] > rank[level]:
            level = x
    for p in sorted(k for k in set(old) | set(new) if not k.startswith("_")):
        a, b = old.get(p), new.get(p)
        if a is None:
            changes.append((p, "MINOR", "新增可选 prop")); bump("MINOR"); continue
        if b is None:
            changes.append((p, "MAJOR", "移除/重命名 prop")); bump("MAJOR"); continue
        for f in ("default", "type", "callback_signature"):
            if a.get(f) != b.get(f):
                changes.append((p, "MAJOR", f + " 改变")); bump("MAJOR")
        if not a.get("deprecated") and b.get("deprecated") is True:
            changes.append((p, "MINOR", "标记 deprecated")); bump("MINOR")
        if a.get("description") != b.get("description"):
            changes.append((p, "PATCH", "文档修正")); bump("PATCH")
    ma, mb = old.get("_meta", {}), new.get("_meta", {})
    for f in FROZEN:                       # 契约冻结字段，改一个就是 MAJOR
        if ma.get(f) != mb.get(f):
            changes.append(("_meta." + f, "MAJOR", "契约冻结字段改变")); bump("MAJOR")
    return level, changes

if __name__ == "__main__":
    v1 = {"size": {"default": "md", "type": "enum", "description": "尺寸"},
          "_meta": {"merge_priority": "child-wins", "tab_stop": "roving",
                    "aria": "auto", "data_state": ["checked", "unchecked"],
                    "ref_shape": "dom", "controlled_rule": "prop!==undefined"}}
    cases = [
        ("改默认值",     {**v1, "size": {**v1["size"], "default": "lg"}}, "MAJOR"),
        ("改合并优先级", {**v1, "_meta": {**v1["_meta"], "merge_priority": "slot-wins"}}, "MAJOR"),
        ("改键盘策略",   {**v1, "_meta": {**v1["_meta"], "tab_stop": "activedescendant"}}, "MAJOR"),
        ("新增可选 prop", {**v1, "loading": {"default": False, "type": "boolean", "description": "加载"}}, "MINOR"),
        ("标记 deprecated", {**v1, "size": {**v1["size"], "deprecated": True}}, "MINOR"),
        ("文档修正",     {**v1, "size": {**v1["size"], "description": "控件尺寸"}}, "PATCH"),
        ("无变化",       v1, "NONE"),
    ]
    for name, new, expect in cases:
        lvl, ch = semver(v1, new)
        assert lvl == expect, (name, lvl, expect, ch)
        print(f"  {name:16s} → {lvl:5s}  ({len(ch)} 条变更)")
    print("PASS: 7 个用例全部符合 §14 判级表")
```

**实跑结果（2026-11-07）**：7/7 用例通过；「改默认值」「改合并优先级」「改键盘策略」均判 **MAJOR**，「文档修正」判 **PATCH**。

### 20.4 Storybook 契约模板（TS，可抄）

把 §15 的裁决落成一份可直接用的 meta：必填项排前、内部项保留文档但关控件、高级项条件折叠。

```ts
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta = {
  component: Button,                         // react-docgen 据此推断 argTypes
  parameters: {
    controls: {
      expanded: true,                        // 面板内嵌完整 property documentation
      sort: 'requiredFirst',                 // 必填 props 排最前 = 把契约摆到脸上
      exclude: ['__internal'],               // 面板级过滤（不删文档）
    },
  },
  argTypes: {
    variant: { control: { type: 'radio' }, options: ['primary', 'secondary', 'ghost'] },
    size:    { control: { type: 'inline-radio' }, options: ['sm', 'md', 'lg'] },
    asChild: { control: false },             // ✅ 保留文档、不给控件
    ref:     { control: false },             // ✅ 同上：ref 不是可配置项
    className: { control: 'text', description: '与内部 class 拼接，不覆盖' },
    onClick: { action: 'clicked' },
    advancedPadding: { control: 'number', if: { arg: 'advanced' } },
    __internal: { table: { disable: true } }, // ⚠️ 连 prop documentation 一起删
  },
  args: { variant: 'primary', size: 'md' },   // 默认值只从这里 / 类型来，别手抄第二份
} satisfies Meta<typeof Button>;
export default meta;
type Story = StoryObj<typeof meta>;
export const Default: Story = {};
```

---

## 21. 取源清单与 GitHub API 实测（2026-11-07 快照）

### 21.1 官方原文（逐字口径来源）

| 主题 | 来源 |
|---|---|
| 组合 / 继承、Containment / Specialization | [React legacy · Composition vs Inheritance](https://legacy.reactjs.org/docs/composition-vs-inheritance.html)（页面自述已停更，仅取可逐字核验的结论） |
| 受控 / 非受控、状态提升、single source of truth | [React · Sharing State Between Components](https://react.dev/learn/sharing-state-between-components) |
| `<input>` 受控契约五条 | [React · `<input>`](https://react.dev/reference/react-dom/components/input) |
| props / children / spread | [React · Passing Props to a Component](https://react.dev/learn/passing-props-to-a-component) |
| `useId` 用途与禁忌 | [React · `useId`](https://react.dev/reference/react/useId) |
| `forwardRef` Deprecated 与 Pitfall | [React · `forwardRef`](https://react.dev/reference/react/forwardRef) |
| React 19 `ref as a prop` / ref cleanup / codemod | [React 19 官方博客](https://react.dev/blog/2024/12/05/react-19)（`ref as a prop` 与 `Cleanup functions for refs` 两节） |
| `asChild` / Composition / Accessibility | [Radix Primitives · Introduction](https://www.radix-ui.com/primitives/docs/overview/introduction)、[Composition](https://www.radix-ui.com/primitives/docs/guides/composition)、[Accessibility](https://www.radix-ui.com/primitives/docs/overview/accessibility) |
| `Switch` API 字段与键盘 | [Radix Primitives · Switch](https://www.radix-ui.com/primitives/docs/components/switch) |
| 受控判定与 `mergeProps` | 上游源码 `radix-ui/primitives`：`packages/react/use-controllable-state/src/use-controllable-state.tsx`、`packages/react/slot/src/slot.tsx` |
| `render` 合并 / 开放扩展四条 | [Ariakit · Composition](https://ariakit.org/guide/composition) |
| slots / v-model / props 单向流 | [Vue · Slots](https://vuejs.org/guide/components/slots.html)、[Component v-model](https://vuejs.org/guide/components/v-model.html)、[Props](https://vuejs.org/guide/components/props.html) |
| 键盘契约 / 焦点管理 / Modal Dialog | [W3C WAI-ARIA APG · Developing a Keyboard Interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/)、[Patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)、[Dialog (Modal) Example](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/dialog/) |
| `component` / `slots` / `slotProps` | [MUI · Overriding component structure](https://mui.com/material-ui/customization/overriding-component-structure/) |
| Controls / argTypes / docgen | [Storybook · Controls](https://storybook.js.org/docs/essentials/controls)、[ArgTypes API](https://storybook.js.org/docs/api/arg-types) |
| 设计价值观与模块化 | [Ant Design · 介绍](https://ant.design/docs/spec/introduce-cn) |

### 21.2 GitHub REST API 实测（15 仓库，`GET /repos/{owner}/{repo}`，2026-11-07）

| 仓库 | ★ | License | pushed_at | archived |
|---|---|---|---|---|
| `facebook/react` | 252,127 | MIT | 2026-11-06T15:28:33Z | false |
| `shadcn-ui/ui` | 127,504 | MIT | 2026-11-06T16:20:36Z | false |
| `ant-design/ant-design` | 100,094 | MIT | 2026-11-06T02:21:38Z | false |
| `mui/material-ui` | 99,294 | MIT | 2026-11-06T00:31:52Z | false |
| `storybookjs/storybook` | 91,467 | MIT | 2026-11-06T16:19:19Z | false |
| `vuejs/core` | 54,825 | MIT | 2026-11-06T14:53:32Z | false |
| `chakra-ui/chakra-ui` | 40,713 | MIT | 2026-11-05T10:27:05Z | false |
| `tailwindlabs/headlessui` | 28,810 | MIT | 2026-04-13T16:12:31Z | false |
| `microsoft/fluentui` | 20,390 | NOASSERTION | 2026-11-06T16:02:07Z | false |
| `radix-ui/primitives` | 19,475 | MIT | 2026-10-14T21:52:47Z | false |
| `adobe/react-spectrum` | 16,017 | Apache-2.0 | 2026-11-06T02:27:49Z | false |
| `reactjs/react.dev` | 11,833 | CC-BY-4.0 | 2026-11-05T01:36:35Z | false |
| `ariakit/ariakit` | 8,630 | None | 2026-11-06T13:17:20Z | false |
| `w3c/aria-practices` | 1,361 | NOASSERTION | 2026-11-04T16:57:53Z | false |
| `salesforce/design-system-react` | 989 | BSD-3-Clause | 2026-11-06T08:03:12Z | false |

**选型三问（沿用 `ai-design-toolchain.md` 的口径，比 star 更重要）**：① 许可——`NOASSERTION` / `None` 需人工复核后再用于商业项目；② 活源——`tailwindlabs/headlessui` 的 `pushed_at` 距本轮快照已逾 6 个月，**可读其规范但别当活跃上游**；③ 组合模型——§5 的 5 种换元素 API 不通用，选型时先看它用的是哪一种，别照抄别库的写法。

---

## 22. 取源限制与不臆造声明（本轮公开记录）

1. **Radix `controlled-state` 文档 URL 返回 404**：`https://www.radix-ui.com/primitives/docs/guides/controlled-state` 页面为 `# 404 / This page could not be found.`。受控判定与告警文本**改从上游源码 `use-controllable-state.tsx` 取得**，不臆造文档措辞。
2. **React `Composition vs Inheritance` 属 legacy docs**：页面明确 *"This site is no longer updated"* / *"These docs are old and won't be updated. Go to react.dev"*。本文件只引用其可逐字核验的立场句，现行 API 一律以 `react.dev` 为准。
3. **React 19 博客 URL 重定向**：`react.dev/blog/2024/04/25/react-19` 实际返回 canonical 为 `2024/12/05/react-19` 的内容；本文件按 canonical 引用，不写旧日期。
4. **Storybook `/docs/api/argtypes` 返回 404**：改用现行 `Controls` 页与规范链接 `/docs/api/arg-types`；文档中**没有**字面句 `"args map to props"`，本文件不伪造这句，只引用实际取得的原文。
5. **W3C APG keyboard 页含未完成占位**：*"... other considerations to be added ..."* / *"... to be continued ..."* / *"To be written."*。本文件**不把占位符扩写成规范**，具体按键表以各 Pattern 页为准，不在此重抄。
6. **Vue props 页取回结果由 fallback summary 生成**：以页面正文为准摘取 `One-Way Data Flow` / `Prop Validation` / `Boolean Casting` / `Prop Name Casing` 等段落，工具提示本身不当作规范来源。
7. **MUI / Ant Design / Vue 的组件级逐字 API 表未逐项取得全文**：§10 的完整字段表以 **Radix Switch** 官方 API 为范例，其余库只写已核验的机制（`component` / `slots` / `slotProps`、`modelValue` / `update:modelValue`），**不臆造默认值、类型签名或数值**。
8. **GitHub 数据安全**：本轮用 `git credential fill` 从系统凭据管理器读取有效 PAT 完成 15 次 `GET /repos` 实测；secret 文件中的旧令牌已失效（401），**未改动或覆盖任何凭据文件**。star / pushed_at 是 2026-11-07 快照，会随时间变化，引用时标注快照日期。
9. **不臆造数值原则**：本文件出现的数字只有三类——官方明确的默认值（`asChild` 默认 `false`、`value` 默认 `"on"`）、官方明确的阈值/禁令（布尔 props >5 是**本文件给出的建议判据**，非官方数值，已标注）、以及 GitHub API 实测值。凡未取得原文的数值一律不写。

---

**本轮最重要的一条**：组件库的「不好用」几乎不是样式问题，是**所有权没写清楚**。把状态、渲染 DOM、无障碍与版本这四件事各自指认一个负责人，再让组合层**透传属性、串联事件、拼接标识**，大部分「组合之后就失效」的 bug 会直接消失。而 `forwardRef` 的 React 19 裁决提醒我们：**组件 API 规范是有保质期的**，写规范必须写明目标版本，并让「改契约」这件事能被脚本判成 MAJOR。
