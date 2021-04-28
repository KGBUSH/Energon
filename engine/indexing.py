# -*- coding: utf-8 -*-

"""

@file: indexing.py
@time: 2021/1/13 7:35 下午
@desc: for Energon Indexing structure for speedup

"""

from rdflib import Graph, Literal
import re

from config import PROJECT_PATH
from config import system_name_list, inter_type_list, intra_type_list, reverse_pairs_list
from config import function_name_dict
from tools.basic import find_inverse_predicate, multi_hop_traversal


class Indexing:
    """ build the indexing structure for the Building """

    def __init__(self, ttl_file_path):
        """ load the graph"""
        self.g = Graph()  # Initialize a new graph.
        self.g.parse(ttl_file_path, format='turtle')  # Load the stored graph.
        self.spo_dict = self.record_all_spo_in_building()
        self.index_system = dict()
        self.index_func = dict()

        # 建索引
        self.build_index()

    def record_all_spo_in_building(self):
        """
        s p o record
        """
        spo_dict = {'s': set(), 'p': set(), 'o': set()}
        for s in self.g.subjects():
            spo_dict['s'].add(s)
        for p in self.g.predicates():
            spo_dict['p'].add(p)
        for o in self.g.objects():
            spo_dict['o'].add(o)
        return spo_dict

    def make_completed_predicate(self, p):
        """p maybe 'hasPoint', need to transform to the 'predicate' in ttl file """
        for value in self.spo_dict['p']:
            if p in value:
                return value
        return None

    def build_system_index(self):
        """
        build the subsystem indexing structure for this building
        """
        # 1. layer: system
        for system_name in system_name_list:
            self.index_system.update({system_name: dict()})

        # 2. layer: segment list
        for key, value in self.index_system.items():
            system_name = key.lower()  # e.g. 'chiller'
            d = value  # here is empty dict
            for sub_name in self.g.subjects():
                if re.compile('(%s_)[0-9]' % system_name).search(sub_name.lower()) or \
                        re.compile('(%s)[0-9]' % system_name).search(sub_name.lower()):
                    d.update({sub_name: {'intra': dict(zip(intra_type_list, [list() for i in range(intra_type_list.__len__())])),
                                         'inter': dict(zip(inter_type_list, [list() for i in range(inter_type_list.__len__())]))
                                         }
                              })

        # 3. layer: Storage Table
        for system_key, system_dict in self.index_system.items():
            for segment_name, segment_dict in system_dict.items():
                # 3.1 intra edge
                for p, down_list in segment_dict['intra'].items():  # edge's name and downstream node list（save as list in Storage Table）
                    predicate = self.make_completed_predicate(p=p)
                    if predicate:  # maybe None
                        for obj in self.g.objects(subject=segment_name, predicate=predicate):
                            down_list.append(obj)  # e.g. obj is Damper_1, Damper_2 in slides
                    # Reverse screening
                    inverse_p = find_inverse_predicate(p=p)
                    inverse_predicate = self.make_completed_predicate(p=inverse_p)
                    if inverse_predicate:
                        for sub in self.g.subjects(predicate=inverse_predicate, object=segment_name):
                            down_list.append(sub)

                # 3.2 inter edge
                for p, down_list in segment_dict['inter'].items():
                    inter_results_list = []
                    predicate = self.make_completed_predicate(p=p)
                    multi_hop_traversal(g=self.g, subject0=segment_name, p=predicate, results_list=inter_results_list)
                    down_list.extend(inter_results_list)

    def build_func_index(self):
        """
        functionality index
        """
        # 1. layer: function
        for function_name in function_name_dict.keys():
            self.index_func.update({function_name: []}
                                   )

        # 2. list to save corresponding sensor
        for function_name, value in self.index_func.items():
            sensor_type = function_name_dict[function_name]
            completed_sensor_type = None

            # find sensor_type full name
            for obj in self.spo_dict['o']:
                if sensor_type in obj:
                    completed_sensor_type = obj
                    break

            if completed_sensor_type is None:  # this if branch means no this sensor_type in building
                continue
            # find 'type' full name
            rdf_type = None
            for p in self.spo_dict['p']:
                if 'type' in p:
                    rdf_type = p
                    break

            for sub in self.g.subjects(predicate=rdf_type, object=completed_sensor_type):
                self.index_func[function_name].append(sub)

    def build_index(self):
        self.build_system_index()
        self.build_func_index()


if __name__ == '__main__':
    ttl_file_path = PROJECT_PATH + '/hvacbrick/CP1_dy_test.ttl'
    ttl_file_path = PROJECT_PATH + '/hvacbrick/hf2.ttl'

    ind = Indexing(ttl_file_path=ttl_file_path)
    # ind.build_index()
