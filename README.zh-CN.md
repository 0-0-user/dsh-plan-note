<div align="center">

<img src="docs/whale.gif" width="460" alt="dsh-plan-note 蓝鲸" />

# dsh-plan-note

**给 DeepSeek Harness 的计划评审加选区批注。**

选中文字 → 写一句意见 → 一次性发回。agent 停留在计划模式，按批注改稿。

<br/>

[![DeepSeek Harness](https://img.shields.io/badge/DeepSeek%20Harness-0.2.x-4D6BFE?style=flat-square)](https://github.com/deepseek-ai/deepseek-harness)
[![License](https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square)](LICENSE)
[![Plugin](https://img.shields.io/badge/type-web%20client%20plugin-4D6BFE?style=flat-square)](#它怎么工作)

**中文** · [English](README.md)

</div>

---

## 为什么做这个

DSH 原生的计划评审只有两个按钮：**同意** 或 **要求修改**。当一个计划有三五处互不相关的问题时，「改一下第三步」这种话根本说不清指的是哪一句。

> **灵感来源**：这个插件参考了 Claude Code 计划评审里的 *Add comment* 功能——选中一句话、就地写批注，让 agent 准确知道你说的是哪一段。`dsh-plan-note` 把这套交互搬到了 DSH。

`dsh-plan-note` 让每条意见都钉在对应的原文上，最后汇总成一份结构化反馈发回去。

## 功能

### 锚定批注

- 在计划的任意段落上拖选，引用原文会和批注一起保存
- 批注列表里始终显示引用，回头能确认自己当时指的是哪句
- 点「定位」跳回原文位置；只要批注还在，那段文字就带红色下划线

### 多条批注

- 标题、段落、列表、代码块里都能选中，数量不限
- 每条批注可以单独删除重写，互不影响
- 底部的「整体意见」用于写不属于某一段的总体反馈

### 一次提交

- 「发送批注」把所有批注和整体意见合成一段 Markdown，走 DSH 已有的提问通道回传
- agent 仍停留在**计划模式**，可以立刻产出修订版供你再看一轮
- 如果计划没问题，直接点「同意执行」即可批准

### 侧栏优先的布局

- 计划在右侧栏的「计划批注」标签页里打开，不压住对话
- 对话框只留一条窄条：`计划批注 · N 条 · [发送批注] [同意执行] [关闭]`
- 发送或同意后侧栏自动关闭；下一次评审会重新打开

### 草稿保护

- 未发送的批注和整体意见按评审保存在浏览器 session storage
- 刷新页面不会丢
- 有未发送批注时，「同意执行」「关闭」禁用，避免意见被静默丢掉

### 跟随主题

- 颜色、边框、字号全部继承宿主主题，深浅色都正常
- 计划用宿主自己的 Markdown 渲染器，标题、列表、表格、代码块和其他地方长得一样

## 安装

三条路，挑一条。

### 1 · 从 GitHub 装（现在就能用）

```bash
dsh plugin --profile <profile> add github:0-0-user/dsh-plan-note
```

把 `<profile>` 换成你的 profile 名（`desktop`、`web` 等），装完重启 DSH。

### 2 · 让 agent 帮你装

把下面这段丢进任意 DSH 会话，让 agent 执行：

```text
帮我装一下 dsh-plan-note 插件，装完重启 DSH：
1. 先找出我正在用的 DSH profile（在 ~/.dsh/profiles 下的目录名）。
2. 执行：dsh plugin --profile <那个 profile> add github:0-0-user/dsh-plan-note
3. 确认插件列表里出现 dsh-plan-note 0.1.0。
如果看不出我用的是哪个 profile，直接问我。
```

### 3 · 从 npm 装（发布后可用）

```bash
dsh plugin --profile <profile> add dsh-plan-note
```

> npm 包尚未发布。发布前请用第 1 或第 2 种方式。

## 用法

### 完整一轮

1. 输入 `/plan` 进入计划模式
2. 描述任务，agent 提交计划，DSH 弹出评审
3. 计划出现在右侧栏的「计划批注」标签页，对话框显示窄条
4. 选中一句话、一段、一个列表项或一行代码
5. 计划下方出现批注输入框：写意见，点「添加批注」
6. 想改几处就重复几次
7. 需要的话在底部写「整体意见」
8. 点「发送批注」，侧栏关闭，agent 收到反馈

### 发送之后会发生什么

- agent 读到引用原文和你的意见，按它改计划
- 计划模式仍然开着，所以它会提交**新一版计划**给你再审一轮
- 上一轮的批注会被清空，新计划从空列表开始

### 三个按钮

| 按钮 | 作用 | 什么时候可点 |
|---|---|---|
| 发送批注 | 把所有批注和整体意见作为一份反馈提交 | 始终可点 |
| 同意执行 | 直接批准计划，退出计划模式 | 没有未发送批注时 |
| 关闭 | 退出评审，agent 回到普通输入框 | 没有未发送批注时 |

### 几个边界情况

- **跨加粗或链接的选区**发送后可能没有高亮（批注文字本身不会丢）
- **刷新页面**不会丢同一轮评审里未发送的批注
- **切换会话**时未完成的评审仍然可以回答，切回来插件会重新接管
- **带着批注点同意**是被禁止的，要么先发出去，要么先删掉

## agent 收到的内容

```markdown
## 计划批注（2 条）

1. 原文：「……」
   意见：……

2. 原文：「……」
   意见：……

## 整体意见
……
```

## 截图

| | |
|---|---|
| ![评审界面](docs/01-review.png) | ![批注列表](docs/02-comments.png) |

> 截图取自真实会话，放进 `docs/` 即可。

## 它怎么工作

- 往 `conversation.composer` 注册一个 chain entry，只接管 `plan-review` 类型的提问
- 用 `sidebar.right.pane.tab` 在右侧栏渲染计划，复用宿主的 `MarkdownText`
- 批注按引用文本锚定，高亮走 CSS Custom Highlight API
- 提交时把「引用 + 意见」作为答案回传给待处理提问——没有宿主 RPC，没有网络请求

## 已知限制

- 依赖 DSH **0.2.2-rc.1** 的 `conversation.composer` 与 `sidebar.right.pane.tab`，内核升级后可能失效
- 跨加粗或链接的选区可能定位不到高亮（批注内容不会丢）
- 只在 Web 客户端可用，没有终端界面

## 卸载

```bash
dsh plugin --profile <profile> remove dsh-plan-note
```

卸载后立刻恢复 DSH 原生计划评审。

## 开发

纯 JavaScript，无构建步骤。`lib/client.js` 是浏览器端 bundle，`tools/make_whale.py` 负责重新生成横幅动画。

## 许可

[MIT](LICENSE)

---

<sub>这是粉丝作品，与 DeepSeek 官方无关，也未获其背书。横幅里的鲸鱼是参考官方 logo 重绘的卡通形象，DeepSeek 名称与标识归其所有者。</sub>

