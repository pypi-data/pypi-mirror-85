from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='dakshbasicpackage',
  version='0.0.1',
  description='Basic Print statement',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Daksh Kanoria',
  author_email='contact@dakshkanria.me',
  license='MIT', 
  classifiers=classifiers,
  keywords='print',
  packages=find_packages(),
  install_requires=[''] 
)
