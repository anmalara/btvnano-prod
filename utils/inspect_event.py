#!/usr/bin/env python3
"""Inspect one event in two NanoAOD files, including jet matching."""

import argparse
import math

import awkward as ak
import numpy as np
import uproot

RUN = 1
LUMI = 1014
EVENT = 4784441
JET_PT_THRESHOLDS = (15.0, 20.0, 30.0)
MATCH_DR = 0.2


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", help="first NanoAOD file, normally PFNano")
    parser.add_argument("second", help="second NanoAOD file, normally central NanoAOD")
    return parser.parse_args()


def find_event(tree):
    arrays = tree.arrays(["run", "luminosityBlock", "event"], library="np")
    matches = np.flatnonzero(
        (arrays["run"] == RUN)
        & (arrays["luminosityBlock"] == LUMI)
        & (arrays["event"] == EVENT)
    )
    if len(matches) != 1:
        raise RuntimeError(f"Expected one matching event, found {len(matches)}")
    return int(matches[0])


def value(tree, entry, branch):
    if branch not in tree.keys():
        return None
    array = tree[branch].array(entry_start=entry, entry_stop=entry + 1, library="ak")
    return ak.to_list(array)[0]


def collection(tree, entry, name):
    count = value(tree, entry, f"n{name}")
    if count is None:
        return []

    fields = (
        "pt",
        "eta",
        "phi",
        "mass",
        "rawPt",
        "rawMass",
        "rawFactor",
        "jetId",
        "nConstituents",
    )
    values = {field: value(tree, entry, f"{name}_{field}") for field in fields}
    objects = []
    for index in range(int(count)):
        objects.append(
            {
                "index": index,
                **{
                    field: values[field][index]
                    if values[field] is not None and index < len(values[field])
                    else None
                    for field in fields
                },
            }
        )
    return objects


def delta_phi(first, second):
    return (first - second + math.pi) % (2 * math.pi) - math.pi


def delta_r(first, second):
    return math.hypot(first["eta"] - second["eta"], delta_phi(first["phi"], second["phi"]))


def match_objects(first, second):
    candidates = []
    for left in first:
        for right in second:
            if left["eta"] is None or right["eta"] is None:
                continue
            candidates.append((delta_r(left, right), left["index"], right["index"]))

    matches = []
    used_first = set()
    used_second = set()
    for distance, left, right in sorted(candidates):
        if distance > MATCH_DR or left in used_first or right in used_second:
            continue
        matches.append((distance, left, right))
        used_first.add(left)
        used_second.add(right)
    return matches, sorted(set(obj["index"] for obj in first) - used_first), sorted(
        set(obj["index"] for obj in second) - used_second
    )


def print_collection(label, objects):
    print(f"{label}: {len(objects)} objects")
    for obj in objects:
        values = " ".join(
            f"{field}={obj[field]}"
            for field in ("pt", "eta", "phi", "mass", "rawPt", "rawFactor", "nConstituents")
            if obj[field] is not None
        )
        print(f"  [{obj['index']}] {values}")


def print_collection_comparison(first, second, name):
    first_objects = collection(first["tree"], first["entry"], name)
    second_objects = collection(second["tree"], second["entry"], name)
    print_collection(f"first {name}", first_objects)
    print_collection(f"second {name}", second_objects)

    matches, unmatched_first, unmatched_second = match_objects(first_objects, second_objects)
    print(f"{name} matches with deltaR < {MATCH_DR}:")
    for distance, left, right in matches:
        first_object = first_objects[left]
        second_object = second_objects[right]
        print(
            f"  first[{left}] <-> second[{right}] deltaR={distance:.4f} "
            f"pt={first_object['pt']} -> {second_object['pt']}"
        )

    print(f"unmatched first {name}: {unmatched_first}")
    print(f"unmatched second {name}: {unmatched_second}")
    if name == "Jet":
        for threshold in JET_PT_THRESHOLDS:
            first_count = sum(obj["pt"] is not None and obj["pt"] > threshold for obj in first_objects)
            second_count = sum(obj["pt"] is not None and obj["pt"] > threshold for obj in second_objects)
            print(f"jets with pt > {threshold:g}: first={first_count} second={second_count}")
        for label, objects, indices in (
            ("first", first_objects, unmatched_first),
            ("second", second_objects, unmatched_second),
        ):
            for index in indices:
                obj = objects[index]
                print(
                    f"  unmatched {label} Jet[{index}]: pt={obj['pt']} "
                    f"eta={obj['eta']} phi={obj['phi']} "
                    f"passes pt>15={obj['pt'] > 15 if obj['pt'] is not None else None} "
                    f"passes pt>20={obj['pt'] > 20 if obj['pt'] is not None else None}"
                )


def print_extra_branches(first, second):
    for label, info in (("first", first), ("second", second)):
        print(f"{label} extra collection sizes:")
        for branch in (
            "nCorrT1METJet",
            "nPFCands",
            "nFatJetPFCand",
            "FatJetPFCand_jetIdx",
            "FatJetPFCand_pfCandIdx",
        ):
            item = value(info["tree"], info["entry"], branch)
            if item is not None:
                print(f"  {branch}={item}")


def main():
    args = parse_args()
    with uproot.open(args.first) as first_file, uproot.open(args.second) as second_file:
        first_tree = first_file["Events"]
        second_tree = second_file["Events"]
        first = {"tree": first_tree, "entry": find_event(first_tree)}
        second = {"tree": second_tree, "entry": find_event(second_tree)}

        print(f"event: run={RUN} luminosityBlock={LUMI} event={EVENT}")
        print(f"first: {args.first}, entry={first['entry']}")
        print(f"second: {args.second}, entry={second['entry']}")
        print_extra_branches(first, second)
        for name in ("Jet", "FatJet", "CorrT1METJet"):
            print_collection_comparison(first, second, name)


if __name__ == "__main__":
    main()
