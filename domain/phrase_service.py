class PhraseService:
    def __init__(self, phrase_repository):
        self.phrase_repo = phrase_repository

    def load_phrase(self):
        self.phrase_repo.load_random_phrase()

    def get_phrase(self):
        return self.phrase_repo.get_phrase()

    def get_phrases(self):
        return self.phrase_repo.get_phrases()
    
    def delete_selected_phrase(self,selected_phrase):
        self.phrase_repo.delete_selected_phrase(selected_phrase)