import sys
import json

from canopy_mcp.policy import CanopyPolicy


# Common Input:

"""
{
  "timestamp": "2026-02-09T10:30:00.000Z",
  "cwd": "/path/to/workspace",
  "sessionId": "session-identifier",
  "hookEventName": "PreToolUse",
  "transcript_path": "/path/to/transcript.json"
}
"""

# Common Output:

"""
{
  "continue": true,
  "stopReason": "Security policy violation",
  "systemMessage": "Unit tests failed"
}

"""

# Exit Codes
# 0 = Success: parse stdout as JSON
# 2 = Blocking error: stop processing and show error to model
# Other = Non-blocking warning: show warning to user, continue processing


# Pre-Tool Input:
"""
{
  "tool_name": "editFiles",
  "tool_input": { "files": ["src/main.ts"] },
  "tool_use_id": "tool-123"
}
"""

# Pre-Tool Output:
"""
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by policy",
    "updatedInput": { "files": ["src/safe.ts"] },
    "additionalContext": "User has read-only access to production files"
  }
}
"""
def pre_tool_use_hook(input_data: dict, session_id: str, policy: CanopyPolicy) -> int:
    tool_name: str = input_data.get("tool_name", "")
    if policy.is_allowed(tool_name):
        # Tool is allowed, continue processing
        print(json.dumps({"continue": True}), file=sys.stdout)
        return 0
    else:
        # Tool is not allowed, block processing
        output = {
            "continue": True,
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Tool '{tool_name}' is blocked by policy.",
        }
        print(json.dumps(output), file=sys.stdout)
        return 2


def handle_hook(policy: CanopyPolicy) -> int:
    # Read the JSON input from stdin
    input_data = json.load(sys.stdin)

    # Process the hook event
    session_id = input_data.get("sessionId")
    hook_event_name = input_data.get("hookEventName")

    if hook_event_name == "PreToolUse":
        return pre_tool_use_hook(input_data, session_id, policy)
    else:
        # Unknown hook event, continue processing
        print(json.dumps({"continue": True}), file=sys.stdout)
        return 0