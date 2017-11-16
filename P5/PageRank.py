#!/usr/bin/python

from collections import namedtuple
import time
import sys

class Edge:
    def __init__ (self, origin=None):
        self.origin = origin # write appropriate value
        self.weight = 0 # write appropriate value TESTING

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)
        
    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0   # write appropriate value

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)

edgeList = [] # list of Edge
edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport

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
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            airportList.append(a)
            airportHash[a.code] = count
            cont += 1
    airportsTxt.close()
    print "There were {0} Airports with IATA code".format(cont)


def readRoutes(fd):
    print "Reading Routes file from {0}".format(fd)
    routesTxt = open(fd, "r");
    count = 0
    for line in routesTxt.readlines():
        e = Edge()
        count = 0
        try:
            temp = line.split(',')
            if len(temp[2]) != 3 or len(temp[4]) != 3 :
                raise Exception('not a IATA code')
            e.origin=temp[2]
            e.weight = 1
            end=temp[4]
        except Exception as inst:
            print(len(temp[2]))
            print(len(temp[4]))
            pass
        else:
            if(edgeHash.has_key(end)):

            else:
                e.weight = 1
            edgeHash[end] = e
            edgeList.append(e)
        routesTxt.close()

def computePageRanks():
    pass
    # write your code

def outputPageRanks():
    pass
    # write your code

def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    print(edgeHash)
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print "#Iterations:", iterations
    print "Time of computePageRanks():", time2-time1


if __name__ == "__main__":
    sys.exit(main())
