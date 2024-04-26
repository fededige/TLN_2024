from nltk import SnowballStemmer
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
    if frame.name in contexts:
        contexts[frame.name] += [word for word in frame.definition.lower().translate(translator).split(' ') if
                                 word in most_frequent_words and word not in contexts[frame.name]]
    else:
        contexts[frame.name] = [word for word in frame.definition.lower().translate(translator).split(' ') if
                                word in most_frequent_words]
    frame_elements = frame.FE.keys()
    for frame_element in frame_elements:
        fed = frame.FE[frame_element]
        contexts[frame_element] = list(set([word for word in fed.definition.lower().translate(translator).split(' ') if
                                            word in most_frequent_words]))
    return contexts


def get_contexts_wn(synsets, most_frequent_words):
    snow_stm = SnowballStemmer('english')
    most_frequent_words_stemmed = [snow_stm.stem(fw) for fw in most_frequent_words]
    translator = str.maketrans('', '', string.punctuation)
    contexts = {}
    for syn in synsets:
        contexts[syn.name()] = list(set([word for word in syn.definition().lower().translate(translator).split(' ') if
                                         snow_stm.stem(word) in most_frequent_words_stemmed]))
        for ex in syn.examples():
            contexts[syn.name()] += list(set([word for word in ex.lower().translate(translator).split(' ') if
                                              snow_stm.stem(word) in most_frequent_words_stemmed]))
    return contexts


def bag_of_word(ctx_w, ctx_s):
    print(ctx_w)
    print(ctx_s)
    print(set(ctx_s).intersection(set(ctx_w)))
    return len(set(ctx_s).intersection(set(ctx_w))) + 1


def mapping(framenet_contexts, wordnet_contexts):
    result = {}
    for frame_element in framenet_contexts.keys():
        score = 0
        for word in wordnet_contexts.keys():
            new_score = bag_of_word(framenet_contexts[frame_element], wordnet_contexts[word])
            print(frame_element, word, new_score)
            if score < new_score:
                score = new_score
                result[frame_element] = word
    return result


def map_to_wn(frame):
    most_frequent_words_fn = get_most_frequent_words_fn(frame)
    framenet_contexts = get_contexts_fn(frame, most_frequent_words_fn)
    wn_synsets = wn.synsets(frame.name)
    most_frequent_words_wn = get_most_frequent_words_wn(wn_synsets)
    wordnet_contexts = get_contexts_wn(wn_synsets, most_frequent_words_wn)
    print("Mapping: ", mapping(framenet_contexts, wordnet_contexts))


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

    print(luca_cena_frame[4])
    map_to_wn(luca_cena_frame[4])

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
