from setuptools import setup, find_packages

import sys
sys.path.insert(0, '.')
from datautildate import __version__, __doc__ as __long_description__

setup(
    name='datautildate',
    version=__version__,
    license='MIT',
    description='Date Utilities for Data Work',
    long_description=__long_description__,
    author='Open Knowledge Foundation',
    author_email='info@okfn.org',
    url='http://okfn.org/projects/datautil/',
    download_url='http://github.com/okfn/datautildate/',
    install_requires=[
        # python-dateutil 2.0 has different _parse method, so stick to 1.4.1
        'python-dateutil>=1.0,<1.99',
        # (optional) for excel handling
        # xlrd
        # (optional) for google docs handling
        # gdata
        ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
