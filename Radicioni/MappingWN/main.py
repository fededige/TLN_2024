from nltk import SnowballStemmer
from nltk.corpus import wordnet as wn
from nltk.corpus import framenet as fn, stopwords
import string

luca_bonamico = [159, 302, 2837, 792, 2668]
luca_cena = [2971, 560, 2840, 797, 1894]
federico = [1683, 366, 1601, 414, 1591]

snow_stm = SnowballStemmer('english')
stopword = stopwords.words('english')


def get_most_frequent_words_fn(frame):
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


def get_most_frequent_words_lu_fn(frame):
    stopword.append('etc')
    translator = str.maketrans('', '', string.punctuation)
    definitions = [frame.definition.lower().translate(translator)]
    frame_elements = frame.FE.keys()

    for frame_element in frame_elements:
        fed = frame.FE[frame_element]
        definitions.append(fed.definition.lower().translate(translator))

    for lexical_unit in frame.lexUnit.keys():
        lu_def = frame.lexUnit[lexical_unit]['definition']
        if 'COD:' in lu_def:
            definitions.append(lu_def.replace('COD:', '').strip().lower().translate(translator))
        else:
            definitions.append(lu_def.replace('FN:', '').strip().lower().translate(translator))

    most_frequent_words = {}
    for definition in definitions:
        for word in definition.split(' '):
            if word != '' and word not in stopword:
                stemmed_word = snow_stm.stem(word)
                if stemmed_word not in most_frequent_words:
                    most_frequent_words[stemmed_word] = 1
                else:
                    most_frequent_words[stemmed_word] += 1

    most_frequent_words = dict(sorted(most_frequent_words.items(), key=lambda item: item[1], reverse=True))
    return [word for word in most_frequent_words.keys()][:12]


def get_most_frequent_words_wn(synsets):
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
                stemmed_word = snow_stm.stem(word)
                if stemmed_word not in most_frequent_words:
                    most_frequent_words[stemmed_word] = 1
                else:
                    most_frequent_words[stemmed_word] += 1
    most_frequent_words = dict(sorted(most_frequent_words.items(), key=lambda item: item[1], reverse=True))

    return [word for word in most_frequent_words.keys()][:12]


def get_contexts_fn_lu(frame, most_frequent_words):
    translator = str.maketrans('', '', string.punctuation)
    contexts = {}
    if frame.name in contexts:
        contexts[frame.name] += [word for word in frame.definition.lower().translate(translator).split(' ') if
                                 snow_stm.stem(word) in most_frequent_words and word not in contexts[frame.name]]
    else:
        contexts[frame.name] = [word for word in frame.definition.lower().translate(translator).split(' ') if
                                snow_stm.stem(word) in most_frequent_words]
    frame_elements = frame.FE.keys()
    for frame_element in frame_elements:
        fed = frame.FE[frame_element]
        contexts[frame_element] = list(set([word for word in fed.definition.lower().translate(translator).split(' ') if
                                            snow_stm.stem(word) in most_frequent_words]))
    # add lu to context
    for lexical_unit in frame.lexUnit.keys():
        contexts[lexical_unit] = list(set([word for word in frame.lexUnit[lexical_unit]['definition'].lower()
                                          .translate(translator).split(' ')
                                           if snow_stm.stem(word) in most_frequent_words]))
    return contexts


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
    ctx_s_stemmed = set([snow_stm.stem(ctx) for ctx in ctx_s])
    ctx_w_stemmed = set([snow_stm.stem(ctx) for ctx in ctx_w])
    return len(ctx_s_stemmed.intersection(ctx_w_stemmed)) + 1


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
    most_frequent_words_fn_lu = get_most_frequent_words_lu_fn(frame)
    print("most_frequent_words_fn: ", most_frequent_words_fn)
    print("most_frequent_words_fn_lu: ", most_frequent_words_fn_lu)
    framenet_contexts = get_contexts_fn(frame, most_frequent_words_fn)
    framenet_contexts_lu = get_contexts_fn_lu(frame, most_frequent_words_fn_lu)
    print("framenet_contexts: ", framenet_contexts)
    print("framenet_contexts_lu: ", framenet_contexts_lu)
    wn_synsets = wn.synsets(frame.name)
    most_frequent_words_wn = get_most_frequent_words_wn(wn_synsets)
    wordnet_contexts = get_contexts_wn(wn_synsets, most_frequent_words_wn)
    mapping_result = mapping(framenet_contexts, wordnet_contexts)
    mapping_result_lu = mapping(framenet_contexts_lu, wordnet_contexts)
    print(mapping_result)
    print(mapping_result_lu)


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

    # print(luca_cena_frame[4])
    map_to_wn(federico_frame[4])
    # print("federico")
    # print([l.name for l in federico_frame])
    # print(luca_cena_frame[1].name)
    # print('\n____ FEs ____')
    # FEs = luca_cena_frame[1].FE.keys()
    # for fe in FEs:
    #     fed = luca_cena_frame[1].FE[fe]
    #     print('\tFE: {}\tDEF: {}'.format(fe, fed.definition))
    #
    # print('\n____ LUs ____')
    # for lexUnit in luca_cena_frame[1].lexUnit.keys():
    #     print(lexUnit)

    # LUsValues = list(f.lexUnit.values())
    # i = 0
    # print(f.lexUnit)
    # LUsKeys = list(f.lexUnit.keys())
    # LUsValues = list(f.lexUnit.values())
    # i = 0
    # while i < len(LUsKeys):
    #     print(f"{LUsKeys[i]} ---> {LUsValues[i]['exemplars']}")
    #     i += 1
    # break
