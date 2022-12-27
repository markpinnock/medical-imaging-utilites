from setuptools import find_packages, setup


setup(
    name='utilities',
    packages=find_packages(),
    version='0.1.0',
    description=('Utilities for processing medical images'),
    author='Mark Pinnock',
    license='MIT',
    entry_points={
        'console_scripts': [
            'check_coordinates=utilities.coordinates:check_coordinates'
        ],
    },
)