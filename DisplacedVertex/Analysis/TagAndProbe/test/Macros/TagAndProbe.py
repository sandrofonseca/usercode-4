import ROOT
from utils import *
# import math
from ROOT import RooRealVar, RooFormulaVar, RooVoigtian, RooChebychev, RooArgList, RooArgSet, \
    RooAddPdf, RooDataSet, RooCategory, RooSimultaneous, RooGenericPdf, RooWorkspace
import Workspace
from array import array 
ROOT.gROOT.LoadMacro("Loader.C++")
ROOT.gROOT.SetBatch(True)


# --------#


MC = True
NoBkgd = True

# Use this for data to take into account the prescale of the trigger
if MC:
    scaleFactor = 1
else:
    scaleFactor = 0.05


# --------#


# Define binning
ptBinsX = [15, 20, 23, 26, 30, 35, 40, 45, 50, 60, 70]
#ptBinsX = [50, 55, 60, 65, 70]
#ptBinsY = [26, 30, 35, 40, 45, 50, 60, 70]
# ptBinsX = [15, 70]
ptBinsY = [20, 10000]

# Define cuts and some useful variables
triggerMatchDeltaR = 0.1
minMass = 10
maxMass = 150
minDeltaR = 0.2
p = Properties(minMass, maxMass, ptBinsX, ptBinsY, triggerMatchDeltaR, NoBkgd, minDeltaR, scaleFactor)


# Trigger efficiency for new trigger over old trigger
tagTrigger = "IsoMu24"
probeTrigger = "HLT_L2DoubleMu23_NoVertex_v"

# Load the input file
tree = ROOT.TChain("T")
tree.Add("/afs/cern.ch/user/d/demattia/work/DisplacedLeptons/TagAndProbe/CMSSW_5_3_8/src/Analysis/TagAndProbe/test/crab_0_140222_011555/res/tagAndProbeA.root")

# Prepare the workspace
ws = RooWorkspace("ws", "workspace")
Workspace.buildPdf(ws, p)

mass = ws.var("mass")
sample = ws.cat("sample")
simPdf = ws.pdf("simPdf")
efficiency = ws.var("efficiency")
meanB = ws.var("meanB")

# Prepare datasets
datasetAllMap = {}
datasetPassMap = {}
hAllMap = {}
hPassMap = {}
for ptBin1 in range(0, len(ptBinsX)):
    for ptBin2 in range(0, len(ptBinsY)):
        datasetAllMap[(ptBin1, ptBin2)] = RooDataSet(buildName("datasetAll_", ptBin1, ptBin2, ptBinsX, ptBinsY), buildName("datasetAll_", ptBin1, ptBin2, ptBinsX, ptBinsY), RooArgSet(mass))
        datasetPassMap[(ptBin1, ptBin2)] = RooDataSet(buildName("datasetPass_", ptBin1, ptBin2, ptBinsX, ptBinsY), buildName("datasetPass_", ptBin1, ptBin2, ptBinsX, ptBinsY), RooArgSet(mass))
        hAllMap[(ptBin1,ptBin2)] = ROOT.TH1F(buildName("hAll_", ptBin1, ptBin2, ptBinsX, ptBinsY), buildName("All events passing old trigger ", ptBin1, ptBin2, ptBinsX, ptBinsY), 100, 60, 120)
        hPassMap[(ptBin1,ptBin2)] = ROOT.TH1F(buildName("hPass_", ptBin1, ptBin2, ptBinsX, ptBinsY), buildName("All events passing old trigger and new trigger ", ptBin1, ptBin2, ptBinsX, ptBinsY), 100, 60, 120)
#Prepare 1D histogram to get the ratio of number of passing probes over all probes muons

counting_all = ROOT.TH1F("counting_all","counting_all", len(ptBinsX)-1, array('d',ptBinsX))
counting_pass = ROOT.TH1F("counting_pass","counting_pass",len(ptBinsX)-1, array('d',ptBinsX))
counting_eff = ROOT.TH1F("counting_eff_SA_MC_probe_negative","counting_eff", len(ptBinsX)-1,  array('d',ptBinsX))
counting_eff.GetXaxis().SetTitle("Probe muon p_{T} [GeV]")
counting_eff.GetYaxis().SetTitle("Number of Passing Probes/Number of All Probes")

# Event loop
allCandidates = 0
passCandidates = 0

processedEvents = 0

totEvents = 50000
# totEvents = tree.GetEntries()
print "total number of events analyzed is", totEvents
progress = 0



