#!/usr/bin/env python

import os # To disable all logging output from TensorFlow using an environment variable.
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' # a min log level for logging in C++. 2 to additionall filter out WARNING.

#from ROOT import TFile, TTree, TMath
from ROOT import *
from array import array

#For test model
import numpy, math
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers.advanced_activations import LeakyReLU, PReLU
from keras.optimizers import SGD, Adam
from keras.utils import np_utils
from keras.models import model_from_json
from keras.optimizers import SGD, Adam, RMSprop, Adagrad, Adadelta, Adamax, Nadam

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

## input normalization function
def Normalize(a):
  max = numpy.amax(a,axis=0)
  min = numpy.amin(a,axis=0)
  norm = (a-min)/(max-min)
  return norm

#loads the model for vbf vs top
path_jh = '/afs/cern.ch/user/l/lusanche/Latinos'
label = '_5:400_12:10000:1_mjj700b'
smodel = str(path_jh)+'/KERAS/run_dnn/Full2016/using_weights/mjj400_mjj700/model_weight/model'+str(label)+'.json'
sweight = str(path_jh)+'/KERAS/run_dnn/Full2016/using_weights/mjj400_mjj700/model_weight/weights'+str(label)+'.h5'
json_file = open(smodel,'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights(sweight)

#compile the model for vbf vs bkg
opt = Adamax();
loaded_model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['acc'])

path_latrees = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/Full2016_Apr17/Apr2017_summer16'
#path_latrees = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/Full2016_Apr17/Apr2017_Run2016H_RemAOD'

paths=[path_latrees+'/lepSel__MCWeights__bSFLpTEffMulti__cleanTauMC__l2loose__hadd__l2tightOR__LepTrgFix__dorochester__formulasMC__wwSel/']
#paths=[path_latrees+'/lepSel__EpTCorr__TrigMakerData__cleanTauData__l2loose__dorochester__multiFakeW__formulasFAKE__hadd__wwSel/']
#paths=[path_latrees+'/lepSel__EpTCorr__TrigMakerData__cleanTauData__l2loose__hadd__l2tightOR__dorochester__formulasDATA__wwSel/']

