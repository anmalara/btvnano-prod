import FWCore.ParameterSet.Config as cms  # type: ignore
from PhysicsTools.NanoAOD.common_cff import CandVars, Var  # type: ignore


def defaultPFCandidateCut():
    cut = "     ( (fromPV()   <=  3 ) || ( pt > 0.1  ) )"
    cut += " && ( (fromPV()   >=  2 ) || ( pt > 3.0  ) )"
    cut += " && ( (abs(pdgId) != 22 ) || ( pt > 0.8  ) )"  # pt cut on photons
    cut += " && ( (abs(pdgId) != 130) || ( pt > 2.0  ) )"  # pt cut on neutral hadrons
    cut += " && ( (abs(pdgId) != 1  ) || ( pt > 2.5  ) )"  # pt cut on HF hadronic
    cut += " && ( (abs(pdgId) != 2  ) || ( pt > 2.5  ) )"  # pt cut on HF EM
    cut += " && ( (abs(pdgId) != 211) || ( pt*puppiWeight > 0.01 ) )"  # pt cut on charged hadrons
    return cut


def addPFCands(process, cut=None, maxLen=None, storeVertexInfo=False):
    if cut is None:
        cut = ""
    if maxLen is not None and maxLen < 0:
        raise ValueError("maxLen must be non-negative or None")

    producerOptions = {}
    if maxLen is not None:
        producerOptions["maxLen"] = cms.uint32(maxLen)

    candidateVariables = cms.PSet(
        CandVars,
        puppiWeight=Var("puppiWeight()", float, doc="Puppi weight", precision=10),
        puppiWeightNoLep=Var("puppiWeightNoLep()", float, doc="puppiWeightNoLep", precision=10),
        vtxChi2=Var("?hasTrackDetails()?vertexChi2():-1", float, doc="vertex chi2", precision=10),
        trkChi2=Var(
            "?hasTrackDetails()?pseudoTrack().normalizedChi2():-1",
            float,
            doc="normalized trk chi2",
            precision=10,
        ),
        dz=Var("?hasTrackDetails()?dz():-1", float, doc="PF dz", precision=10),
        dzErr=Var("?hasTrackDetails()?dzError():-1", float, doc="PF dz error", precision=10),
        d0=Var("?hasTrackDetails()?dxy():-1", float, doc="PF d0", precision=10),
        d0Err=Var("?hasTrackDetails()?dxyError():-1", float, doc="PF d0 error", precision=10),
        pvAssocQuality=Var(
            "pvAssociationQuality()",
            int,
            doc="primary vertex association quality. 0: NotReconstructedPrimary, 1: OtherDeltaZ, 4: CompatibilityBTag, 5: CompatibilityDz, 6: UsedInFitLoose, 7: UsedInFitTight",
        ),
        lostInnerHits=Var(
            "lostInnerHits()",
            int,
            doc="lost inner hits. -1: validHitInFirstPixelBarrelLayer, 0: noLostInnerHits, 1: oneLostInnerHit, 2: moreLostInnerHits",
        ),
        lostOuterHits=Var(
            "?hasTrackDetails()?pseudoTrack().hitPattern().numberOfLostHits('MISSING_OUTER_HITS'):0",
            int,
            doc="lost outer hits",
        ),
        numberOfHits=Var("numberOfHits()", int, doc="number of hits"),
        numberOfPixelHits=Var("numberOfPixelHits()", int, doc="number of pixel hits"),
        trkQuality=Var("?hasTrackDetails()?pseudoTrack().qualityMask():0", int, doc="track quality mask"),
        trkHighPurity=Var(
            "?hasTrackDetails()?pseudoTrack().quality('highPurity'):0", bool, doc="track is high purity"
        ),
        trkAlgo=Var("?hasTrackDetails()?pseudoTrack().algo():-1", int, doc="track algorithm"),
        trkP=Var("?hasTrackDetails()?pseudoTrack().p():-1", float, doc="track momentum", precision=-1),
        trkPt=Var("?hasTrackDetails()?pseudoTrack().pt():-1", float, doc="track pt", precision=-1),
        trkEta=Var("?hasTrackDetails()?pseudoTrack().eta():-1", float, doc="track eta", precision=12),
        trkPhi=Var("?hasTrackDetails()?pseudoTrack().phi():-1", float, doc="track phi", precision=12),
        energy=Var("energy", float, precision=10, doc="PF candidate energy"),
        Vtx_x=Var("vertex().x()", float, precision=10, doc="vertex x position"),
        Vtx_y=Var("vertex().y()", float, precision=10, doc="vertex y position"),
        Vtx_z=Var("vertex().z()", float, precision=10, doc="vertex z position"),
        caloFrac=Var("caloFraction()", float, precision=10, doc="calorimeter energy fraction"),
        hcalFrac=Var("hcalFraction()", float, precision=10, doc="HCAL energy fraction"),
        dzAssociatedPV=Var("dzAssociatedPV()", float, precision=10, doc="dz with respect to the PV"),
        isIsoChHad=Var("isIsolatedChargedHadron()", int, doc="is an isolated charged hadron"),
        fromPV=Var("fromPV()", int, doc="primary vertex association"),
        vtxIdx=Var(
            "?vertexRef().isNonnull()?vertexRef().key():-1",
            int,
            doc="index of the associated vertex in offlineSlimmedPrimaryVertices",
        ),
    )

    process.customConstituentsExtTable = cms.EDProducer(
        "SimplePATCandidateFlatTableProducer",
        src=cms.InputTag("packedPFCandidates"),
        cut=cms.string(cut),
        name=cms.string("PFCands"),
        doc=cms.string("ParticleFlow candidates"),
        singleton=cms.bool(False),  # the number of entries is variable
        extension=cms.bool(False),  # this is the extension table for the AK8 constituents
        variables=candidateVariables,
        **producerOptions,
    )

    process.customizedPFCandsTask = cms.Task(process.customConstituentsExtTable)
    if storeVertexInfo:
        process.pfCandVertexTable = cms.EDProducer(
            "SimpleVertexFlatTableProducer",
            src=cms.InputTag("offlineSlimmedPrimaryVertices"),
            cut=cms.string(""),
            name=cms.string("PFCandVtx"),
            doc=cms.string("reconstructed primary vertices associated with PF candidates"),
            singleton=cms.bool(False),
            extension=cms.bool(False),
            variables=cms.PSet(
                x=Var("position().x()", float, doc="vertex x position, in cm", precision=10),
                y=Var("position().y()", float, doc="vertex y position, in cm", precision=10),
                z=Var("position().z()", float, doc="vertex z position, in cm", precision=16),
                xErr=Var("xError()", float, doc="vertex x uncertainty, in cm", precision=10),
                yErr=Var("yError()", float, doc="vertex y uncertainty, in cm", precision=10),
                zErr=Var("zError()", float, doc="vertex z uncertainty, in cm", precision=10),
                ndof=Var("ndof()", float, doc="number of degrees of freedom", precision=8),
                chi2=Var("normalizedChi2()", float, doc="normalized chi2", precision=8),
                ntracks=Var("tracksSize()", int, doc="number of associated tracks"),
                isFake=Var("isFake()", bool, doc="vertex is fake"),
            ),
        )
        process.customizedPFCandsTask.add(process.pfCandVertexTable)
    process.schedule.associate(process.customizedPFCandsTask)
    return process


