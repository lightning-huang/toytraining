import ConfigParser,sys;

def print_tree_ensemble(config, out):
	if not ("TreeEnsemble" in config.sections()):
		return
	out.write('[TreeEnsemble]\n');
	out.write('Inputs=' + config.get('TreeEnsemble','Inputs')+'\n');
	out.write('Evaluators='+config.get('TreeEnsemble','Evaluators')+'\n');
	out.write('\n')
	input_count=int(config.get('TreeEnsemble','Inputs'))
	evaluator_count=int(config.get('TreeEnsemble','Evaluators'))
	#print input sections
	for i in range(1, input_count+1):
		out.write('[Input:%s]'%i+"\n")
		if config.get('Input:%s'%i,'Transform').lower()=="linear":
			out.write('Name='+config.get('Input:%s'%i,'Name')+"\n")
			out.write('Transform='+config.get('Input:%s'%i,'Transform')+"\n")
			out.write('Slope='+config.get('Input:%s'%i,'Slope')+"\n")
			out.write('Intercept='+config.get('Input:%s'%i,'Intercept')+"\n")
		else:
			out.write('Transform='+config.get('Input:%s'%i,'Transform')+"\n")
			out.write('Expression='+config.get('Input:%s'%i,'Expression')+"\n")
		out.write('\n')
	#print evaluator sections
	for i in range(1, evaluator_count+1):
		out.write('[Evaluator:%s]'%i+"\n")
		if config.get('Evaluator:%s'%i,'EvaluatorType').lower()=="decisiontree":
			out.write('EvaluatorType='+config.get('Evaluator:%s'%i,'EvaluatorType')+"\n")
			out.write('NumInternalNodes='+config.get('Evaluator:%s'%i,'NumInternalNodes')+"\n")
			out.write('SplitFeatures='+config.get('Evaluator:%s'%i,'SplitFeatures')+"\n")
			out.write('Threshold='+config.get('Evaluator:%s'%i,'Threshold')+"\n")
			out.write('LTEChild='+config.get('Evaluator:%s'%i,'LTEChild')+"\n")
			out.write('GTChild='+config.get('Evaluator:%s'%i,'GTChild')+"\n")
			out.write('Output='+config.get('Evaluator:%s'%i,'Output')+"\n")
		else:
			out.write('EvaluatorType='+config.get('Evaluator:%s'%i,'EvaluatorType')+"\n")
			out.write('NumNodes='+config.get('Evaluator:%s'%i,'NumNodes')+"\n")
			out.write('Nodes='+config.get('Evaluator:%s'%i,'Nodes')+"\n")
			out.write('Weights='+config.get('Evaluator:%s'%i,'Weights')+"\n")
			out.write('Type='+config.get('Evaluator:%s'%i,'Type')+"\n")
			out.write('Bias='+config.get('Evaluator:%s'%i,'Bias')+"\n")
		out.write("\n")
	
	
