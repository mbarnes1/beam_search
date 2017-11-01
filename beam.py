from copy import deepcopy
import heapq
from itertools import izip
import logging


class BeamSearch(object):
    def __init__(self, n_beams, scorer, actions):
        """

        :param n_beams: Number of beams
        :param scorer: Object with compute_score(sequences) method
        :param actions: Iterable of possible actions, e.g. items to add to sequence
        """
        self._n_beams = n_beams
        self._scorer = scorer
        self._actions = actions

    def search(self, max_length, beams=None, EOS='.'):
        """
        :param max_length: Maximum sequence length to search over
        :param beams: Initialize beams. If none, initializes to empty beam.
        :param EOS: End-of-sentence token
        :return beams: Beam search result sequences.
        :return best_scores: Scores corresponding to beams
        """
        # Input validation
        if beams is None:
            beams = [['']] * self._n_beams
            initial_beam_length = 0
        else:
            assert (type(beams) is list)
            assert (len(beams) == self._n_beams)
            assert (all(type(beam) == list for beam in beams))
            assert (all(len(beam) == 1 for beam in beams))
            assert (all(isinstance(beam[0], basestring) for beam in beams))
            assert len(set([len(beam[0].split(' ')) for beam in beams])) == 1  # all beams are same length
            initial_beam_length = len(beams[0][0].split(' '))

        # Beam search
        new_beams = deepcopy(beams)
        for i in range(initial_beam_length, max_length):
            for beam in beams:
                if beam[0][-1] != EOS:
                    new_beams.extend(([' '.join([beam[0], word])] for word in self._actions))
                else:
                    new_beams.append(beam)
            if len(new_beams) == self._n_beams:  # all beam searches finished. this is a speed-up
                break
            new_beams = dict(izip(xrange(len(new_beams)), new_beams))
            scores = self._scorer(new_beams)

            # Sort to get best beams
            optimize_bleu = 3  # consider 4-gram bleu scores
            best_scores = heapq.nlargest(self._n_beams, enumerate(scores[optimize_bleu]), key=lambda x: x[1])
            beams = [new_beams[best[0]] for best in best_scores]
            new_beams = []
            print 'Beam length {} \n \t'.format(i+1), '\n \t'.join(['{}: {}'.format(score[1], beam[0]) for score, beam in izip(best_scores, beams)])
        return beams, best_scores
