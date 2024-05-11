import string
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn


def get_most_common(defs, n, subject, remove_stopwords_flag=True):
    frequency = {}
    for definition in defs:
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


def right_synset(name, synsets):
    for syn in synsets:
        if syn.name() == name:
            return syn


def get_n_hyponym(n_hyponym, synset):
    hyponyms = synset.hyponyms()
    stack = hyponyms.copy()
    length = len(stack)
    i = 0
    j = 0
    while len(stack) > 0 and i < n_hyponym:
        el = stack.pop(0)
        new_hyponyms = right_synset(el.name(), wn.synsets(el.lemma_names()[0])).hyponyms()
        if len(new_hyponyms) > 0:
            hyponyms += new_hyponyms
            stack += new_hyponyms
        if j == length - 1:
            i += 1
            length += len(stack)
        j += 1
    return list(hyponyms)


def get_n_hypernym(n_hypernym, synset):
    hypernyms = synset.hypernyms()
    stack = hypernyms.copy()
    length = len(stack)
    i = 0
    j = 0
    while len(stack) > 0 and i < n_hypernym:
        el = stack.pop(0)
        new_hypernyms = right_synset(el.name(), wn.synsets(el.lemma_names()[0])).hypernyms()
        if len(new_hypernyms) > 0:
            hypernyms += new_hypernyms
            stack += new_hypernyms
        if j == length - 1:
            i += 1
            length += len(stack)
        j += 1
    return list(hypernyms)


def get_wordnet_synset(subject, n_hyponym=0, n_hypernym=0, consider_hyponym=False, consider_hypernym=False):
    synsets = wn.synsets(subject)
    result = {}
    for synset in synsets:
        result[synset.name()] = [synset.definition()]
        result[synset.name()] += [ex for ex in synset.examples()]
        if consider_hyponym:
            for el in get_n_hyponym(n_hyponym, synset):
                result[synset.name()] += [el.definition()]
                result[synset.name()] += [ex for ex in el.examples()]
        if consider_hypernym:
            for el in get_n_hypernym(n_hypernym, synset):
                result[synset.name()] += [el.definition()]
                result[synset.name()] += [ex for ex in el.examples()]
    return result


def get_wordnet_synset_2(subject, n_hyponym=0, n_hypernym=0, consider_hyponym=False, consider_hypernym=False):
    synsets = wn.synsets(subject)
    result = {}
    for synset in synsets:
        result[synset.name()] = [synset.definition()]
        result[synset.name()] += [ex for ex in synset.examples()]
        if consider_hyponym:
            for el in get_n_hyponym(n_hyponym, synset):
                result[el.name()] = [el.definition()]
                result[el.name()] += [ex for ex in el.examples()]
        if consider_hypernym:
            for el in get_n_hypernym(n_hypernym, synset):
                result[el.name()] = [el.definition()]
                result[el.name()] += [ex for ex in el.examples()]
    return result


def get_similarity(genus, definition):
    sum = 0
    for word in definition.split(' '):
        if word in genus:
            sum += 1
    return sum / len(definition.split(' '))


def get_wn_synset(genus, wordnet_defs_exs):
    result = {}
    for syn in wordnet_defs_exs.keys():
        syn_similarity = 0
        for definition in wordnet_defs_exs[syn]:
            syn_similarity += get_similarity(genus, definition)
        result[syn] = syn_similarity / len(wordnet_defs_exs[syn])
    return result


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
    genus = get_most_common(pen, 10, "pen", remove_stopwords_flag=True)
    # print("pen 10 most common word without stopwords: \n", genus)
    wordnet_defs_exs = get_wordnet_synset("pen", consider_hyponym=True, consider_hypernym=True)
    res = get_wn_synset(genus, wordnet_defs_exs)
    print("Mapping between our definition and wordnet (only direct synset)\n", dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))

    wordnet_defs_exs = get_wordnet_synset_2("pen", consider_hyponym=True, consider_hypernym=True)
    res = get_wn_synset(genus, wordnet_defs_exs)
    print("Mapping between our definition and wordnet (inlcuding hyperonym and hyponym)\n", dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))
    print()
    print("PEN with stopword")
    genus = get_most_common(pen, 10, "pen", remove_stopwords_flag=False)
    # print("pen 10 most common word without stopwords: \n", genus)
    wordnet_defs_exs = get_wordnet_synset("pen", consider_hyponym=True, consider_hypernym=True)
    res = get_wn_synset(genus, wordnet_defs_exs)
    print("Mapping between our definition and wordnet (only direct synset)\n",
          dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))

    wordnet_defs_exs = get_wordnet_synset_2("pen", consider_hyponym=True, consider_hypernym=True)
    res = get_wn_synset(genus, wordnet_defs_exs)
    print("Mapping between our definition and wordnet (inlcuding hyperonym and hyponym)\n",
          dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))
    print()
    print("CIGARETTE")
    genus = get_most_common(cigarette, 10, "cigarette", remove_stopwords_flag=True)
    # print("cigarette 10 most common word without stopwords: \n", genus)
    wordnet_defs_exs = get_wordnet_synset("cigarette", consider_hyponym=True, consider_hypernym=True)
    res = get_wn_synset(genus, wordnet_defs_exs)
    print("Mapping between our definition and wordnet (only direct synset)\n",
          dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))

    wordnet_defs_exs = get_wordnet_synset_2("cigarette", consider_hyponym=True, consider_hypernym=True)
    res = get_wn_synset(genus, wordnet_defs_exs)
    print("Mapping between our definition and wordnet (inlcuding hyperonym and hyponym)\n",
          dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))
    print()
    print("CLOUD")
    genus = get_most_common(cloud, 10, "cloud", remove_stopwords_flag=True)
    # print("cloud 10 most common word without stopwords: \n", genus)
    wordnet_defs_exs = get_wordnet_synset("cloud", consider_hyponym=True, consider_hypernym=True)
    res = get_wn_synset(genus, wordnet_defs_exs)
    print("Mapping between our definition and wordnet (only direct synset)\n",
          dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))

    wordnet_defs_exs = get_wordnet_synset_2("cloud", consider_hyponym=True, consider_hypernym=True)
    res = get_wn_synset(genus, wordnet_defs_exs)
    print("Mapping between our definition and wordnet (inlcuding hyperonym and hyponym)\n",
          dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))
    print()
    print("ONTOLOGY")
    genus = get_most_common(ontology, 10, "ontology", remove_stopwords_flag=True)
    # print("ontology 10 most common word without stopwords: \n", genus)
    wordnet_defs_exs = get_wordnet_synset("ontology", consider_hyponym=True, consider_hypernym=True)
    res = get_wn_synset(genus, wordnet_defs_exs)
    print("Mapping between our definition and wordnet (only direct synset)\n",
          dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))

    wordnet_defs_exs = get_wordnet_synset_2("ontology", consider_hyponym=True, consider_hypernym=True)
    res = get_wn_synset(genus, wordnet_defs_exs)
    print("Mapping between our definition and wordnet (inlcuding hyperonym and hyponym)\n",
          dict(sorted(res.items(), key=lambda item: item[1], reverse=True)))
