import math
import ROOT
from ROOT import RooArgSet
import bisect

muMass = 0.1057


class Properties:
    """Stores the min and max mass and the binning in pt"""
    def __init__(self, minMass, maxMass, ptBinsX, ptBinsY, triggerMatchDeltaR, NoBkgd, minDeltaR, scaleFactor):
        self.minMass = minMass
        self.maxMass = maxMass
        self.ptBinsX = ptBinsX
        self.ptBinsY = ptBinsY
        self.triggerMatchDeltaR = triggerMatchDeltaR
        self.NoBkgd = NoBkgd
        self.minDeltaR = minDeltaR
        self.scaleFactor = scaleFactor


def deltaPhi(phi1, phi2):
    result = phi1 - phi2;
    if result > math.pi: result -= 2*math.pi
    if result <= -math.pi: result += 2*math.pi
    return result

def delta_R(v1, v2):
    return math.sqrt(deltaPhi(v1.phi(), v2.phi())**2 + (v1.eta()-v2.eta())**2)

def deltaR(phi1, eta1, phi2, eta2):
    return math.sqrt(deltaPhi(phi1, phi2)**2 + (eta1-eta2)**2)

def passSelectionGlobalMuon(track):
    if ( track.pt > 26 and abs(track.eta) < 2) and track.isolation/track.pt < 0.1 and track.trackerLayersWithMeasurement >= 6  and abs(track.dxy) < 30. and abs(track.dz) < 30.:
#and track.trackQuality:
        return True

#Pass selection for tracks...
def passSelection(track):
    if ( track.pt > 26 and abs(track.eta) < 2) and track.isolation/track.pt < 0.1 and track.trackerLayersWithMeasurement >= 6 and abs(track.dxy) < 30. and abs(track.dz) < 30 and track.trackQuality:
        return True


# We need to check this later..
def passSelectionStandAlone(track):
    if ( track.pt > 17) and abs(track.eta) < 2.4 :
        return True

def passDileptonSelection(track1, track2, cosine):
    if track1.charge == track2.charge: return False
    if deltaR(track1.phi, track1.eta, track2.phi, track2.eta) < 0.2: return False
    if cosine <= -0.79: return False
    return True

def computeCosineAndMass(mu1, mu2):
    muon1 = ROOT.TLorentzVector()
    muon2 = ROOT.TLorentzVector()
    muon1.SetPtEtaPhiM(mu1.pt, mu1.eta, mu1.phi, muMass)
    muon2.SetPtEtaPhiM(mu2.pt, mu2.eta, mu2.phi, muMass)
    cosine = math.cos(muon1.Angle(muon2.Vect()))
    mass = (muon1+muon2).M()
    return (cosine, mass)

def fillTriggerMatchedTrack(track, triggerObjects, matchedTracks, p):
    for triggerMuon in triggerObjects:
        if (deltaR(triggerMuon.phi, triggerMuon.eta, track.phi, track.eta) < p.triggerMatchDeltaR):
            matchedTracks.append(track)
            return True

#def fillTriggerMatchedStandAlone(track, triggerObjects, matchedTracks, p):
#    for triggerMuon in triggerObjects:
#        if (deltaR(triggerMuon.phi, triggerMuon.eta, track.phi, track.eta) < p.triggerMatchDeltaR):
#            matchedTracks.append(track)
#            return True

#def fillTriggerMatchedGlobalMuon(track, triggerObjects, matchedTracks, p):
#    for triggerMuon in triggerObjects:
#        if (deltaR(triggerMuon.phi, triggerMuon.eta, track.phi, track.eta) < p.triggerMatchDeltaR):
#            matchedTracks.append(track)
#            return True

def fillSingleCandidate(mass, p, track1, track2, histoMap, datasetMap, gen_counting):
    cosineAndMass = computeCosineAndMass(track1, track2)
    if not passDileptonSelection(track1, track2, cosineAndMass[0]): return False
    if cosineAndMass[1] < p.minMass or cosineAndMass[1] > p.maxMass: return False
    mass.setVal(cosineAndMass[1])
    bins = find_bins(track1.pt, track2.pt, p.ptBinsX, p.ptBinsY)
    if bins[0] == -1 or bins[1] == -1: return False
    if track1.charge == track2.charge: return False
    histoMap[bins].Fill(mass.getVal())
    datasetMap[bins].add(RooArgSet(mass))
    gen_counting.Fill(track1.pt)
    return True

def fillCandidates(mass, properties, matchedTracks, histoMap, datasetMap):
    if len(matchedTracks) == 2:
        fillSingleCandidate(mass, properties, matchedTracks[0], matchedTracks[1], histoMap, datasetMap)

def fillCandidates_tnp(mass, properties, matchedTags, probes, histoMap, datasetMap, gen_counting):
    for tag in matchedTags:
        for probe in probes:
            if deltaR(tag.phi, tag.eta, probe.phi, probe.eta) > properties.minDeltaR :
                fillSingleCandidate(mass, properties, probe, tag, histoMap, datasetMap, gen_counting)

def find_bins(pt1, pt2, ptBinsX, ptBinsY):
    return (bisect.bisect_right(ptBinsX, pt1)-1, bisect.bisect_right(ptBinsY, pt2)-1)

def find_position(bin1, bin2, ptBinsX):
    return bin1+len(ptBinsX)*bin2

def find_position_NoOverflow(bin1, bin2, ptBinsX):
    return bin1+(len(ptBinsX)-1)*bin2

def buildName(baseName, ptBin1, ptBin2, ptBinsX, ptBinsY):
    return baseName+str(ptBinsX[ptBin1])+"_"+str(ptBinsY[ptBin2])

def buildNamePars(baseName, ptBin1, ptBin12, ptBin2, ptBin22, ptBinsX, ptBinsY):
    return baseName+str(ptBinsX[ptBin1])+"_"+str(ptBinsX[ptBin12])+"_"+str(ptBinsY[ptBin2])+"_"+str(ptBinsY[ptBin22])


def progressCounter(progress):
    output = ""
    print "\r"
    output += "["
    for i in range (0, 10):
        if i < progress/10: output += "====="
        else: output += "-----"
    output += "] " + str(progress) + "%"
    print output
