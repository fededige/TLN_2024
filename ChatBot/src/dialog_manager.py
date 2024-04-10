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

    def print_danny(self, text):
        print("Prof. Danny: ", text)

    def greetings(self):
        text = "Welcome to TLN exam. I will ask you some questions about the first part of TLN course. Let's start!"
        self.print_danny(text)

    def clean_answer(self, answer):
        answer.strip()
        if answer[len(answer) - 1] != '.':
            answer += '.'
        return answer

    def compute_score(self, total_score, total_weight):
        final_score = total_score / total_weight
        return round(final_score)

    def exam(self):
        self.greetings()
        total_score = 0
        weight = [1, 2, 1]
        total_weight = 0
        while self.num_questions < 4:
            question = self.generate_question()
            if question is None:
                print("No question")
                return
            self.frame.add_question(question)
            self.print_danny(question.get_text())
            answer = self.clean_answer(input("User: "))
            total_score += self.analyze_user_answer(question, answer) * weight[question.get_type() - 1]
            total_weight += weight[question.get_type() - 1]
            self.num_questions += 1

        final_score = self.compute_score(total_score, total_weight)
        self.print_danny(f"score: {round(final_score)}")
        return

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

        return self.check_answer(answer_tokens, question)

    def check_answer(self, tokens, question):
        new_keyword_count = 0
        g = generator.Generator()
        max_score = 30
        res = 0
        for token in tokens:
            if self.frame.add_keyword(token):
                new_keyword_count += 1

        parser_question = dependecy_parser.DependecyParser(question.get_text())
        question_topic = parser_question.get_topic()
        if self.frame.check_frame_complete():
            a = g.generate_answer(question_topic, "positive", question.get_type())
            self.print_danny(a)
            res = max_score
        elif new_keyword_count > 0:
            a = g.generate_answer(question_topic, "mild", question.get_type())
            self.print_danny(a)
            res = (max_score * new_keyword_count) / len(question.get_keywords())
        else:
            a = g.generate_answer(question_topic, "negative", question.get_type())
            self.print_danny(a)
        return res


if __name__ == '__main__':
    dialog_manager = DialogManager()
    dialog_manager.exam()
