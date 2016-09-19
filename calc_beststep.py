import sys,math

if len(sys.argv)<4:
	print "usage: python calc_beststep.py scorefile scoreIndex gradientfile"
	sys.exit(1)


scorefile=sys.argv[1]
scoreColumnIndex=int(sys.argv[2])
gradientfile=sys.argv[3]

scorefd=file(scorefile)
gradientfd=file(gradientfile)


linecount=0
result=0.0

for linescore in scorefd:
	linecount+=1
	linescore=linescore.strip()
	gradientline=gradientfd.next()
	gradientline=gradientline.strip()
	if not linescore:
		break
	if not gradientline:
		break
	if linecount==1:
		pass
	else:
		score=float(linescore.split("\t")[scoreColumnIndex])
		gradient=float(gradientline)
		result+=score*gradient
print result
scorefd.close()
gradientfd.close()