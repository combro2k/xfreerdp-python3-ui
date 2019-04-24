import setuptools

from distutils.core import setup

setup(
    name='xfreerdpui',
    version='0.1dev',
    packages=['xfreerdpui',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    entry_points = {
        'console_scripts': ['xfreerdpui=xfreerdpui.xfreerdpui:main'],
    },
    extra_require={
        ':"linux" in sys_platform': [
            'gtk3'
        ]
    },
)
