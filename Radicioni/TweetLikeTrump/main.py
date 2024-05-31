import random as r


def count_word_freq(tweets):
    word_frequency = {}
    for tweet in tweets:
        for word in tweet.split(' '):
            if word not in word_frequency:
                word_frequency[word] = 1
            else:
                word_frequency[word] += 1
    return word_frequency


def count_bigram_freq(tweets):
    bigram_frequency = {}
    for tweet in tweets:
        i = 0
        words = tweet.split(' ')
        while i < len(words) - 1:
            bigram = f"{words[i]} {words[i + 1]}"
            if bigram not in bigram_frequency:
                bigram_frequency[bigram] = 1
            else:
                bigram_frequency[bigram] += 1
            i += 1
    return bigram_frequency


def count_trigram_freq(tweets):
    trigram_frequency = {}
    for tweet in tweets:
        i = 0
        words = tweet.split(' ')
        while i < len(words) - 2:
            trigram = f"{words[i]} {words[i + 1]} {words[i + 2]}"
            if trigram not in trigram_frequency:
                trigram_frequency[trigram] = 1
            else:
                trigram_frequency[trigram] += 1
            i += 1
    return trigram_frequency


def bigram_mle(word, previous_word):  # word = loser!, previous_word = total. => P("loser!" | "total")
    freq_first_word = word_freq[previous_word]
    freq_bigram = bigram_freq[f"{previous_word} {word}"]
    return freq_bigram / freq_first_word


def trigram_mle(word, previous_words):  # word = loser!, previous_word = a total. => P("loser!" | "a total")
    freq_bigram = bigram_freq_better[previous_words]
    freq_trigram = trigram_freq[f"{previous_words} {word}"]
    return freq_trigram / freq_bigram


def compute_bigram_probabilities():
    bigram_probabilities = {}
    for key in bigram_freq.keys():
        first_word, second_word = key.split(' ')
        if first_word not in bigram_probabilities:
            bigram_probabilities[first_word] = [[second_word, bigram_mle(second_word, first_word)]]
        else:
            bigram_probabilities[first_word].append([second_word, bigram_mle(second_word, first_word)])
    return bigram_probabilities


def compute_trigram_probabilities():
    trigram_probabilities = {}
    for key in trigram_freq.keys():
        first_word, second_word, third_word = key.split(' ')
        bigram = f"{first_word} {second_word}"
        if bigram not in trigram_probabilities:
            trigram_probabilities[bigram] = [[third_word, trigram_mle(third_word, bigram)]]
        else:
            trigram_probabilities[bigram].append([third_word, trigram_mle(third_word, bigram)])
    return trigram_probabilities


def predict_next_word(param):
    return r.choices([word[0] for word in param], weights=[prob[1] for prob in param])[0]


def generate_tweet():
    tweet = "<s>"
    predicted = "<s>"
    while predicted != '</s>':
        predicted = predict_next_word(bigram_probabilities[predicted])
        tweet += f" {predicted}"
    return tweet


def generate_tweet_trigram():
    tweet = "<s> <s>"
    last_bigram = "<s> <s>"
    while last_bigram != "</s> </s>":
        predicted = predict_next_word(trigram_probabilities[last_bigram])
        tweet += f" {predicted}"
        words = last_bigram.split(" ")
        last_bigram = f"{words[1]} {predicted}"
    return tweet


if __name__ == '__main__':
    corpus = "/home/federico/informatica/TLN/Radicioni/TweetLikeTrump/trump_twitter_archive/tweets.csv"
    f = open(corpus, "r", encoding="utf-8")
    f.readline()
    tweets_bigram = []
    tweets_bigram_better = []
    tweets_trigram = []
    for line in f.readlines():
        tweets_bigram.append(f"<s> {line.split(',')[1].strip()} </s>")
        tweets_bigram_better.append(f"<s> <s> {line.split(',')[1].strip()} </s> </s>")
        tweets_trigram.append(f"<s> <s> {line.split(',')[1].strip()} </s> </s>")

    word_freq = count_word_freq(tweets_bigram)
    bigram_freq = count_bigram_freq(tweets_bigram)
    bigram_freq_better = count_bigram_freq(tweets_bigram_better)
    trigram_freq = count_trigram_freq(tweets_trigram)

    bigram_probabilities = compute_bigram_probabilities()

    result = generate_tweet()
    print("bi-gram model: ", result.replace('<s> ', '').replace(' </s>', ''))

    trigram_probabilities = compute_trigram_probabilities()

    result_trigram = generate_tweet_trigram()
    print("tri-gram model: ", result_trigram.replace('<s> ', '').replace(' </s>', ''))
