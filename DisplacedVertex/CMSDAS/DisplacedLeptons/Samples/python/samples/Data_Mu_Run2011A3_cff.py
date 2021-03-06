sampleDataSet = '/DoubleMu/Run2011A-05Aug2011-v1/AOD'
sampleNumEvents = 5824586 # according to DBS, as of 24 Nov 2011

# global tag needs to be chosen to match release, trigger menu and alignment conditions.
# see https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions
sampleGlobalTag = 'GR_R_42_V21A::All'
sampleHLTProcess = '*'

# data quality run/lumi section selection
sampleJSON = "https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions11/7TeV/Reprocessing/Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_MuonPhys_v2.txt"

# restrict run range (mainly to get a sample with consistent trigger configuration)
sampleRunRange = [160000,999999]

# use checkAllFilesOpened whenever possible, and noDuplicateCheck when necessary
sampleDuplicateCheckMode = "checkAllFilesOpened"

# "DATA" or "MC"
sampleType = "DATA"

sampleRelease = "CMSSW_4_2_7" # original (i.e. RECO file) release,
                              # not the one we plan to process them with

sampleProcessRelease = "CMSSW_4_2_7" # release used to create new files with

sampleBaseDir = "root://xrootd.rcac.purdue.edu//store/user/demattia/longlived/"+sampleProcessRelease+"/Data_Mu_Run2011A3"

sampleRecoFiles = []

