import rasterio
import numpy as np
import warnings
import aeronet.dataset as ds
from typing import List
from rasterio.windows import Window
from pysharpen.methods import ImgProc
from pysharpen.functional import saturate_cast


class Worker_nogeo:
    """
    A
    """
    def __init__(self, methods: List[ImgProc],
                 resampling='bilinear', out_dtype=None):

        self.out_dtype = out_dtype
        self.resampling = resampling
        # methods have to be initialized
        self.methods = methods


