import string
from nltk.corpus import stopwords

# Calcolo delle frequenze delle parole all'interno di defs.
# Restituisce la lista delle parole ordinate secondo la loro frequenza.
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

# Calcola le parole più comuni in base a threshold,
# cioè vengono prese solo quelle parole la cui frequenza relativa è maggiore di threshold
def get_most_common(defs, frequency, threshold):
    frequency_total = {}
    for word in frequency:
        for definition in defs:
            if word in definition:
                if word not in frequency_total:
                    frequency_total[word] = 1
                else:
                    frequency_total[word] += 1
    result = []
    for word in frequency_total.keys():
        def_frequency = frequency_total[word] / len(defs)
        if def_frequency >= threshold:
            result.append(word)
        else:
            break
    return result

# Calcola la similarity dividendo la cardinalità delle parole più comuni per il numero totale delle definizioni
def get_similarity(total_common_word, total_def):
    return total_common_word / total_def


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

    # threshold serve per prendere solo le parole che compaiono almeno nel (threshold * 100)% delle frasi
    threshold = 0.3
    print("Threshold utilizzato nell'esecuzione: ", threshold)
    print()

    print("PEN (GENERICO/CONCRETO)")
    frequency = word_frequency(pen)
    most_frequent = get_most_common(pen, frequency, threshold)
    similarity = get_similarity(len(most_frequent), len(pen))
    print("intersezione delle parole più comuni: ", most_frequent)
    print("valore di similarità: ", similarity)
    print()

    print("CIGARETTE (SPECIFICO/CONCRETO)")
    frequency = word_frequency(cigarette)
    most_frequent = get_most_common(cigarette, frequency, threshold)
    similarity = get_similarity(len(most_frequent), len(cigarette))
    print("intersezione delle parole più comuni: ", most_frequent)
    print("valore di similarità: ", similarity)
    print()

    print("CLOUD (GENERICO/ASTRATTO)")
    frequency = word_frequency(cloud)
    most_frequent = get_most_common(cloud, frequency, threshold)
    similarity = get_similarity(len(most_frequent), len(cloud))
    print("intersezione delle parole più comuni: ", most_frequent)
    print("valore di similarità: ", similarity)
    print()

    print("ONTOLOGY (SPECIFICO/ASTRATTO)")
    frequency = word_frequency(ontology)
    most_frequent = get_most_common(ontology, frequency, threshold)
    similarity = get_similarity(len(most_frequent), len(ontology))
    print("intersezione delle parole più comuni: ", most_frequent)
    print("valore di similarità: ", similarity)
    print()
