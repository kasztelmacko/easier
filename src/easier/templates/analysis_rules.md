# Workspace conventions

This analysis uses several context files.

## analysis_assistant_notes.md

Purpose:
Scratchpad for the AI assistant.

Permissions:
- Read: Yes
- Write: Yes

Use this file to:
- Record intermediate observations
- Capture ideas
- Keep temporary notes
- Store reminders for future reasoning

The user may edit this file, but it is primarily owned by the assistant.

---

## analysis_user_notes.md

Purpose:
User-owned notes.

Permissions:
- Read: Yes
- Write: No

Never modify this file.

---

## analysis_progress.md

Purpose:
Current project status.

Permissions:
- Read: Yes
- Write: Yes

Keep this file up to date whenever meaningful progress is made.

---

## analysis_context.md

Purpose:
High-level project context provided by the user.

Permissions:
- Read: Yes
- Write: No

Treat this file as immutable unless the user explicitly asks you to edit it.
