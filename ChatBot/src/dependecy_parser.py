import spacy


class DependecyParser:
    def __init__(self, text):
        self.text = text
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = self.nlp(text)

    # def get_tokens(self):
    #     chunks = set([chunk.text for chunk in self.doc.noun_chunks])
    #     res = chunks.copy()
    #     entities = set([entity.text for entity in self.doc.ents])
    #     for chunk in chunks:
    #         for entity in entities:
    #             if len(chunk) < len(entity):
    #                 if chunk not in entity:
    #                     res.add(entity)
    #             else:
    #                 if entity not in chunk:
    #                     res.add(chunk)
    #     if len(chunks) == 0:
    #         return entities
    #     return res

    def get_tokens(self):
        chunks = set([chunk.text for chunk in self.doc.noun_chunks])
        res = chunks.copy()
        entities = set([entity.text for entity in self.doc.ents])
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
        t = str(token)
        for el in self.doc:
            if str(el) in token and el.pos_ == "DET":
                t = token.replace(el.text, "", 1)
        return t.strip()


if __name__ == "__main__":
    parser = DependecyParser("the answer is: seven")
    print("test get_tokens(): ", parser.get_tokens())
