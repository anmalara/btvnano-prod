from addPFCands_cff import addEventFilter, addPFCands, defaultPFCandidateCut
from PhysicsTools.NanoAOD.common_cff import Var  # type: ignore
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_addDeepInfoAK4_switch  # type: ignore
from Configuration.Eras.Modifier_run3_nanoAOD_pre142X_cff import run3_nanoAOD_pre142X  # type: ignore


def PFnano_customize(process):
    process = addPFCands(process, cut=defaultPFCandidateCut(), maxLen=500)
    run3_nanoAOD_pre142X.toModify(nanoAOD_addDeepInfoAK4_switch, nanoAOD_addRobustParTAK4Tag_switch=True)
    run3_nanoAOD_pre142X.toModify(
        process.jetPuppiTable.variables,
        btagRobustParTAK4B=Var(
            "?(pt>=15)?bDiscriminator('pfParticleTransformerAK4JetTags:probb')+"
            "bDiscriminator('pfParticleTransformerAK4JetTags:probbb')+"
            "bDiscriminator('pfParticleTransformerAK4JetTags:problepb'):-1",
            float,
            doc="RobustParTAK4 b+bb+lepb tag discriminator",
            precision=10,
        ),
    )
    return addEventFilter(process)


def PFVtxnano_customize(process):
    return addPFCands(process, cut="", maxLen=None, storeVertexInfo=True)
