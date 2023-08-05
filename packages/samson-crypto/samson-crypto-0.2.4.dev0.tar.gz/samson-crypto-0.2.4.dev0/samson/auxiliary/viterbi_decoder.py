# from samson.auxiliary.english_data import ENGLISH_ONE_GRAMS, ENGLISH_TWO_GRAMS
from math import log10

from samson.auxiliary.lazy_loader import LazyLoader
_eng_data = LazyLoader('_eng_data', globals(), 'samson.auxiliary.english_data')

# http://practicalcryptography.com/cryptanalysis/text-characterisation/word-statistics-fitness-measure/
class ViterbiDecoder(object):
    """
    Statistical model that decodes non-delimited English text into tokens using maximum likelihood metrics.
    """

    def __init__(self):
        self.Pw = {}
        self.N = 1024908267229 ## Number of tokens

        # Calculate first order log probabilities
        for key in _eng_data.ENGLISH_ONE_GRAMS.keys():
            self.Pw[key.upper()] = log10(float(_eng_data.ENGLISH_ONE_GRAMS[key]) / self.N)


        # Get second order word model
        self.Pw2 = {}

        # Calculate second order log probabilities
        for key in _eng_data.ENGLISH_TWO_GRAMS.keys():
            word1 = key.split()[0].upper()

            if word1 not in self.Pw:
                self.Pw2[key.upper()] = log10(float(_eng_data.ENGLISH_TWO_GRAMS[key]) / self.N)
            else:
                self.Pw2[key.upper()] = log10(float(_eng_data.ENGLISH_TWO_GRAMS[key]) / self.N) - self.Pw[word1]


        # Precalculate the probabilities we assign to words not in our dict, L is length of word
        self.unseen = [log10(10. / (self.N * 10**L)) for L in range(50)]




    def cPw(self, word: str, prev: str='<UNK>') -> float:
        """
        Calculates the conditional word probability.

        Parameters:
            word (str): Current word.
            prev (str): Previous word.
        
        Returns:
            float: Log probability of `word` based on `prev`.
        """
        second_order_word = (prev + ' ' + word)

        if word not in self.Pw:
            return self.unseen[len(word)]

        elif second_order_word not in self.Pw2:
            return self.Pw[word]

        else:
            return self.Pw2[second_order_word]




    def score(self, text: str, max_word_len=20) -> (float, list):
        """
        Scores and tokenizes the text according to the maximum likelihood.

        Parameters:
            text         (str): Text to tokenize/decode.
            max_word_len (int): Maximum token length.
        
        Returns:
            (float, list): Most probable decoding as (score, token_list).
        """
        text = text.upper()

        prob = [[-99e99] * max_word_len for _ in range(len(text))]
        strs = [[''] * max_word_len for _ in range(len(text))]

        for j in range(max_word_len):
            prob[0][j] = self.cPw(text[:j+1])
            strs[0][j] = [text[:j+1]]

        for i in range(1,len(text)):
            for j in range(max_word_len):
                if i+j+1 > len(text): break
                candidates = [(prob[i-k-1][k] + self.cPw(text[i: i+j+1], strs[i-k-1][k][-1]),
                               strs[i-k-1][k] + [text[i: i+j+1]]) for k in range(min(i, max_word_len))]

                prob[i][j], strs[i][j] = max(candidates)

        ends = [(prob[-i-1][i], strs[-i-1][i]) for i in range(min(len(text), max_word_len))]
        return max(ends)
