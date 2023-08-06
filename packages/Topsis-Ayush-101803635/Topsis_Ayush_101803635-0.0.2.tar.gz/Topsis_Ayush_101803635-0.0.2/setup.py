from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Topsis_Ayush_101803635',
  version='0.0.2',
  description='myTopsisPackage',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ayush anand Saxena',
  author_email='asaxena_be18@thapar.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='TOPSIS', 
  packages=find_packages(),
  install_requires=['pandas','math'] 
)

