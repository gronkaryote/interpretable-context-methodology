# Examples: Decisions in Action

Ten examples drawn from real patterns in analytics and BI request intake. Six include edge cases. Each shows the raw input and the full triage decision.

---

## Example 1 — Standard Enhancement (Clear Accept)

**Input:**
```
From: Supply Chain Analyst
Channel: Email to BI support inbox
Request: Can you add a filter for warehouse site to the Inventory Projection
dashboard? Right now it shows all sites combined and I need to be able to
look at one site at a time. No major rush — just whenever the team has bandwidth.
Context: The Inventory Projection dashboard is live in Power BI.
```

**Decision:**

```
TRIAGE DECISION
───────────────────────────────────────────
Request Type:    Report Enhancement
Ownership:       Analytics / BI Team
Readiness:       READY — site dimension exists in the semantic model; scope is
                 bounded; no in-flight changes affect this report
Priority:        P4 — Backlog (requester explicitly stated "no rush")
Action:          Log to BI backlog. Assign to next available developer. No
                 discovery session needed — scope is clear.
Escalation Flag: NO
───────────────────────────────────────────
Triage Note: Requester's "whenever you have bandwidth" framing floors
this at P4 per Rule 4.3. The request is fully ready; it will move to P2
once a developer has capacity in sprint planning.
```

---

## Example 2 — Access Request with Scope Default

**Input:**
```
From: Finance Director
Channel: Slack DM to Analytics Manager
Request: Hey, can you give my new analyst access to the finance dashboards?
She started this week.
Context: Team uses Power BI. "Finance dashboards" is a workspace containing
seven reports.
```

**Decision:**

```
TRIAGE DECISION
───────────────────────────────────────────
Request Type:    Access / Permissions Request
Ownership:       Analytics / BI Team
Readiness:       NOT READY — scope is ambiguous ("finance dashboards" =
                 workspace with 7 reports; item-level vs. workspace-level
                 not specified)
Priority:        P3 — Next Sprint (access requests are typically fast
                 to fulfill once scoped; no urgency signal beyond "started
                 this week")
Action:          Reply to Finance Director: confirm which specific reports
                 the analyst needs. Default to item-level access for the
                 reports named. Do not grant workspace-level access without
                 BI lead confirmation. Create a ticket once scope is confirmed.
Escalation Flag: YES — if workspace-level access is confirmed needed,
                 escalate to BI lead for approval before granting.
───────────────────────────────────────────
Triage Note: This arrived via Slack DM — informal channel. Per Rule 7.1,
it cannot be sprint-scheduled until a ticket exists. The access scope is
the blocker, not the channel; resolving scope unlocks both issues at once.
Default to item-level per Rule 5.1.
```

---

## Example 3 — Edge Case: "Missing Data" That Is Not a Bug

**Input:**
```
From: Sales Operations Manager
Channel: Service desk ticket
Request: The Sales Performance report is showing no data for the last
two weeks. We're in a regional planning meeting tomorrow and need this
fixed urgently.
Context: Report has been live for 8 months. No recent deployments noted.
```

**Decision:**

```
TRIAGE DECISION
───────────────────────────────────────────
Request Type:    Data Anomaly (NOT classified as Defect — see Triage Note)
Ownership:       Analytics / BI Team (surface check) + Data Engineering
                 (root cause investigation)
Readiness:       NOT READY for a fix — root cause unconfirmed; symptom
                 has not been verified against source data
Priority:        P1 — Same Day (regional planning meeting is tomorrow;
                 urgency is validated by a concrete event)
Action:          Step 1 (BI, immediate): Open the report in development
                 mode and check the date filter state and slicer defaults —
                 "no data" for a two-week window is a common filter-state
                 presentation, not a data absence. Step 2 (only if filter
                 state is correct): Check the data pipeline for refresh
                 failures in the last 48 hours. Step 3: If pipeline shows
                 failures, escalate to Data Engineering with timestamps.
                 Do not log a bug or write a fix until the root cause is
                 confirmed.
Escalation Flag: YES — if pipeline failure is confirmed, escalate to Data
                 Engineering immediately given tomorrow's meeting.
───────────────────────────────────────────
Triage Note: Per Rule 1.1, "missing data" claims must be verified before
classifying as Defect. The most common cause of "no data showing" in
self-serve BI reports is a date slicer or filter defaulting to a range
that excludes recent data — a display interaction, not a data absence.
Verify this in 5 minutes before opening a pipeline investigation. Only
classify as Defect if the data exists in the source and the report was
previously displaying it correctly.
```

