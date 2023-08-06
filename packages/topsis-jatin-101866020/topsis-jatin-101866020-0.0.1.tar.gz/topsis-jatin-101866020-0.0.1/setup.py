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
  name='topsis-jatin-101866020',
  version='0.0.1',
  description='topsis score and rank calculator',
  long_description=open('README.md').read(),
  url='',  
  author='Jatin Rana',
  author_email='jjatin_bemba18@thapar.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='topsis', 
  packages=find_packages(),
  install_requires=[''] 
)