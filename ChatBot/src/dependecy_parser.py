import spacy


class DependecyParser:
    def __init__(self, text):
        self.text = text
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = self.nlp(text)

    def get_tokens(self):
        return set([chunk.text for chunk in self.doc.noun_chunks])

    def get_test(self):
        chunks = set([chunk.text for chunk in self.doc.noun_chunks])
        res = chunks.copy()
        print(chunks)
        entities = set([entity.text for entity in self.doc.ents])
        print(entities)
        for chunk in chunks:
            for entity in entities:
                if chunk not in entity:
                    res.add(entity)
        if len(chunks) == 0:
            return entities
        return res

    def get_topic(self):
        subjects = []
        sentence = next(self.doc.sents)
        for word in sentence:
            if word.dep_ == "nsubj":
                subjects.append(word)

        for token in self.get_tokens():
            for subject in subjects:
                if str(subject) in token:
                    return self.remove_article(token)
        return None

    def remove_article(self, token):
        t = ""
        for el in self.doc:
            if str(el) in token and el.pos_ == "DET":
                t = token.replace(el.text, "")
        return t.strip()

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
    parser = DependecyParser("The 6 phenomena are Turns,Speech acts,Grounding,Dialogue structure,Initiative,Implicature")
    print(parser.get_test())


