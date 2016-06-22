import csv


#We want output in the form Label \t Text (5 word window)

outlines = []

def get5words(hedgeWord, context):
    startIndex = context.find(hedgeWord)
    prev = context[:startIndex]
    prev = prev.strip()
    prevWords = prev.split()
    after = context[startIndex + len(hedgeWord):]
    after = after.strip()
    afterWords = after.split()
    
    print context
    print hedgeWord
    print prevWords
    print afterWords

    if len(prevWords) == 0:
        words = ["start", "start"]
    elif len(prevWords) == 1:
        words = ["start", prev[0]]
    else:
        words = [prevWords[len(prevWords) - 2],prevWords[len(prevWords) - 1]]

    words.append(hedgeWord)

    if len(afterWords) == 0:
        words.append("stop")
        words.append("stop")
    elif len(afterWords) == 1:
        words.append(afterWords[0])
        words.append("stop")
    else:
        words.append(afterWords[0])
        words.append(afterWords[1])

    return words




def main():
    with open('amended_data.csv', 'rU') as input:
        reader = csv.reader(input)
        for line in reader:
            hedge = line[1]
            
            sentence = line[2]
           
            judgment = float(line[3])
       
            text = " ".join(get5words(hedge, sentence))
            output_text = str(int(judgment)) + "\t" + text
            outlines.append(output_text)


    with open('output.txt', 'w') as out:
        for l in outlines:
            out.write(l)
            out.write("\n")


main()
