from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'

]
 
setup(
  name='TOPSIS-Divyam-101803644',
  version='0.0.1',
  description='Topsis',
  long_description=open('README.txt').read(),
  url='',  
  author='Divyam Singla',
  author_email='divyamsingla0405@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='topsis', 
  packages=find_packages(),
  install_requires=[''] 
)