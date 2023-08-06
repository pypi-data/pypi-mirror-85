from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='sbackup',
  version='0.0.1',
  description='Folder/File backup manager by seletive file extensions',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Swarnadeep Seth',
  author_email='swdseth@yahoo.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='backup, backup manager', 
  packages=find_packages(),
  install_requires=['python3-tk'] 
)
