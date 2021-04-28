from rdflib import Graph, Literal

from hvacbrick.namespace import *
from hvacbrick.misc import *


def buildingGraph(BUILDING, NO_OF_CHILLERS, OUTPUT=None):
    g = Graph()

    for key in NAMESPACE_:
        g.bind(key, NAMESPACE_[key])

    g.add((HK[BUILDING], RDF['type'], BRICK['Building']))
    g.add((HK[BUILDING], BRICK['hasID'], Literal(BUILDING)))

    for i in range(1, NO_OF_CHILLERS + 1):
        suffix = str(i)
        chiller = 'chiller' + suffix
        returnTemp = 'returnTemp' + suffix
        supplyTemp = 'supplyTemp' + suffix

        g.add((HK[chiller], RDF['type'], BRICK['Chiller']))
        g.add((HK[chiller], BRICK['hasID'], Literal(suffix)))

        g.add((HK[returnTemp], RDF['type'], BRICK['Chilled_Water_Return_Temperature_Sensor']))
        g.add((HK[returnTemp], BRICK['hasID'], Literal('returnTemp')))

        g.add((HK[supplyTemp], RDF['type'], BRICK['Chilled_Water_Supply_Temperature_Sensor']))
        g.add((HK[supplyTemp], BRICK['hasID'], Literal('supplyTemp')))

        g.add((HK[returnTemp], BF['isPointOf'], HK[chiller]))
        g.add((HK[supplyTemp], BF['isPointOf'], HK[chiller]))

        g.add((HK[chiller], BF['hasLocation'], HK[BUILDING]))

    return g


if __name__ == "__main__":
    BUILDING = 'CP1_dy_test0204_25scale'
    g = buildingGraph(BUILDING, 25)
    g.serialize(destination = BUILDING + '.ttl', format = 'turtle')
    # print_graph(g)
    #
    # # Load the graph
    # g = Graph()  # Initialize a new graph.
    # # g.parse('sample_building_sol.ttl', format='turtle')  # Load the stored graph.
    # g.parse('CP1_dy_test.ttl', format='turtle')  # Load the stored graph.
    #
    # # for subj, pred, obj in g:
    # #     print((subj, pred, obj))
    # #
    # # print('============')
    # #
    # # import pprint
    # # for stmt in g:
    # #     pprint.pprint(stmt)
    #
    # # # print(list(g.objects()))
    # # for obj in g.subject_objects(BF['isPointOf']):
    # #     print(obj)
    # #     aa=1
    #
    # for item in g.subjects():
    #     print(item)