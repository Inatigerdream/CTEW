from setuptools import setup


setup(
  name='fp_combo_gen',
  version='1.0',
  py_modules=['fp_combo_gen'],
  install_requires=[
    'Click','xlrd','pandas', 'scipy','progressbar2'
  ],
  entry_points='''
    [console_scripts]
    fp_combo_gen=fp_combo_gen:cli
  '''
)
