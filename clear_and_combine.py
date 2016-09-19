import ConfigParser,sys,netprinter;

config1=ConfigParser.ConfigParser();
config2=ConfigParser.ConfigParser();
outConfig=ConfigParser.ConfigParser();
if len(sys.argv)<4:
    print "usage: python clear_and_combine.py net1.ini net2.ini output.ini"
    sys.exit(-1);
net1path=sys.argv[1];
net2path=sys.argv[2];
outfile=sys.argv[3];

config1.read(net1path);
config2.read(net2path);

def EnsureTreeEnsemble(netpath,config):
    if not ('TreeEnsemble' in config.sections()):
        print "%s should be a tree ensemble!"%netpath;
        sys.exit(1);

def ProcessInput(config, netpath, featurenameset, freeformset, dictForIndex):
    inputCount=config.getint('TreeEnsemble','Inputs');
    print "%s has %s input"%(netpath,inputCount);
    for i in range(1,inputCount+1):
        if config.get('Input:%s'%i,"Transform").lower()=="linear":
            featurenameset.add(config.get('Input:%s'%i,'Name').lower());
            dictForIndex[i]=config.get('Input:%s'%i,'Name').lower();
        elif config.get('Input:%s'%i,"Transform").lower()=="freeform":
            freeformset.add(config.get('Input:%s'%i,'Expression').lower());
            dictForIndex[i]=config.get('Input:%s'%i,'Expression').lower();

def FindLastTree(config, realLast):
    result=realLast;
    while config.get("Evaluator:%s"%result,'EvaluatorType').lower()=="aggregator":
        result-=1;
    return result;

def TransformNative2Global(dictlocal, globaldict, input):
    tokens=input.split('\t');
    output=[];
    for token in tokens:
        num=int(token.split(":")[1]);
        name=dictlocal[num];
        index=globaldict[name];
        output.append("I:%s"%index);
    return "\t".join(output);
    
if __name__=="__main__":
    EnsureTreeEnsemble(net1path,config1);
    EnsureTreeEnsemble(net2path,config2);
    featurenameset=set();
    freeformset=set();
    #index to name
    dict1={};
    dict2={};
    ProcessInput(config1, net1path, featurenameset, freeformset, dict1);
    ProcessInput(config2, net2path, featurenameset, freeformset, dict2);
    evaluatorCount1=config1.getint("TreeEnsemble","Evaluators");
    print "%s has %s evaluators"%(net1path,evaluatorCount1)
    lastTreeIndex1=FindLastTree(config1,evaluatorCount1)
    print "%s has %s decision trees"%(net1path, lastTreeIndex1)
    evaluatorCount2=config2.getint("TreeEnsemble","Evaluators")
    print "%s has %s evaluators"%(net2path,evaluatorCount2);
    lastTreeIndex2=FindLastTree(config2,evaluatorCount2)
    print "%s has %s decision trees"%(net2path, lastTreeIndex2)
    
    outConfig.add_section('TreeEnsemble');
    outConfig.set('TreeEnsemble','Inputs' , str(len(featurenameset)+len(freeformset)))
    outConfig.set('TreeEnsemble','Evaluators', str(lastTreeIndex1 + lastTreeIndex2))
    #name to index
    globaldict={}
    index=1
    for freeform in freeformset:
        globaldict[freeform]=index;
        outConfig.add_section('Input:%s'%index);
        outConfig.set('Input:%s'%index,'Transform','FreeForm');
        outConfig.set('Input:%s'%index,'Expression',freeform);
        index+=1;
    for name in featurenameset:
        globaldict[name]=index;
        outConfig.add_section('Input:%s'%index)
        outConfig.set('Input:%s'%index,'Name',name);
        outConfig.set('Input:%s'%index,'Transform','linear');
        outConfig.set('Input:%s'%index,'Slope','1');
        outConfig.set('Input:%s'%index,'Intercept','0');
        index+=1;
    index=1
    for i in range(1,lastTreeIndex1+1):
        if config1.get("Evaluator:%s"%i,'EvaluatorType').lower()!="aggregator":
            outConfig.add_section("Evaluator:%s"%index)
            outConfig.set("Evaluator:%s"%index,'EvaluatorType','DecisionTree');
            outConfig.set("Evaluator:%s"%index,'NumInternalNodes',config1.get("Evaluator:%s"%i,'NumInternalNodes'));
            outConfig.set("Evaluator:%s"%index,'SplitFeatures',TransformNative2Global(dict1, globaldict,config1.get("Evaluator:%s"%i,'SplitFeatures')));
            outConfig.set("Evaluator:%s"%index,'Threshold',config1.get("Evaluator:%s"%i,'Threshold'));
            outConfig.set("Evaluator:%s"%index,'LTEChild',config1.get("Evaluator:%s"%i,'LTEChild'));
            outConfig.set("Evaluator:%s"%index,'GTChild',config1.get("Evaluator:%s"%i,'GTChild'));
            outConfig.set("Evaluator:%s"%index,'Output',config1.get("Evaluator:%s"%i,'Output'));
            index+=1;
    for i in range(1,lastTreeIndex2+1):
        if config2.get("Evaluator:%s"%i,'EvaluatorType').lower()!="aggregator":
            outConfig.add_section("Evaluator:%s"%index)
            outConfig.set("Evaluator:%s"%index,'EvaluatorType','DecisionTree');
            outConfig.set("Evaluator:%s"%index,'NumInternalNodes',config2.get("Evaluator:%s"%i,'NumInternalNodes'));
            outConfig.set("Evaluator:%s"%index,'SplitFeatures',TransformNative2Global(dict2, globaldict,config2.get("Evaluator:%s"%i,'SplitFeatures')));
            outConfig.set("Evaluator:%s"%index,'Threshold',config2.get("Evaluator:%s"%i,'Threshold'));
            outConfig.set("Evaluator:%s"%index,'LTEChild',config2.get("Evaluator:%s"%i,'LTEChild'));
            outConfig.set("Evaluator:%s"%index,'GTChild',config2.get("Evaluator:%s"%i,'GTChild'));
            outConfig.set("Evaluator:%s"%index,'Output',config2.get("Evaluator:%s"%i,'Output'));
            index+=1;
    outConfig.set('TreeEnsemble','Evaluators', str(index-1))
    out=file(outfile,'w');
    netprinter.print_tree_ensemble(outConfig, out)
    out.close();
    print "combine finished to %s"%outfile
