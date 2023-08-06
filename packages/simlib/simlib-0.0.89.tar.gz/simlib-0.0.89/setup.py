"""
setup.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from setuptools import setup


# Read version
with open('version.yml', 'r') as f:
    data = f.read().splitlines()
version_dict = dict([element.split(': ') for element in data])

# Convert the version_data to a string
version = '.'.join([str(version_dict[key]) for key in ['major', 'minor', 'patch']])

# Read in requirements.txt
with open('requirements.txt', 'r') as stream:
    requirements = stream.read().splitlines()

# Long description
with open('README.md', 'r') as stream:
    long_description = stream.read()

# Setup
setup(
    name='simlib',
    version=version,
    author='C. Lockhart',
    author_email='chris@lockhartlab.org',
    description='A toolkit for molecular dynamics simulations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://www.lockhartlab.org",
    packages=[
        'simlib',
        'simlib.analysis',
        'simlib.analysis.protein',
        'simlib.core',
        'simlib.external',
        'simlib.geometry',
        'simlib.io',
        'simlib.misc',
        'simlib.transform',
        'simlib.viz'
    ],
    install_requires=[
        'glovebox',
        'numpy',
        'pandas',
        'privatize',
        'typelike', 'hypothesis', 'numba'
    ],
    include_package_data=True,
    zip_safe=True
)
