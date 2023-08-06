from setuptools import setup, find_packages

with open("README.txt", "r") as fh:
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
  name='sklearning',
  version='0.0.1',
  description='metrics module',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='',  
  author='Dereck Jos',
  author_email='dereckjos12@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='metrics',
  packages=find_packages(),
  install_requires=[''] 
)
