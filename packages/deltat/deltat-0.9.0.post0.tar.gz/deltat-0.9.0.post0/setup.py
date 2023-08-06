#!/usr/bin/python3
import re

import setuptools


def extract_version(filename):
    with open(filename, 'r') as fh:
        for line in fh:
            match = re.match('''VERSION\s*=\s*["']([-_.0-9a-z]+)(\+?)["']''', line)
            if match:
                if match[2] == '':
                    return match[1]
                else:
                    return match[1] + '.post'
    exit("Cannot extract version number from %s" % filename)


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="deltat",
    version=extract_version('deltat/__init__.py'),
    author="Marcel Waldvogel",
    author_email="marcel.waldvogel@trifence.ch",
    description="Friendly text to timedelta conversion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/MarcelWaldvogel/deltat",
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[],
    python_requires='>=3.2',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
)
