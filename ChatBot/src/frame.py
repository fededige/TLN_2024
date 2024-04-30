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

    def add_keyword(self, keyword, polarity=False):
        if self.question is None:
            return False
        if self.question.get_type() == 4:
            if polarity:
                self.complete = True
                return True
            return False
        elif self.question.get_type() == 5:
            if polarity:
                self.complete = True
                return True
            return False
        else:
            if keyword.lower() in [x.lower() for x in self.question.get_keywords()]:
                self.current_keywords.add(keyword.lower())
                self.check_frame_complete()
                return True
            else:
                return False

    def check_already_said(self, keyword):
        return keyword.lower() in self.current_keywords
