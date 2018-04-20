#### Some useful links:

* Twiki Latinos: https://twiki.cern.ch/twiki/bin/view/CMS/LatinosAnalyses13TeV

* To join Latinos: https://github.com/orgs/latinos/invitation?via_email=1

* Twiki page for VBF analysis: https://twiki.cern.ch/twiki/bin/view/CMS/LatinosVBF2016

* Access to the github repository Latinos: https://github.com/latinos

### 1. Setup Latinos framework

- Access your lxplus account: ```ssh -Y username@lxplus.cern.ch```
- Login shell: ```bash -l```

#### 1.1 Build the work area:
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

#### 1.2 Setup github repository:

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

Clonning more repos:

$ cd LatinoAnalysis/ShapeAnalysis/

$ git clone git@github.com:latinos/PlotsConfigurations.git %clonnig the repo 'PlotsConfigurations' of latinos github

$ cmsenv

$ scramv1 b                                 %compile (or scramv1 b -j 10)

## VBF analysis:

$ cd PlotsConfigurations/Configurations/VBF/

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
1. First time only 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Get the combine package. Follow the instructions documented in the revision r170 of the combine twiki.

cd $COMBINE_DIRECTORY

Get Andrea's scripts to modify datacards.

cd $COMBINE_DIRECTORY

git clone https://github.com/amassiro/ModificationDatacards

Copy and edit the latino user configuration file.

cd $CMSSW_DIRECTORY/LatinoAnalysis/Tools/python

cp userConfig_TEMPLATE.py userConfig.py

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
look at samples.py

Full2016]$ easyDescription.py   --inputFileSamples=samples.py   --outputFileSamples=my_expanded_samples.py

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
2. Produce histograms
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

This step reads the post-processed latino trees and produces histograms for several variables and phase spaces.

$$$$$$$$$$$$$$$$$$$ cd Full2016/

The first step reads the post-processed latino trees and produces histograms for several variables and phase spaces (create a directory 'rootFile' where is 'plots_VBF.root' file),

$$$$$$$$$$$$$$$$$$$ mkShapes.py             --pycfg=configuration.py             --inputDir=/eos/cms/store/group/phys_higgs/cmshww/amassiro/Full2016_Apr17/Apr2017_summer16/lepSel__MCWeights__bSFLpTEffMulti__cleanTauMC__l2loose__hadd__l2tightOR__formulasMC__wwSel             --batchSplit=AsMuchAsPossible            --doBatch=True            --batchQueue=2nd

The jobs can take a while, thus it is natural to check their status.

$$$$$$$$$$$$$$$$$$$ mkBatch.py         -s

After all your jobs are finished, and before going to the next step, check the .jid files in the following output directory (tag is specified in configuration.py):

$$$$$$$$$$$$$$$$$$$ ls -l jobs/mkShapes__VBF/*.jid
    
If you find .jid files it means that the corresponding jobs failed, check the .err and .out files to understand the reason of the failure.

If a job takes too long / fails, one can kill it and resubmit manually, e.g.:

$$$$$$$$$$$$$$$$$$$ bsub -q 2nd jobs/mkShapes__VBF/mkShapes__VBF__hww2l2v_13TeV_of2j_vbf__Vg.sh

$$$$$$$$$$$$$$$$$$$ bsub -q 2nd jobs/mkShapes__VBF/mkShapes__VBF__hww2l2v_13TeV_of2j_vbf__Fake9.sh

If several jobs failed and you want to resubmit them all at once you can do:

$$$$$$$$$$$$$$$$$$$ cd jobs/mkShapes__VBF

$$$$$$$$$$$$$$$$$$$ for i in *jid; do bsub -q 2nd ${i/jid/sh}; done

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
3. Put all your apples in one basket
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Once the previous jobs have finished we hadd the outputs.

$$$$$$$$$$$$$$$$$$$ mkShapes.py            --pycfg=configuration.py             --inputDir=/eos/cms/store/group/phys_higgs/cmshww/amassiro/Full2016_Apr17/Apr2017_summer16/lepSel__MCWeights__bSFLpTEffMulti__cleanTauMC__l2loose__hadd__l2tightOR__formulasMC__wwSel             --batchSplit=AsMuchAsPossible             --doHadd=True

NB: If the --batchSplit=AsMuchAsPossible option is used, do not hadd the outputs by hand but use the command above instead.
    Otherwise the MC statistical uncertainties are not treated in the correct way.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
4. Read histograms
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

At this stage one can either produce plots or datacards.
Produce plots

Now we are ready to make data/MC comparison plots.

$$$$$$$$$$$$$$$$$$$ mkPlot.py              --inputFile=rootFile/plots_VBF.root           --showIntegralLegend=1

Produce datacards

$$$$$$$$$$$$$$$$$$$ mkDatacards.py             --pycfg=configuration.py          --inputFile=rootFile/plots_VBF.root

To move or copy the plots to the web,

$ mkdir $HOME/www/*/new_directory

$ pushd $HOME/www/*/new_directory

$ wget https://raw.githubusercontent.com/latinos/PlotsConfigurations/master/index.php

$ popd

$ cp plotVBF/*png $HOME/www/new_directory/

Time to check and share the results: https://lusanche.web.cern.ch/lusanche/*/new_directory/
