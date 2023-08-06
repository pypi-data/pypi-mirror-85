
import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "estime2",
    version = "0.0.19",
    author =\
        "Christian Olivier Nambeu <christianolivier.nambeu@canada.ca>, " +\
        "Junkyu Park <junkyu.park@canada.ca>",
    description = "Population table manipulation.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitlab.com/joon3216/estime2",
    packages = setuptools.find_packages(),
    python_requires = ">=3.6.1",
    license = "MIT License",
    install_requires = [
        "matplotlib",
        "pandas",
        "xlrd"
    ],
    classifiers = [
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ]
)
