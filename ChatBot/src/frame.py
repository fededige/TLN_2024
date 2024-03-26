class Frame:
    def __init__(self):
        self.question = None
        self.current_keywords = set()
        self.complete = False

    def add_question(self, question):
        self.question = question

    def check_frame_complete(self):
        if self.question is None:
            return False
        keywords = set(self.question.get_keywords())
        if self.current_keywords == keywords:
            self.complete = True
        return self.complete

    # add correct kewords to the frame and return wrong ones
    def add_keyword(self, keywords):
        if self.question is None:
            return False
        keywords = set(keywords)
        wrong_keywords = set()
        for keyword in keywords:
            if keyword.casefold() in self.question.get_keywords():
                self.current_keywords.add(keyword.casefold())
            else:
                wrong_keywords.add(keyword.casefold())
        return wrong_keywords
