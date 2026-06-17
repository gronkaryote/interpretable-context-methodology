# Analytics & Reporting Triage Operator

A folder-based AI operator you drop into a Claude project. It classifies, routes, and prioritizes inbound analytics and reporting requests — end to end — without asking you what to do.

---

## What it does

The Triage Analyst receives a raw request (email text, ticket description, Slack message, meeting note) and returns a structured triage decision:

- **Request type** — what kind of work is this?
- **Ownership** — which team should own it?
- **Readiness** — is it actually buildable yet?
- **Priority** — when should it be worked?
- **Action** — what happens next?
- **Escalation flag** — does a lead need to weigh in?

It makes these decisions. It does not scope requirements, estimate story points, write code, or design reports.

---

## Setup

1. Create a new Claude project
2. Drop the `analytics-reporting-triage-operator/` folder into the project's knowledge files:
   - `identity.md`
   - `rules.md`
   - `examples.md`
   - `reference/` (all four files)
3. Set the project instructions to: *"You are the Triage Analyst. Follow your identity and rules exactly."*

---

## How to use it

Paste the raw request into the chat. Include as much context as you have:

```
From: [requester name or role]
Channel: [email / ticket / Slack / meeting]
Request: [verbatim request text]
Context: [anything else you know — related reports, active sprints, dependencies]
```

The operator returns a triage decision card. No follow-up questions unless a required field is genuinely missing and the gap would change the classification.

---

## What good output looks like

```
TRIAGE DECISION
───────────────────────────────────────────
Request Type:    Report Enhancement
Ownership:       Analytics / BI Team
Readiness:       NOT READY — source data not yet in the data layer
Priority:        Backlog (condition: unblock after DE pipeline delivers)
Action:          Log to backlog. Notify requester of dependency. Revisit in sprint planning once DE confirms pipeline is live.
Escalation Flag: No
───────────────────────────────────────────
Triage Note: The underlying data exists in the source system but has not been
loaded into the analytics layer. Accept the request into backlog and surface
the dependency to the requester — do not start development until the pipeline
is confirmed live.
```

---

## What it does NOT do

- Does not ask clarifying questions just to appear thorough
- Does not accept "I'll need to investigate" as a triage output
- Does not treat urgency claimed by the requester as fact — validates it
- Does not build, code, design, or estimate
- Does not accept business-provided SQL as a build specification

---

## Who this is for

Any analytics team — one person or twenty — that receives requests from multiple channels and needs a consistent, defensible intake decision every time. Works for Power BI teams, Tableau teams, Looker teams, in-house SQL/Python teams, or any hybrid.

---

## Files in this folder

| File | Purpose |
|------|---------|
| `identity.md` | Who the operator is; what it owns; inputs and outputs |
| `rules.md` | The complete decision logic — classification, routing, readiness, priority, escalation |
| `examples.md` | Ten real-pattern decisions including six edge cases |
| `reference/request-intake-checklist.md` | Questions to answer before submitting a request |
| `reference/readiness-rubric.md` | Five-criteria test for whether a request is build-ready |
| `reference/priority-matrix.md` | Urgency × impact matrix with definitions |
| `reference/routing-decision-tree.md` | Decision tree for team ownership |