---

## Example 4 — Edge Case: The Feasibility Trap

**Input:**
```
From: VP of Operations
Channel: Meeting note relayed by Business Analyst
Request: We want a real-time dashboard showing production line efficiency
by shift, by machine, and by SKU. We're going to start tracking this
manually in Excel for now and want it in Power BI within a month.
Context: No systematic data capture exists yet. Plant floor data is not
connected to any ERP or data system.
```

**Decision:**

```
TRIAGE DECISION
───────────────────────────────────────────
Request Type:    New Report / Dashboard Build
Ownership:       Analytics / BI Team (future) — NOT ready to assign yet
Readiness:       NOT READY — R1 fails: required data is not in the analytics
                 layer or any connected source system; R2 fails: grain
                 (shift/machine/SKU) is defined but data to support it does
                 not exist; R5 partial: scope is described but not achievable
                 on stated timeline
Priority:        P4 — Backlog (with condition: revisit after data capture
                 pipeline is operational)
Action:          Respond to VP via Business Analyst: accept the request into
                 the backlog and document the required progression —
                 (1) Manual Excel capture begins [no BI dependency],
                 (2) Systematic capture method or source system integration
                 defined and implemented [Data Engineering dependency],
                 (3) Pipeline to analytics layer built [Data Engineering],
                 (4) BI report built [Analytics / BI Team]. One month is not
                 a realistic timeline for steps 1–4 from a standing start.
                 Provide this progression as a written note back to the VP.
Escalation Flag: YES — VP-level request; timeline expectations require a
                 frank, documented response. Escalate to Analytics Director
                 to align expectations in writing.
───────────────────────────────────────────
Triage Note: Per Rule 3.1, this is a textbook feasibility trap. The
dashboard is a valid long-term goal, but the data capture infrastructure
doesn't exist. Starting a BI build on top of "we'll track it in Excel
for now" creates a report that shows whatever someone remembered to type,
not operational truth. The correct response is to accept the intent,
document the dependency chain, and set honest timeline expectations.
```

---

## Example 5 — Edge Case: Self-Service SQL Redirect

**Input:**
```
From: Finance Analyst
Channel: Email to Analytics Manager
Request: Our ERP vendor just sent us a SQL query that pulls all the
GL transaction details we need for the year-end audit report. Can you
take this query and build it into a Power BI report? I've attached the
SQL file.
Context: Attachment contains 200-line SQL query authored by an ERP vendor.
```

**Decision:**

```
TRIAGE DECISION
───────────────────────────────────────────
Request Type:    New Report / Dashboard Build
Ownership:       Self-Service (redirect) — NOT Analytics / BI Team
Readiness:       NOT READY for BI intake — self-service redirect applies
                 before readiness is evaluated
Priority:        Rejected (for the framing as presented — see Action)
Action:          Respond to Finance Analyst: the analytics team does not
                 operationalize vendor-provided SQL queries as report
                 specifications. Two paths forward — (1) Self-service:
                 if the analyst has database access, they can run the
                 vendor query directly in their tool of choice; (2) BI
                 intake: if a sustained, maintained report is needed,
                 submit requirements — what decisions does this report
                 drive? what grain? what filters? The BI team will scope
                 from requirements, not from the vendor's query.
Escalation Flag: NO
───────────────────────────────────────────
Triage Note: Per Rule 2.2, business- or vendor-provided SQL is not a
valid build specification. The analytics team owns requirements-driven
development; taking a vendor query as spec creates a maintenance burden
the team doesn't own and can't debug. The redirect is firm but the
two-path response keeps the door open for a proper intake if this is
a recurring business need.
```

---

## Example 6 — Edge Case: Urgency Inflation

**Input:**
```
From: Regional Sales Manager
Channel: Teams message to BI Developer (direct)
Request: URGENT — I need the Sales by Territory report updated to include
the new Northeast Zone split ASAP. This is critical for my team.
Context: Northeast Zone split was announced 6 weeks ago. This is the first
request received. No meeting or deadline is mentioned. Developer notes
there are three other enhancements queued for this same report.
```

