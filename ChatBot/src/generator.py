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
            obj = self.nlgFactory.createNounPhrase("the " + obj)
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
        else:
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
            return self.generate_final_comment(score, random.choice(obj_final_comment),
                                               random.choice(final_comment_list[0]))
        elif positivity == "positive":
            return self.generate_final_comment(score, random.choice(obj_final_comment),
                                               random.choice(final_comment_list[1]))
        elif positivity == "mild":
            return self.generate_final_comment(score, random.choice(obj_final_comment),
                                               random.choice(final_comment_list[2]))
        elif positivity == "negative":
            return self.generate_final_comment(score, random.choice(obj_final_comment),
                                               random.choice(final_comment_list[3]))

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

    def generate_question(self, keywords, topic, type):
        keyword = self.nlgFactory.createNounPhrase(random.choice(keywords))
        topic = self.nlgFactory.createNounPhrase("the", topic)
        if type == 3:
            p = self.nlgFactory.createPrepositionPhrase(random.choice(tricky_questions))
            p.addComplement(topic)
            s2 = self.nlgFactory.createClause(keyword, "be")
            s2.addPostModifier(p)
        else:
            s2 = self.nlgFactory.createClause(topic, "be")
            s2.addPostModifier(keyword)
        s2.setFeature(simplenlg.Feature.INTERROGATIVE_TYPE, simplenlg.InterrogativeType.YES_NO)
        return self.realiser.realise(s2).getRealisation().capitalize() + '?'
# Is the topic keyword?


if __name__ == "__main__":
    g = Generator()
    print(g.generate_question(["generative"], "hmm model", 1))
    # for i in range(5):
    #     print(g.generate_question(["a", "b", "c"], "topic"))
    # g.generate_answer_with_params("say", "the 7 phases", "you", None, "correctly", None, "Well done")
    # g.generate_answer_with_params("write", "answer", "you", None, "the correct", None, "Wow")
    # g.generate_answer_with_params("say", "phases", "you", None, "some of the", None, "Good job")
    # g.generate_answer_with_params("enter", "phases", "you", None, "the correct", None, "Be careful", True)
    # g.generate_answer_with_params(random.choice(verbs_first_type), "NLG symbolic phases", "you", None,
    #                               random.choice(positive_obj_modifiers), None, random.choice(comment_list[0]))


