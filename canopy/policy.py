
import re


class CanopyPolicy():
    def __init__(self, policy: dict):
        self.policy = policy
        self.selected_policy = "default"
        self.seen_tools = set()

    def is_allowed(self, tool_call: str) -> bool:
        self.seen_tools.add(tool_call)

        flows = self.policy.get("flows", {})
        for flow_name, flow in flows.items():
            if flow_name == self.selected_policy:
                allowed_calls = flow.get("allowed_calls", [])
                
                for call in self.seen_tools:
                    allowed = False
                    for allowed_call in allowed_calls:
                        regex_call = re.compile(allowed_call)
                        if regex_call.fullmatch(call):
                            allowed = True
                            break
                    
                    if not allowed:
                        return False
                    
                return True

        return False