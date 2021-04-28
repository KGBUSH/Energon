from pyparsing import Keyword, MatchFirst
from config import system_name_list

SELECT = Keyword("SELECT", caseless = True)
FROM = Keyword("FROM", caseless = True)
WHERE = Keyword("WHERE", caseless = True)
FILTER = Keyword("FILTER", caseless = True)
LABEL = Keyword("LABEL", caseless = True)
AND = Keyword("AND", caseless = True)
OR = Keyword("OR", caseless = True)

SUBSYSTEM_LOOKUP = system_name_list
