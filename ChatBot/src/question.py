class Question:
    def __init__(self, text, keywords, type, false_keywords=None):
        self.text = text
        self.keywords = keywords
        self.type = type
        self.false_keywords = false_keywords

    def get_keywords(self):
        return self.keywords

    def get_text(self):
        return self.text

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_false_keywords(self):
        return self.false_keywords
