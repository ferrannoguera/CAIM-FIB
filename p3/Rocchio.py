import numpy

alfa=1
beta=0.5
#hay que calcular el tfidf para todos los k documentos relevantes
tfidfs = []
#veces que se ejecuta rocchio
nrounds = 1
#valor arbitrario de k
k = 10

def rocchio(q):
    return alfa*q +beta * numpy.mean(tfidfs)

from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

import argparse

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q

__author__ = 'bejar'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, help='Index to search')
    parser.add_argument('--nhits', default=10, type=int, help='Number of hits to return')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')

    args = parser.parse_args()

    index = args.index
    query = args.query
    print(query)
    nhits = args.nhits

    try:
        client = Elasticsearch()
        s = Search(using=client, index=index)

        if query is not None:
            q = Q('query_string',query=query[0])
            for i in range(1, len(query)):
                q &= Q('query_string',query=query[i])

            s = s.query(q)
            response = s[0:nhits].execute()
            for r in response:  # only returns a specific number of results
                #print('ID= %s SCORE=%s' % (r.meta.id,  r.meta.score))
                print('%s' % (r.meta.score))# la ID nos importa poco diría, solo printo el score
                print('PATH= %s' % r.path)
                #print('TEXT: %s' % r.text[:50]) #el text es una excerpt
                print('-----------------------------------------------------------------')

        else:
            print('No query parameters passed')

        print ('%d Documents'% response.hits.total)

    except NotFoundError:
        print('Index %s does not exists' % index)

"""

if __name__ == '__main__':
    #obtain query more relevant 
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, help='Index to search')
    i=0
    while i< nrounds:
        #obtain k more relevant documents
        
        #newquery = rocchio(oldquery)
        ++i
    #print k most relevant documents"""
        
