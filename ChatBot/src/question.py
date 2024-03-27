class Question:
    def __init__(self, text, keywords, type):
        self.text = text
        self.keywords = keywords
        self.type = type

    def get_keywords(self):
        return self.keywords

    def get_text(self):
        return self.text

    def get_type(self):
        return self.type