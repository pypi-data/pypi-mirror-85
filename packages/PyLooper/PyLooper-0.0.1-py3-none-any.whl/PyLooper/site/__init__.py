import platform

class Site(object):
    ufhpc = "ufhpc"
    laptop = "laptop"
    @property
    def where(self):
        host_name = platform.node()
        if self.ufhpc in host_name:
            return self.ufhpc
        else:
            return self.laptop
