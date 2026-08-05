# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: MC_allPFVtx_2024 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions auto:phase1_2024_realistic --step NANO --nThreads 4 --era Run3 --filein /store/mc/RunIII2024Summer24MiniAODv6/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/2520000/00045344-a602-4022-ac1e-81161a31a314.root -n 100 --customise pfnano_cff.PFVtxnano_customize --no_exec --customise_commands process.genWeightsTable.keepAllPSWeights=True
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3

process = cms.Process("NANO", Run3)

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
    input=cms.untracked.int32(10000), output=cms.optional.untracked.allowed(cms.int32, cms.PSet)
)

# Input source
process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(
        # "/store/mc/RunIII2024Summer24MiniAODv6/GJ-4Jets-2NLO2LO_Bin-PTG-25_Par-BiasedPTG_TuneSherpaDef_13p6TeV_sherpaMEPS/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/110000/395bf78b-1661-430c-89f0-6ca7555e4d63.root",
        # "/store/mc/RunIII2024Summer24MiniAODv6/GJ-4Jets-2NLO2LO_Bin-PTG-25_Par-BiasedPTG_TuneSherpaDef_13p6TeV_sherpaMEPS/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/110000/00627772-8db6-4d13-88c9-8ae54ccdf848.root",
        # "/store/mc/RunIII2024Summer24MiniAODv6/GJ-4Jets-2NLO2LO_Bin-PTG-25_Par-BiasedPTG_TuneSherpaDef_13p6TeV_sherpaMEPS/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/110000/009b4e2c-54d7-47f1-8e14-dde5f5301917.root",
        # "/store/mc/RunIII2024Summer24MiniAODv6/GJ-4Jets-2NLO2LO_Bin-PTG-25_Par-BiasedPTG_TuneSherpaDef_13p6TeV_sherpaMEPS/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/110000/009fcceb-77da-472e-b1c1-7693bfad9eba.root",
        # "/store/mc/RunIII2024Summer24MiniAODv6/GJ-4Jets-2NLO2LO_Bin-PTG-25_Par-BiasedPTG_TuneSherpaDef_13p6TeV_sherpaMEPS/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/110000/00daa524-20f7-45d8-9af1-68f4b48f9e68.root",
        # "/store/mc/RunIII2024Summer24MiniAODv6/GJ-4Jets-2NLO2LO_Bin-PTG-25_Par-BiasedPTG_TuneSherpaDef_13p6TeV_sherpaMEPS/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/110000/00ee9883-c5a8-44a2-a8ce-d77a3a8bec20.root",
        # "/store/mc/RunIII2024Summer24MiniAODv6/GJ-4Jets-2NLO2LO_Bin-PTG-25_Par-BiasedPTG_TuneSherpaDef_13p6TeV_sherpaMEPS/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/110000/00fec023-00b9-43f9-ba72-d26dbbe3a0f2.root",
        # "/store/mc/RunIII2024Summer24MiniAODv6/GJ-4Jets-2NLO2LO_Bin-PTG-25_Par-BiasedPTG_TuneSherpaDef_13p6TeV_sherpaMEPS/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/110000/01358600-cfed-4213-9d0e-2c0d4d597d35.root",
        # "/store/mc/RunIII2024Summer24MiniAODv6/GJ-4Jets-2NLO2LO_Bin-PTG-25_Par-BiasedPTG_TuneSherpaDef_13p6TeV_sherpaMEPS/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/110000/01a5cd56-eb16-4f6c-91d9-26bedfeb195a.root",
        # "/store/mc/RunIII2024Summer24MiniAODv6/GJ-4Jets-2NLO2LO_Bin-PTG-25_Par-BiasedPTG_TuneSherpaDef_13p6TeV_sherpaMEPS/MINIAODSIM/150X_mcRun3_2024_realistic_v2-v2/110000/01a74a45-aa9e-4144-a718-741b55d7da76.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_10.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_20.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_30.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_40.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_50.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_60.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_70.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_80.root",
        "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_90.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_11.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_21.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_31.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_41.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_51.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_61.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_71.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_81.root",
        # "file:/eos/cms/store/group/phys_higgs/vbfhiggs/DarkPhoton/darkphoton-ggF/RunIII2024Summer24MiniAODv6/20260715_093320_RunIII2024Summer24MiniAODv6_91.root",
        # "file:rootfiles/darkphoton_mini.root",
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
    annotation=cms.untracked.string("MC_allPFVtx_2024 nevts:100"),
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
    # fileName=cms.untracked.string("MC_allPFVtx_2024_NANO.root"),
    # fileName=cms.untracked.string("rootfiles/gjet/MC_allPFVtx_2024_NANO_gjet_395bf78b-1661-430c-89f0-6ca7555e4d63.root"),
    # fileName=cms.untracked.string("rootfiles/gjet/MC_allPFVtx_2024_NANO_gjet_00627772-8db6-4d13-88c9-8ae54ccdf848.root"),
    # fileName=cms.untracked.string("rootfiles/gjet/MC_allPFVtx_2024_NANO_gjet_009b4e2c-54d7-47f1-8e14-dde5f5301917.root"),
    # fileName=cms.untracked.string("rootfiles/gjet/MC_allPFVtx_2024_NANO_gjet_009fcceb-77da-472e-b1c1-7693bfad9eba.root"),
    # fileName=cms.untracked.string("rootfiles/gjet/MC_allPFVtx_2024_NANO_gjet_00daa524-20f7-45d8-9af1-68f4b48f9e68.root"),
    # fileName=cms.untracked.string("rootfiles/gjet/MC_allPFVtx_2024_NANO_gjet_00ee9883-c5a8-44a2-a8ce-d77a3a8bec20.root"),
    # fileName=cms.untracked.string("rootfiles/gjet/MC_allPFVtx_2024_NANO_gjet_00fec023-00b9-43f9-ba72-d26dbbe3a0f2.root"),
    # fileName=cms.untracked.string("rootfiles/gjet/MC_allPFVtx_2024_NANO_gjet_01358600-cfed-4213-9d0e-2c0d4d597d35.root"),
    # fileName=cms.untracked.string("rootfiles/gjet/MC_allPFVtx_2024_NANO_gjet_01a5cd56-eb16-4f6c-91d9-26bedfeb195a.root"),
    # fileName=cms.untracked.string("rootfiles/gjet/MC_allPFVtx_2024_NANO_gjet_01a74a45-aa9e-4144-a718-741b55d7da76.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_10.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_20.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_30.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_40.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_50.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_60.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_70.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_80.root"),
    fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_90.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_11.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_21.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_31.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_41.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_51.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_61.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_71.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_81.root"),
    # fileName=cms.untracked.string("rootfiles/darkphoton/MC_allPFVtx_2024_NANO_dark_91.root"),
    # fileName=cms.untracked.string("MC_allPFVtx_2024_NANO_darkphoton.root"),
    outputCommands=process.NANOAODSIMEventContent.outputCommands,
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag

process.GlobalTag = GlobalTag(process.GlobalTag, "auto:phase1_2024_realistic", "")

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

# Automatic addition of the customisation function from pfnano_cff
from pfnano_cff import PFVtxnano_customize

# call to customisation function PFVtxnano_customize imported from pfnano_cff
process = PFVtxnano_customize(process)

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeCommon

# call to customisation function nanoAOD_customizeCommon imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeCommon(process)

# Add complete stable generator particles and extend the standard MC tables
from addPFCands_cff import addGenStable

process = addGenStable(process)

# End of customisation functions


# Customisation from command line

process.genWeightsTable.keepAllPSWeights = True
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete

process = customiseEarlyDelete(process)
# End adding early deletion
