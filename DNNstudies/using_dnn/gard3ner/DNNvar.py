#
#     ___ \       \   |     \   |
#     |    |    |\ \  |   |\ \  |                          _)         |      | 
#     |    |    | \ \ |   | \ \ |      \ \   /  _` |   __|  |   _` |  __ \   |   _ \ 
#     |    |    |  \  |   |  \  |       \ \ /  (   |  |     |  (   |  |   |  |   __/
#    _____/    _|   \_|  _|   \_|        \_/  \__,_| _|    _| \__,_| _.__/  _| \___|
#

#!/usr/bin/env python

from LatinoAnalysis.Gardener.gardening import TreeCloner

import optparse
import os
import sys
import ROOT import *
import numpy
import array
import re
import warnings
import os.path
from math import *
import math

from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense, Dropout, Activation
from keras.layers.advanced_activations import LeakyReLU, PReLU
from keras.optimizers import SGD, Adam, RMSprop, Adagrad, Adadelta, Adamax, Nadam
from keras.utils import np_utils

class DNNvarFiller(TreeCloner):
    def __init__(self):
       pass

#    def createDNNvar(self):
#        self.AddVariable("DNNvar", (self.var))
#        
#        ## DNN trained json.bkg" + self.kind + ".xml")
#        self.Keras("DNN","/afs/cern.ch/user/l/lusanche/Latinos/KERAS/run_dnn/Full2016/using_weights/model.json")

    def help(self):
        return '''Add DNN variable'''

    def addOptions(self,parser):
        pass

    def checkOptions(self,opts):
        pass

    def process(self,**kwargs):
#        self.getDNNvar = None
#        self.var  = array.array('d',[0]))
        tree  = kwargs['tree']
        input = kwargs['input']
        output = kwargs['output']

        # does that work so easily and give new variable itree and otree?
        self.connect(tree,input)
        newbranches = ['dnnvar']
        self.clone(output,newbranches)

        dnnvar   = numpy.ones(1, dtype=numpy.double)

        self.otree.Branch('dnnvar',  dnnvar,  'dnnvar/D')

#        self.createDNNvar()

        nentries = self.itree.GetEntries()
        print 'Total number of entries: ',nentries 

        # avoid dots to go faster
        itree     = self.itree
        otree     = self.otree

#        # change this part into correct path structure... 
#        cmssw_base = os.getenv('CMSSW_BASE')
#        ROOT.gROOT.LoadMacro(cmssw_base+'/src/LatinoAnalysis/Gardener/python/variables/DMVar.C+g')
#----------------------------------------------------------------------------------------------------  

        print '- Starting eventloop'
        step = 5000
        for i in xrange(nentries):
            itree.GetEntry(i)

            ## print event count
            if i > 0 and i%step == 0.:
                print i,'events processed.'

#            dnnvar[0] = -9999.
            
            # just because it is easier to write later ...
            pt1 = itree.std_vector_lepton_pt[0]
            pt2 = itree.std_vector_lepton_pt[1]
            
#            if pt1>0 and pt2>0 : 
#              self.var[0]   =  itree.DNNvar
#              dnnvar[0] = self.getDNNvar.Evaluate("DNN")
             
            otree.Fill()
            
        self.disconnect()
print '- Eventloop completed'
