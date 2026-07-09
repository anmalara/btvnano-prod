# btvnano-prod

Based from pfnano-prod from [Congqiao](colizz/pfnano-prod)

Submit crab jobs for btvNano production using crabb.py. 


**This branch is set for CMSSW_15_0_X_2026-01-19-2300 for NanoV15 production (N.B.: experimental, upgrading to the latest CMSSW version is recommended).**

## Instruction for user 
Step 1: setup up cmssw & setup crab

```bash
cmsrel CMSSW_15_0_X_2026-01-19-2300
cd CMSSW_15_0_X_2026-01-19-2300/src
## if not on lxplus with cc7
source /cvmfs/grid.cern.ch/centos7-umd4-ui-4_200423/etc/profile.d/setup-c7-ui-example.sh
source /cvmfs/cms.cern.ch/common/crab-setup.sh prod # note: this is new w.r.t. 106X instructions
source /cvmfs/cms.cern.ch/cmsset_default.sh
## if on lxplus
crabsetup
### 
cmsenv
git cms-merge-topic Ming-Yan:130X-fixPuppi_NanoV12
scram b -j 10
```

Step 2: setup `btvnano-prod` 

```bash
git clone https://github.com/cms-btv-pog/btvnano-prod.git -b NanoAODv15_Summer2024
```

Step 2.1 modify the configuration in `crab_ymls`



```yaml

  workArea: data_2022_MINIAODv4_BTagMu
  storageSite: T2_XXX # ===>  change to your storage site
  outLFNDirBase: /store/user/XXX/PFNano_Run3/data_2022_MINIAODv4 # XXX to be user name
  voGroup:  # or if you are dcms
```

Step 3: submit crab jobs configured in `crab_ymls/`.

```bash
# make the submit python file and submit
python3 crabby.py -c crab_ymls/XXX --make --submit 
# Only generate configuration
python3 crabby.py -c crab_ymls/XXX --make 
# This disable publish config and produce single file per dataset
python3 crabby.py -c crab_ymls/XXX --make --submit --test True
```

Step 4: track the production status using nice tool from Jan van der Linden

https://github.com/JanvanderLinden/mrCrabs/tree/main


Step 5: Creation of csv tables with the job progress status.

There is a standalone script ```crab_status.py``` which takes the crab directory from your work area as an input and parses the job status info in a csv table. The csv files are saved in the btveos-www area and can be monitored in browser. It takes a second input of your submitted yml script to make a comparison between datasets and the crab directory outputs. 

First install `yaml`, `pandas`, and `matplotlib`:
```
pip install pyyaml --user
pip install pandas --user
pip install matplotlib --user
```

Usage:
```python
python crab_status.py <crab_dir_path> <crab_yml to compare>
# example
python crab_status.py mc_summer22_MINIAODv4_qcdmu/ crab_ymls/mc_summer22_MINIAODv4_qcdmu.yml 
```

Additionally it produces progress plots for each jobs. You can monitor them here:
```https://btvweb.web.cern.ch/BTVNanoProduction/ProgressPlots/```
To view your tables:
```https://btvweb.web.cern.ch/BTVNanoProduction/csvoutputs/prod_tables.php```
In the drop down menu, select the process that you've produced.


## How to update

0. prepare `cmsDriver` commands according XPOG recipe or check with the request ID

