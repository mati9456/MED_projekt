
'''
load sequence data from txt file to python array
'''
def importDatabasa(path:str):
    sequences = []
    with open(path, 'r') as file:
        for line in file:
            line = line.replace(" -1 -2", "")
            itemSets = []
            for set in line.strip().split("-1"):
                itemSet = []
                for item in set.split():
                    itemSet.append(int(item))
                itemSets.append(itemSet)
            sequences.append(itemSets)
    return sequences