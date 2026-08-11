#!/usr/bin/env python3
"""Compare the Events trees of two ROOT files, matching events by identity."""

import argparse
import fnmatch
import math
import sys

import awkward as ak  # type: ignore
import numpy as np
import uproot  # type: ignore

EVENT_ID_BRANCHES = ("run", "luminosityBlock", "event")
PFNANO = "MC_allPF_2024_NANO.root"
NANO = "39aa9afd-1996-476a-bfac-2f891d4effde.root"
TREE_NAME = "Events"
JET_PT_MIN = 20.0
HF_JET_PT_MIN = 50.0
JET_MATCH_DR = 0.1
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
    "L1_",
    "HLT_",
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
    parser.add_argument("--pfnano", type=str, default=PFNANO, help="PFNano ROOT file")
    parser.add_argument("--nano", type=str, default=NANO, help="central NanoAOD ROOT file")
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
    idx = {}
    duplicates = []
    for entry, key in enumerate(keys):
        if key in idx:
            duplicates.append(key)
        else:
            idx[key] = entry
    if duplicates:
        preview = ", ".join(map(str, duplicates[:5]))
        raise RuntimeError(f"{label} contains duplicate event identifiers: {preview}")
    return idx


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


def delta_phi(first, second):
    """Return the absolute angular separation, accounting for phi wrapping."""
    difference = abs(float(first) - float(second))
    return min(difference, 2.0 * math.pi - difference)


def delta_r(first_eta, first_phi, second_eta, second_phi):
    return math.hypot(float(first_eta) - float(second_eta), delta_phi(first_phi, second_phi))


def match_objects(first, second):
    """Match collection objects above the pT threshold one-to-one by direction."""
    first_high = [idx for idx, pt in enumerate(first["pt"]) if pt is not None and float(pt) > JET_PT_MIN]
    second_high = [idx for idx, pt in enumerate(second["pt"]) if pt is not None and float(pt) > JET_PT_MIN]

    candidates = []
    for first_idx in first_high:
        for second_idx in second_high:
            distance = delta_r(
                first["eta"][first_idx],
                first["phi"][first_idx],
                second["eta"][second_idx],
                second["phi"][second_idx],
            )
            if distance <= JET_MATCH_DR:
                candidates.append((distance, first_idx, second_idx))

    matches = []
    used_first = set()
    used_second = set()
    for _, first_idx, second_idx in sorted(candidates):
        if first_idx in used_first or second_idx in used_second:
            continue
        matches.append((first_idx, second_idx))
        used_first.add(first_idx)
        used_second.add(second_idx)

    unmatched_first = [idx for idx in first_high if idx not in used_first]
    unmatched_second = [idx for idx in second_high if idx not in used_second]
    return matches, unmatched_first, unmatched_second


def compare_collection_branch(
    branch,
    first_values,
    second_values,
    collection_matches,
    count_branch,
    rtol,
    atol,
    first_pt=None,
    second_pt=None,
    object_pt_min=None,
):
    """Compare a collection after dropping low-pT objects and aligning matches."""
    mismatches = []
    compared_first = []
    compared_second = []
    for entry, (matches, unmatched_first, unmatched_second) in enumerate(collection_matches):
        if branch == count_branch:
            first_value = len(matches) + len(unmatched_first)
            second_value = len(matches) + len(unmatched_second)
        else:
            first_row = first_values[entry]
            second_row = second_values[entry]
            selected_matches = matches
            if object_pt_min is not None:
                selected_matches = [
                    (first_idx, second_idx)
                    for first_idx, second_idx in matches
                    if max(first_pt[entry][first_idx], second_pt[entry][second_idx]) >= object_pt_min
                ]
            first_value = [first_row[first_idx] for first_idx, _ in selected_matches]
            second_value = [second_row[second_idx] for _, second_idx in selected_matches]

        compared_first.append(first_value)
        compared_second.append(second_value)
        values_differ = not values_equal(first_value, second_value, rtol, atol)
        if values_differ or (branch == count_branch and (unmatched_first or unmatched_second)):
            mismatches.append(entry)
    return mismatches, compared_first, compared_second