def addGenStable(process):
    """Add complete packed generator particles and extend existing MC tables."""

    statusFlags = (
        "statusFlags().isLastCopyBeforeFSR()                  * 16384 +"
        "statusFlags().isLastCopy()                           * 8192  +"
        "statusFlags().isFirstCopy()                          * 4096  +"
        "statusFlags().fromHardProcessBeforeFSR()             * 2048  +"
        "statusFlags().isDirectHardProcessTauDecayProduct()   * 1024  +"
        "statusFlags().isHardProcessTauDecayProduct()         * 512   +"
        "statusFlags().fromHardProcess()                      * 256   +"
        "statusFlags().isHardProcess()                        * 128   +"
        "statusFlags().isDirectHadronDecayProduct()           * 64    +"
        "statusFlags().isDirectPromptTauDecayProduct()        * 32    +"
        "statusFlags().isDirectTauDecayProduct()              * 16    +"
        "statusFlags().isPromptTauDecayProduct()              * 8     +"
        "statusFlags().isTauDecayProduct()                    * 4     +"
        "statusFlags().isDecayedLeptonHadron()                * 2     +"
        "statusFlags().isPrompt()                             * 1"
    )

    process.genStableTable = cms.EDProducer(
        "SimplePATGenParticleFlatTableProducer",
        src=cms.InputTag("packedGenParticles"),
        cut=cms.string(""),
        name=cms.string("GenStable"),
        doc=cms.string("complete packedGenParticles collection, without selection"),
        singleton=cms.bool(False),
        extension=cms.bool(False),
        variables=cms.PSet(
            pt=Var("pt", float, precision=10),
            eta=Var("eta", float, precision=10),
            phi=Var("phi", float, precision=10),
            mass=Var("mass", float, precision=10),
            energy=Var("energy", float, precision=10),
            px=Var("px", float, precision=10),
            py=Var("py", float, precision=10),
            pdgId=Var("pdgId", int, doc="PDG id"),
            charge=Var("charge", int, doc="electric charge"),
            status=Var("status", int, doc="particle status; packed particles have status 1"),
            statusFlags=Var(statusFlags, "uint16", doc="generator status flags stored bitwise"),
            motherPrunedIdx=Var(
                "?numberOfMothers>0?motherRef().key():-1",
                "int",
                doc="index of the mother in prunedGenParticles",
            ),
        ),
    )

    process.genStableTask = cms.Task(process.genStableTable)
    process.schedule.associate(process.genStableTask)
    return process


def addEventFilter(process):
    """Add the NanoFilter after the common NanoAOD tables."""
    process.nanoFilter = cms.EDFilter(
        "NanoFilter",
        jets=cms.InputTag("linkedObjects", "jets"),
        met=cms.InputTag("slimmedMETs"),
        electrons=cms.InputTag("linkedObjects", "electrons"),
        muons=cms.InputTag("linkedObjects", "muons"),
        photons=cms.InputTag("linkedObjects", "photons"),
        metPtMin=cms.double(100.0),
        nJetMin=cms.uint32(2),
        jetPtMin=cms.double(20.0),
        electronPtMin=cms.double(20.0),
        muonPtMin=cms.double(20.0),
        photonPtMin=cms.double(150.0),
    )

    is_mc = hasattr(process, "NANOAODSIMoutput")
    sequence = process.nanoSequenceMC if is_mc else process.nanoSequence
    sequence.insert(sequence.index(process.nanoSequenceCommon) + 1, process.nanoFilter)
    return process
