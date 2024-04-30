import random
import simplenlg
from sentences_pool import *


class Generator:
    def __init__(self):
        self.lexicon = simplenlg.Lexicon.getDefaultLexicon()
        self.nlgFactory = simplenlg.NLGFactory(self.lexicon)
        self.realiser = simplenlg.Realiser(self.lexicon)

    def generate_answer_with_params(self, verb, obj, subj, sbj_modifier, obj_modifier, verb_modifier, comment,
                                    negative=None, past=None):
        p = self.nlgFactory.createClause()
        if sbj_modifier is not None:
            subj = self.nlgFactory.createNounPhrase(subj)
            subj.addModifier(sbj_modifier)
        if obj_modifier is not None:
            obj = self.nlgFactory.createNounPhrase(obj)
            obj.addPreModifier(obj_modifier)
        if verb_modifier is not None:
            verb = self.nlgFactory.createVerbPhrase(verb)
            verb.addModifier(verb_modifier)
        p.setSubject(subj)
        p.setVerb(verb)
        p.setObject(obj)
        if negative is not None:
            p.setFeature(featureName=simplenlg.Feature.NEGATED, featureValue=True)
        if past is not None:
            p.setFeature(featureName=simplenlg.Feature.TENSE, featureValue=simplenlg.Tense.PAST)

        p2 = self.nlgFactory.createClause(comment)

        s1 = self.nlgFactory.createSentence(p)
        s2 = self.nlgFactory.createSentence(p2)

        r = random.random()
        if r < 0.35:
            par1 = self.nlgFactory.createParagraph([s2, s1])
        elif r < 0.6:
            par1 = self.nlgFactory.createParagraph([s1, s2])
        elif r < 0.55:
            if negative is None:
                par1 = self.nlgFactory.createParagraph([s1])
            else:
                par1 = self.nlgFactory.createParagraph([s2, s1])
        else:
            par1 = self.nlgFactory.createParagraph([s1, s2])

        output = self.realiser.realise(par1).getRealisation()
        return output

    def generate_answer(self, topic, positivity, q_type):
        answer = ""
        if q_type == 3:
            if positivity == "positive":
                answer = self.generate_answer_with_params(random.choice(verbs_first_type), topic, subject, None,
                                                          random.choice(positive_obj_modifiers), None,
                                                          random.choice(comment_list[0]), past=True)
            elif positivity == "negative":
                answer = self.generate_answer_with_params(random.choice(verbs_first_type), topic, subject, None,
                                                          random.choice(negative_obj_modifiers), None,
                                                          random.choice(comment_list[1]), past=True)
            elif positivity == "mild":
                answer = self.generate_answer_with_params(random.choice(verbs_first_type), topic, subject, None,
                                                          random.choice(mild_obj_modifiers), None,
                                                          random.choice(comment_list[2]), past=True)
        elif q_type == 2 or q_type == 1 or q_type == 4 or q_type == 5:
            if positivity == "positive":
                answer = self.generate_answer_with_params(random.choice(verbs_second_type), topic, subject, None,
                                                          random.choice(obj_modifiers_second_type), None,
                                                          random.choice(comment_list[0]))
            elif positivity == "negative":
                answer = self.generate_answer_with_params(random.choice(verbs_second_type), topic, subject, None,
                                                          random.choice(obj_modifiers_second_type), None,
                                                          random.choice(comment_list[1]), True)
            elif positivity == "mild":
                answer = self.generate_answer_with_params(random.choice(mild_verbs_second_type), obj_second_type,
                                                          subject, None,
                                                          random.choice(mild_obj_modifiers_second_type), None,
                                                          random.choice(comment_list[2]))
        return answer

    def generate_result(self, score, positivity):
        if positivity == "extra-positive":
            return self.generate_final_comment(score, random.choice(obj_final_comment), random.choice(final_comment_list[0]))
        elif positivity == "positive":
            return self.generate_final_comment(score, random.choice(obj_final_comment), random.choice(final_comment_list[1]))
        elif positivity == "mild":
            return self.generate_final_comment(score, random.choice(obj_final_comment), random.choice(final_comment_list[2]))
        elif positivity == "negative":
            return self.generate_final_comment(score, random.choice(obj_final_comment), random.choice(final_comment_list[3]))

    def generate_final_comment(self, score, obj, comment):
        comment_clause = self.nlgFactory.createClause(comment)
        comment_sentence = self.nlgFactory.createSentence(comment_clause)
        if score > 18:
            score_clause = self.nlgFactory.createClause(
                "Your " + obj + " is " + ("30L" if score > 30 else str(score)))
            score_sentence = self.nlgFactory.createSentence(score_clause)
        else:
            score_clause = self.nlgFactory.createClause("You failed the exam")
            score_sentence = self.nlgFactory.createSentence(score_clause)

        r = random.random()
        if r < 0.5:
            final_comment = self.nlgFactory.createParagraph([comment_sentence, score_sentence])
        else:
            final_comment = self.nlgFactory.createParagraph([score_sentence, comment_sentence])

        output = self.realiser.realise(final_comment).getRealisation()
        return output

    def generate_question(self, keywords, topic):
        return ""

