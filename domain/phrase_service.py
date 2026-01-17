class PhraseService:
    def __init__(self, phrase_repository):
        self.phrase_repo = phrase_repository

    def load_phrase(self):
        self.phrase_repo.load_random_phrase()

