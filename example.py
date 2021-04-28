from engine.engineQL import *

query1 = """
SELECT Chiller(B)
FROM Building B
WHERE B.BuildingID = 'CP1' AND B.Source = 'LOCAL'
FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191231'
LABEL 'cop'
"""

query2 = """
SELECT VAV(B) * (Temperature(B) + Setpoint(B))
FROM Building B
WHERE B.BuildingID = 'ecp' AND B.Source = 'LOCAL'
FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191231'
LABEL 'epc'
"""

query3 = """
SELECT (Chiller(B) + VAV(B)) + AHU(B)
FROM Building B
WHERE B.BuildingID = 'hf2' AND B.Source = 'LOCAL'
FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191231'
LABEL 'cop'
"""

query4 = """
SELECT Temperature(B) + Luminance(B)
FROM Building B
WHERE B.BuildingID = 'hf2' AND B.Source = 'LOCAL'
FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191231'
LABEL 'cop'
"""

query5 = """
SELECT FLOW_rate(B) * VAV(B)
FROM Building B
WHERE B.BuildingID = 'hf2' AND B.Source = 'LOCAL'
FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191231'
LABEL 'cop'
"""

query6 = """
SELECT Chiller(B) % Room(B)
FROM Building B
WHERE B.BuildingID = 'hf2' AND B.Source = 'LOCAL'
FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191231'
LABEL 'cop'
"""

query7 = """
SELECT ((Chiller(B) % Room(B))*Temperature(B))+VAV(B)
FROM Building B
WHERE B.BuildingID = 'hf2' AND B.Source = 'LOCAL'
FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191231'
LABEL 'cop'
"""

################################   application   ################################

fdd_for_ahu_query = """
    SELECT AHU(B) * ((Temperature(B) + Setpoint(B)) + (Pressure(B) + Signal(B)))
    FROM Building B
    WHERE B.BuildingID = 'ontology_fdd' AND B.Source = 'LOCAL'
    FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191230'
    LABEL 'dumper stuck'
    """

# (Chiller(B) * ((Temperature(B) + Flow_Rate(B)) + Power(B))) + (Temperature(B) * Weather(B))
cop_query = """
    SELECT (Chiller(B) * ((Temperature(B) + Flow_Rate(B)) + Power(B))) + (Temperature(B) * Weather(B))
    FROM Building B
    WHERE B.BuildingID = 'ontology_cop' AND B.Source = 'LOCAL'
    FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191230'
    LABEL 'dumper stuck'
    """

# Weather(B) * Temperature(B) + Zone(B) * Temperature(B) +
# (Weather(B) * Temperature(B)) + (ZONE(B) * Temperature(B)) + ((AHU(B) % VAV(B)) * (Temperature(B) + Flow_Rate(B)))

ecp_query = """
    SELECT (Weather(B) * Temperature(B))  + ((AHU(B) % VAV(B)) * (Temperature(B) + Flow_Rate(B)))
    FROM Building B
    WHERE B.BuildingID = 'ontology_ecp' AND B.Source = 'LOCAL'
    FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191230'
    LABEL 'dumper stuck'
    """

# # data, labels = engine(fdd_for_ahu_query)  # 0.000088s  0.000075s  0.000074s
# data, labels = engine(ecp_query)  # 0.000095s  0.000093s  0.000099s
# data, labels = engine(cop_query)  # 0.000083s  0.000079s  0.000087s
#
# print(data, labels)


###################################



fdd_for_ahu_query = """
    SELECT AHU(B) * ((Temperature(B) + Setpoint(B)) + (Pressure(B) + Signal(B)))
    FROM Building B
    WHERE B.BuildingID = 'ontology_ecp' AND B.Source = 'LOCAL'
    FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191230'
    LABEL 'dumper stuck'
    """

# (Chiller(B) * ((Temperature(B) + Flow_Rate(B)) + Power(B))) + (Temperature(B) * Weather(B))
cop_query = """
    SELECT (Chiller(B) * ((Temperature(B) + Flow_Rate(B)) + Power(B))) + (Temperature(B) * Weather(B))
    FROM Building B
    WHERE B.BuildingID = 'ontology_ecp' AND B.Source = 'LOCAL'
    FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191230'
    LABEL 'dumper stuck'
    """

# Weather(B) * Temperature(B) + Zone(B) * Temperature(B) +
# (Weather(B) * Temperature(B)) + (ZONE(B) * Temperature(B)) + ((AHU(B) % VAV(B)) * (Temperature(B) + Flow_Rate(B)))

ecp_query = """
    SELECT ((Zone(B) * Temperature(B) )  + (Weather(B) * Temperature(B))) + ((AHU(B) % VAV(B)) * (Temperature(B) + Flow_Rate(B)))
    FROM Building B
    WHERE B.BuildingID = 'ontology_ecp' AND B.Source = 'LOCAL'
    FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191230'
    LABEL 'dumper stuck'
    """

# ((Light(B) % ROOM(B)) * Setpoint(B))
bic_query = """
    SELECT ((Light(B) % ROOM(B)) * Setpoint(B)) + (Weather(B) * (Solar_Radiance_Rate(B) + Solar_Angle(B)))
    FROM Building B
    WHERE B.BuildingID = 'ontology_bic' AND B.Source = 'LOCAL'
    FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191230'
    LABEL 'dumper stuck'
    """


energon(cop_query)  # 0.000083s  0.000079s  0.000087s
energon(ecp_query)  # 0.000095s  0.000093s  0.000099s
energon(fdd_for_ahu_query)  # 0.000088s  0.000075s  0.000074s
energon(bic_query)

"""
只和 query这句话的长短有关，和operator使用类型五官

"""

