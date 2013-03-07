 #!/usr/bin/python -tt

import sys
from collections import defaultdict
import numpy
import string
import twitterclient

class Markov(object):

  def read(self, filename):
    ''' Reads in training corpus text file. Cleans, splits, and adds beginning and end signifiers. '''

    with open(filename) as f:
      for line in f:
        yield ['^', '^'] + line.strip().lower().split() + ['$']


  def generateTrigrams(self, tokens):
    ''' Break headline into trigrams '''

    trigrams = []

    for idx, item in enumerate(tokens[:-2]):
      trigrams.append((item, tokens[idx+1], tokens[idx+2]))
    
    return trigrams


  def generateMatrix(self, filename):
    ''' Run through the list of trigrams and add them to the occurence matrix '''

    self.matrix = {}
    self.bigrams = defaultdict(list)

    headlines = self.read(filename)

    for headline in headlines:

      trigrams = self.generateTrigrams(headline)

      for trigram in trigrams:
        bigram = trigram[:2]
        current_word = trigram[-1]

        (old_count, seenBefore) = self.matrix.get(trigram, (0, False))

        if not seenBefore:
          self.bigrams[bigram].append(current_word)

        self.matrix[trigram] = (1 + old_count, True)


  def generateNextWord(self, prev_word, current_word):

    bigram = (prev_word, current_word)

    words = []
    counts = []

    for word in self.bigrams[bigram]:
      trigram = bigram + (word,)
      (count, _) = self.matrix[trigram]
      words.append(word)
      counts.append(count)

    if not counts: 
      return '$'      
    # pick one of the possibilities, with probability weighted by frequency in training corpus
    cumcounts = numpy.cumsum(counts)
    coin = numpy.random.randint(cumcounts[-1])
    for index, item in enumerate(cumcounts):
      if item >= coin:
        return words[index]


  def generateParagraph(self, initial_word=None):
    
    if not initial_word:
        initial_word = self.generateNextWord('^', '^')
        
    prev_word = '^'
    current_word = initial_word
    paragraph = [ initial_word ]

    while (current_word != '$' and len(paragraph) < 20): 
      paragraph.append(current_word)
      prev_word, current_word = current_word, self.generateNextWord( prev_word, current_word )

    paragraph = ' '.join(paragraph[1:])  # strip off leading caret
    return string.capwords(paragraph)


def main():

  DEBUG = True

  if len(sys.argv) != 2:
    print 'Usage: $ %s <inputFile>' % sys.argv[0]
    sys.exit(1)

  # construct matrix based on input text
  filename = sys.argv[1]
  m = Markov()
  m.generateMatrix(filename)

  # construct new chains that will fit in a tweet
  while True:
    tweet = m.generateParagraph() 
    if len(tweet) < 120:
      break

  # send to twitter
  if DEBUG: print("Tweeting: '%s'" % tweet) 
  twitterclient.postTweet(tweet)

if __name__ == '__main__':
  main()
