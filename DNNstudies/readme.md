
# DNN analysis
Using NN and Deep Learning to optimize the VBF selection

## 1 Install Keras on LXPLUS

### 1.1 Get Python 2.7 in your path:
```
cmsrel CMSSW_X_Y_Z
cd CMSSW_X_Y_Z/src
cmsenv
```
### 1.2. Install PIP locally:
```
wget https://bootstrap.pypa.io/get-pip.py 
python get-pip.py --user
```
### 1.3. Install Keras locally:
```
~/.local/bin/pip install --user keras
```
## 2. Shape analysis with DNN

### 2.1. Run the command:
```
cd LatinoAnalysis/Tools/python/
cp userConfig_TEMPLATE.py userConfig.py
```
edit the `userConfig.py` to put a directory in your own user area

### 2.2. To submit the jobs:
```
 mkShapes.py —pycfg=<Config>  —inputDir=<Dir> --doBatch=True --batchSplit=Cuts,Samples
 ```
 ### 2.3. Check you the status of jobs:
```
 mkBatch.py -s
 ```
 
