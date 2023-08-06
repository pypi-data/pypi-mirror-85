import numpy as np

from PyLooper.Common.Module import Module

import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule

mod = SourceModule("""
#include <stdio.h>

__global__ void calculate(float *dest, float *gen_weight, float xs, float lumi, float sumw )
{
  const int i = threadIdx.x + blockDim.x * blockIdx.x;
  dest[i] = gen_weight[i] * xs * lumi / sumw;
}
""")
calculate_xs_weight = mod.get_function("calculate")

class GPUCrossSectionWeighter(Module):
    def analyze(self,data,dataset,cfg):
        if not dataset.skip_weight:
            if dataset.isMC:
                cfg.collector.xs_weight = data["genWeight"]*dataset.xs*dataset.lumi/dataset.sumw
            else:
                cfg.collector.xs_weight = np.ones(data["genWeight"].shape)

