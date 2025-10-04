
class CanopyPolicy():
    def __init__(self, policy: dict):
        self.policy = policy

    def is_allowed(self, tool_call: str) -> bool:
        flows = self.policy.get("flows", {})
        for flow_name, flow in flows.items():
            allowed_calls = flow.get("allowed_calls", [])
            if tool_call in allowed_calls:
                return True

        return False