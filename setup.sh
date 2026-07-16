#!/bin/bash

source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsenv
source /cvmfs/cms.cern.ch/common/crab-setup.sh prod
voms-proxy-init -rfc -voms cms -valid 192:00

export BTVNANO_PATH=$(pwd -L)
export PYTHONPATH=${BTVNANO_PATH}:${PYTHONPATH}
