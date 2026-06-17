# Setup: Analytics & Reporting Triage Operator

This file is a guided setup questionnaire. Run it once when you first load the operator into your Claude project.

**To begin:** Type `run setup` in the chat. Claude will walk you through each section and write your `config.md` file automatically.

If you prefer to configure manually, fill in the template in `config.md` directly.

---

## What setup does

Setup asks you 12 questions across 5 categories. When complete, Claude writes a `config.md` that all operator files read for org-specific behavior:

- Your priority labels (P1/P2 or Critical/High or your own)
- Your ticketing system (so Action fields output the right format)
- Your team structure (so routing rules use the right team names)
- Your sprint cadence (so P2/P3 language matches your cycle)
- Your connection method (so the operator gives you the right intake instructions)

Setup takes about 5 minutes. You only do it once.

---

## The 12 Questions

### Category 1: Your BI Platform

**Q1.** Which tool does your team use to build and deliver reports and dashboards?
- A) Microsoft Power BI
- B) Tableau
- C) Looker / Looker Studio
- D) Metabase
- E) Qlik Sense / QlikView
- F) Other (describe it)

*Why this matters: terminology in triage decision cards ("semantic model," "workbook," "LookML model," etc.) will match your platform.*

---

**Q2.** Where does your team's underlying data live?
- A) Microsoft Fabric / Azure Data Lake
- B) Snowflake
- C) Databricks
- D) AWS Redshift / S3
- E) Google BigQuery
- F) On-premise data warehouse
- G) Mix of the above or other (describe it)

*Why this matters: routing rules for "data doesn't exist yet" blockers reference the right layer and team.*

---

### Category 2: Your Team Structure

**Q3.** How is your analytics team structured?
- A) Solo analyst — I handle everything (BI, data, and requests)
- B) Small BI team (2–5 people), no separate data engineering team
- C) BI team with a separate data engineering team
- D) BI team, separate DE team, and separate source system / ERP team
- E) Other (describe it)

*Why this matters: routing rules change significantly. If there's no DE team, pipeline work stays with BI.*

---

**Q4.** Who has authority to make final triage decisions?
- A) One person (Analytics Manager, BI Lead, etc.) — what is their role title?
- B) Any BI team member can triage
- C) Rotating ownership per sprint
- D) Other

*Why this matters: escalation language and the Escalation Flag output reference this role.*

---

### Category 3: Your Process

**Q5.** What ticketing system does your team use to track work?
- A) ServiceNow
- B) Jira
- C) Azure DevOps (ADO)
- D) Asana
- E) Linear
- F) Trello
- G) We use a shared spreadsheet or document
- H) No formal system yet
- I) Other (name it)

*Why this matters: the Action field in each triage decision card gives instructions in the format your system uses.*

---

**Q6.** What is your sprint cadence?
- A) 1-week sprints
- B) 2-week sprints
- C) 3-week sprints
- D) Kanban (no fixed sprints)
- E) We don't use sprints yet

*Why this matters: "P2 — Current Sprint" and "P3 — Next Sprint" labels only make sense if you have sprints. Kanban teams get different priority language.*

---

**Q7.** How many active development slots does your team have in a typical sprint?
(Count only people who build — not managers, not analysts who only gather requirements)
- A) 1 developer
- B) 2–3 developers
- C) 4–6 developers
- D) 7+ developers

*Why this matters: queue-aware priority. The operator will flag when a new P2 request would exceed your sprint capacity.*

---

**Q8.** What priority labels does your team use?
- A) P1 / P2 / P3 / P4 (use the operator's defaults)
- B) Critical / High / Medium / Low
- C) Urgent / Normal / Low
- D) Custom — I'll describe them

*Why this matters: the operator outputs whatever labels your org already uses.*

---

### Category 4: Your Source Systems

**Q9.** Which source/operational systems feed your analytics environment? Select all that apply.
- A) Microsoft Dynamics 365 (D365 / F&O)
- B) SAP (ERP or BW)
- C) Salesforce (CRM)
- D) NetSuite
- E) Oracle ERP
- F) A custom or legacy ERP
- G) Warehouse Management System (WMS) — which one?
- H) Other (name them)

*Why this matters: routing rules reference the source system team by name when a fix belongs upstream.*

---

### Category 5: Your Connection Method

**Q10.** How will requests reach the operator? Pick your primary method.
- A) **Copy-paste** — someone on the team manually pastes request text into the Claude project chat (no setup required)
- B) **Upload email files** — drag .msg or .eml files exported from Outlook or Gmail into the Claude project
- C) **Power Automate** — requests from email or Microsoft Forms trigger a flow that calls the Claude API (Microsoft ecosystem; no-code)
- D) **ServiceNow webhook** — new tickets in ServiceNow automatically trigger a triage call
- E) **Jira webhook** — new issues in Jira automatically trigger a triage call
- F) **Slack bot** — slash command or keyword in a Slack channel triggers triage
- G) **Custom API** — I have a developer who will wire this up; generate the code scaffold

*Why this matters: setup generates the appropriate integration files or instructions for your chosen method.*

---

**Q11.** (If you chose C, D, E, F, or G above) Do you have the following available?
- [ ] An Anthropic API key
- [ ] Admin access to the system you're connecting (ServiceNow, Jira, Slack workspace, etc.)
- [ ] A place to host a webhook receiver if needed (Azure, AWS, a server) — only required for D, E, F, G

*If you're missing any of these, setup will generate instructions for obtaining them and pick up where you left off.*

---

### Category 6: Backlog Tracking

**Q12.** Do you want the operator to track a running backlog across sessions?
- A) **Yes, full tracking** — the operator updates `current-backlog.md` after every triage decision and considers the existing queue when assigning priority
- B) **Yes, lightweight** — I'll paste my current backlog manually when I want queue-aware priority; the operator won't auto-update files
- C) **No** — treat every request independently; don't track a backlog

*Why this matters: with full tracking, the operator knows "you already have 4 P2s this sprint" and adjusts priority accordingly. Without it, each request is evaluated in isolation.*

---

## After Setup

Once you answer all 12 questions, Claude will:

1. Write your `config.md` file with all your org-specific settings
2. Generate any integration files for your chosen connection method (into the `integrations/` subfolder)
3. Confirm which operator behaviors have changed from the defaults
4. Give you a one-paragraph "how to use this" summary tailored to your setup

You can re-run setup at any time by typing `run setup` — it will ask if you want to update specific sections or start fresh.

---

## Manual Configuration

If you prefer not to run the conversational setup, open `config.md` and fill in each field directly. All fields have defaults that work without customization — the operator runs out of the box, setup just makes it better.
