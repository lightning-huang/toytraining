using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace AlterRankerEnsembleWeights
{
    class WeightsAndBias
    {
        public double[] weights;
        public double bias;
    }
    class Program
    {
        private static string MakeENumberString(int count)
        {
            List<string> es = new List<string>();
            for (int i = 1; i <= count; ++i)
            {
                es.Add("E:" + i);
            }
            return string.Join("\t", es);
        }

        private static WeightsAndBias GetWeightsAndBias(string weightsTxt)
        {
            WeightsAndBias result = new WeightsAndBias();
            using (var reader = new StreamReader(weightsTxt))
            {
                string buf = null;
                List<double> weights = new List<double>();
                double bias = 0.0;
                int counter = 1;
                while ((buf = reader.ReadLine()) != null)
                {
                    if (string.IsNullOrWhiteSpace(buf))
                    {
                        continue;
                    }
                    if (buf.StartsWith("E"))
                    {
                        var tokens = buf.Split(new char[] { '\t' }, StringSplitOptions.RemoveEmptyEntries);
                        // fill the gap between full and this actual results
                        for (; ("E" + counter) != tokens[0]; counter++)
                        {
                            weights.Add(0.0);
                        }
                        if (tokens.Length == 2)
                        {
                            weights.Add(double.Parse(tokens[1]));
                        }
                        else
                        {
                            weights.Add(double.Parse(tokens[1]));
                            buf = reader.ReadLine();
                            if (string.IsNullOrWhiteSpace(buf))
                            {
                                throw new Exception("no bias found!");
                            }
                            bias = double.Parse(buf);
                        }
                        counter++;
                    }
                }
                result.weights = weights.ToArray();
                result.bias = bias;

            }
            return result;
        }

        static void Main(string[] args)
        {
            var weightsTxt = args[0];
            var modelIni = args[1];
            var output = args[2];
            var parser = new IniParser(modelIni);

            var evaluatorsString = parser.GetSetting("TreeEnsemble", "Evaluators");
            if (evaluatorsString == null)
            {
                throw new Exception("the model file is not a valid TreeEnsemble format.");
            }
            var result = GetWeightsAndBias(weightsTxt);
            var evaluators = int.Parse(evaluatorsString);
            var aggregatorIndex = -1;
            if (string.Equals(parser.GetSetting("Evaluator:" + evaluators, "EvaluatorType"), "Aggregator", StringComparison.OrdinalIgnoreCase))
            {
                if (string.Equals(parser.GetSetting("Evaluator:" + (evaluators - 1), "EvaluatorType"), "Aggregator", StringComparison.OrdinalIgnoreCase))
                {
                    if (parser.GetSetting("Evaluator:" + (evaluators - 1), "Weights") != null)
                    {
                        aggregatorIndex = evaluators - 1;
                    }
                    else
                    {
                        throw new Exception("it seems the last 2nd was the weights, but did not find it.");
                    }
                }
                else
                {
                    if (parser.GetSetting("Evaluator:" + evaluators, "Weights") != null)
                    {
                        aggregatorIndex = evaluators;
                    }
                    else
                    {
                        throw new Exception("it seems the last was the weights, but did not find it.");
                    }
                }
            }
            // aggregatorIndex==-1, add one section
            // aggregatorIndex==other, just change that one
            bool hitAggregator = false;
            bool completeWriteWeights = false;
            bool completeWriteBias = false;
            using (var reader = new StreamReader(modelIni))
            {
                using (var writer = new StreamWriter(output))
                {
                    string buf = null;
                    while ((buf = reader.ReadLine()) != null)
                    {
                        if (buf.StartsWith("Evaluators"))
                        {
                            if (aggregatorIndex == -1)
                            {
                                writer.WriteLine("Evaluators=" + (evaluators + 1));
                                continue;
                            }
                        }
                        else if (buf.Contains("[Evaluator:" + aggregatorIndex + "]"))
                        {
                            hitAggregator = true;
                        }
                        else if (buf.StartsWith("Weights") && hitAggregator && !completeWriteWeights && aggregatorIndex != -1)
                        {
                            writer.WriteLine("Weights=" + string.Join("\t", result.weights.Select(item => item.ToString("0.######"))));
                            completeWriteWeights = true;
                            continue;
                        }
                        else if (buf.StartsWith("Bias") && hitAggregator && !completeWriteBias && aggregatorIndex != -1)
                        {
                            writer.WriteLine("Bias=" + result.bias.ToString("0.######"));
                            completeWriteBias = true;
                            continue;
                        }
                        writer.WriteLine(buf);
                    }
                    if (aggregatorIndex == -1)
                    {
                        writer.WriteLine();
                        writer.WriteLine("[Evaluator:" + (evaluators + 1) + "]");
                        writer.WriteLine("EvaluatorType=Aggregator");
                        writer.WriteLine("NumNodes=" + evaluators);
                        writer.WriteLine("Nodes=" + MakeENumberString(evaluators));
                        writer.WriteLine("Weights=" + string.Join("\t", result.weights.Select(item => item.ToString("0.######"))));
                        writer.WriteLine("Type=Linear");
                        writer.WriteLine("Bias=" + result.bias.ToString("0.######"));
                    }
                }
            }
        }
    }
}
