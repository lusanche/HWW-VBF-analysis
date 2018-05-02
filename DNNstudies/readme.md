
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
## 2. Shape analysis with DNN (batch queue mode for mkShape)

### 2.1. To make the batch interface working:
```
cd LatinoAnalysis/Tools/python/
cp userConfig_TEMPLATE.py userConfig.py
```
edit the `userConfig.py` to put a directory in your own user area

### 2.2. To submit the jobs:
```
 mkShapes.py —pycfg=<Config>  —inputDir=<Dir> --doBatch=True --batchSplit=Cuts,Samples
```
Where the `batchSplit` option is controlling the way you split your jobs by Cuts and Samples, i.e. removing some of them you can by example run all samples in single job per Samples (`#jobs = #Samples`) or all Cuts in single jobs per Samples (`#jobs = #Cuts`) or even removing it fully run everything in a single job.
 
 ### 2.3. Check you the job status disployed:
```
LatinoAnalysis/Tools/scripts/mkBatch.py -s
```
When all the jobs are done, you have to perform an ‘hadd’ by doing:
```
mkShapes.py —pycfg=<Config>  —inputDir=<Dir> --doHadd=True --batchSplit=Cuts,Samples
```
BUT making sure you use the same `—batchSplit=` as in the first command.

BTW, the doHadd step will not work if jobs are not done or if some root files are missing and it will throw you an error.

Similarly the doBatch step will refuse to resubmit jobs unless all are done on the farm.

Then you should be able to do the _mkPlot_ and other mkDatacards command on top of the file resulting from the hadd.

