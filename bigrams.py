#!/usr/bin/python -tt

import sys
import json
import re
import collections
import numpy

class Markov(object):
  """docstring for ClassName"""

  def read(self, filename):
    with open(filename) as f:
      headlines = f.readlines()

    # entirefile = json.load(f)
    # headlines = [entry['title'] for entry in entirefile["items"]]

    headlines = map(str.lower, headlines) # TODO: keep proper nouns
    headlines = map(str.strip, headlines)
    headlines = [re.split('\W+', headline) for headline in headlines] # TODO: fix regex
    for headline in headlines:
      if headline[-1] == '': del(headline[-1]) # EMBRACE THE JANK

    headlines = [['^'] + headline + ['$'] for headline in headlines]

    return headlines

  def generateBigrams(self, tokens):
    grams = []
    for idx, item in enumerate(tokens[:-1]):
      grams.append((item, tokens[idx+1]))
    return grams

  def generateMatrix(self, filename):
    # read in headlines, generate tuples

    # initializes a 2D dictionary with default values of 0
    self.matrix = {} 

    headlines = self.read(filename)

    for headline in headlines:
      bigrams = self.generateBigrams(headline)
      self.updateMatrix(bigrams)


  def updateMatrix(self, bigrams):
    '''Take a list of (w1, w2) bigrams
    and updates the counts stored of count of word2 following word1
    '''
    for prev_word, current_word in bigrams:
      self.matrix.setdefault(prev_word, collections.defaultdict(int))
      self.matrix[prev_word][current_word] += 1
  

  def generateNextWord(self, prev_word):

    conditional_words = self.matrix[prev_word]
    words, counts = zip(*conditional_words.items())
    cumcounts = numpy.cumsum(counts)

    coin = numpy.random.randint(cumcounts[-1])

    for index, item in enumerate(cumcounts): 
      if item > coin: 
        return words[index]


  def generateParagraph(self, seed_word='why'):
    
    current_word = seed_word
    paragraph = ['why']
    while (current_word != '$' and len(paragraph) < 20): # TODO: more graceful ending
      paragraph.append(current_word)
      current_word = self.generateNextWord(current_word)

    return ' '.join(paragraph[1:]) # strip off caret


  def __str__(self):
    s = ''
    for word, cfd in self.matrix.iteritems():
      for word2, count in cfd.iteritems():
        s += '%s %s: %d\n' % (word, word2, count)
    return s

def main():

  if len(sys.argv) != 3:
    print 'usage: ./markov.py file num'
    sys.exit(1)

  filename = sys.argv[1]
  
  m = Markov()
  m.generateMatrix(filename)
  for i in xrange(int(sys.argv[2])):
    print m.generateParagraph('how')
    print m.generateParagraph('why')

if __name__ == '__main__':
  main()
