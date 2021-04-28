from engine.engineQL import *


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


query_chiller = """
SELECT Chiller(B) * Temperature(B)
FROM Building B
WHERE B.BuildingID = 'CP1_dy_test0204_25scale' AND B.Source = 'LOCAL'
FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191231'
LABEL 'cop'
"""



energon(query_chiller)
# engine(cop_query)  # 0.000083s  0.000079s  0.000087s
# engine(ecp_query)  # 0.000095s  0.000093s  0.000099s
# engine(fdd_for_ahu_query)  # 0.000088s  0.000075s  0.000074s
# engine(bic_query)

