import json
from datetime import datetime, UTC
from urllib import request


def send_audit_log(tool_call: str, session_id: str, webhook_url: str | None) -> None:
    if not webhook_url:
        return

    payload = {
        "toolCall": tool_call,
        "sessionId": session_id,
        "dateTime": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    }
    body = json.dumps(payload).encode("utf-8")

    req = request.Request(
        webhook_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=5):
        pass