
import re
import sys


class CanopyPolicy():
    def __init__(self, policy: dict):
        self.policy = policy

    def is_allowed(self, tool_call: str) -> bool:

        flows = self.policy.get("flows", {})
        for flow_name, flow in flows.items():
            allowed_calls = flow.get("allowed_calls", [])

            if not flow.get("disabled", False):
                allowed = False
                for allowed_call in allowed_calls:
                    print(f"Checking {tool_call} against {allowed_call}", file=sys.stderr)
                    regex_call = re.compile(allowed_call)
                    if regex_call.fullmatch(tool_call):
                        allowed = True
                        break
                
                if allowed:
                    return True
                
        return False
