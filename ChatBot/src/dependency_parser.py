import spacy


class DependencyParser:
    def __init__(self):
        self.text = ""
        self.nlp = spacy.load("en_core_web_lg")
        self.doc = None

    def set_text(self, text):
        self.text = text
        self.doc = self.nlp(text)

    def get_tokens(self):
        chunks = set([chunk.text for chunk in self.doc.noun_chunks])
        # print(chunks)
        res = chunks.copy()
        entities = set([entity.text for entity in self.doc.ents])
        # print(entities)
        for chunk in chunks:
            for entity in entities:
                if chunk not in entity:
                    res.add(entity)
        if len(chunks) == 0:
            res = entities.copy()
        res = self.split_words(res)
        return self.clear_tokens(res)

    def clear_tokens(self, tokens):
        res = tokens.copy()
        for el in tokens:
            if ',' in el:
                res.remove(el)
                res.update([word.strip() for word in el.split(',')])
        return res

    def split_words(self, tokens):
        res = tokens.copy()
        for el in tokens:
            if ' ' in el:
                res.update([word.strip() for word in el.split(' ')])
        return res

    def get_topic(self):
        subjects = []
        sentence = next(self.doc.sents)
        topic = ""
        for word in sentence:
            if word.dep_ == "nsubj":
                subjects.append(word)
        for token in self.get_tokens():
            for subject in subjects:
                if str(subject) in token:
                    if len(token) > len(topic):
                        topic = token
        if topic == "":
            return None
        return self.remove_article(topic)

    def remove_article(self, token):
        t = str(token)
        for el in self.doc:
            if str(el) in token and el.pos_ == "DET":
                t = token.replace(el.text, "", 1)
        return t.strip()


if __name__ == "__main__":
    parser = DependencyParser()
    parser.set_text("3 phenomena are: ")
    print("test get_tokens(): ", parser.get_tokens())
    print("test get_topic(): ", parser.get_topic())
