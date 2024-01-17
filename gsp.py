from collections import defaultdict
import data_loader
import numpy
import copy


def gsp(min_support, database, verbose=False):
    """
    The FreeSpan algorithm.
    """
    if min_support <= 0 or len(database) <= 0:
        return []
    l1 = generate_l1(database, min_support)
    if len(l1) == 0:
        return []
    
    print(l1)
    
    l1_database = dict2database(l1)

    candidates = generate_candidates(l1_database)
    #candidates_support = scan_candidates(database, candidates)
    candidates_support = []
    for c in candidates:
        candidates_support.append(calculate_support(c, database))

    candidates_accepted = []
    accepted_supports = []
    for index, support in enumerate(candidates_support):
        if support >= min_support:
            candidates_accepted.append(candidates[index])
            accepted_supports.append(support)

    print(candidates_accepted)
    print(accepted_supports)

    while len(candidates_accepted) != 0:
        candidates = generate_candidates(candidates_accepted)
        #candidates_support = scan_candidates(database, candidates)
        candidates_support = []
        for c in candidates:
            candidates_support.append(calculate_support(c, database))
            
        candidates_accepted = []
        accepted_supports = []
        for index, support in enumerate(candidates_support):
            if support >= min_support:
                candidates_accepted.append(candidates[index])
                accepted_supports.append(support)

        print(candidates_accepted)
        print(accepted_supports)

    
    return []


def generate_l1(database, min_support):
    """
    Calculate the support for every element (of length 1) in the database.
    """

    # In defaultdict(int) undefined elements default to 0.
    res = defaultdict(int)
    for sequence in database:
        items = set()
        items_part = set()
        for itemset in sequence:
            for item in itemset:
                if item not in items:
                    items.add(item)
        for i in items:
            res[i] += 1
    
    # remove elements with support less than min support
    res_filtered = {k: v for k, v in res.items() if v >= min_support}
    return res_filtered


def generate_candidates(L):
    candidates = []
    # L = [[{a}, {b}, {c}], [{ab}, {c}], [{ad}, {c}]]
    # elements = {a: 3, b: 2, c: 3, d: 1}
    # elements.keys()

    elements = generate_l1(L, 1)
    elements = elements.keys()

    # elements = [a,b,c,d]
    for seq in L:
        for el in elements:
            candidates.append([*seq, {el}])
            if not el in seq[-1]:
                if el > list(seq[-1])[0]:
                    continue
                candidates.append([*seq[:-1], {*seq[-1], el}])
    return candidates

def scan_candidates(database, candidates):
    supports = []
    for pattern in candidates:
        support = 0
        for sequence in database:
            count = 0
            for itemset_c in pattern:
                for itemset_s in sequence:
                    if itemset_c.issubset(itemset_s):
                        count = count + 1
                if count >= len(pattern):
                    support = support + 1
        supports.append(support)
    return supports

def calculate_support(pattern, database):
    # Initialize support count
    support_count = 0
    
    # Iterate through each sequence in the database
    for sequence in database:
        # Check if the pattern is a subsequence of the current sequence
        if is_subsequence(pattern, sequence):
            support_count += 1
    
    return support_count

def is_subsequence(pattern, sequence):
    # Initialize pointers for pattern and sequence
    pattern_pointer = 0
    sequence_pointer = 0
    
    # Iterate through the sequence
    while pattern_pointer < len(pattern) and sequence_pointer < len(sequence):
        # Check if the current itemset in the pattern is in the current itemset of the sequence
        if pattern[pattern_pointer].issubset(sequence[sequence_pointer]):
            pattern_pointer += 1
        sequence_pointer += 1
    
    # If all itemsets in the pattern are found as subsequences, return True
    return pattern_pointer == len(pattern)

def dict2database(dict):
    database = []
    for item in dict.keys():
        database.append([{item}])
    return database


file_path = "dataSets/test3.txt"

database = data_loader.importDatabase(file_path)

gsp(3, database, True)
