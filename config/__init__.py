# -*- coding: utf-8 -*-

"""

@file: __init__.py.py
@time: 2021/1/13 9:33 下午
@desc:

"""

import os
from hvacbrick.namespace import *

# project path
PROJECT_PATH = os.path.abspath(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))

# systems
system_name_list = ["AHU", "CHILLER", "VAV", "ZONE", "WEATHER", "SOLAR_PANEL", "ROOM", "LIGHT", "BLIND"]

# functionality
function_name_dict = {"TEMPERATURE": 'Temperature_Sensor',
                      "HUMIDITY": "Humidity_Sensor",
                      "PRESSURE": "Pressure_Sensor",
                      "FLOW_RATE": "Flow_Sensor",
                      "SIGNAL": "Signal_Sensor",
                      "SETPOINT": "Setpoint_Sensor",
                      'LUMINANCE': "Luminance_Sensor",
                      'POWER': "Power_Sensor"
                      }


# definition of predicates (edges)
intra_type_list = [
    'hasPoint',
    # BF['hasPart'],
    'isPointOf',
    # BF['isPartOf']

]

inter_type_list = [
    'feeds',
    'hasLocation'
]

reverse_pairs_list = [
    {'hasPoint', 'isPointOf'},
    # {BF['hasPart'], BF['isPartOf']}
]

# Building Indexing global
BUILDING_INDEX = {}

# system or functionality flag
SUB_FLAG = {'system': 0, 'functionality': 1}
