class Analyzer(object):
    def __init__(self):
        self.header = "*"*100
        pass

    def build_dataset(self,cfg):
        self.dataset_list = cfg.dataset_list
        if cfg.verbose:
            print(self.header)
            print("Building dataset: ")
        for d in self.dataset_list:
            if cfg.verbose:
                print(d.name,len(d.componentList),"files")
            for c in d.componentList:
                c.build()
        if cfg.verbose:
            print(self.header)

    def build_training(self,cfg):
        self.training_list = cfg.training_list
        if cfg.verbose:
            print(self.header)
            print("Building training: ")
        for t in self.training_list:
            if cfg.verbose: print(t.name)
            t.build()
        if cfg.verbose:
            print(self.header)

    def loop(self,cfg,progressbar): 
        for d in self.dataset_list:
            for i,c in enumerate(d.componentList):
                taskname = d.name+"_"+str(i)
                c.loop(taskname,cfg,d,progressbar)
    
    def train(self,cfg,progressbar): 
        for i,t in enumerate(self.training_list):
            taskname = t.name+"_"+str(i)
            t.run(taskname,cfg,progressbar)

    def sumup(self,cfg):
        for m in cfg.modules:
            m.sumup(cfg)
