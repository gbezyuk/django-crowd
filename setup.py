from distutils.core import setup

setup(
    name='django-crowd',
    version='0.42dev',
    packages=['crowd',],
    install_requires=['httplib2'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    author="Konstantin Volkov",
    author_email="konstantin-j-volkov@yandex.ru",
    maintainer="Grigoriy Beziuk",
    maintainer_email="gbezyuk@gmail.com"
)
