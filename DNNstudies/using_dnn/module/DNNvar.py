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

#
#     ___ \       \   |     \   |
#     |    |    |\ \  |   |\ \  |                          _)         |      | 
#     |    |    | \ \ |   | \ \ |      \ \   /  _` |   __|  |   _` |  __ \   |   _ \ 
#     |    |    |  \  |   |  \  |       \ \ /  (   |  |     |  (   |  |   |  |   __/
#    _____/    _|   \_|  _|   \_|        \_/  \__,_| _|    _| \__,_| _.__/  _| \___|
#

class DNNvarFiller(TreeCloner):
    def __init__(self):
       pass

    def createDNNvar(self):
        self.AddVariable("DNNvar", (self.var))
        
        ## DNN training json
        self.Keras("DNN","/afs/cern.ch/user/l/lusanche/Latinos/KERAS/run_dnn/Full2016/using_weights/model.json")

    def help(self):
        return '''Add DNN variable'''

    def addOptions(self,parser):
        pass

    def checkOptions(self,opts):
        pass

    def process(self,**kwargs):
        
        self.getDNNvar = None
        
        self.var  = array.array('d',[0]))
        
        tree  = kwargs['tree']
        input = kwargs['input']
        output = kwargs['output']
        
        # does that work so easily and give new variable itree and otree?
        self.connect(tree,input)
        newbranches = ['DNNvar']
        
        self.clone(output,newbranches)

        DNNvar   = numpy.ones(1, dtype=numpy.double)

        self.otree.Branch('dnnvar',  dnnvar,  'dnnvar/D')

        self.createDNNvar()

        nentries = self.itree.GetEntries()
        print 'Total number of entries: ',nentries 

        # avoid dots to go faster
        itree     = self.itree
        otree     = self.otree

        print '- Starting eventloop'
        step = 5000
        for i in xrange(nentries):
            itree.GetEntry(i)

            ## print event count
            if i > 0 and i%step == 0.:
                print i,'events processed.'

            self.var[0]   =  itree.DNNvar
            DNNvar[0] = self.getDNNvar.Evaluate("DNN")
             
            otree.Fill()
            
        self.disconnect()
        print '- Eventloop completed'