samplePatFiles = [
  sampleBaseDir+"/pat/PATtuple_1_1_IBy.root",
  sampleBaseDir+"/pat/PATtuple_2_1_lml.root",
  sampleBaseDir+"/pat/PATtuple_3_1_uFy.root",
  sampleBaseDir+"/pat/PATtuple_4_1_Rqz.root",
  sampleBaseDir+"/pat/PATtuple_5_1_33u.root",
  sampleBaseDir+"/pat/PATtuple_6_1_rzQ.root",
  sampleBaseDir+"/pat/PATtuple_7_1_Mxq.root",
  sampleBaseDir+"/pat/PATtuple_8_1_KxL.root",
  sampleBaseDir+"/pat/PATtuple_9_1_bWP.root",
  sampleBaseDir+"/pat/PATtuple_10_1_wtI.root",
  sampleBaseDir+"/pat/PATtuple_11_1_AaD.root",
  sampleBaseDir+"/pat/PATtuple_12_1_my7.root",
  sampleBaseDir+"/pat/PATtuple_13_1_Pk4.root",
  sampleBaseDir+"/pat/PATtuple_14_1_5VE.root",
  sampleBaseDir+"/pat/PATtuple_15_1_XZe.root",
  sampleBaseDir+"/pat/PATtuple_16_1_C6V.root",
  sampleBaseDir+"/pat/PATtuple_17_1_lbL.root",
  sampleBaseDir+"/pat/PATtuple_18_1_r8D.root",
  sampleBaseDir+"/pat/PATtuple_19_1_o4A.root",
  sampleBaseDir+"/pat/PATtuple_20_1_Cw7.root",
  sampleBaseDir+"/pat/PATtuple_21_1_UIa.root",
  sampleBaseDir+"/pat/PATtuple_22_1_Ryf.root",
  sampleBaseDir+"/pat/PATtuple_23_1_8Dc.root",
  sampleBaseDir+"/pat/PATtuple_24_1_zow.root",
  sampleBaseDir+"/pat/PATtuple_25_1_C33.root",
  sampleBaseDir+"/pat/PATtuple_26_1_fQz.root",
  sampleBaseDir+"/pat/PATtuple_27_1_4r1.root",
  sampleBaseDir+"/pat/PATtuple_28_1_Ehe.root",
  sampleBaseDir+"/pat/PATtuple_29_1_GPb.root",
  sampleBaseDir+"/pat/PATtuple_30_1_qxV.root",
  sampleBaseDir+"/pat/PATtuple_31_1_iKz.root",
  sampleBaseDir+"/pat/PATtuple_32_1_qB4.root",
  sampleBaseDir+"/pat/PATtuple_33_1_Ffw.root",
  sampleBaseDir+"/pat/PATtuple_34_1_K63.root",
  sampleBaseDir+"/pat/PATtuple_35_1_yhQ.root",
  sampleBaseDir+"/pat/PATtuple_36_1_uaG.root",
  sampleBaseDir+"/pat/PATtuple_37_1_j5h.root",
  sampleBaseDir+"/pat/PATtuple_38_1_71v.root",
  sampleBaseDir+"/pat/PATtuple_39_1_zrT.root",
  sampleBaseDir+"/pat/PATtuple_40_1_E2a.root",
  sampleBaseDir+"/pat/PATtuple_41_1_VCc.root",
  sampleBaseDir+"/pat/PATtuple_42_1_Cqr.root",
  sampleBaseDir+"/pat/PATtuple_43_1_7xL.root",
  sampleBaseDir+"/pat/PATtuple_44_1_H2M.root",
  sampleBaseDir+"/pat/PATtuple_45_1_bP5.root",
  sampleBaseDir+"/pat/PATtuple_46_1_0zd.root",
  sampleBaseDir+"/pat/PATtuple_47_1_jDe.root",
  sampleBaseDir+"/pat/PATtuple_48_1_7t9.root",
  sampleBaseDir+"/pat/PATtuple_49_1_mKz.root",
  sampleBaseDir+"/pat/PATtuple_50_1_4ZL.root",
  sampleBaseDir+"/pat/PATtuple_51_1_CKP.root",
  sampleBaseDir+"/pat/PATtuple_52_1_xca.root",
  sampleBaseDir+"/pat/PATtuple_53_1_gYd.root",
  sampleBaseDir+"/pat/PATtuple_54_1_D8i.root",
  sampleBaseDir+"/pat/PATtuple_55_1_LA4.root",
  sampleBaseDir+"/pat/PATtuple_56_1_GWd.root",
  sampleBaseDir+"/pat/PATtuple_57_1_4Ot.root",
  sampleBaseDir+"/pat/PATtuple_58_1_cYY.root",
  sampleBaseDir+"/pat/PATtuple_59_1_rtX.root",
  sampleBaseDir+"/pat/PATtuple_60_1_hKL.root",
  sampleBaseDir+"/pat/PATtuple_61_1_X6j.root",
  sampleBaseDir+"/pat/PATtuple_62_1_qmP.root",
  sampleBaseDir+"/pat/PATtuple_63_1_cMx.root",
  sampleBaseDir+"/pat/PATtuple_64_1_nJ1.root",
  sampleBaseDir+"/pat/PATtuple_65_1_pfa.root",
  sampleBaseDir+"/pat/PATtuple_66_1_xjE.root",
  sampleBaseDir+"/pat/PATtuple_67_1_WmX.root",
  sampleBaseDir+"/pat/PATtuple_68_1_bZn.root",
  sampleBaseDir+"/pat/PATtuple_69_1_laH.root",
  sampleBaseDir+"/pat/PATtuple_70_1_JEQ.root",
  sampleBaseDir+"/pat/PATtuple_71_1_xEE.root",
  sampleBaseDir+"/pat/PATtuple_72_1_2wW.root",
  sampleBaseDir+"/pat/PATtuple_73_1_2JW.root",
  sampleBaseDir+"/pat/PATtuple_74_1_XtT.root",
  sampleBaseDir+"/pat/PATtuple_75_1_qIW.root",
  sampleBaseDir+"/pat/PATtuple_76_1_VMt.root",
  sampleBaseDir+"/pat/PATtuple_77_1_erI.root",
  sampleBaseDir+"/pat/PATtuple_78_1_w28.root",
  sampleBaseDir+"/pat/PATtuple_79_1_hMh.root",
  sampleBaseDir+"/pat/PATtuple_80_1_xwI.root",
  sampleBaseDir+"/pat/PATtuple_81_1_2J9.root",
  sampleBaseDir+"/pat/PATtuple_82_1_cIQ.root",
  sampleBaseDir+"/pat/PATtuple_83_1_2gG.root",
  sampleBaseDir+"/pat/PATtuple_84_1_yV3.root",
  sampleBaseDir+"/pat/PATtuple_85_1_SMK.root",
  sampleBaseDir+"/pat/PATtuple_86_1_stM.root",
  sampleBaseDir+"/pat/PATtuple_87_1_NEM.root",
  sampleBaseDir+"/pat/PATtuple_88_1_qcv.root"
]
