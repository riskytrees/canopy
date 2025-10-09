
import re
import sys
import tomllib


class CanopyPolicy():
    def __init__(self, policy_path: str):
        self.policy_path = policy_path
        self.policy = self.load_policy(policy_path)

    def load_policy(self, path: str) -> dict:
        with open(path, "rb") as f:
            return tomllib.load(f)

    def is_allowed(self, tool_call: str) -> bool:
        self.policy = self.load_policy(self.policy_path)

        flows = self.policy.get("flows", {})
        for _flow_name, flow in flows.items():
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
