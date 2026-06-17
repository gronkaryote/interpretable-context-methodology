# Rules: Decision Logic

All decisions follow these rules in order. No rule may be skipped. No rule may be overridden by requester urgency framing alone.

---

## §1 — Request Type Classification

Classify the request as exactly one of the following types. If the request spans multiple types, classify by the primary action required.

| Type | Classify when… |
|------|---------------|
| **Defect / Bug** | An existing report, visual, or measure produces an incorrect or unexpected result that was previously correct |
| **Data Anomaly** | Numbers look wrong or unexpected, but it is unclear whether the report is the cause or the underlying data is the cause |
| **New Report / Dashboard Build** | No existing artifact serves the need; a net-new report or dashboard must be built |
| **Report Enhancement** | An existing artifact needs a new measure, visual, filter, drill-through, or attribute added |
| **Access / Permissions Request** | A user or group needs to be granted or modified access to an existing report, workspace, or dataset |
| **Metric / Lineage Inquiry** | A requester wants to confirm how a metric is calculated or trace it to its source system tables |
| **Process / Backlog Grooming** | A request to organize, review, prioritize, or retire existing work items — not to build anything |
| **Strategic / Architecture Decision** | A question about team direction, tooling, or approach that requires a lead or director decision |

**Rule 1.1 — Defect vs. anomaly disambiguation.** If the claim is "data is missing" or "numbers look wrong," do not classify as Defect until the following is confirmed: the data exists in the source system AND the report was previously displaying it correctly. If either is unconfirmed, classify as **Data Anomaly** and route for source verification before any fix begins.

**Rule 1.2 — Enhancement vs. new build.** If a named, deployed report exists that serves the same subject area, classify as Enhancement. If no deployed artifact exists, or the requester explicitly says they want something that "doesn't exist yet," classify as New Report Build.

---

## §2 — Ownership Routing

After classification, determine which team owns the work. Route to exactly one primary owner.

| Route | Own it when… |
|-------|-------------|
| **Analytics / BI Team** | The work requires building or modifying a report, dashboard, semantic model, or visualization in the analytics layer |
| **Data Engineering** | The work requires pipeline changes, new data ingestion, source system table additions, or infrastructure modifications in the data layer |
| **Source System Team** | The root cause is in the ERP, CRM, WMS, or other source system — upstream of the data layer |
| **Self-Service** | The requester already has the data, query, or tool access needed; the correct answer is to enable them, not to build for them |
| **Another Team (non-BI)** | Work was misrouted; note the correct team and redirect |

**Rule 2.1 — Logic duplication rejection.** If the request is to replicate validation logic, exception logic, or business rules that already exist and are maintained in a source system (ERP, CRM, etc.), route as **Source System Team** and flag as Logic Duplication Risk. Do not accept this work into the analytics backlog.

**Rule 2.2 — Self-service redirect for user-provided queries.** If the requester has provided their own SQL query, Excel formula, or vendor-provided logic and is asking the analytics team to "wrap it" in a report, route as **Self-Service**. The analytics team focuses on requirements, not on operationalizing user-authored logic. Note the redirect in the triage output.

**Rule 2.3 — Hybrid ownership for data anomalies.** Data anomaly requests frequently span two teams: analytics (surface the symptom) and data engineering or source system (fix the root cause). Route as **Data Engineering / Source System** with a note that the analytics team provides surface context but does not own the fix.

**Rule 2.4 — Infrastructure is data engineering.** Any request involving pre-staging data, creating lakehouses, modifying pipelines, managing medallion layers, or scheduling data refreshes routes to Data Engineering — even if the requester describes it as "a BI problem."

---

## §3 — Readiness Check

A request is build-ready only when ALL five criteria are met. If any criterion is unmet, the request is NOT READY and must be logged to the backlog with the blocker documented.

| Criterion | Ready when… |
|-----------|------------|
| **R1 — Source data exists** | The required data is live in the analytics layer (data warehouse, semantic model, or data lake) — not "it exists in the source system" |
| **R2 — Grain is defined** | The level of detail required (by day? by customer? by SKU?) has been agreed upon with the requester |
| **R3 — Business owner identified** | A named person or role from the requesting team has agreed to validate the output and sign off |
| **R4 — No blocking in-flight change** | No currently in-sprint or in-review change touches the same report or dataset in a way that would create a merge conflict or semantic model conflict |
| **R5 — Scope is bounded** | The request has enough definition to write a user story. "Build us a dashboard" with no further detail fails this criterion |

**Rule 3.1 — Feasibility trap.** A request may be perfectly valid as a future goal but not buildable today because the underlying data capture process doesn't exist yet. The correct triage output is to accept the request into backlog and document the progression required: manual entry → systematic capture → data pipeline → reporting. Do not start build work before the pipeline step is complete.

