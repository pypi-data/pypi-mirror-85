

from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='TOPSIS_Jaiwant_101803389',
  version='0.0.1',
  description='A very basic  TOPSIS calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Jaiwant Singh',
  author_email='jaiwantsingh2000@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='TOPSIS', 
  packages=find_packages(),
  install_requires=[''] 
)