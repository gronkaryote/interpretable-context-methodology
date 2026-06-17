# Request Intake Checklist

Use this checklist to capture the information needed before submitting a request to the Triage Analyst. Complete as many fields as you can — the operator will flag what is missing and what it means for the classification.

---

## Required (operator cannot classify without these)

- [ ] **What do you want?**
  Describe the request in plain language. What should exist or work differently after this is done?

- [ ] **Who is asking?**
  Your role or team. (Individual name is optional; role is required for routing.)

- [ ] **How did this request arrive?**
  Email / service desk ticket / Slack or Teams / meeting note / verbal relay

---

## Strongly Recommended (missing items become readiness blockers)

- [ ] **Which report, dashboard, or dataset is involved?**
  Name it specifically. "The P&L dashboard" is sufficient. "The finance report" is not.

- [ ] **Does the underlying data already exist in an analytics tool or data warehouse?**
  Yes / No / Unknown — if Unknown, note where you believe the data lives (source system, spreadsheet, etc.)

- [ ] **Is there a specific event, meeting, or deadline driving urgency?**
  Name the event and date. "It's important to us" is not an urgency signal.

- [ ] **Who from your team will validate the output and sign off?**
  Name or role. This person must be available during development for questions.

- [ ] **Is there a related ticket, email thread, or prior request?**
  Link or reference if it exists. This prevents duplicate intake.

---

## Optional (adds clarity, speeds triage)

- [ ] **What decision does this report or data enable?**
  "We use this to decide X during Y process." If you can't answer this, the request may need to be scoped before intake.

- [ ] **How often will this be used and by whom?**
  Daily operational use vs. monthly executive review changes the priority signal.

- [ ] **Have you tried to get this information yourself?**
  If the data is accessible in a source system or self-service tool, the operator may redirect rather than build.

---

## Red flags (review before submitting)

These patterns indicate the request may be misrouted or not ready:

- You're attaching a SQL query or Excel formula and asking BI to "build this" — likely a self-service redirect
- The data "will exist soon" or "is being entered manually for now" — likely a feasibility block
- You're asking BI to recreate something that already exists in your ERP, CRM, or WMS — likely a logic duplication rejection
- You don't have a named person who can validate the output — the request will be blocked at readiness check
- You're asking for access to "everything" rather than specific reports — will be scoped down at triage
