from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='pysharedoscom',
  version='v1.4',
  description='Pyshare Library',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Aldhiya Rozak',
  author_email='Aldhiya.rozak@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='menu',
  packages=find_packages(),
  install_requires=['']
)
