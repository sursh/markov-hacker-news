#!/usr/bin/python -tt

import sys
import json
import re
import collections
import numpy
import string
import cPickle as pickle

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
    grams = []
    for idx, item in enumerate(tokens[:-2]):
      grams.append((item, tokens[idx+1], tokens[idx+2]))
    return grams

  def generateMatrix(self, filename):
    ''' Run through the list of trigrams and add them to the occurence matrix '''

    self.matrix = {}

    try: # load as pickle

      with open('matrix.p', 'rb') as f:
        self.matrix = pickle.load(f)

    except: # interpret file as newline separated headlines

      headlines = self.read(filename)

      for headline in headlines:

        trigrams = self.generateTrigrams(headline)

        for first_word, second_word, third_word in trigrams:
          self.matrix.setdefault( (first_word, second_word), collections.defaultdict(int)) 
          self.matrix[(first_word, second_word)][third_word] += 1

      print("DUMPING %d" % len(self.matrix))
      pickle.dump(self.matrix, open("matrix.p", "wb"))

  def generateNextWord(self, prev_word, current_word):

    conditional_words = self.matrix[ (prev_word, current_word) ]
    words, counts = zip(*conditional_words.items())

    # pick one of the possibilities, with probability weighted by frequency in training corpus
    cumcounts = numpy.cumsum(counts)
    coin = numpy.random.randint(cumcounts[-1])
    for index, item in enumerate(cumcounts):
      if item > coin:
        return words[index]


  def generateParagraph(self, seed2 = 'i', seed1 = '^',):
    
    prev_word = seed1
    current_word = seed2
    paragraph = [ seed1 ]

    while (current_word != '$' and len(paragraph) < 20): # TODO: more graceful ending
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

  if len(sys.argv) != 3:
    print 'usage: ./markov.py inputFile numOfResults'
    sys.exit(1)

  filename = sys.argv[1]
  
  m = Markov()
  m.generateMatrix(filename)

  for i in xrange(int(sys.argv[2])):
    print m.generateParagraph('how')
    print m.generateParagraph('why')

if __name__ == '__main__':
  main()
