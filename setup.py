from distutils.core import setup

setup(
    name='django-crowd',
    version='0.41dev',
    packages=['crowd',],
    install_requires=['httplib2'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)
