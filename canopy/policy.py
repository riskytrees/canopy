
import re


class CanopyPolicy():
    def __init__(self, policy: dict):
        self.policy = policy

    def is_allowed(self, tool_call: str) -> bool:

        flows = self.policy.get("flows", {})
        for flow_name, flow in flows.items():
            allowed_calls = flow.get("allowed_calls", [])
            
            allowed = False
            for allowed_call in allowed_calls:
                regex_call = re.compile(allowed_call)
                if regex_call.fullmatch(tool_call):
                    allowed = True
                    break
            
            if not allowed:
                return False
                
            return True

        return False