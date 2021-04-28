# -*- coding: utf-8 -*-

"""

@file: buildingGraph2.py
@time: 2021/1/16 10:10 下午
@desc:

"""

from rdflib import Graph, Literal

from hvacbrick.namespace import *
from hvacbrick.misc import *

def graphTest():
    g = Graph()
    for key in NAMESPACE_:
        g.bind(key, NAMESPACE_[key])
    '''
    Define a test building and bind ID to it.
    '''
    g.add( (HK['Test1'], RDF['type'], BRICK['Building']) )
    g.add( (HK['Test1'], BRICK['hasID'], Literal('Test1')) )

    '''
    Define the root nodes of subsystems.
    '''
    g.add( (HK['Chiller_1'], RDF['type'], BRICK['Chiller']) )
    g.add( (HK['Chiller_2'], RDF['type'], BRICK['Chiller']) )
    g.add( (HK['Chiller_3'], RDF['type'], BRICK['Chiller']) )

    g.add( (HK['AHU_1'], RDF['type'], BRICK['AHU']) )
    g.add( (HK['AHU_2'], RDF['type'], BRICK['AHU']) )

    g.add( (HK['VAV_1'], RDF['type'], BRICK['VAV']) )
    g.add( (HK['VAV_2'], RDF['type'], BRICK['VAV']) )

    g.add( (HK['Room_1'], RDF['type'], BRICK['Room']) )
    g.add( (HK['Room_2'], RDF['type'], BRICK['Room']) )
    g.add( (HK['Room_3'], RDF['type'], BRICK['Room']) )

    g.add( (HK['Light_1'], RDF['type'], BRICK['Luminaire']) )
    g.add( (HK['Light_2'], RDF['type'], BRICK['Luminaire']) )

    '''
    Define relationship between above root nodes (systems).
    '''
    g.add( (HK['Chiller_1'], BF['feeds'], HK['AHU_1']) )
    g.add( (HK['Chiller_2'], BF['feeds'], HK['AHU_1']) )
    g.add( (HK['Chiller_2'], BF['feeds'], HK['AHU_2']) )
    g.add( (HK['Chiller_3'], BF['feeds'], HK['AHU_2']) )

    g.add( (HK['AHU_1'], BF['feeds'], HK['VAV_1']) )
    g.add( (HK['AHU_2'], BF['feeds'], HK['VAV_2']) )

    g.add( (HK['VAV_1'], BF['feeds'], HK['Room_1']) )
    g.add( (HK['VAV_2'], BF['feeds'], HK['Room_2']) )

    g.add( (HK['Light_1'], BF['hasLocation'], HK['Room_2']) )
    g.add( (HK['Light_2'], BF['hasLocation'], HK['Room_3']) )

    '''
    Define the sub-components and sensors of systems
    '''
    # define chiller_1
    g.add((HK['Damper_1'], RDF['type'], BRICK['Damper']))
    g.add((HK['Chiller_1'], BF['hasPart'], HK['Damper_1']))
    g.add((HK['Chiller_Temp_11'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['Chiller_Temp_12'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['Chiller_1'], BF['hasPoint'], HK['Chiller_Temp_11']))
    g.add((HK['Damper_1'], BF['hasPoint'], HK['Chiller_Temp_12']))

    # define chiller_2
    g.add((HK['Damper_2'], RDF['type'], BRICK['Damper']))
    g.add((HK['Chiller_2'], BF['hasPart'], HK['Damper_2']))
    g.add((HK['Chiller_Temp_21'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['Chiller_Temp_22'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['Chiller_2'], BF['hasPoint'], HK['Chiller_Temp_21']))
    g.add((HK['Damper_2'], BF['hasPoint'], HK['Chiller_Temp_22']))

    # define chiller_3
    g.add((HK['Chiller_Temp_31'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['Chiller_Temp_32'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['Chiller_3'], BF['hasPoint'], HK['Chiller_Temp_31']))
    g.add((HK['Chiller_3'], BF['hasPoint'], HK['Chiller_Temp_32']))

    # define AHU_1
    g.add((HK['AHU_Temp_11'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['AHU_Flow_11'], RDF['type'], BRICK['Flow_Sensor']))
    g.add((HK['AHU_1'], BF['hasPoint'], HK['AHU_Temp_11']))
    g.add((HK['AHU_1'], BF['hasPoint'], HK['AHU_Flow_11']))

    # define AHU_2
    g.add((HK['AHU_Temp_21'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['AHU_Flow_21'], RDF['type'], BRICK['Flow_Sensor']))
    g.add((HK['AHU_2'], BF['hasPoint'], HK['AHU_Temp_21']))
    g.add((HK['AHU_2'], BF['hasPoint'], HK['AHU_Flow_21']))

    # define VAV_1
    g.add((HK['VAV_Temp_11'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['VAV_Flow_11'], RDF['type'], BRICK['Flow_Sensor']))
    g.add((HK['VAV_1'], BF['hasPoint'], HK['VAV_Temp_11']))
    g.add((HK['VAV_1'], BF['hasPoint'], HK['VAV_Flow_11']))

    # define VAV_2
    g.add((HK['VAV_Temp_21'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['VAV_Flow_21'], RDF['type'], BRICK['Flow_Sensor']))
    g.add((HK['VAV_2'], BF['hasPoint'], HK['VAV_Temp_21']))
    g.add((HK['VAV_2'], BF['hasPoint'], HK['VAV_Flow_21']))

    # define Room_1
    g.add((HK['Room_Temp_11'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['Room_Temp_12'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['Room_1'], BF['hasPoint'], HK['Room_Temp_11']))
    g.add((HK['Room_1'], BF['hasPoint'], HK['Room_Temp_12']))

    # define Room_2
    g.add((HK['Room_Temp_21'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['Room_Temp_22'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['Room_2'], BF['hasPoint'], HK['Room_Temp_21']))
    g.add((HK['Room_2'], BF['hasPoint'], HK['Room_Temp_22']))

    # define Room_3
    g.add((HK['Room_Temp_31'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['Room_Temp_32'], RDF['type'], BRICK['Temperature_Sensor']))
    g.add((HK['Room_3'], BF['hasPoint'], HK['Room_Temp_31']))
    g.add((HK['Room_3'], BF['hasPoint'], HK['Room_Temp_32']))

    # define light_1
    g.add((HK['Luminance_11'], RDF['type'], BRICK['Luminance_Sensor']))
    g.add((HK['Luminance_12'], RDF['type'], BRICK['Luminance_Sensor']))
    g.add((HK['Light_1'], BF['hasPoint'], HK['Luminance_11']))
    g.add((HK['Light_1'], BF['hasPoint'], HK['Luminance_12']))

    # define light_2
    g.add((HK['Luminance_21'], RDF['type'], BRICK['Luminance_Sensor']))
    g.add((HK['Luminance_22'], RDF['type'], BRICK['Luminance_Sensor']))
    g.add((HK['Light_2'], BF['hasPoint'], HK['Luminance_21']))
    g.add((HK['Light_2'], BF['hasPoint'], HK['Luminance_22']))

    return g

if __name__ == "__main__":
    BUILDING = 'Test0116'
    # g = buildingGraph(BUILDING, 6)
    g = graphTest()
    g.serialize(destination = BUILDING + '.ttl', format = 'turtle')
    # print_graph(g)

    # Load the graph
    # g = Graph() # Initialize a new graph.
    # g.parse('sample_building_sol.ttl', format='turtle') # Load the stored graph.