files = [    
#             'latino_DYJetsToTT_MuEle_M-50__part0',
#             'latino_DYJetsToTT_MuEle_M-50__part1',
#             'latino_DYJetsToTT_MuEle_M-50_ext1__part0',
#             'latino_DYJetsToTT_MuEle_M-50_ext1__part1',
#             'latino_DYJetsToLL_M-10to50',
              'latino_DYJetsToLL_M-50__part0',
              'latino_DYJetsToLL_M-50__part1',
              'latino_DYJetsToLL_M-50__part2',
              'latino_DYJetsToLL_M-50__part3',
              'latino_DYJetsToLL_M-50__part4',
              'latino_DYJetsToLL_M-50__part5',
              'latino_DYJetsToLL_M-50__part6',
              'latino_DYJetsToLL_M-50__part7',
              'latino_DYJetsToLL_M-50__part8',
              'latino_DYJetsToLL_M-50__part9',
              'latino_DYJetsToLL_M-50__part10',
              'latino_DYJetsToLL_M-50__part11',
              'latino_DYJetsToLL_M-50__part12',
              'latino_DYJetsToLL_M-50__part13',
              'latino_DYJetsToLL_M-50__part14',
              'latino_DYJetsToLL_M-50__part15',
              'latino_DYJetsToLL_M-50__part16',
              'latino_DYJetsToLL_M-50__part17',
              'latino_DYJetsToLL_M-50__part18',
              'latino_DYJetsToLL_M-50__part19',
#             'latino_TTTo2L2Nu__part0',
#             'latino_TTTo2L2Nu__part1',
#             'latino_TTTo2L2Nu__part10',
#             'latino_TTTo2L2Nu__part11',
#             'latino_TTTo2L2Nu__part12',
#             'latino_TTTo2L2Nu__part13',
#             'latino_TTTo2L2Nu__part14',
#             'latino_TTTo2L2Nu__part15',
#             'latino_TTTo2L2Nu__part16',
#             'latino_TTTo2L2Nu__part17',
#             'latino_TTTo2L2Nu__part18',
#             'latino_TTTo2L2Nu__part19',
#             'latino_TTTo2L2Nu__part2',
#             'latino_TTTo2L2Nu__part20',
#             'latino_TTTo2L2Nu__part3',
#             'latino_TTTo2L2Nu__part4',
#             'latino_TTTo2L2Nu__part5',
#             'latino_TTTo2L2Nu__part6',
#             'latino_TTTo2L2Nu__part7',
#             'latino_TTTo2L2Nu__part8',
#             'latino_TTTo2L2Nu__part9',
#             'latino_ST_tW_antitop',
#             'latino_ST_tW_top',
#             'latino_ST_t-channel_antitop',
#             'latino_ST_t-channel_top',
#             'latino_ST_s-channel',
#             'latino_WWTo2L2Nu',
#             'latino_WpWmJJ_EWK_noTop',
#             'latino_GluGluWWTo2L2Nu_MCFM',
#             'latino_Wg_MADGRAPHMLM',
#             'latino_Zg__part0',
#             'latino_Zg__part1',
#             'latino_Zg__part2',
#             'latino_WZTo3LNu_mllmin01_ext1__part0',
#             'latino_WZTo3LNu_mllmin01_ext1__part1',
#             'latino_WZTo3LNu_mllmin01_ext1__part2',
#             'latino_ZZTo2L2Nu__part0',
#             'latino_ZZTo2L2Nu__part1',
#             'latino_ZZTo2L2Nu__part2',
#             'latino_WZTo2L2Q__part0',
#             'latino_WZTo2L2Q__part1',
#             'latino_WZTo2L2Q__part2',
#             'latino_WZTo2L2Q__part3',
#             'latino_ZZTo2L2Q__part0',
#             'latino_ZZTo2L2Q__part1',
#             'latino_ZZTo2L2Q__part2',
#             'latino_ZZZ',
#             'latino_WZZ',
#             'latino_WWZ',
#             'latino_WWW',
#             'latino_GluGluHToWWTo2L2NuPowheg_M125',
#             'latino_VBFHToWWTo2L2Nu_M125',
#             'latino_HZJ_HToWW_M125',
#             'latino_ggZH_HToWW_M125',
#             'latino_HWminusJ_HToWW_M125',
#             'latino_HWplusJ_HToWW_M125',
#             'latino_bbHToWWTo2L2Nu_M125_yb2',
#             'latino_bbHToWWTo2L2Nu_M125_ybyt',
#             'latino_ttHToNonbb_M125',
#             'latino_GluGluHToTauTau_M125',
#             'latino_VBFHToTauTau_M125',
#             'latino_HZJ_HToTauTau_M125',
#             'latino_HWplusJ_HToTauTau_M125',
#             'latino_HWminusJ_HToTauTau_M125',
 # B - fake
#             'latino_MuonEG_Run2016B-03Feb2017_ver2-v2',
#             'latino_DoubleMuon_Run2016B-03Feb2017_ver2-v2__part0',
#             'latino_DoubleMuon_Run2016B-03Feb2017_ver2-v2__part1',
#             'latino_DoubleMuon_Run2016B-03Feb2017_ver2-v2__part2',
#             'latino_SingleMuon_Run2016B-03Feb2017_ver2-v2__part0',
#             'latino_SingleMuon_Run2016B-03Feb2017_ver2-v2__part1',
#             'latino_SingleMuon_Run2016B-03Feb2017_ver2-v2__part2',
#             'latino_DoubleEG_Run2016B-03Feb2017_ver2-v2__part0',
#             'latino_DoubleEG_Run2016B-03Feb2017_ver2-v2__part1',
#             'latino_SingleElectron_Run2016B-03Feb2017_ver2-v2__part0',
#             'latino_SingleElectron_Run2016B-03Feb2017_ver2-v2__part1',
 # C - fake
#             'latino_MuonEG_Run2016C-03Feb2017-v1',
#             'latino_DoubleMuon_Run2016C-03Feb2017-v1__part0',
#             'latino_DoubleMuon_Run2016C-03Feb2017-v1__part1',
#             'latino_SingleMuon_Run2016C-03Feb2017-v1__part0',
#             'latino_SingleMuon_Run2016C-03Feb2017-v1__part1',
#             'latino_DoubleEG_Run2016C-03Feb2017-v1',
#             'latino_SingleElectron_Run2016C-03Feb2017-v1',
 # D - fake
#             'latino_MuonEG_Run2016D-03Feb2017-v1',
#             'latino_DoubleMuon_Run2016D-03Feb2017-v1__part0',
#             'latino_DoubleMuon_Run2016D-03Feb2017-v1__part1',
#             'latino_SingleMuon_Run2016D-03Feb2017-v1__part0',
#             'latino_SingleMuon_Run2016D-03Feb2017-v1__part1',
#             'latino_DoubleEG_Run2016D-03Feb2017-v1',
#             'latino_SingleElectron_Run2016D-03Feb2017-v1',
 # E - fake
#             'latino_MuonEG_Run2016E-03Feb2017-v1',
#             'latino_DoubleMuon_Run2016E-03Feb2017-v1__part0',
#             'latino_DoubleMuon_Run2016E-03Feb2017-v1__part1',
#             'latino_SingleMuon_Run2016E-03Feb2017-v1__part0',
#             'latino_SingleMuon_Run2016E-03Feb2017-v1__part1',
#             'latino_DoubleEG_Run2016E-03Feb2017-v1',
#             'latino_SingleElectron_Run2016E-03Feb2017-v1',
 # F - fake
#             'latino_MuonEG_Run2016F-03Feb2017-v1',
#             'latino_DoubleMuon_Run2016F-03Feb2017-v1__part0',
#             'latino_DoubleMuon_Run2016F-03Feb2017-v1__part1',
#             'latino_SingleMuon_Run2016F-03Feb2017-v1__part0',
#             'latino_SingleMuon_Run2016F-03Feb2017-v1__part1',
#             'latino_DoubleEG_Run2016F-03Feb2017-v1',
#             'latino_SingleElectron_Run2016F-03Feb2017-v1',
 # G - fake
#             'latino_MuonEG_Run2016G-03Feb2017-v1',
#             'latino_DoubleMuon_Run2016G-03Feb2017-v1__part0',
#             'latino_DoubleMuon_Run2016G-03Feb2017-v1__part1',
#             'latino_DoubleMuon_Run2016G-03Feb2017-v1__part2',
#             'latino_DoubleMuon_Run2016G-03Feb2017-v1__part3',
#             'latino_SingleMuon_Run2016G-03Feb2017-v1__part0',
#             'latino_SingleMuon_Run2016G-03Feb2017-v1__part1',
#             'latino_SingleMuon_Run2016G-03Feb2017-v1__part2',
#             'latino_SingleMuon_Run2016G-03Feb2017-v1__part3',
#             'latino_DoubleEG_Run2016G-03Feb2017-v1__part0',
#             'latino_DoubleEG_Run2016G-03Feb2017-v1__part1',
#             'latino_SingleElectron_Run2016G-03Feb2017-v1__part0',
#             'latino_SingleElectron_Run2016G-03Feb2017-v1__part1',
 # H - fake
#             'latino_MuonEG_Run2016H-03Feb2017_ver2-v1',
#             'latino_DoubleMuon_Run2016H-03Feb2017_ver2-v1__part0',
#             'latino_DoubleMuon_Run2016H-03Feb2017_ver2-v1__part1',
#             'latino_DoubleMuon_Run2016H-03Feb2017_ver2-v1__part2',
#             'latino_DoubleMuon_Run2016H-03Feb2017_ver2-v1__part3',
#             'latino_SingleMuon_Run2016H-03Feb2017_ver2-v1__part0',
#             'latino_SingleMuon_Run2016H-03Feb2017_ver2-v1__part1',
#             'latino_SingleMuon_Run2016H-03Feb2017_ver2-v1__part2',
#             'latino_SingleMuon_Run2016H-03Feb2017_ver2-v1__part3',
#             'latino_DoubleEG_Run2016H-03Feb2017_ver2-v1__part0',
#             'latino_DoubleEG_Run2016H-03Feb2017_ver2-v1__part1',
#             'latino_SingleElectron_Run2016H-03Feb2017_ver2-v1__part0',
#             'latino_SingleElectron_Run2016H-03Feb2017_ver2-v1__part1',
#             'latino_MuonEG_Run2016H-03Feb2017_ver3-v1',
#             'latino_DoubleMuon_Run2016H-03Feb2017_ver3-v1',
#             'latino_SingleMuon_Run2016H-03Feb2017_ver3-v1',
#             'latino_DoubleEG_Run2016H-03Feb2017_ver3-v1',
#             'latino_SingleElectron_Run2016H-03Feb2017_ver3-v1',
 # B - data
#            'latino_MuonEG_Run2016B-03Feb2017_ver2-v2',
#            'latino_DoubleMuon_Run2016B-03Feb2017_ver2-v2__part0',
#            'latino_DoubleMuon_Run2016B-03Feb2017_ver2-v2__part1',
#            'latino_DoubleMuon_Run2016B-03Feb2017_ver2-v2__part2',
#            'latino_SingleMuon_Run2016B-03Feb2017_ver2-v2__part0',
#            'latino_SingleMuon_Run2016B-03Feb2017_ver2-v2__part1',
#            'latino_SingleMuon_Run2016B-03Feb2017_ver2-v2__part2',
#            'latino_DoubleEG_Run2016B-03Feb2017_ver2-v2',
#            'latino_SingleElectron_Run2016B-03Feb2017_ver2-v2',
 # C - data
#            'latino_MuonEG_Run2016C-03Feb2017-v1',
#            'latino_DoubleMuon_Run2016C-03Feb2017-v1',
#            'latino_SingleMuon_Run2016C-03Feb2017-v1',
#            'latino_DoubleEG_Run2016C-03Feb2017-v1',
#            'latino_SingleElectron_Run2016C-03Feb2017-v1',
 # D - data
#            'latino_MuonEG_Run2016D-03Feb2017-v1',
#            'latino_DoubleMuon_Run2016D-03Feb2017-v1__part0',
#            'latino_DoubleMuon_Run2016D-03Feb2017-v1__part1',
#            'latino_SingleMuon_Run2016D-03Feb2017-v1__part0',
#            'latino_SingleMuon_Run2016D-03Feb2017-v1__part1',
#            'latino_DoubleEG_Run2016D-03Feb2017-v1',
#            'latino_SingleElectron_Run2016D-03Feb2017-v1',
 # E - data
#            'latino_MuonEG_Run2016E-03Feb2017-v1',
#            'latino_DoubleMuon_Run2016E-03Feb2017-v1__part0',
#            'latino_DoubleMuon_Run2016E-03Feb2017-v1__part1',
#            'latino_SingleMuon_Run2016E-03Feb2017-v1__part0',
#            'latino_SingleMuon_Run2016E-03Feb2017-v1__part1',
#            'latino_DoubleEG_Run2016E-03Feb2017-v1',
#            'latino_SingleElectron_Run2016E-03Feb2017-v1',
 # F - data
#            'latino_MuonEG_Run2016F-03Feb2017-v1',
#            'latino_DoubleMuon_Run2016F-03Feb2017-v1__part0',
#            'latino_DoubleMuon_Run2016F-03Feb2017-v1__part1',
#            'latino_SingleMuon_Run2016F-03Feb2017-v1__part0',
#            'latino_SingleMuon_Run2016F-03Feb2017-v1__part1',
#            'latino_DoubleEG_Run2016F-03Feb2017-v1',
#            'latino_SingleElectron_Run2016F-03Feb2017-v1',
 # G - data
#            'latino_MuonEG_Run2016G-03Feb2017-v1',
#            'latino_DoubleMuon_Run2016G-03Feb2017-v1__part0',
#            'latino_DoubleMuon_Run2016G-03Feb2017-v1__part1',
#            'latino_DoubleMuon_Run2016G-03Feb2017-v1__part2',
#            'latino_SingleMuon_Run2016G-03Feb2017-v1__part0',
#            'latino_SingleMuon_Run2016G-03Feb2017-v1__part1',
#            'latino_SingleMuon_Run2016G-03Feb2017-v1__part2',
#            'latino_DoubleEG_Run2016G-03Feb2017-v1__part0',
#            'latino_DoubleEG_Run2016G-03Feb2017-v1__part1',
#            'latino_SingleElectron_Run2016G-03Feb2017-v1__part0',
#            'latino_SingleElectron_Run2016G-03Feb2017-v1__part1',
 # H - data
#            'latino_MuonEG_Run2016H-03Feb2017_ver2-v1',
#            'latino_DoubleMuon_Run2016H-03Feb2017_ver2-v1__part0',
#            'latino_DoubleMuon_Run2016H-03Feb2017_ver2-v1__part1',
#            'latino_DoubleMuon_Run2016H-03Feb2017_ver2-v1__part2',
#            'latino_DoubleMuon_Run2016H-03Feb2017_ver2-v1__part3',
#            'latino_SingleMuon_Run2016H-03Feb2017_ver2-v1__part0',
#            'latino_SingleMuon_Run2016H-03Feb2017_ver2-v1__part1',
#            'latino_SingleMuon_Run2016H-03Feb2017_ver2-v1__part2',
#            'latino_DoubleEG_Run2016H-03Feb2017_ver2-v1__part0',
#            'latino_DoubleEG_Run2016H-03Feb2017_ver2-v1__part1',
#            'latino_SingleElectron_Run2016H-03Feb2017_ver2-v1__part0',
#            'latino_SingleElectron_Run2016H-03Feb2017_ver2-v1__part1',
#            'latino_MuonEG_Run2016H-03Feb2017_ver3-v1',
#            'latino_DoubleMuon_Run2016H-03Feb2017_ver3-v1',
#            'latino_SingleMuon_Run2016H-03Feb2017_ver3-v1',
#            'latino_DoubleEG_Run2016H-03Feb2017_ver3-v1',
#            'latino_SingleElectron_Run2016H-03Feb2017_ver3-v1',
]

