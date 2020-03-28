from collections import Counter
import math

class Tokenizer:
    @staticmethod
    def nGrams(text, mode='unigrams'):
        """returns the tokenized text"""

        # create unigrams
        tokens = list(text)

        # simply return unigrams
        if mode == 'unigrams':
            return tokens

        # create bigrams and return them
        if mode == 'bigrams':
            return [''.join(tokens[i:i + 1]) for i in range(0, len(tokens) - 1)]

        # create quadgrams and return them
        if mode == 'quadgrams':
            return [(''.join(tokens[i:i + 4])) for i in range(0, len(tokens) - 4)]


class TextStatistics:

    def __init__(self, text):
        super().__init__()
        self._text = text
        self._unigramDist = self._distribution('unigrams')
        self._bigramDist = self._distribution('bigrams')
        self._quadgramDist = self._distribution('quadgrams')

    def __call__(self, mode='unigrams'):
        if mode == 'unigrams':
            return self._unigramDist

        if mode == 'bigrams':
            return self._bigramDist

        if mode == 'quadgrams':
            return self._quadgramDist

    def _distribution(self, mode='unigrams'):
        """calculates the ngram distribution"""
        # create ngrams
        if mode == 'unigrams':
            ngrams = Tokenizer.nGrams(self._text, mode)
        elif mode == 'bigrams':
            ngrams = Tokenizer.nGrams(self._text, mode)
        elif mode == 'quadgrams':
            ngrams = Tokenizer.nGrams(self._text, mode)

        # count ngrams
        counter = Counter(ngrams)
        s = sum(counter.values())

        dist = {}

        # calculate distribution in log domain
        for e in counter:
            dist[e] = math.log10(counter[e] / s)

        return dist


class NGramAnalyzer:

    def __init__(self, referenceStatistics):
        super().__init__()
        self._ref = referenceStatistics

    def logLikelihood(self, text, mode='unigrams'):
        """returns the log-likelihood for a given text"""
        refDist = self._ref(mode)
        fitnessScore = 0.0

        # get ngrams from text
        ngrams = Tokenizer.nGrams(text, mode)

        # calculate score in log domain
        for ngram in ngrams:
            logProb = dict.get(refDist, ngram)

            if not logProb:
                fitnessScore -= 10
            else:
                fitnessScore += logProb

        return fitnessScore
