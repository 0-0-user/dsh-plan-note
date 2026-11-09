<div align="center">

<img src="docs/whale.gif" width="460" alt="dsh-plan-note whale" />

# dsh-plan-note

**Inline annotations for DeepSeek Harness plan review.**

Select text → write a comment → send one structured review. The agent stays in plan mode and revises.

<br/>

[![DeepSeek Harness](https://img.shields.io/badge/DeepSeek%20Harness-0.2.x-4D6BFE?style=flat-square)](https://github.com/deepseek-ai/deepseek-harness)
[![License](https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square)](LICENSE)
[![Plugin](https://img.shields.io/badge/type-web%20client%20plugin-4D6BFE?style=flat-square)](#how-it-works)

[中文](README.zh-CN.md) · **English**

</div>

---

## Why

DSH's plan gate is binary: **approve** or **ask for changes**. That is too coarse when a plan has several unrelated problems — "change step three" loses the sentence it refers to.

`dsh-plan-note` keeps every comment attached to the exact passage it talks about, and sends them back as one structured review.

## Features

| | |
|---|---|
| 🎯 **Anchored comments** | Drag over plan text; the quote travels with the comment |
| 🧵 **Many at once** | Collect as many comments as you need, locate or delete each |
| 📦 **One review** | A single structured Markdown block, agent stays in plan mode |
| 🪟 **Sidebar, not chat** | The plan lives in the right sidebar; chat keeps a slim action bar |
| 💾 **Draft safety** | Unsent comments survive a page refresh |
| 🌗 **Theme aware** | Colours and font size inherit the host theme |

## Install

Pick whichever path fits you.

### 1 · GitHub (works today)

```bash
dsh plugin --profile <profile> add github:0-0-user/dsh-plan-note
```

Replace `<profile>` with your profile name (`desktop`, `web`, …). Restart DSH afterwards.

### 2 · Ask your agent

Paste this into any DSH session and let the agent do it:

```text
帮我安装 dsh-plan-note 插件，然后重启应用：
dsh plugin --profile <profile> add github:0-0-user/dsh-plan-note
装好后确认插件列表里出现 dsh-plan-note，版本 0.1.0。
```

### 3 · npm (once published)

```bash
dsh plugin --profile <profile> add dsh-plan-note
```

> The npm package is not published yet. Until it is, use path 1 or 2.

## Usage

1. Enter plan mode with `/plan` and let the agent submit a plan.
2. The plan opens in the right sidebar under **Plan notes**.
3. Select a passage → write your comment → **添加批注**.
4. Repeat for as many passages as needed.
5. **发送批注** sends everything, closes the sidebar, and the agent revises.

| Button | Does |
|---|---|
| 发送批注 | Send the structured review |
| 同意执行 | Approve the plan as-is |
| 关闭 | Dismiss the review, keep the sidebar |

While comments are unsent, **同意执行** and **关闭** are disabled, so feedback is never dropped silently.

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

## Screenshots

| | |
|---|---|
| ![review](docs/01-review.png) | ![comments](docs/02-comments.png) |

> Screenshots are captured from a real session; drop them into `docs/`.

## How it works

- Registers a `conversation.composer` chain entry that claims only `plan-review` questions.
- Renders the plan in a `sidebar.right.pane.tab` tab, using the host's `MarkdownText`.
- Comments anchor to quoted text; highlights use the CSS Custom Highlight API.
- Submitting answers the pending question with the quote + comment block — no host RPC, no network.

## Known limitations

- Targets DSH **0.2.2-rc.1** APIs (`conversation.composer`, `sidebar.right.pane.tab`); a future kernel may change them.
- A selection spanning bold or links may not highlight (the comment itself is kept).
- The plugin is a web-client plugin; there is no terminal UI.

## Uninstall

```bash
dsh plugin --profile <profile> remove dsh-plan-note
```

Removing it restores DSH's built-in plan review immediately.

## Development

Plain JavaScript, no build step. `lib/client.js` is the browser bundle; `tools/make_whale.py` regenerates the banner.

## License

[MIT](LICENSE)
