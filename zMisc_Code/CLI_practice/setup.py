from setuptools import setup

setup(
    name='ncct',
    version='0.0.0',
    url='',
    license='',
    author='Ryan Lougee',
    author_email='Lougee.Ryan@epa.gov',
    description='converts DTXSID to DTXSID',
    py_modules=[],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['docopt', 'pandas'],
    entry_points="""
    [console_scripts]
    NCCT = NCCT_CLI:main
    """
)