MC: Find the [NANOAOD request](https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=BTV-Run3Summer23BPixNanoAODv12-00001&page=0&shown=127) in McM, and click the third icon in actions. The script contains MC driver commands
data: Get the request ID from [pMp](https://cms-pdmv-prod.web.cern.ch/pmp/historical?r=27Jun2023&showDoneRequestsList=true), replace with the ID of the dataset for the following link `ReReco-Run2023D-BTagMu-22Sep2023_v1-00001` to your ID [https://cms-pdmv-prod.web.cern.ch/rereco/api/requests/get_cmsdriver/ReReco-Run2023D-BTagMu-22Sep2023_v1-00001](https://cms-pdmv-prod.web.cern.ch/rereco/api/requests/get_cmsdriver/ReReco-Run2023D-BTagMu-22Sep2023_v1-00001)

<details><summary>cms driver commands</summary>
<p>

  ### data 2022 NanoV12
  ```
  cmsDriver.py data_2022_22Sep2023 --conditions 130X_dataRun3_v2 --datatier NANOAOD --era Run3,run3_miniAOD_12X --eventcontent NANOAOD --filein /store/data/Run2022C/BTagMu/MINIAOD/22Sep2023-v1/40000/fc8f31f6-4bf7-4b51-8f6d-ef0833c1e383.root --fileout file:data_defaultAK4.root --nThreads 4 --number -1 --scenario pp --step NANO --data --customise PhysicsTools/NanoAOD/custom_btv_cff.PrepBTVCustomNanoAOD_DATA --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000;process.NANOAODoutput.fakeNameForCrab = cms.untracked.bool(True)" --no_exec
  ```
  ### MC 2022 NanoV12- preEE
  ```
  cmsDriver.py MC_preEE2022_22Sep2023 --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:MC_defaultAK4_preEE.root --conditions 130X_mcRun3_2022_realistic_v5 --step NANO --scenario pp --filein /store/mc/Run3Summer22MiniAODv4/QCD_PT-15to20_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2022_realistic_v5-v2/2520000/056b90db-c5cf-4f5f-a4cb-1c69bf4e65b5.root --era Run3  --mc -n -1 --customise PhysicsTools/NanoAOD/custom_btv_cff.PrepBTVCustomNanoAOD_MC  --nThreads 4  --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000;process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)"  --no_exec
```
  ### MC 2022 NanoV12 -postEE
  ```
  cmsDriver.py MC_2022_22Sep2023 --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:MC_defaultAK4.root --conditions 130X_mcRun3_2022_realistic_postEE_v6 --step NANO --scenario pp --filein /store/mc/Run3Summer22EEMiniAODv4/QCD_PT-15to20_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2022_realistic_postEE_v6-v2/2520000/177762d0-23ed-436f-aa0d-a20c33e33dc3.root --era Run3  --mc -n -1 --customise PhysicsTools/NanoAOD/custom_btv_cff.PrepBTVCustomNanoAOD_MC  --nThreads 4  --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000;process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)"  --no_exec
```
  ### data 2023 NanoV12
  ```
  cmsDriver.py data_2023_22Sep2023 --conditions 130X_dataRun3_Prompt_v1 --datatier NANOAOD --era Run3 --eventcontent NANOAOD --filein /store/data/Run2023C/BTagMu/MINIAOD/22Sep2023_v2-v1/2540000/0a4d9d3c-566d-48f2-886d-fbd4d5d513cf.root --fileout file:data_defaultAK4_2023.root --nThreads 2 --no_exec --number -1  --scenario pp --step NANO --data  --customise "PhysicsTools/NanoAOD/custom_btv_cff.PrepBTVCustomNanoAOD_DATA"
```

  ### MC 2023 NanoV12 - preBPix 
  ```
cmsDriver.py MC_Summer23 --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:MC_defaultAK4_2023.root --conditions 130X_mcRun3_2023_realistic_v14 --step NANO --scenario  pp --era Run3_2023 --mc -n -1   --filein /store/mc/Run3Summer23BPixMiniAODv4/DYTo2L_MLL-4to50_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_postBPix_v2-v1/60000/661a9e9a-e693-4216-9ea1-8d03793951ab.root  --customise PhysicsTools/NanoAOD/custom_btv_cff.PrepBTVCustomNanoAOD_MC  --nThreads 4  --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000;process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)"  --no_exec
```
  ### MC 2023 NanoV12 -postBPix 
  ```
  cmsDriver.py MC_Summer23_postBPix --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:MC_defaultAK4_2023_postBpix.root --conditions 130X_mcRun3_2023_realistic_postBPix_v2 --step NANO --scenario pp --filein /store/mc/Run3Summer23BPixMiniAODv4/DYTo2L_MLL-4to50_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_postBPix_v2-v1/60000/661a9e9a-e693-4216-9ea1-8d03793951ab.root --era Run3_2023 --no_exec --mc -n -1 --customise PhysicsTools/NanoAOD/custom_btv_cff.PrepBTVCustomNanoAOD_MC  --nThreads 4  --customise_commands="process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)));process.MessageLogger.cerr.FwkReport.reportEvery=1000;process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)"  --no_exec
  ```

</p>
</details>

1. add golden json to `jsons/`
2. add additional dict in `samples.yml` with campaign name with list of samples


## Notes for developer (TBD)

```yaml
data_2022_MINIAODv4: 
    BTagMu: 
        - /BTagMu/Run2022C-22Sep2023-v1/MINIAOD
        - /BTagMu/Run2022D-22Sep2023-v1/MINIAOD
        - /BTagMu/Run2022E-22Sep2023-v1/MINIAOD
        - /BTagMu/Run2022F-22Sep2023-v2/MINIAOD
        - /BTagMu/Run2022G-22Sep2023-v1/MINIAOD
```

2. replace following lines in `make_yml.py` then do `python make_yml.py`

```python
# production_yml_prefix:config_python
config_prefix = {
    'mc_summer22_MINIAODv4': 'MC_preEE2022_22Sep2023',
    'mc_summer22EE_MINIAODv4': 'MC_2022_22Sep2023',
    'data_2022_MINIAODv4': 'data_2022_22Sep2023',
}
# BTV Tag name
tag_extension = 'BTV_Run3_2022_Comm_MINIAODv4'  
# Lumimask for data, put 
lumimask='Cert_Collisions2022_355100_362760_Golden.json'
```

