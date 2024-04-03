import random

import simplenlg


class Generator:
    def __init__(self):
        self.lexicon = simplenlg.Lexicon.getDefaultLexicon()
        self.nlgFactory = simplenlg.NLGFactory(self.lexicon)
        self.realiser = simplenlg.Realiser(self.lexicon)

    def generate_answer(self, verb, obj, subj, sbj_modifier, obj_modifier, verb_modifier, comment, negative=None):
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
        p.setFeature(featureName=simplenlg.Feature.TENSE, featureValue=simplenlg.Tense.PAST)

        p2 = self.nlgFactory.createClause(comment)

        s1 = self.nlgFactory.createSentence(p)
        s2 = self.nlgFactory.createSentence(p2)

        r = random.random()
        if r < 0.25:
            par1 = self.nlgFactory.createParagraph([s2, s1])
        elif 0.25 < r < 0.5:
            par1 = self.nlgFactory.createParagraph([s1, s2])
        elif 0.5 < r < 0.75:
            if negative is None:
                par1 = self.nlgFactory.createParagraph([s1])
            else:
                par1 = self.nlgFactory.createParagraph([s2, s1])
        else:
            if negative is None:
                par1 = self.nlgFactory.createParagraph([s2])
            else:
                par1 = self.nlgFactory.createParagraph([s1, s2])

        output = self.realiser.realise(par1).getRealisation()
        print(output)
        return output


# "You've mentioned several of the key phenomena."
# "You've identified some important aspects of human dialogue."
# "You've included a few of the symbolic phases."
# "You've mentioned some of the tasks involved in NLG."

if __name__ == "__main__":
    g = Generator()
    g.generate_answer("say", "the 7 phases", "you", None, "correctly", None, "Well done")
    g.generate_answer("write", "answer", "you", None, "the correct", None, "Wow")
    g.generate_answer("say", "phases", "you", None, "some of the", None, "Good job")
    g.generate_answer("enter", "phases", "you", None, "the correct", None, "Be careful", True)

comment_list = [
    [
        "Well done",
        "Correct",
        "Excellent response",
        "Great Job",
        "Brilliant",
        "Excellent response",
        "Exactly",
        "Right",
        "Precise"
    ],
    [
        "Incorrect",
        "Try again",
        "Not quite there",
        "Wrong answer",
        "Not correct",
        "That's not it",
        "Incorrect response",
        "Not quite what we're looking for",
        "Try a different approach",
    ],
    [
        "Close, but not there yet",
        "Almost",
        "You're on the right track",
        "A good attempt",
        "Not bad",
        "Keep trying",
        "You're getting warmer",
        "Nice try",
        "Getting closer"
    ]
]
