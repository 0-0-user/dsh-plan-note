<div align="center">

<img src="docs/hero.png" width="100%" alt="dsh-plan-note hero card" />

# dsh-plan-note

**Inline annotations for DeepSeek Harness plan review.**

Select a passage, write a comment, send one structured review — the agent stays in plan mode and revises.

[![npm](https://img.shields.io/npm/v/dsh-plan-note?style=flat-square&logo=npm&color=4D6BFE)](https://www.npmjs.com/package/dsh-plan-note)
[![License](https://img.shields.io/badge/license-MIT-2ea44f?style=flat-square)](LICENSE)
[![DSH](https://img.shields.io/badge/DeepSeek%20Harness-0.2.x-4D6BFE?style=flat-square)](https://github.com/deepseek-ai/deepseek-harness)
[![Release](https://img.shields.io/github/v/release/0-0-user/dsh-plan-note?style=flat-square&label=release)](https://github.com/0-0-user/dsh-plan-note/releases)

[**Quick start**](#quick-start) · [**Demo**](#demo) · [**Usage**](#usage) · [**Limits**](#limits) · [中文](README.zh-CN.md)

</div>

---

<a id="intro"></a>

<img src="docs/sections/en/01-intro.png" width="100%" alt="Intro" />

DSH's plan gate gives you two buttons: **approve** or **ask for changes**. That is too coarse for a plan with several unrelated problems — "change step three" loses the sentence it refers to.

`dsh-plan-note` keeps every comment attached to the exact passage it talks about, then sends them back as one structured review. It is inspired by the *Add comment* flow in Claude Code's plan review.

<a id="demo"></a>

<img src="docs/sections/en/02-demo.png" width="100%" alt="Demo" />

### 1. The demo

<img src="docs/01-review.png" width="100%" alt="Plan review in the sidebar" />

<a id="demo-select"></a>

### 2. Selecting text

Drag over any passage of the plan; the comment box opens underneath.

<img src="docs/02-selection.png" width="100%" alt="Text selected" />

<a id="demo-comment"></a>

### 3. Adding a comment

Write the remark and press **添加批注**; the comment is pinned to that passage. Approve and close are greyed out until the comment is sent.

<img src="docs/03-comment.png" width="100%" alt="First comment added" />

<a id="demo-multi"></a>

### 4. Multiple comments and the overall note

Add as many comments as you need; the overall note at the bottom holds feedback that is not tied to one passage.

<img src="docs/04-overall.png" width="100%" alt="Multiple comments and overall note" />

<a id="index"></a>

<img src="docs/sections/en/03-index.png" width="100%" alt="Contents" />

<table>
<tr>
<td width="54%" valign="top">

<table>
<tr><td><a href="#demo">Demo</a></td></tr>
<tr><td><a href="#features">Main features</a></td></tr>
<tr><td><a href="#use-cases">Where it helps</a></td></tr>
<tr><td><a href="#quick-start">Quick start</a></td></tr>
<tr><td><a href="#usage">Usage</a></td></tr>
<tr><td><a href="#limits">Compatibility and limits</a></td></tr>
<tr><td><a href="#dev">Development</a></td></tr>
<tr><td><a href="#thanks">Acknowledgements</a></td></tr>
<tr><td><a href="#feedback">Feedback</a></td></tr>
</table>

</td>
<td width="46%" align="center" valign="middle">

<img src="docs/mark.png" width="170" alt="DeepSeek whale mark" />

<img src="docs/brand.png" width="300" alt="deepseek harness plan note" />

</td>
</tr>
</table>

<a id="features"></a>

<img src="docs/sections/en/04-features.png" width="100%" alt="Main features" />

| | |
|---|---|
| **Anchored comments** | Drag over any passage; the quote is stored with the comment and shown in the list |
| **Multiple comments** | Collect as many as you need, locate each one, delete and rewrite freely |
| **One review** | Everything is merged into a single Markdown block and returned through DSH's own question channel |
| **Sidebar layout** | The plan opens in the right sidebar; the chat keeps only a slim action bar |
| **Draft protection** | Unsent comments survive a refresh; approving is blocked while feedback is pending |
| **Native look** | Colours, borders and font size inherit the host theme; the plan uses the host's Markdown renderer |

<a id="use-cases"></a>

<img src="docs/sections/en/05-use-cases.png" width="100%" alt="Where it helps" />

- Multi-step implementation plans where several details must be fixed before any code is written.
- Migrations, API changes and rollouts where compatibility, rollback and sequencing each need a note.
- Any review where "looks fine" and "not fine" are not the only two answers.

<a id="quick-start"></a>

<img src="docs/sections/en/06-quick-start.png" width="100%" alt="Quick start" />

Requires DSH 0.2.x with the web client. Pick one install path.

**GitHub**

```bash
dsh plugin --profile <profile> add github:0-0-user/dsh-plan-note
```

**npm**

```bash
dsh plugin --profile <profile> add dsh-plan-note
```

**Ask your agent**

```text
Install the plugin `dsh-plan-note` for me, then restart DSH:
1. Find my active DSH profile (a folder under ~/.dsh/profiles).
2. Run: dsh plugin --profile <that-profile> add dsh-plan-note
3. Confirm dsh-plan-note 0.1.0 appears in the plugin list.
If the profile is not obvious, ask me which one to use.
```

Restart DSH (or hard-reload the web UI) after installing.

<a id="usage"></a>

<img src="docs/sections/en/07-usage.png" width="100%" alt="Usage" />

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

### What the agent receives

```markdown
## 计划批注（2 条）

1. 原文：「……」
   意见：……

2. 原文：「……」
   意见：……

## 整体意见
……
```

<a id="limits"></a>

<img src="docs/sections/en/08-limits.png" width="100%" alt="Compatibility and limits" />

- Targets DSH **0.2.2-rc.1** APIs (`conversation.composer`, `sidebar.right.pane.tab`); a future kernel may change them.
- Web client only — there is no terminal UI.
- A selection spanning bold or links may fail to highlight; the comment itself is never lost.
- The plan is rendered as Markdown, so annotations anchor to rendered text rather than character offsets.

<a id="dev"></a>

<img src="docs/sections/en/09-dev.png" width="100%" alt="Development" />

Plain JavaScript, no build step.

```
lib/client.js           browser bundle (ModuleLoader contract)
lib/index.js            empty host half
cordis.patch.yml        one loader row
tools/make_hero.py      generates docs/hero.png
tools/make_sections.py  generates the section banners
docs/                   banner, mark and demo screenshots
```

Issues and pull requests are welcome. Please keep the bundle dependency-free.

<a id="thanks"></a>

<img src="docs/sections/en/10-thanks.png" width="100%" alt="Acknowledgements" />

- [Claude Code](https://www.anthropic.com/claude-code) — the inline *Add comment* flow that inspired this plugin.
- [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) — the plugin platform and its slot APIs.
- The whale mark is DeepSeek's; the banner is a fan-made composition around it.

<a id="feedback"></a>

<img src="docs/sections/en/11-feedback.png" width="100%" alt="Feedback" />

Feedback, suggestions and criticism are all welcome.

- GitHub Issues: <https://github.com/0-0-user/dsh-plan-note/issues>
- Xiaohongshu (RED): 1551112051
- Bilibili: 1615793632

Demo videos will be posted on both platforms as well.

---

<sub>Fan-made project. Not affiliated with or endorsed by DeepSeek or Anthropic. Product names belong to their owners.</sub>
