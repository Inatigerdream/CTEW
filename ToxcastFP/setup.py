from setuptools import setup

setup(
    name='ToxcastFP_generator',
    version='1.0.0',
    url='',
    license='',
    author='Ryan Lougee',
    author_email='Lougee.Ryan@epa.gov',
    description='Adds and updates Toxcast Chemical Fingerprints',
    py_modules=[],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['docopt', 'pandas', 'colorama'],
    entry_points="""
    [console_scripts]
    ToxcastFP_generator = ToxcastFP_generator:main
    """
)
