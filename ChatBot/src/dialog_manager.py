import frame
import random
import questions_pool

class DialogManager:
    def __init__(self):
        self.num_questions = 0
        self.wrong_questions = 0
        self.memory = []
        self.frame = frame.Frame()

    def greetings(self):
        print("Prof. Danny: Welcome to TLN exam. I will ask you some questions about the first part of TLN course.")

    def start_exam(self):
        self.greetings()
        question = random.choice(questions_pool.questions)
        self.frame.add_question(question)

        while self.num_questions < 4 or not self.frame.complete:
            # genera domanda
            self.num_questions += 1
        return


if __name__ == '__main__':
    dialog_manager = DialogManager()
    dialog_manager.start_exam()