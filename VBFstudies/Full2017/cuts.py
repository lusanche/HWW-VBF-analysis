
# cuts

supercut = 'mll>12 \
         && Lepton_pt[0]>25 && Lepton_pt[1]>10 \
         && Alt$(Lepton_pt[2],0)<10 \
         && MET_pt>20 \
         && ptll>30 \
         && Lepton_pdgId[0]*Lepton_pdgId[1]==-11*13 \
         && njet==2 \
         && CleanJet_pt[0]>30 && CleanJet_pt[1]>30 \
         && Alt$(CleanJet_pt[2],0)<30 \
         '

#========================================== Signal regions - lowmjj
#
cuts['hww2l2v_13TeV_of2j_lowmjj_detajj'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*13) \
                                         && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
                                         && (mth>=60 && mth<125) \
                                         && (abs(CleanJet_eta[0])<4.7) && (abs(CleanJet_eta[1])<4.7) \
                                         && (abs((Lepton_eta[0]-(CleanJet_eta[0]+CleanJet_eta[1])/2)/detajj) < 0.5) \
                                         && (abs((Lepton_eta[1]-(CleanJet_eta[0]+CleanJet_eta[1])/2)/detajj) < 0.5) \
                                         && (detajj>3.5 && mjj>=400 && mjj<700) \
                                         && bVeto \
                                         '

#cuts['hww2l2v_13TeV_of2j_lowmjj_nodetajj'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*13) \
#                                           && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
#                                           && (mth>=60 && mth<125) \
#                                           && (abs(CleanJet_eta[0])<4.7) && (abs(CleanJet_eta[1])<4.7) \
#                                           && (abs((Lepton_eta[0]-(CleanJet_eta[0]+CleanJet_eta[1])/2)/detajj) < 0.5) \
#                                           && (abs((Lepton_eta[1]-(CleanJet_eta[0]+CleanJet_eta[1])/2)/detajj) < 0.5) \
#                                           && (mjj>=400 && mjj<700) \
#                                           && bVeto \
#                                           '
#
#========================================== Signal regions - highmjj
#
#cuts['hww2l2v_13TeV_of2j_highmjj_detajj'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*13) \
#                                         && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
#                                         && (mth>=60 && mth<125) \
#                                         && (abs(CleanJet_eta[0])<4.7) && (abs(CleanJet_eta[1])<4.7) \
#                                         && (abs((Lepton_eta[0]-(CleanJet_eta[0]+CleanJet_eta[1])/2)/detajj) < 0.5) \
#                                         && (abs((Lepton_eta[1]-(CleanJet_eta[0]+CleanJet_eta[1])/2)/detajj) < 0.5) \
#                                         && (detajj>3.5 && mjj>=700) \
#                                         && bVeto \
#                                         '
#
#cuts['hww2l2v_13TeV_of2j_highmjj_nodetajj'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*13) \
#                                           && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
#                                           && (mth>=60 && mth<125) \
#                                           && (abs(CleanJet_eta[0])<4.7) && (abs(CleanJet_eta[1])<4.7) \
#                                           && (abs((Lepton_eta[0]-(CleanJet_eta[0]+CleanJet_eta[1])/2)/detajj) < 0.5) \
#                                           && (abs((Lepton_eta[1]-(CleanJet_eta[0]+CleanJet_eta[1])/2)/detajj) < 0.5) \
#                                           && (mjj>=700) \
#                                           && bVeto \
#                                           '
#
#========================================== control regions
#
#cuts['hww2l2v_13TeV_top_of2j'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*13) \
#                               && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
#                               && (mll>50) \
#                               && (detajj>3.5 && mjj>400) \
#                               && btag2 \
#                               '
#
#cuts['hww2l2v_13TeV_dytt_of2j'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*13) \
#                                && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
#                                && (mll>40 && mll<80) && mth<60 \
#                                && (detajj>3.5 && mjj>400) \
#                                && bVeto \
#                                '
#
# 11 = e
# 13 = mu
# 15 = tau
