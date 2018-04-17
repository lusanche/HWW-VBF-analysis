#!/usr/bin/env python

## about CMSSW in LXPLUS
#import sys
#sys.path.insert(0,"/afs/cern.ch/user/l/lusanche/.local/lib/python2.7/site-packages")

## Create first network with Keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.constraints import maxnorm

from keras.callbacks import ModelCheckpoint

## Feature Extraction with Univariate Statistical Tests (Chi-squared for classification)
import pandas
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

## Scatterplot Matrix
from pandas.tools.plotting import scatter_matrix

## MLP for dataset serialize to JSON/YAML and HDF5
from keras.models import model_from_json
#from keras.models import model_from_yaml

from ROOT import *
ROOT.gStyle.SetOptStat(0)
from sklearn.metrics import roc_curve, auc
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random

## load dataset
dataset_training=np.loadtxt("../data_txt/sigXbkg_train.txt",delimiter=",")
#dataset_training=np.loadtxt("/afs/cern.ch/user/l/lusanche/Latinos/KERAS/data_txt/Full2016/sigXbkg_train.txt",delimiter=",")
print(dataset_training.shape)

## split the attributes (columns) into input (X) and output (Y) variables...
X_training = dataset_training[:,0:12] #  columns
W_t = dataset_training[:,12] # weights
Y_training = dataset_training[:,13] # class: final columns
W_training = abs(W_t)

## create model
model = Sequential()
model.add(Dense(72, input_dim=12, init='normal', activation='relu'))
#model.add(Dense(72, input_dim=12, kernel_initializer='normal', activation='relu'))
#model.add(Dropout(0.1))
model.add(Dense(48, init='normal', activation='relu', W_constraint=maxnorm(1)))
#model.add(Dense(48, kernel_initializer='normal', activation='relu', kernel_constraint=maxnorm(1)))
model.add(Dropout(0.1))
model.add(Dense(24, init='normal', activation='relu', W_constraint=maxnorm(1)))
#model.add(Dense(24, kernel_initializer='normal', activation='relu', kernel_constraint=maxnorm(1)))
#model.add(Dropout(0.1))
model.add(Dense(4, init='normal', activation='relu', W_constraint=maxnorm(1)))
#model.add(Dense(4, kernel_initializer='normal', activation='relu', kernel_constraint=maxnorm(1)))
#model.add(Dropout(0.1))
model.add(Dense(1, init='uniform', activation='sigmoid'))
#model.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))

## Compile model (required to make predictions) ==> Logarithmic Loss Function: binary_crossentropy
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print("Created model and loaded weights from file")

## checkpoint
filepath="model1_weights_best.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

## Fix random seed for reproducibility
seed = 7 # Only shuffles the array along the first axis of a multi-dimensional array.
np.random.seed(seed) 
np.random.shuffle(X_training)
np.random.seed(seed)
np.random.shuffle(Y_training)
np.random.seed(seed)
np.random.shuffle(W_training)

## Fit the model
history = model.fit(X_training, Y_training, batch_size=50, nb_epoch=500, verbose=2, validation_split=0.2, callbacks=callbacks_list, sample_weight=W_training)
#history = model.fit(X_training, Y_training, batch_size=50, epochs=500, verbose=2, validation_split=0.2, callbacks=callbacks_list, sample_weight=W_training)
## Evaluate the model
scores = model.evaluate(X_training, Y_training, verbose=0)

## serialize model to JSON/YAML
model_json = model.to_json()
with open("model1.json", "w") as json_file:
    json_file.write(model_json)
#model_yaml = model.to_yaml()
#with open("model1.yaml", "w") as yaml_file:
#    yaml_file.write(model_yaml)
## serialize weights to HDF5
model.save_weights("model1_weights_json.h5")
#model.save_weights("model1_weights_yaml.h5")

