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
        if minimum - 1 >= 0:
            prev_value = plot[minimum - 1]
        if minimum + 1 < len(plot):
            succ_value = plot[minimum + 1]

        if prev_value is not None:
            print(f"Delta in {minimum} between {prev_value} and {min_value} is:", (prev_value - min_value))
        elif succ_value is not None:
            print(f"Delta in {minimum} between {succ_value} and {min_value} is: ", (succ_value - min_value))
        else:
            print("No Delta computed")

        if prev_value is not None and (prev_value - min_value) > threshold:
            real_minimums.append(minimum)
        elif succ_value is not None and (succ_value - min_value) > threshold:
            real_minimums.append(minimum)
    return real_minimums


def get_segments(block_size, real_minimums, sentences):
    segments = []
    positions = [0]
    for minimum in real_minimums:
        pos = (block_size * minimum) + block_size
        positions.append(pos)
    if len(sentences) not in positions:
        positions.append(len(sentences))

    for j in range(len(positions) - 1):
        segments.append(sentences[positions[j]:positions[j + 1]])
    return segments


# def get_exact_cut(real_minimums, blocks):
#     for minimum in real_minimums:
#         new_block = []
#         for s in blocks[minimum]:
#             new_block.append(s)
#         for s in blocks[minimum + 1]:
#             new_block.append(s)
#
#         plot = [0.0] * (len(new_block) - 1)
#
#         for i in range(len(new_block) - 1):
#             plot[i] = get_cohesion([new_block[i]], [new_block[i + 1]])
#             print(plot[i])
#             print("similarity between:")
#             print("\t", new_block[i])
#             print("and")
#             print("\t", new_block[i + 1])
#             print()


if __name__ == '__main__':
    stopword = stopwords.words('english')
    translator = str.maketrans('', '', string.punctuation)
    text_name = "text1"
    f = open(f"./{text_name}.txt", "r")
    real_sentences = get_real_sentences(f)
    sentences = get_sentences(f)
    block_size = 4
    if len(sentences) % block_size != 0:
        plot = [0.0] * (int((len(sentences) / block_size)))
    else:
        plot = [0.0] * (int((len(sentences) / block_size)) - 1)


    blocks = get_blocks(block_size, sentences)

    for i in range(len(blocks) - 1):
        plot[i] = get_cohesion(blocks[i], blocks[i + 1])

    minimums = argrelextrema(np.array(plot), np.less)[0].tolist()
    threshold = 0.166
    real_minimums = get_real_minimums(minimums, plot, threshold)

    segments = get_segments(block_size, real_minimums, sentences)

    x = range(len(plot))
    plt.plot(x, plot)
    plt.xticks(x)
    plt.title(f"Block Size = {block_size}, threshold = {threshold}, number of sentences = {len(sentences)}")
    for minimum in real_minimums:
        plt.axvline(x=minimum, color='r')
    plt.savefig(f"{text_name}_{block_size}_plot.png")

    for seg in segments:
        for s in seg:
            print(s)
        print()
    print(len(segments))

    # for i in range(len(blocks)):
    #     print(blocks[i])
    #     print(i)
    #     print()


    # test = get_exact_cut(real_minimums, blocks)

    # segment_num = 0
    # last_block = []
    # for seg in segments:
    #     plt.clf()
    #     if len(seg) % block_size != 0:
    #         plot = [0.0] * (int((len(seg) / block_size)))
    #     else:
    #         plot = [0.0] * (int((len(seg) / block_size)) - 1)
    #     blocks = get_blocks(block_size, seg)
    #     for i in range(len(blocks) - 1):
    #         plot[i] = get_cohesion(blocks[i], blocks[i + 1])
    #     if len(last_block) > 0:
    #         plot.insert(0, get_cohesion(last_block, blocks[0]))
    #     print(plot)
    #     last_block = blocks[len(blocks) - 1]
    #     minimums = argrelextrema(np.array(plot), np.less)[0].tolist()
    #     real_minimums = get_real_minimums(minimums, plot, 0.05)
    #     segments = get_segments(block_size, real_minimums, seg)
    #     segment_num += 1
    # plt.plot(range(len(plot)), plot)
    # for minimum in real_minimums:
    #     plt.axvline(x=minimum, color='r')
    # plt.savefig(f"segment-{segment_num}.png")
    # print()
    # print()
