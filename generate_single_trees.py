import ConfigParser, sys, netprinter

config = ConfigParser.ConfigParser();
if len(sys.argv) < 3:
    print "usage: python generate_single_trees.py xx.ini outputfolder"
    sys.exit(-1)
    
netpath = sys.argv[1]
outputfolder = sys.argv[2]

config.read(netpath)

evaluatorCount = int(config.get('TreeEnsemble','Evaluators'))

for i in range (1, evaluatorCount+1):
    if config.get('Evaluator:%s'%i, 'EvaluatorType').lower() == 'decisiontree':
        outconfig = ConfigParser.ConfigParser()
        outconfig.read(netpath)
        outconfig.set('Evaluator:1','EvaluatorType','DecisionTree')
        outconfig.set("Evaluator:1",'NumInternalNodes',config.get("Evaluator:%s"%i,'NumInternalNodes'));
        outconfig.set("Evaluator:1",'SplitFeatures',config.get("Evaluator:%s"%i,'SplitFeatures'));
        outconfig.set("Evaluator:1",'Threshold',config.get("Evaluator:%s"%i,'Threshold'));
        outconfig.set("Evaluator:1",'LTEChild',config.get("Evaluator:%s"%i,'LTEChild'));
        outconfig.set("Evaluator:1",'GTChild',config.get("Evaluator:%s"%i,'GTChild'));
        outconfig.set("Evaluator:1",'Output',config.get("Evaluator:%s"%i,'Output'));
        outconfig.set('TreeEnsemble','Evaluators','1')
        for j in range (2, evaluatorCount+1):
            outconfig.remove_section("Evaluator:%s"%j)
        print "E%d.ini ready to output"%i
        out=file((outputfolder+"\\E%d.ini")%i,'w')
        netprinter.print_tree_ensemble(outconfig,out)
        out.close()