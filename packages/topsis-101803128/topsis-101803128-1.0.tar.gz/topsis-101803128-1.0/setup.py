import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="topsis-101803128",
    version="1.0",
    description="A Python package implementing TOPSIS technique.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Divyamdj/topsis-divyam",
    author="Divyam Jain",
    author_email="divyamvswild@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=['scipy',
                      'tabulate',
                      'numpy',
                      'pandas',
                      'csv',
                      'math'
     ],
     entry_points={
        "console_scripts": [
            "topsis=topsis.topsis:main",
        ]
    },
)