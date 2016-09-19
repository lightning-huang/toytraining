using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace AlterRankerEnsembleWeights
{
    public class IniParser
    {
        private Hashtable keyPairs = new Hashtable();
        private string iniFilePath;

        private struct SectionPair
        {
            public string Section;
            public string Key;
        }

        public IniParser(string iniPath)
        {
            TextReader iniFile = null;
            string strLine = null;
            string currentRoot = null;
            string[] keyPair = null;
            iniFilePath = iniPath;

            if (File.Exists(iniPath))
            {
                try
                {
                    iniFile = new StreamReader(iniPath);
                    strLine = iniFile.ReadLine();
                    while (strLine != null)
                    {
                        strLine = strLine.Trim();
                        if (strLine.StartsWith(";"))
                        {
                            strLine = iniFile.ReadLine();
                            continue;
                        }
                        if (strLine != "")
                        {
                            if (strLine.StartsWith("[") && strLine.EndsWith("]"))
                            {
                                // all the sectionName is in lowercase except ROOT
                                currentRoot = strLine.Substring(1, strLine.Length - 2).ToLower();
                            }
                            else
                            {
                                string multilineItem = strLine;
                                while (multilineItem != null && multilineItem.EndsWith("_"))
                                {
                                    multilineItem = iniFile.ReadLine();
                                    strLine = strLine.Remove(strLine.Length - 1, 1) + multilineItem;
                                }
                                keyPair = strLine.Split(new char[] { '=' }, 2);
                                SectionPair sectionPair;
                                string value = null;
                                if (currentRoot == null)
                                    currentRoot = "root";
                                sectionPair.Section = currentRoot;
                                sectionPair.Key = keyPair[0];
                                if (keyPair.Length > 1)
                                    value = keyPair[1];
                                keyPairs[sectionPair] = value;
                            }
                        }
                        strLine = iniFile.ReadLine();
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine(iniPath);
                    Console.WriteLine(currentRoot);
                    Console.WriteLine(keyPair[0]);
                    Console.WriteLine(keyPair[1]);
                    throw ex;
                }
                finally
                {
                    if (iniFile != null)
                        iniFile.Close();
                }
            }
            else
                throw new FileNotFoundException("Unable to locate " + iniPath);

        }

        public string GetSetting(string sectionName, string settingName)
        {
            SectionPair sectionPair;
            sectionPair.Section = sectionName.ToLower();
            sectionPair.Key = settingName;

            return (string)keyPairs[sectionPair];
        }



        public string[] EnumSection(string sectionName)
        {
            List<string> tmpArray = new List<string>();
            foreach (SectionPair pair in keyPairs.Keys)
            {
                if (pair.Section == sectionName.ToLower())
                    tmpArray.Add(pair.Key);
            }
            return tmpArray.ToArray();
        }
    }
}
