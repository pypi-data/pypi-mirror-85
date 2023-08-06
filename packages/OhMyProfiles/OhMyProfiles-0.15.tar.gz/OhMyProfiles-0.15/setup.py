from setuptools import setup, find_packages

setup(
    name='OhMyProfiles',
    version='v0.15',
    description='A  module for manager profile',
    py_modules=['OhMyProfiles'],
    author='johnpoint',
    author_email='me@lvcshu.com',
    url='https://github.com/johnpoint/Oh-My-Profiles',
    requires=['hashlib', 'os', 'sys', 'json', 'uuid', 'zipfile'],
    license='GPL-3.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'omp=OhMyProfiles.omp:entry',
        ]
    }
)
