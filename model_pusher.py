'''
    better under your searchgold corext window and copy this file into your searchgold folder and then run it.
    Usage for example : python model_pusher.py d:\searchgold en-us
    
    if you do not have python runtime, please install one python2.7.x and set it into the path of user environment and restart searchgold corext
'''

import sys,os,re
placeholder="<enter description here>";
fileparttag="Files:"

def path2pattern(searchgold_folder,target_net_folder):
    result=target_net_folder.replace(searchgold_folder,"")
    result=result.replace("\\","/")
    return result
    
def prepare_changelist(comment,pattern,lines):
    output=[]
    filepart=False
    for line in lines:
        if line.find(placeholder)!=-1:
            output.append(line.replace(placeholder,comment))
        elif line.startswith(fileparttag):
            filepart=True
            output.append(line)
        elif filepart:
            if line.lower().find(pattern.lower())!=-1:
                output.append(line)
        else:
            output.append(line)
    if not filepart:
        print "There are no files need to integrate, please check if there already exists pending change lists or you did nothing"
        sys.exit(-1)
    return output

    
def do_integrate(src_folder,target_folder):
    if not target_folder.endswith('AnswersRankerList.txt'):
        os.system("mkdir \""+target_folder+"\"")
    command=''' sd integrate %s\\... %s\\...  '''%(src_folder, target_folder)
    if target_folder.endswith('AnswersRankerList.txt'):
        command=''' sd integrate %s %s  '''%(src_folder, target_folder)
    os.system(command);

    command="sd resolve"
    os.system(command)

    command='''sd change -o > tmp.txt'''
    os.system(command)

    f=file("tmp.txt")
    lines=f.readlines()
    f.close()
    comment="integrate change of rankers for "+ alias +" in "+ market +" from test to canary"
    if target_folder.endswith('AnswersRankerList.txt'):
        comment="integrate change of answersrankerlist for "+ alias +" from test to canary"
    if target_folder.find('\\APlusRanker-Prod\\')!=-1:
        if target_folder.endswith('AnswersRankerList.txt'):
            comment="integrate change of answersrankerlist for "+ alias +" from canary to prod"
        else:
            comment="integrate change of rankers for "+ alias +" in "+ market +" from canary to prod"

    target_pattern=path2pattern(searchgold_folder,target_folder)

    newlines=prepare_changelist(comment,target_pattern,lines)

    f=file("tmp.txt",'w')
    f.writelines(newlines)
    f.close()

    os.system("type tmp.txt")

    command="sd change -i < tmp.txt >out_mine.txt"
    os.system(command)

    f=file("out_mine.txt")
    first_line=f.next().strip()
    f.close()

    change_id=re.match("Change (\\d+)",first_line).groups()[0]

    command="sd submit -c "+change_id
    os.system(command)

if len(sys.argv) < 3:
    print "usage: python model_pusher.py <searchgold_folder> <market> [mode]"
    print "   this command would user tmp.txt and out_mine.txt, please be careful for the file override"
    print ''' mode - nothing, the mode is to integrate models from test to canary and prod.
                     prod, the mode is to just integrate models from canary to prod.
                     rankerlist, the mode is to integrate the answersrankerlist from test to canary and prod
                     rankerlistprod, the mode is to integrate the answersrankerlist from canary to prod
                     wrong things other than those above, just treat as nothing.
    '''
    sys.exit(-1)

    
searchgold_folder=sys.argv[1]
market=sys.argv[2];
alias=os.getenv('USERNAME')
if len(sys.argv)>4:
    alias=sys.argv[4]
    print "alias change to "+alias

testfolder=searchgold_folder+"\\deploy\\builds\\data\\Answers\\AplusRanker-Test"
canaryfolder=searchgold_folder+"\\deploy\\builds\\data\\latest\\APlusRanker-Prod-canary"
prodfolder=searchgold_folder+"\\deploy\\builds\\data\\latest\\APlusRanker-Prod"




testnetfolder=testfolder+"\\"+market+"\\Experiments\\"+alias
canarynetfolder=canaryfolder+"\\"+market+"\\Experiments\\"+alias
prodnetfolder=prodfolder+"\\"+market+"\\Experiments\\"+alias

testlistfile=testfolder+"\\AnswersRankerList.txt"
canarylistfile=canaryfolder+"\\AnswersRankerList.txt"
prodlistfile=prodfolder+"\\AnswersRankerList.txt"

# 1 - nets to canary and prod from test
# 2 - nets to prod from canary
# 3 - answersrankerlist to canary and prod from test
# 4 - answersrankerlist to prod from canary
instant_prod_mode=1
if len(sys.argv)>3:
    if sys.argv[3]=='prod':
        instant_prod_mode=2
    elif sys.argv[3]=='rankerlist':
        instant_prod_mode=3
    elif sys.argv[3]=='rankerlistprod':
        instant_prod_mode=4


if instant_prod_mode==2:
    do_integrate(canarynetfolder,prodnetfolder);
elif instant_prod_mode==3:
    do_integrate(testlistfile,canarylistfile)
    choice=raw_input("Do you want to continue to integrate from canary to prod? (Y/N)")
    if choice=='Y' or choice=='y':
        print "continue..."
        do_integrate(canarylistfile,prodlistfile)
elif instant_prod_mode==4:
    do_integrate(canarylistfile,prodlistfile)
else:
    do_integrate(testnetfolder,canarynetfolder)
    choice=raw_input("Do you want to continue to integrate from canary to prod? (Y/N)")
    if choice=='Y' or choice=='y':
        print "continue..."
        do_integrate(canarynetfolder,prodnetfolder);

