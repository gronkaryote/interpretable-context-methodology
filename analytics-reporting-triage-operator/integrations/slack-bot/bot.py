"""
BI Triage Operator — Slack Bot

Handles /triage slash commands and optional keyword-triggered auto-triage
in a designated #bi-requests channel.

Uses Slack Bolt for Python (pip install slack-bolt).

Required environment variables:
    ANTHROPIC_API_KEY       Your Anthropic API key
    SLACK_BOT_TOKEN         Bot User OAuth Token (xoxb-...)
    SLACK_SIGNING_SECRET    From Slack App credentials page
    TRIAGE_CHANNEL          Channel to watch for keyword triggers (no #)
    TRIGGER_PHRASES         Comma-separated phrases that trigger auto-triage
    OPERATOR_SYSTEM_PROMPT  Combined text of identity.md + rules.md + config.md
    CLAUDE_MODEL            Model to use (default: claude-sonnet-4-6)
"""

import os
import requests
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
TRIAGE_CHANNEL = os.environ.get("TRIAGE_CHANNEL", "bi-requests")
TRIGGER_PHRASES = [p.strip().lower() for p in os.environ.get("TRIGGER_PHRASES", "request,report,dashboard,access,bug,broken,urgent").split(",")]
OPERATOR_SYSTEM_PROMPT = os.environ["OPERATOR_SYSTEM_PROMPT"]
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

bolt_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)
flask_app = Flask(__name__)
handler = SlackRequestHandler(bolt_app)


def call_claude(user_message: str) -> str:
    """Call the Claude API and return the triage decision card."""
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


def format_slack_message(decision_card: str) -> list:
    """Format the triage decision card as Slack blocks for clean rendering."""
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*TRIAGE DECISION* — Analytics & Reporting Triage Operator",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"```{decision_card}```",
            },
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Automated triage. Reply in thread with questions or additional context.",
                }
            ],
        },
    ]


@bolt_app.command("/triage")
def handle_slash_triage(ack, say, command):
    """Handle /triage slash command."""
    ack()

    request_text = command.get("text", "").strip()
    if not request_text:
        say("Usage: `/triage [describe your request]`\nExample: `/triage Can we add a site filter to the Inventory dashboard?`")
        return

    user_message = (
        f"From: Slack user ({command.get('user_name', 'unknown')})\n"
        f"Channel: Slack slash command\n"
        f"Request: {request_text}"
    )

    decision_card = call_claude(user_message)
    say(blocks=format_slack_message(decision_card), text="Triage decision ready.")


@bolt_app.event("message")
def handle_channel_message(event, say, client):
    """Auto-triage messages in the designated #bi-requests channel that contain trigger phrases."""

    # Ignore bot messages and message edits
    if event.get("subtype") or event.get("bot_id"):
        return

    # Only watch the configured triage channel
    channel_info = client.conversations_info(channel=event["channel"])
    channel_name = channel_info["channel"]["name"]
    if channel_name != TRIAGE_CHANNEL:
        return

    # Only trigger on messages containing at least one trigger phrase
    message_text = event.get("text", "").lower()
    if not any(phrase in message_text for phrase in TRIGGER_PHRASES):
        return

    user_message = (
        f"From: Slack user\n"
        f"Channel: #{TRIAGE_CHANNEL} (Slack message)\n"
        f"Request: {event.get('text', '')}"
    )

    decision_card = call_claude(user_message)

    # Reply in thread so the decision is attached to the original message
    say(
        thread_ts=event["ts"],
        blocks=format_slack_message(decision_card),
        text="Triage decision ready.",
    )


@flask_app.route("/slack/triage", methods=["POST"])
def slack_triage():
    return handler.handle(request)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/health", methods=["GET"])
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8080)
