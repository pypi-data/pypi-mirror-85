from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='multilabel_stratify',
  version='0.0.2',
  description='A function that generates stratified test-train splits for multi-label data',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/maxitron93/multilabel_stratify',  
  author='Maxi Merrillees',
  author_email='maxi.merrillees@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='multi-label multilabel stratify stratified split', 
  packages=find_packages(),
  install_requires=['numpy'] 
)