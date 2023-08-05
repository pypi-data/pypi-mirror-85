import os
import setuptools
import sys

# NOTE: If dijkstra.cpp does not exist:
# cython -3 --fast-fail -v --cplus dijkstra.pyx

import numpy as np

extra_compile_args = [
  '-std=c++11', '-O3', '-ffast-math', 
]

if sys.platform == 'darwin':
  extra_compile_args += [ '-stdlib=libc++', '-mmacosx-version-min=10.9' ]

setuptools.setup(
  setup_requires=['pbr', 'numpy'],
  extras_require={
    ':python_version == "2.7"': ['futures'],
    ':python_version == "2.6"': ['futures'],
  },
  ext_modules=[
    setuptools.Extension(
      'dijkstra3d',
      sources=[ 'dijkstra3d.cpp' ],
      language='c++',
      include_dirs=[ np.get_include() ],
      extra_compile_args=extra_compile_args,
    )
  ],
  pbr=True)





