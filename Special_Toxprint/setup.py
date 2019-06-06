from setuptools import setup


setup(
  name='SQL_special_toxprint_generator',
  version='1.0',
  py_modules=['SQL_special_toxprint_generator'],
  install_requires=[
    'Click','xlrd','pandas','PyMySQL','PyYAML','mysqlclient', 'SQLAlchemy', 
    ],
  entry_points='''
    [console_scripts]
    SQL_special_toxprint_generator=SQL_special_toxprint_generator:cli
  '''
)
