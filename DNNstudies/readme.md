
# DNN analysis
Using NN and Deep Learning to optimize the VBF selection

## 1. Gardener module

Common tools to modify tree variables, add new variables, add weights, ...

### 1.0. Build a compatible area and setup github repository:
```
export SCRAM_ARCH=slc6_amd64_gcc630
cmsrel CMSSW_9_4_6_patch1
cd CMSSW_9_4_6_patch1/src/
cmsenv
git clone git@github.com:latinos/LatinoAnalysis.git
scram b
```
### 1.1. First copy an existing module :
```
cd LatinoAnalysis/Gardener/python/variables
cp anyVariable.py newVariable.py
```
### 1.2. Import the new module in [gardener.py](https://github.com/latinos/LatinoAnalysis/blob/master/Gardener/scripts/gardener.py) :
```ruby
from LatinoAnalysis.Gardener.variables.VBF_DNNvar      import DNNvarFiller
```
### 1.3. Add it to the list of nuisnaces in gardener.py :
```ruby
modules['vbfdnnvarFiller'] = DNNvarFiller()
```
### 1.4. Document how-to use it :
```
cd ../../scripts/
./gardener.py vbfdnnvarFiller \
/eos/cms/store/group/phys_higgs/cmshww/amassiro/Full2016_Apr17/Apr2017_summer16/lepSel__MCWeights__bSFLpTEffMulti__cleanTauMC__l2loose__hadd__l2tightOR__LepTrgFix__formulasMC__wwSel/latino_VBFHToWWTo2L2Nu_M125.root \
/eos/user/l/lusanche/Full2016/VBF_DNNvar/latino_VBFHToWWTo2L2Nu_M125_DNN.root
```

## 2. [Shape analysis](https://cms-hcomb.gitbooks.io/combine/content/part2/settinguptheanalysis.html#shape-analysis) with DNN (batch queue mode for mkShape)
after obtaining a data card  in [VBF analysis](https://github.com/lusanche/HWWanalysis/tree/master/VBFstudies#2-vbf-analysis-plots-configuration-for-mkshapes-mkplot-mkdatacards), prepare to use [combine](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HATSatLPC2014StatisticsTools)

### 2.1. Setting up the environment (once)
```
export SCRAM_ARCH=slc6_amd64_gcc530
cmsrel CMSSW_8_1_0
cd CMSSW_8_1_0/src 
cmsenv
```
### 2.2. Standalone compilation in lxplus
```
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
source env_standalone.sh
make -j 8; make # second make fixes compilation error of first
```
### 2.3. Update to a reccomended tag - currently the reccomended tag is v7.0.8
```
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v7.0.8
scramv1 b clean; scramv1 b # always make a clean build
```
### 2.4. Expected/Observed significance

### 2.5. Lumiscale
```
combine -M Significance -t -1 --expectSignal=1 --setParameters lumiscale=2.78551 --freezeParameters lumiscale test_lumiscale/datacards_15Sep_SRvbf_combine2/hww2l2v_13TeV_of2j_vbf/DNNvar/datacard.txt
```
