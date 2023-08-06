from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='TOPSIS_Lakshya_101803492',
  packages=['TOPSIS_Lakshya_101803492'],
  version='0.0.65',
  description='Implementation of Multiple Criteria Decision Making (MCDM) using TOPSIS in Python.',
  long_description=open('README.md').read(),
  long_description_content_type="text/markdown",
  url='https://github.com/lakkshh',
  download_url='https://github.com/lakkshh/TOPSIS_Python/archive/0.0.2.tar.gz',
  author='Lakshya Gupta',
  author_email='lg0605@gmail.com',
  license='MIT', 
  classifiers=classifiers, 
  include_package_data = True,
  python_requires='>=3.0',
  keywords=['simple', 'topsis', 'implementation', 'python'],
  install_requires=['pandas','numpy'] 
)