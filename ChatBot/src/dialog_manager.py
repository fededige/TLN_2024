import frame
import random
import questions_pool
import dependency_parser
import generator
import time
import sys


class DialogManager:
    def __init__(self):
        self.num_questions = 0
        self.wrong_questions = 0
        self.memory_questions = []
        self.memory_answers = []
        self.frame = frame.Frame()
        self.g = generator.Generator()
        self.dependency_parser = dependency_parser.DependencyParser()

    def print_danny(self, text):
        text = text.strip()
        print(f"Prof. Danny: {text}")

    def greetings(self):
        text = "Welcome to TLN exam. I will ask you some questions about the first part of TLN course. Let's start!"
        self.print_danny(text)

    def closing(self, final_comment):
        sys.stdout.write("Prof. Danny: Congrats, you finished the exam! Wait for the result")
        i = 0
        while i < 3:
            time.sleep(1.5)
            sys.stdout.write(".")
            sys.stdout.flush()
            i += 1
        sys.stdout.write("\n")
        time.sleep(1)
        self.print_danny(final_comment)

    def clean_answer(self, answer):
        answer = answer.strip()
        if answer[len(answer) - 1] != '.':
            answer += '.'
        return answer

    def compute_score(self, total_score, total_weight):
        final_score = total_score / total_weight
        return round(final_score)

    def exam(self):
        self.greetings()
        total_score = 0
        weight = [1, 2, 1, 1, 1]
        total_weight = 0
        while self.num_questions < 4:
            question = self.generate_question()
            question_text = self.change_question(question)
            if question is None:
                return
            self.frame.add_question(question)
            self.print_danny(question_text)
            answer = self.clean_answer(input("User: "))
            answer_tokens = self.analyze_user_answer(answer)
            temp_score, question_complete = self.check_answer(answer_tokens, question)
            if not question_complete and question.get_type() != 1 and question.get_type() != 4 and question.get_type() != 5:
                self.print_danny(f"Do you want to add something else about {self.dependency_parser.get_topic()}?")
                answer = self.clean_answer(input("User: "))
                answer_tokens = self.analyze_user_answer(answer)
                temp_score += self.check_answer(answer_tokens, question)[0]
                self.num_questions += 0.5
            if question_complete:
                total_score += temp_score * weight[question.get_type() - 1]
            else:
                total_score += temp_score * weight[question.get_type() - 1] * 0.85
            total_weight += weight[question.get_type() - 1]
            self.num_questions += 1

        final_score = self.compute_score(total_score, total_weight)
        final_comment = self.g.generate_result(round(final_score),
                                               "extra-positive" if final_score > 27 else (
                                                   "positive" if final_score > 23 else (
                                                       "mild" if final_score > 18 else "negative")))
        self.closing(final_comment)
        return

    def change_question(self, question):
        rnd = random.randint(0, 100)

        if rnd < 20:
            self.dependency_parser.set_text(question.get_text())
            question.set_type(4)
            self.g.generate_question(question.get_keywords(), self.dependency_parser.get_topic())
        elif 20 < rnd < 40:
            self.dependency_parser.set_text(question.get_text())
            question.set_type(5)
            self.g.generate_question(question.get_false_keywords(), self.dependency_parser.get_topic())
        else:
            return question.get_text()

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

    def analyze_user_answer(self, answer):
        new_answer = ""
        answer_tokens = []
        a = answer[:len(answer) - 1]
        sentences = a.split('.') if '.' in a else answer
        for sentence in sentences:
            if not dependency_parser.get_negativity(sentence):
                new_answer += sentence
        if new_answer != "":
            self.dependency_parser.set_text(self.clean_answer(new_answer))
            answer_tokens = self.dependency_parser.get_tokens()
        return answer_tokens

    def check_answer(self, tokens, question):
        new_keyword_count = 0
        max_score = 32
        res = 0
        complete = False
        flag_already_said = False
        already_said = []
        if question.get_type() < 4:
            for token in tokens:
                flag_already_said = self.frame.check_already_said(token)
                if flag_already_said:
                    already_said.append(token)
                elif self.frame.add_keyword(token):
                    new_keyword_count += 1
        else:
            if self.frame.add_keyword(None, self.dependency_parser.get_polarity()):
                new_keyword_count += 1
        self.dependency_parser.set_text(question.get_text())
        question_topic = self.dependency_parser.get_topic()

        if self.frame.check_frame_complete():
            a = self.g.generate_answer(question_topic, "positive", question.get_type())
            self.print_danny(a)
            res = max_score
            complete = True
        elif new_keyword_count > 0:
            a = self.g.generate_answer(question_topic, "mild", question.get_type())
            self.print_danny(a)
            res = (max_score * new_keyword_count) / len(question.get_keywords())
        else:
            if flag_already_said:
                self.print_danny("You already said all this thing. "
                                 "You lost your chance, next time try adding something new.")
            else:
                a = self.g.generate_answer(question_topic, "negative", question.get_type())
                self.print_danny(a)
        return res, complete


if __name__ == '__main__':
    dialog_manager = DialogManager()
    dialog_manager.exam()
