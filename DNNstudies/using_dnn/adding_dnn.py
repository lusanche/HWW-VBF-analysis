#!/usr/bin/env python

import sys
sys.path.insert(0,"/afs/cern.ch/user/l/lusanche/.local/lib/python2.7/site-packages")

#from ROOT import TFile, TTree, TMath
from ROOT import *
from array import array

#For test model
import numpy, math
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers.advanced_activations import LeakyReLU, PReLU
from keras.optimizers import SGD, Adam, RMSprop, Adagrad, Adadelta, Adamax, Nadam
from keras.utils import np_utils
from keras.models import model_from_json

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

#loads the model
smodel = "/afs/cern.ch/user/l/lusanche/KERAS/run_dnn/model1.json"
sweight = "/afs/cern.ch/user/l/lusanche/KERAS/run_dnn/model1_weights_json.h5"
json_file = open(smodel,'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights(sweight)

opt = Adamax();

#compile the model
loaded_model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['acc'])

paths = ["~/eosuser/user/l/lusanche/samples/reduced/"
	 ]

files = [    "latino_vbf_m125v1_alt_reduced",
             "latino_ggf_reduced",
             "latino_ww_reduced",
             "latino_DYJetsToLL_reduced",
             "latino_top_reduced",
]

for ifile in files:
  for ipath in paths:
    file_name = ipath+ifile
    file_name_root = file_name + ".root"
    print("Classifying file %s" % file_name_root)
    
    f = TFile( file_name_root )
    tree = f.Get('latino')
    nentries = tree.GetEntries()
    
    new_file = TFile( file_name + "_dnn" + ".root", 'recreate' )
    new_tree = TTree("latino", "probe_tree")
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
      
    Y_pred  = loaded_model.predict(X_test)
    for i in range(nentries):   
      tree.GetEntry(i)  
      n[0] = Y_pred[i][0]
      new_tree.Fill()

    new_tree.Write()
    new_file.Close()
    f.Close()
