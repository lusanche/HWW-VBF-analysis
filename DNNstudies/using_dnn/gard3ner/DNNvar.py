#!/usr/bin/env python

from LatinoAnalysis.Gardener.gardening import TreeCloner
import numpy
import ROOT
from ROOT import TMVA, TFile, TString
import sys
import optparse
import re
import warnings
import os
import os.path
import array
from math import *
import math
import keras

class DNNvarFiller(TreeCloner):
    def __init__(self):
       pass

    def createDNNvarMVA(self):
        self.getDNNvarMVAV = ROOT.TMVA.Reader();
        ## the order is important for TMVA!
        self.getDNNvarMVAV.AddVariable("DNNvar", (self.var1))
        ## I need to declare the spectator ... for some strange ROOT reasons ...
        #self.getMuccaMVAV.AddSpectator("std_vector_jet_pt[0]",   (self.var17))
        ## mva trainined xml
        #baseCMSSW = os.getenv('CMSSW_BASE')
        #self.getMuccaMVAV.BookMVA("BDT",baseCMSSW+"/src/LatinoAnalysis/Gardener/python/data/mucca/TMVAClassification_BDTG.weights.bkg" + self.kind + ".xml")
        self.getDNNvarMVAV.BookMVA("PyKeras","/afs/cern.ch/user/l/lusanche/Latinos/KERAS/run_dnn/Full2016/using_weights/model1.json")

    def help(self):
        return '''Add DNN variable'''

    def addOptions(self,parser):
        description = self.help()
        group = optparse.OptionGroup(parser,self.label, description)
        group.add_option('-k', '--kind',   dest='kind', help='Which background training to be used', default='1')
        group.add_option('-s', '--signal', dest='signal', help='Signal model', default='VBF')
        parser.add_option_group(group)
        return group
        pass


    def checkOptions(self,opts):
        if not (hasattr(opts,'kind')):
            raise RuntimeError('Missing parameter')
        self.kind      = opts.kind
        print " kind   = ", self.kind
        self.signal    = opts.signal
        print " signal = ", self.signal


    def process(self,**kwargs):

        self.getDNNvarMVAV = None

        self.var1  = array.array('d',[0])
        #self.var17 = array.array('f',[0])
        
        tree  = kwargs['tree']
        input = kwargs['input']
        output = kwargs['output']

        self.connect(tree,input)
        newbranches = ['dnnmva'+ self.kind]

        self.clone(output,newbranches)

        dnnmva   = numpy.ones(1, dtype=numpy.double)

        self.otree.Branch('dnnmva'+ self.kind,  dnnmva,  'dnnmva' + self.kind + '/D')

        self.createDNNvarMVA()

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

            dnnmva[0] = -9999.
            
            # just because it is easier to write later ...
            pt1 = itree.std_vector_lepton_pt[0]
            pt2 = itree.std_vector_lepton_pt[1]
            
            if pt1>0 and pt2>0 : 

              self.var1[0]   =  itree.DNNvar
              #self.var17[0]  =  itree.std_vector_jet_pt[0]
              
              dnnmva[0] = self.getDNNvarMVAV.EvaluateMVA("DNN")
              
            otree.Fill()
            
        self.disconnect()
print '- Eventloop completed'
