import sys
import json

from canopy_mcp.policy import CanopyPolicy
import os


# VSCode Common Input:

"""
{
  "timestamp": "2026-02-09T10:30:00.000Z",
  "cwd": "/path/to/workspace",
  "sessionId": "session-identifier",
  "hookEventName": "PreToolUse",
  "transcript_path": "/path/to/transcript.json"
}
"""

# Gemini Common Input:

"""
{
  "session_id": string,      // Unique ID for the current session
  "transcript_path": string, // Absolute path to session transcript JSON
  "cwd": string,             // Current working directory
  "hook_event_name": string, // The firing event (e.g. "BeforeTool")
  "timestamp": string        // ISO 8601 execution time
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

def load_policy_state(policy: CanopyPolicy, session_id) -> CanopyPolicy:
    try:
        with open(f"/tmp/.canopy/.sessions/{session_id}.json", "r") as f:
            state = json.load(f)
            policy.picked_flow = state.get("picked_flow")
            policy.seen_allowed_flows = set(state.get("seen_allowed_flows", []))
    except FileNotFoundError:
        # No previous state found, continue with current policy
        pass
    return policy

# Stores important parts of CanopyPolicy in a session-specific file for later retrieval.
# This allows the policy to be reloaded in subsequent hook calls for the same session.
# Stored in ~/.canopy/.sessions/{session_id}.json
def save_policy_state(session_id, policy: CanopyPolicy) -> None:
  session_dir = os.path.expanduser("/tmp/.canopy/.sessions")
  os.makedirs(session_dir, exist_ok=True)
  session_file = os.path.join(session_dir, f"{session_id}.json")
  with open(session_file, "w") as f:
    json.dump({
      "picked_flow": policy.picked_flow,
      "seen_allowed_flows": list(policy.seen_allowed_flows)
    }, f)



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
    session_id = input_data.get("sessionId", input_data.get("session_id"))
    hook_event_name = input_data.get("hookEventName", input_data.get("hook_event_name"))

    policy = load_policy_state(policy, session_id)

    resp_code = None

    if hook_event_name == "PreToolUse":
        resp_code = pre_tool_use_hook(input_data, session_id, policy)
    else:
        # Unknown hook event, continue processing
        print(json.dumps({"continue": True}), file=sys.stdout)
        resp_code = 0

    save_policy_state(session_id, policy)
    return resp_code