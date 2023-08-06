from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()


classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='topsis-ishan-101816037',
  version='0.0.1',
  description='topsis score and rank calculator',
  long_description=open('README.md').read(),
  url='',  
  author='Ishan Sakhuja',
  author_email='isakhuja_be18@thapar.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='topsis', 
  packages=find_packages(),
  install_requires=[''] 
)