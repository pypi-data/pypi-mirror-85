from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='TOP_SIS_CAL',
  version='0.0.1',
  description='Calculation of TOPSIS',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  long_description_content_type='text/markdown',
  author='Rushab Kanodia',
  author_email='rkanodia_be18@thapar.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='TOP_SIS', 
  packages=find_packages(),
  install_requires=[''] 
)