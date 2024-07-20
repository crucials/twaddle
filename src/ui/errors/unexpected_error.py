from ui.errors.detailed_error import DetailedError


class UnexpectedError(DetailedError):
    def __init__(self, error: Exception | None = None):
        explanation = "dont know what that is"

        if error:
            explanation += f". more info: {error.__str__()}"

        super().__init__("unexpected-error", explanation)
