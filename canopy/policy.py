
class CanopyPolicy():
    def __init__(self, policy: dict):
        self.policy = policy

    def is_allowed(self, tool_call: str) -> bool:
        return True