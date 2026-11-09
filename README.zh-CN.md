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

`dsh-plan-note` 让每条意见都钉在对应的原文上，最后汇总成一份结构化反馈发回去。

## 功能

| | |
|---|---|
| 🎯 **锚定批注** | 拖选计划里的文字，引用原文跟着批注一起发回 |
| 🧵 **多条共存** | 想写几条写几条，能定位、能删除 |
| 📦 **一次提交** | 汇总成一段 Markdown，agent 仍停在计划模式 |
| 🪟 **在侧栏，不占对话** | 计划放右侧栏，对话框只留一条窄操作条 |
| 💾 **草稿保护** | 未发送的批注刷新页面不丢 |
| 🌗 **跟随主题** | 配色与字号继承宿主，深浅色都正常 |

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
帮我安装 dsh-plan-note 插件，然后重启应用：
dsh plugin --profile <profile> add github:0-0-user/dsh-plan-note
装好后确认插件列表里出现 dsh-plan-note，版本 0.1.0。
```

### 3 · 从 npm 装（发布后可用）

```bash
dsh plugin --profile <profile> add dsh-plan-note
```

> npm 包尚未发布。发布前请用第 1 或第 2 种方式。

## 用法

1. 输入 `/plan` 进入计划模式，让 agent 提交计划
2. 计划自动出现在右侧栏的「计划批注」标签页
3. 选中一段 → 写意见 → 点「添加批注」
4. 想加几条就重复几次
5. 点「发送批注」，侧栏自动关闭，agent 按批注改稿

| 按钮 | 作用 |
|---|---|
| 发送批注 | 提交结构化反馈 |
| 同意执行 | 直接批准计划 |
| 关闭 | 退出评审，侧栏保留 |

**有未发送批注时，「同意执行」和「关闭」会禁用**，避免意见被静默丢掉。

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
