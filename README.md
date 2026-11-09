<div align="center">

<img src="docs/whale.gif" width="460" alt="dsh-plan-note whale" />

# dsh-plan-note

**Inline annotations for DeepSeek Harness plan review.**

Select text → write a comment → send one structured review. The agent stays in plan mode and revises.

<br/>

[![DeepSeek Harness](https://img.shields.io/badge/DeepSeek%20Harness-0.2.x-4D6BFE?style=flat-square)](https://github.com/deepseek-ai/deepseek-harness)
[![npm](https://img.shields.io/npm/v/dsh-plan-note?style=flat-square)](https://www.npmjs.com/package/dsh-plan-note)
[![License](https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square)](LICENSE)
[![Plugin](https://img.shields.io/badge/type-web%20client%20plugin-4D6BFE?style=flat-square)](#how-it-works)

[中文](README.zh-CN.md) · **English**

</div>

---

## Why

DSH's plan gate is binary: **approve** or **ask for changes**. That is too coarse when a plan has several unrelated problems — "change step three" loses the sentence it refers to.

> **Inspiration.** This plugin borrows the inline-comment experience from Claude Code's plan review: select a sentence, attach a remark, and let the agent see exactly what you meant. `dsh-plan-note` brings that interaction to DSH.

`dsh-plan-note` keeps every comment attached to the exact passage it talks about, and sends them back as one structured review.

## Features

### Anchored comments

- Drag over any passage of the plan; the quote is captured with the comment.
- The quote is shown in the comment list, so you always know what you reacted to.
- Click **定位** to scroll back to that passage; the passage is underlined in red while the comment exists.

### Multi-comment review

- Collect as many comments as you need across headings, paragraphs, lists and code blocks.
- Each comment can be edited before sending (delete and re-add) and carries its own note.
- An optional **整体意见** box holds feedback that does not belong to a single passage.

### One structured review

- **发送批注** turns everything into a single Markdown block and returns it through DSH's existing question channel.
- The agent stays in **plan mode** and can immediately produce a revised plan for another round.
- Approving later is still possible: **同意执行** sends the approve label directly.

### Sidebar-first layout

- The plan opens in the right sidebar as a **plan notes** tab, not on top of the conversation.
- The chat surface only keeps a slim bar: `计划批注 · N 条 · [发送批注] [同意执行] [关闭]`.
- Sending or approving closes the sidebar automatically; the next review reopens it.

### Draft protection

- Unsent comments and the overall note are kept in the browser's session storage, per review.
- Reloading the page does not lose your work.
- While comments are unsent, **同意执行** and **关闭** are disabled, so feedback cannot be dropped silently.

### Native look

- Colours, borders and font size inherit the host theme; light and dark both work.
- Markdown renders with the host's own renderer, so headings, lists, tables and code blocks look like the rest of DSH.

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
Install the plugin `dsh-plan-note` for me, then restart DSH:
1. Find my active DSH profile (a folder under ~/.dsh/profiles).
2. Run: dsh plugin --profile <that-profile> add github:0-0-user/dsh-plan-note
3. Confirm dsh-plan-note 0.1.0 appears in the plugin list.
If the profile is not obvious, ask me which one to use.
```

### 3 · npm

```bash
dsh plugin --profile <profile> add dsh-plan-note
```

Published as [`dsh-plan-note`](https://www.npmjs.com/package/dsh-plan-note).

## Usage

### A full round

1. Type `/plan` to enter plan mode.
2. Describe the task; the agent submits a plan and DSH opens the review.
3. The plan appears in the right sidebar under **plan notes**; the chat shows the slim bar.
4. Select a sentence, paragraph, list item or code line.
5. A comment box appears under the plan: write the remark, press **添加批注**.
6. Repeat for every passage you want changed.
7. Optionally write the overall note at the bottom.
8. Press **发送批注**. The sidebar closes and the agent receives the review.

### What happens after you send

- The agent reads the quoted passages plus your notes and revises the plan.
- Plan mode stays active, so it submits a **new plan** for another review round.
- Your previous comments are cleared; the new plan starts with an empty list.

### The three buttons

| Button | What it does | When it is available |
|---|---|---|
| 发送批注 | Sends every comment and the overall note as one structured review | Always |
| 同意执行 | Approves the plan as-is and exits plan mode | Only when no comment is pending |
| 关闭 | Dismisses the review; the agent returns to the normal composer | Only when no comment is pending |

### Edge cases worth knowing

- **Selection across bold or links** may not be highlighted after sending (the comment text itself is kept).
- **Reloading the page** keeps unsent comments for the same review.
- **Switching sessions** while a review is pending leaves the review answerable; the plugin re-registers when you come back.
- **Approving with comments open** is intentionally blocked; delete or send them first.

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

---

<sub>Fan-made project. Not affiliated with or endorsed by DeepSeek. The whale banner is a cartoon inspired by DeepSeek's logo; DeepSeek and its marks belong to their owner.</sub>

