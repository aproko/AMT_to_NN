import os
from os import listdir
from os.path import isfile, join
import datetime
import csv
import sys
import itertools
import numpy

input_filename = sys.argv[1]

def addFields(csv_string_list):
    HIT_judgments = {}
    for csv_string in csv_string_list:

        for i in range(0,9):
            #Each entry key is a string of the sentenceID and the hedgeword
            #Each entry is a list [sentence, hedgeword, yes_judgment, no_judgment]
            ent_key = ",".join([csv_string[37+i*9],csv_string[39+i*9]])
            if ent_key in HIT_judgments:
                entry = HIT_judgments[ent_key]
            else:
                entry = [csv_string[38 + i*9], csv_string[39 + i*9], 0,0]


            if csv_string[119+i] == "n":
                entry[3] = entry[3] + 1
            else:
                entry[2] = entry[2] + 1
 

            HIT_judgments[ent_key] = list(entry)

    #We find what the majority vote judgment was 
    for ent, jud in HIT_judgments.items():
        agreement = float(jud[2])/float(jud[3]+jud[2])
        if agreement > 0.5:
            final = 1.0
        else:
            final = 0.0
            agreement = 1 - agreement
        #jud[0] is the sentence, jud[1] is the hedgeword, and we return the final judgment and the agreement as lists to allow easier merging later on
        HIT_judgments[ent] = [jud[0], jud[1], [final], [agreement]]
    return  HIT_judgments

def addAgreement(all_hits, new_hits):
    for hit_key, hit_value in new_hits.items():
        if hit_key in all_hits:
            ent = all_hits[hit_key]
            ent[2] = ent[2] + hit_value[2]
            ent[3] = ent[3] + hit_value[3]
            all_hits[hit_key] = ent
          
        else:
            all_hits[hit_key] = hit_value
    return all_hits

def process(hit_list, turkers):
    return itertools.combinations(hit_list, turkers)


def main():

    fileLines = {}
    with open(input_filename, 'rU') as input_file:
        reader = csv.reader(input_file)
        next(reader, None)
        first_line = reader.next()
        current_HIT_id = first_line[0]
     
        hits = {}
        one_hit_lines = []
        hit_agr = {}
        
        #We aggregate all the results of one HIT first
        one_hit_lines.append(first_line)
            
        for line in reader:
            if line[0] == current_HIT_id:
                
                #Check if the answer to the check question is correct
                if line[36] == line[118]:
                    one_hit_lines.append(line)
            else:
                #Once we get to a new HIT, we process the previous HIT's results
                hitLines = process(one_hit_lines, len(one_hit_lines))
                count = 0
            
                for it in hitLines:
                    count += 1
                    hits = addFields(it) #returns dictionary of (SentenceID --> [Sentence, Hedge, 1/0 majority vote]
                    hit_agr = addAgreement(hit_agr, hits) # 1/0 majority vote to existing other judgments:  (SentenceID --> [Sentence, Hedge, mj_vote1, mj_vote2, ..., mj_voten]
                for kkk, vvv in hit_agr.items():
                    hit_agr[kkk] = [vvv[0], vvv[1], numpy.mean(vvv[2]), numpy.mean(vvv[3])]
                fileLines.update(hit_agr)
                current_HIT_id = line[0]
                one_hit_lines = []
                if line[36] == line[118]:
                    one_hit_lines.append(line)
                        
        hitLines = process(one_hit_lines, len(one_hit_lines))
        count = 0
        for it in hitLines:
            count += 1
            hits = addFields(it)
            hit_agr = addAgreement(hit_agr, hits)
        for kk, vv in hit_agr.items():
            hit_agr[kk] = [vv[0], vv[1], numpy.mean(vv[2]), numpy.mean(vv[3])]
        fileLines.update(hit_agr)



        with open("processed_data.csv", 'w') as outFile:
            outFile.write("SentenceID,HedgeWord,Sentence,Final,Agreement\n")
            for item, value in fileLines.items():
                fi = value[2]
                if value[2] > 1.0:
                    fi = value[2] / 2
                agr = value[3]
                if value[3] > 1.0:
                    agr = value[3] / 2
                outFile.write(item + "," + ",".join(["\""+value[0]+"\"", str(fi), str(agr)]))
                outFile.write("\n")

main()
