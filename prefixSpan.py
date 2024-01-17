from collections import defaultdict
from io import TextIOWrapper
import data_loader

"""
In this implementation sequential database is an array of sequences.
A sequence is an array of itemsets.
Itemset is a set of items (numbers).

In the written sequence notation, often an underscore symbol (_) is used
to denote that the the prefix and this itemset can form a single element.
I used -1 instead.
"""

def scan_database(database, min_support = 0):
    """
    Calculate the support for every element (of length 1) in the database.

    Returns tuple of dicts:
    - The first dict contains the supports of all elements
      if they were added to the pattern as the next itemset.
    - The second dict contains the supports of all elements
      if they were added to the last itemset in the pattern.
    """
    # In defaultdict(int) undefined elements default to 0.
    res = defaultdict(int)
    res_part = defaultdict(int)
    for sequence in database:
        items = set()
        items_part = set()
        for itemset in sequence:
            if -1 in itemset:
                for item in itemset:
                    if item not in items_part and item != -1:
                        items_part.add(item)
            else:
                for item in itemset:
                    if item not in items:
                        items.add(item)
        for i in items:
            res[i] += 1
        for i in items_part:
            res_part[i] += 1
    
    res_filtered = {k: v for k, v in res.items() if v >= min_support}
    res_part_filtered = {k: v for k, v in res_part.items() if v >= min_support}
    return res_filtered, res_part_filtered


def project_database(database, prefix, forms_one_element = False):
    """
    Project a database given a prefix (element of length 1).
    """
    res = []
    for sequence in database:
        projected_sequence = project_sequence(sequence, prefix, forms_one_element)
        if len(projected_sequence) > 0:
            res.append(projected_sequence)
    return res


def project_sequence(sequence, prefix, forms_one_element = False):
    """
    Project a sequence given a prefix (element of length 1).

    Returns a projected sequence. If the itemset, from which the item was removed,
    remained nonempty, -1 is added to this itemset to denote, that more elements
    can expand the current prefix's itemset.
    """
    for idx, itemset in enumerate(sequence):
        if not forms_one_element and -1 in itemset:
            continue
        if prefix in itemset:
            first_element = itemset.copy()
            first_element.remove(prefix)
            first_element.discard(-1)
            if len(first_element) == 0:
                return sequence[idx+1:]
            first_element.add(-1)
            return [first_element, *sequence[idx+1:]]
    return []


def prefix_span(min_support, database, output_file: TextIOWrapper, pattern = [], verbose = False):

    """
    The PrefixSpan algorithm.
    """
    if min_support <= 0 or len(database) <= 0:
        return
    elements, elements_part = scan_database(database, min_support)
    if len(elements) + len(elements_part) == 0:
        return

    for element, v in elements.items():
        projected_database = project_database(database, element)
        new_pattern = [*pattern, {element}]
        if verbose:
            print(f"Pattern: {new_pattern} has support {v}")
        output_file.write(' -1 '.join([' '.join(map(str, x)) for x in new_pattern]) + f" -1 #SUP: {v}\n")
        prefix_span(min_support, projected_database, output_file, new_pattern, verbose)
    for element_part, v in elements_part.items():
        projected_database = project_database(database, element_part, True)
        new_pattern = [*pattern[:-1], {*pattern[-1], element_part}]
        if verbose:
            print(f"Pattern: {new_pattern} has support {v}")
        output_file.write(' -1 '.join([' '.join(map(str, x)) for x in new_pattern]) + f" -1 #SUP: {v}\n")
        prefix_span(min_support, projected_database, output_file, new_pattern, verbose)


if __name__ == "__main__":
    file_path = "dataSets/BIBLE.txt"

    database = data_loader.importDatabase(file_path)

    with open('prefix_span_result.txt', 'w') as file:
        prefix_span(4000, database, file) # 11%
