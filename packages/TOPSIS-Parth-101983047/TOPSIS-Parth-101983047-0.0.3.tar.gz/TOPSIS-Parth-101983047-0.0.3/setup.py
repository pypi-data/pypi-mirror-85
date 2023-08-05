import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS-Parth-101983047",
    version="0.0.3",
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
    install_requires=['pandas','os'],
    python_requires='>=3.6',
)
