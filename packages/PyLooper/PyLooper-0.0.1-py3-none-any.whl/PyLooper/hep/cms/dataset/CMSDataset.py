import numpy as np
import uproot

from PyLooper.common.dataset import Dataset

class CMSDataset(Dataset):
    def __init__(self,name,componentList,xs=None,sumw=None,isMC=True,isSignal=False,lumi=None,plot_name=None,skip_weight=False,branches=[]):
        self.name = name
        self.componentList = componentList
        self.xs = xs
        self.lumi = lumi
        self.sumw = sumw
        self.isMC = isMC
        self.isData = not isMC
        self.isSignal = isSignal
        self.skip_weight = skip_weight
        self.plot_name = self.name if not plot_name else plot_name
        self.branches = branches

    def read_sumw_by_text_file(self,text_file_path):
        f = open(text_file_path,"r")
        l = f.readlines()[0]
        self.sumw = float(l.split()[0])
    
    def read_sumw_by_hist(self,text_file_path,hist_path):
        f = uproot.open(text_file_path)
        self.sumw = np.sum(f[hist_path])
