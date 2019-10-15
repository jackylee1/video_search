from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn


class SimilarityMatch():
    def __init__(self):
        pass

    def penn_to_wn(self, tag):
        """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
        if tag.startswith('N'):
            return 'n'

        if tag.startswith('V'):
            return 'v'

        if tag.startswith('J'):
            return 'a'

        if tag.startswith('R'):
            return 'r'

        return None

    def tagged_to_synset(self, word, tag):
        wn_tag = self.penn_to_wn(tag)
        if wn_tag is None:
            return None
        try:
            return wn.synsets(word, wn_tag)[0]
        except:
            return None

    def sentence_similarity(self, sentence1, sentence2):
        """ compute the sentence similarity using Wordnet """
        # Tokenize and tag
        sentence1 = pos_tag(word_tokenize(sentence1))
        sentence2 = pos_tag(word_tokenize(sentence2))

        # Get the synsets for the tagged words
        synsets1 = [
            self.tagged_to_synset(*tagged_word) for tagged_word in sentence1
        ]
        synsets2 = [
            self.tagged_to_synset(*tagged_word) for tagged_word in sentence2
        ]

        # Filter out the Nones
        synsets1 = [ss for ss in synsets1 if ss]
        synsets2 = [ss for ss in synsets2 if ss]

        score, count = 0.0, 0
        if len(synsets1) > 0 and len(synsets2) > 0:
            # For each word in the first sentence
            for synset in synsets1:
                # Get the similarity value of the most similar word in the other sentence
                sim_scores = [synset.path_similarity(ss) for ss in synsets2]
                # print(sim_scores)
                best_score = max([s if s else 0 for s in sim_scores])
                # Check that the similarity could have been computed
                if best_score != 0:
                    score += best_score
                    count += 1
            # Average the values
        if count > 0:
            score /= count
        return score

    def symmetric_sentence_similarity(self, sentence1, sentence2):
        """ compute the symmetric sentence similarity using Wordnet """
        return (self.sentence_similarity(sentence1, sentence2) +
                self.sentence_similarity(sentence2, sentence1)) / 2
