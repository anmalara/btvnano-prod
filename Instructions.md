# Instructions for Hinv samples

More general info can be found in the ReadME file.
This information overrules the instructions in the ReadME file.

## Recipe

Use the EL8 environment and the production architecture for `CMSSW_15_0_2`.
Merge the official 15_0_X backport from `cms-sw/cmssw#47686`.

```bash
cmsrel CMSSW_15_0_2
cd CMSSW_15_0_2/src
cmsenv
git cms-init
git cms-merge-topic mseidel42:btvNano_150X_backport
git clone git@github.com:anmalara/btvnano-prod.git -b NanoAODv15_Summer2024
scram b -j 10
cd btvnano-prod
source setup.sh
```

Remember to source the `setup.sh` file at each login.

```bash
cd CMSSW_15_0_2/src/btvnano-prod
source setup.sh
```

## TODO

The b-tagging and pT-regression variables are slightly different from central NanoAOD, although the differences are small. Investigate their origin and confirm that they are acceptable.
