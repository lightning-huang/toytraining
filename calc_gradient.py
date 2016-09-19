import sys,math

def sigmoid(x):
	exp_x=math.exp(x)
	return exp_x / (1.0 + exp_x)

if len(sys.argv)<5:
	print "usage: python calc_gradient.py scorefile labelfile outputfile scoreColumnIndex [weighted gradient(true/false)]"
	sys.exit(1)


scorefile=sys.argv[1]
labelfile=sys.argv[2]
outputfile=sys.argv[3]
scoreColumnIndex=int(sys.argv[4])
weightedGradient=False
if(len(sys.argv)>5 and sys.argv[5].lower()=="true"):
	weightedGradient=True
if scorefile!="0":
	scorefd=file(scorefile)
labelfd=file(labelfile)
out=file(outputfile,"w")
labelIndex=-1
weightIndex=-1
linecount=0


for lineLabel in labelfd:
	linecount+=1
	if scorefile=="0":
		lineScore="0\t0\t0\t0"
	else:
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
		if weightIndex==-1 and weightedGradient:
			print "you chose weightedGradient but m:weight(ignore case) could not be found!"
			sys.exit(1)
		out.write("m:gradient\n")
	else:
		score=float(lineScore.strip().split("\t")[scoreColumnIndex])
		lineLabel=lineLabel.strip()
		tokens=lineLabel.split("\t")
		label=float(tokens[labelIndex])
		weight=1.0
		if weightedGradient:
			weight=float(tokens[weightIndex])
		p=sigmoid(score)
		out.write(str(weight*(label-p))+"\n")
		if linecount%5000==0:
			print linecount
print linecount
if scorefile!="0":
	scorefd.close()
labelfd.close()
out.close()