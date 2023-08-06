from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='TOPSIS_Ayush_101803401',
  version='0.0.1',
  description='A very basic file of topsis',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='AYUSH',
  author_email='ayush15goel@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='topsis', 
  packages=find_packages(),
  install_requires=[''] 
)
