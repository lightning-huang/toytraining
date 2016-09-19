import sys

if len(sys.argv)<3:
    print "usage: python csvline2tsv.py inputfile outputfile"
    sys.exit(1)

    
input=file(sys.argv[1])
allheader=set()
dicts=[]
for line in input:
    line=line.strip()
    if line:
        tokens=line.split(',')
        onedict={}
        for token in tokens:
            pair=token.split(':')
            allheader.add(pair[0])
            onedict[pair[0]]=pair[1]
        dicts.append(onedict)

input.close()

output=file(sys.argv[2],'w')
allheader=list(allheader)
output.write('\t'.join(allheader)+"\n");
for one in dicts:
    line = []
    for key in allheader:
        if one.has_key(key):
            line.append(one[key])
        else:
            line.append('0')
    output.write('\t'.join(line)+"\n")
output.close()