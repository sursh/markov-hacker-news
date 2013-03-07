markov-hacker-news
==================

TODO: 

- [x] Fix regex to not split on apostrophes & fix title casing
- Set it to pick a common starting word for the first seed
- [x] Recapitalize sentences before output
- [x] Use pickle to only generate the matrix once
- [x] Turn into Twitter bot with heroku
- [x] fix length of tweets
- [x] add seed function
- [ ] cut off long tail of sentence seeds

- [ ] Implement real HN headlines (maybe)
- [ ] Implement check to make sure generated lines aren't coincidentally real ones (maybe)
- [ ] Toward the end of a sentence, transition into bigrams instead of trigrams (maybe)
- [ ] Add links (maybe)

Curious: what is the effect of removing the probability weighting when choosing the next word?
