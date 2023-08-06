import sys
# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system's.
sys.path.pop(0)
from setuptools import setup
sys.path.append("..")
import sdist_upip

setup(name='micropython-ZJB',
      version='4.0',
      description='A test for ZJB',
      long_description=open('README.md').read(),
      url='https://zjbin.xyz',
      author='Stephen Zhu',
      author_email='1524427210zjb@gmail.com',
      maintainer='Stephen Zhu',
      maintainer_email='1524427210zjb@gmail.com',
      license='MIT',
      #cmdclass={'sdist': sdist_upip.sdist},
      )