## load JSON/YAML and create model
json_file = open('model1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
#yaml_file = open('model1.yaml', 'r')
#loaded_model_yaml = yaml_file.read()
#yaml_file.close()
#loaded_model = model_from_yaml(loaded_model_yaml)
## load weights into new model
loaded_model.load_weights("model1_weights_json.h5")
#loaded_model.load_weights("model1_weights_yaml.h5")

## dataset test
dataset_testing = np.loadtxt("../data_txt/sigXbkg_test.txt", delimiter=",")
#dataset_testing = np.loadtxt("/afs/cern.ch/user/l/lusanche/Latinos/KERAS/data_txt/Full2016/sigXbkg_test.txt", delimiter=",")

## split the attributes (columns) into input (X) and output (Y) variables...
X_testing = dataset_testing[:,0:12] #  columns
Y_testing = dataset_testing[:,13] # class: final columns

## evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
score = loaded_model.evaluate(X_testing, Y_testing, verbose=0)

## Calculate predictions
predictions = loaded_model.predict(X_testing)#X_training)

print("finish!")

sig = TH1D("sig","",100,-0.025,1.025)
sig.SetLineColor(kRed)
sig.SetFillColor(kRed)
sig.SetFillStyle(3008)
bkg = TH1D("bkg","",100,-0.025,1.025)
bkg.SetLineColor(kBlue)
bkg.SetFillColor(kBlue)
bkg.SetFillStyle(3008)
sig.GetXaxis().SetTitle("criterion value")
sig.GetYaxis().SetTitle("Events")

g1 = TGraph()
g1.SetLineColor(kRed)
g1.SetLineWidth(3) #g1.SetTitle("Signal efficiency;criterion value;TPR (Sensitivity)")
g2 = TGraph()
g2.SetLineColor(kBlue)
g2.SetLineWidth(3) #g2.SetTitle("Bakcground efficiency;criterion value;FPR (1-Specificity)")
ipoint=0

## building ROC curve
n=101
ROC = np.zeros((n,2))
for j in range(n):
  jcut = j/(n-1.)
  TN=FP=TP=FN=0
  for i in range(len(Y_testing)):#Y_training)):
    if Y_testing[i]==0:#Y_training[i]==0:
      if jcut==0:
	bkg.Fill(predictions[i])
      if predictions[i]<jcut:
	TN=TN+1
      else :
	FP=FP+1
    else :
      if jcut==0:
	sig.Fill(predictions[i])
      if predictions[i]>jcut:
	TP=TP+1
      else :
	FN=FN+1
  TPR = TP/float(TP+FN)
  ROC[j,1]=TPR
  FPR = FP/float(FP+TN)
  TNR = TN/float(FP+TN)
  ROC[j,0]=TNR#FPR
  g1.SetPoint(ipoint,jcut,TPR)
  g2.SetPoint(ipoint,jcut,TNR)#FPR)
  ipoint=ipoint+1

AUC = 0.
for i in range(n-1):
    AUC += fabs(ROC[i,0]-ROC[i+1,0]) * (ROC[i+1,1]+ROC[i,1])
AUC *= 0.5

CV = TCanvas()
CV.cd()
bkg.Draw()
sig.Draw("same")

# list all data in history
#print(history.history.keys())
# summarize history for accuracy
fig = plt.figure(figsize=(6,6.5))
plt.subplot(211)
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.grid()
plt.legend(['train', 'test'], loc='best', fancybox=True)#, title='Model Accuracy')
# summarize history for loss
plt.subplot(212)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.grid()
plt.legend(['train', 'test'], loc='best', fancybox=True)#,  title='Model Loss')#, loc='upper left')

## Plot the ROC curve.
fig = plt.figure(figsize=(6,6))
plt.plot(ROC[:,1], ROC[:,0], lw=2)
plt.plot([0,1],[0,1],'r--')
plt.xlim([-0.05,1.05])
plt.ylim([-0.05,1.05])
plt.xlabel('$Signal\ \ efficiency$')
plt.ylabel('$Background\ \ rejection$')#efficiency$')
plt.grid()
plt.title('Receiver Operating Characteristic')
fig.text(0.18,0.47,'AUC = %.2f%%'%(AUC*100),fontsize=22)
fig.text(0.18,0.37,'train_%s: %.2f%%'%(model.metrics_names[1], scores[1]*100),fontsize=15)
fig.text(0.18,0.31,'test_%s : %.2f%%'%(loaded_model.metrics_names[1], score[1]*100),fontsize=15)
fig.text(0.18,0.23,'train_%s: %.4f%%'%(model.metrics_names[0], scores[0]/100.0),fontsize=15)
fig.text(0.18,0.17,'test_%s  : %.4f%%'%(loaded_model.metrics_names[0], score[0]/100.0),fontsize=15)
plt.show()
