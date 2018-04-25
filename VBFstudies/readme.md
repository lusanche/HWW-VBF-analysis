### Some useful links:

* Twiki Latinos:  [Analysis 13TeV](https://twiki.cern.ch/twiki/bin/view/CMS/LatinosAnalyses13TeV) ,  [Framework for 2017](https://twiki.cern.ch/twiki/bin/view/CMS/LatinosFrameworkFor2017)  and  [Tutorials](https://twiki.cern.ch/twiki/bin/view/CMS/LatinosFrameworkTutorials)

* To join Latinos: https://github.com/orgs/latinos/invitation?via_email=1

* Twiki page for VBF analysis: https://twiki.cern.ch/twiki/bin/view/CMS/LatinosVBF2016

* Access to the github repository Latinos: https://github.com/latinos

* [EOS](https://github.com/piedraj/AnalysisCMS#9-eos)

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
look at files and modify them according to the interest. 
```
easyDescription.py   --inputFileSamples=samples.py   --outputFileSamples=my_expanded_samples.py
```

#### 2.1. Produce histograms:

- The first step reads the post-processed latino trees and produces histograms for several variables and phase spaces (create a directory 'rootFile' where is 'plots_VBF.root' file)
```
mkShapes.py     --pycfg=configuration.py  \
                --inputDir=/eos/cms/store/group/phys_higgs/cmshww/amassiro/Full2016_Apr17/Apr2017_summer16/lepSel__MCWeights__bSFLpTEffMulti__cleanTauMC__l2loose__hadd__l2tightOR__formulasMC__wwSel  \
                --batchSplit=AsMuchAsPossible            --doBatch=True            --batchQueue=2nd
```
- The jobs can take a while, thus it is natural to check their status: ```mkBatch.py         -s```

- After all your jobs are finished, and before going to the next step, check the .jid files in the following output directory (tag is specified in configuration.py):
```
ls -l jobs/mkShapes__VBF/*.jid
```
- If you find .jid files it means that the corresponding jobs failed, check the .err and .out files to understand the reason of the failure.

- If a job takes too long/fails, one can [kill](https://twiki.cern.ch/twiki/bin/view/Main/BatchJobs#JobKill) it and resubmit manually, e.g.:
```
bsub -q 2nd jobs/mkShapes__VBF/mkShapes__VBF__hww2l2v_13TeV_of2j_vbf__Vg.sh
bsub -q 2nd jobs/mkShapes__VBF/mkShapes__VBF__hww2l2v_13TeV_of2j_vbf__Fake9.sh
```
- If several jobs failed and you want to resubmit them all at once you can do:
```
cd jobs/mkShapes__VBF
for i in *jid; do bsub -q 2nd ${i/jid/sh}; done
```

- Once the previous jobs have finished we hadd the outputs, put all your apples in one basket
```
mkShapes.py      --pycfg=configuration.py   \
                 --inputDir=/eos/cms/store/group/phys_higgs/cmshww/amassiro/Full2016_Apr17/Apr2017_summer16/lepSel__MCWeights__bSFLpTEffMulti__cleanTauMC__l2loose__hadd__l2tightOR__formulasMC__wwSel   \
                 --batchSplit=AsMuchAsPossible             --doHadd=True
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

- https://github.com/latinos/PlayWithDatacards
- [CMSSW74X](https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#ROOT6_SLC6_release_CMSSW_7_4_X)
- Transform datacard in to table
```
./tableFromCards.py  hww-12.9.mH125_of2jvbf_dnn.txt
```
https://github.com/latinos/PlayWithDatacards/blob/master/systematicsAnalyzer.py
```
python   scripts/prepareTables2.py
python   scripts/prepareTables2.py  |  /bin/sh
python   systematicsAnalyzer.py    datacard.txt    --all   -m   125    -f    tex    >     output_datacard.tex
```
you need to install the Higgs combine package (ROOT6 SLC6 release CMSSW_7_4_X)

https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit

to better debug, try to have only 1 signal sample, 1 background sample and data.

From the error (that is a "combine" error) it seems you did not run on data.

Get the combine package. Follow the instructions documented in the revision r170 of the combine twiki.
```
cd $COMBINE_DIRECTORY
```
Get Andrea's scripts to modify datacards.
```
cd $COMBINE_DIRECTORY
git clone https://github.com/amassiro/ModificationDatacards
```
Copy and edit the latino user configuration file.
```
cd $CMSSW_DIRECTORY/LatinoAnalysis/Tools/python
cp userConfig_TEMPLATE.py userConfig.py
```
