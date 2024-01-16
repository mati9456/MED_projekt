import data_loader
import numpy as np
import itertools

#load dataset 
#SPMF datasets contain 1 sequance per line. Every sequance (and line) ands with -2. Every itemset ends with -1

file_path = "dataSets/BIBLE.txt"
#file_path = "dataSets/LEVIATHAN.txt"
#file_path = "dataSets/kosarak_sequences.txt"


database = data_loader.importDatabase(file_path)

def prefixSpan(database, minsup, S=[]):
    
    # find all elements
    unique_elements = np.unique(**database)
    supports = []
    
    for element in unique_elements:
        support = 0
        for sequance in database:
            if element in sequance:
                support = support + 1
        supports.append(support)






    #for i, sequance in enumerate(database):
    #    items, supports = findSupp(sequance)

        



def findSupp(sequance):
    unique_items = np.unique(itertools.chain.from_iterable(sequance))
    supports = []
    for unique_item in unique_items:
        support_for_item = 0
        for set in sequance:
            unique_in_set = np.unique(set)
            if unique_item in unique_in_set:
                support_for_item = 1
                continue
        supports.append(support_for_item)
    
    return unique_items, supports


prefixSpan(database, 3)

print("dupa")