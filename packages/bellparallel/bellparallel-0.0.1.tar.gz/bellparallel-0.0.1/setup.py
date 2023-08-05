#!/usr/bin/python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='bellparallel',
    version='0.0.1',
    description='Parallel execution utils',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Fabian Bell',
    author_email='fabianx.bell@gmail.com',
    url='https://github.com/FabianBell/Packages/tree/master/bell_parallel',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_required='>=3.8'
    )
