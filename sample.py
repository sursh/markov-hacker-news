import time
from collections import defaultdict
from collections import Counter
import numpy as np
import re

split_re = re.compile('[!\t \-\(\)?:/\r\n]+')
matrix = None

def get_trigrams(tokens):
    trigrams = []
    for idx, token in enumerate(tokens[:-2]):
        trigrams.append( (token, tokens[idx+1], tokens[idx+2]) )
        
    return trigrams

def get_headlines(fname):
    with open(fname) as f:
        for line in f:
            yield ['^'] + [w for w in split_re.split(line.lower())][:-1] + ['$']

def sample_next(bigram):
    '''
    Samples the next word given a bigram
    '''
    
    words  = []
    counts = []

    for (a, b, word), count in matrix.iteritems():
        words.append(word)
        counts.append(count)

    if len(counts) == 0:
        raise ValueError('No trigrams starting with %s-%s' % bigram)

    idx = sample_idx_from(counts)

    return words[idx]

def sample_idx_from(frequencies):
    '''
    Samples an index from a list of frequencies
    with probability proportional to the frequency
    of the array index.
    '''

    cdf = np.cumsum(frequencies) / np.sum(frequencies, dtype=float)
    coin = np.random.random()
    for index, item in enumerate(cdf):
        if item >= coin:
            return index

def main(fname):

    global matrix

    print 'loading matrix'
    headlines = get_headlines(fname)
    trigrams  = (trigram for headline in headlines for trigram in get_trigrams(headline))
    matrix = Counter(trigrams)

    matrix = filter(lambda (k,v): v > 1, matrix.iteritems())
    time.sleep(50)

    #for j in xrange(10):
    #    bigram = ('how', 'the')

    #    print bigram,
    #    for i in xrange(8):
    #        w = sample_next(bigram)
    #        print w,
    #        bigram = bigram[1], (w,)

if __name__ == '__main__':
    main('hnfull.txt')
