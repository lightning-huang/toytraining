import sys,math


if len(sys.argv)<4:
	print "usage: python calc_loss.py scorefile labelfile scoreColumnIndex [weightedLoss(true/false)]"
	sys.exit(1)
	

scorefile=sys.argv[1]
labelfile=sys.argv[2]
scoreColumnIndex=int(sys.argv[3])
weightedLoss=False
if(len(sys.argv)>4 and sys.argv[4].lower()=="true"):
	weightedLoss=True
scorefd=file(scorefile)
labelfd=file(labelfile)
labelIndex=-1
weightIndex=-1
linecount=0
totalLoss=0.0

for lineLabel in labelfd:
	linecount+=1
	lineScore=scorefd.next()
	if not lineLabel:
		break
	if linecount==1:
		lineLabel=lineLabel.strip()
		tokens=lineLabel.split("\t")
		columnIndex=0
		for token in tokens:
			if token.lower()=="m:label":
				labelIndex=columnIndex
			elif token.lower()=="m:weight":
				weightIndex=columnIndex
			columnIndex+=1
		if labelIndex==-1:
			print "could not found m:label (ignore case)!"
			sys.exit(1)
		if weightIndex==-1 and weightedLoss:
			print "you chose weightedLoss but m:weight(ignore case) could not be found!"
			sys.exit(1)
	else:
		score=float(lineScore.strip().split("\t")[scoreColumnIndex])
		lineLabel=lineLabel.strip()
		tokens=lineLabel.split("\t")
		label=float(tokens[labelIndex])
		weight=1.0
		if weightedLoss:
			weight=float(tokens[weightIndex])
		totalLoss+= weight*(math.log(1.0+math.exp(score)) - score*label)
print totalLoss
scorefd.close()
labelfd.close()