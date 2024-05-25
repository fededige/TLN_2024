from nltk import SnowballStemmer
from nltk.corpus import wordnet as wn
from nltk.corpus import framenet as fn, stopwords
from nltk.tokenize import word_tokenize
import nltk
import string

luca_bonamico = [159, 302, 2837, 792, 2668]
luca_cena = [2971, 560, 2840, 797, 1894]
federico = [1683, 366, 1601, 414, 1591]

snow_stm = SnowballStemmer('english')
stopword = stopwords.words('english')


def get_most_frequent_words_fn(frame):
    stopword.append('etc')
    translator = str.maketrans('', '', string.punctuation)
    definitions = [frame.definition.lower().translate(translator)]
    frame_elements = frame.FE.keys()

    for frame_element in frame_elements:
        fed = frame.FE[frame_element]
        definitions.append(fed.definition.lower().translate(translator))

    for lexical_unit in frame.lexUnit.keys():
        lu_def = frame.lexUnit[lexical_unit]['definition']
        if 'COD:' in lu_def:
            definitions.append(lu_def.replace('COD:', '').strip().lower().translate(translator))
        else:
            definitions.append(lu_def.replace('FN:', '').strip().lower().translate(translator))

    most_frequent_words = {}
    for definition in definitions:
        for word in definition.split(' '):
            if word != '' and word not in stopword:
                stemmed_word = snow_stm.stem(word)
                if stemmed_word not in most_frequent_words:
                    most_frequent_words[stemmed_word] = 1
                else:
                    most_frequent_words[stemmed_word] += 1

    most_frequent_words = dict(sorted(most_frequent_words.items(), key=lambda item: item[1], reverse=True))
    return [word for word in most_frequent_words.keys()][:12]


def get_most_frequent_words_wn(synsets):
    stopword.append('etc')
    translator = str.maketrans('', '', string.punctuation)
    definitions = []
    for syn in synsets:
        definitions.append(syn.definition().lower().translate(translator))
        definitions += [ex.lower().translate(translator) for ex in syn.examples()]
        for hypon in syn.hyponyms():
            definitions.append(hypon.definition().lower().translate(translator))
            definitions += [ex.lower().translate(translator) for ex in hypon.examples()]
        for hyper in syn.hypernyms():
            definitions.append(hyper.definition().lower().translate(translator))
            definitions += [ex.lower().translate(translator) for ex in hyper.examples()]

    most_frequent_words = {}
    for definition in definitions:
        for word in definition.split(' '):
            if word != '' and word not in stopword:
                stemmed_word = snow_stm.stem(word)
                if stemmed_word not in most_frequent_words:
                    most_frequent_words[stemmed_word] = 1
                else:
                    most_frequent_words[stemmed_word] += 1
    most_frequent_words = dict(sorted(most_frequent_words.items(), key=lambda item: item[1], reverse=True))

    return [word for word in most_frequent_words.keys()][:12]


def get_contexts_fn(frame, most_frequent_words):
    translator = str.maketrans('', '', string.punctuation)
    contexts = {}
    contexts[frame.name] = [word for word in frame.definition.lower().translate(translator).split(' ') if
                            snow_stm.stem(word) in most_frequent_words]
    frame_elements = frame.FE.keys()
    for frame_element in frame_elements:
        fed = frame.FE[frame_element]
        contexts[frame_element] = [word for word in fed.definition.lower().translate(translator).split(' ') if
                                   snow_stm.stem(word) in most_frequent_words]
    # add lu to context
    for lexical_unit in frame.lexUnit.keys():
        contexts[lexical_unit] = [word for word in frame.lexUnit[lexical_unit]['definition'].lower()
                                  .translate(translator).split(' ') if snow_stm.stem(word) in most_frequent_words]
    for context in contexts.keys():
        contexts[context] = list(set(contexts[context]))
    return contexts


