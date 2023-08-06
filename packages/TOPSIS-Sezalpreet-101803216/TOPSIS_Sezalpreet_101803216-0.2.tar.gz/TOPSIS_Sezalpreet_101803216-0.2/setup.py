from setuptools import setup
def readme():
  with open('README.md') as f:
    README  = f.read()
  return README


setup(
  name = 'TOPSIS_Sezalpreet_101803216',
  packages = ['TOPSIS_Sezalpreet_101803216'],
  version = '0.2',
  license='MIT',
  description = 'This is python program for implementation of topsis',
  long_description= readme(),
  long_description_content_type = "text/markdown",
  author = 'Sezalpreet Kaur',
  author_email = 'sezalprkaur@gmail.com',
  url = 'https://github.com/sezalprkaur/Topsis.git',
  install_requires=[
          'pandas',
          'numpy',
          'csv',
      ],
  include_package_data = True,
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)