
from rdflib import RDFS, RDF, OWL, XSD, Namespace

BRICK_VERSION = '1.1.0'

BRICK = Namespace('https://brickschema.org/schema/' + BRICK_VERSION + '/Brick#')
BF = Namespace('https://brickschema.org/schema/' + BRICK_VERSION + '/BrickFrame#')
BRICKTAG = Namespace('https://brickschema.org/schema/' + BRICK_VERSION + '/BrickTag#')
HK = Namespace('http://hk.building.com#')

SDO = Namespace('http://schema.org#')
XML = Namespace('http://www.w3.org/XML/1998/namespace')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
DCTERMS = Namespace('http://purl.org/dc/terms')

NAMESPACE_ = {
    'brick': BRICK,
    'bf': BF,
    'tag': BRICKTAG,
    'hk': HK,

    'sdo': SDO,
    'xml': XML,
    'skos': SKOS,
    'dcterms': DCTERMS,

    'rdfs': RDFS,
    'rdf': RDF,
    'owl': OWL,
    'xsd': XSD,
}