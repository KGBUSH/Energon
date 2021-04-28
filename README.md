# DAS

## Installation

Python version 3.7.4

Library dependencies are sepecified in requirements.txt

## Introduction

**What is a building ontology**:
    
    Building ontology uses a metadata schema to define the entities and their relatioships in the building.
    It is represented as RDF triples, and can be queries with SparQL queries.

**Readings**:
    
    Read more about what is SparQL, and how to write SparQL queries.

### The problem:

Input:
1. Ontology definition of the building. `ontology/CP1.ttl`
2. Raw data. `data/CP1.csv`

Output:

Extract the subset of the raw data with the features needed for a specific HVAC application.


Assumption:

*The name of the features of the raw data is associated with the UUID in the sensor defined in the ontology*

### Previous approach

1. Write SparQL query extracting metadata from the ontology definition
2. With the SparQL query result, use UUID associated with the sensor and extract corresponding features from raw data

### DAS approach

Write DASQL query to extract the features needed

The DAS query language, **DAS**, following the concept of object database, can be defined as ***select-from-where*** expressions. The syntax of
 is as follows:


**SELECT** *ontology algebra* \
**FROM** *list of buildings* \
**WHERE** *predicate expressions* \
**FILTER** *predicate expressions* \
**LABEL** *list of labels*


For example,

`SELECT Chiller(B)` \
`FROM Building B` \
`WHERE B.BuildingID = 'PolyU' AND B.Source = 'LOCAL'` \
`FILTER B.TIMESTAMP > '20190801' AND B.TIMESTAMP < '20191231'` \
`LABEL 'COP'`

In this example, ontology from building 'PolyU' is selected and bounded to object B, from which all chiller related nodes in B are traversed. FILTER further specifies the filtering conditions for data selection. In this case, data within time window (2019.08.01, 2019.12.31) are selected. Building a supervised learning model often requires data set with labels, LABEL clause retrieves a list of labels used for further modelling.

ontology algebra are composed by applying set operators union(+), difference(-), intersection(*) on top of building elements. Building elements are automatically extracted subset of the complete building ontology. The following are a short list of building elements:

`Chiller`, `AHU`, `Weather`, `VAV`, `Temperature`, `Setpoint`

A typical example of the ontology algebra is: `Chiller(B) + AHU(B)`. This means I am taking all the node related to chiller union AHU from building `B`. And `Chiller(B) * Temperature(B)` means I am taking all the temperature node from the Chiller group in the Building `B`.

**Your task is to use building elements and algebra operators in DAS QL to extract the data needed for the application.**


## Application 1. COP prediction

Chiller in HVAC systems are used to provide constant temperature, pressure and flow of chilled water to create cooling load that cools the air passing through AHU. The maincomponents of the chiller are: compressor, evaporator, condenserand expanding valve. Profiling a chiller can help estimate the internal state of a chiller to determine the chiller load. Moreover, based on that, the total energy consumption and electricity cost of thechiller plants can be minimized.

Theoretically, the COP, Coefficient of Performance of the chiller is used to profile a chiller which is defined as follows: COP = Q/E = c × m × ∆T/E where Q is the cooling load, E is the electrical work consumed perunit time, c is the heat capacity of water which can be considered as a constant under a normal condition, m is the mass of water perunit time and ∆T is the difference between supply chilled water temperature and return chilled water temperature.

This formula shows that the higher the COP is, the higher the energy utilization efficiency of the chiller is. However, practically COP is affected by various physical factorssuch as the age of chiller, working time, and environment conditions(e.g. outdoor temperature) and has nonlinear pattern with them. A data-driven approach is to build machine learning models over historical data to predict COP values in real time. Therefore, the prediction task can be done by first extract historical data related to chiller plants in the HVAC system and then build models on top of it.

Specifically, to determine the instant COP with the real-time collected data, we firstly use a fast clustering algorithm to seek historical data with similar conditions, and then use the similar data to train a immediate ML-model, based on which, the instant COP can be accurately predicted.

According to above, COP is related to not only the factors in chiller itself such as return and supply chilled water temperature, the power consumption of the chiller and other involved factors, but also the environmental factors such as outdoor air temperature.

## Application 2. Energy Consumption Prediction (ontology/ecp.ttl, data/ecp.csv)

Energy Consumption Prediction (ECP) is a Model Predictive Control (MPC) method to save energy consumption of a HVAC system. In general, EPC minimizes the overall energy consumption by predicting the energy consumption of the system with a group of available operations. What's more, based on EPC and instant electricity price, the system manager can determine the control strategy to minimize electricity charges.

We implement this approach on a building which the controllable operation is temperature and setpoint of VAV.

## Application 3. Fault Detection and Diagnosis for AHU (ontology/mzvav.ttl, data/mzvav.csv)

The purpose of FDD is to find faults in an HVAC system so that corresponding actions can be taken for fault elimination. Accurate FDD can reduce system downtime, improve system efficiency, reduce unnecessary energy consumption, and extend system service time.

Typical FDD methods fall into two categories: model-based and data-driven. In the data-driven approach, FDD is implemented in a way that models historical data containing potential faults. This means the data is labeled with various types of faults, and the modeling is done through supervised learning. 

Air Handling Unit (AHU) is a device in the HVAC system that processes the air to be sent into the building rooms to ensure thermal comfort in temperature, humidity and flow mass. A typical AHU consists of a supply fan with a variable frequency drive (VFD), a return fan with a VFD, cooling and heating coils, cooling and heating control valves, outdoor air (OA) and return air (RA) dampers.

Therefore, to detect faults from AHU, the required data is related to AHU unit, e.g. temperature, setpoint of AHU.
