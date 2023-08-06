from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 #open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read()
setup(
  name='DataStructures10',
  version='1.0.1',
  description='Data structure components module',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='',  
  author='Dereck Jos',
  author_email='derijos55@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='data_structure',
  packages=find_packages(),
  install_requires=[''] 
)
