from distutils.core import setup

setup(
    name='xfreerdpui',
    version='0.1dev',
    packages=['xfreerdpui',],
    scripts=['bin/xfreerdpui'],
    name='xfreerdp-python3-ui',
    version='0.1dev',
    packages=['xfreerdp-python3-ui',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)
