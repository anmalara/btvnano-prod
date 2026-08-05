# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: MC_allPF_2023_preBPix --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions auto:phase1_2023_realistic --step NANO --nThreads 4 --era Run3,run3_nanoAOD_pre142X --filein /store/mc/Run3Summer23MiniAODv4/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/0092e4e1-8cb2-4c2f-b57a-4fa2f42a517f.root -n 100 --customise PhysicsTools/NanoAOD/custom_btv_cff.BTVCustomNanoAOD_allPF --no_exec --customise_commands process.genWeightsTable.keepAllPSWeights=True
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3
from Configuration.Eras.Modifier_run3_nanoAOD_pre142X_cff import run3_nanoAOD_pre142X

process = cms.Process("NANO", Run3, run3_nanoAOD_pre142X)

# import of standard configurations
process.load("Configuration.StandardSequences.Services_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load("SimGeneral.MixingModule.mixNoPU_cfi")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("PhysicsTools.NanoAOD.nano_cff")
process.load("Configuration.StandardSequences.EndOfProcess_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.maxEvents = cms.untracked.PSet(
    input=cms.untracked.int32(-1), output=cms.optional.untracked.allowed(cms.int32, cms.PSet)
)

# Input source
process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(
        ##TTBAR
        # "/store/mc/Run3Summer23MiniAODv4/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/0a66bac8-1932-4250-978e-93334cbefbc3.root", #27k
        # "/store/mc/Run3Summer23MiniAODv4/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/0a6ce090-6ccd-443c-b438-6811140d27ae.root", #27k
        # "/store/mc/Run3Summer23MiniAODv4/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/0c7b8c74-be41-4b10-ad82-eff4632b86b1.root", #12k
        # "/store/mc/Run3Summer23MiniAODv4/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/0cb3154d-f1db-4ac1-90b2-8a024405ac82.root", # 39k
        # "/store/mc/Run3Summer23MiniAODv4/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/0d753283-c052-4313-a81a-96195cae3f18.root", # 27k
        # "/store/mc/Run3Summer23MiniAODv4/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/0e123dec-9b5f-45f0-85dd-cb7aa14a86a9.root", # 27k
        # "/store/mc/Run3Summer23MiniAODv4/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/0e3ed7af-7684-4eda-8062-c12e7de92d19.root", #30k
        # "/store/mc/Run3Summer23MiniAODv4/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/0f39906a-c5c2-4a2d-9b47-4418172095f3.root", #27k
        # "/store/mc/Run3Summer23MiniAODv4/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/0f575c91-f79f-4cc8-9945-3c1ed52a4133.root", #27k
        # QCD 300to800
        # "/store/mc/Run3Summer23MiniAODv4/QCD_PT-300to470_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2530000/1db91dca-6303-498a-8af5-ac8d4245afa9.root",  #44k
        # "/store/mc/Run3Summer23MiniAODv4/QCD_PT-300to470_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2530000/2619b13e-9f59-4698-ada7-e2c45d3becac.root",  #44k
        # "/store/mc/Run3Summer23MiniAODv4/QCD_PT-300to470_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2530000/2b6ae049-a088-4eed-b38c-4626e5d201ac.root",  #44k
        # "/store/mc/Run3Summer23MiniAODv4/QCD_PT-470to600_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2530000/0cefad84-2a2d-4437-b823-ff1174d79671.root",  #23k
        # "/store/mc/Run3Summer23MiniAODv4/QCD_PT-470to600_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2530000/0ded25a0-fe67-4ab6-a63c-a2d8247a9dc7.root",  #29k
        # "/store/mc/Run3Summer23MiniAODv4/QCD_PT-470to600_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2530000/10c20574-0d30-4ca4-a6b4-879a5a49e882.root",  #41k
        # "/store/mc/Run3Summer23MiniAODv4/QCD_PT-600to800_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/066fd0a2-3ba0-4802-bf25-0c8d33b51b59.root",  #33k
        # "/store/mc/Run3Summer23MiniAODv4/QCD_PT-600to800_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/069be365-b68b-40b6-b194-f3bfcedb2a65.root",  #40k
        # "/store/mc/Run3Summer23MiniAODv4/QCD_PT-600to800_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/073fb367-2d35-4096-ae5b-53a3f0123379.root",  #40k
        # QCD extra 15to300 and 800toinf
        # "/store/mc/Run3Summer23MiniAODv4/QCD_PT-15to20_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v3/2520000/00a76d11-1ab4-4d3d-a0fb-28186f592990.root", #29k done
        # "/store/mc/Run3Summer23MiniAODv4/QCD_PT-20to30_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/090953ca-59db-472e-867e-69d8733b320e.root", #29k
        "/store/mc/Run3Summer23MiniAODv4/QCD_PT-30to50_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2530000/0450bc9b-c5c2-4b59-a4b3-cf848d77493b.root",  # 12k
        "/store/mc/Run3Summer23MiniAODv4/QCD_PT-50to80_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/09f0a32d-5070-4792-8962-a5f98745d3a8.root",  # 3k
        "/store/mc/Run3Summer23MiniAODv4/QCD_PT-80to120_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/332463d1-d695-4d93-8b7e-01ef0a8d8ad3.root",  # 26k
        "/store/mc/Run3Summer23MiniAODv4/QCD_PT-120to170_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/1cde0559-d349-4275-b1c2-6e0c675bbccf.root",  # 30k
        "/store/mc/Run3Summer23MiniAODv4/QCD_PT-170to300_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/04c52fc4-f62a-4196-bf75-b33f357f4dc2.root",  # 26k
        "/store/mc/Run3Summer23MiniAODv4/QCD_PT-800to1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/01264b19-e6e0-426d-be5d-25b8d587c179.root",  # 20k
        "/store/mc/Run3Summer23MiniAODv4/QCD_PT-1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/MINIAODSIM/130X_mcRun3_2023_realistic_v14-v2/2520000/004dcc2f-2f09-41c1-ab6e-4b85568a8032.root",  # 20k
    ),
    secondaryFileNames=cms.untracked.vstring(),
)

