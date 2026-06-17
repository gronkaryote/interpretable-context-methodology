# Operator Commands

These are the commands the Triage Analyst recognizes. Type them in the Claude project chat exactly as shown.

---

## Core Commands

### `/triage`
**Usage:** `/triage [paste request text here]`

Runs triage on a new request. Returns a full decision card and, if backlog tracking is enabled, appends the item to `current-backlog.md`.

```
/triage
From: Supply Chain Manager
Channel: Email
Request: Can you add a site filter to the Floor Space report?
Context: Report is live. No urgency mentioned.
```

---

### `/close [ID]`
**Usage:** `/close BI-0004`

Marks an item as closed. Operator moves the row from `current-backlog.md` to `archive-backlog.md`, records the closed date, prompts for a final status and one-line resolution note.

The operator will ask:
1. Final status (Completed / Rejected / Withdrawn / Superseded / Duplicate)
2. One-line resolution (what happened?)

---

### `/backlog`
**Usage:** `/backlog`

Displays the current queue from `current-backlog.md` sorted by priority, grouped by status. Highlights capacity overloads (more P2s in sprint than developer slots allow).

Optional filters:
- `/backlog p1` — show only P1 items
- `/backlog blocked` — show only blocked items
- `/backlog [owner]` — show items for a specific team or person

---

### `/capacity`
**Usage:** `/capacity`

Shows the sprint capacity snapshot: how many P1 and P2 slots are filled vs. available. Flags overloads. Useful before sprint planning.

Output example:
```
SPRINT CAPACITY
───────────────────────────────────
Sprint:        Sprint 22 (Jun 9–20)
Developers:    2 active
───────────────────────────────────
P1 active:     1 / 2 cap     ✓ OK
P2 in sprint:  4 / 4 cap     ⚠ AT CAP — new P2 items will queue to P3
P3 queued:     3
P4 backlog:    7
Blocked:       2  (see /backlog blocked for details)
───────────────────────────────────
Recommendation: Sprint is at P2 capacity. Triage any new P2-qualifying
requests as P3 unless a P1/P2 item closes first.
```

---

### `/block [ID] [reason]`
**Usage:** `/block BI-0007 Waiting on ERP sprint 9 to deliver exception status columns`

Updates an item's status to Blocked and records the dependency. Operator updates `current-backlog.md`.

---

### `/unblock [ID]`
**Usage:** `/unblock BI-0007`

Re-evaluates a blocked item. Operator checks whether the stated dependency has been resolved (you describe the current state), re-runs the readiness check, and updates priority if needed.

---

### `/requeue [ID]`
**Usage:** `/requeue BI-0011`

Moves a Deferred item back to active status when its named condition has been met. Operator re-evaluates readiness and priority given the current backlog state.

---

### `/retriage [ID]`
**Usage:** `/retriage BI-0003`

Re-runs triage on an existing item. Use when circumstances have changed (new urgency event, dependency resolved, scope has changed). Operator shows the original decision and the updated decision side-by-side.

---

## Analysis Commands

These queries run against `archive-backlog.md` and the current state in `current-backlog.md`.

### `/report`
**Usage:** `/report`

Generates a triage health summary:
- Request volume by type (last 30 days if date range is available)
- Priority distribution
- Top rejection reasons
- Average days from Triaged to In Sprint for P2 items
- Items blocked longest

---

### `/history [search term]`
**Usage:** `/history P&L dashboard`

Searches `archive-backlog.md` for closed items matching the term. Useful for checking whether a similar request was handled before and how.

---

### `/patterns`
**Usage:** `/patterns`

Analyzes the archive for recurring request patterns — types that are frequently rejected, requesters who bypass formal channels, request types that are consistently blocked by the same dependency. Returns a ranked list of systemic issues.

---

## Setup Commands

### `run setup`
**Usage:** `run setup`

Launches the interactive setup questionnaire from `SETUP.md`. Writes or updates `config.md`. Run once on first use, or anytime you want to update a configuration setting.

---

### `/config`
**Usage:** `/config`

Displays your current configuration from `config.md` in a readable summary. Does not modify anything.

---

### `/reset-backlog`
**Usage:** `/reset-backlog`

Clears `current-backlog.md` (moves all remaining open items to archive with status "Superseded" and a note). Use at the start of a new fiscal year or after a major team restructure. Requires confirmation before executing.

---

## Command Quick Reference

| Command | Purpose |
|---------|---------|
| `/triage [request]` | Triage a new request |
| `/close [ID]` | Close and archive an item |
| `/backlog` | View current queue |
| `/capacity` | Check sprint capacity |
| `/block [ID] [reason]` | Mark an item as blocked |
| `/unblock [ID]` | Re-evaluate a blocked item |
| `/requeue [ID]` | Re-activate a deferred item |
| `/retriage [ID]` | Re-run triage on an existing item |
| `/report` | Triage health summary |
| `/history [term]` | Search archive |
| `/patterns` | Analyze systemic issues |
| `run setup` | Run or re-run setup |
| `/config` | View current configuration |
| `/reset-backlog` | Archive all open items (use carefully) |