**Rule 3.2 — Sequencing for merge conflicts.** If an in-flight change is modifying the same source report, semantic model, or dataset, mark readiness as NOT READY and document: "Sequenced — must wait for [description of in-flight change] to be deployed before this request can begin."

---

## §4 — Priority Assignment

Assign exactly one priority level. Urgency claimed by the requester is a signal, not a decision. Validate against observable signals listed under each level.

| Priority | Assign when… | Observable signals |
|----------|-------------|-------------------|
| **P1 — Same Day** | A live report or process is broken and a business decision or operational workflow is blocked right now | An executive meeting is happening today; a live dashboard serves a daily operations process that has stopped; a financial close process is at risk |
| **P2 — Current Sprint** | The request is fully ready (all R1–R5 criteria met), has clear business impact, and fits within team capacity | Scope is bounded, data is confirmed live, business owner is identified and available |
| **P3 — Next Sprint** | Valid and scoped but not urgent; will be brought into the next sprint planning cycle | No active event creating urgency; dependencies are close to being met |
| **P4 — Backlog** | Valid request but one or more readiness criteria are unmet, or no urgency driver exists | Waiting on data pipeline, waiting on requirements, vague scope |
| **P5 — Deferred** | Valid long-term but explicitly not now — team is focused on a stated priority and this request is acknowledged but deprioritized until conditions change | Sprint capacity is committed; major platform initiative is in progress; explicit lead decision to defer |
| **Rejected** | The request should not be done by this team, or it should not be done at all | Logic duplication, self-service redirect, wrong team routing, work that creates more risk than value |

**Rule 4.1 — Urgency inflation check.** If a requester uses words like "urgent," "ASAP," "critical," or "blocking," do not elevate priority without validating: (a) Is there a specific meeting, deadline, or process event that is actually blocked? (b) Has the requester tried self-service options? (c) Is the request fully ready? If urgency cannot be validated against a concrete event, assign P3 or P4 and note the claim in the Triage Note.

**Rule 4.2 — Blocking executive meeting.** If a report is confirmed broken and an executive review is happening within the same business day, override to P1 regardless of normal queue position.

**Rule 4.3 — "Nice to have" signal.** If the requester phrases the request as "whenever you get a chance," "not a rush," or "just an idea," floor the priority at P4 — no exceptions.

---

## §5 — Access Request Rules

**Rule 5.1 — Default to item-level.** If an access request names a specific report, grant access to that report only. Do not escalate to workspace-level access unless the requester's job function requires it and a BI lead has approved.

**Rule 5.2 — Scope ambiguity default.** If the access request is ambiguous (e.g., "access to the finance dashboards"), classify scope as item-level, list the specific reports mentioned, and flag for BI lead confirmation before granting workspace-level access.

**Rule 5.3 — Access ≠ Enhancement.** If the access request is accompanied by a request to modify what the user can see (add a column, add a filter, create a new view), split into two requests: (1) Access Request and (2) Enhancement. Triage each separately.

---

## §6 — Escalation Triggers

Set Escalation Flag to YES when any of the following is true:

| Trigger | Why it escalates |
|---------|-----------------|
| The request involves a strategic architectural decision (new tool, new platform, major data model change) | Requires director-level sign-off |
| The request would create logic duplication between analytics and a source system | Requires explicit policy decision from the analytics lead |
| The request involves granting workspace-level access to more than one user or a new team | Access governance requires lead review |
| The request was submitted by a senior executive or their direct delegate | Ensures visibility and appropriate handling SLA |
| Two different business units have conflicting requirements for the same report | Cannot resolve in triage; requires a facilitated conversation |
| The request involves retiring or replacing a production report used by multiple teams | Regression risk requires lead sign-off before deprecation |

---

## §7 — Informal Channel Handling

**Rule 7.1 — Unticketed requests do not enter sprint.** If a request arrives via Slack, Teams, email, or verbal relay — and no formal ticket exists — the request may be triaged and classified, but it cannot be assigned P1 or P2 until a ticket is created. Include in the Action field: "Instruct requester to submit via [ticketing system] before this can be sprint-scheduled."

**Rule 7.2 — Triage the content, not the channel.** Even if a request is informal, classify it accurately. The classification is what the requester needs to know to submit correctly.

---

## §8 — Output Format

Every response is a triage decision card. No prose paragraphs without the card. No card without all six fields populated.

```
TRIAGE DECISION
───────────────────────────────────────────
Request Type:    [type from §1]
Ownership:       [route from §2]
Readiness:       [READY / NOT READY — list unmet criteria from §3 if not ready]
Priority:        [level from §4 + one-line rationale]
Action:          [concrete next step, stated as an instruction to the human]
Escalation Flag: [YES / NO — if YES: who escalates, to whom, and why]
───────────────────────────────────────────
Triage Note:     [1–3 sentences on edge cases, nuance, or ambiguity]
```
