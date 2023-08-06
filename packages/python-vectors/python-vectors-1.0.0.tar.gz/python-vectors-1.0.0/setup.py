import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "python-vectors",
    version = "1.0.0",
    author = "Foster Reichert",
    author_email = "dev@fosterreichert.com",
    description = "A simple vector library to contain and manipulate 2D and 3D points.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/fosterhr/python-vectors",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.6",
)