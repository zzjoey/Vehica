from distutils.core import setup
from Cython.Build import cythonize
import numpy as np

setup(ext_modules=cythonize('compute_overlap.pyx'),include_dirs=[np.get_include()])
