#!/usr/bin/python -tt

import sys
import json
import re
import collections

class Markov(object):
  """docstring for ClassName"""

  def read(self, filename):
    f = open(filename)

    entirefile = json.load(f)

    headlines = [entry['title'] for entry in entirefile["items"]]

    headlines = map(unicode.lower, headlines) # TODO: keep proper nouns
    headlines = map(unicode.strip, headlines)
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

      #print '%r %r' % (prev_word, current_word)

  def generateText(self):
    pass

  def __str__(self):
    return str(self.matrix)

def main():

  if len(sys.argv) != 2:
    print 'usage: ./markov.py file'
    sys.exit(1)

  filename = sys.argv[1]

  if not filename.endswith(".json"):
    print 'error: need json file'
    sys.exit(1)

  
  m = Markov()
  m.generateMatrix(filename)

if __name__ == '__main__':
  main()
