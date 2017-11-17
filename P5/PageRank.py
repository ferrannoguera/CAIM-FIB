#!/usr/bin/python
from __future__ import division
from collections import namedtuple
import time
import sys

class Airport:
    def __init__ (self,id=None,code=None, name=None):
        self.id = 0
        self.name = name
        self.code = code
        self.aristdict = dict()
        self.outweight = 0   # num de aristas que salen del aeropuerto

    def __repr__(self):
        return self.name


pageRankList = []
pageRankListAux = []
airportSinkList = [] # list of Airport
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
            a.code=temp[4][1:-1]
            a.id = cont
        except Exception as inst:
            pass
        else:
            if not airportHash.has_key(a.code):
                airportHash[a.code] = a
                cont += 1
    airportsTxt.close()
    global numAirports
    numAirports = cont
    for key, value in airportHash.iteritems():
        pageRankList.append((1/numAirports))
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
            not_exists = False
            if (not airportHash.has_key(origin)):
                not_exists = True
            if (not airportHash.has_key(end)):
                not_exists = True
            if (not not_exists):
                if(airportHash[origin].aristdict.has_key(end)):
                    airportHash[origin].aristdict[end] += 1
                    airportHash[origin].outweight += 1
                else:
                    airportHash[origin].aristdict[end] = 1
                    airportHash[origin].outweight += 1
        routesTxt.close()


def getSinkAirports():
    global airportSinkList
    for key, value in airportHash.iteritems():
        if (value.outweight == 0):
            airportSinkList.append(value.code)



def computePageRanks():
    itera = 200
    count = 0
    damping = 0.85
    const1 = (1-damping)/numAirports
    global pageRankList
    global airportSinkList
    global airportHash
    pageRankListAux = pageRankList
    while(count <= itera):
        const3 = 0
        for i in airportSinkList:
            const3 += (pageRankList[airportHash[i].id]/numAirports)
        for keyi, valuei in airportHash.iteritems():
            const2 = 0
            for keyj, valuej in airportHash[keyi].aristdict.iteritems():
                if airportHash[keyj].outweight != 0:
                    pagerank = pageRankList[airportHash[keyj].id]
                    const2 += (pagerank*valuej)/airportHash[keyj].outweight
            pageRankListAux[valuei.id] = const1+damping*(const2+const3)
        pageRankList = pageRankListAux
        print(sum(pageRankList))
        count += 1
    return count


def outputPageRanks():
    aux2 = []
    aux3 = []
    for j, i in airportHash.iteritems():
        aux2.append(i.name)
        aux3.append(pageRankList[i.id])
    plot = zip(aux3, aux2)
    plot = sorted(plot)
    plot.reverse()
    print(plot)


def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    getSinkAirports()
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print "#Iterations:", iterations-1
    print "Time of computePageRanks():", time2-time1


if __name__ == "__main__":
    sys.exit(main())
