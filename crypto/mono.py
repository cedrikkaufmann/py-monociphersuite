import string
import random
import secrets

from crypto.io import IfStream
from crypto.analysis.statistics import TextStatistics
from crypto.analysis.statistics import NGramAnalyzer


def swap(str, indexA, indexB):
    tmp = list(str)
    tmp[indexA] = tmp[indexB]
    tmp[indexB] = str[indexA]
    return ''.join(tmp)


def randomExclusiveSet(upperBound):
    a = 0
    b = 0

    while a == b:
        a = secrets.randbelow(26)
        b = secrets.randbelow(26)

    return {a, b}


class Cipher:

    def __init__(self, key):
        super().__init__()

        # parse and save the key
        self.parseKey(key)

    @staticmethod
    def generateKey():
        """returns a random permutation of the alphabet"""

        # get lowercase alphabetic characters
        alphabet = list(string.ascii_lowercase)

        # shuffle letters
        random.shuffle(alphabet)

        # return shuffled key
        return ''.join(alphabet)

    def parseKey(self, key):
        """parses the key and save it as encryption/decryption dictionary"""

        # check if key is string
        if type(key) != str:
            raise Exception(f'Key has to be of type string but given: {type(key)}')

        # check if keylength is correct
        if len(key) != 26:
            k = ''.join(sorted(list(key)))
            raise Exception(f'Invalid keylength: {len(key)}, for key: {k}')

        # convert key to lowercase
        key = key.lower()

        # create empty dictionary
        self._keyDict = {}
        self._inverseKeyDict = {}

        # iterate over key and create encryption/decryption dictionary
        for i, c in enumerate(key):
            # check if given char is actually a letter
            if not c.isalpha():
                raise Exception(f'Key has to contain alphabetic characters only: {c}')

            # get letter from iteration index
            k = chr(i + 97)

            # check if letter alraedy assigned
            if dict.get(self._keyDict, k):
                raise Exception(f'Character should appear only once: {c}')

            # save to dictionary
            self._keyDict[k] = c
            self._inverseKeyDict[c] = k

    def encrypt(self, payload):
        """encrypts the given payload"""

        # ciphertext
        cipher = ''

        # iterate over payload and encrypt
        for c in payload:
            cipher += self._keyDict[c]

            # return encrypted payload
        return cipher

    def decrypt(self, payload):
        """decrypts the given payload"""

        # plaintext
        plain = ''

        # ieterate over payload and decrypt
        for c in payload:
            plain += self._inverseKeyDict[c]

        # return decrypted payload
        return plain

    @staticmethod
    def deriveKey(payload, refDataFile):
        """derives a key from ciphertext"""

        # Phase 1: Derive initial key from text statistics

        # Load reference data
        ref = IfStream(refDataFile)

        # build reference and cipher statistics
        refStats = TextStatistics(ref.data)
        cipherStats = TextStatistics(payload)

        # get unigram distribution
        cipherUnigramDist = cipherStats('unigrams')
        refUnigramDist = refStats('unigrams')

        # expand cipher unigrams if some letters are missing
        usedLetters = {}

        for l in string.ascii_lowercase:
            usedLetters[l] = False

        for l in cipherUnigramDist:
            usedLetters[l] = True

        for l in usedLetters:
            if not usedLetters[l]:
                refUnigramDist[l] = -10

        # sort distributions according to most likely letters
        sortedRefUnigramDist = sorted(refUnigramDist.items(), key=lambda u: u[1], reverse=True)
        sortedCipherUnigramDist = sorted(cipherUnigramDist.items(), key=lambda u: u[1], reverse=True)

        # derive a first key by unigram stats assignment
        subDic = {}

        for n in range(26):
            c = sortedRefUnigramDist[n][0]

            if n <= len(sortedCipherUnigramDist) - 1:
                usedLetters[c] = True
                subDic[c] = sortedCipherUnigramDist[n][0]
            else:
                subDic[c] = c

        key = ''
        for c in string.ascii_lowercase:
            key += subDic[c]

        # Phase 2: Optimize initial key by key swapping and maximum likelihood method
        analyzer = NGramAnalyzer(refStats)
        counter = 0  # convergence counter

        # decrypt with current best-key
        c = Cipher(key)
        plain = c.decrypt(payload)

        # calculate fitness score by weighted likelihoods
        fitness = 10 * analyzer.logLikelihood(plain, 'unigrams') + analyzer.logLikelihood(plain, 'bigrams') + \
                  300 * analyzer.logLikelihood(plain, 'quadgrams')
        
        while counter < 2000:
            # generate random indices
            randomIndices = randomExclusiveSet(26)

            # now swap random letters in key
            newKey = swap(key, randomIndices.pop(), randomIndices.pop())

            # decrypt ciphertext with new key and calculate new fitness score
            cNew = Cipher(newKey)
            plain = cNew.decrypt(payload)
            fitnessNew = 10 * analyzer.logLikelihood(plain, 'unigrams') + analyzer.logLikelihood(plain, 'bigrams') + \
                         300 * analyzer.logLikelihood(plain, 'quadgrams')

            # if key produces better fitness, save new key as best-key
            if fitnessNew > fitness:
                key = newKey
                fitness = fitnessNew
                counter = 0
            else:
                # no improvement, count up convergence counter
                counter += 1

        # return key
        return key
