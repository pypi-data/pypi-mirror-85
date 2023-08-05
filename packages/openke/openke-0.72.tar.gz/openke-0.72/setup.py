import os

import setuptools
from setuptools.command.install import install

with open("README.md", "r") as fh:
    long_description = fh.read()


class PostInstallCommand(install):
    def run(self):
        os.system('g++ ./openke/base/Base.cpp -fPIC -shared -o ./openke/release/Base.so -pthread -O3 -march=native -std=c++11')


setuptools.setup(
    name='openke',
    version='0.72',
    scripts=['openke/make.sh'],
    authors=["thunlp", "zeionara"],
    author_email="zeionara@gmail.com",
    description="A library for operating knowledge graph models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zeionara/OpenKE",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'install': PostInstallCommand
    },
)