process.options = cms.untracked.PSet(
    IgnoreCompletely=cms.untracked.vstring(),
    Rethrow=cms.untracked.vstring(),
    TryToContinue=cms.untracked.vstring(),
    accelerators=cms.untracked.vstring("*"),
    allowUnscheduled=cms.obsolete.untracked.bool,
    canDeleteEarly=cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules=cms.untracked.bool(True),
    dumpOptions=cms.untracked.bool(False),
    emptyRunLumiMode=cms.obsolete.untracked.string,
    eventSetup=cms.untracked.PSet(
        forceNumberOfConcurrentIOVs=cms.untracked.PSet(allowAnyLabel_=cms.required.untracked.uint32),
        numberOfConcurrentIOVs=cms.untracked.uint32(0),
    ),
    fileMode=cms.untracked.string("FULLMERGE"),
    forceEventSetupCacheClearOnNewRun=cms.untracked.bool(False),
    holdsReferencesToDeleteEarly=cms.untracked.VPSet(),
    makeTriggerResults=cms.obsolete.untracked.bool,
    modulesToCallForTryToContinue=cms.untracked.vstring(),
    modulesToIgnoreForDeleteEarly=cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks=cms.untracked.uint32(0),
    numberOfConcurrentRuns=cms.untracked.uint32(1),
    numberOfStreams=cms.untracked.uint32(0),
    numberOfThreads=cms.untracked.uint32(1),
    printDependencies=cms.untracked.bool(False),
    sizeOfStackForThreadsInKB=cms.optional.untracked.uint32,
    throwIfIllegalParameter=cms.untracked.bool(True),
    wantSummary=cms.untracked.bool(False),
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation=cms.untracked.string("MC_allPF_2023_preBPix nevts:100"),
    name=cms.untracked.string("Applications"),
    version=cms.untracked.string("$Revision: 1.19 $"),
)

# Output definition

process.NANOAODSIMoutput = cms.OutputModule(
    "NanoAODOutputModule",
    compressionAlgorithm=cms.untracked.string("LZMA"),
    compressionLevel=cms.untracked.int32(9),
    dataset=cms.untracked.PSet(
        dataTier=cms.untracked.string("NANOAODSIM"), filterName=cms.untracked.string("")
    ),
    fileName=cms.untracked.string("MC_allPF_2023_preBPix_NANO.root"),
    # fileName = cms.untracked.string('/eos/user/c/cmunozdi/AnalysisSamples/MC_allPF_2023_preBPix_qcdmuextra_NANO.root'),
    outputCommands=process.NANOAODSIMEventContent.outputCommands,
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag

process.GlobalTag = GlobalTag(process.GlobalTag, "auto:phase1_2023_realistic", "")

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step, process.endjob_step, process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask

associatePatAlgosToolsTask(process)

# Setup FWK for multithreaded
process.options.numberOfThreads = 4
process.options.numberOfStreams = 0

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.custom_btv_cff
from PhysicsTools.NanoAOD.custom_btv_cff import BTVCustomNanoAOD_allPF

# call to customisation function BTVCustomNanoAOD_allPF imported from PhysicsTools.NanoAOD.custom_btv_cff
process = BTVCustomNanoAOD_allPF(process)

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeCommon

# call to customisation function nanoAOD_customizeCommon imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeCommon(process)

# End of customisation functions


# Customisation from command line

process.genWeightsTable.keepAllPSWeights = True
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete

process = customiseEarlyDelete(process)
# End adding early deletion
