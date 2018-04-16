#include <iostream>
#include "TFile.h"
#include "TTree.h"
#include <fstream>

using namespace std;

void root_to_txt(){
  
  //TString filenames[1]={"latino_vbf_m125v1_reduced.root"};//,
  //TString filenames[1]={"latino_vbf_m125v1_alt_reduced.root"};//,
  //TString filenames[1]={"latino_vbf_m125v2_reduced.root"};//,
  //TString filenames[1]={"latino_vbf_m125v2_alt_reduced.root"};//,
  //TString filenames[1]={"latino_ggf_reduced.root"};//,
  //TString filenames[1]={"latino_ww_reduced.root"};//,
  //TString filenames[1]={"latino_DYJetsToLL_M-10andTT_M-50_reduced.root"};//,
  TString filenames[1]={"latino_top_reduced.root"};
  
  for (int i=0; i<1; i++) {
       TFile *samples=new TFile(filenames[i]);  
       TTree *t=(TTree*)samples->Get("latino");
       
       std::vector<float> *ptl, *etal, *phil, *flal, *ptj, *etaj, *phij, *cmvaj;
       float ptll, mth, mll, metPfType1, metPfType1Phi, metPfType1SumEt, njet, detajj, mjj, drll, xs_w;
  
      t->SetBranchAddress("std_vector_lepton_pt",&ptl);
      t->SetBranchAddress("std_vector_lepton_eta",&etal);
      t->SetBranchAddress("std_vector_lepton_phi",&phil);
      t->SetBranchAddress("std_vector_lepton_flavour",&flal);
      t->SetBranchAddress("std_vector_jet_pt",&ptj);
      t->SetBranchAddress("std_vector_jet_eta",&etaj);
      t->SetBranchAddress("std_vector_jet_phi",&phij);
      t->SetBranchAddress("std_vector_jet_cmvav2",&cmvaj);
      t->SetBranchAddress("ptll",&ptll);
      t->SetBranchAddress("mll",&mll);
      t->SetBranchAddress("mjj",&mjj);
      t->SetBranchAddress("mth",&mth);
      t->SetBranchAddress("detajj",&detajj);
      t->SetBranchAddress("metPfType1",&metPfType1);
      t->SetBranchAddress("njet",&njet);
      t->SetBranchAddress("drll",&drll);
      t->SetBranchAddress("XSWeight",&xs_w);
      
      int nevents = 0;
      float ptj_threshold = 20, bveto = -0.5884;//-0.715;
      
      for (int j=0; j<t->GetEntries(); j++) {
	   t->GetEntry(j);
	   
	   float ptl1 = (*ptl)[0], ptl2 = (*ptl)[1], ptl3 = (*ptl)[2], etal1 = (*etal)[0], etal2 = (*etal)[1], phil1 = (*phil)[0], phil2 = (*phil)[1];
	   float ptj1 = (*ptj)[0], ptj2 = (*ptj)[1], ptj3 = (*ptj)[2], ptj4 = (*ptj)[3], ptj5 = (*ptj)[4], ptj6 = (*ptj)[5], ptj7 = (*ptj)[6], ptj8 = (*ptj)[7];
	   float ptj9 = (*ptj)[8], ptj10 = (*ptj)[9], etaj1 = (*etaj)[0], etaj2 = (*etaj)[1], phij1 = (*phij)[0], phij2 = (*phij)[1];
	   float cmvaj1 = (*cmvaj)[0], cmvaj2 = (*cmvaj)[1], cmvaj3 = (*cmvaj)[2], cmvaj4 = (*cmvaj)[3], cmvaj5 = (*cmvaj)[4], cmvaj6 = (*cmvaj)[5], cmvaj7 = (*cmvaj)[6];
	   float cmvaj8 = (*cmvaj)[7], cmvaj9 = (*cmvaj)[8], cmvaj10 = (*cmvaj)[9], flal1 = (*flal)[0], flal2 = (*flal)[1];
	   
	   if ( mll>12 && (ptl1>25&&ptl2>10&&ptl3<10) && metPfType1>20 && ptll>30 && (flal1*flal2==-11*13)// && (detajj>3.5 && mll<80 && drll<2.0)
	        && (abs(flal2)==13||ptl2>13) && (mth>=60&&mth<125) && njet==2 && (abs(etaj1)<4.7&&abs(etaj2)<4.7) && mjj>400
	        && (ptj1>=30&&ptj2>=30) && (cmvaj1<bveto&&cmvaj2<bveto) && (ptj3<ptj_threshold||cmvaj3<bveto) && (ptj4<ptj_threshold||cmvaj4<bveto) 
		&& (ptj5<ptj_threshold||cmvaj5<bveto) && (ptj6<ptj_threshold||cmvaj6<bveto) && (ptj7<ptj_threshold||cmvaj7<bveto) && (ptj8<ptj_threshold||cmvaj8<bveto) 
		&& (ptj9<ptj_threshold||cmvaj9<bveto) && (ptj10<ptj_threshold||cmvaj10<bveto) ) {
	            cout << ptl1 << "," << etal1 << "," << phil1 << "," << ptl2 << "," << etal2 << "," << phil2 << "," ;
		    cout << ptj1 << "," << etaj1 << "," << phij1 << "," << ptj2 << "," << etaj2 << "," << phij2 << "," ;
		    cout << xs_w << "," ;
	            //if (i==0) cout << 1 << endl;
	            if (i==0) cout << 0 << endl;
	       }
           }
        }
}

