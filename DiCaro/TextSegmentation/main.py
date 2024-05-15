import string


def get_cohesion(block_size):
    return


def get_sentences(file):
    sentences = []
    for lines in file.readlines():
        sentences += [line.lower().strip().translate(translator) for line in lines.split('.')]

    clean_sentences = []
    for sentence in sentences:
        if len(sentence.split(' ')) > 1:
            clean_sentences.append(sentence)

    return clean_sentences


def get_blocks(block_size, sentences):
    blocks = []
    i = 0
    while i < len(sentences):
        blocks.append(sentences[i:i+block_size])
        i += block_size
    return blocks


if __name__ == '__main__':
    translator = str.maketrans('', '', string.punctuation)
    f = open("./text1.txt", "r")

    sentences = get_sentences(f)
    block_size = 3
    plot = [0] * round((len(sentences) / block_size))

    blocks = get_blocks(block_size, sentences)