def get_contexts_wn(synsets, most_frequent_words):
    translator = str.maketrans('', '', string.punctuation)
    contexts = {}
    for syn in synsets:
        contexts[syn.name()] = [word for word in syn.definition().lower().translate(translator).split(' ') if
                                snow_stm.stem(word) in most_frequent_words]
        for ex in syn.examples():
            contexts[syn.name()] += [word for word in ex.lower().translate(translator).split(' ') if
                                     snow_stm.stem(word) in most_frequent_words]

    for context in contexts.keys():
        contexts[context] = list(set(contexts[context]))
    return contexts


def bag_of_word(ctx_f, ctx_s):
    ctx_s_stemmed = set([snow_stm.stem(ctx) for ctx in ctx_s])
    ctx_f_stemmed = set([snow_stm.stem(ctx) for ctx in ctx_f])
    return len(ctx_s_stemmed.intersection(ctx_f_stemmed)) + 1


def mapping(framenet_context, wordnet_contexts):
    score = 0
    result = ""
    for synset in wordnet_contexts.keys():
        new_score = bag_of_word(framenet_context, wordnet_contexts[synset])
        if score < new_score:
            score = new_score
            result = synset
    return result


def clean_name(frame_element):
    res = frame_element
    if '.' in frame_element:
        res = frame_element.split('.')[0].split('[')[0].strip()
    if '_' in frame_element or ' ' in frame_element:
        words = word_tokenize(frame_element.replace('_', ' ').lower())
        pos_tag = nltk.pos_tag(words)
        pos = [p[1] for p in pos_tag]
        index = 0
        if 'JJ' in pos:
            if 'NN' in pos:
                index = pos.index('NN')
            elif 'NNS' in pos:
                index = pos.index('NNS')
        elif 'VB' in pos or 'VBD' in pos or 'VBG' in pos or 'VBN' in pos or 'VBP' in pos or 'VBZ' in pos:
            for p in pos:
                if p in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                    index = pos.index(p)
        else:
            if 'NN' in pos:
                index = pos.index('NN')
            elif 'NNS' in pos:
                index = pos.index('NNS')
        res = pos_tag[index][0]
    return res


def map_to_wn(frame):
    mapping_result = {}
    most_frequent_words_fn = get_most_frequent_words_fn(frame)
    framenet_contexts = get_contexts_fn(frame, most_frequent_words_fn)
    for frame_element in framenet_contexts.keys():
        element_synsets = wn.synsets(clean_name(frame_element))
        most_frequent_words_wn = get_most_frequent_words_wn(element_synsets)
        wordnet_contexts = get_contexts_wn(element_synsets, most_frequent_words_wn)
        mapping_result[frame_element] = mapping(framenet_contexts[frame_element], wordnet_contexts)
    return mapping_result


def check_accuracy(mapping_gold, frame_mapped):
    count_correct = 0
    for key in frame_mapped.keys():
        if key in mapping_gold.keys():
            if frame_mapped[key] == mapping_gold[key]:
                count_correct += 1
    return count_correct / len(mapping_gold)


