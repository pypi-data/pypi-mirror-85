import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS-Parth-101983047", # Replace with your own username
    version="0.0.1",
    author="Parth Verma",
    author_email="vermaparth818@gmail.com",
    description="A simplified package to perform TOPSIS Analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/parth818/TOPSIS-Parth-101983047",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
