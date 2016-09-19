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
for key in allheader:
    if dicts[0].has_key(key) and dicts[1].has_key(key):
        if dicts[0][key]!=dicts[1][key]:
            output.write(key+"\t"+dicts[0][key]+"\t"+dicts[1][key]+"\n");
    else:
        if dicts[0].has_key(key):
            output.write(key+"\t"+dicts[0][key]+"\t"+"0\n")
        elif dicts[1].has_key(key):
            output.write(key+"\t0\t"+dicts[1][key]+"\n")
output.close()