from pyparsing import Group, delimitedList, Optional, Word, alphas, alphanums, quotedString, \
    pyparsing_common, Literal, infixNotation, opAssoc, oneOf, empty
from engine.engineKeywords import SELECT, FROM, WHERE, FILTER, LABEL, AND, OR, SUBSYSTEM_LOOKUP

from rdflib import Graph
import os
import pandas as pd

from hvacbrick.building2 import Building2
from hvacbrick.misc import print_graph

from tools.basic import TimeRecorder

__TRACE__ = False

def getBuilding(BuildingID=None, Source=None):
    """
    retrive ontology from database
    and return building objects
    """
    if BuildingID:
        # if isinstance(BuildingID, str):
        #     if BuildingID[0] in '"\'':
        #         BuildingID = BuildingID[1:-1]
        # else:
        #     BuildingID = str(BuildingID)
        g = Graph()
        ttl = "./ontology/" + BuildingID + ".ttl"
        if os.path.isfile(ttl):
            g.parse(ttl, format="turtle")
        # return Building(BuildingID, g, ttl_path=ttl)
        return Building2(BuildingID, ttl_path=ttl)

#
# def evalAlgebra_bak(algebra, buildingDic):
#     if __TRACE__:
#         print("algebra:", algebra)
#     if len(algebra) == 2:
#         sub, building = algebra
#         # SUBSYSTEM_LOOKUP is used to provide hints and constraints
#         if sub.upper() in SUBSYSTEM_LOOKUP:
#             return buildingDic[building].extract_subsys(sub)  # sub: 'VAV'
#         else:
#             return buildingDic[building].extract_functional(sub)
#     left, op, right = algebra
#     if op == '+':
#         return evalAlgebra(left, buildingDic) + evalAlgebra(right, buildingDic)
#     elif op == '-':
#         return evalAlgebra(left, buildingDic) - evalAlgebra(right, buildingDic)
#     elif op == '*':
#         return evalAlgebra(left, buildingDic) * evalAlgebra(right, buildingDic)


def evalAlgebra(algebra, buildingDic):
    """
    # buildingsDic:  {'B': {'BuildingID': 'ecp', 'Source': 'LOCAL'}}
    """
    if __TRACE__:
        print("algebra:", algebra)
    if len(algebra) == 2:
        sub, building = algebra
        # SUBSYSTEM_LOOKUP is used to provide hints and constraints
        if sub.upper() in SUBSYSTEM_LOOKUP:
            return buildingDic[building].extract_sub_system(sub)
        else:
            return buildingDic[building].extract_sub_functionality(sub)
    left, op, right = algebra
    if op == '+':
        return evalAlgebra(left, buildingDic) + evalAlgebra(right, buildingDic)
    elif op == '-':
        return evalAlgebra(left, buildingDic) - evalAlgebra(right, buildingDic)
    elif op == '*':
        return evalAlgebra(left, buildingDic) * evalAlgebra(right, buildingDic)
    elif op == '%':
        return evalAlgebra(left, buildingDic) % evalAlgebra(right, buildingDic)

def trace(b):
    global __TRACE__
    __TRACE__ = b

def getData(subs, labels):
    if __TRACE__:
        print_graph(subs.ontology)
    csvfile = "./data/" + subs.buildingID + ".csv"
    if os.path.isfile(csvfile):
        data = pd.read_csv(csvfile)    
    query = """ select ?uuid where { ?sub ?pred ?uuid . filter ( ?pred = brick:hasUuid ) . } """
    features = set()
    default_features = set(['time', 'coolingLoad', 'flowRate', 'R2', 'age', 'chillerName'])
    # label = set(['cop', 'damper stuck', 'heating coil valve leaking', 'cooling coil valve stuck'])
    for row in subs.ontology.query(query):
        features.add(str(row[0]))
    existing_features = set(data.columns).intersection(features.union(default_features))
    existing_labels = set(data.columns).intersection(set(labels))
    if __TRACE__:
        print(existing_features, existing_labels)

    return data[existing_features], data[existing_labels]

def normalization(pred):
    if any(e == 'AND' or e == 'OR' for e in pred):
        return pred
    else:
        # TO DO normaliztion
        return [pred]

