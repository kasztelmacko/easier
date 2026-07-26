---
name: analysis-planning
description: Structure analysis approach before starting work. Use after adding all relevant context to the analysis_context.md and /other_context
---

# When to use

Use this skill **only when the user explicitly requests** `/plan` or clearly asks to create a plan. Do not invoke it proactively or for general planning suggestions.
Planning is especially important when the analysis involves multiple steps, uncertain data availability, or a tight deadline where sequencing matters. A 15-minute planning session prevents hours of wrong-direction work.
The plan is created for human user to analyse a problem along AI, rather than fully automate the analysis process.

# Process

1. **Decompose the question** — break the business question into sub-questions using `references/scoping_framework.md`; each sub-question should be answerable with a single data pull or calculation.
2. **Propose needed data** - propose what columns, or data sources will be usefull for the analysis. Instead of listing table or column names, just list what may be useful. The human will know where to look for that data. 
3. **Produce the plan** — fill in `context/analysis_plan.md` with the structured analysis plan and a TODO list.

# Inputs the skill needs

- Analysis brief or requirements doc (from `analysis_context.md` and `/other_context`)
- Available data sources

# Output

- Completed analysis plan with sequenced steps (`context/analysis_plan.md`)
