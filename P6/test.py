import os
import time
from collections import namedtuple

import requests

TestCase = namedtuple('TestCase', ['min_freq', 'max_freq', 'nwords'])

test_cases = [
    TestCase(min_freq=0.05, max_freq=0.2, nwords=200),
    TestCase(min_freq=0.1, max_freq=0.3, nwords=200),
    TestCase(min_freq=0.02, max_freq=0.15, nwords=200),
]

times = []


def main():
    try:
        requests.get('http://localhost:9200/?pretty')
    except Exception as e:
        raise Exception('ElasticSearch is not running')
    for case in test_cases:
        extract = 'python ExtractData.py --index news --minfreq {min_freq} --maxfreq {max_freq} --numwords {nwords}'.format(**case._asdict())
        print extract

        os.system(extract)
        for i in range(20, 9, -1):
            os.system('python GeneratePrototypes.py --nclust {}'.format(i))
            t1 = time.time()
            os.system('python MRKmeans.py --iter 200')
            t2 = time.time()
            times.append(t2 - t1)
            path = './results/{}%_{}%_{}words/{}_classes'.format(case.min_freq * 100, case.max_freq * 100, case.nwords,
                                                                 i)
            os.system('python ProcessResults.py --path {}'.format(path))
            os.system('rm prototypes*.txt assignment*.txt')


if __name__ == '__main__':
    main()
    print(times)
