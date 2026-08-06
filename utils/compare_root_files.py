#!/usr/bin/env python3
"""Compare the Events trees of two ROOT files, matching events by identity."""

import argparse
import fnmatch
import math
import sys

import awkward as ak
import numpy as np
import uproot

EVENT_ID_BRANCHES = ("run", "luminosityBlock", "event")
PF_NANO = "MC_allPF_2024_NANO.root"
CENTRAL_NANO = "39aa9afd-1996-476a-bfac-2f891d4effde.root"
TREE_NAME = "Events"
IGNORED_BRANCHES = [
    #     "FatJetSVs",
    # "GenJetSVs",
    # "JetSVs",
    # "GenFatJetSVs",
    # "GenFatJetCands",
    # "GenJetCands",
    # "JetPFCands",
    # "FatJetPFCands",
    # "GenCands",
    "PFCands",
    # "Jet_Deep",
    # "GenPart",
    # "Electron_genPartIdx",
    # "LowPtElectron_genPartIdx",
    # "Muon_genPartIdx",
    # "Photon_genPartIdx",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Check that events and branch contents from the first ROOT file occur in the second."
    )
    parser.add_argument("--rtol", type=float, default=0.01, help="Relative float tolerance")
    parser.add_argument("--atol", type=float, default=1e-4, help="Absolute float tolerance")
    parser.add_argument(
        "--max-mismatches",
        type=int,
        default=20,
        help="Maximum value mismatches printed per branch (default: 20)",
    )
    parser.add_argument(
        "--max-events",
        type=int,
        help="Compare only the first N entries of the first file",
    )
    return parser.parse_args()


def is_ignored(branch, patterns):
    return any(
        fnmatch.fnmatchcase(branch, pattern) or branch.startswith(pattern) or branch == f"n{pattern}"
        for pattern in patterns
    )


def event_keys(tree, entry_stop=None):
    arrays = tree.arrays(EVENT_ID_BRANCHES, entry_stop=entry_stop, library="np")
    return list(zip(*(arrays[name].tolist() for name in EVENT_ID_BRANCHES)))


def build_unique_index(keys, label):
    index = {}
    duplicates = []
    for entry, key in enumerate(keys):
        if key in index:
            duplicates.append(key)
        else:
            index[key] = entry
    if duplicates:
        preview = ", ".join(map(str, duplicates[:5]))
        raise RuntimeError(f"{label} contains duplicate event identifiers: {preview}")
    return index


def values_equal(first, second, rtol, atol):
    if isinstance(first, (list, tuple)) or isinstance(second, (list, tuple)):
        if not isinstance(first, (list, tuple)) or not isinstance(second, (list, tuple)):
            return False
        return len(first) == len(second) and all(
            values_equal(a, b, rtol, atol) for a, b in zip(first, second)
        )

    if isinstance(first, dict) or isinstance(second, dict):
        if not isinstance(first, dict) or not isinstance(second, dict):
            return False
        return first.keys() == second.keys() and all(
            values_equal(first[key], second[key], rtol, atol) for key in first
        )

    if isinstance(first, (float, np.floating)) or isinstance(second, (float, np.floating)):
        try:
            if math.isnan(float(first)) and math.isnan(float(second)):
                return True
            return math.isclose(float(first), float(second), rel_tol=rtol, abs_tol=atol)
        except (TypeError, ValueError):
            return False

    return first == second


def main():
    args = parse_args()
    patterns = IGNORED_BRANCHES

    with uproot.open(PF_NANO) as first_file, uproot.open(CENTRAL_NANO) as second_file:
        first_tree = first_file[TREE_NAME]
        second_tree = second_file[TREE_NAME]
        first_branches = set(first_tree.keys())
        second_branches = set(second_tree.keys())

        branches = sorted(branch for branch in first_branches if not is_ignored(branch, patterns))
        missing_branches = sorted(set(branches) - second_branches)
        if missing_branches:
            print("Branches from the first file missing in the second:", file=sys.stderr)
            for branch in missing_branches:
                print(f"  {branch}", file=sys.stderr)

        branches = [branch for branch in branches if branch in second_branches]
        first_keys = event_keys(first_tree, args.max_events)
        second_keys = event_keys(second_tree)
        build_unique_index(first_keys, "First file")
        second_index = build_unique_index(second_keys, "Second file")

        missing_events = [key for key in first_keys if key not in second_index]
        if missing_events:
            print(f"Events from the first file missing in the second: {len(missing_events)}", file=sys.stderr)
            for key in missing_events[: args.max_mismatches]:
                print(f"  run={key[0]} luminosityBlock={key[1]} event={key[2]}", file=sys.stderr)
            return 1

        second_entries = np.asarray([second_index[key] for key in first_keys], dtype=np.int64)
        mismatched_branches = 0

        for branch in branches:
            first_values = ak.to_list(first_tree[branch].array(entry_stop=args.max_events))
            second_values = ak.to_list(second_tree[branch].array()[second_entries])
            mismatches = [
                entry
                for entry, (first, second) in enumerate(zip(first_values, second_values))
                if not values_equal(first, second, args.rtol, args.atol)
            ]
            if not mismatches:
                continue

            mismatched_branches += 1
            print(f"Branch {branch!r} differs in {len(mismatches)} event(s):", file=sys.stderr)
            for entry in mismatches[: args.max_mismatches]:
                key = first_keys[entry]
                print(
                    f"  run={key[0]} luminosityBlock={key[1]} event={key[2]} "
                    f"first={first_values[entry]!r} second={second_values[entry]!r}",
                    file=sys.stderr,
                )

    print(f"Compared {len(first_keys)} events and {len(branches)} branches.")
    print(f"Ignored {len(patterns)} branch pattern(s).")
    if missing_branches or mismatched_branches:
        print(
            f"FAILED: {len(missing_branches)} missing and {mismatched_branches} mismatched branch(es).",
            file=sys.stderr,
        )
        return 1

    print("PASS: all selected events and branch contents match.")
    return 0


if __name__ == "__main__":
    main()
