from collections import defaultdict
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


def prefix_span(min_support, database, pattern = []):
    """
    The PrefixSpan algorithm.
    """
    if min_support <= 0 or len(database) <= 0:
        return []
    elements, elements_part = scan_database(database, min_support)
    if len(elements) + len(elements_part) == 0:
        return []
    
    if len(elements) > 0:
        for element, v in elements.items():
            print(f"Pattern: {[*pattern, {element}]} has support {v}")
    if len(elements_part) > 0:
        for element_part, v in elements_part.items():
            print(f"Pattern: {[*pattern[:-1], {*pattern[-1], element_part}]} has support {v}")

    for element, _ in elements.items():
        projected_database = project_database(database, element)
        prefix_span(min_support, projected_database, [*pattern, {element}])
    for element_part, _ in elements_part.items():
        projected_database = project_database(database, element_part, True)
        prefix_span(min_support, projected_database, [*pattern[:-1], {*pattern[-1], element_part}])


# def write_patterns_to_file(patterns, output_file):
#     with open(output_file, 'w') as file:
#         for pattern in patterns:
#             file.write(str(pattern) + '\n')


if __name__ == "__main__":
    file_path = "dataSets/test.txt"

    database = data_loader.importDatabase(file_path)

    # a,b,c,d = 1,2,3,4
    # database = [
    #     [{a,b}, {c}, {a}],
    #     [{a,b}, {b}, {c}],
    #     [{b}, {c}, {d}],
    #     [{b}, {a,b}, {c}]
    # ]

    prefix_span(2, database)