def main():
    args = parse_args()
    patterns = IGNORED_BRANCHES

    with uproot.open(args.pfnano) as first_file, uproot.open(args.nano) as second_file:
        first_tree = first_file[TREE_NAME]
        second_tree = second_file[TREE_NAME]
        first_branches = set(first_tree.keys())
        second_branches = set(second_tree.keys())

        branches = sorted(branch for branch in first_branches if not is_ignored(branch, patterns))
        missing_branches = sorted(set(branches) - second_branches)
        missing_in_first = sorted(
            branch
            for branch in second_branches
            if branch not in first_branches and not is_ignored(branch, patterns)
        )
        if missing_branches:
            print("Branches from the first file missing in the second:", file=sys.stderr)
            for branch in missing_branches:
                print(f"  {branch}", file=sys.stderr)
        if missing_in_first:
            print("Branches from the second file missing in the first:", file=sys.stderr)
            for branch in missing_in_first:
                print(f"  {branch}", file=sys.stderr)

        branches = [branch for branch in branches if branch in second_branches]
        first_keys = event_keys(first_tree, args.max_events)
        second_keys = event_keys(second_tree)
        build_unique_index(first_keys, "First file")
        second_idx = build_unique_index(second_keys, "Second file")

        missing_events = [key for key in first_keys if key not in second_idx]
        if missing_events:
            print(f"Events from the first file missing in the second: {len(missing_events)}", file=sys.stderr)
            for key in missing_events[: args.max_mismatches]:
                print(f"  run={key[0]} luminosityBlock={key[1]} event={key[2]}", file=sys.stderr)
            return 1

        second_entries = np.asarray([second_idx[key] for key in first_keys], dtype=np.int64)
        jet_kinematics = ("Jet_pt", "Jet_eta", "Jet_phi")
        first_jet_values = {
            branch: ak.to_list(first_tree[branch].array(entry_stop=args.max_events))
            for branch in jet_kinematics
        }
        second_jet_values = {branch: ak.to_list(second_tree[branch].array()) for branch in jet_kinematics}
        jet_matches = [
            match_objects(
                {key: first_jet_values[f"Jet_{key}"][entry] for key in ("pt", "eta", "phi")},
                {key: second_jet_values[f"Jet_{key}"][second_entry] for key in ("pt", "eta", "phi")},
            )
            for entry, second_entry in enumerate(second_entries)
        ]
        first_jet_pt = first_jet_values["Jet_pt"]
        second_jet_pt = [second_jet_values["Jet_pt"][entry] for entry in second_entries]
        corr_kinematics = {"pt": "CorrT1METJet_rawPt", "eta": "CorrT1METJet_eta", "phi": "CorrT1METJet_phi"}
        first_corr_values = {
            key: ak.to_list(first_tree[branch].array(entry_stop=args.max_events))
            for key, branch in corr_kinematics.items()
        }
        second_corr_values = {
            key: ak.to_list(second_tree[branch].array()) for key, branch in corr_kinematics.items()
        }
        corr_matches = [
            match_objects(
                {key: first_corr_values[key][entry] for key in corr_kinematics},
                {key: second_corr_values[key][second_entry] for key in corr_kinematics},
            )
            for entry, second_entry in enumerate(second_entries)
        ]
        mismatched_branches = 0

        for branch in branches:
            first_values = ak.to_list(first_tree[branch].array(entry_stop=args.max_events))
            second_values = ak.to_list(second_tree[branch].array()[second_entries])
            if branch == "nJet" or branch.startswith("Jet_"):
                collection_matches = jet_matches
                count_branch = "nJet"
                object_pt_min = HF_JET_PT_MIN if branch.startswith("Jet_hf") else None
                first_collection_pt = first_jet_pt
                second_collection_pt = second_jet_pt
            elif branch == "nCorrT1METJet" or branch.startswith("CorrT1METJet_"):
                collection_matches = corr_matches
                count_branch = "nCorrT1METJet"
                object_pt_min = None
                first_collection_pt = None
                second_collection_pt = None
            else:
                collection_matches = None

            if collection_matches is not None:
                mismatches, compared_first, compared_second = compare_collection_branch(
                    branch,
                    first_values,
                    second_values,
                    collection_matches,
                    count_branch,
                    args.rtol,
                    args.atol,
                    first_collection_pt,
                    second_collection_pt,
                    object_pt_min,
                )
            else:
                compared_first = first_values
                compared_second = second_values
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
                    f"first={compared_first[entry]!r} second={compared_second[entry]!r}",
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
