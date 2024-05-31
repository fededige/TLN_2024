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
        if not self.complete:
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
            if not polarity:
                self.complete = True
                return True
            return False
        else:
            for x in self.question.get_keywords():
                # print(x, keyword)
                if self.remove_article(keyword.lower()) == x.lower():
                    # print("CORRECT!!!", keyword)
                    self.current_keywords.add(x)
                    self.check_frame_complete()
                    return True
            return False
            # if self.remove_article(keyword.lower()) in [x.lower() for x in self.question.get_keywords()]:
            #     print("CORRECT!!!", keyword)
            #     self.current_keywords.add(self.remove_article(keyword.lower()))
            #     self.check_frame_complete()
            #     return True
            # else:
            #     return False

    def check_already_said(self, keyword):
        return keyword.lower() in self.current_keywords

    def remove_article(self, keyword):
        if 'a' in keyword.lower().split(' '):
            keyword = keyword.replace('a ', '')
        if 'the' in keyword.lower().split(' '):
            keyword = keyword.replace('the ', '')
        return keyword

if __name__ == "__main__":
    frame = Frame()
    print(frame.remove_article("a golden tree"))