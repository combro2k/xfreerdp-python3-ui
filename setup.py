import setuptools

from distutils.core import setup

setup(
    name='xfreerdpui',
    author='Martijn van Maurik',
    author_email='git@vmaurik.nl',
    version='0.1dev',
    packages=['xfreerdpui',],
    license='MIT',
    long_description=open('README.txt').read(),
    url='https://github.com/combro2k/xfreerdp-python3-ui/',
    entry_points = {
        'console_scripts': ['xfreerdpui=xfreerdpui.xfreerdpui:main'],
    },
#    scripts=['bin/xfreerdpui'],
#    install_requires=[
#        'qtile',
#    ],
    python_requires='>=3',
)
