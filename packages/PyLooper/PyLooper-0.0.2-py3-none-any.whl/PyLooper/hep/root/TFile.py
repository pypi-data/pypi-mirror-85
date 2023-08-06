import uproot

from PyLooper.progressbar.ProgressReport import ProgressReport

class TFile(object):
    """Wrapper for root file"""
    def __init__(self,input_path,tree_path_in_file):
        self.input_path = input_path
        self.tree_path_in_file = tree_path_in_file

    def build(self):
        self.file = uproot.open(self.input_path)
        self.tree = self.file[self.tree_path_in_file]

    def loop(self,taskname,cfg,dataset,progressbar):
        report = ProgressReport(taskname,0,self.tree.numentries)
        batches = [cfg.entrysteps for i in range(int(self.tree.numentries/cfg.entrysteps))]+[self.tree.numentries%cfg.entrysteps]
        for m in cfg.modules:
            m.begin(dataset,cfg)
        for ibatch,data in enumerate(self.tree.iterate(dataset.branches, entrysteps=cfg.entrysteps,namedecode=cfg.namedecode,)):
            cfg.ibatch = batches[ibatch] 
            for m in cfg.modules:
                m.analyze(data,dataset,cfg)
            report.done += batches[ibatch]
            progressbar.present(report)
        for m in cfg.modules:
            m.end(dataset,cfg)
