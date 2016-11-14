# encoding:utf-8

from setuptools import setup, find_packages

from  stockqtl import __version__

with open("requirements.txt") as file:
    required =file.read().splitlines()

long_description = str(open('readme.md', 'rb').read())

setup(
    name="chinastock",
    url="https://github.com/nooperpudd/chinastock",
    license="MIT",
    version=__version__,
    description="Crawling historical and Real-time Quotes data of China stocks",
    long_description=long_description,
    author="winton",
    author_email="winton@quant.vc",
    packages=find_packages(exclude="test"),
    keywords="China Stock API",
    zip_safe=False,
    requires=required,
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ]

)
