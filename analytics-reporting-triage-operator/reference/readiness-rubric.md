# Readiness Rubric

A request is **build-ready** only when all five criteria below pass. If any criterion fails, the request goes to backlog with the blocker documented. Development does not begin until all five pass.

This rubric is used during triage (§3 of rules.md) to set the Readiness field in the decision card.

---

## The Five Criteria

### R1 — Source Data Exists in the Analytics Layer

**Pass:** The required data fields are live in the data warehouse, semantic model, or analytics-layer dataset. "It exists in the source system" is not sufficient — it must be accessible to the reporting tool without requiring new pipeline work.

**Fail signals:**
- "The ERP team will have this ready after their next sprint"
- "We're going to start capturing this in Excel"
- "The data exists in the source system but we haven't pulled it in yet"
- A request for a field that has never been in any analytics artifact

**What to do on fail:** Log to backlog. Document the dependency (which team, which sprint, which pipeline). Create a re-evaluation trigger date.

---

### R2 — Grain and Scope Are Defined

**Pass:** The level of detail required is agreed upon. By day or by week? By customer or by region? By SKU or by product category? The answers are documented or can be confirmed in a single exchange.

**Fail signals:**
- "We want to see everything" (no grain specified)
- Conflicting requirements between stakeholders on the same request
- Scope described as a feeling ("comprehensive," "full picture") rather than dimensions and filters

**What to do on fail:** Return to the requester with two or three specific scoping questions. Do not begin discovery until answered.

---

### R3 — Business Owner Identified

**Pass:** A named person or role from the requesting business unit has agreed to validate the output, answer questions during development, and sign off at UAT. This person must be available — not just theoretically responsible.

**Fail signals:**
- "Anyone from that team can answer questions"
- The person who submitted the request has no ability to make decisions about what's correct
- The identified owner is on leave or unavailable for the development window

**What to do on fail:** Block development. A report delivered without a validation owner becomes abandoned or incorrect. Require owner confirmation before sprint assignment.

---

### R4 — No Blocking In-Flight Change

**Pass:** No currently in-sprint or in-review work touches the same report, semantic model, or dataset in a way that would create a merge conflict or require rework after deployment.

**Fail signals:**
- Another developer is actively modifying the same semantic model
- A refactoring story is in progress for the same report
- A data layer change is being tested that affects the same tables or measures

**What to do on fail:** Mark as Sequenced. Document what must deploy first and add a re-evaluation trigger. Assign after the blocking item closes.

---

### R5 — Scope Is Bounded Enough to Write a User Story

**Pass:** The request has enough specificity that a developer could write a user story with acceptance criteria. It doesn't need to be fully specified — but it must be specific enough that "done" has a definition.

**Fail signals:**
- "Build us a dashboard for the operations team"
- "We need better visibility into our supply chain"
- "Something like what [Competitor] has"
- A request submitted as a meeting summary with no clear output defined

**What to do on fail:** Return to the requester with a scoping conversation. A 30-minute requirements discussion is far cheaper than three weeks of building toward a moving target.

---

## How to Document a Readiness Failure

In the triage decision card, list each failing criterion and the specific reason:

```
Readiness: NOT READY
  - R1 FAIL: Exception status fields not yet in analytics layer;
             blocked on ERP sprint 7 (~3 weeks)
  - R3 FAIL: No business owner identified; Finance Director delegated
             to "the team" — requires a named contact before dev begins
```

Never write "NOT READY" without documenting which criteria failed and why. The blocker documentation is the product of the readiness check — without it, the item sits in backlog indefinitely with no path forward.
