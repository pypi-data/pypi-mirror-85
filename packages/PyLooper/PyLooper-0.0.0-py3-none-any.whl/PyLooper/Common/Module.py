import os

class Module(object):
    def __init__(self,name):
        self.name = name
    
    def begin(self,dataset,cfg):
        pass

    def end(self,dataset,cfg):
        pass

    def analyze(self,data,dataset,cfg):
        pass

    def sumup(self,cfg):
        pass
