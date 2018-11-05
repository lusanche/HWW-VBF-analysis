#!/usr/bin/env python

import os # To disable all logging output from TensorFlow using an environment variable.
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' # a min log level for logging in C++. 2 to additionall filter out WARNING.

## Create first network with Keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.constraints import maxnorm
from ROOT import *
from sklearn.metrics import roc_curve, auc

## MLP for dataset serialize to JSON/YAML and HDF5
from keras.models import model_from_json
#from keras.models import model_from_yaml

import pandas
import numpy as np
import random
#import matplotlib
#matplotlib.use('Agg') # generate images without having a window appear:  Agg (for PNGs), PDF, SVG or PS
import matplotlib.pyplot as plt

## input normalization function
def Normalize(a):
  max = np.amax(a,axis=0)
  min = np.amin(a,axis=0)
  norm = (a-min)/(max-min)
  return norm

## load dataset train/test
path = '/home/juniorhiggs/Documentos/Latinos/Full2016/KERAS'
dataset_training=np.loadtxt(path+'/1.samples_txt/using_weights/InputNorm/mjj400_mjj700/sXb/train_sXb_mjj400b.txt',delimiter=',')
dataset_testing= np.loadtxt(path+'/1.samples_txt/using_weights/InputNorm/mjj400_mjj700/sXb/test_sXb_mjj400b.txt', delimiter=',')

##############################
#########  TRAINING  #########
##############################

## split the attributes (columns) into input (X) and output (Y) variables...
X_training = dataset_training[:,0:12] #  columns
X_training = Normalize(X_training) # norm
W_training = abs(dataset_training[:,12]) # weights
Y_training = dataset_training[:,13] # class: final columns

bsize=5
nepoch=400
n_neu_hid1=10000
#dropout1=0.5
bsne = '_'+str(bsize)+':'+str(nepoch)+'_12:'
nnxhl = str(n_neu_hid1)+':1_mjj400b_tfSWTsr'
## create model
model = Sequential()
model.add(Dense(n_neu_hid1, input_dim=12, kernel_initializer='normal', activation='relu')) # input_dim : input neuron number
#model.add(Dense(n_neu_hid2, kernel_initializer='normal', activation='relu', W_constraint=maxnorm(1)))
#model.add(Dropout(dropout1))
model.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))

## Compile model (required to make predictions) ==> Logarithmic Loss Function: binary_crossentropy
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print("Created model and loaded weights from file")

## Fix random seed for reproducibility
seed = 7 # Only shuffles the array along the first axis of a multi-dimensional array.
np.random.seed(seed)
np.random.shuffle(X_training)
np.random.seed(seed)
np.random.shuffle(Y_training)
np.random.seed(seed)
np.random.shuffle(W_training)

## Fit the model
history = model.fit(X_training, Y_training, batch_size=bsize, epochs=nepoch, verbose=2, validation_split=0.2, sample_weight=W_training)

print(dataset_training.shape[0], 'train data')
print(dataset_testing.shape[0], 'test data')

## Evaluate the model
scores = model.evaluate(X_training, Y_training, verbose=0)

## serialize model to JSON
model_json = model.to_json()
with open('model_weight/model'+bsne+nnxhl+'.json', 'w') as json_file:
    json_file.write(model_json)
## serialize weights to HDF5
model.save_weights('model_weight/weights'+bsne+nnxhl+'.h5')

