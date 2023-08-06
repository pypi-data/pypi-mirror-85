import distutils.dir_util
from distutils.command import build
import os, sys, re
try:
    import setuptools
    from setuptools import setup, find_packages
    from setuptools.command import install
except ImportError:
    sys.stderr.write("Warning: could not import setuptools; falling back to distutils.\n")
    from distutils.core import setup
    from distutils.command import install

from pymodaq_pid_models.version import get_version

with open('README.rst') as fd:
    long_description = fd.read()

setupOpts = dict(
    name='pymodaq_pid_models',
    description='PID models to use with PyMoDAQ',
    long_description=long_description,
    license='MIT',
    url='http://pymodaq.cnrs.fr',
    author='Sébastien Weber',
    author_email='sebastien.weber@cemes.fr',
    classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        ],)

def listAllPackages(pkgroot):
    path = os.getcwd()
    n = len(path.split(os.path.sep))
    subdirs = [i[0].split(os.path.sep)[n:] for i in os.walk(os.path.join(path, pkgroot)) if '__init__.py' in i[2]]
    return ['.'.join(p) for p in subdirs]


allPackages = (listAllPackages(pkgroot='pymodaq_pid_models')) #+
               #['pyqtgraph.'+x for x in helpers.listAllPackages(pkgroot='examples')])


setup(
    version=get_version(),
     #cmdclass={'build': Build,},
    #           'install': Install,
    #           'deb': helpers.DebCommand,
    #           'test': helpers.TestCommand,
    #           'debug': helpers.DebugCommand,
    #           'mergetest': helpers.MergeTestCommand,
    #           'style': helpers.StyleCommand},
    packages=find_packages(),
    install_requires=[],
    **setupOpts
)

