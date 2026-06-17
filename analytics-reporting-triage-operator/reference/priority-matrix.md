# Priority Matrix

Use this matrix to validate a priority assignment. Priority is set by the intersection of **Urgency** (time sensitivity) and **Impact** (business consequence of not having this).

The matrix produces a recommended priority level. Rules 4.1–4.3 in rules.md can override the matrix output in specific conditions.

---

## The Matrix

|                        | **Impact: Low**<br>Nice to have; work continues without it | **Impact: Medium**<br>Reduces efficiency; workarounds exist | **Impact: High**<br>Decision is blocked; process degrades; data is wrong |
|------------------------|-----------------------------------------------------------|-------------------------------------------------------------|-------------------------------------------------------------------------|
| **Urgency: None**<br>No deadline; no event | P4 — Backlog | P4 — Backlog | P3 — Next Sprint |
| **Urgency: Soft**<br>Coming up in the next cycle | P4 — Backlog | P3 — Next Sprint | P2 — Current Sprint |
| **Urgency: Hard**<br>Specific event or deadline in <2 weeks | P3 — Next Sprint | P2 — Current Sprint | P1 — Same Day if live; P2 if build-new |
| **Urgency: Critical**<br>Happening today; already blocked | Reject or P3 (re-evaluate urgency) | P1 — Same Day | P1 — Same Day |

---

## Urgency Definitions

**None** — No event driving the timing. Requester would like it eventually.
Signal phrases: "whenever you get to it," "just an idea," "for the future"

**Soft** — The timing matters but there's flexibility. Tied to an upcoming cycle (month close, quarterly review, sprint planning).
Signal phrases: "for the next monthly review," "before our Q3 planning," "in the next couple of sprints"

**Hard** — A specific event with a real date. The report directly serves that event.
Signal phrases: "we have an executive review on [date]," "month close is in 8 days," "go-live is March 1"

**Critical** — The event is today or the process is broken right now.
Signal phrases: "the meeting is in 2 hours," "the pipeline has been down since this morning," "finance can't close without this"

---

## Impact Definitions

**Low** — The requesting team has a viable workaround. The absence of this report creates inconvenience, not harm.
Examples: an extra export step, a slightly different drill path, a visual they prefer but don't strictly need

**Medium** — The workaround exists but is costly: manual reconciliation, data being pulled from multiple sources, key users spending significant time on a process the report would automate.
Examples: 2+ hours of weekly manual Excel work that a report would replace; filter state that makes a useful view require multiple clicks

**High** — No viable workaround. The business decision cannot be made, the process cannot run, or the data being shown is wrong and is actively misleading the team.
Examples: live report showing incorrect financials before an executive meeting; a pipeline metric used to trigger operational decisions returning null; a defect that causes incorrect data to appear correct

---

## Override Rules (from rules.md)

| Condition | Override |
|-----------|---------|
| Requester says "urgent" but no concrete event is named | Do NOT elevate. Apply Rule 4.1 — validate against observable signals. If not validated, drop to P3 or P4. |
| Executive meeting is confirmed today and the report is broken | Override to P1 regardless of matrix position (Rule 4.2) |
| Requester says "whenever you get a chance" | Floor to P4 regardless of impact (Rule 4.3) |
| Request is NOT READY (any R1–R5 failure) | Assign P4 regardless of urgency. Priority cannot be higher than P4 if the item cannot be started. |
| Request is a strategic or architecture decision | Remove from this matrix. Route to Escalation. |

---

## Priority Definitions (quick reference)

| Level | Label | Meaning |
|-------|-------|---------|
| P1 | Same Day | Drop other work. Address today. |
| P2 | Current Sprint | Assign to active sprint. Starts this week. |
| P3 | Next Sprint | Queued for next sprint planning. Starts in 1–2 weeks. |
| P4 | Backlog | Valid but unscheduled. Re-evaluated each sprint planning cycle. |
| P5 | Deferred | Acknowledged but explicitly not now. Named condition for re-evaluation. |
| — | Rejected | This team should not do this work, or the work should not be done. |
