import setuptools

from distutils.core import setup

setup(
    name='xfreerdpui',
    author='Martijn van Maurik',
    author_email='git@vmaurik.nl',
    version='0.1dev',
    packages=['xfreerdpui',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    url='https://github.com/combro2k/xfreerdp-python3-ui/',
    entry_points = {
        'console_scripts': ['xfreerdpui=xfreerdpui.xfreerdpui:main'],
    },
    install_reuires=[
        'gtk3',
        'qtile',
    ],
)
