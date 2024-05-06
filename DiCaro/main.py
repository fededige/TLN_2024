import string
from nltk import SnowballStemmer
from nltk.corpus import stopwords


def get_similarity(defs):
    word_in_common = set([snow_stm.stem(word) for word in defs[0].split(' ') if word not in stopword])
    min_len = len(defs[0])
    i = 0
    for definition in defs:
        words = [snow_stm.stem(word) for word in definition.split(' ') if word not in stopword]
        if len(words) > 0:
            word_in_common = word_in_common.intersection(words)
            if len(definition) < min_len:
                min_len = len(words)
    return len(word_in_common) / min_len


if __name__ == '__main__':
    snow_stm = SnowballStemmer('english')
    stopword = stopwords.words('english')
    translator = str.maketrans('', '', string.punctuation)
    f = open("./TLN-definitions-23.tsv", "r")
    print(f.readline())
    pen = []
    cigarette = []
    cloud = []
    ontology = []
    for line in f.readlines():
        splitted_line = line.split('\t')
        pen.append(splitted_line[1].replace('"', '').replace('\n', '').strip().lower().translate(translator))
        cigarette.append(splitted_line[2].replace('"', '').replace('\n', '').strip().lower().translate(translator))
        cloud.append(splitted_line[3].replace('"', '').replace('\n', '').strip().lower().translate(translator))
        ontology.append(splitted_line[4].replace('"', '').replace('\n', '').strip().lower().translate(translator))

    pen_similarity = get_similarity(pen)
    print(pen_similarity)
