Hacker News Markov chain generator
==================

Generates new-to-world Hacker News headlines, trained on several years of previous headlines. It uses a [Markov chain generator]() and trigrams to produce mostly human-sounding headlines. Old bigrams version also included for comparison. 

Follow the Twitter bot [here]! 

By [Sasha Laundy](http://github.com/sursh) and [David Lundgren](http://github.com/maxlikely) at [Hacker School](http://hackerschool.com). 

TODO: 

- [x] Fix regex to not split on apostrophes & fix title casing
- Set it to pick a common starting word for the first seed
- [x] Recapitalize sentences before output
- [x] Use pickle to only generate the matrix once
- [x] Turn into Twitter bot with heroku
- [x] fix length of tweets
- [x] add seed function
- [ ] cut off long tail of sentence seeds

TODO SOMEDAY: 

- [ ] Implement real HN headlines so Twitter bot is a "is this real or not?" stream
- [ ] Implement check to make sure generated lines aren't coincidentally real ones
- [ ] Toward the end of a sentence, transition into bigrams instead of trigrams