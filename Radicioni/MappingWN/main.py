from nltk.corpus import wordnet as wn
from nltk.corpus import framenet as fn, stopwords
import string

luca_bonamico = [159, 302, 2837, 792, 2668]
luca_cena = [2971, 560, 2840, 797, 1894]
federico = [1683, 366, 1601, 414, 1591]


def get_most_frequent_words_fn(frame):
    stopword = stopwords.words('english')
    stopword.append('etc')
    translator = str.maketrans('', '', string.punctuation)
    definitions = [frame.definition.lower().translate(translator)]
    frame_elements = frame.FE.keys()
    for frame_element in frame_elements:
        fed = frame.FE[frame_element]
        definitions.append(fed.definition.lower().translate(translator))

    most_frequent_words = {}
    for definition in definitions:
        for word in definition.split(' '):
            if word != '' and word not in stopword:
                if word not in most_frequent_words:
                    most_frequent_words[word] = 1
                else:
                    most_frequent_words[word] += 1

    most_frequent_words = dict(sorted(most_frequent_words.items(), key=lambda item: item[1], reverse=True))
    return [word for word in most_frequent_words.keys()][:12]


def get_most_frequent_words_wn(synsets):
    stopword = stopwords.words('english')
    stopword.append('etc')
    translator = str.maketrans('', '', string.punctuation)
    definitions = []
    for syn in synsets:
        definitions.append(syn.definition().lower().translate(translator))
        definitions += [ex.lower().translate(translator) for ex in syn.examples()]
        for hypon in syn.hyponyms():
            definitions.append(hypon.definition().lower().translate(translator))
            definitions += [ex.lower().translate(translator) for ex in hypon.examples()]
        for hyper in syn.hypernyms():
            definitions.append(hyper.definition().lower().translate(translator))
            definitions += [ex.lower().translate(translator) for ex in hyper.examples()]

    most_frequent_words = {}
    for definition in definitions:
        for word in definition.split(' '):
            if word != '' and word not in stopword:
                if word not in most_frequent_words:
                    most_frequent_words[word] = 1
                else:
                    most_frequent_words[word] += 1
    most_frequent_words = dict(sorted(most_frequent_words.items(), key=lambda item: item[1], reverse=True))

    return [word for word in most_frequent_words.keys()][:12]


def get_contexts_fn(frame, most_frequent_words):
    translator = str.maketrans('', '', string.punctuation)
    contexts = {}
    contexts[frame.name] = [word for word in frame.definition.lower().translate(translator).split(' ') if
                            word in most_frequent_words]
    frame_elements = frame.FE.keys()
    for frame_element in frame_elements:
        fed = frame.FE[frame_element]
        contexts[frame_element] = [word for word in fed.definition.lower().translate(translator).split(' ') if
                                   word in most_frequent_words]
    return contexts


def map_to_wn(frame):
    most_frequent_words_fn = get_most_frequent_words_fn(frame)
    framenet_contexts = get_contexts_fn(frame, most_frequent_words_fn)
    wn_synsets = wn.synsets(frame.name)
    most_frequent_words_wn = get_most_frequent_words_wn(wn_synsets)
    print(most_frequent_words_wn)


if __name__ == '__main__':
    f = fn.frame(luca_bonamico[0])
    luca_bonamico_frame = []
    luca_cena_frame = []
    federico_frame = []

    for frame_id in luca_bonamico:
        luca_bonamico_frame.append(fn.frame(frame_id))

    for frame_id in luca_cena:
        luca_cena_frame.append(fn.frame(frame_id))

    for frame_id in federico:
        federico_frame.append(fn.frame(frame_id))

    map_to_wn(luca_bonamico_frame[0])

    # for f in luca_bonamico_frame:
    #     print("\n", f.name)
    #     print("\n", f.definition)
    #     print('\n____ FEs ____')
    #     FEs = f.FE.keys()
    #     for fe in FEs:
    #         fed = f.FE[fe]
    #         print('\tFE: {}\tDEF: {}'.format(fe, fed.definition))
    #     break
    #     # print('\n____ LUs ____')
    #     # LUs = f.lexUnit.keys()
    #     # for lu in LUs:
    #     #     print(lu)
