from nltk import SnowballStemmer
from nltk.corpus import wordnet as wn
from nltk.corpus import framenet as fn, stopwords
from nltk.tokenize import word_tokenize
import nltk
import string
import re


luca_bonamico = [159, 302, 2837, 792, 2668]
luca_cena = [2971, 560, 2840, 797, 1894]
federico = [1683, 366, 1601, 414, 1591]

snow_stm = SnowballStemmer('english')
stopword = stopwords.words('english')


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
        contexts[frame_element] = [word for word in fed.definition.lower().translate(translator).split(' ') if
                                   snow_stm.stem(word) in most_frequent_words]
    # add lu to context
    for lexical_unit in frame.lexUnit.keys():
        contexts[lexical_unit] = [word for word in frame.lexUnit[lexical_unit]['definition'].lower()
                                  .translate(translator).split(' ')
                                  if snow_stm.stem(word) in most_frequent_words]
    for context in contexts.keys():
        contexts[context] = list(set(contexts[context]))
    return contexts


def get_contexts_wn(synsets, most_frequent_words):
    most_frequent_words_stemmed = [snow_stm.stem(fw) for fw in most_frequent_words]
    translator = str.maketrans('', '', string.punctuation)
    contexts = {}
    for syn in synsets:
        contexts[syn.name()] = [word for word in syn.definition().lower().translate(translator).split(' ') if
                                snow_stm.stem(word) in most_frequent_words_stemmed]
        for ex in syn.examples():
            contexts[syn.name()] += [word for word in ex.lower().translate(translator).split(' ') if
                                     snow_stm.stem(word) in most_frequent_words_stemmed]

    for context in contexts.keys():
        contexts[context] = list(set(contexts[context]))
    return contexts


def bag_of_word(ctx_w, ctx_s):
    # print(ctx_w)
    # print(ctx_s)
    ctx_s_stemmed = set([snow_stm.stem(ctx) for ctx in ctx_s])
    ctx_w_stemmed = set([snow_stm.stem(ctx) for ctx in ctx_w])
    # print(ctx_s_stemmed.intersection(ctx_w_stemmed))
    return len(ctx_s_stemmed.intersection(ctx_w_stemmed)) + 1


def mapping(framenet_context, wordnet_contexts):
    score = 0
    result = ""
    for synset in wordnet_contexts.keys():
        # print(synset)
        new_score = bag_of_word(framenet_context, wordnet_contexts[synset])
        if score < new_score:
            score = new_score
            result = synset
    # print("Score: ", score)
    # if result != "":
    #     print(f"framenet_context, wordnet_contexts[{result}]", framenet_context, wordnet_contexts[result])
    return result


def clean_name(frame_element):
    res = frame_element
    if '.' in frame_element:
        res = frame_element.split('.')[0].split('[')[0].strip()
    elif '_' in frame_element:
        words = word_tokenize(frame_element.replace('_', ' ').lower())
        pos_tag = nltk.pos_tag(words)
        pos = [p[1] for p in pos_tag]
        print(pos)
        index = 0
        if 'JJ' in pos:
            if 'NN' in pos:
                index = pos.index('NN')
            elif 'NNS' in pos:
                index = pos.index('NNS')
        elif 'VB' in pos or 'VBD' in pos or 'VBG' in pos or 'VBN' in pos or 'VBP' in pos or 'VBZ' in pos:
            pass
            # index = pos.index(r"VB.*")
        res = pos_tag[index][0]
    return res


def map_to_wn(frame):
    mapping_result = {}
    most_frequent_words_fn_lu = get_most_frequent_words_lu_fn(frame)
    framenet_contexts = get_contexts_fn_lu(frame, most_frequent_words_fn_lu)
    # print("framenet_contexts: ", framenet_contexts)
    for frame_element in framenet_contexts.keys():
        element_synsets = wn.synsets(clean_name(frame_element))
        most_frequent_words_wn = get_most_frequent_words_wn(element_synsets)
        # print(f"most_frequent_words_wn '{element_synsets}': ", most_frequent_words_wn)
        wordnet_contexts = get_contexts_wn(element_synsets, most_frequent_words_wn)
        mapping_result[frame_element] = mapping(framenet_contexts[frame_element], wordnet_contexts)
        # print("\n------------------------------------")
        # print(f"wordnet_contexts: '{frame_element}'", wordnet_contexts)
        # print("------------------------------------")
    # mapping_result_lu = mapping(framenet_contexts_lu, wordnet_contexts)
    print(mapping_result)


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
    # for luca_bonamico_f in luca_bonamico_frame:
    #     map_to_wn(luca_bonamico_f)

    for frame in federico_frame:
        print(frame.name)

    print(clean_name("Fire_break"))
    print(clean_name("Time_of_creation"))
    print(clean_name("Specific_individual"))
    print(clean_name("Religious_belief"))
    print(clean_name("Change_of_temperature"))
    print(clean_name("Interrupt_process"))
    print(clean_name("Attempting_and_resolving_scenario"))
    print([1, 2, 3].index(4))
    # c = get_contexts_wn(wn.synsets('brush'), get_most_frequent_words_wn(wn.synsets('brush')))
    # print(c)
    # print(luca_bonamico_frame[0])
    # print('\n____ LUs ____')
    # LUs = luca_bonamico_frame[0].lexUnit.values()
    # for lu in LUs:
    #     print(lu)
    # print(LUs)
    # print('\n____ FEs ____')
    # FEs = luca_cena_frame[1].FE.keys()
    # for fe in FEs:
    #     fed = luca_cena_frame[1].FE[fe]
    #     print('\tFE: {}\tDEF: {}'.format(fe, fed.definition))
    #
    # print('\n____ LUs ____')
    # for lexUnit in luca_cena_frame[1].lexUnit.keys():
    #     print(lexUnit)
    #
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