**Decision:**

```
TRIAGE DECISION
───────────────────────────────────────────
Request Type:    Report Enhancement
Ownership:       Analytics / BI Team
Readiness:       NOT READY — R4 fails: three other enhancements are
                 currently queued for the same report; merge conflict risk
                 requires sequencing review; R5: zone split mapping/data
                 needs confirmation as live in the analytics layer
Priority:        P3 — Next Sprint (urgency claim does not validate;
                 no concrete event, meeting, or deadline is cited; request
                 is 6 weeks old; see Triage Note)
Action:          (1) Instruct requester to submit via the formal ticketing
                 system — this arrived via direct Teams message to a
                 developer. (2) Confirm the Northeast Zone split data is
                 live in the analytics layer before any work begins. (3)
                 Sequence this enhancement after the three in-queue changes
                 for this report are deployed. (4) Respond to requester
                 with the sequencing explanation and an estimated sprint.
Escalation Flag: NO
───────────────────────────────────────────
Triage Note: Per Rule 4.1, "URGENT" and "ASAP" framing without a
concrete blocking event does not elevate priority. The 6-week gap between
the zone split announcement and this request contradicts the urgency claim.
Per Rule 7.1, direct developer DMs are informal channel — the request
needs a ticket before it can be sprint-scheduled. Additionally, the
developer should not accept scope changes through direct messages — this
protects the team from invisible scope creep.
```

---

## Example 7 — Edge Case: Upstream Dependency Blocker

**Input:**
```
From: Accounts Payable Lead
Channel: Service desk ticket
Request: We need a Power BI dashboard showing invoice exception statuses —
blocked, pending approval, variance flags. The ERP team said this data
will be available "after their next sprint."
Context: ERP team is in sprint 7. BI team is aware the exception status
columns don't yet exist in any data pipeline. ERP sprint 7 delivers in
3 weeks.
```

**Decision:**

```
TRIAGE DECISION
───────────────────────────────────────────
Request Type:    New Report / Dashboard Build
Ownership:       Analytics / BI Team (after dependency resolves) — blocked
                 on Source System Team (ERP) delivering exception status data
Readiness:       NOT READY — R1 fails: exception status columns do not
                 exist in the analytics layer or any pipeline; dependency
                 is ERP sprint 7 delivery (~3 weeks)
Priority:        P4 — Backlog (with condition: move to P2 when ERP sprint 7
                 closes and Data Engineering confirms columns are live in
                 the analytics layer)
Action:          Log to BI backlog with dependency flag. Create a calendar
                 reminder to re-evaluate readiness 3 weeks from today once
                 ERP sprint 7 closes. Respond to AP Lead with: "Request
                 accepted into backlog. We cannot begin development until
                 ERP sprint 7 delivers the exception status fields and
                 Data Engineering has loaded them into our analytics layer.
                 We'll follow up at that point."
Escalation Flag: NO
───────────────────────────────────────────
Triage Note: The readiness failure here is a known, time-boxed dependency
rather than an open-ended unknown. Logging with a specific re-evaluation
trigger ("ERP sprint 7 closes") converts this from a vague backlog item
to a actionable one. Do not start any design or prototyping work — without
the actual data columns, any prototype will be speculative and may need
to be rebuilt.
```

---

## Example 8 — Edge Case: Logic Duplication Rejection

**Input:**
```
From: Supply Chain Manager
Channel: Email to BI support inbox
Request: Our ERP system calculates order quantity variances and flags them
as exceptions. But the interface is hard to use and we can't export to
Excel. Can BI just rebuild that exception logic in Power BI so we have
a better interface?
Context: The variance and exception logic is maintained by the ERP team
and is calculated in the source system. It has been live and validated
for 3 years.
```

**Decision:**

