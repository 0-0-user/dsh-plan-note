# dsh-plan-note

[中文说明](README.zh-CN.md) · English

Inline annotations for **DeepSeek Harness** plan review. Select any passage of a plan, write a comment on it, collect several comments, and send them back as one structured review — without leaving plan mode.

![Annotating a plan in the DSH sidebar](docs/01-review.png)

## Why

DSH's plan gate is binary: approve or ask for changes. That is too coarse when a plan needs several unrelated corrections. `dsh-plan-note` keeps every comment attached to the exact sentence it refers to.

## Features

- **Anchored comments** — drag over plan text, comment on it; the quote travels with the comment
- **Multiple comments** — collect as many as you need, locate or delete each one
- **One review** — send a single structured Markdown block; the agent stays in plan mode
- **Sidebar UI** — the plan lives in the right sidebar; the chat surface keeps only a slim action bar
- **Draft safety** — unsent comments and the overall note survive a page refresh
- **Theme aware** — colours and font size inherit the host theme

## Install

From GitHub:

```bash
dsh plugin --profile <name> add github:0-0-user/dsh-plan-note
```

From a local checkout:

```bash
dsh plugin --profile <name> add /path/to/dsh-plan-note
```

Restart the DSH app (or hard-reload the web UI) after installing or updating.

## Usage

1. Enter plan mode (`/plan`) and let the agent submit a plan.
2. The plan opens in the right sidebar under **计划批注 / Plan notes**.
3. Select text → write a comment → **添加批注**.
4. Repeat for as many passages as needed.
5. **发送批注** sends them, closes the sidebar, and the agent revises the plan.

Buttons: **发送批注** (send), **同意执行** (approve), **关闭** (dismiss). While comments are unsent, approve and dismiss are disabled so feedback is never dropped silently.

## What the agent receives

```markdown
## 计划批注（2 条）

1. 原文：「……」
   意见：……

2. 原文：「……」
   意见：……

## 整体意见
……
```

## Known limitations

- Targets the DSH `conversation.composer` and `sidebar.right.pane.tab` APIs of **0.2.2-rc.1**; a future kernel may change them.
- Highlights are matched by quoted text, so a selection spanning bold or links may not highlight (the comment itself is kept).
- The plan is rendered as Markdown; annotations anchor to rendered text rather than character offsets.

## Uninstall

```bash
dsh plugin --profile <name> remove dsh-plan-note
```

Removing the plugin restores DSH's built-in plan review.

## Development

Plain JavaScript, no build step. The browser bundle is `lib/client.js` and follows DSH's `window.__ModuleLoader__` contract.

## License

MIT
