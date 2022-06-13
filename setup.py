
import os
import sys

import setuptools

sys.path.append(os.path.join(os.path.dirname(__file__), 'nodegraph'))

import pkg_info

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

description = (
    'A node graph framework that can be re-implemented into applications that '
    'supports PySide6'
)
classifiers = [
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10',
    'Documentation :: https://fivedbrothers.github.io/nodegraph/api/html/index.html',
    'Source :: https://github.com/fivedbrothers/nodegraph/',
]

setuptools.setup(
    name=pkg_info.__module_name__,
    version=pkg_info.__version__,
    authors=pkg_info.__authors__,
    porter=pkg_info.__porter__,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=pkg_info.__url__,
    packages=setuptools.find_packages(exclude=['example_nodes']),
    classifiers=classifiers,
    install_requires=requirements,
    include_package_data=True,
    python_requires='>=3.10',
    extras_require={
        'PySide6': ['PySide6>=6.2.3']
    }
)


"""
python setup.py sdist
sudo python setup.py install
"""
