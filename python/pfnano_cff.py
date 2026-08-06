from addPFCands_cff import addEventFilter, addPFCands, defaultPFCandidateCut


def PFnano_customize(process):
    process = addPFCands(process, cut=defaultPFCandidateCut(), maxLen=500)
    return addEventFilter(process)


def PFVtxnano_customize(process):
    return addPFCands(process, cut="", maxLen=None, storeVertexInfo=True)
