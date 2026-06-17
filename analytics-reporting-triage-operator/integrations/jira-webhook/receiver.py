"""
BI Triage Operator — Jira Webhook Receiver

Receives issue-created events from Jira, calls the Claude API to triage,
and posts the decision card as a comment on the Jira issue.

Deploy to any Python host with a public HTTPS URL.

Required environment variables:
    ANTHROPIC_API_KEY           Your Anthropic API key
    JIRA_BASE_URL               e.g., https://yourcompany.atlassian.net
    JIRA_EMAIL                  Email address of the Jira API token user
    JIRA_API_TOKEN              Jira API token
    JIRA_PROJECT_KEY            Only triage issues in this project (e.g., BI)
    WEBHOOK_SECRET              Shared secret set in the Jira webhook config
    OPERATOR_SYSTEM_PROMPT      Combined text of identity.md + rules.md + config.md
    CLAUDE_MODEL                Model to use (default: claude-sonnet-4-6)
"""

import os
import hmac
import hashlib
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
JIRA_BASE_URL = os.environ["JIRA_BASE_URL"].rstrip("/")
JIRA_EMAIL = os.environ["JIRA_EMAIL"]
JIRA_API_TOKEN = os.environ["JIRA_API_TOKEN"]
JIRA_PROJECT_KEY = os.environ.get("JIRA_PROJECT_KEY", "BI")
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]
OPERATOR_SYSTEM_PROMPT = os.environ["OPERATOR_SYSTEM_PROMPT"]
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"


def validate_webhook_secret(req):
    provided = req.headers.get("X-Webhook-Secret", "")
    return hmac.compare_digest(provided, WEBHOOK_SECRET)


def extract_issue_fields(payload: dict) -> dict:
    issue = payload.get("issue", {})
    fields = issue.get("fields", {})
    reporter = fields.get("reporter") or {}
    return {
        "issue_key": issue.get("key", ""),
        "summary": fields.get("summary", ""),
        "description": (fields.get("description") or "")[:3000],
        "issue_type": (fields.get("issuetype") or {}).get("name", ""),
        "priority": (fields.get("priority") or {}).get("name", ""),
        "reporter": reporter.get("displayName", "Unknown"),
        "project_key": (fields.get("project") or {}).get("key", ""),
    }


def build_user_message(issue: dict) -> str:
    return (
        f"From: {issue['reporter']}\n"
        f"Channel: Jira ticket\n"
        f"Issue: {issue['issue_key']} ({issue['issue_type']})\n"
        f"Request: {issue['summary']}\n"
        f"Details:\n{issue['description']}"
    )


def call_claude(user_message: str) -> str:
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


def add_jira_comment(issue_key: str, comment_text: str) -> None:
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "TRIAGE DECISION — automated via Analytics & Reporting Triage Operator",
                            "marks": [{"type": "strong"}],
                        }
                    ],
                },
                {
                    "type": "codeBlock",
                    "attrs": {"language": "text"},
                    "content": [{"type": "text", "text": comment_text}],
                },
            ],
        }
    }
    response = requests.post(
        url,
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json=payload,
        timeout=15,
    )
    response.raise_for_status()


@app.route("/triage", methods=["POST"])
def triage():
    if not validate_webhook_secret(request):
        return jsonify({"error": "Unauthorized"}), 401

    payload = request.get_json(force=True)
    if not payload:
        return jsonify({"error": "Empty payload"}), 400

    # Only process issue-created events
    if payload.get("webhookEvent") != "jira:issue_created":
        return jsonify({"status": "ignored", "reason": "not an issue_created event"}), 200

    issue = extract_issue_fields(payload)

    # Only triage issues in the configured project
    if issue["project_key"] != JIRA_PROJECT_KEY:
        return jsonify({"status": "ignored", "reason": f"project {issue['project_key']} not configured for triage"}), 200

    user_message = build_user_message(issue)
    decision_card = call_claude(user_message)
    add_jira_comment(issue["issue_key"], decision_card)

    return jsonify({"status": "ok", "issue": issue["issue_key"]}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
