
# DNN analysis
Using NN and Deep Learning to optimize the VBF selection

## 1. Gardener

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

## 2. Shape analysis with DNN (batch queue mode for mkShape)
after obtaining a data card  in [VBF analysis]{https://github.com/lusanche/HWWanalysis/tree/master/VBFstudies#2-vbf-analysis-plots-configuration-for-mkshapes-mkplot-mkdatacards}

### 2.1. 

### 2.2. 
