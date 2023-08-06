import os,sys,importlib,time

from PyLooper.common.Analyzer import Analyzer

from PyLooper.progressbar.ProgressBar import ProgressBar

from PyLooper.utils.mkdir_p import mkdir_p

def read_cfg(path):
    spec = importlib.util.spec_from_file_location("configuration", path)
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    return cfg

# __________________________________________________________________________________________ ||
def loop():
    cfg = read_cfg(sys.argv[1])
    if cfg.verbose:
        print("Starting")
    start_time = time.time()
    
    cfg.collector.init_job()
    ana = Analyzer()
    progressbar = ProgressBar()
    ana.build_dataset(cfg)
    ana.loop(cfg,progressbar,)
    
    elapsed_time = time.time() - start_time
    print("Time used: "+str(elapsed_time)+"s")

# __________________________________________________________________________________________ ||
def train():
    cfg = read_cfg(sys.argv[1])
    if cfg.verbose:
        print("Starting")
    start_time = time.time()
    
    cfg.collector.init_job()
    ana = Analyzer()
    progressbar = ProgressBar()
    ana.build_training(cfg)
    ana.train(cfg,progressbar,)
    
    elapsed_time = time.time() - start_time
    print("Time used: "+str(elapsed_time)+"s")

# __________________________________________________________________________________________ ||
def sumup():
    cfg = read_cfg(sys.argv[1])
    if cfg.verbose:
        print("Starting")
    start_time = time.time()
    
    cfg.collector.init_job()
    ana = Analyzer()
    ana.build_dataset(cfg)
    ana.sumup(cfg)
    
    elapsed_time = time.time() - start_time
    print("Time used: "+str(elapsed_time)+"s")
