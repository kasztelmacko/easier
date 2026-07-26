---
name: summarize
description: Summarize analysis progress, findings, and next steps for the user.
---

# When to use

Use this skill **only when the user explicitly requests** `/summarize` or clearly asks to summarize the conversation. Do not invoke it proactively.

**Purpose:** Compact the session into durable analysis context so future turns can continue without the full conversation history.

# Scope

Work only with the analysis context files under `context/`, following the workspace conventions:

| File | Action |
|------|--------|
| `context/analysis_progress.md` | Read and write — keep current project status up to date |
| `context/analysis_assistant_notes.md` | Read and write — assistant scratchpad for durable observations |
| `context/analysis_context.md` | Read only — treat as immutable unless the user explicitly asks to edit it |
| `context/analysis_user_notes.md` | Read only — never modify |

Do **not** update global agent rules, `CLAUDE.md`, `AGENTS.md`, Cursor rules, Copilot instructions, or any other AI-layout files. Those layouts differ by agent; this skill only touches the `context/` files above.

# Process

1. **Read current context** — load the writable and read-only files above (skip empty ones lightly) so updates do not overwrite useful existing content.

2. **Session analysis** — from the conversation and those files, identify:
   - Work completed and findings
   - Decisions and trade-offs
   - Problems encountered and how they were resolved
   - Open items / next steps
   - Intermediate observations worth keeping for future reasoning

3. **Update `analysis_progress.md`** — rewrite or amend so it reflects current status: done, in progress, blocked, and what comes next. Keep it concise and current.

4. **Update `analysis_assistant_notes.md`** — append or merge only durable observations, ideas, and reminders that help future reasoning. Do not dump the transcript; skip anything already captured or no longer useful.

5. **Session summary** — show the user a short summary (below). Only claim file updates you actually made.

# Output

1. Updated `context/analysis_progress.md`
2. Updated `context/analysis_assistant_notes.md` when there is something worth keeping
3. A session summary for the user:

```markdown
## Session Summary

### Completed
- [Bullet list of work done]

### Findings
- [Key analysis findings]

### Decisions
- [Key decisions made during the session]

### Open Items
- [Anything left incomplete or for next session]

### Context Updates
- analysis_progress.md → [what changed]
- analysis_assistant_notes.md → [what changed, or "None"]
```

# Critical rules

1. **Be concise** — short summaries and short file updates
2. **Preserve essential info** — do not lose important analysis context
3. **Never modify** `analysis_user_notes.md` or `analysis_context.md` unless the user explicitly asks
4. **Never update** global/agent rule files or AI-layout docs
5. **Don't duplicate** — skip what is already documented in the context files
6. **Focus on actionable status** — prefer what helps the next session over narrative
