class TranscriberNotInitializedError(Exception):
    def __init__(self):
        super().__init__(
            "speech transcriber is not initialized, probably because " + "of some error"
        )
