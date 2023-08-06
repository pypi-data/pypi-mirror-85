import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    install_requires=[
        "importlib-metadata==2.0.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "jsonpickle==1.4.1",
        "numpy==1.19.4",
        "scipy==1.5.4",
        "zipp==3.4.0; python_version >= '3.6'",
    ],
    name="argueview",
    version="0.1.2",
    author="Sophia Hadash",
    author_email="s.hadash@tue.nl",
    description="ArgueView is a tool for generating text-based presentations for machine-learning predictions and feature-importance based explanation tools. The tool makes use of Toulmin's model of argumentation for structuring the text-based explanations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SophiaHadash/ArgueView",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Development Status :: 3 - Alpha",
    ],
    keywords="explanations, text, toulmin, argumentation",
    python_requires=">=3.5",
)
