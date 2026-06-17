# Integrations

Choose the connection method that fits your environment. Each subfolder contains everything you need to wire requests into the operator automatically.

---

## Available Integrations

| Folder | Method | Who it's for | Complexity |
|--------|--------|-------------|-----------|
| `power-automate/` | Microsoft Power Automate | Microsoft shops (Power BI + M365) — no code | Zero-code |
| `servicenow-webhook/` | ServiceNow outbound webhook | Teams using ServiceNow as their ticketing system | Low — needs ServiceNow admin |
| `jira-webhook/` | Jira webhook + Python receiver | Teams using Jira | Low — needs Jira admin + hosting |
| `slack-bot/` | Slack Bolt app | Teams who live in Slack | Low — needs Slack admin + hosting |

If none of these fit, use **copy-paste** (no setup) or run `run setup` and choose "Custom API" to get a code scaffold for your specific environment.

---

## What all integrations have in common

Every integration does the same three things:

1. **Receive** the request from your source (email, ticket, Slack message)
2. **POST** the request text to the Claude API with the operator files as system context
3. **Write** the triage decision card back to the source (as a ticket comment, Slack reply, email, etc.)

The only thing that changes between integrations is steps 1 and 3.

---

## Before you start any integration

You need an Anthropic API key.

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign in or create an account
3. Navigate to **API Keys** → **Create Key**
4. Copy the key — you only see it once
5. Store it as an environment variable or secret in your integration platform (never hardcode it)

The model to use: `claude-sonnet-4-6` (fast and accurate for triage workloads)

---

## System prompt for all integrations

When calling the Claude API, pass your operator files as the system prompt. The minimum required:

```
[Contents of identity.md]
[Contents of rules.md]
[Contents of config.md]
[Contents of current-backlog.md]
```

Optionally include `reference/` files for edge case coverage.

The user message is the raw request text. That's it.

---

## Cost estimate

Each triage call sends roughly 4,000–6,000 tokens (system prompt + request) and returns ~500 tokens.

At current Claude Sonnet pricing, that's approximately **$0.02–0.04 per triage call**.

For a team triaging 20 requests per week, budget under $1/week.