```
TRIAGE DECISION
───────────────────────────────────────────
Request Type:    New Report / Dashboard Build
Ownership:       Source System Team (ERP) — Logic Duplication Risk applies;
                 see Triage Note
Readiness:       NOT READY for BI intake — Logic Duplication Risk must be
                 resolved before acceptance
Priority:        Rejected (as requested) — redirect to a better path
Action:          Respond to Supply Chain Manager: rebuilding ERP-maintained
                 exception logic in Power BI creates two sources of truth
                 for the same calculation — which version is authoritative
                 when they diverge? Instead, propose: (1) Work with ERP
                 team to add an export capability to the existing exception
                 view, or (2) Surface the ERP exception flag as a raw field
                 in the data pipeline — BI displays it, ERP owns it. Route
                 option (2) as a data pipeline request to Data Engineering.
Escalation Flag: YES — Logic Duplication Risk requires an explicit policy
                 decision from the Analytics lead before any alternative
                 path is accepted.
───────────────────────────────────────────
Triage Note: Per Rule 2.1, rebuilding business logic that already exists
in a source system is a standing rejection pattern. The risk: two systems
calculating the same thing drift apart over time, and the business loses
trust in both. The two proposed alternatives preserve single-source-of-truth.
Option 2 (expose the flag, don't recalculate it) is usually the right
architecture — BI becomes the presentation layer, not the logic layer.
```

---

## Example 9 — Edge Case: Merge Conflict Sequencing

**Input:**
```
From: Finance Business Analyst
Channel: ADO work item submitted through formal intake
Request: Add a current-month-to-date view to the P&L dashboard so finance
can see actuals vs. budget without waiting for month close.
Context: Analytics Manager notes that a BI developer is currently mid-sprint
on a P&L refactoring story that modifies the underlying semantic model and
measure structure. That story is 4–5 days from being deployed.
```

**Decision:**

```
TRIAGE DECISION
───────────────────────────────────────────
Request Type:    Report Enhancement
Ownership:       Analytics / BI Team
Readiness:       NOT READY — R4 fails: an in-flight P&L semantic model
                 refactoring is in progress; starting this enhancement now
                 would create a merge conflict or require rebuilding measures
                 against an about-to-change model
Priority:        P2 — Current Sprint (once the refactoring deploys; all
                 other readiness criteria are met; request is well-scoped
                 and has clear business value for the finance close cycle)
Action:          Accept into current sprint queue with sequencing hold.
                 Assign to a BI developer to begin after the P&L
                 refactoring story deploys (~4–5 business days). Notify
                 Finance Business Analyst of the sequencing reason and
                 the expected start date.
Escalation Flag: NO
───────────────────────────────────────────
Triage Note: Per Rule 3.2, this is a sequencing block, not a true
readiness failure. The request is valid, scoped, and ready in every
other dimension — the only blocker is an in-flight change to the same
artifact. Setting a P2 with a sequencing hold preserves the priority
without creating a merge conflict. The developer starting this work
should pull the refactoring branch first to ensure they're building
on the new model structure.
```

---

## Example 10 — Edge Case: Strategic Request That Looks Like a Build Request

**Input:**
```
From: Analytics Manager
Channel: Internal team discussion
Request: Our legacy report migration list has 40 reports on it. Should
we keep treating this list as our roadmap, or should we stop and only
build new reports based on what the business actually needs today?
Context: The migration list was created 18 months ago. Multiple reports
on the list have had zero access in the past 6 months per usage data.
```

**Decision:**

```
TRIAGE DECISION
───────────────────────────────────────────
Request Type:    Strategic / Architecture Decision
Ownership:       Director of Data & Analytics (decision authority)
Readiness:       READY for a decision conversation — the question is
                 well-framed and usage data is available to inform it
Priority:        P2 — Current Sprint (this is blocking sprint planning
                 prioritization; resolving it unlocks backlog direction
                 for the whole team)
Action:          Schedule a focused 30-minute decision meeting with the
                 Director of Data & Analytics. Bring: (1) the current
                 migration list with last-access dates from usage data,
                 (2) a count of reports with zero access in the last 6
                 months, (3) a proposed alternative: move legacy reports
                 to a separate archival workspace and build new reports
                 only on confirmed business need. Document the decision
                 in writing for the team backlog.
Escalation Flag: YES — direction of the reporting roadmap is a director-
                 level decision. Analytics Manager should not resolve
                 this unilaterally.
───────────────────────────────────────────
Triage Note: This is correctly classified as Strategic rather than a
build request. The answer to "should we build these 40 reports?" is not
found in a backlog — it's found in a direction-setting conversation with
leadership. The usage data is the key input: reports with zero access
in 6 months are strong candidates for archival rather than migration.
The recommended outcome of the meeting is to stop anchoring on the
legacy list and shift to needs-based discovery ("what decision does
this report enable?") as the intake filter for new work.
```
