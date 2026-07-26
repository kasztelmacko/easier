---
name: plan-revise
description: Revise the existing analysis plan when new context emerges during the conversation. Use only when the user explicitly requests /plan-revise or clearly asks to revise the plan.
---

# When to use

Use this skill **only when the user explicitly requests** `/plan-revise` or clearly asks to revise the plan. Do not invoke it proactively when new ideas appear in conversation.
Revising is useful when new data, constraints, or findings make the current plan incomplete, mis-sequenced, or partly wrong — without throwing away work already done.

# Process

1. **Read the current plan** — load `context/analysis_plan.md` and note which items are completed vs pending.
2. **Fold in new context** — from the conversation (and updated `analysis_context.md` / `/other_context` if present), decide what to add, reorder, update, or drop among pending/future items.
3. **Revise in place** — update `context/analysis_plan.md` with these rules:
   - **Preserve completed** — leave finished steps and their status untouched.
   - **Keep existing wording** — do not rephrase or rewrite existing plan text unless that specific part must change for correctness.
   - **Full revise otherwise** — add new sub-questions, data needs, or TODOs; reorder or drop pending items when new context requires it.
4. **Keep structure** — stay within the same plan sections (business question, sub-questions, data plan, approach, out of scope, TODO list).

# Inputs the skill needs

- Existing analysis plan (`context/analysis_plan.md`)
- New context from the conversation (and optional updates in `analysis_context.md` / `/other_context`)

# Output

- Updated analysis plan in `context/analysis_plan.md` reflecting the revise, with completed work preserved
