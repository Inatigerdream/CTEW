from setuptools import setup

setup(
    name='removeduplicates',
    version='0.0.0',
    url='',
    license='',
    author='Ryan Lougee',
    author_email='Lougee.Ryan@epa.gov',
    description='removes/condenses duplicate chemical IDs',
    py_modules=[],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['docopt', 'pandas', 'colorama'],
    entry_points="""
    [console_scripts]
    removeduplicates = removeduplicates:main
    """
)
