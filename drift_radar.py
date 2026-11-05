import argparse
import bisect
import csv
import json
import math
from pathlib import Path

def finite(values):
    result = [float(value) for value in values]
    if not result or any(not math.isfinite(value) for value in result):
        raise ValueError("Samples must be nonempty and finite")
    return result

def compare(reference, current, bins=10):
    if bins < 2:
        raise ValueError("bins must be at least two")
    reference, current = finite(reference), finite(current)
    ordered = sorted(reference)
    cuts = sorted(set(ordered[min(len(ordered) - 1, int(i * len(ordered) / bins))] for i in range(1, bins)))
    if ordered[0] == ordered[-1]:
        cuts = [ordered[0], math.nextafter(ordered[0], math.inf)]
    def distribution(values):
        counts = [0] * (len(cuts) + 1)
        for value in values:
            counts[bisect.bisect_right(cuts, value)] += 1
        return [(count + .5) / (len(values) + .5 * len(counts)) for count in counts]
    baseline, observed = distribution(reference), distribution(current)
    psi = sum((q - p) * math.log(q / p) for p, q in zip(baseline, observed))
    return {"psi": psi, "reference_count": len(reference), "current_count": len(current), "reference_mean": sum(reference) / len(reference), "current_mean": sum(current) / len(current), "cuts": cuts, "reference_distribution": baseline, "current_distribution": observed}

def load(path):
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("CSV needs unique column names")
        columns = {name: [] for name in reader.fieldnames}
        for row in reader:
            if None in row:
                raise ValueError("CSV row has extra fields")
            for name in columns:
                columns[name].append(float(row[name]))
        return columns

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", type=Path)
    parser.add_argument("current", type=Path)
    parser.add_argument("--threshold", type=float, default=.2)
    parser.add_argument("--bins", type=int, default=10)
    args = parser.parse_args()
    if not math.isfinite(args.threshold) or args.threshold < 0:
        parser.error("threshold must be finite and nonnegative")
    reference, current = load(args.reference), load(args.current)
    if reference.keys() != current.keys():
        parser.error("CSV schemas must match")
    report = {name: compare(reference[name], current[name], args.bins) for name in reference}
    for value in report.values():
        value["alert"] = value["psi"] > args.threshold
    print(json.dumps(report, indent=2))
    raise SystemExit(int(any(value["alert"] for value in report.values())))

if __name__ == "__main__":
    main()
