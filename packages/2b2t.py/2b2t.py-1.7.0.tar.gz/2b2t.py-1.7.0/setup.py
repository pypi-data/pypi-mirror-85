from py2b import __author__, __version__
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='2b2t.py',
    version=__version__,
    author=__author__,
    description='A package for all things 2b2t',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BGP0/2b2t.py',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)