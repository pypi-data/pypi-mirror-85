import uproot
import numpy as np

class ROOTWrapper(object):
    def __init__(self,input_path_dict,tree_path_in_file):
        self.input_path_dict = input_path_dict
        self.tree_path_in_file = tree_path_in_file

    def build(self):
        self.file_dict = {k: uproot.open(input_path) for k,input_path in self.input_path_dict.items()}
        self.tree_dict = {k: f[self.tree_path_in_file] for k,f in self.file_dict.items()}

    def get(self,iepoch,cfg):
        entrystart_dict = {k: np.random.randint(0,t.numentries-cfg.batch_per_tree) for k,t in self.tree_dict.items()}
        return [self.tree_dict[k].pandas.df(branches=cfg.branches,entrystart=entrystart,entrystop=entrystart+cfg.batch_per_tree) for k,entrystart in entrystart_dict.items()]
        
