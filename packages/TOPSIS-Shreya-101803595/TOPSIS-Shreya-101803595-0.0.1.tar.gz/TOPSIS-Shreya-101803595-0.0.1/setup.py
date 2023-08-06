from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='TOPSIS-Shreya-101803595',
  version='0.0.1',
  description='This Python Package is used to implement the TOPSIS Algorithm',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type = "text/markdown",
  url='',  
  author='Shreya Gupta',
  author_email='sgupta2_be18@thapar.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='TOPSIS', 
  packages=find_packages(),
  include_package_data=True,
  install_requires=['numpy','pandas'],
  entry_points={
        "console_scripts": ["topsis=packageTopsis:main",]},
)