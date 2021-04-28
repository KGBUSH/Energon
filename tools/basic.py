# -*- coding: utf-8 -*-

"""

@file: basic.py
@time: 2021/1/13 8:34 下午
@desc:

"""
from config import reverse_pairs_list
import time


def find_inverse_predicate(p):
    """ find_inverse_predicate, can return None """
    for s in reverse_pairs_list:
        if p in s:
            s_tmp = s.copy()
            s_tmp.remove(p)
            return s_tmp.pop()
    return None  # not all predicate has inverse value


def multi_hop_traversal(g, subject0, p, results_list):
    """
    based on（across system）predicate，find all system that initial subject0 can visit
    subject0: initial node while traverse
    """
    # 3.2 inter edge
    # for predicate, down_list in segment_dict['inter'].items():  # edge's name and downstream list（ save as lsit in Storage Table）
    for obj in g.objects(subject=subject0, predicate=p):
        results_list.append(obj)
        # recursively
        multi_hop_traversal(g=g, subject0=obj, p=p, results_list=results_list)  # the second parameter


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


class TimeRecorder(object):
    def __init__(self):
        self.tick_time = 0

    def tick(self):
        self.tick_time = time.time()

    def tock(self, process_name):
        now = time.time()
        elpased = now - self.tick_time
        self.tick_time = now
        print("\n\n[%s] used time : %8.6fs" % (process_name, elpased))
