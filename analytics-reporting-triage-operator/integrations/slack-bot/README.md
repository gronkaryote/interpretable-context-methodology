# Slack Bot Integration

A Slack bot that triages requests directly in your BI team's Slack workspace.

Two trigger modes:
1. **Slash command** — anyone types `/triage [request description]` in any channel; bot replies with the decision card
2. **Keyword watch** — bot monitors a designated channel (e.g., `#bi-requests`) and auto-triages any message that contains a trigger phrase

---

## What you need

- Slack workspace admin access (to create a Slack app)
- A place to host the bot (see options below)
- An Anthropic API key

---

## Step 1 — Create the Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From scratch**
2. Name: `BI Triage Bot`
3. Pick your workspace

### Add a Slash Command
1. In your app settings, go to **Slash Commands** → **Create New Command**
2. Command: `/triage`
3. Request URL: `https://[your-bot-url]/slack/triage` (fill in after deploying)
4. Short description: `Triage a BI analytics request`
5. Usage hint: `[describe your request]`

### Add Event Subscriptions (for keyword watch mode)
1. Go to **Event Subscriptions** → enable
2. Request URL: `https://[your-bot-url]/slack/events`
3. Subscribe to bot events: `message.channels`
4. Add the bot to the `#bi-requests` channel

### Set Bot Token Scopes
Go to **OAuth & Permissions** → **Bot Token Scopes**, add:
- `commands`
- `chat:write`
- `channels:history` (for keyword watch)
- `channels:read`

### Install the App
Go to **OAuth & Permissions** → **Install to Workspace** → copy the **Bot User OAuth Token**

---

## Step 2 — Deploy the bot

Set these environment variables:
```
ANTHROPIC_API_KEY=sk-ant-...
SLACK_BOT_TOKEN=xoxb-...        # Bot User OAuth Token from Step 1
SLACK_SIGNING_SECRET=...        # From App credentials page
TRIAGE_CHANNEL=bi-requests      # Channel to watch for keyword triggers (without #)
TRIGGER_PHRASES=help,request,report,dashboard,access,bug,broken,data
OPERATOR_SYSTEM_PROMPT=<contents of identity.md + rules.md + config.md>
```

**Deploy options:**
- **Railway** — connect your GitHub repo, Railway deploys automatically (free tier available)
- **Render** — similar to Railway, free tier available
- **Azure App Service** — best for Microsoft shops already on Azure
- **AWS Lambda + API Gateway** — lowest cost for low-volume usage

---

## Step 3 — Update the Slash Command URL

Once deployed, go back to your Slack app settings and update the Request URL for both the slash command and event subscription to your deployed URL.

---

## How it works in Slack

**Slash command:**
```
/triage The Sales by Territory report is missing data for the Northeast region.
        This is needed for the Monday leadership review.
```
Bot replies in the channel with the full triage decision card.

**Keyword watch (in #bi-requests):**
```
User: Hey team, quick request — can we get access to the P&L dashboard for 
      our new FP&A hire?
```
Bot auto-replies in the thread with the decision card.

---

## Customizing trigger phrases

Edit the `TRIGGER_PHRASES` environment variable. These are simple substring matches — if any phrase appears in a message in the watched channel, the bot triages it.

Default phrases: `help, request, report, dashboard, access, bug, broken, data, urgent, asap`

For a low-noise setup, only watch a dedicated `#bi-requests` channel rather than a general team channel.
