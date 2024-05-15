import string
from nltk import SnowballStemmer
from nltk.corpus import stopwords


# def get_similarity(defs):
#     word_in_common = set([snow_stm.stem(word) for word in defs[0].split(' ') if word not in stopword])
#     min_len = len(defs[0])
#     i = 0
#     for definition in defs:
#         words = [snow_stm.stem(word) for word in definition.split(' ') if word not in stopword]
#         if len(words) > 0:
#             word_in_common = word_in_common.intersection(words)
#             if len(definition) < min_len:
#                 min_len = len(words)
#     return len(word_in_common) / min_len


def word_frequency(defs):
    frequency = {}
    for definition in defs:
        words = [word for word in definition.split(' ') if word not in stopword]
        for word in words:
            if word not in frequency.keys():
                frequency[word] = 1
            else:
                frequency[word] += 1
    return list(dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True)).keys())


def get_most_commomn(defs, frequency, threshold):
    freqency_total = {}
    for word in frequency:
        for definition in defs:
            if word in definition:
                if word not in freqency_total:
                    freqency_total[word] = 1
                else:
                    freqency_total[word] += 1
    result = []
    for word in freqency_total.keys():
        def_frequency = freqency_total[word] / len(defs)
        if def_frequency >= threshold:
            result.append(word)
        else:
            break
    return result


def get_similarity(total_common_word, total_def):
    return total_common_word / total_def


if __name__ == '__main__':
    snow_stm = SnowballStemmer('english')
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

    threshold = 0.6
    frequency = word_frequency(pen)
    most_frequent = get_most_commomn(pen, frequency, threshold)
    similarity = get_similarity(len(most_frequent), len(pen))
    print(frequency)
    print(most_frequent)
    print(similarity)
    print()

    frequency = word_frequency(cigarette)
    most_frequent = get_most_commomn(cigarette, frequency, threshold)
    similarity = get_similarity(len(most_frequent), len(cigarette))
    print(frequency)
    print(most_frequent)
    print(similarity)
    print()

    frequency = word_frequency(cloud)
    most_frequent = get_most_commomn(cloud, frequency, threshold)
    similarity = get_similarity(len(most_frequent), len(cloud))
    print(frequency)
    print(most_frequent)
    print(similarity)
    print()

    frequency = word_frequency(ontology)
    most_frequent = get_most_commomn(ontology, frequency, threshold)
    similarity = get_similarity(len(most_frequent), len(ontology))
    print(frequency)
    print(most_frequent)
    print(similarity)
    print()
