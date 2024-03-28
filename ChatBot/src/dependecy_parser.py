import spacy

class DependecyParser:
    def __init__(self, text):
        self.text = text
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = self.nlp(text)

    def get_tokens(self):
        tokens = set([chunk.text for chunk in self.doc.noun_chunks])
        # print(tokens)
        return tokens

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

if __name__ == "__main__":
    keywords_answer = DependecyParser("We're programming a dialogue system able to ask you questions about the exam. This exam is called Natural Language Processing")
    keywords_answer.get_tokens()