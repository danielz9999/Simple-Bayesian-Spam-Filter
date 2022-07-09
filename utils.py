def read_classification_from_file(fname):
    dict = {}
    with open(fname, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            words = line.strip().split()
            dict[words[0]] = words[1]

    
    return dict
