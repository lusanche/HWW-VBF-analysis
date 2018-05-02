## Gardener

Common tools to modify tree variables, add new variables, add weights, ...

### 0. Build a compatible area and setup github repository:
```
export SCRAM_ARCH=slc6_amd64_gcc630
cmsrel CMSSW_9_4_6_patch1
cd CMSSW_9_4_6_patch1/src/
cmsenv
git clone git@github.com:latinos/LatinoAnalysis.git
scram b
```
### 1. First copy an existing module :
```
cd LatinoAnalysis/Gardener/python/variables
cp anyVariable.py newVariable.py
```
### 2. Import the new module in gardener.py :
* https://github.com/latinos/LatinoAnalysis/blob/master/Gardener/scripts/gardener.py
```diff
+ from LatinoAnalysis.Gardener.variables.newVariable      import NewVariableFiller
```
### 3. Add it to the list of nuisnaces in gardener.py :
```diff
+ modules['newvariableFiller']=NewVariableFiller()
```
### 4. Document how-to use it in Gardener/test/README.md :
```
cd ../../scripts/
gardener.py  newVariableFiller  input.root  output.root
```
