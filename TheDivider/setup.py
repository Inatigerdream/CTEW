from setuptools import setup


setup(
  name='divider',
  version='1.0',
  py_modules=['divider'],
  install_requires=[
    'Click','xlrd','pandas',
    ],
  entry_points='''
    [console_scripts]
    divider=divider:cli
  '''
)
