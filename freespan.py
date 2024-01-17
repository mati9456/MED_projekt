from collections import defaultdict
import data_loader
import numpy
import copy


def free_span(min_support, database):
    """
    The FreeSpan algorithm.
    """
    if min_support <= 0 or len(database) <= 0:
        return []
    f_list = generate_f_list(database, min_support)
    if len(f_list) == 0:
        return []
    
    f_matrix = generate_f_matrix(database, f_list)

    length2_patterns = generate_length2_patterns(f_matrix, f_list, min_support)

    repeating_item_annotation = generate_annotation_item(f_matrix, f_list, min_support)
    
    return []


def generate_f_list(database, min_support = 0):
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
    return sorted(res_filtered.items(), key=lambda x: x[1], reverse=True)


def generate_f_matrix(database, f_list):
    f_matrix = numpy.zeros((len(f_list), len(f_list), 3), dtype=int)
    for j, (item1, count) in enumerate(f_list):
        for k in range(j, len(f_list)):
            item2, _ = f_list[k]
            for sequance in database:
                # for j == k indexes (patterns of same item occuring multiple times) index 0 will be used
                if j == k:
                    count = 0
                    for itemset in sequance:
                        if item1 in itemset:
                            count = count + 1
                    if count > 1:
                        f_matrix[j][k][0] = f_matrix[j][k][0] + 1
                else:
                    item1_indexes = []
                    item2_indexes = []
                    for index, itemset in enumerate(sequance):
                        if item1 in itemset:
                            item1_indexes.append(index)
                        if item2 in itemset:
                            item2_indexes.append(index)
                    item1_before2 = False
                    item2_before1 = False
                    items_together = False
                    for index1 in item1_indexes:
                        for index2 in item2_indexes:
                            if not item1_before2 and index1 < index2:
                                item1_before2 = True
                            if not item2_before1 and index1 > index2:
                                item2_before1 = True
                            if not items_together and index1 == index2:
                                items_together = True
                    if item1_before2:
                        f_matrix[j][k][0] = f_matrix[j][k][0] + 1
                    if item2_before1:
                        f_matrix[j][k][1] = f_matrix[j][k][1] + 1
                    if items_together:
                        f_matrix[j][k][2] = f_matrix[j][k][2] + 1
    return f_matrix


def generate_length2_patterns(f_matrix, f_list, min_support):
    patterns = []
    for _ in range(0, len(f_list)):
        patterns.append([])

    for j in range(0, f_matrix.shape[0]):
        for k in range(j, f_matrix.shape[1]):
            supp = f_matrix[j][k][0]
            if supp >= min_support:
                patterns[k].append(([f_list[j][0], f_list[k][0]], supp))
            supp = f_matrix[j][k][1]
            if supp >= min_support:
                patterns[k].append(([f_list[k][0], f_list[j][0]], supp))
            supp = f_matrix[j][k][2]
            if supp >= min_support:
                patterns[k].append(([(f_list[j][0], f_list[k][0])], supp))
    return patterns


def generate_annotation_item(f_matrix, f_list, min_support):
    repeating_item_annotation = []
    for _ in range(0, len(f_list)):
        repeating_item_annotation.append([])

    for j in range(0, f_matrix.shape[0]):
        for k in range(j, f_matrix.shape[1]):
            if j == k:
                if f_matrix[j][k][0] >= min_support:
                    repeating_item_annotation[k].append(["<", f_list[j][0], "+", f_list[k][0], "+"])
            else:
                bracket = "<"
                plus1 = "="
                plus2 = "="

                if f_matrix[j][j][0] >= min_support:
                    plus1 = "+"
                if f_matrix[k][k][0] >= min_support:
                    plus2 = "+"

                if plus1 == "+" or plus2 == "+":
                    A, B, C = f_matrix[j][k]
                    if A >= min_support and B >= min_support:
                        bracket = "{"
                        repeating_item_annotation[k].append([bracket, f_list[j][0], plus1, f_list[k][0], plus2])
                    else:
                        bracket = "<"
                        if A >= min_support:
                            repeating_item_annotation[k].append([bracket, f_list[j][0], plus1, f_list[k][0], plus2])
                        if B >= min_support:
                            repeating_item_annotation[k].append([bracket, f_list[k][0], plus2, f_list[j][0], plus1])

    return repeating_item_annotation


def generate_pojection_annotation(f_matrix, f_list, min_support, length2_patterns, repeating_item_annotation):
    projection_annotation = []
    for _ in range(0, len(f_list)):
        projection_annotation.append([])

    for j in range(0, f_matrix.shape[0]):
        for k in range(j, f_matrix.shape[1]):
            for i in range(j, k):
                if (f_matrix[j][k][0] > min_support or f_matrix[j][k][1] > min_support and
                    f_matrix[k][i][0] > min_support or f_matrix[k][i][1] > min_support and
                    f_matrix[i][j][0] > min_support or f_matrix[i][j][1] > min_support
                    ):
                    

            





file_path = "dataSets/test3.txt"

database = data_loader.importDatabase(file_path)

free_span(2, database)
