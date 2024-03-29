import simplenlg


class Generator:
    def __init__(self):
        self.lexicon = simplenlg.Lexicon.getDefaultLexicon()
        self.nlgFactory = simplenlg.NLGFactory(self.lexicon)
        self.realiser = simplenlg.Realiser(self.lexicon)

    def positive_answer_list(self, verb, obj, subject, sbj_modifier, obj_modifier, verb_modifier, comment, negative=None):
        p = self.nlgFactory.createClause()
        sbj = self.nlgFactory.createNounPhrase(subject)
        verb = self.nlgFactory.createVerbPhrase(verb)
        obj = self.nlgFactory.createNounPhrase(obj)
        if sbj_modifier is not None:
            sbj.addModifier(sbj_modifier)
        if obj_modifier is not None:
            obj.addPreModifier(obj_modifier)
        if verb_modifier is not None:
            obj.addModifier(verb_modifier)
        p.setSubject(sbj)
        p.setVerb(verb)
        p.setObject(obj)
        if negative is not None:
            p.setNegated(True)
        p.setFeature(featureName=simplenlg.Feature.TENSE, featureValue=simplenlg.Tense.PAST)

        p2 = self.nlgFactory.createClause(comment)

        s1 = self.nlgFactory.createSentence(p)
        s2 = self.nlgFactory.createSentence(p2)

        par1 = self.nlgFactory.createParagraph([s2, s1])

        output = self.realiser.realise(par1).getRealisation()
        print(output)
        return output

    # def negative_answer_list(self):
    #     p = self.nlgFactory.createClause()
    #     sbj = self.nlgFactory.createNounPhrase(subject)
    #     verb = self.nlgFactory.createVerbPhrase(verb)
    #     obj = self.nlgFactory.createNounPhrase(obj)


# domanda di tipo 3 (lista) positive/quasi positive
# Well done, you said all the 7 phases correctly
# Wow, your answer is completely correct!
# Good job, you said some of the correct phases

# domanda di tipo 3 (lista) completamente negative
# Comment, non hai scritto nessuna delle fasi corrette
# Comment, hai sbagliato tutte le fasi inserite
# Comment, le fasi inserite sono errate
# Be careful, you didn't enter any of the correct phases.

if __name__ == "__main__":
    g = Generator()
    g.positive_answer_list("say", "the 7 phases", "you", None, "correctly", None, "Well done")
    g.positive_answer_list("be", "correct", "your answer", None, "completely", None, "Wow")
    g.positive_answer_list("say", "phases", "you", None, "some of the", None, "Good job")

    g.positive_answer_list("enter", "phases", "you", None, "the correct", None, "Be careful", True)
