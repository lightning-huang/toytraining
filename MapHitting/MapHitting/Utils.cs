using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MapHitting
{
    public class Utils
    {
        private static Dictionary<string, HashSet<string>> QueryMap = new Dictionary<string, HashSet<string>>();
        private static bool ResourceParsed = false;

        public static bool TriggerQuery(string resourceFile, string normalizedQuery, string market)
        {
            if (!ResourceParsed)
            {
                var lines = File.ReadAllLines(resourceFile).Where(line => !string.IsNullOrWhiteSpace(line)).Select(line => line.Trim()).ToList();
                
                foreach (var line in lines)
                {
                    var tokens = line.Split('\t');
                    var endIndex = tokens[0].LastIndexOf(',');
                    var query = tokens[0].Substring(0, endIndex);
                    var marketInData = tokens[1];
                    if (!QueryMap.ContainsKey(marketInData))
                    {
                        QueryMap[marketInData] = new HashSet<string>();
                    }
                    QueryMap[marketInData].Add(query);
                }
                ResourceParsed = true;
            }

            if (QueryMap.ContainsKey(market))
            {
                return QueryMap[market].Contains(normalizedQuery);
            }
            return false;
        }
    }
}
