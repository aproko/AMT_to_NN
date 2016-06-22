import csv
from collections import namedtuple
hedgeSen = namedtuple("hedgeSen", ["hedge", "sentence"])
dict = {}

with open('processed_data.csv', 'rU') as infile:
    reader = csv.reader(infile)
    next(reader, None)
    for line in reader:
        key = hedgeSen(hedge=line[1],sentence=line[2])
        if key in dict:
            dict[key].append(float(line[4]))
        else:
            dict[key] = [line[0], line[3], float(line[4])]

with open('amended_data.csv', 'w') as out:
    for key, val in dict.items():
        out.write(",".join([val[0],key.hedge,key.sentence,val[1],str(sum(val[2:])/float(len(val) - 2))]))
        out.write("\n")
