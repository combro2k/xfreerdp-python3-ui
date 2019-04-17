import setuptools

from distutils.core import setup

setup(
    name='xfreerdpui',
    version='0.1dev',
#    packages=['xfreerdpui',],
    packages=setuptools.find_packages(),
    scripts=['bin/xfreerdpui'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)
