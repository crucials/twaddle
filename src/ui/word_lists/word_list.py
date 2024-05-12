class WordList:
    def __init__(self, name: str, path: str | None = None,
                 words: list[str] | None = None, created_by_user = False):
        """
        ### Parameters
        `path`: from where to load word list txt data (one word on one line format).
        if it's specified, `words` parameter will be ignored
        """
        self.name = name
        self.custom = created_by_user

        if path:
            with open(path) as wordsStream:
                self.words = wordsStream.read().split('\n')
        elif words:
            self.words = words
        else:
            self.words = []
