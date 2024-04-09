import frame
import random
import questions_pool
import dependecy_parser
import generator


class DialogManager:
    def __init__(self):
        self.num_questions = 0
        self.wrong_questions = 0
        self.memory_questions = []
        self.memory_answers = []
        self.frame = frame.Frame()

    def greetings(self):
        text = "Welcome to TLN exam. I will ask you some questions about the first part of TLN course. Let's start!"
        self.print_danny(text)

    def exam(self):
        self.greetings()

        while self.num_questions < 4 or not self.frame.complete:
            question = self.generate_question()
            if question is None:
                print("No question")
                return
            self.frame.add_question(question)
            self.print_danny(question.get_text())

            answer = input("User: ")
            
            self.analyze_user_answer(question, answer)
            self.num_questions += 1
        return

    def print_danny(self, text):
        print("Prof. Danny: ", text)

    def generate_question(self):
        if len(self.memory_questions) == len(questions_pool.questions):
            return None
        rnd = random.randint(0, 100)
        if rnd < 21:
            q = random.choice(questions_pool.questions_binary)
        elif rnd > 59:
            q = random.choice(questions_pool.questions_list)
        else:
            q = random.choice(questions_pool.questions_open)
        if q in self.memory_questions:
            return self.generate_question()
        self.memory_questions.append(q)
        return q

    def analyze_user_answer(self, question, answer):
        parser_answer = dependecy_parser.DependecyParser(answer)
        answer_tokens = parser_answer.get_tokens()

        self.check_answer(answer_tokens, question)

        # if question.get_type() == 1:
        #     print()
        # elif question.get_type() == 2:
        #     print()
        # else:
        #     print()

    def check_answer(self, tokens, question):
        new_keyword_count = 0
        g = generator.Generator()
        for token in tokens:
            if self.frame.add_keyword(token):
                new_keyword_count += 1
        parser_question = dependecy_parser.DependecyParser(question.get_text())
        question_topic = parser_question.get_topic()
        if self.frame.check_frame_complete():
            a = g.generate_answer(question_topic, "positive", question.get_type())
            self.print_danny(a)
        elif new_keyword_count > 0:
            a = g.generate_answer(question_topic, "mild", question.get_type())
            self.print_danny(a)
        else:
            a = g.generate_answer(question_topic, "negative", question.get_type())
            self.print_danny(a)


if __name__ == '__main__':
    dialog_manager = DialogManager()
    dialog_manager.exam()
