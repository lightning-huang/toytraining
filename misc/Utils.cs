

public class Utils 
{
    private static List<string> ResolveKeysByVotes(Dictionary<string, int> histogram)
    {
        if (histogram == null)
        {
            return null;
        }

        return histogram.GroupBy(pair => pair.Key.ToLowerInvariant()).Select(group => group.OrderByDescending(pair => pair.Value).First().Key).ToList();
    }

    private static void DumpPotentialNameIntoDict(IEnumerable<string> src, Dictionary<string, int> histogram)
    {
        if (src != null && histogram != null)
        {
            foreach (var item in src)
            {
                if (!string.IsNullOrWhiteSpace(item))
                {
                    var tempCamel = Char.ToUpperInvariant(item[0]) + (item.Length > 1 ? item.Substring(1).ToLowerInvariant() : "");

                    if (item.Length > 1 && item != tempCamel && item.Any(c => Char.IsUpper(c)))
                    {
                        if (!histogram.ContainsKey(item))
                        {
                            histogram[item] = 0;
                        }

                        histogram[item] += 1;
                    }
                }
            }
        }
    }
}