import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SPARQL-Burger",
    version="1.0.1",
    author="Panos Mitzias",
    author_email="pmitzias@gmail.com",
    description="A Python SPARQL query builder that automates the generation of SPARQL graph patterns, SPARQL Select and SPARQL Update queries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/panmitz/SPARQL-Burger",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    )
)