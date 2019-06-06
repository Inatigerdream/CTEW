from setuptools import setup

setup(
    name='toxprint_generator',
    version='1.0.0',
    url='',
    license='',
    author='Ryan Lougee',
    author_email='Lougee.Ryan@epa.gov',
    description='fills MySQL db with toxprint chemotypes',
    py_modules=[],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
    'docopt','xlrd','pandas','PyMySQL','PyYAML','mysqlclient', 'SQLAlchemy', 'numpy'
    ],
    entry_points="""
    [console_scripts]
    toxprint_generator = SQL_toxprint_generator:main
    """
)