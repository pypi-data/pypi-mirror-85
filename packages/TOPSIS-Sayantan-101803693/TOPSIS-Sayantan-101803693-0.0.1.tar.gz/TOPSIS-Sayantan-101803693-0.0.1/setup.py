import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "TOPSIS-Sayantan-101803693",
    version = "0.0.1",
    author = "Sayantan Pradhan",
    author_email = "pradhan.sayantan24@gmail.com",
    description = "Library to use topsis",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/sayantan24/TOPSIS-Sayantan-101803693",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)