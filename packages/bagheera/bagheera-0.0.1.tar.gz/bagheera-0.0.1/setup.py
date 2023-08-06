import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bagheera", # Replace with your own username
    version="0.0.1",
    author="Bagheera",
    author_email="bergmann.jerome@gmail.com",
    description="An implementation of the bagheera programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bagheera-lang/bagheera-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)