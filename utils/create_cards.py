#!/usr/bin/env python3

import os
import subprocess
import yaml  # type:ignore
from utils.colors import blue, cyan, green, red


def dasgoclient(commands, fname, overwrite=False, extend=True, remove=False):
    if overwrite == extend:
        raise ValueError(red("Combination not allowed"))

    test_name = "test.txt"
    with open(test_name, "w") as f:
        for command in commands:
            subprocess.call(command, shell=True, stdout=f)

    samples = []
    if os.path.exists(fname) and extend:
        with open(fname, "r") as f:
            samples = [line.strip() for line in f.readlines()]

    print(blue(f"Starting with {len(samples)} samples:"))
    print(cyan(f"    -->: {samples}"))

    with open(test_name, "r") as f:
        for line in f.readlines():
            sample = line.strip()
            if not overwrite and sample in samples:
                continue
            samples.append(sample)

    # samples = [sample for sample in samples if "ext" not in sample]
    print(blue(f"Storing {len(samples)} samples:"))
    print(green(f"    -->: {samples}"))
    if len(samples) == 0:
        print(red("No valid samples found."))

    if len(samples) != len(set(samples)):
        raise RuntimeError(red("Unexpected number of files: duplicates are found"))

    with open(fname, "w") as f:
        for sample in samples:
            f.write(f"{sample}\n")

    os.remove(test_name)
    if remove:
        os.remove(fname)
    return samples


def create_das_dataset_list(datasets, tags, fname, aod):
    commands = [
        f'dasgoclient -query="dataset=/{dataset}/*{tag}*/{aod} dataset status= VALID"'
        for dataset in datasets
        for tag in tags
    ]
    dasgoclient(commands=commands, fname=fname)


def create_card(driver_name, datasets, data):
    os.makedirs("utils/cards", exist_ok=True)
    card_name = datasets.replace("datasets/", "utils/cards/card_").replace(".txt", ".yml")
    print(blue(f"Creating card: {card_name}"))

    config = f"utils/{driver_name}_NANO.py"
    if not os.path.exists(config):
        raise ValueError(red(f"Config not found :{config}. Please run ./utils/create_drivers.py"))

    card_info = {
        "campaign": {
            "storageSite": "T2_BE_IIHE",
            "outLFNDirBase": "/store/group/phys_higgs/hinv",
            "tag_extension": "PFNano",
            "config": config,
            "data": data,
            "datasets": datasets,
        }
    }

    with open(card_name, "w") as yaml_file:
        yaml.dump(card_info, yaml_file, default_flow_style=False)


def run_data():
    # PDs to run over
    jetmet = ["JetHT", "MET", "JetMET", "JetMET0", "JetMET1"]
    egamma = ["EGamma", "EGamma0", "EGamma1", "EGamma2", "EGamma3", "EGamma4", "EGamma5"]
    datasets = jetmet + egamma

    # map to link the needed tag, driver and run to loop over
    gt_v6 = "MINIv6NANOv15"
    common_runs = ["C", "D", "E", "F", "G"]
    year_run_map = {
        "2022_CD": {"tag": "22Sep2023", "driver": "data_2022_CDE", "year": "2022", "runs": ["C", "D"]},
        "2022_E": {"tag": "22Sep2023", "driver": "data_2022_CDE", "year": "2022", "runs": ["E"]},
        "2022_FG": {"tag": "22Sep2023", "driver": "data_2022_FG", "year": "2022", "runs": ["F", "G"]},
        "2023_CD": {"tag": "22Sep2023_v*", "driver": "data_2023_CD", "year": "2023", "runs": ["C", "D"]},
        "2024": {"tag": gt_v6, "driver": "data_2024", "year": "2024", "runs": common_runs + ["H", "I"]},
        "2025": {"tag": "PromptReco", "driver": "data_2025", "year": "2025", "runs": ["B"] + common_runs},
        "2026": {"tag": "PromptReco", "driver": "data_2026", "year": "2026", "runs": ["B", "D"]},
    }

    for name, info in year_run_map.items():
        tags = [f"Run{info['year']}{run}-{info['tag']}" for run in info["runs"]]
        fname = f"datasets/data_{name}.txt"
        create_das_dataset_list(datasets=datasets, tags=tags, fname=fname, aod="MINIAOD")
        create_card(driver_name=info["driver"], datasets=fname, data=True)


