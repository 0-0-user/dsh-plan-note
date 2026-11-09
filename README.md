<div align="center">

<img src="docs/hero.png" width="100%" alt="dsh-plan-note hero card" />

# dsh-plan-note

**Inline annotations for DeepSeek Harness plan review.**

Select a passage, write a comment, send one structured review — the agent stays in plan mode and revises.

[![npm](https://img.shields.io/npm/v/dsh-plan-note?style=flat-square&logo=npm&color=4D6BFE)](https://www.npmjs.com/package/dsh-plan-note)
[![License](https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square)](LICENSE)
[![DSH](https://img.shields.io/badge/DeepSeek%20Harness-0.2.x-4D6BFE?style=flat-square)](https://github.com/deepseek-ai/deepseek-harness)
[![Release](https://img.shields.io/github/v/release/0-0-user/dsh-plan-note?style=flat-square&label=release)](https://github.com/0-0-user/dsh-plan-note/releases)

[**Quick start**](#quick-start) · [**Usage**](#usage) · [**Limits**](#compatibility-and-limits) · [**Releases**](https://github.com/0-0-user/dsh-plan-note/releases) · [中文](README.zh-CN.md)

</div>

---

## Intro

DSH's plan gate gives you two buttons: **approve** or **ask for changes**. That is too coarse for a plan with several unrelated problems — "change step three" loses the sentence it refers to.

`dsh-plan-note` keeps every comment attached to the exact passage it talks about, then sends them back as one structured review. It is inspired by the *Add comment* flow in Claude Code's plan review.

## Contents

<table>
<tr>
<td width="60%" valign="middle">

- [Main features](#main-features)
- [Where it helps](#where-it-helps)
- [Quick start](#quick-start)
- [Usage](#usage)
- [Compatibility and limits](#compatibility-and-limits)
- [Development](#development)
- [Acknowledgements](#acknowledgements)
- [Feedback](#feedback)

</td>
<td width="40%" align="center" valign="middle">

<img src="docs/whale.gif" width="260" alt="cartoon whale" />

</td>
</tr>
</table>

## Main features

| | |
|---|---|
| **Anchored comments** | Drag over any passage; the quote is stored with the comment and shown in the list |
| **Multiple comments** | Collect as many as you need, locate each one, delete and rewrite freely |
| **One review** | Everything is merged into a single Markdown block and returned through DSH's own question channel |
| **Sidebar layout** | The plan opens in the right sidebar; the chat keeps only a slim action bar |
| **Draft protection** | Unsent comments survive a refresh; approving is blocked while feedback is pending |
| **Native look** | Colours, borders and font size inherit the host theme; the plan uses the host's Markdown renderer |

## Where it helps

- Multi-step implementation plans where several details must be fixed before any code is written.
- Migrations, API changes and rollouts where compatibility, rollback and sequencing each need a note.
- Any review where "looks fine" and "not fine" are not the only two answers.

## Quick start

Requires DSH 0.2.x with the web client. Pick one install path.

### GitHub

```bash
dsh plugin --profile <profile> add github:0-0-user/dsh-plan-note
```

### npm

```bash
dsh plugin --profile <profile> add dsh-plan-note
```

### Ask your agent

```text
Install the plugin `dsh-plan-note` for me, then restart DSH:
1. Find my active DSH profile (a folder under ~/.dsh/profiles).
2. Run: dsh plugin --profile <that-profile> add dsh-plan-note
3. Confirm dsh-plan-note 0.1.0 appears in the plugin list.
If the profile is not obvious, ask me which one to use.
```

Restart DSH (or hard-reload the web UI) after installing.

## Usage

### A full round

1. Type `/plan` to enter plan mode.
2. Describe the task; the agent submits a plan and DSH opens the review.
3. The plan appears in the right sidebar under **plan notes**; the chat shows the slim bar.
4. Select a sentence, paragraph, list item or code line.
5. Write the remark in the comment box and press **添加批注**.
6. Repeat for every passage you want changed.
7. Optionally add the overall note at the bottom.
8. Press **发送批注**. The sidebar closes and the agent receives the review.

### What happens after sending

- The agent reads the quoted passages plus your notes and revises the plan.
- Plan mode stays active, so it submits a **new plan** for another round.
- Previous comments are cleared; the new plan starts empty.

### The three buttons

| Button | Does | Available |
|---|---|---|
| 发送批注 | Sends all comments and the overall note as one review | Always |
| 同意执行 | Approves the plan as-is and exits plan mode | Only with no pending comment |
| 关闭 | Dismisses the review and returns the normal composer | Only with no pending comment |

### Edge cases

- A selection spanning bold or links may not highlight after sending; the comment text is kept.
- Reloading the page keeps unsent comments for the same review.
- Switching sessions leaves the review answerable; the plugin re-registers when you come back.
- Approving with pending comments is intentionally blocked.

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

> Captured from a real session; drop the images into `docs/`.

## Compatibility and limits

- Targets DSH **0.2.2-rc.1** APIs (`conversation.composer`, `sidebar.right.pane.tab`); a future kernel may change them.
- Web client only — there is no terminal UI.
- A selection spanning bold or links may fail to highlight; the comment itself is never lost.
- The plan is rendered as Markdown, so annotations anchor to rendered text rather than character offsets.

## Development

Plain JavaScript, no build step.

```
lib/client.js        browser bundle (ModuleLoader contract)
lib/index.js         empty host half
cordis.patch.yml     one loader row
tools/make_whale.py  regenerates docs/whale.gif
docs/                banner and screenshots
```

Regenerate the banner:

```bash
python tools/make_whale.py
```

Issues and pull requests are welcome. Please keep the bundle dependency-free.

## Acknowledgements

- [Claude Code](https://www.anthropic.com/claude-code) — the inline *Add comment* flow that inspired this plugin.
- [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) — the plugin platform and its slot APIs.
- The whale banner is a fan-made cartoon based on DeepSeek's logo.

## Feedback

Open an issue: <https://github.com/0-0-user/dsh-plan-note/issues>

---

<sub>Fan-made project. Not affiliated with or endorsed by DeepSeek or Anthropic. Product names belong to their owners.</sub>
