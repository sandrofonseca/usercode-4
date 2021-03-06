// -*- C++ -*-
//
// Package:    AlgValidator
// Class:      AlgValidator
//
// Code extracted from Roberto.cc, 02/04/08 R.Casagrande
//
/**\class AlgValidator AlgValidator.cc AnalysisExamples/AlgValidator/src/AlgValidator.cc

Description: <one line class summary>

*/
//
// $Id: AlgValidator.h
//
//

// System include files
// --------------------
#include <memory>
#include <vector>

// User include files
// ------------------
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

// Root include files
// ------------------
#include "TH1D.h"
#include "TH2F.h"
#include "TProfile.h"
#include "TFile.h"

//=====ROBERTO===================
//-------------------------
//tracce e vertici
//-------------------------

// For the SimVertex
#include "SimDataFormats/Vertex/interface/SimVertex.h"
#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"

//For the SimTracks
#include "SimDataFormats/Track/interface/SimTrack.h"
#include "SimDataFormats/Track/interface/SimTrackContainer.h"

// GenJets
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/JetReco/interface/GenJet.h"

// Data include files
// ------------------

#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"

#include "DataFormats/TrackReco/interface/TrackBase.h"

//=====ROBERTO==============================

// Associator for the jets
// -----------------------
#include "AnalysisExamples/AnalysisClasses/interface/AssociatorEt.h"


// Class declaration
// -----------------
class AlgValidator : public edm::EDAnalyzer {
public:
  explicit AlgValidator(const edm::ParameterSet&);
  ~AlgValidator();


private:
  virtual void beginJob(const edm::EventSetup&) ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
 
 
  int eventcounter_;

  // Declare as static so that only one exists, even if more
  // than one AlgValidator object is created
  // -------------------------------------------------------
  
  edm::ParameterSet conf_;
  TFile* OutputFile;

  // Declare here, since it does not have a default constructor
  // it will be initialized with an initialization list ( in
  // the AlgValidator constructor ).
  //  HiVariables HiVar;

  // Use a dynamic construction, or the TFile problem will crash the job
  // when moving from one input file to another.
  // The histograms must be created after the TFile is opened.
 
  
  edm::InputTag offlineJetLabel_;
  edm::InputTag offlineMEtLabel_;
  edm::InputTag MCParticleLabel_;
  
  //======ROBERTO==============
  
  //------------------------
  //tracce e vertici
  //------------------------
  edm::InputTag simVtxLabel_;
  edm::InputTag simTkLabel_;
  edm::InputTag simPUVtxLabel_;
  std::string impactParameterTagInfos;
  edm::InputTag vtxSample_;
  //  edm::InputTag genJetsLabel_;
  bool SIM_;
  //======ROBERTO==============
  
  bool QCD_;
  std::string OutputEffFileName;

  //=====ROBERTO============
  
  //Histograms for Njet  
  TH1D * H_NJet_withTracks_;
  TH1D * H_NJet_withNoTracks_;
  
  //Histogram Z jet 
  TH1D * H_ZJetWAvg_;
  TH1D * H_ZJetWAvgError_;
  //Histograms for Dz jet - vertices 
  TH1D * H_Vmin_;
  TH1D * H_DzJetVtxWAvg_;
  TH1D * H_DzJetVtxWAvg2Best_;
  TH2D * H_DzJetVtxWAvg_vs_2Best_;
 
  //Histograms of Z jet and error after the rejection algorithm (5 sigma)
  TH1D *  H_ZJet_RJAlg_;
  TH1D *  H_ZErrorJet_RJAlg_;
  //Histograms for Dz jet - vertices 
  TH1D *  H_idRJAlg_;
  TH1D *  H_DzJetVtx_RJAlg_;
  TH1D *  H_Dz2JetVtx_RJAlg_;
  TH2D *  H_DzJetVtx_RJAlg_vs_2Best_;

  TH1D *  H_P1P2_;

  TH2D *  H_pVsp_ ;

  TH1D *  H_nVtxMap_;
  TH1D *  H_nVtxMapRJAlg_;
  TH1D *  H_nVtxMapSAAlg_;
  TH1D *  H_nVtxMapProbEval_;

  TH1D *  H_ProbRJAlg_;

  TH1D *  H_ProbAfterFAAlg_;

  TH1D * H_ProbAfterSAAlg_;

  TH1D *  H_idVtxFAAlg_;
  TH1D *  H_idVtxSAAlg_;

  TH1D *  H_DzAfterSAAlg_;

  TH1D * H_nTrack_RJAlg_;

  TH2D *  H_nJMaxVsNjTot_SAAlg_;

  TH2D *  H_nJMaxVsNjTot_RJAlg_;

  TH2D * H_nTkRJAlgVSzJetError_;
  TH2D * H_nTkRJAlgVSzJet_;

  TH1D * H_nJet_;

  TH1D * H_nJMax_SAAlg_;
  TH1D * H_nJMax_RJAlg_;
  TH1D * H_nJMax_BeforeAlg_ ;
  TH1D * H_nJMax_ProbEval_;

  TH1D * H_VtxMinDz_;

  TProfile *  H_ProfileVtxVsNjBeforeAlg_;
  TProfile *  H_ProfileVtxVsNjRJAlg_;
  TProfile *  H_ProfileVtxVsNjSAAlg_;
  TProfile *  H_ProfileVtxVsNjProbEval_;

  TH1D *  H_ZVtx_;
  TH1D *  H_ZVtxError_;

  TH1D *  H_DzAfterProbEval_;

  TH2D * H_ZBeforevsAfterRJAlg_;

  TH2D * H_ZPvVsZBeforeAlg_;
  TH2D * H_ZPvVsZRJAlg_;
  TH2D * H_ZPvVsZProbEval_;

  TH2D * H_ZPvVsZRecoBeforeAlg_;
  TH2D * H_ZPvVsZRecoRJAlg_;
  TH2D * H_ZPvVsZRecoProbEval_;

  TH2D * H_ZjetSimVsReco_;		
  TH1D * H_dzVtxSimRecoBeforeAlg_;	
  TH2D * H_dzVtxSimRecoBeforeAlgVsNtk_;	
  TH2D * H_ZjetSimVsReco_RJAlg_;	
  TH1D * H_dzVtxSimRecoRJAlg_;		
  TH2D * H_dzVtxSimRecoRJAlgVsNtk_;	
  TH1D * H_dzVtxSimRecoProbEval_;        

  TH1D * H_dzVtxHMSimRecoProbEval_;
  TH1D * H_dzVtxHMSimRecoBeforeAlg_;
  TH1D * H_dzVtxHMSimRecoRJAlg_;


  TH2D *  H_nJSimVsnJRecoVtxHMProbEval_;
  TH2D *  H_nJSimVsnJRecoVtxHMBeforeAlg_;
  TH2D *  H_nJSimVsnJRecoVtxHMRJAlg_;

  TH2D * H_nJSimVsnJRecoVtxHMProbEvalWeighted_;
  TH2D * H_nJSimVsnJRecoVtxHMBeforeAlgWeighted_;
  TH2D * H_nJSimVsnJRecoVtxHMRJAlgWeighted_;

  //=====ROBERTO============

  float loose_;
  float medium_;
  float tight_;

  std::vector<double> pMatrixSing25_;
  std::vector<double> pMatrix25_;
};
