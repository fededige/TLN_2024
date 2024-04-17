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


if __name__ == '__main__':
    f = open("./trump_twitter_archive/tweets.csv", "r")
    print(f.readline())
    tweets_bigram = []
    tweets_trigram = []
    for line in f.readlines():
        tweets_bigram.append(f"<s> {line.split(',')[1].strip()} </s>")
        tweets_trigram.append(f"<s> <s> {line.split(',')[1].strip()} </s> </s>")

    word_freq = count_word_freq(tweets_bigram)
    bigram_freq = count_bigram_freq(tweets_bigram)
    trigram_freq = count_trigram_freq(tweets_trigram)
    print(trigram_freq)

    for key in trigram_freq.keys():
        if trigram_freq[key] > 3:
            print(f"{key}: {trigram_freq[key]}")

    # calcolo probabilità trigramma "a total loser!"
    freq_a_total = bigram_freq['a total']
    freq_a_total_loser = trigram_freq['a total loser!']
    loser_given_a_total = freq_a_total_loser / freq_a_total

    # calcolo probabilità bigramma "total loser!"
    freq_total = word_freq['total']
    freq_total_loser = bigram_freq['total loser!']
    loser_given_total = freq_total_loser / freq_total
    print(loser_given_total)