def run_mc():
    # map to link the needed campaign and driver
    year_campaign_map = {
        "2022": {
            "campaign": "Run3Summer22",
            "miniaod": "MiniAODv4",
            "driver": "mc_2022",
            "GT": "130X_mcRun3_2022_realistic_v5",
        },
        "2022EE": {
            "campaign": "Run3Summer22EE",
            "miniaod": "MiniAODv4",
            "driver": "mc_2022_EE",
            "GT": "130X_mcRun3_2022_realistic_postEE_v6",
        },
        "2023": {
            "campaign": "Run3Summer23",
            "miniaod": "MiniAODv4",
            "driver": "mc_2023",
            "GT": "130X_mcRun3_2023_realistic_v*",
        },
        "2023BPix": {
            "campaign": "Run3Summer23BPix",
            "miniaod": "MiniAODv4",
            "driver": "mc_2023_BPix",
            "GT": "130X_mcRun3_2023_realistic_postBPix_v*",
        },
        "2024": {
            "campaign": "RunIII2024Summer24",
            "miniaod": "MiniAODv6",
            "driver": "mc_2024",
            "GT": "150X_mcRun3_2024_realistic_v2",
        },
    }

    tune_energy = "TuneCP5_13p6TeV"
    amcatnlo_fxfx = f"{tune_energy}_amcatnloFXFX-pythia8"
    madgraph = f"{tune_energy}_madgraph-pythia8"
    madgraph_mlm = f"{tune_energy}_madgraphMLM-pythia8"
    powheg = f"{tune_energy}_powheg-pythia8"
    powheg_madspin = f"{tune_energy}_powheg-madspin-pythia8"
    pts = ["100", "200", "400", "600"]
    ht_qcd = ["400to600", "600to800", "800to1000", "1000to1200", "1200to1500", "1500to2000", "2000"]

    # list of MC samples to run over
    def get_datasets_map(is_v6):
        bin_header = "Bin-" if is_v6 else ""
        par_header = "Par-" if is_v6 else ""
        tag = "-" if is_v6 else "_"
        wh_powheg = f"{tune_energy}_{'powhegMINLO' if is_v6 else 'powheg-minlo'}-pythia8"

        def get_higgs_sample(prod: str, is_v6: bool) -> str:
            """Build the Higgs dataset stem for one production mode and version."""
            mass = "Par-M-125" if is_v6 else "M-125"
            decay = "Hto2Zto4Nu"
            pt = "Bin-PT-150" if is_v6 else "PT-150"
            wqq = "-Wto2Q" if is_v6 else "_Wto2Q"
            zqq = "Zto2Q" if is_v6 else "_Zto2Q"
            tags = {
                "ggH": "GluGluH" if is_v6 else "GluGlu",
                "vbfH": "VBFH" if is_v6 else "VBF",
                "WHp": "WplusH" if is_v6 else "Wplus",
                "WHm": "WminusH" if is_v6 else "Wminus",
                "ZH": "ZH-Hto2Zto4Nu" if is_v6 else "ZHto2Zto4Nu",
                "ggZH": "GluGluZH-Zto2Q" if is_v6 else "GluGluZH_Zto2Q_",
            }

            tag = tags[prod]
            if is_v6:
                tag = tag + "-"
            sample = f"{tag}{decay}_{mass}"
            if prod == "ggH":
                sample = f"{tag}{decay}_{pt}_{mass}"
            if prod == "ZH":
                sample = f"{tag}{zqq}_{mass}"
            if prod == "ggZH":
                sample = f"{tag}{decay}_{mass}"
            if "WH" in prod:
                sample = f"{tag}{decay}{wqq}_{mass}"
            return sample

        datasets_map = {
            # Signal
            "HToInvisible": [
                f"{get_higgs_sample('ggH', is_v6)}_{powheg}",
                f"{get_higgs_sample('vbfH', is_v6)}_{powheg}",
                f"{get_higgs_sample('WHm', is_v6)}_{wh_powheg}",
                f"{get_higgs_sample('WHp', is_v6)}_{wh_powheg}",
                f"{get_higgs_sample('ZH', is_v6)}_{wh_powheg}",
                f"{get_higgs_sample('ggZH', is_v6)}_{powheg}",
            ],
            # V+jet
            "QCD_Znunu": [f"Zto2Nu-2Jets_{bin_header}PTNuNu-{pt}_{amcatnlo_fxfx}" for pt in pts],
            "QCD_Zll": [f"DYto2L-2Jets_{bin_header}MLL-50{tag}PTLL-{pt}_{amcatnlo_fxfx}" for pt in pts],
            "QCD_W": [f"WtoLNu-2Jets_{bin_header}PTLNu-{pt}_{amcatnlo_fxfx}" for pt in pts],
            "EWK_Zll": [f"VBFto2L_{bin_header}MLL-50_{madgraph}"],
            "EWK_Znunu": [f"VBFto2Nu_{madgraph}"],
            "EWK_W": [f"VBFtoLNu_{madgraph}"],
            "QCD_G": [
                f"GJ-4Jets-2NLO2LO_{bin_header}PTG-120_{par_header}BiasedPTG_TuneSherpaDef_13p6TeV_sherpaMEPS"
            ],
            "EWK_G": [f"VBFtoG_{bin_header}PTG-{pt}_{madgraph}" for pt in ["100to200", "200"]],
            # Minor backgrounds
            "TTbar": [f"TTto{decay}_{powheg}" for decay in ["2L2Nu", "LNu2Q"]],
            "TW": [
                f"{top}to{decay}_{powheg}" for top in ["TbarWplus", "TWminus"] for decay in ["2L2Nu", "LNu2Q"]
            ],
            "SingleT_t": [f"{top}toLNu-t-channel-4FS_{powheg_madspin}" for top in ["TbarBQ", "TBbarQ"]],
            "WW": [f"WWto{decay}_{powheg}" for decay in ["2L2Nu", "LNu2Q"]],
            "WZ": [f"WZto{decay}_{powheg}" for decay in ["2L2Q", "2Nu2Q", "3LNu", "L3Nu", "LNu2Q"]],
            "ZZ": [f"ZZto{decay}_{powheg}" for decay in ["2L2Nu", "2L2Q", "2Nu2Q", "4L"]],
            "WGamma": [f"WGto{decay}G-1Jets_{amcatnlo_fxfx}" for decay in ["2Q", "LNu"]],
            "ZGamma": [f"ZGto{decay}G-1Jets_{amcatnlo_fxfx}" for decay in ["2Q", "2Nu"]],
            "QCDJets": [f"QCD-4Jets_{bin_header}HT-{ht}_{madgraph_mlm}" for ht in ht_qcd],
        }
        return datasets_map

    for year, info in year_campaign_map.items():
        tags = [f"{info['campaign']}{info['miniaod']}-{info['GT']}"]
        is_v6 = info["miniaod"] == "MiniAODv6"
        datasets_map = get_datasets_map(is_v6)
        for sample, datasets in datasets_map.items():
            fname = f"datasets/mc_{year}_{sample}.txt"
            create_das_dataset_list(datasets=datasets, tags=tags, fname=fname, aod="MINIAODSIM")
            create_card(driver_name=info["driver"], datasets=fname, data=False)


def main():
    run_data()
    run_mc()


if __name__ == "__main__":
    main()
