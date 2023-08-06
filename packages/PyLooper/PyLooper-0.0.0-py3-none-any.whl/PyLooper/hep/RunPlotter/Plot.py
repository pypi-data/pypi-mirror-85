class Plot(object):
    def __init__(self,name,array_func,event_weight_func,hist,
            dim=1,
            selection_func=None
            ):
        self.name = name
        self.array_func = array_func
        self.event_weight_func = event_weight_func
        self.hist = hist
        self.dim = dim
        self.selection_func = selection_func

        self.data_color = 'black'