## load JSON/YAML and create model
json_file = open('model_weight/model'+bsne+nnxhl+'.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
## load weights into new model
loaded_model.load_weights('model_weight/weights'+bsne+nnxhl+'.h5')

##############################
##########  TESTING  #########
##############################

## split the attributes (columns) into input (X) and output (Y) variables...
X_testing = dataset_testing[:,0:12] #  columns
X_testing = Normalize(X_testing) # norm
W_testing = abs(dataset_testing[:,12]) # weights
Y_testing = dataset_testing[:,13] # class: final columns

## RST: Fix random seed for reproducibility
seed = 7 # Only shuffles the array along the first axis of a multi-dimensional array.
np.random.seed(seed)
np.random.shuffle(X_testing)
np.random.seed(seed)
np.random.shuffle(Y_testing)
np.random.seed(seed)
np.random.shuffle(W_testing)

## evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
score = loaded_model.evaluate(X_testing, Y_testing, verbose=0, sample_weight=W_testing)

## Calculate predictions
predictions_train = loaded_model.predict(X_training)
predictions_test = loaded_model.predict(X_testing)

# list all data in history
#print(history.history.keys())
# summarize history for accuracy
fig = plt.figure(figsize=(9,6.5))
plt.subplot(211)
plt.plot(history.history['acc'], lw=2)
plt.plot(history.history['val_acc'], lw=2)#, ls='--')
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.grid()
plt.legend(['train', 'valid'], loc='best', fancybox=True)#, title='Model Accuracy')
# summarize history for loss
plt.subplot(212)
plt.plot(history.history['loss'], lw=2)
plt.plot(history.history['val_loss'], lw=2)#, ls='--')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.grid()
plt.legend(['train', 'valid'], loc='best', fancybox=True)#,  title='Model Loss')#, loc='upper left')
fig.savefig('plots/evol'+bsne+nnxhl+'.png')

sig_train = TH1D("sig_train","",100,-0.025,1.025)
sig_train.SetLineColor(kRed)
bkg_train = TH1D("bkg_train","",100,-0.025,1.025)
bkg_train.SetLineColor(kBlue)
sig_test = TH1D("sig_test","",100,-0.025,1.025)
sig_test.SetLineColor(kRed)
sig_test.SetFillColor(kRed)
sig_test.SetFillStyle(3008)
bkg_test = TH1D("bkg_test","",100,-0.025,1.025)
bkg_test.SetLineColor(kBlue)
bkg_test.SetFillColor(kBlue)
bkg_test.SetFillStyle(3008)

g1 = TGraph()
g2 = TGraph()

## building ROC curve
ipoint=0
n=101
ROC_train = np.zeros((n,2))
ROC_test = np.zeros((n,2))
for j in range(n):
  jcut = j/(n-1.)
  TN_train=FP_train=TP_train=FN_train=TN_test=FP_test=TP_test=FN_test=0
  
  for i in range(len(Y_training)):####################3 training ##################3
    if Y_training[i]==0:
      if jcut==0:
	bkg_train.Fill(predictions_train[i])
      if predictions_train[i]<jcut:
	TN_train=TN_train+1
      else :
	FP_train=FP_train+1
    else :
      if jcut==0:
	sig_train.Fill(predictions_train[i])
      if predictions_train[i]>jcut:
	TP_train=TP_train+1
      else :
	FN_train=FN_train+1
  TPR_train = TP_train/float(TP_train+FN_train)#signal efficiency
  FPR_train = FP_train/float(FP_train+TN_train)#background efficiency
  TNR_train = TN_train/float(FP_train+TN_train)#background rejection
  ROC_train[j,1]=TPR_train
  ROC_train[j,0]=TNR_train#FPR_train
  g1.SetPoint(ipoint,jcut,TPR_train)
  g2.SetPoint(ipoint,jcut,TNR_train)#FPR_train)

  for i in range(len(Y_testing)):####################3 testing ##################3
    if Y_testing[i]==0:
      if jcut==0:
	bkg_test.Fill(predictions_test[i])
      if predictions_test[i]<jcut:
	TN_test=TN_test+1
      else :
	FP_test=FP_test+1
    else :
      if jcut==0:
	sig_test.Fill(predictions_test[i])
      if predictions_test[i]>jcut:
	TP_test=TP_test+1
      else :
	FN_test=FN_test+1
  TPR_test = TP_test/float(TP_test+FN_test)#signal efficiency
  FPR_test = FP_test/float(FP_test+TN_test)#background efficiency
  TNR_test = TN_test/float(FP_test+TN_test)#background rejection
  ROC_test[j,1]=TPR_test
  ROC_test[j,0]=TNR_test#FPR_test
  g1.SetPoint(ipoint,jcut,TPR_test)
  g2.SetPoint(ipoint,jcut,TNR_test)#FPR_test)
  
  ipoint=ipoint+1

AUC_train=AUC_test=0.
for i in range(n-1):
    AUC_train += abs(ROC_train[i,0]-ROC_train[i+1,0]) * (ROC_train[i+1,1]+ROC_train[i,1])
    AUC_test += abs(ROC_test[i,0]-ROC_test[i+1,0]) * (ROC_test[i+1,1]+ROC_test[i,1])
AUC_train *= 0.5
AUC_test *= 0.5

# Plot the ROC curve.
fig = plt.figure(figsize=(6,6.5))
plt.plot(ROC_train[:,1], ROC_train[:,0], lw=2)
plt.plot(ROC_test[:,1], ROC_test[:,0], lw=2)#, ls='--')
plt.plot([0,1],[0,1], 'r--')
plt.xlim([-0.05,1.05])
plt.ylim([-0.05,1.05])
font = { 'family':'serif' , 'color':'darkred' , 'weight':'normal' , 'size': 13, }
plt.xlabel('Signal efficiency',fontdict=font)
plt.ylabel('Background rejection',fontdict=font)
plt.grid()
fonts = { 'family':'serif' , 'color':'darkred' , 'weight':'normal' , 'size': 15, }
plt.title('Receiver Operating Characteristic',fontdict=fonts)
plt.legend(['ROC train (AUC = %.2f%%)'%(AUC_train*100),'ROC test (AUC = %.2f%%)'%(AUC_test*100)], loc='best', fancybox=True)
fig.savefig('plots/roc'+bsne+nnxhl+'.png')

leg = TLegend(0.3,0.6,0.7,0.9)
leg.AddEntry(sig_train, 'Signal train', 'f')
leg.AddEntry(sig_test, 'Signal test', 'f')
leg.AddEntry(bkg_train, 'Background train', 'f')
leg.AddEntry(bkg_test, 'Background test', 'f')

CV = TCanvas()
CV.cd()
bkg_train.Draw()
sig_train.Draw("same")
bkg_test.Draw("same")
sig_test.Draw("same")
leg.Draw()
CV.SaveAs('plots/disc'+bsne+nnxhl+'.png')
CV.SaveAs('plots/disc'+bsne+nnxhl+'.root')

plt.show()
