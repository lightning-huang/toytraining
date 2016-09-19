import sys,os,re
#
#  put this file into the branch\private\package before running.
#
ansranker_path = "Xap.Service.AnswersRanker.Product\\src\\AnswersRanker\\AnswersRanker\\ProdExperiment\\"
entityplugin_path = "Xap.Service.Entityplugin.Product\\src\\EntityPlugin\\EntityPlugin\\ProdExperiment\\"
generic_pattern = "newName\\s*=\\s*\"%s\"\s+newVersion=\"(.+)\""
key_workflows = ["AnswersRanker.Workflow_AnswersRankerPreProcess", "AnswersRanker.Workflow_AnswersRanker", "AnswersRanker.Workflow_BackgroundAnswerWorkflow", "AnswersRanker.Workflow_FeatureExtraction"]
global_versions={}
def ansranker_workflow_read_visitor(arg, dirname, fnames):
    for xml in fnames:
        xmlpath = os.path.join(dirname,xml)
        f = file(xmlpath)
        for line in f:
            line = line.strip()
            if not line: continue
            for key_workflow in key_workflows:
                current_pattern = generic_pattern%key_workflow
                m = re.search(current_pattern, line)
                if m:
                    this_version = m.group(1)
                    if global_versions.has_key(key_workflow):
                        if global_versions[key_workflow] != this_version:
                            raise Exception("the workflow " + key_workflow + " in answers ranker prod experiment folder has inconsistent versions")
                        else:
                            pass
                    else:
                        global_versions[key_workflow] = this_version
        f.close()

def entityplugin_workflow_write_visitor(arg, dirname, fnames):
    for xml in fnames:
        xmlpath = os.path.join(dirname,xml)
        f = file(xmlpath)
        output_buff = []
        need_write_back = False
        for line in f:
            raw_line = line
            output_buff.append(raw_line)
            line = line.strip()
            if not line: continue
            for key_workflow in key_workflows:
                current_pattern = generic_pattern%key_workflow
                m = re.search(current_pattern, line)
                if m:
                    this_version = m.group(1)
                    whole_match_str = m.group(0)
                    if this_version != global_versions[key_workflow]:
                        need_write_back = True
                        new_str = whole_match_str.replace(this_version, global_versions[key_workflow])
                        newline = raw_line.replace(whole_match_str, new_str)
                        output_buff[-1] = newline
        f.close()
        if need_write_back:
            os.system("sd edit "+ xmlpath)
            out_file = file(xmlpath, 'w')
            out_file.writelines(output_buff)
            out_file.close()
        

os.path.walk(ansranker_path, ansranker_workflow_read_visitor, "*.xml")
os.path.walk(entityplugin_path, entityplugin_workflow_write_visitor, "*.xml")

      