import sys,math

if len(sys.argv)<2:
	print "usage: python choose.py resultfile"
	sys.exit(1)

resultfile=sys.argv[1]
resultfd=file(resultfile)
linecount=0

best=0.0
bestIndex=0
for result in resultfd:
	linecount+=1
	result=result.strip()
	resultscore=float(result)
	if resultscore>best:
		best=resultscore
		bestIndex=linecount-1
print bestIndex
resultfd.close()
