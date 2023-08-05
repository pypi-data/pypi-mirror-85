from setuptools import setup, find_packages
import sys

message = 'autodatasets has been renamed to d8, please use `pip install d8`'

argv = lambda x: x in sys.argv

if (argv('install') or  # pip install ..
        (argv('--dist-dir') and argv('bdist_egg'))):  # easy_install
    raise Exception(message)

if argv('bdist_wheel'):  # modern pip install
    raise Exception(message)

requirements = [
    'kaggle',
    'pandas>=1.1.0',
    'tqdm',
]

setup(
    name='autodatasets',
    version='0.0.2',
    python_requires='>=3.5',
    author='',
    author_email='',
    url='',
    description='',
    license='Apache 2.0',
    packages=find_packages(),
    zip_safe=True,
    install_requires=requirements,
    include_package_data=True,
    package_data={'autodatasets':[]},
    entry_points={
        'console_scripts': [
            'autodatasets = autodatasets.main:main',
            'ad = autodatasets.main:main'
        ]
    },
)
