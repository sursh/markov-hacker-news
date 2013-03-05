def build_matrix(trigrams):
    self.matrix  = {}
    self.bigrams = defaultdict(list)

    for trigram in trigrams:

        bigram = trigram[:2]
        current_word = trigram[-1]

        old_count, watched = self.matrix.get(trigram, (0, False))

        if not watched:
            self.bigrams[bigram].append(current_word)

        self.matrix[trigram] = (1 + old_count, True)

def sample_next(bigram):

  for word in self.bigrams[bigram]]) 
    words, freqs = zip(* [(word, self.matrix[bigram + (word,)]) 

    idx = sample_idx_from(freqs)

    return words[idx]