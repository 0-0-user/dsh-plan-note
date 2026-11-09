# dsh-plan-note

[English](README.md) · 中文

给 **DeepSeek Harness** 的计划评审加选区批注。在计划里选中任意一段，写一句意见，凑齐几条之后一次性发回给 agent，全程不离开计划模式。

![在 DSH 右侧栏里给计划加批注](docs/01-review.png)

## 解决什么问题

DSH 原生的计划评审只有「同意」和「要求修改」两个按钮。当一个计划有几处互不相关的问题时，这个二选一太粗。`dsh-plan-note` 让每条意见都钉在它对应的那句原文上。

## 功能

- **锚定批注**：拖选计划里的文字即可写批注，引用原文会跟着一起发回
- **多条共存**：想写几条写几条，可以定位、可以删除
- **一次提交**：汇总成一段结构化 Markdown，agent 仍停留在计划模式
- **侧栏界面**：计划放在右侧栏，对话框只留一条窄操作条
- **草稿保护**：未发送的批注和整体意见，刷新页面不丢
- **跟随主题**：配色与字号继承宿主，浅色深色都正常

## 安装

从 GitHub 装：

```bash
dsh plugin --profile <profile名> add github:0-0-user/dsh-plan-note
```

从本地目录装：

```bash
dsh plugin --profile <profile名> add /path/to/dsh-plan-note
```

装完需要重启 DSH 应用（或硬刷新网页端）才生效。

## 用法

1. 输入 `/plan` 进入计划模式，让 agent 提交计划
2. 计划会自动出现在右侧栏的「计划批注」标签页
3. 选中文字 → 写意见 → 点「添加批注」
4. 想加几条就重复几次
5. 点「发送批注」，侧栏自动关闭，agent 按批注改稿

按钮说明：「发送批注」提交反馈，「同意执行」直接批准，「关闭」退出评审。**有未发送批注时，后两个按钮会禁用**，避免意见被静默丢弃。

## agent 收到的格式

```markdown
## 计划批注（2 条）

1. 原文：「……」
   意见：……

2. 原文：「……」
   意见：……

## 整体意见
……
```

## 已知限制

- 依赖 DSH **0.2.2-rc.1** 的 `conversation.composer` 与 `sidebar.right.pane.tab`，内核升级后可能失效
- 高亮按引用文本匹配，跨加粗或链接的选区可能定位不到（批注内容不会丢）
- 计划以 Markdown 渲染，批注锚定的是渲染后的文字

## 卸载

```bash
dsh plugin --profile <profile名> remove dsh-plan-note
```

卸载后恢复 DSH 原生计划评审。

## 开发

纯 JavaScript，无构建步骤。浏览器端入口是 `lib/client.js`，遵循 DSH 的 `window.__ModuleLoader__` 约定。

## 许可

MIT
