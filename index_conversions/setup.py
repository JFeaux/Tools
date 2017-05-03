from distutils.core import setup 
from Cython.Build import cythonize 
from distutils.extension import Extension 
 
sourcefiles = ['index_wrap.pyx', 'index.cpp']
ext = [Extension('*',
                 sourcefiles,
                 extra_compile_args = ['-O3',
                                       '-std=c++11',
                                       '-fno-var-tracking-assignments'],
                 language='c++')] 
 
setup(ext_modules = cythonize(ext))
 
