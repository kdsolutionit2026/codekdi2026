---
description: Look at the UI in a real browser at three breakpoints, then report what is actually wrong
argument-hint: /app/invoices or "the sign-in screen"
allowed-tools: Read, Grep, Glob, Bash, mcp__playwright__*
---

Review the UI at **$ARGUMENTS** using **playwright mcp**. Do not describe what the code should render — open it
and report what it does render.

## 1. Open it

Start the dev server if it is not already running (`pnpm dev` in the background, wait for "ready"), then
`browser_navigate` to `http://localhost:3000$ARGUMENTS`.

If you cannot reach the page, report the exact error and stop. Do not screenshot a blank tab and call it fine.

## 2. Capture at three widths

For each of **360 × 800** (mobile), **768 × 1024** (tablet), **1440 × 900** (desktop):
`browser_resize`, take a screenshot, and **read the images**. Then judge each one against this list, and quote
what you actually see:

| Check | Fail looks like |
|---|---|
| Layout holds | horizontal scroll, overlapping text, clipped buttons, content under the bottom nav |
| Tap targets | anything interactive smaller than 44 × 44 px on mobile |
| Text wraps | truncated labels, orphaned words, Bangla losing its matras |
| Contrast | muted grey on grey; text that fails 4.5:1 |
| States | no empty state, no loading skeleton, no error state with a `request_id` |
| Density | desktop using mobile-sized spacing, or mobile showing a desktop table |
| Brand | any hardcoded company name, logo URL or footer string (must come from the platform profile) |
| Money | amounts in a font that cannot show them, or aligned inconsistently in a column |

## 3. Interact

Keyboard only: `Tab` through the page in DOM order, confirm focus is visible and the skip-link works. Then
submit the main form empty, with garbage, and with a very long value. Report what happened.

## 4. Report

- **Blocking** — layout broken, contrast failing, an action that does not work, a hardcoded brand string.
- **Should fix** — spacing off-token, inconsistent alignment, weak empty state.
- **Fine** — say nothing.

For each issue: the route, the breakpoint, what you saw, and the file that owns it. Then fix the blocking ones
and re-capture. Do not claim "responsive" until you have looked at all three widths.