for event in tree:
    if processedEvents > totEvents:
        break
    processedEvents += 1

    if int(float(processedEvents)/float(totEvents)*100) % 10 == 0 and int(float(processedEvents)/float(totEvents)*100) > progress:
        progress = 100*processedEvents/totEvents
        progressCounter(progress)
    if processedEvents == totEvents - 1:
        progressCounter(100);


    # Get the trigger outcome for this event
    tagTriggerFired = False
    probeTriggerFired = False
    for name in event.triggerNames:
        if name.find(tagTrigger) != -1: tagTriggerFired = True
    # If none of the two triggers fired we can skip the event
    if not tagTriggerFired :
        continue

    # IsoMu24 filter name
    tagTriggerObjects = event.hltL3crIsoL1sMu16L1f0L2f16QL3f24QL3crIsoRhoFiltered0p15Objects
    # DoubelMu23NoVertex filter name
    probeTriggerObjects = event.hltL2DoubleMu23NoVertexL2PreFilteredObjects

    matchedMuonsTagTrigger = []
    passingMuonsProbe = []
    allMuonsProbe = []

    for muon in event.muons:
        # Find a matching trigger object in DeltaR
        if passSelectionGlobalMuon(muon):
            fillTriggerMatchedTrack(muon, tagTriggerObjects, matchedMuonsTagTrigger, p)

    for standAloneMuon in event.refittedStandAloneMuons:
        if passSelectionStandAlone(standAloneMuon):
            fillTriggerMatchedTrack(standAloneMuon, probeTriggerObjects, passingMuonsProbe, p)
            allMuonsProbe.append(standAloneMuon)


    fillCandidates_tnp(mass, p, matchedMuonsTagTrigger, passingMuonsProbe, hPassMap, datasetPassMap, counting_pass)
    fillCandidates_tnp(mass, p, matchedMuonsTagTrigger, allMuonsProbe, hAllMap, datasetAllMap, counting_all)

#print "all candidates =", hAllMap[1,1].GetEntries()
# print "pass candidates =", hPassMap[1,1].GetEntries()
for i in range(0, len(ptBinsX)):
    print "all candidates =", hAllMap[i,0].GetEntries()
    print "pass candidates =", hPassMap[i,0].GetEntries()
# print "all candidates =", hAllMap[0,0].GetEntries()
# print "pass candidates =", hPassMap[0,0].GetEntries()

#Define a canvas to see superimposed deltaR distribution...
canvas = ROOT.TCanvas("AllAndPassCanvas", "AllAndPassCanvas", 800, 800)
canvas.Divide(len(ptBinsX),len(ptBinsY))
for ptBin1 in range(0, len(ptBinsX)):
    for ptBin2 in range(0, len(ptBinsY)):
        canvas.cd(find_position(ptBin1, ptBin2, ptBinsX)+1)
        hAllMap[(ptBin1, ptBin2)].Draw()
        hPassMap[(ptBin1, ptBin2)].Draw("same")
        hPassMap[(ptBin1, ptBin2)].SetLineColor(2)

canvas.Print("AllAndPassCanvas.pdf")

# Plot the fit results

def plotResults(ptBin1, ptBin2, combData, canvas2, canvas3):
    frame1 = mass.frame(ROOT.RooFit.Bins(30),ROOT.RooFit.Title("All events"))
    # Plot all data tagged as physics sample
    combData.plotOn(frame1,ROOT.RooFit.Cut("sample==sample::all"))
    # Plot "physics" slice of simultaneous pdf.
    # NBL You _must_ project the sample index category with data using ProjWData
    # as a RooSimultaneous makes no prediction on the shape in the index category
    # and can thus not be integrated
    simPdf.plotOn(frame1, ROOT.RooFit.Slice(sample,"all"), ROOT.RooFit.ProjWData(RooArgSet(sample),combData))
    simPdf.plotOn(frame1, ROOT.RooFit.Slice(sample,"all"), ROOT.RooFit.Components("backgroundAll"), ROOT.RooFit.ProjWData(RooArgSet(sample),combData), ROOT.RooFit.LineStyle(ROOT.kDashed))

    # The same plot for the control sample slice
    frame2 = mass.frame(ROOT.RooFit.Bins(30),ROOT.RooFit.Title("Passing events"))
    combData.plotOn(frame2,ROOT.RooFit.Cut("sample==sample::pass"))
    simPdf.plotOn(frame2,ROOT.RooFit.Slice(sample,"pass"),ROOT.RooFit.ProjWData(RooArgSet(sample),combData))
    simPdf.plotOn(frame2,ROOT.RooFit.Slice(sample,"pass"),ROOT.RooFit.Components("backgroundPass"),ROOT.RooFit.ProjWData(RooArgSet(sample),combData),ROOT.RooFit.LineStyle(ROOT.kDashed))

    canvas2.cd(find_position(ptBin1, ptBin2, ptBinsX)+1)
    frame1.GetYaxis().SetTitleOffset(1.4)
    frame1.Draw()
    frame1.SetName(buildNamePars("fitAll_", ptBin1, ptBin1+1, ptBin2, ptBin2+1, ptBinsX, ptBinsY))
    frame1.SaveAs(buildNamePars("fitAll_", ptBin1, ptBin1+1, ptBin2, ptBin2+1, ptBinsX, ptBinsY)+".root")

    canvas3.cd(find_position(ptBin1, ptBin2, ptBinsX)+1)
    frame2.GetYaxis().SetTitleOffset(1.4)
    frame2.Draw()
    frame2.SetName(buildNamePars("fitPass_", ptBin1, ptBin1+1, ptBin2, ptBin2+1, ptBinsX, ptBinsY))
    frame2.SaveAs(buildNamePars("fitPass_", ptBin1, ptBin1+1, ptBin2, ptBin2+1, ptBinsX, ptBinsY)+".root")


