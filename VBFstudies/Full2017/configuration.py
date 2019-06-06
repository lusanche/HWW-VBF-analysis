# example of configuration file
treeName = 'Events'
 
# ===== sub categories
tag = 'DYemb'
#tag = 'lowmjj_detajj'
#tag = 'lowmjj_nodetajj'
#tag = 'highmjj_detajj'
#tag = 'highmjj_nodetajj'

# used by mkShape to define output directory for root files
outputDir = 'rootFile_'+tag

# file with TTree aliases and list of variables/cuts/samples/plots
aliasesFile = 'aliases.py'
variablesFile = 'variables.py'
cutsFile = 'cuts.py'
#samplesFile = 'samples.py'
samplesFile = 'samples_embed.py'
plotFile = 'plot.py' 

# luminosity to normalize to (in 1/fb)
lumi = 41.5

# used by mkPlot/mkDatacards to define output directory for plots/datacards
# different from "outputDir" to do things more tidy
outputDirPlots = 'plot_'+tag
outputDirDatacard = 'datacards_'+tag

# structure file for datacard
structureFile = 'structure.py'

# nuisances file for mkDatacards/mkShape
#nuisancesFile = 'nuisances.py'
nuisancesFile = 'nuisances_embed.py'
