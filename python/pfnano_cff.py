from addPFCands_cff import addPFCands, defaultPFCandidateCut


def PFnano_customize(process):
    return addPFCands(process, cut=defaultPFCandidateCut(), maxLen=500)


def PFVtxnano_customize(process):
    return addPFCands(process, cut="", maxLen=None, storeVertexInfo=True)
