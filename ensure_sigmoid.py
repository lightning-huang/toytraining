import ConfigParser,sys,netprinter

config=ConfigParser.ConfigParser();
if len(sys.argv)<3:
	print "usage: python ensure_sigmoid.py xxx.ini output.ini"
	sys.exit(1)
	

netpath=sys.argv[1]
outpath=sys.argv[2]
config.read(netpath)

evaluatorCount=int(config.get('TreeEnsemble','Evaluators'))
needAddSigmoid=True;
index=evaluatorCount
while config.get('Evaluator:%s'%index,'EvaluatorType').lower()=='aggregator':
	if config.get('Evaluator:%s'%index,'Type').lower()=="sigmoid":
		needAddSigmoid=False
	index-=1
if needAddSigmoid:
	config.set('TreeEnsemble','Evaluators',str(evaluatorCount+1))
	config.add_section('Evaluator:%s'%(evaluatorCount+1))
	config.set('Evaluator:%s'%(evaluatorCount+1), 'EvaluatorType', 'Aggregator')
	config.set('Evaluator:%s'%(evaluatorCount+1), 'NumNodes', '1')
	config.set('Evaluator:%s'%(evaluatorCount+1), 'Nodes', 'E:%s'%evaluatorCount)
	config.set('Evaluator:%s'%(evaluatorCount+1), 'Weights', '1.0')
	config.set('Evaluator:%s'%(evaluatorCount+1), 'Type', 'Sigmoid')
	config.set('Evaluator:%s'%(evaluatorCount+1), 'Bias', '0.0')
out=file(outpath,'w')
netprinter.print_tree_ensemble(config, out)
out.close()
	
