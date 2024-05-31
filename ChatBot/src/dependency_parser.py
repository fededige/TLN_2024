import spacy
import questions_pool
from spacytextblob.spacytextblob import SpacyTextBlob


class DependencyParser:
    def __init__(self):
        self.text = ""
        self.nlp = spacy.load("en_core_web_lg")
        self.nlp.add_pipe('spacytextblob')
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

    def get_polarity(self):
        if 'yes' in self.text.lower():
            return True
        elif 'no' in self.text.lower():
            return False
        sentiment_score = self.doc._.blob.polarity
        if sentiment_score > 0:
            return True
        elif sentiment_score < 0:
            return False
        else:
            return None


def get_negativity(sentence):
    elements = ["no", "\'t", "none", "nor", "neither"]
    for el in elements:
        if el in sentence.lower():
            return True
    return False


if __name__ == "__main__":
    parser = DependencyParser()
    text = "generative."
    parser.set_text(text)
    print(parser.get_tokens())

    # for q in questions_pool.questions:
    #
    #     print(q.get_text())
    #     print(parser.get_topic())
    # sentiment = parser.get_polarity()
    # print(f"Sentence: {sentence} -- Sentiment: {sentiment}")
