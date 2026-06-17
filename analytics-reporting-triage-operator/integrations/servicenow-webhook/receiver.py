"""
BI Triage Operator — ServiceNow Webhook Receiver

Receives ticket data from ServiceNow, calls the Claude API to triage it,
and writes the decision card back to the ticket as a Work Note.

Deploy to Azure Functions, AWS Lambda, or any Python host with HTTPS.

Required environment variables:
    ANTHROPIC_API_KEY           Your Anthropic API key
    SERVICENOW_INSTANCE         e.g., yourcompany.service-now.com
    SERVICENOW_USER             ServiceNow API user with write access
    SERVICENOW_PASSWORD         ServiceNow API user password
    WEBHOOK_SECRET              A shared secret to validate requests from ServiceNow
    OPERATOR_SYSTEM_PROMPT      Combined text of identity.md + rules.md + config.md
    CLAUDE_MODEL                Model to use (default: claude-sonnet-4-6)
"""

import os
import json
import hmac
import hashlib
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
SERVICENOW_INSTANCE = os.environ["SERVICENOW_INSTANCE"]
SERVICENOW_USER = os.environ["SERVICENOW_USER"]
SERVICENOW_PASSWORD = os.environ["SERVICENOW_PASSWORD"]
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]
OPERATOR_SYSTEM_PROMPT = os.environ["OPERATOR_SYSTEM_PROMPT"]
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"


def validate_webhook_secret(req):
    """Verify the request comes from our ServiceNow instance."""
    provided = req.headers.get("X-Webhook-Secret", "")
    return hmac.compare_digest(provided, WEBHOOK_SECRET)


def build_user_message(ticket: dict) -> str:
    return (
        f"From: {ticket.get('caller', 'Unknown')}\n"
        f"Channel: ServiceNow ticket\n"
        f"Ticket: {ticket.get('ticket_number', 'N/A')}\n"
        f"Category: {ticket.get('category', 'N/A')}\n"
        f"Request: {ticket.get('short_description', '')}\n"
        f"Details:\n{ticket.get('description', '')[:3000]}"
    )


def call_claude(user_message: str) -> str:
    """Call the Claude API and return the triage decision card text."""
    response = requests.post(
        ANTHROPIC_API_URL,
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": CLAUDE_MODEL,
            "max_tokens": 1024,
            "system": OPERATOR_SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": user_message}],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["content"][0]["text"]


def add_work_note(sys_id: str, note: str) -> None:
    """Write the triage decision card to the ServiceNow ticket as a Work Note."""
    url = f"https://{SERVICENOW_INSTANCE}/api/now/table/sc_request/{sys_id}"
    payload = {"work_notes": f"[TRIAGE DECISION — automated]\n\n{note}"}
    response = requests.patch(
        url,
        auth=(SERVICENOW_USER, SERVICENOW_PASSWORD),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json=payload,
        timeout=15,
    )
    response.raise_for_status()


@app.route("/triage", methods=["POST"])
def triage():
    if not validate_webhook_secret(request):
        return jsonify({"error": "Unauthorized"}), 401

    ticket = request.get_json(force=True)
    if not ticket:
        return jsonify({"error": "Empty payload"}), 400

    sys_id = ticket.get("sys_id")
    if not sys_id:
        return jsonify({"error": "Missing sys_id"}), 400

    user_message = build_user_message(ticket)
    decision_card = call_claude(user_message)
    add_work_note(sys_id, decision_card)

    return jsonify({"status": "ok", "ticket": ticket.get("ticket_number")}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
