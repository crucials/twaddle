class DetailedError(Exception):
    def __init__(self, name: str, explanation: str):
        super().__init__(f"{name}: {explanation}")
        self.name = name
        self.explanation = explanation
