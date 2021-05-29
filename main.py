from apriori import apriori
import time
from argparse import ArgumentParser
from argparse import ArgumentTypeError
from generaterules import generate_rules
from index import InvertedIndex
from item import item_str


def set_to_string(s):
    ss = ""
    for x in sorted(map(item_str, s)):
        if ss != "":
            ss += " "
        ss += str(x)
    return ss


def float_between_0_and_1(string):
    value = float(string)
    if value < 0.0 or value > 1.0:
        msg = "%r is not in range [0,1]" % string
        raise ArgumentTypeError(msg)
    return value


def float_gteq_1(string):
    value = float(string)
    if value < 1.0:
        msg = "%r is not in range [1,∞]" % string
        raise ArgumentTypeError(msg)
    return value


def main():
    parser = ArgumentParser(
        description="Association rule data mining in Python")
    parser.add_argument("--input", dest="input", required=True)
    parser.add_argument("--output", dest="output", required=True)
    parser.add_argument(
        "--min-confidence",
        dest="min_confidence",
        type=float_between_0_and_1,
        required=True)
    parser.add_argument(
        "--min-support",
        dest="min_support",
        type=float_between_0_and_1,
        required=True)
    parser.add_argument(
        "--min-lift",
        dest="min_lift",
        type=float_gteq_1,
        required=True)
    args = parser.parse_args()

    program_start = time.time()
    start = program_start
    print("Association Rule Mining using Apriori")
    print("Input file: {}".format(args.input))
    print("Output file: {}".format(args.output))
    print("Minimum support: {}".format(args.min_confidence))
    print("Minimum confidence: {}".format(args.min_support))
    print("Minimum lift: {}".format(args.min_lift))

    print("Generating frequent itemsets using Apriori...", flush=True)

    with open(args.input, "r") as f:
        data = f.read()
    index = InvertedIndex()
    index.load(data)
    print(f"Loaded {len(index)} transactions")

    itemsets_with_counts = apriori(index, args.min_support)

    itemsets = [t[0] for t in itemsets_with_counts]
    itemset_counts = {tuple(t[0]): t[1] for t in itemsets_with_counts}

    duration = time.time() - start
    print(
        "Apriori mined {} items in {:.2f} seconds".format(
            len(itemsets),
            duration),
        flush=True)

    start = time.time()
    rules = generate_rules(
        itemsets,
        itemset_counts,
        len(index),
        args.min_confidence,
        args.min_lift)
    duration = time.time() - start
    print(
        "Generated {} rules in {:.2f} seconds".format(
            len(rules),
            duration),
        flush=True)

    start = time.time()
    with open(args.output, "w") as f:
        f.write("Antecedent->Consequent,Confidence,Lift,Support\n")
        for (antecedent,
             consequent,
             confidence,
             lift,
             support) in rules:
            f.write("{} -> {},{:.4f},{:.4f},{:.4f}\n". format(set_to_string(antecedent),
                                                              set_to_string(consequent), confidence, lift, support))
    print(
        "Wrote rules to disk in {:.2f} seconds".format(
            duration),
        flush=True)

    duration = time.time() - program_start
    print("Total runtime {:.2f} seconds".format(duration))


if __name__ == "__main__":
    main()
