class Question:
    def __init__(self, text, key_words):
        self.text = text
        self.key_words = key_words

    def get_keywords(self):
        return self.key_words

    def get_text(self):
        return self.text
