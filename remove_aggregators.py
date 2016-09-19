import ConfigParser,sys,netprinter

config=ConfigParser.ConfigParser();
if len(sys.argv)<3:
    print "usage: python remove_aggregators.py xxx.ini output.ini"
    sys.exit(1)
    

netpath=sys.argv[1]
outpath=sys.argv[2]
config.read(netpath)

evaluatorCount=int(config.get('TreeEnsemble','Evaluators'))

index=evaluatorCount
while index>=1:
    if config.get('Evaluator:%s'%index,'EvaluatorType').lower()=='aggregator':
        if index < evaluatorCount:
            for i in range(index+1, evaluatorCount+1):
                config.remove_section('Evaluator:%s'%(i-1))
                config.add_section('Evaluator:%s'%(i-1))
                config.set('Evaluator:%s'%(i-1),'EvaluatorType','DecisionTree')
                config.set("Evaluator:%s"%(i-1),'NumInternalNodes',config.get("Evaluator:%s"%i,'NumInternalNodes'));
                config.set("Evaluator:%s"%(i-1),'SplitFeatures',config.get("Evaluator:%s"%i,'SplitFeatures'));
                config.set("Evaluator:%s"%(i-1),'Threshold',config.get("Evaluator:%s"%i,'Threshold'));
                config.set("Evaluator:%s"%(i-1),'LTEChild',config.get("Evaluator:%s"%i,'LTEChild'));
                config.set("Evaluator:%s"%(i-1),'GTChild',config.get("Evaluator:%s"%i,'GTChild'));
                config.set("Evaluator:%s"%(i-1),'Output',config.get("Evaluator:%s"%i,'Output'));
            config.remove_section('Evaluator:%s'%evaluatorCount)
        else:
            config.remove_section('Evaluator:%s'%index)
        evaluatorCount-=1
    index-=1
config.set('TreeEnsemble','Evaluators',str(evaluatorCount))
print evaluatorCount
print config.get('TreeEnsemble','Evaluators')
out=file(outpath,'w')
netprinter.print_tree_ensemble(config, out)
out.close()
    
