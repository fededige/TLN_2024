import string
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import math


def get_most_common(defs, n, subject, remove_stopwords_flag=True):
    frequency = {}
    for definition in defs:
        if len(definition) <= 0:
            continue
        if remove_stopwords_flag:
            words = [word for word in definition.split(' ') if word not in stopword and word != subject]
        else:
            words = [word for word in definition.split(' ') if word != subject]
        for word in words:
            if word not in frequency.keys():
                frequency[word] = 1
            else:
                frequency[word] += 1
    return list(dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True)).keys())[:n]


def get_wordnet_synsets(genus, depth=0, consider_hyponym=False, consider_hypernym=False):
    result = []
    for word in genus:
        synsets = wn.synsets(word)
        for s in synsets:
            result.append(s)
    result = list(set(result))
    stack = result.copy()
    length = len(stack)
    i = 0
    j = 0
    while len(stack) > 0 and i < depth:
        el = stack.pop(0)
        new_synsets = []
        if consider_hypernym:
            new_synsets = el.hypernyms()
        if consider_hyponym:
            new_synsets += el.hyponyms()
        if len(new_synsets) > 0:
            result += new_synsets
            for synset in new_synsets:
                if synset not in stack:
                    stack.append(synset)
        if j == length - 1:
            i += 1
            length += len(stack)
        j += 1

    result = list(set(result))
    return result


def get_wordnet_definition(synsets):
    result = {}
    for synset in synsets:
        result[synset.name()] = synset.definition()
    return result


def get_similarity(defs, genus, all_synset_definition):
    vector_defs = [0] * len(genus)
    vector_synset = [0] * len(genus)
    vector_result = {}

    for definition in defs:
        definition = f" {definition} "
        for i in range(len(genus)):
            if genus[i] in definition:
                vector_defs[i] += definition.count(f" {genus[i]} ")

    for synset in all_synset_definition:
        definition = f" {all_synset_definition[synset].strip().lower().translate(translator)} "
        for i in range(len(genus)):
            if genus[i] in definition:
                vector_synset[i] += definition.count(f" {genus[i]} ")
        vector_result[synset] = vector_synset.copy()
        vector_synset = [0] * len(genus)

    result = {}

    for element in vector_result.keys():
        numerator = 0
        for i in range(len(vector_defs)):
            numerator += vector_defs[i] * vector_result[element][i]

        sum_defs = 0
        sum_synset = 0
        for i in range(len(vector_defs)):
            sum_defs += vector_defs[i] * vector_defs[i]
            sum_synset += vector_result[element][i] * vector_result[element][i]

        denominator = math.sqrt(sum_defs) * math.sqrt(sum_synset)
        if denominator == 0:
            result[element] = 0
        else:
            result[element] = numerator / denominator
    return dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:10])


