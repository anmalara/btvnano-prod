#!/usr/bin/env python3

import os
from utils.colors import green, blue


def modify_file(file_path):

    with open(file_path, "r") as file:
        lines = file.readlines()

    modified_lines = []

    # Loop through each line and add modifications when the match is found
    for line in lines:
        modified_lines.append(line)

        if "outputCommands=process.NANOAOD" in line and "EventContent.outputCommands," in line:
            modified_lines.append(
                '    SelectEvents=cms.untracked.PSet(SelectEvents=cms.vstring("nanoAOD_step")),\n'
            )

        if "Additional output definition" in line:
            modified_lines.append(
                'process.TFileService = cms.Service("TFileService", fileName=cms.string("histograms.root"))\n'
            )

    with open(file_path, "w") as file:
        file.writelines(modified_lines)

    print(f"File '{file_path}' successfully modified.")


def create_driver(name, info):
    gt = info["GT"]
    driver_type = name.split("_", 1)[0]
    if driver_type not in {"data", "mc"}:
        raise ValueError(f"Driver name must start with data_ or mc_: {name}")
    eventcontent = "NANOAOD" if driver_type == "data" else "NANOAODSIM"
    customs = info["customs"]
    era = info.get("era", "Run3")
    command = f"cmsDriver.py {name} --{driver_type} --eventcontent {eventcontent} --datatier {eventcontent} --step NANO --conditions {gt} --era {era} --nThreads 4 -n -1 --no_exec"
    for custom in customs:
        command += f" --customise={custom}"
    command += f" --customise_commands=\"process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000;process.{eventcontent}output.fakeNameForCrab = cms.untracked.bool(True)\""
    print(blue("Creating driver with:"))
    print(green("  --> " + command))
    os.system(command)
    print(blue("Moved to ./utils/"))
    os.system(f"mv {name}_NANO.py utils/")
    os.system(f"black utils/{name}_NANO.py")
    modify_file(f"utils/{name}_NANO.py")


def main():
    year_run_map = {
        "data_2022_CDE": {
            "GT": "150X_dataRun3_v5",
            "customs": ["pfnano_cff.PFnano_customize"],
        },
        "data_2022_FG": {
            "GT": "150X_dataRun3_v5",
            "customs": ["pfnano_cff.PFnano_customize"],
        },
        "data_2023_CD": {
            "GT": "150X_dataRun3_v5",
            "customs": ["pfnano_cff.PFnano_customize"],
        },
        "data_2024": {
            "GT": "150X_dataRun3_v2",
            "customs": ["pfnano_cff.PFnano_customize"],
        },
        "data_2025": {
            "GT": "150X_dataRun3_Prompt_v1",
            "customs": ["pfnano_cff.PFnano_customize"],
        },
        "data_2026": {
            "GT": "161X_dataRun3_Prompt_v1",
            "customs": ["pfnano_cff.PFnano_customize"],
        },
        "mc_2022": {
            "GT": "150X_mcRun3_2024_realistic_v2",
            "customs": ["pfnano_cff.PFnano_customize"],
        },
        "mc_2022_EE": {
            "GT": "150X_mcRun3_2024_realistic_v2",
            "customs": ["pfnano_cff.PFnano_customize"],
        },
        "mc_2023": {
            "GT": "150X_mcRun3_2024_realistic_v2",
            "customs": ["pfnano_cff.PFnano_customize"],
        },
        "mc_2023_BPix": {
            "GT": "150X_mcRun3_2024_realistic_v2",
            "customs": ["pfnano_cff.PFnano_customize"],
        },
        "mc_2024": {
            "GT": "150X_mcRun3_2024_realistic_v4",
            "customs": ["pfnano_cff.PFnano_customize"],
        },
        "mc_2024Vtx": {
            "GT": "150X_mcRun3_2024_realistic_v4",
            "customs": ["pfnano_cff.PFVtxnano_customize", "addPFCands_cff.addGenStable"],
        },
    }

    for name, info in year_run_map.items():
        create_driver(name=name, info=info)

    return


if __name__ == "__main__":
    main()
