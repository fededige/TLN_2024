import simplenlg

lexicon = simplenlg.Lexicon.getDefaultLexicon()
nlgFactory = simplenlg.NLGFactory(lexicon)
realiser = simplenlg.Realiser(lexicon)

s1 = nlgFactory.createSentence("dog happy bone")

output = realiser.realiseSentence(s1)
print(output)

p = nlgFactory.createClause()
p.setSubject("dog")
p.setVerb("eat")
p.setObject("the bone")

p.setFeature(featureName=simplenlg.Feature.TENSE, featureValue=simplenlg.Tense.PAST)

output = realiser.realiseSentence(p)
print(output)