#!/usr/bin/python -tt

import sys
import json
import re

class Markov(object):
  """docstring for ClassName"""

  def read(self, filename):
    f = open(filename)

    entirefile = json.load(f)

    headlines = [entry['title'] for entry in entirefile["items"]]

    headlines = map(unicode.lower, headlines) # TODO: keep proper nouns
    headlines = map(unicode.strip, headlines)
    headlines = [re.split('\W+', headline) for headline in headlines]
    headlines = [['^'] + headline + ['$'] for headline in headlines]

    return headlines

  def generateBigrams(self, tokens):


  def generateMatrix(self, filename):
    
    headlines = self.read(filename)

    for headline in headlines

    # read in headlines, generate tuples


  def generateText(self):
    pass



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