if __name__ == "__main__":
    g = Generator()
    # g.generate_answer_with_params("say", "the 7 phases", "you", None, "correctly", None, "Well done")
    # g.generate_answer_with_params("write", "answer", "you", None, "the correct", None, "Wow")
    # g.generate_answer_with_params("say", "phases", "you", None, "some of the", None, "Good job")
    # g.generate_answer_with_params("enter", "phases", "you", None, "the correct", None, "Be careful", True)
    # g.generate_answer_with_params(random.choice(verbs_first_type), "NLG symbolic phases", "you", None,
    #                               random.choice(positive_obj_modifiers), None, random.choice(comment_list[0]))

obj_final_comment = ["score", "mark", "grade", "result", "evaluation"]
final_comment_list = [
    [
        "Congratulations! You've demonstrated a great understanding of the topics covered.",
        "Excellent work! You've shown a deep knowledge of the subject.",
        "Well done! You've exceeded expectations with your dedication and preparation.",
        "You've shown great dedication to your studies, and it's evident in your results.",
        "You've demonstrated a strong mastery of the concepts, congratulations!",
        "It's clear you've worked hard to achieve this result, congratulations!",
        "You've achieved an excellent score thanks to your precision and attention to detail.",
        "Keep it up! Your commitment and passion for the subject are evident."
    ],
    [
        "You're on the right track, but there's still room for improvement.",
        "You've done very well, showing proficiency in most areas of the exam.",
        "Your result reflects a high level of competency, with only minor areas for improvement.",
        "You're close to reaching the top level, showcasing a thorough understanding of the concepts.",
        "Your score indicates a very good understanding of the material, with just a few areas that could be "
        "strengthened."
    ],
    [
        "There's room for improvement in your understanding of the material.",
        "Your preparation could have been more extensive.",
        "Your result reflects the need for additional effort and focus.",
        "With a bit more practice, you'll grasp the concepts better.",
        "Your effort is appreciated, but there are areas that need refinement.",
        "It's clear you're making progress, but there's still work to be done.",
        "Your performance shows potential, keep working at it.",
        "There's potential for improvement with more focused study.",
        "Your understanding is developing, keep up the good work.",
    ],
    [
        "You might need to review some concepts more closely.",
        "There were some gaps in your understanding of the subject.",
        "You'll need to work on mastering the concepts further.",
        "There were some inaccuracies in your answers that need addressing.",
        "It's important to demonstrate more commitment and passion for the subject."
        "Consider reviewing the material to strengthen your understanding.",
        "Don't get discouraged, learning takes time and effort."
    ]
]