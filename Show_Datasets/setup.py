from setuptools import setup

setup(
    name='showdatasets',
    version='1.0.0',
    url='',
    license='',
    author='Ryan Lougee',
    author_email='Lougee.Ryan@epa.gov',
    description='Lists stored datasets matching a given string',
    py_modules=[],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['docopt', 'pandas', 'colorama'],
    entry_points="""
    [console_scripts]
    showdatasets = showdatasets:main
    """
)
