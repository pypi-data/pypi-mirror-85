from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='rotate_matrix',
  version='0.0.1',
  description='Rotate any matrix of any type, either clockwise or anti-clockwise instantly.',
#   long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Udipta/Naninture',
  author_email='uddipta2255@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='rotate matrix', 
  packages=find_packages(),
  install_requires=[''],
)