def evalQuery(tokens):
    """
    The execution plan looks like:
    1. Construct algebra function call
    2. Extract data from ontology extration
    3. Post filter the sensor data
    """
    time_recorder = TimeRecorder()
    time_recorder.tick()
    length = len(tokens[0])

    if length == 1:
        # extract everything
        algebra = tokens[0][0]
        print("You are trying to extract everything!")
        pass
    
    algebra = tokens[0][0]
    buildingList = tokens[0][1]
    buildings = tokens[0][2]
    filtering = None
    labels = []
    if length >= 4:
        filtering = tokens[0][3]
    if length >= 5:
        for label in tokens[0][4]:
            if isinstance(label, str):
                if label[0] in '"\'':
                    labels.append(label[1:-1])
            else:
                labels.append(str(label))


    if __TRACE__:
        print("algebra: ", algebra)
        print("buildingList: ", buildingList)
        print("buildings: ", buildings)
        print("filtering: ", filtering)
        print("labels: ", labels)

    buildingsDic = {}

    for _, building in buildingList:
        buildingsDic[building] = {}
    
    buildings = normalization(buildings)

    for building in buildings:
        # TO DO:
        # transform to conjunctive normal form
        # process CNF
        if building in ('AND', 'OR'):
            continue
        else:
            building, _, kw, predicate, arg = building

            if isinstance(arg, str):
                if arg[0] in '"\'':
                    arg = arg[1:-1]

            if building in buildingsDic:
                buildingsDic[building][kw] = arg

    # time_recorder.tock("Test building index started1 !")
    for building in buildingsDic:
        args = buildingsDic[building]  # buildingsDic:  {'B': {'BuildingID': 'ecp', 'Source': 'LOCAL'}}
        buildingsDic[building] = getBuilding(**args)

    if __TRACE__:
        print("building lookups: ", buildingsDic)

    # algebra ([(['VAV', 'B'], {}), '*', ([(['Temperature', 'B'], {}), '+', (['Setpoint', 'B'], {})], {})], {})

    time_recorder.tock("Test ontology loading Finished !")
    for i in range(1):
        subontology = evalAlgebra(algebra, buildingsDic)
    time_recorder.tock("Test subontology Finished !")
    print('\n\n')
    return
    data, label = getData(subontology, labels)

    return data, label

# identifier = Word(alphanums)
identifier = Word(alphas+"_", alphanums+"_")
literal = quotedString ^ pyparsing_common.number
building = Literal('Building') ^ Literal('SubBuilding')
sub_extraction = Group(identifier + Literal('(').suppress() + delimitedList(identifier) + Literal(')').suppress()).setName('Subontology Extraction')
algebra = infixNotation(sub_extraction,
                        [ ('-', 1, opAssoc.RIGHT),
                          (oneOf('%'), 2, opAssoc.LEFT),
                          (oneOf('* /'), 2, opAssoc.LEFT),
                          (oneOf('+ -'), 2, opAssoc.LEFT) ]).setName('Algebra')
buildings = Group(delimitedList(
    Group(building + empty() + identifier)
)).setName('Building List')

predicate = Group(identifier + Literal('.') + identifier + oneOf('> < = >= <= !=') + literal)
predicates = infixNotation(predicate,
                            [ (AND, 2, opAssoc.LEFT),
                              (OR, 2, opAssoc.LEFT) ]).setName('Predicates')

quantifications = predicates

labels = Group(delimitedList(literal))

query = Group(
    SELECT.suppress() + algebra +
    Optional(
        FROM.suppress() + buildings + 
        WHERE.suppress() + predicates +
        Optional(
            FILTER.suppress() + quantifications
        )
    ) +
    Optional(LABEL.suppress() + labels)
    ).addParseAction(evalQuery)

def energon(q):
    from pyparsing import ParseException
    retv = None
    try:
        retv = query.parseString(q)[0]
    except ParseException:
        print("Not a valid Energon Query!")
    finally:
        return retv

from cmd import Cmd

class Energon(Cmd):
    prompt = 'ENERGON:>'
    def do_exit(self, inp):
        print("Bye")
        return True

    def default(self, inp):
        print(energon(inp))
        return False

# __ENERGON__ = Energon().cmdloop()

if __name__ == '__main__':
    Energon().cmdloop()