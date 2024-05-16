import math
import string
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import numpy as np


def get_cohesion(block1, block2):
    word_union = []
    for sentence in block1:
        for word in sentence.split(' '):
            if word not in word_union and word not in stopword:
                word_union.append(word)
    for sentence in block2:
        for word in sentence.split(' '):
            if word not in word_union and word not in stopword:
                word_union.append(word)
    vector1 = [0] * len(word_union)
    vector2 = [0] * len(word_union)
    for sentence in block1:
        for word in sentence.split(' '):
            if word in word_union:
                vector1[word_union.index(word)] += 1
    for sentence in block2:
        for word in sentence.split(' '):
            if word in word_union:
                vector2[word_union.index(word)] += 1
    numerator = 0
    sum1 = 0
    sum2 = 0
    for i in range(len(vector1)):
        numerator += vector1[i] * vector2[i]
        sum1 += (vector1[i] * vector1[i])
        sum2 += (vector2[i] * vector2[i])

    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    return numerator / denominator


def get_sentences(file):
    file.seek(0)
    sentences = []
    for lines in file.readlines():
        sentences += [line.lower().strip().translate(translator) for line in lines.split('.')]

    clean_sentences = []
    for sentence in sentences:
        if len(sentence.split(' ')) > 1:
            clean_sentences.append(sentence)

    return clean_sentences

def get_real_sentences(file):
    file.seek(0)
    sentences = []
    for lines in file.readlines():
        sentences += [line.strip() for line in lines.split('.')]

    clean_sentences = []
    for sentence in sentences:
        if len(sentence.split(' ')) > 1:
            clean_sentences.append(sentence)

    return clean_sentences


def get_blocks(block_size, sentences):
    blocks = []
    i = 0
    while i < len(sentences):
        blocks.append(sentences[i:i + block_size])
        i += block_size

    length = len(blocks[len(blocks) - 1])
    if length < block_size:
        j = length - 1
        while j < block_size - 1:
            blocks[len(blocks) - 1].append('')
            j += 1

    return blocks


def get_real_minimums(minimums, plot, threshold):
    real_minimums = []
    for minimum in minimums:
        min_value = plot[minimum]
        prev_value = None
        succ_value = None
        if minimum - 1 > 0:
            prev_value = plot[minimum - 1]
        if minimum + 1 < len(plot):
            succ_value = plot[minimum + 1]
        if prev_value is not None and (prev_value - min_value) > threshold:
            real_minimums.append(minimum)
        elif succ_value is not None and (succ_value - min_value) > threshold:
            real_minimums.append(minimum)
    return real_minimums


def get_paragraphs(block_size, real_minimums, sentences):
    paragraphs = []
    positions = [0]
    for minimum in real_minimums:
        pos = (block_size * minimum) + block_size
        positions.append(pos)
    if len(sentences) not in positions:
        positions.append(len(sentences))

    for j in range(len(positions) - 1):
        paragraphs.append('. '.join(sentences[positions[j]:positions[j+1]]))
    return paragraphs


if __name__ == '__main__':
    stopword = stopwords.words('english')
    translator = str.maketrans('', '', string.punctuation)
    f = open("./text3.txt", "r")
    real_sentences = get_real_sentences(f)
    sentences = get_sentences(f)
    print(len(real_sentences), real_sentences)
    print(len(sentences), sentences)
    block_size = 3
    if len(sentences) % block_size != 0:
        plot = [0] * (int((len(sentences) / block_size)))
    else:
        plot = [0] * (int((len(sentences) / block_size)) - 1)

    blocks = get_blocks(block_size, sentences)

    for i in range(len(blocks) - 1):
        plot[i] = get_cohesion(blocks[i], blocks[i + 1])

    minimums = argrelextrema(np.array(plot), np.less)[0].tolist()

    real_minimums = get_real_minimums(minimums, plot, 0.13)

    paragraphs = get_paragraphs(block_size, real_minimums, real_sentences)
    print(len(paragraphs), paragraphs)


    x_axis = [[], [], ["1-4", "3-6", "5-8", "7-10", "9-12", "11-14", "13-16", "15-18"], ["1-6", "4-9", "7-12", "10-15", "13-18"], ["1-8", "5-13", "9-17", "13-18"]]
    plt.plot(range(len(plot)), plot)
    plt.savefig(f"plot{block_size}.png")
