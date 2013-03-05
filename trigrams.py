#!/usr/bin/python -tt

import sys
import json
import re
from collections import defaultdict
import numpy
import string
import cPickle as pickle
import twitterclient

class Markov(object):

  def read(self, filename):
    with open(filename) as f:
      headlines = f.readlines()

    headlines = map(str.lower, headlines)
    headlines = map(str.strip, headlines)
    headlines = [re.split('\s+', headline) for headline in headlines]
    for headline in headlines:
      if headline[-1] == '': del(headline[-1]) # clear lingering null entries
      if headline[0] == '': del(headline[0])

    headlines = [['^'] + headline + ['$'] for headline in headlines]

    return headlines

  def generateTrigrams(self, tokens):
    ''' Create a list of tuples, where each tuple is a trigram '''
    
    print "making trigrams"

    grams = []
    for idx, item in enumerate(tokens[:-2]):
      grams.append((item, tokens[idx+1], tokens[idx+2]))
    return grams

  def generateMatrix(self, filename):
    ''' Run through the list of trigrams and add them to the occurence matrix '''

    self.matrix = {}
    self.bigrams = defaultdict(list)

    try: # load matrix from pickle file
      with open('matrix.p', 'rb') as f:
        self.matrix = pickle.load(f)

    except: # construct matrix from text file

      headlines = self.read(filename)

      print "constructing matrix"

      for headline in headlines:

        trigrams = self.generateTrigrams(headline)

        for trigram in trigrams:
          bigram = trigram[:2]
          current_word = trigram[-1]

          (old_count, seenBefore) = self.matrix.get(trigram, (0, False))

          if not seenBefore:
            self.bigrams[bigram].append(current_word)

          self.matrix[trigram] = (1 + old_count, True)

      #print("Pickling %d" % len(self.matrix))
      #pickle.dump(self.matrix, open("matrix.p", "wb"))

  def generateNextWord(self, prev_word, current_word):

    bigram = (prev_word, current_word)

    words = []
    counts = []

    for word in self.bigrams[bigram]:
      trigram = bigram + (word,)
      counts = self.matrix[trigram]
      words.append(word)
      counts.append(counts)

    # pick one of the possibilities, with probability weighted by frequency in training corpus
    cumcounts = numpy.cumsum(counts)
    coin = numpy.random.randint(cumcounts[-1])
    for index, item in enumerate(cumcounts):
      if item > coin:
        print words[index]
        return words[index]


  def generateParagraph(self, seed2 = 'i', seed1 = '^',):
    
    prev_word = seed1
    current_word = seed2
    paragraph = [ seed1 ]

    while (current_word != '$' and len(paragraph) < 20): 
      paragraph.append(current_word)
      prev_word, current_word = current_word, self.generateNextWord( prev_word, current_word )

    paragraph = ' '.join(paragraph[1:])  # strip off leading caret
    return string.capwords(paragraph)


  def __str__(self):
    s = ''
    for word, cfd in self.matrix.iteritems():
      for word2, count in cfd.iteritems():
        s += '%s %s: %d\n' % (word, word2, count)
    return s

def main():

  if len(sys.argv) != 2:
    print 'usage: ./markov.py inputFile'
    sys.exit(1)

  filename = sys.argv[1]
  
  m = Markov()
  m.generateMatrix(filename)

  while True:
    tweet = m.generateParagraph('how') # todo: new seed
    if len(tweet) < 120:
      break

  print("Tweeting %d" % tweet)
  twitterclient.postTweet(tweet)

if __name__ == '__main__':
  main()
