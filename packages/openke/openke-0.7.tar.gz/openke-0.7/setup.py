import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='openke',
    version='0.7',
    scripts=['openke_'],
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
    ]
)
