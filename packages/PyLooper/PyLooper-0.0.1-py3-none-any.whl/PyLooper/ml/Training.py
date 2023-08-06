from PyLooper.progressBar.ProgressReport import ProgressReport

class Training(object):
    def __init__(self,name,data_wrapper,optimizer,):
        self.name = name
        self.data_wrapper = data_wrapper
        self.optimizer = optimizer

    def build(self):
        self.data_wrapper.build()

    def run(self,taskname,cfg,progressbar):
        self.report = ProgressReport(taskname,0,cfg.nepoch)
        for m in cfg.modules:
            m.begin(self,cfg)
        for iepoch in range(cfg.nepoch):
            data = self.data_wrapper.get(iepoch,cfg)
            for m in cfg.modules:
                m.analyze(data,self,cfg)
            self.report.done += 1
            progressbar.present(self.report)
        for m in cfg.modules:
            m.end(self,cfg)
