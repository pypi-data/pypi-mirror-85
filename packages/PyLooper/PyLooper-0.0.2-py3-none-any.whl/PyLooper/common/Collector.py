from PyLooper.utils.mkdir_p import mkdir_p

class Collector(object):
    def __init__(self,output_path):
        self.output_path = output_path

    def init_job(self):
        mkdir_p(self.output_path)

