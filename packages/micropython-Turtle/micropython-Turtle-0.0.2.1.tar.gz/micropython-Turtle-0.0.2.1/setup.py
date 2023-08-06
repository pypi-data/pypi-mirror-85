import sys 
# Remove current dir from sys.path, otherwise setuptools will peek up our 
# module instead of system's.
sys.path.pop(0) 
from setuptools import setup
sys.path.append("..") 
import sdist_upip 

setup(name='micropython-Turtle',
      version='0.0.2.1',
      description='A Turtle for micropython and add a little game',       
      long_description=open('README.md').read(),
      url='',
      author='David Huang',       
      author_email='menghua0416@hotmail.com',       
      maintainer='David Huang',       
      maintainer_email='menghua0416@hotmail.com',       
      license='MIT',       
      packages=['Turtle','game']
      )