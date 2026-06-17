# Jira Webhook Integration

When a new issue is created in a Jira project, this integration:
1. Receives the webhook event from Jira
2. Runs triage via the Claude API
3. Adds the decision card as a comment on the Jira issue

---

## What you need

- Jira admin access (to configure webhooks)
- A Jira API token (user-level, not admin)
- The webhook receiver running somewhere with a public HTTPS URL
- An Anthropic API key

---

## Step 1 — Get a Jira API token

1. Go to [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **Create API token**
3. Label it `BI Triage Operator`
4. Copy the token — you only see it once

---

## Step 2 — Deploy the receiver

Set these environment variables:
```
ANTHROPIC_API_KEY=sk-ant-...
JIRA_BASE_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=the-email-of-your-api-token-user@yourcompany.com
JIRA_API_TOKEN=your-jira-api-token
JIRA_PROJECT_KEY=BI         # Only triage issues in this project
WEBHOOK_SECRET=choose-a-random-string
OPERATOR_SYSTEM_PROMPT=<contents of identity.md + rules.md + config.md>
```

Deploy `receiver.py` as you would any Flask app (Azure Functions, AWS Lambda, Railway, Render, etc.).

---

## Step 3 — Configure the Jira webhook

1. In Jira, go to **Settings (gear icon) → System → Webhooks**
2. Click **Create a WebHook**
3. Set:
   - Name: `BI Triage Operator`
   - URL: `https://[your-receiver-url]/triage`
   - Events: Check **Issue → created**
   - JQL filter: `project = BI` (replace with your project key)
4. In the request body, Jira automatically sends the full issue payload
5. Save

---

## Step 4 — Test

1. Create a new issue in your BI Jira project
2. Within ~10 seconds, a comment should appear on the issue with the triage decision card
3. Check your receiver logs if nothing appears

---

## Customizing the comment format

By default the comment is posted as plain text. Jira supports Atlassian Document Format (ADF) for rich formatting. `receiver.py` posts plain text by default, which renders cleanly. To use code blocks and formatting, update the `add_jira_comment` function to wrap the card in an ADF `codeBlock` node.
