from rdflib import Graph, URIRef, Literal
import pandas as pd
import os

from hvacbrick.namespace import *

class HVACGraph(object):
    """
    Used for defining building graphs
    brich schema is generated and placed in ./Brick.ttl
    HVAC data should be in csv format and placed in data/*
    """
    def __init__(self, initGraph):

        BRICKPATH = os.path.dirname(__file__) + "/../Brick/Brick.ttl"

        self.m = {}

        if isinstance(initGraph, Graph):
            self.bldg = initGraph
        elif isinstance(initGraph, str):
            self.bldg = Graph()
            self.bldg.parse(initGraph, format='turtle')
        else:
            raise Exception("Unknown graph type!")

        self.bldg.parse(BRICKPATH, format = 'turtle')
        
        for ns in NAMESPACE_:
            nspace = NAMESPACE_[ns]
            self.bldg.bind(ns, nspace)
            strnspace = str(nspace)
            if '#' in strnspace:
                self.m[strnspace.split('#')[0]] = ns
            else:
                self.m[strnspace] = ns

    def query(self, query, fullURI = False, pprint = False):
        
        preparedQuery = """"""
        
        for ns in NAMESPACE_:
            nspace = str(NAMESPACE_[ns])
            preparedQuery += "PREFIX " + ns + ": <" + nspace + "> "
        
        preparedQuery += query
        
        rows = self.bldg.query(preparedQuery)

        if not fullURI:
            rows = [ [self.m[r.split('#')[0]] + ':' + r.split('#')[1] \
                if isinstance(r, URIRef) and '#' in r else r for r in row] for row in rows ]
        else:
            rows = list(rows)

        if pprint:
            for row in rows:
                print(row)
            print("****** QUERY EOF ******")

        return rows

    def getBuildingStream(self, building):
        preparedQuery = """select ?buildingID where {
            ?building rdf:type brick:Building .
            ?building brick:hasID ?buildingID .
            }
            """
        filePath = 'data/'
        buildingIDs = self.query(preparedQuery)
        if [Literal(building)] in buildingIDs:
            df = pd.read_csv(filePath + building + '.csv', parse_dates = [2] )
            return df
        else:
            raise Exception("Building {0} not exist!".format(building))