## Configuration for 2017 data

- treeBaseDir: /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/

- MC:   Fall2017_nAOD_v1_Full2017v2/MCl1loose2017v2__MCCorr2017__btagPerEvent__l2loose__l2tightOR2017/
- FAKE: Run2017_nAOD_v1_Full2017v2/DATAl1loose2017v2__DATACorr2017__l2loose__fakeW/
- DATA: Run2017_nAOD_v1_Full2017v2/DATAl1loose2017v2__DATACorr2017__l2loose/

## 1. Setup Latinos framework

- Access your lxplus account: ```ssh -Y username@lxplus.cern.ch```
- Login shell: ```bash -l```

#### 1.1. Build the work area:
- See installed projects available for platform and build work area
```
scram list CMSSW
export SCRAM_ARCH=slc6_amd64_gcc530
cmsrel CMSSW_8_0_26_patch1
```
- setup the runtime variable environment every time you start work in your project area
```
cd CMSSW_8_0_26_patch1/src/
cmsenv
```
or ```eval `scramv1 runtime -sh` ```

#### 1.2. Setup github repository:

- Generate an [SSH key](https://help.github.com/articles/connecting-to-github-with-ssh/) and then initialize git locally
```
git cms-init
```
- Clone the 'setup' repository of latinos github
```
git clone --branch 13TeV git@github.com:latinos/setup.git LatinosSetup
```
- Setup 'Setup.sh' by sourcing (or ```bash```)
```
source LatinosSetup/Setup.sh
```

## 2. VBF analysis: Plots configuration for mkShapes, mkPlot, mkDatacards
```
cd LatinoAnalysis/ShapeAnalysis/
git clone git@github.com:latinos/PlotsConfigurations.git
cmsenv
```
Compile ```scramv1 b -j8```
```
cd PlotsConfigurations/Configurations/VBF/
```
look at samples.py 
```
easyDescription.py   --inputFileSamples=samples.py   --outputFileSamples=my_expanded_samples.py
```

#### 2.1. Produce histograms:

- Do not forget to address the jobs and edit the 'userConfig.py' to put a directory in your own user area:

/afs/cern.ch/user/l/lusanche/Latinos/CMSSW_8_X_Y/src/LatinoAnalysis/ShapeAnalysis/PlotsConfigurations/Configurations/VBF/
```
cd LatinoAnalysis/Tools/python/
cp userConfig_TEMPLATE.py userConfig.py
```
- The first step reads the post-processed latino trees and produces histograms for several variables and phase spaces (create a directory 'rootFile' where is 'plots_VBF.root' file)
```
mkShapes.py     --pycfg=configuration.py \
                --inputDir=/eos/cms/store/caf/user/lenzip/Apr2017_summer16/lepSel__MCWeights__bSFLpTEffMulti__cleanTauMC__l2loose__hadd__l2tightOR__LepTrgFix__dorochester__formulasMC__wwSel__doDNN/  \
                --batchSplit=AsMuchAsPossible \
                --doBatch=True \
                --batchQueue=2nd
```
- The jobs can take a while, thus it is natural to check their status: ```mkBatch.py         -s```

- After all your jobs are finished, and before going to the next step, check the .jid files in the following output directory (tag is specified in configuration.py):
```
ls -l jobs/mkShapes__VBF/*.jid
```
- If you find .jid files it means that the corresponding jobs failed, check the .err and .out files to understand the reason of the failure.

- If a job takes too long/fails, one can [job kill](https://twiki.cern.ch/twiki/bin/view/Main/BatchJobs#JobKill) it and resubmit manually, e.g.:
```
bsub -q 2nd jobs/mkShapes__VBF/mkShapes__VBF__hww2l2v_13TeV_of2j_vbf__Vg.sh
```
- If several jobs failed and you want to resubmit them all at once you can do:
```
cd jobs/mkShapes__VBF
for i in *jid; do bsub -q 2nd ${i/jid/sh}; done
```

- Once the previous jobs have finished we had the outputs, put all your apples in one basket
```
mkShapes.py      --pycfg=configuration.py \
                 --inputDir=/eos/cms/store/caf/user/lenzip/Apr2017_summer16/lepSel__MCWeights__bSFLpTEffMulti__cleanTauMC__l2loose__hadd__l2tightOR__LepTrgFix__dorochester__formulasMC__wwSel__doDNN/ \
                 --batchSplit=AsMuchAsPossible \
                 --doHadd=True
```
NB: If the ```--batchSplit=AsMuchAsPossible``` option is used, do not hadd the outputs by hand but use the command above instead.    Otherwise the MC statistical uncertainties are not treated in the correct way.

#### 2.2.  Read histograms

At this stage one can either produce plots or datacards.

- Produce plots: Now we are ready to make data/MC comparison plots.
```
mkPlot.py              --inputFile=rootFile/plots_VBF.root           --showIntegralLegend=1
```
- Produce datacards
```
mkDatacards.py             --pycfg=configuration.py          --inputFile=rootFile/plots_VBF.root
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
