#!/usr/bin/env python

from setuptools import setup
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

# read version from package
exec(open('catapult/_version.py').read())

setup(
    name='catapult',
    version=__version__,
    description='TAP, TAP-J, and TAP-Y output for unittest suites',
    long_description=read_md('README.md'),
    author='Joshua C Elliott',
    author_email='joshuacelliott@gmail.com',
    license='MIT',
    url='https://github.com/jcelliott/catapult',
    packages=['catapult'],
    include_package_data=True,
    keywords="TAP TAP-J TAP-Y testing unittest",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Testing",
    ],

    install_requires=[
        "arrow >=0.4.2,<0.5",
        "nose >=1.3.1,<1.4",
        "PyYAML >=3.11,<3.12",
    ],

    entry_points={
        'nose.plugins.0.10': [
            'catapult = catapult:CatapultPlugin'
        ]
    },
)
