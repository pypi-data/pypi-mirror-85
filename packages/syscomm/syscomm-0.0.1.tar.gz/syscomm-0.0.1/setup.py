from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='syscomm',
  version='0.0.1',
  description='A module to use cmd commands in python',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Luke Dixon',
  author_email='monkeyodixon@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='system', 
  packages=find_packages(),
  install_requires=[''] 
)