# After filling the datasets, build the combined dataset
combDataMap = {}
frMap = {}

from array import array
hEff = ROOT.TH2D("hEff", "hEff", len(ptBinsX)-1, array('d',ptBinsX), len(ptBinsY)-1, array('d',ptBinsY))
hEff1D = ROOT.TH1D("hEff1D", "hEff1D", len(ptBinsX)-1, array('d',ptBinsX))

# Canvases for fit results
canvas2 = ROOT.TCanvas("RooFitCanvas", "RooFitCanvas", 800, 800)
canvas2.Divide(len(ptBinsX),len(ptBinsY))
canvas3 = ROOT.TCanvas("RooFitCanvasPass", "RooFitCanvasPass", 800, 800)
canvas3.Divide(len(ptBinsX),len(ptBinsY))

# Construct combined dataset in (x,sample) and perform simultaneous fit
# Skip the last, overflow, bin from fitting to save time. It does not appear in the final plots.
# Note that the following code assumes an extra bin to build the name of the output file.
for ptBin1 in range(0, len(ptBinsX)-1):
    for ptBin2 in range(0, len(ptBinsY)-1):
        combDataMap[(ptBin1, ptBin2)] = RooDataSet("combData"+"_"+str(ptBin1)+"_"+str(ptBin2),"combined data "+str(ptBin1)+"_"+str(ptBin2),
                                                   RooArgSet(mass),ROOT.RooFit.Index(sample),
                                                   ROOT.RooFit.Import("all",datasetAllMap[(ptBin1, ptBin2)]),
                                                   ROOT.RooFit.Import("pass",datasetPassMap[(ptBin1, ptBin2)]))
        #meanB.setRange(ptBinsX[ptBin1]+ptBinsY[ptBin2], ptBinsX[ptBin1+1]+ptBinsY[ptBin2+1])
        #meanB.setVal((ptBinsX[ptBin1]+ptBinsY[ptBin2]+ptBinsX[ptBin1+1]+ptBinsY[ptBin2+1])/2)
        frMap[(ptBin1, ptBin2)] = simPdf.fitTo(combDataMap[(ptBin1,ptBin2)], ROOT.RooFit.Save(ROOT.kTRUE), ROOT.RooFit.Extended(ROOT.kTRUE), ROOT.RooFit.NumCPU(4))
        # Use this for minos (better error estimate, but takes longer)
        frMap[(ptBin1, ptBin2)].Print("v")
        simPdf.getParameters(combDataMap[(ptBin1, ptBin2)]).writeToFile(buildNamePars("parameters_", ptBin1, ptBin1+1, ptBin2, ptBin2+1, ptBinsX, ptBinsY)+".txt")
        hEff.SetBinContent(ptBin1+1, ptBin2+1, efficiency.getVal())
        hEff.SetBinError(ptBin1+1, ptBin2+1, efficiency.getError())
        hEff1D.SetBinContent(ptBin1+1, efficiency.getVal())
        hEff1D.SetBinError(ptBin1+1, efficiency.getError())
        plotResults(ptBin1, ptBin2, combDataMap[(ptBin1,ptBin2)], canvas2, canvas3)

canvas2.Print("RooFitCanvas.pdf")
canvas3.Print("RooFitCanvasPass.pdf")

canvas4 = ROOT.TCanvas("efficiency", "efficiency", 800, 800)
hEff.Draw("COLZTEXTE")
canvas4.Print("Efficiency.pdf")
canvas5 = ROOT.TCanvas("efficiency1D", "efficiency1D", 600, 600)
hEff1D.Draw()
canvas5.Print("Efficiency1D.pdf")
