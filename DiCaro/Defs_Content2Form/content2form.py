import string

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import math
from nltk.tokenize import word_tokenize

# Calcolo delle frequenze per ogni parola in defs,
# restituisce le n_frequent_words più frequenti e il genus composto dagli n_genus nomi più frequenti.
# remove_stopwords_flag indica se considerare le stopwords o meno
def get_most_frequent(defs, n_frequent_words, n_genus, subject, remove_stopwords_flag=True):
    frequency = {}
    only_nouns = set()
    words = []
    for definition in defs:
        text = word_tokenize(definition)
        pos_tagging = nltk.pos_tag(text)
        if len(definition) <= 0:
            continue
        for word in definition.split(' '):
            if remove_stopwords_flag:
                if word != subject and word not in stopword:
                    words.append(word)
                    for tuple in pos_tagging:
                        if tuple[0] == word and tuple[1] in "NN, NNS":
                            only_nouns.add(word)
            else:
                if word != subject:
                    words.append(word)
                    for tuple in pos_tagging:
                        if tuple[0] == word and tuple[1] in "NN, NNS":
                            only_nouns.add(word)
        for word in words:
            if word not in frequency.keys():
                frequency[word] = 1
            else:
                frequency[word] += 1
    top_n_frequent_words = list(dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True)).keys())[
                         :n_frequent_words]
    genus = []
    for word in top_n_frequent_words:
        if word in only_nouns:
            genus.append(word)
    return top_n_frequent_words, genus[:n_genus]

# Recupera tutti i synsets delle parole del genus e dei loro iponimi e iperonimi con una profondità depth
# consider_hyponym e consider_hypernym indicano se cercare o meno iponimi e iperonimi di un senso
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

# Recuperare per tutti i synset calcolati precedentemente le loro definizioni
def get_wordnet_definition(synsets):
    result = {}
    for synset in synsets:
        result[synset.name()] = synset.definition()
    return result

# Calcolo della similarità di jaccard per ogni synset, tra defs, cioè le definizioni in input e la synset_definition
def jaccard_similarity(defs, synset_definitions):
    result = {}
    defs_string = ""
    for definition in defs:
        defs_string += f"{definition} "
    for synset in synset_definitions:
        definition = f" {synset_definitions[synset].strip().lower().translate(translator)} "
        intersection = set()
        union = set([w for w in defs_string.split(' ')])
        for word in definition.split(' '):
            union.add(word)
            if word in defs_string.split(' '):
                intersection.add(word)
        similarity = len(intersection) / len(union)
        result[synset] = similarity
    return dict(sorted(result.items(), key=lambda item: item[1], reverse=True)[:10])

# Costruisce la rappresentazione vettoriale per ogni synset e per le definizioni date in input,
# viene calcolata la similarita mediante la cosine similarity tra e definizioni in input e ogni synset
def get_cos_similarity(defs, genus, all_synset_definition):
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

    for element in vector_result:
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

# Estrae tutti i synset con similarità massima
def get_final_synsets(values):
    synset_result = {}
    last_value = 0
    for element in values:
        if last_value == 0:
            synset_result[element] = values[element]
            last_value = values[element]
        elif values[element] == last_value:
            synset_result[element] = values[element]
        else:
            break
    return synset_result


if __name__ == '__main__':
    stopword = stopwords.words('english')
    translator = str.maketrans('', '', string.punctuation)
    f = open("./TLN-definitions-24.csv", "r")
    f.readline()
    pen = []
    cigarette = []
    cloud = []
    ontology = []
    # pulizia delle definizioni in input
    for line in f.readlines():
        splitted_line = line.split('#')
        pen.append(splitted_line[1].replace('"', '').replace('\n', '').strip().lower().translate(translator))
        cigarette.append(splitted_line[2].replace('"', '').replace('\n', '').strip().lower().translate(translator))
        cloud.append(splitted_line[3].replace('"', '').replace('\n', '').strip().lower().translate(translator))
        ontology.append(splitted_line[4].replace('"', '').replace('\n', '').strip().lower().translate(translator))

    print("PEN")
    most_frequent_word, genus = get_most_frequent(pen, 10, 5, "pen", remove_stopwords_flag=True)
    all_synsets = get_wordnet_synsets(genus, 3, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    cosine_similarity = get_cos_similarity(pen, most_frequent_word, all_synset_definition)
    similarity = jaccard_similarity(most_frequent_word, all_synset_definition)
    print("cosine_similarity: ", get_final_synsets(cosine_similarity))
    print("jaccard_similarity: ", get_final_synsets(similarity))

    print("\nCIGARETTE")
    most_frequent_word, genus = get_most_frequent(cigarette, 10, 5, "cigarette", remove_stopwords_flag=True)
    all_synsets = get_wordnet_synsets(genus, 3, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    cosine_similarity = get_cos_similarity(cigarette, most_frequent_word, all_synset_definition)
    similarity = jaccard_similarity(most_frequent_word, all_synset_definition)
    print("cosine_similarity: ", get_final_synsets(cosine_similarity))
    print("jaccard_similarity: ", get_final_synsets(similarity))

    print("\nCLOUD")
    most_frequent_word, genus = get_most_frequent(cloud, 10, 5, "cloud", remove_stopwords_flag=True)
    all_synsets = get_wordnet_synsets(genus, 3, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    cosine_similarity = get_cos_similarity(cloud, most_frequent_word, all_synset_definition)
    similarity = jaccard_similarity(most_frequent_word, all_synset_definition)
    print("cosine_similarity: ", get_final_synsets(cosine_similarity))
    print("jaccard_similarity: ", get_final_synsets(similarity))

    print("\nONTOLOGY")
    most_frequent_word, genus = get_most_frequent(ontology, 10, 5, "ontology", remove_stopwords_flag=True)
    all_synsets = get_wordnet_synsets(genus, 3, consider_hyponym=True, consider_hypernym=True)
    all_synset_definition = get_wordnet_definition(all_synsets)
    cosine_similarity = get_cos_similarity(ontology, most_frequent_word, all_synset_definition)
    similarity = jaccard_similarity(most_frequent_word, all_synset_definition)
    print("cosine_similarity: ", get_final_synsets(cosine_similarity))
    print("jaccard_similarity: ", get_final_synsets(similarity))