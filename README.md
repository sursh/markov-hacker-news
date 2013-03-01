markov-hacker-news
==================

TODO: 

- [x] Fix regex to not split on apostrophes & fix title casing
- Set it to pick a common starting word for the first seed
- [x] Recapitalize sentences before output
- Turn into Twitter bot
- Toward the end of a sentence, transition into bigrams instead of trigrams
- Use semantic analysis and language patterns


Tweeting through Buffer: 

Host a script on Heroku and set up a cron job to run once a day and stuff four tweets into Buffer. (Want to use Oauth2, and constructing the matrix is very intensive)

- create the twitter account
- register a new application http://bufferapp.com/developers/apps/create


http://bufferapp.com/developers/api/oauth

http://bufferapp.com/developers/api/updates#updatescreate