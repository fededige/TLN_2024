class Frame:
    def __init__(self):
        self.question = None
        self.current_keywords = set()
        self.complete = False

    def add_question(self, question):
        self.question = question
        self.complete = False
        self.current_keywords = set()

    def check_frame_complete(self):
        if self.question is None:
            return False
        keywords = set(self.question.get_keywords())
        if self.current_keywords == keywords:
            self.complete = True
        return self.complete

    def add_keyword(self, keyword):
        if self.question is None:
            return False
        if keyword.lower() in [x.lower() for x in self.question.get_keywords()]:
            self.current_keywords.add(keyword.lower())
            self.check_frame_complete()
        else:
            return False
        return True
