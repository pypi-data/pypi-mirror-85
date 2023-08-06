import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylinlin",
    version="0.0.1",
    author="Owen Leong",
    author_email="owenl131@gmail.com",
    description="A nice linear algebra library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/owenl131/pylinlin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
