# ServiceNow Webhook Integration

When a new ticket is created in ServiceNow, this integration:
1. Triggers a webhook that calls the Claude API
2. Runs triage on the ticket description
3. Writes the decision card back to the ticket as a work note

---

## What you need

- ServiceNow admin access (to create Business Rules and REST Message records)
- An Anthropic API key
- The webhook receiver running somewhere (see Step 2 options)

---

## Architecture

```
New ServiceNow ticket created
         ↓
Business Rule fires (server-side script)
         ↓
REST Message POSTs to your webhook receiver
         ↓
Webhook receiver calls Claude API
         ↓
Claude returns triage decision card
         ↓
Webhook receiver calls ServiceNow REST API
to add decision card as a Work Note on the ticket
```

---

## Step 1 — Deploy the webhook receiver

The receiver is a small Python app (`receiver.py` in this folder). It:
- Listens for POST requests from ServiceNow
- Calls the Claude API with your operator files as context
- Calls back to ServiceNow to add the work note

**Option A: Azure Functions (recommended for Microsoft shops)**
```bash
# Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4

# Deploy
cd integrations/servicenow-webhook
func azure functionapp publish YOUR_FUNCTION_APP_NAME
```

**Option B: AWS Lambda**
Zip `receiver.py` and its dependencies, upload to Lambda, create an API Gateway trigger.

**Option C: Any Python host**
`receiver.py` is a standard Flask app. Deploy it anywhere that can serve HTTPS and is reachable from your ServiceNow instance.

Set these environment variables wherever you deploy:
```
ANTHROPIC_API_KEY=sk-ant-...
SERVICENOW_INSTANCE=yourcompany.service-now.com
SERVICENOW_USER=your-api-user
SERVICENOW_PASSWORD=your-api-password
WEBHOOK_SECRET=choose-a-random-string
OPERATOR_SYSTEM_PROMPT=<contents of identity.md + rules.md + config.md>
```

---

## Step 2 — Configure ServiceNow

### Create the REST Message

1. In ServiceNow, navigate to **System Web Services → Outbound → REST Message**
2. Click **New**
3. Set:
   - Name: `BI Triage Operator`
   - Endpoint: `https://[your-receiver-url]/triage`
4. Add an HTTP Method named `POST`
5. In the HTTP Request body, use:
```json
{
  "ticket_number": "${ticket_number}",
  "short_description": "${short_description}",
  "description": "${description}",
  "caller": "${caller}",
  "category": "${category}",
  "sys_id": "${sys_id}"
}
```

### Create the Business Rule

1. Navigate to **System Definition → Business Rules**
2. Click **New**
3. Set:
   - Name: `BI Triage — Auto-classify on create`
   - Table: `sc_request` (or `incident`, depending on your ticket type)
   - When: `after`
   - Insert: `true`
   - Update: `false`
4. Add a condition: `Category is Analytics / BI` (or however your org tags BI requests)
5. In the Script tab:
```javascript
(function executeRule(current, previous) {
    var rm = new sn_ws.RESTMessageV2('BI Triage Operator', 'POST');
    rm.setStringParameterNoEscape('ticket_number', current.number.toString());
    rm.setStringParameterNoEscape('short_description', current.short_description.toString());
    rm.setStringParameterNoEscape('description', current.description.toString());
    rm.setStringParameterNoEscape('caller', current.caller_id.getDisplayValue());
    rm.setStringParameterNoEscape('category', current.category.toString());
    rm.setStringParameterNoEscape('sys_id', current.sys_id.toString());
    rm.executeAsync();
})(current, previous);
```

---

## Step 3 — Test

1. Create a test ticket with category set to Analytics / BI
2. Check the Business Rule execution history (**System Log → Business Rules**)
3. Check your receiver logs for the incoming POST and outbound Claude API call
4. Check the ticket — the triage decision card should appear as a Work Note within ~10 seconds
