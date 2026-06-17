# Current Backlog

Tracks all open requests. The operator reads this file on every triage call to reason about queue capacity and relative priority.

**Do not add items manually.** Use the `/triage` command — the operator appends automatically.
**To close an item:** Use the `/close [ID]` command — the operator moves it to `archive-backlog.md`.

---

## Sprint Capacity Snapshot

*Updated by the operator after each triage call.*

```
Sprint:          [current sprint label or date range]
Developers:      [n] active
P1 active:       0 / 2 cap
P2 in sprint:    0 / 4 cap
P3 queued:       0
P4 backlog:      0
Blocked:         0  (awaiting dependency)
```

---

## Active Items

| ID | Date Triaged | Request Summary | Type | Owner | Readiness | Priority | Status | Urgency Driver | Blocked By |
|----|-------------|-----------------|------|-------|-----------|----------|--------|---------------|------------|
| — | — | No items yet. Run `/triage [request]` to add the first one. | — | — | — | — | — | — | — |

---

## Status Definitions

| Status | Meaning |
|--------|---------|
| `Triaged` | Classified and prioritized; not yet assigned to a sprint |
| `In Sprint` | Actively being worked in current sprint |
| `Blocked` | Cannot start — dependency documented in Blocked By column |
| `Sequenced` | Ready but must wait for another item to deploy first |
| `Under Review` | In UAT or stakeholder validation |
| `Pending Info` | Operator waiting on requester to provide missing information |

---

## Commands Reference

| Command | What it does |
|---------|-------------|
| `/triage [paste request text]` | Run triage on a new request; append result to this file |
| `/close [ID]` | Move item from this file to `archive-backlog.md` with closed date |
| `/backlog` | Display the current queue sorted by priority |
| `/capacity` | Show sprint capacity snapshot and flag any overloads |
| `/block [ID] [reason]` | Mark an item as Blocked with a named dependency |
| `/unblock [ID]` | Re-evaluate a Blocked item; update readiness and priority |
| `/requeue [ID]` | Move a Deferred item back to active when its condition is met |

---

## Notes

*Use this section for backlog-level context the operator should know when triaging new requests — e.g., "team is in a platform migration freeze until [date]," "no new report builds accepted until ERP go-live," "sprint 18 is capacity-locked."*

```
[No notes yet.]
```
