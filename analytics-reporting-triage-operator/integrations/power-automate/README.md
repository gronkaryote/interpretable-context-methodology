# Power Automate Integration

No-code integration for Microsoft environments. Works with:
- Shared mailbox (emails to a BI support inbox → triage decision added as a reply or logged to SharePoint)
- Microsoft Forms (form submission → triage decision sent back to submitter)
- ServiceNow + M365 hybrid (ticket created → Power Automate triggers → Claude triages → decision written to ticket)

---

## What you need

- Power Automate (included in most Microsoft 365 plans)
- An Anthropic API key
- A shared mailbox or Forms form (depending on your trigger)
- Optional: A SharePoint list or Teams channel to log decisions

---

## Setup: Email Trigger (most common)

### Step 1 — Store your API key

In Power Automate, go to **Data → Connections → New Connection → HTTP**.

Alternatively, store the key in **Azure Key Vault** and reference it as a secret. This is the more secure option for production use.

### Step 2 — Import the flow template

1. Download `bi-triage-email-flow.json` from this folder
2. In Power Automate, go to **My Flows → Import → Import Package**
3. Upload the JSON file
4. Map the connections (your M365 account, HTTP connector)
5. Update the three variables in the flow:
   - `ANTHROPIC_API_KEY` — your API key
   - `SHARED_MAILBOX` — the email address requests come from (e.g., `bi-requests@yourcompany.com`)
   - `OPERATOR_SYSTEM_PROMPT` — paste the combined contents of `identity.md` + `rules.md` + `config.md`

### Step 3 — Test it

Send a test email to your shared mailbox. The flow should:
1. Trigger on new email arrival
2. Extract the subject + body
3. POST to the Claude API
4. Reply to the email thread with the triage decision card

---

## Flow Logic (what the template does)

```
TRIGGER: New email arrives in shared mailbox [bi-requests@yourcompany.com]
│
├── CONDITION: Is sender an internal domain? (filter spam/auto-replies)
│   └── NO → Do nothing
│   └── YES → Continue
│
├── ACTION: Compose the user message
│   From: [email sender]
│   Channel: Email
│   Subject: [email subject]
│   Request: [email body, first 2000 characters]
│
├── ACTION: HTTP POST to Claude API
│   URL: https://api.anthropic.com/v1/messages
│   Headers:
│     x-api-key: [ANTHROPIC_API_KEY]
│     anthropic-version: 2023-06-01
│     content-type: application/json
│   Body: (see bi-triage-email-flow.json for full schema)
│
├── ACTION: Parse the response (extract triage decision card from content[0].text)
│
└── ACTION: Reply to email thread with the decision card
    (or: Post to Teams channel, or: Add row to SharePoint list)
```

---

## Customizing the output destination

By default the flow replies to the email thread. You can change the final action to:

**Post to a Teams channel:**
Add a "Post message in a chat or channel" action. Use the triage decision card as the message body. Good for giving the whole team visibility.

**Add a row to a SharePoint list:**
Add a "Create item" action pointing to a SharePoint list with columns matching the decision card fields. This gives you a queryable backlog in SharePoint without any additional tooling.

**Create a ticket in ServiceNow or Jira:**
Add the appropriate connector action after the Claude API call. Map the decision card fields (Request Type, Priority, Ownership) to the ticket fields.

---

## Microsoft Forms Trigger (alternative)

If your team submits requests via a Microsoft Form:

1. Create a Form with fields matching the `reference/request-intake-checklist.md` questions
2. Use the "When a new response is submitted" trigger in Power Automate
3. Replace the email body extraction with "Get response details" → map form fields to the user message
4. Rest of the flow is identical

This is the cleanest intake path for teams who want structured requests rather than free-text emails.
