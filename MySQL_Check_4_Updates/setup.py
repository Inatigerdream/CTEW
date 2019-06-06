from setuptools import setup


setup(
  name='update_qsar_datasets',
  version='1.0',
  py_modules=['MySQL_Check_4_Updates'],
  install_requires=['Click','xlrd','pandas','PyMySQL','PyYAML','mysqlclient', 'SQLAlchemy'],
  entry_points='''
    [console_scripts]
    update_qsar_datasets=update_qsar_datasets:cli
  '''
)
