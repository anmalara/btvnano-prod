# Instructions for PFNano samples

More general info can be found in the ReadME file.
This information overrules the instuctions in the ReadME file.

## Environment

At the moment, job submission to CRAB is possible only from `lxplus8`. Make sure you compile from the correct environment. Ask if you need help!!!

```bash
cmsrel CMSSW_15_0_2
cd CMSSW_15_0_2/src
cmsenv
git cms-init
git cms-merge-topic mseidel42:btvNano_150X_backport
git clone git@github.com:anmalara/btvnano-prod.git -b NanoAODv15_Summer2024
cd $CMSSW_BASE/src
scram b -j 10
cd btvnano-prod

```

Remeber to source the `setup.sh` file at each login.
```bash
source setup.sh
```

## Create drivers and cards

The campaign, Global Tag, customization, and dataset mappings are hard-coded
in the utility scripts. Update those mappings when changing the production
configuration.

Create the CMSSW driver configurations:

```bash
./utils/create_drivers.py
```

This writes files such as `utils/mc_2024_NANO.py` and
`utils/data_2024_NANO.py`. The drivers run the `NANO` step and apply the
customization configured for each campaign.

`utils/create_drivers.py` also configures the output module to select
`nanoAOD_step` and adds the `TFileService` writing `histograms.root`; these do
not need to be added manually. The selection is important whenever a filter
is placed on the NanoAOD path, because only events passing that path are
written to the output:

```python
SelectEvents=cms.untracked.PSet(SelectEvents=cms.vstring("nanoAOD_step")),
```

If a custom workflow uses an `EDFilter`, define it in the customization and
place it on the appropriate NanoAOD path. If the filter produces histograms,
you **MUST** include this line:

```python
process.TFileService = cms.Service("TFileService", fileName=cms.string("histograms.root"))
```

The generated drivers already include this service; add it manually only when
creating or editing a driver outside `utils/create_drivers.py`.

Create DAS input lists and the corresponding cards:

```bash
./utils/create_cards.py
```

The input lists are written under `datasets/`; CRAB cards are written under
`utils/cards/`. Cards follow the convention
`card_{type}_{year}_{sample}.yml`.

## Submit with CRAB

`utils/crabby.py` reads a generated card and creates one CRAB task per DAS
dataset. It uses `utils/template_crab.py` as the CRAB baseline. The template
transfers `utils/mergeHistogramInFile.py` to each worker; the CRAB executable
script should run `cmsRun` and then use that helper to merge the histogram
cycles written to `histograms.root`.

Make sure the executable script referenced by `template_crab.py`
(`utils/ScriptExe.sh`) is present before submitting.
`mergeHistogramInFile.py` reads `histograms.root` and writes the merged event
count histograms to `hists_nevents.root` by default.

Use the generated card directly with `utils/crabby.py`:

- create the CRAB configurations:
  ```bash
  python3 utils/crabby.py -c utils/cards/card_{type}_{year}_{sample}.yml --make
  ```
- submit jobs:
  ```bash
  python3 utils/crabby.py -c utils/cards/card_{type}_{year}_{sample}.yml --submit
  ```
- print the status of the generated CRAB tasks:
  ```bash
  python3 utils/crabby.py -c utils/cards/card_{type}_{year}_{sample}.yml --status
  ```
- resubmit an existing CRAB task:
  ```bash
  python3 utils/crabby.py -c utils/cards/card_{type}_{year}_{sample}.yml --resubmit
  ```

Replace `{type}`, `{year}`, and `{sample}` with the desired card components
before running the command.

Use `--test` together with `--make` to generate a one-unit configuration with
publication disabled.
