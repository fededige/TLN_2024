import spacy

class DependecyParser:
    def __init__(self, text):
        self.text = text
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = self.nlp(text)




# # Load English tokenizer, tagger, parser and NER
# nlp = spacy.load("en_core_web_sm")
#
# # Process whole documents
# text = ("the phases are Pluto, Minnie, Micky Mouse")
# doc = nlp(text)
#
# # Analyze syntax
# print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
# print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
#
# # Find named entities, phrases and concepts
# for entity in doc.ents:
#     print(entity.text, entity.label_)