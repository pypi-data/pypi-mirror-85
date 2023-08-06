import os,pickle,copy,operator
import numpy as np
from functools import reduce

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from PyLooper.common.Module import Module

from PyLooper.utils.mkdir_p import mkdir_p 

class Plotter(Module):
    def begin(self,dataset,cfg):
        dataset.hist_dict = {}
        for p in cfg.plots:
            dataset.hist_dict[p] = copy.deepcopy(p.hist)

    def analyze(self,data,dataset,cfg):
        for p in cfg.plots:
            array_to_fill = p.array_func(data,dataset,cfg)
            event_weight_to_fill = p.event_weight_func(data,dataset,cfg) 
            if p.selection_func: event_weight_to_fill *= p.selection_func(dataset,dataset,cfg)
            dataset.hist_dict[p].fill(array_to_fill,event_weight_to_fill)

    def end(self,dataset,cfg):
        output_dir = self._create_pickle_dir(cfg,dataset) 
        mkdir_p(output_dir)
        for p in cfg.plots:
            f = open(self._create_pickle_path(cfg,dataset,p),"wb")
            pickle.dump(dataset.hist_dict[p],f)

    def _create_pickle_dir(self,cfg,dataset):
        return os.path.join(cfg.collector.output_path,dataset.name)

    def _create_pickle_path(self,cfg,dataset,p):
        return os.path.join(self._create_pickle_dir(cfg,dataset),p.name+".p")

    def _read_pickle_hist(self,cfg,p):
        for d in cfg.dataset_list:
            d.hist = pickle.load(open(self._create_pickle_path(cfg,d,p),"rb"))

    def sumup(self,cfg):
        for p in cfg.plots:
            self._read_pickle_hist(cfg,p)
            if cfg.merged_dataset_list:
                self.add_dataset(cfg,p)
                mc_list = [d for d in cfg.merged_dataset_list if d.isMC and not d.isSignal]
            else:
                mc_list = [d for d in cfg.dataset_list if d.isMC and not d.isSignal]
            data_list = [d for d in cfg.dataset_list if d.isData]
            signal_list = [d for d in cfg.dataset_list if d.isSignal]
            if mc_list and data_list and p.dim == 1:
                self.plot_data_mc_1d(cfg,mc_list,data_list,signal_list,p)
            elif mc_list and not data_list and p.dim == 1:
                self.plot_mc_1d(cfg,mc_list,signal_list,p)
            else:
                raise RuntimeError

    def add_dataset(self,cfg,p):
        if cfg.merged_dataset_list:
            for mc in cfg.merged_dataset_list:
                mc.hist = reduce(operator.add,[d.hist for d in mc.sample_list])

    def make_mc_array_1d(self,mc_list):
        mc_bin_content = np.concatenate([mc.hist.numpy_content for mc in mc_list],axis=1)
        mc_bin_error2 = np.concatenate([mc.hist.numpy_error2 for mc in mc_list],axis=1)
        mc_bin_edges = np.concatenate([mc.hist.numpy_edges for mc in mc_list],axis=1)
        mc_bin_centers = np.concatenate([mc.hist.numpy_centers for mc in mc_list],axis=1)
        return mc_bin_content,mc_bin_error2,mc_bin_edges,mc_bin_centers

    def make_data_array_1d(self,data_list):
        data_bin_content = np.concatenate([data.hist.numpy_content for data in data_list],axis=1)
        data_bin_edges = data_list[0].hist.numpy_edges
        data_bin_centers = data_list[0].hist.numpy_centers
        data_total_bin_content = np.sum(data_bin_content,axis=1)
        return data_bin_content,data_bin_edges,data_bin_centers

    def plot_mc_1d(self,cfg,mc_list,signal_list,p):
        plt.clf()

        fig = plt.figure(constrained_layout=False,figsize=(10,13),)
        gs = fig.add_gridspec(10,1)
        
        mc_bin_content,mc_bin_error2,mc_bin_edges,mc_bin_centers = self.make_mc_array_1d(mc_list)

        plt.hist(mc_bin_centers, bins=mc_bin_edges[:,0], weights=mc_bin_content,stacked=True,label=[mc.plot_name+": {:.2f}".format(np.sum(mc.hist.content),) for mc in mc_list])
                        
        for sig in signal_list:
            plt.hist(sig.hist.numpy_centers, bins=sig.hist.numpy_edges[:,0], weights=sig.hist.numpy_content,label=sig.plot_name+": {:.2f}".format(np.sum(sig.hist.content),),histtype='step',linewidth=2,)
        plt.legend(loc='best')

        output_path = os.path.join(cfg.collector.output_path,p.name+".png")
        fig.savefig(output_path)

    def plot_data_mc_1d(self,cfg,mc_list,data_list,signal_list,p,):
        plt.clf()

        fig = plt.figure(constrained_layout=False,figsize=(10,13),)
        gs = fig.add_gridspec(10,1)
        ax1 = fig.add_subplot(gs[:7,:])
        ax2 = fig.add_subplot(gs[7:,:])

        nbins = mc_list[0].hist.nbins
    
        mc_bin_content,mc_bin_error2,mc_bin_edges,mc_bin_centers = self.make_mc_array_1d(mc_list)

        data_bin_content,data_bin_edges,data_bin_centers = self.make_data_array_1d(data_list)
        data_total_bin_content = np.sum(data_bin_content,axis=1)
 
        ax1.hist(mc_bin_centers, bins=mc_bin_edges[:,0], weights=mc_bin_content,stacked=True,label=[mc.plot_name+": {:.2f}".format(np.sum(mc.hist.content),) for mc in mc_list])
        data_bin_error = self.make_data_error(data_total_bin_content) 
        ax1.errorbar(data_bin_centers, data_total_bin_content, yerr=data_bin_error, marker=".", linestyle="None", color=p.data_color,label="Data: "+str(int(np.sum(data_total_bin_content))),)

        for sig in signal_list:
            ax1.hist(sig.hist.numpy_centers, bins=sig.hist.numpy_edges[:,0], weights=sig.hist.numpy_content,label=sig.plot_name+": {:.2f}".format(np.sum(sig.hist.content),),histtype='step',linewidth=2,)
        ax1.legend(loc='best')
        
        ratio,ratioerr = self.make_data_mc_ratio(mc_bin_content,data_total_bin_content,data_bin_error,)
        ax2.errorbar(data_bin_centers,ratio,yerr=ratioerr,marker=".",linestyle="None", color=p.data_color,)
        ax2.set_xlim(ax1.get_xlim())
        ax2.set_ylim(0.,2.)
        start, end = ax2.get_ylim()
        ax2.yaxis.set_ticks(np.arange(start, end, 0.25))
        ax2.grid()
        
        output_path = os.path.join(cfg.collector.output_path,p.name+".png")
        fig.savefig(output_path)

    def make_data_error(self,data_total_bin_content):
        return np.sqrt(data_total_bin_content)

    def make_data_mc_ratio(self,mc_bin_content,data_total_bin_content,data_bin_error,):
        mc_total_bin_content = np.sum(mc_bin_content,axis=1)
        ratio = data_total_bin_content/mc_total_bin_content
        ratio[ratio == np.inf] = 0.
        data_rel_bin_error = 1./data_bin_error
        data_rel_bin_error[data_rel_bin_error == np.inf] = 0.
        ratioerr = ratio * data_rel_bin_error 
        return ratio,ratioerr
