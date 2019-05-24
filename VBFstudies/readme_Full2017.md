## VBF analysis for 2017 data

- treeBaseDir: /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/

- MC:   Fall2017_nAOD_v1_Full2017v2/MCl1loose2017v2__MCCorr2017__btagPerEvent__l2loose__l2tightOR2017/
- FAKE: Run2017_nAOD_v1_Full2017v2/DATAl1loose2017v2__DATACorr2017__l2loose__fakeW/
- DATA: Run2017_nAOD_v1_Full2017v2/DATAl1loose2017v2__DATACorr2017__l2loose/

## 1. Setup Latinos framework

- Access your lxplus account: ```ssh -Y username@lxplus.cern.ch```
- Login shell: ```bash -l```

#### 1.1. Setup a CMSSW release:

- See installed projects available for platform and build work area
```
scram list CMSSW
export SCRAM_ARCH=slc6_amd64_gcc630
cmsrel CMSSW_9_4_9
```
- setup the runtime variable environment every time you start work in your project area
```
cd CMSSW_9_4_9/src/
cmsenv
```
or ```eval `scramv1 runtime -sh` ```

#### 1.2. Setup github repository:

- Get the latino main code
```
cd $CMSSW_BASE/src/
git clone --branch 13TeV git@github.com:latinos/setup.git LatinosSetup
source LatinosSetup/SetupShapeOnly.sh
```
- Get PlotsConfigurations
```
cd $CMSSW_BASE/src/
git clone git@github.com:latinos/PlotsConfigurations.git
```
- Compile
```
cd $CMSSW_BASE/src/
cmsenv
scram b -j 10
```

## 2. VBF analysis: Plots configuration for mkShapes, mkPlot, mkDatacards

- Common tools for analysis
```
cd Latinos/CMSSW_9_4_9/src/
voms-proxy-init -voms cms -rfc --valid 168:0
cmsenv
cd PlotsConfigurations/Configurations/VBF/Full2017/
```
- Look at samples.py 
```
easyDescription.py   --inputFileSamples=samples.py   --outputFileSamples=my_expanded_samples.py
```

#### 2.1. Produce shapes:

- Do not forget to address the Jobs and edit the 'userConfig.py' to put a directory in your own user area:
```
cd /afs/cern.ch/user/l/lusanche/Latinos/CMSSW_9_4_9/src/LatinoAnalysis/Tools/python/
cp userConfig_TEMPLATE.py userConfig.py
```
 modify baseDir = '/afs/cern.ch/user/l/lusanche/Latinos/CMSSW_9_4_9/src/PlotsConfigurations/Configurations/VBF/Full2017/'
 
- The first step reads the post-processed latino trees and produces histograms for several variables and phase spaces (create a directory 'rootFile' where is 'plots_VBF.root' file)
```
cd -
mkShapesMulti.py --pycfg=configuration.py --doBatch=1 --batchSplit=Samples,Files --batchQueue=workday
```
- The jobs can take a while, thus it is natural to check their status: ```condor_q``` or ```mkBatch.py  -s```

- After all your jobs are finished, and before going to the next step, check the .jid files in the following output directory (TAG is specified in configuration.py):
```
ls -l jobs/mkShapes__TAG/*.jid
```
- If you find .jid files it means that the corresponding jobs failed, check the .err and .out files to understand the reason of the failure.

- If a job takes too long/fails, one can understand [condor](http://batchdocs.web.cern.ch/batchdocs/local/quick.html) it and resubmit manually, e.g.:
```
../jobs/mkShapes__TAG/mkShapes__TAG__ALL__DATA.18.sh
```

- Add root files: nce the previous jobs have finished we had the outputs, put all your apples in one basket
```
mkShapesMulti.py --pycfg=configuration.py --doHadd=1  --batchSplit=Samples,Files
```

- If this is too slow try to hadd manually
```
cd rootFileTAG
hadd -j 5 -f plots_TAG.root plots_TAG_ALL_*
```

#### 2.2.  Read histograms

At this stage one can either produce plots or datacards.

- Produce plots: Now we are ready to make data/MC comparison plots.
```
mkPlot.py --pycfg=configuration.py --inputFile=rootFileTAG/plots_TAG.root
```
- Produce datacards
```
mkDatacards.py --pycfg=configuration.py --inputFile=rootFileTAG/plots_TAG.root
```
## 3. To move or copy the plots to the web,
```
mkdir $HOME/www/*/new_directory
pushd $HOME/www/*/new_directory
wget https://raw.githubusercontent.com/latinos/PlotsConfigurations/master/index.php
popd
cp plotVBF/*png $HOME/www/new_directory/
```
Time to check and share the results: `https://username.web.cern.ch/username/*/new_directory/`

## 4. Play with datacards:

- Setup everything that is needed:

  - Install the Higgs Combine Package with [ROOT6 SLC6 release CMSSW74X](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#ROOT6_SLC6_release_CMSSW_7_4_X), necessary to use [SystematicsAnalyzer.py](https://github.com/latinos/PlayWithDatacards/blob/master/systematicsAnalyzer.py) (see line 49).
  
  - Clone some repositories (in CMSSW810):
```
git clone git@github.com:amassiro/PlayWithDatacards.git
git clone git@github.com:amassiro/ModificationDatacards.git
```
  - Enter to [PlayWithDatacards](https://github.com/latinos/PlayWithDatacards) (```cd .../PlayWithDatacards```).
  
  - Activate Combine:
  ```
  cd /afs/cern.ch/user/l/lusanche/Latnos/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit
  cmsenv
  scramv1 b -j 20
  cd -
  ```
- Modify the content for your analysis:
```
cp scripts/prepareTable.py scripts/prepareTable2.py
vim scripts/prepareTable2.py
```
- Create table running (for a set of datacards):
```
python   scripts/prepareTables2.py
python   scripts/prepareTables2.py  |  /bin/sh
```
- Or for a specific datacrd:
```
python   systematicsAnalyzer.py    datacard.txt    --all   -m   125    -f    tex    >     output_datacard.tex
```
to better debug, try to have only 1 signal sample, 1 background sample and data.

From the error (that is a "combine" error) it seems you did not run on data.



- Make combination of datacards and workspaces by editing the script 'scripts/doCombination.sh' and running
```
./doCombination.sh
```


