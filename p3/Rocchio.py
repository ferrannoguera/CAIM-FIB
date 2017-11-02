


from __future__ import print_function, division
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.client import CatClient
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q

import argparse

import numpy as np


__author__ = 'ferranyguillem'



alfa=1
beta=0.5
#hay que calcular el tfidf para todos los k documentos relevantes
tfidfs = []
#veces que se ejecuta rocchio
nrounds = 1
#valor arbitrario de k
k = 2
#docs => k docs that matter
docs = []


def document_term_vector(client, index, id):
    """
    Returns the term vector of a document and its statistics a two sorted list of pairs (word, count)
    The first one is the frequency of the term in the document, the second one is the number of documents
    that contain the term

    :param client:
    :param index:
    :param id:
    :return:
    """
    termvector = client.termvectors(index=index, doc_type='document', id=id, fields=['text'],
                                    positions=False, term_statistics=True)

    file_td = {}
    file_df = {}

    if 'text' in termvector['term_vectors']:
        for t in termvector['term_vectors']['text']['terms']:
            file_td[t] = termvector['term_vectors']['text']['terms'][t]['term_freq']
            file_df[t] = termvector['term_vectors']['text']['terms'][t]['doc_freq']
    return sorted(file_td.items()), sorted(file_df.items())


def doc_count(client, index):
    """
    Returns the number of documents in an index

    :param client:
    :param index:
    :return:
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])


#s'haura de modificar una mica
def toTFIDF(client, index, file_id):
    """
    Returns the term weights of a document
    :param file:
    :return:
    """
    file_tv, file_df = document_term_vector(client, index, file_id)
    max_freq = max([f for _, f in file_tv])
    #print('max_freq %s' % max_freq)
    dcount = doc_count(client, index)
    #print('dcount %s' % dcount)
    terms = []
    tfidfw = []
    #print("START")
    for (t, w),(_, df) in zip(file_tv, file_df):
        idfi = float(np.log2(dcount/df))
        #print('df %s' % df)
        #print('idfi %s' % idfi)
        tfdi = float(w/max_freq)
        #print('w %s' % w)
        #print('tfdi %s' % tfdi)
        wdi = tfdi * idfi
        terms.append(t)
        tfidfw.append(wdi)
    return zip(terms,(tfidfw)) #treta la normalitzacio


def normalize(tw):
    """
    Normalizes the weights in t so that they form a unit-length vector
    It is assumed that not all weights are 0
    :param tw:
    :return:
    """
    count = 0
    for ti in tw:
        count += ti*ti
    count = np.sqrt(count)
    for i in range(0,len(tw)):
        tw[i] = tw[i]/count
        
    return tw


def print_term_weigth_vector(twv):
    """
    Prints the term vector and the correspondig weights
    :param twv:
    :return:
    """
    print("Weight of the vector: ")
    print (len(twv))
    for (ttvi,twvi) in twv:
        print(ttvi)
        print(twvi)
    print("End of Weight of the vector")


def rocchio(q):
    return alfa*q +beta * numpy.mean(tfidfs)


def sumar_l(l1,l2):
    l1 = dict(l1)
    l2 = dict(l2)
    newdict = {}
    for key, value in l1.iteritems():
        newdict.append({key,value+l2[key]})
    return newlist = list(newdict)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, help='Index to search')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')

    args = parser.parse_args()

    index = args.index
    query = args.query
    print(query)

    try:
        client = Elasticsearch()
        s = Search(using=client, index=index)

        if query is not None:
            q = Q('query_string',query=query[0])
            for i in range(1, len(query)):
                q &= Q('query_string',query=query[i])

            s = s.query(q)
            response = s[0:(k+1)].execute()
            for r in response:  # only returns a specific number of results
                print('ID= %s SCORE=%s' % (r.meta.id,  r.meta.score))
                print('PATH= %s' % r.path)
                print('-----------------------------------------------------------------')
                docs.append(r.meta.id)

        else:
            print('No query parameters passed')

        print ('%d Documents'% response.hits.total)

    except NotFoundError:
        print('Index %s does not exists' % index)
        
    print('DOCUMENTS USATS:')
    tmp = k
    while tmp != 0:
        print(docs[tmp])
        tmp -= 1
    print('---------------------------------------')
    
    oldd = {}
    while (nrounds != 0):
        for i in range(0,k):
            newd = toTFIDF(client, index, docs[i])
            print('NEWD')
            print_term_weigth_vector(newd)
            oldd = sumar_l(oldd,newd)
            print('OLDD')
            print_term_weigth_vector(oldd)
        #tfidfs = normalize(oldd/k)
        #print_term_weigth_vector(tfidfs)
        nrounds-=1
    
    #file1_tw = toTFIDF(client, index, docs[0])
    #print_term_weigth_vector(file1_tw)
    #print('---------------------------------------')
    #file1_tw = toTFIDF(client, index, docs[1])
    #print_term_weigth_vector(file1_tw)


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
        