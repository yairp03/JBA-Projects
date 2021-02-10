from nltk import WhitespaceTokenizer, trigrams
from collections import defaultdict, Counter
from random import choice, choices

EXIT = 'exit'
GOOD_WORD = 1
BAD_WORD = 0
END_SENTENCE = -1
SENTENCE_ENDINGS = '.', '!', '?'
MIN_SENTENCE_LEN = 5
BAD_TRIES_TIMEOUT = 10


def main():
    file_name = input()
    tokenizer = WhitespaceTokenizer()
    with open(file_name, "r", encoding="utf-8") as f:
        tokens = tokenizer.tokenize(f.read())
    trigrms = list(trigrams(tokens))
    trigrams_freq = defaultdict(Counter)
    for t in trigrms:
        trigrams_freq[f"{t[0]} {t[1]}"][t[2]] += 1

    for _ in range(10):
        print(*generate_sentence(trigrams_freq))


def generate_sentence(trigrams_freq):
    sentence = []
    head1, head2 = 'a', ''
    while not (head1[0].isupper() and head1[-1] not in SENTENCE_ENDINGS):
        head1, head2 = choice(list(trigrams_freq.keys())).split(' ')
    sentence.extend((head1, head2))
    bad_tries = 0
    while True:
        head = f'{head1} {head2}'
        tail = choices(list(trigrams_freq[head].keys()), trigrams_freq[head].values())[0]
        res = check_word(tail, sentence)
        if not res:
            bad_tries += 1
            if bad_tries >= BAD_TRIES_TIMEOUT:
                return generate_sentence(trigrams_freq)
            continue
        bad_tries = 0
        sentence.append(tail)
        if res == END_SENTENCE:
            break
        head1, head2 = head2, tail
    return sentence


def check_word(tail, sentence):
    if sentence[-1][-1] in SENTENCE_ENDINGS:
        return GOOD_WORD if tail[0].isupper() and tail[-1] not in SENTENCE_ENDINGS else BAD_WORD
    if tail[-1] in SENTENCE_ENDINGS and len(sentence) >= MIN_SENTENCE_LEN - 1:
        return END_SENTENCE
    return GOOD_WORD


if __name__ == '__main__':
    main()
