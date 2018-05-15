"""
.. module:: MRKmeansDef

MRKmeansDef
*************

:Description: MRKmeansDef

    

:Authors: bejar
    

:Version: 

:Created on: 17/07/2017 7:42 

"""

from __future__ import division

from collections import defaultdict, OrderedDict

import numpy as np
from mrjob.job import MRJob
from mrjob.step import MRStep

__author__ = 'bejar'


class DefaultOrderedDict(OrderedDict, defaultdict):
    def __init__(self, default_factory=None, *args, **kwargs):
        super(DefaultOrderedDict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory


class MRKmeansStep(MRJob):
    prototypes = {}

    def jaccard(self, prot, doc):
        """
        Compute here the Jaccard similarity between  a prototype and a document
        prot should be a list of pairs (word, probability)
        doc should be a list of words
        Words must be alphabeticaly ordered

        The result should be always a value in the range [0,1]
        :type prot: {str: float}
        """
        dotp = 0
        for w in doc:
            dotp += prot.get(w, 0)
        prot_norm = np.linalg.norm(prot.values()) ** 2

        res = dotp / (prot_norm + len(doc) - dotp)

        return res

    def configure_options(self):
        """
        Additional configuration flag to get the prototypes files

        :return:
        """
        super(MRKmeansStep, self).configure_options()
        self.add_file_option('--prot')

    def load_data(self):
        """
        Loads the current cluster prototypes

        :return:
        """
        f = open(self.options.prot, 'r')
        for line in f:
            cluster, words = line.split(':')
            cp = {}
            for word in words.split():
                w, fr = word.split('+')
                cp[w] = float(fr)
            self.prototypes[cluster] = cp

    def assign_prototype(self, _, line):
        """
        This is the mapper it should compute the closest prototype to a document

        Words should be sorted alphabetically in the prototypes and the documents

        This function has to return at list of pairs (prototype_id, document words)

        You can add also more elements to the value element, for example the document_id
        """

        # Each line is a string docid:wor1 word2 ... wordn
        doc, words = line.split(':')
        lwords = words.split()

        #
        # Compute map here
        #
        prot = ''
        jac = 0
        for pr, wr in self.prototypes.iteritems():
            j = self.jaccard(wr, lwords)
            if j >= jac:
                jac = j
                prot = pr

        # Return pair key, value
        yield prot, (doc, lwords)

    def aggregate_prototype(self, key, values):
        """
        input is cluster and all the documents it has assigned
        Outputs should be at least a pair (cluster, new prototype)

        It should receive a list with all the words of the documents assigned for a cluster

        The value for each word has to be the frequency of the word divided by the number
        of documents assigned to the cluster

        Words are ordered alphabetically but you will have to use an efficient structure to
        compute the frequency of each word

        :param key:
        :param values:
        :return:
        """
        ndocs = 0
        words = []
        docs = []
        occurrences = defaultdict(lambda: 0)
        for val2 in values:
            ndocs += 1
            docs.append(val2[0])
            words += val2[1]
        calc_ndocs = (1 / ndocs)
        for word in words:
            occurrences[word] += calc_ndocs

        val = ' '.join([str(k) + '+' + str(v) for k, v in sorted(occurrences.iteritems())])
        docsi = ' '.join([str(di) for di in docs])
        yield key, (docsi, val)

    def steps(self):
        return [MRStep(mapper_init=self.load_data, mapper=self.assign_prototype,
                       reducer=self.aggregate_prototype)
                ]


if __name__ == '__main__':
    # t1 = time.time()
    MRKmeansStep.run()
    # t2 = time.time()
    # print('TIME: {}'.format(t2 - t1))
