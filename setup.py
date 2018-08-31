from distutils.core import setup, Extension
import numpy

# define the extension module
ProjOutputData_module = Extension('ProjOutputData_module', sources=['CreateData.cpp'],include_dirs=[numpy.get_include()])

# run the setup
setup(ext_modules=[ProjOutputData_module])