if __name__ == '__main__':
    stopword = stopwords.words('english')
    translator = str.maketrans('', '', string.punctuation)
    f = open("./TLN-definitions-24.csv", "r")
    print(f.readline())
    pen = []
    cigarette = []
    cloud = []
    ontology = []
    for line in f.readlines():
        splitted_line = line.split('#')
        pen.append(splitted_line[1].replace('"', '').replace('\n', '').strip().lower().translate(translator))
        cigarette.append(splitted_line[2].replace('"', '').replace('\n', '').strip().lower().translate(translator))
        cloud.append(splitted_line[3].replace('"', '').replace('\n', '').strip().lower().translate(translator))
        ontology.append(splitted_line[4].replace('"', '').replace('\n', '').strip().lower().translate(translator))

    print("PEN")
    most_common_word = get_most_common(pen, 10, "pen", remove_stopwords_flag=True)
    print("pen 10 most common word without stopwords: \n", most_common_word)
    all_synsets = get_wordnet_synsets(most_common_word, 3, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    synsets_similarity = get_similarity(pen, most_common_word, all_synset_definition)
    print("synsets_similarity: ", synsets_similarity)

    genus = ["write", "object", "tool", "ink"]
    all_synsets = get_wordnet_synsets(genus, 3, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    synsets_similarity = get_similarity(pen, most_common_word, all_synset_definition)
    print("synsets_similarity: ", synsets_similarity)

    genus = ["write", "object", "tool"]
    all_synsets = get_wordnet_synsets(genus, 3, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    synsets_similarity = get_similarity(pen, most_common_word, all_synset_definition)
    print("synsets_similarity: ", synsets_similarity)

    genus = ["write", "object", "tool", "ink", "writing"]
    all_synsets = get_wordnet_synsets(genus, 3, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    synsets_similarity = get_similarity(pen, most_common_word, all_synset_definition)
    print("synsets_similarity: ", synsets_similarity)

    print("CIGARETTE")
    most_common_word = get_most_common(cigarette, 10, "cigarette", remove_stopwords_flag=True)
    print("cigarette 10 most common word without stopwords: \n", most_common_word)
    all_synsets = get_wordnet_synsets(most_common_word, 3, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    synsets_similarity = get_similarity(cigarette, most_common_word, all_synset_definition)
    print("synsets_similarity: ", synsets_similarity)

    genus = ["tobacco", "object", "smoked"]
    all_synsets = get_wordnet_synsets(genus, 3, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    synsets_similarity = get_similarity(cigarette, most_common_word, all_synset_definition)
    print("synsets_similarity: ", synsets_similarity)

    print("Cloud")
    most_common_word = get_most_common(cloud, 10, "cloud", remove_stopwords_flag=True)
    print("cloud 10 most common word without stopwords: \n", most_common_word)
    all_synsets = get_wordnet_synsets(most_common_word, 4, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    synsets_similarity = get_similarity(cloud, most_common_word, all_synset_definition)
    print("synsets_similarity: ", synsets_similarity)

    genus = ["phenomenon", "atmosphere", "sky"]
    all_synsets = get_wordnet_synsets(genus, 3, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    synsets_similarity = get_similarity(cloud, most_common_word, all_synset_definition)
    print("synsets_similarity: ", synsets_similarity)

    print("Ontology")
    most_common_word = get_most_common(ontology, 10, "ontology", remove_stopwords_flag=True)
    print("ontology 10 most common word without stopwords: \n", most_common_word)
    all_synsets = get_wordnet_synsets(most_common_word, 3, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    synsets_similarity = get_similarity(ontology, most_common_word, all_synset_definition)
    print("synsets_similarity: ", synsets_similarity)

    genus = ["knowledge", "philosophical", "structure"]
    all_synsets = get_wordnet_synsets(genus, 3, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    synsets_similarity = get_similarity(ontology, most_common_word, all_synset_definition)
    print("synsets_similarity: ", synsets_similarity)

    # all_synsets = get_wordnet_synsets(genus, 1, consider_hyponym=True, consider_hypernym=True)
    # all_synset_definition = get_wordnet_definition(all_synsets)
    # print(all_synset_definition)

    # print("test: ", wn.synset("writing_implement.n.01").definition())
    # print("test: ", wn.synset("use.v.02").hyponyms())
    # print("test: ", wn.synset("use.v.02").hypernyms())

    # res = get_wn_synset(genus, wordnet_defs_exs)
    # print("Mapping between our definition and wordnet (only direct synset)\n", dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))
    #
    # wordnet_defs_exs = get_wordnet_synset_2("pen", consider_hyponym=True, consider_hypernym=True)
    # res = get_wn_synset(genus, wordnet_defs_exs)
    # print("Mapping between our definition and wordnet (inlcuding hyperonym and hyponym)\n", dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))
    # print()
    # print("PEN with stopword")
    # genus = get_most_common(pen, 10, "pen", remove_stopwords_flag=False)
    # # print("pen 10 most common word without stopwords: \n", genus)
    # wordnet_defs_exs = get_wordnet_synset("pen", consider_hyponym=True, consider_hypernym=True)
    # res = get_wn_synset(genus, wordnet_defs_exs)
    # print("Mapping between our definition and wordnet (only direct synset)\n",
    #       dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))
    #
    # wordnet_defs_exs = get_wordnet_synset_2("pen", consider_hyponym=True, consider_hypernym=True)
    # res = get_wn_synset(genus, wordnet_defs_exs)
    # print("Mapping between our definition and wordnet (inlcuding hyperonym and hyponym)\n",
    #       dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))
