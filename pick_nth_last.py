import ConfigParser,sys,netprinter

config=ConfigParser.ConfigParser();
if len(sys.argv)<3:
    print "usage: python pick_nth_last.py xxx.ini output.ini nth"
    sys.exit(1)
    

netpath=sys.argv[1]
outpath=sys.argv[2]
index=int(sys.argv[3])-1
config.read(netpath)

evaluatorCount=int(config.get('TreeEnsemble','Evaluators'))

pickIndex=evaluatorCount-index;
config.set('Evaluator:1','EvaluatorType','DecisionTree')
config.set("Evaluator:1",'NumInternalNodes',config.get("Evaluator:%s"%pickIndex,'NumInternalNodes'));
config.set("Evaluator:1",'SplitFeatures',config.get("Evaluator:%s"%pickIndex,'SplitFeatures'));
config.set("Evaluator:1",'Threshold',config.get("Evaluator:%s"%pickIndex,'Threshold'));
config.set("Evaluator:1",'LTEChild',config.get("Evaluator:%s"%pickIndex,'LTEChild'));
config.set("Evaluator:1",'GTChild',config.get("Evaluator:%s"%pickIndex,'GTChild'));
config.set("Evaluator:1",'Output',config.get("Evaluator:%s"%pickIndex,'Output'));
for i in range(2, evaluatorCount+1):
    config.remove_section('Evaluator:%s'%i)
evaluatorCount=1
config.set('TreeEnsemble','Evaluators',str(evaluatorCount))
print evaluatorCount
print config.get('TreeEnsemble','Evaluators')
out=file(outpath,'w')
netprinter.print_tree_ensemble(config, out)
out.close()
    