for ifile in files:
  for ipath in paths:
    file_name = ipath+ifile
    file_name = file_name + '.root'
    print('Classifying file %s' % file_name)
    
    f = TFile( file_name )
    tree = f.Get('latino')
    nentries = tree.GetEntries()
    #
    eosjh = '/eos/user/l/lusanche/Full2016/VBF_DNNvar/400mjj700NodetajjDNN/Apr2017_summer16'
    #eosjh = '/eos/user/l/lusanche/Full2016/VBF_DNNvar/400mjj700NodetajjDNN/Apr2017_Run2016H_RemAOD'
    #
    path_eosjh = eosjh+'/lepSel__MCWeights__bSFLpTEffMulti__cleanTauMC__l2loose__hadd__l2tightOR__LepTrgFix__dorochester__formulasMC__wwSel__doDNN/'
    #path_eosjh = eosjh+'/lepSel__EpTCorr__TrigMakerData__cleanTauData__l2loose__dorochester__multiFakeW__formulasFAKE__hadd__wwSel__doDNN/'
    #path_eosjh = eosjh+'/lepSel__EpTCorr__TrigMakerData__cleanTauData__l2loose__hadd__l2tightOR__dorochester__formulasDATA__wwSel__doDNN/'
    new_file = TFile( path_eosjh + ifile + '.root' , 'recreate' )
    new_tree = TTree('latino', 'probe_tree')
    new_tree = tree.CloneTree(0)
    n = numpy.zeros(1, dtype=float)
    new_tree.Branch( 'DNNvar', n, 'DNNvar/D' )
    
    X_test = [[0 for i in range(12)] for j in range(nentries)]
 
    ientry = 0
    for i in tree:
      X_test[ientry][0] = i.std_vector_lepton_pt[0]
      X_test[ientry][1] = i.std_vector_lepton_eta[0]
      X_test[ientry][2] = i.std_vector_lepton_phi[0]
      X_test[ientry][3] = i.std_vector_lepton_pt[1]
      X_test[ientry][4] = i.std_vector_lepton_eta[1]
      X_test[ientry][5] = i.std_vector_lepton_phi[1]
      X_test[ientry][6] = i.std_vector_jet_pt[0]
      X_test[ientry][7] = i.std_vector_jet_eta[0]
      X_test[ientry][8] = i.std_vector_jet_phi[0]
      X_test[ientry][9] = i.std_vector_jet_pt[1]
      X_test[ientry][10] = i.std_vector_jet_eta[1]
      X_test[ientry][11] = i.std_vector_jet_phi[1]
      ientry = ientry + 1
      #print 'Pocessing event=',ientry
      
    Y_pred  = loaded_model.predict(Normalize(X_test))
    for i in range(nentries):   
      tree.GetEntry(i)  
      n[0] = Y_pred[i][0]
      new_tree.Fill()
    
    new_tree.Write()
    new_file.Close()
    f.Close()