if __name__ == '__main__':
    luca_bonamico_frame = []
    luca_cena_frame = []
    federico_frame = []

    for frame_id in luca_bonamico:
        luca_bonamico_frame.append(fn.frame(frame_id))

    for frame_id in luca_cena:
        luca_cena_frame.append(fn.frame(frame_id))

    for frame_id in federico:
        federico_frame.append(fn.frame(frame_id))

    luca_bonamico_frame_mapped = []
    for luca_bonamico_f in luca_bonamico_frame:
        luca_bonamico_frame_mapped.append(map_to_wn(luca_bonamico_f))

    luca_cena_frame_mapped = []
    for luca_cena_f in luca_cena_frame:
        luca_cena_frame_mapped.append(map_to_wn(luca_cena_f))

    federico_frame_mapped = []
    for federico_f in federico_frame:
        federico_frame_mapped.append(map_to_wn(federico_f))

    print(luca_bonamico_frame_mapped)
    print(luca_cena_frame_mapped)
    print(federico_frame_mapped)

    grooming_gold = {
        'Grooming': 'groom.v.03',
        'Result': 'consequence.n.01',
        'Agent': 'agentive_role.n.06',
        'Patient': 'affected_role.n.01',
        'Instrument': 'instrument.n.01',
        'Body_part': 'body.n.01',
        'Medium': '',
        'Frequency': 'frequency.n.01',
        'Manner': 'manner.n.01',
        'Time': 'time.n.01',
        'Place': 'topographic_point.n.01',
        'Duration': 'duration.n.01',
        'Purpose': 'purpose.n.01',
        'Means': 'mean.v.07',
        'bathe.v': 'bathe.v.03',
        'wash.v': 'wash.v.02',
        'lave.v': 'wash.v.02',
        'shower.v': 'shower.v.03',
        'pluck.v': 'pluck.v.01',
        'floss.v': 'floss.v.01',
        'shave.v': 'shave.v.01',
        'wax.v': 'wax.v.01',
        'comb.v': 'comb.v.01',
        'shampoo.v': 'shampoo.v.01',
        'manicure.v': 'manicure.v.01',
        'pedicure.n': 'pedicure.n.01',
        'ablution.n': 'ablution.n.01',
        'moisturize.v': 'humidify.v.01',
        'soap.v': 'soap.v.1',
        'cleanse.v': 'cleanse.v.01',
        'facial.n': 'facial.n.02',
        'manicure.n': 'manicure.n.01',
        'groom.v': 'dress.v.15',
        'brush [teeth].v': 'brush.v.03',
        'brush [hair].v': 'brush.v.01',
        'plait.v': 'braid.v.01',
        'file.v': 'file.v.02',
    }

    becoming_gold = {
        'Becoming': 'become.v.02',
        'Place': 'topographic_point.n.01',
        'Time': 'time.n.01',
        'Duration_of_final_state': 'duration.n.01',
        'Manner': 'manner.n.01',
        'Entity': 'entity.n.01',
        'Final_quality': 'quality.n.03',
        'Final_category': 'class.n.01',
        'Transitional_period': 'time_period.n.01',
        'Initial_state': 'state.n.02',
        'Circumstances': 'circumstances.n.01',
        'Initial_category': 'class.n.01',
        'Group': 'group.n.01',
        'Explanation': 'explanation.n.01',
        'become.v': 'become.v.02',
        'turn.v': 'become.v.02',
    }

    desiring_gold = {
        'Desiring': 'desire.v.01',
        'Experiencer': '',
        'Event': 'event.n.02',
        'Focal_participant': 'participant.n.01',
        'Degree': 'degree.n.01',
        'Explanation': 'explanation.n.01',
        'Purpose_of_event': 'function.n.02',
        'Location_of_event': 'location.n.01',
        'Duration': 'duration.n.01',
        'Attempting_and_resolving_scenario': '',
        'want.v': 'desire.v.01',
        'desire.v': 'desire.v.01',
        'desire.n': 'desire.n.02',
        'desirous.a': 'desirous.a.01',
        'lust.n': 'crave.v.01',
        'lust.v': 'crave.v.01',
        'hunger.v': 'crave.v.01',
        'hunger.n': 'hunger.n.02',
        'hungry.a': ' athirst.a.01',
        'thirst.n': 'hunger.n.02',
        'thirst.v': 'crave.v.02',
        'thirsty.a': 'athirst.a.01',
        'long.v': 'hanker.v.02',
        'longing.n': 'longing.n.01',
        'urge.n': 'urge.n.02',
        'aspire.v': 'draw_a_bead_on.v.02',
        'wish.n': 'wish.n.02',
        'wish (that).v': 'wish.v.01',
        'eager.a': 'eager.a.01',
    }

    accuracy = check_accuracy(grooming_gold, luca_bonamico_frame_mapped[0])
    print("accuracy: ", accuracy, len(grooming_gold))
    print()
    print()
    accuracy = check_accuracy(becoming_gold, luca_cena_frame_mapped[0])
    print("accuracy: ", accuracy, len(becoming_gold))
    print()
    print()
    accuracy = check_accuracy(desiring_gold, federico_frame_mapped[1])
    print("accuracy: ", accuracy, len(desiring_gold))
