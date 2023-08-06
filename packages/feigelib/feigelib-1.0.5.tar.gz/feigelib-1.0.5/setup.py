import setuptools
from distutils.core import setup
from setuptools import find_packages

setuptools.setup(
    name="feigelib",
    version="1.0.5",
    author="feige studio",
    author_email="3357135715@qq.com",
    description="xueersi feige",
    long_description="",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
    ],
    packages=find_packages('f_print'),
    package_dir={'':'f_print'},


)