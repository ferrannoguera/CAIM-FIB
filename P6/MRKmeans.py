"""
.. module:: MRKmeans

MRKmeans
*************

:Description: MRKmeans

    Iterates the MRKmeansStep script

:Authors: bejar
    

:Version: 

:Created on: 17/07/2017 10:16 

"""
from __future__ import print_function, division

import argparse
import os
import shutil
import time

from MRKmeansStep import MRKmeansStep

__author__ = 'bejar'

if __name__ == '__main__':
    t1 = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--prot', default='prototypes.txt', help='Initial prototpes file')
    parser.add_argument('--docs', default='documents.txt', help='Documents data')
    parser.add_argument('--iter', default=50, type=int, help='Number of iterations')
    parser.add_argument('--nmaps', default=1, type=int, help='Number of parallel map processes to use')
    parser.add_argument('--nreduces', default=1, type=int, help='Number of parallel reduce processes to use')

    args = parser.parse_args()
    assign = {}

    # Copies the initial prototypes
    cwd = os.getcwd()
    shutil.copy(cwd + '/' + args.prot, cwd + '/prototypes0.txt')
    
    old_proto = {}
    old_assign = {}
    first_iter = True
    itertimes = []
    nomove = False  # Stores if there has been changes in the current iteration
    for i in range(args.iter):
        tinit = time.time()  # For timing the iterations

        # Configures the script
        print('Iteration %d ...' % (i + 1))
        # The --file flag tells to MRjob to copy the file to HADOOP
        # The --prot flag tells to MRKmeansStep where to load the prototypes from
        fil = cwd + '/prototypes%d.txt' % i
        prot = cwd + '/prototypes%d.txt' % i
        mr_job1 = MRKmeansStep(args=['-r', 'local', args.docs,
                                     '--file', fil,
                                     '--prot', prot,
                                     '--jobconf', 'mapreduce.job.maps=%d' % args.nmaps,
                                     '--jobconf', 'mapreduce.job.reduces=%d' % args.nreduces])

        # Runs the script
        with mr_job1.make_runner() as runner1:
            runner1.run()
            new_assign = {}
            new_proto = {}
            nomove = True
            # Process the results of the script, each line one results
            for line in runner1.stream_output():
                key, value = mr_job1.parse_output_line(line)
                new_proto[key] = value[1]
                new_assign[key] = value[0]
                if old_assign:
                    old_docs = old_assign[key]
                    if old_docs != value[0]:
                        #print(value[0])
                        nomove = False
                
            # if '' in new_proto:
            #    import pdb; pdb.set_trace()
            # If your scripts returns the new assignments you could write them in a file here
            fileend = '_converged' if nomove and not first_iter else str(i + 1)
            with open('prototypes%s.txt' % fileend, 'w+') as protos:
                for k, v in new_proto.iteritems():
                    protos.write(k + ':' + v+'\n')
                    
            with open('assigment%s.txt' % fileend, 'w+') as ass:
                for k, d in new_assign.iteritems():
                    ass.write(k + ':' + d+'\n')
            # You should store the new prototypes here for the next iteration
            #if first_iter:
                #first_iter = False
                #nomove = False
            
            #if not nomove:
                #old_proto = new_proto

            # If you have saved the assignments, you can check if they have changed from the previous iteration
            if first_iter:
                first_iter = False
                nomove = False
            
            if not nomove:
                old_assign = new_assign

        print("Time= %f seconds" % (time.time() - tinit))
        itertimes.append(time.time()-tinit)
        if nomove:  # If there is no changes in two consecutive iteration we can stop
            print("Algorithm converged")
            break
    print('Total time: {}'.format(time.time()-t1))
    print('Mean iteration time: {}'.format(sum(itertimes)/len(itertimes)))
    # Now the last prototype file should have the results
