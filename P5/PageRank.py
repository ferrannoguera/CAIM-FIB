#!/usr/bin/python
from __future__ import division
from collections import namedtuple
import time
import sys

#class Edge:
#    def __init__ (self, origin=None):
#        self.origin = origin # write appropriate value
#        self.weight = 0 # write appropriate value TESTING

#    def __repr__(self):
#        return "edge: {0} {1}".format(self.origin, self.weight)
        
    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, name=None):
        self.pageRank = 0.0
        self.name = name
        self.aristdict = dict()
        self.outweight = 0   # num de aristas que salen del aeropuerto

    def __repr__(self):
    	return self.name
        #return "{t{2}\t{1}}".format(self.name, self.outweight)

#edgeList = [] # list of Edge
#edgeHash = dict() # hash of edge to ease the match
#airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport
numAirports = 0

def readAirports(fd):
    print "Reading Airport file from {0}".format(fd)
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            #airportList.append(a)
            airportHash[code] = a
            cont += 1
    airportsTxt.close()
    numAirports = cont
    for key, value in airportHash.iteritems():
    	value.pageRank = (1/numAirports)
    print "There were {0} Airports with IATA code".format(cont)


def readRoutes(fd):
    print "Reading Routes file from {0}".format(fd)
    routesTxt = open(fd, "r");
    for line in routesTxt.readlines():
        try:
            temp = line.split(',')
            if len(temp[2]) != 3:
                raise Exception('not a IATA code')
            if len(temp[4]) != 3:
            	raise Exception('not a IATA code')
            origin=temp[2]
            end=temp[4]
        except Exception as inst:
            print("ESTO ES UN DESMADRE QUEREMOS PADRE Y MADRE")
            pass
        else:
        	not_exists = False;
        	if (not airportHash.has_key(origin)):
        		not_exists = True
    		if (not not_exists):
	            if(airportHash[origin].aristdict.has_key(end)):
	            	airportHash[origin].aristdict[end] += 1
	            else:
	                airportHash[origin].aristdict[end] = 0
	            airportHash[origin].outweight += 1
        routesTxt.close()

def computePageRanks():
    itera = 100
    count = 0
    damping = 0.8
    const1 = (1-damping)/numAirports
    #while(count <= itera):



def outputPageRanks():
    pass
    # write your code

def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    #print(airportHash)
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print "#Iterations:", iterations
    print "Time of computePageRanks():", time2-time1


if __name__ == "__main__":
    sys.exit(main())
