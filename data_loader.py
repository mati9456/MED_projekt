
def importDatabase(path: str):
    """
    Load sequence data from txt file to array
    """
    sequences = []
    with open(path, 'r') as file:
        for line in file:
            line = line.replace(" -1 -2", "")
            sequence = []
            for item_set in line.strip().split("-1"):
                items = item_set.split()
                sequence.append(set([int(x) for x in items]))
            sequences.append(sequence)
    return sequences