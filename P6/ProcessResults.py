"""
.. module:: ProcessPrototype

ProcessPrototype
******

:Description: ProcessPrototype

    Prints the results of a clustering for a specific iteration

    It assumes that the results are written in two files assignmentsN.txt and prototypesN.txt.

    assignments.txt has lines with three elements "CLASSN documentid"
    prototypes.txt has the standard format

:Authors:
    bejar

:Version: 

:Date:  14/07/2017
"""

from __future__ import print_function, division

import argparse
import errno
import os
from itertools import islice

__author__ = 'bejar'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prot', default='prototypes_converged.txt', help='prototype file')
    parser.add_argument('--assign', default='assigment_converged.txt', help='assigment file')
    parser.add_argument('--natt', default=10, type=int, help='Number of attributes to show')
    parser.add_argument('--path', default='', help='Path where files will be stored')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        try:
            os.makedirs(args.path)
        except OSError as exc:  # Per si les mosques
            if exc.errno != errno.EEXIST:
                raise

    f = open(args.prot, 'r')
    f2 = open(args.assign, 'r')
    prots = {}
    print("BY PROTOTYPES")
    for line in f:
        cl, attr = line.split(':')
        print(cl)
        latt = sorted([(float(at.split('+')[1]), at.split('+')[0]) for at in attr.split()], reverse=True)
        print(latt[:args.natt])
        prots[cl] = latt
    filepath = os.path.join(args.path, 'prototype_freqs.txt')
    with open(filepath, 'w') as f:
        for k, v in sorted(prots.iteritems()):
            f.write(k + '\n')
            f.write('-' * 50 + '\n')
            for k2, v2 in v:
                f.write(v2 + ': ' + str(k2) + '\n')

    print("")
    print("BY ASSIGNMENTS")
    assignments = {}
    for line in f2:
        cl, attr = line.split(':')
        print(cl)
        latt = [(str(at.split('/')[0])) for at in attr.split()]
        subjects = {}
        for subj in latt:
            if not subj in subjects:
                subjects[subj] = 1
            else:
                subjects[subj] += 1
        sorted_subj = sorted(subjects.iteritems(), key=lambda x: x[1], reverse=True)
        assignments[cl] = sorted_subj
        print(list(islice(sorted_subj, args.natt)))
    filepath = os.path.join(args.path, 'assignment_freqs.txt')
    with open(filepath, 'w') as f:
        for k, v in sorted(assignments.iteritems(), key=lambda x: int(x[0][5:])):
            f.write(k + '\n')
            f.write('-' * 50 + '\n')
            for k2, v2 in v:
                f.write(k2 + ': ' + str(v2) + '\n')
            f.write('-' * 50 + '\n')
