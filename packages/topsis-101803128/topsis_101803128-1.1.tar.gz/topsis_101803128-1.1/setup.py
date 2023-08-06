import pathlib
# from distutils.core import setup
from setuptools import setup

long_description="hello"


# This call to setup() does all the work
setup(
    name="topsis_101803128",  # How you named your package folder (MyLib)
    packages = ['topsis_101803128'],   # Chose the same as "name"
    version="1.1",   # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="A Python package implementing TOPSIS technique.",   # Give a short description about your library
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Divyam Jain",   # Type in your name
    author_email="divyamvswild@gmail.com",  # Type in your E-Mail
    url="https://github.com/Divyamdj/Topsis-Pypi-Package",    # Provide either the link to your github or to your website
    download_url="https://github.com/Divyamdj/Topsis-Pypi-Package/archive/v1.1.tar.gz",
    keywords=['Topsis', 'Topsis Ranking'],    # Keywords that define your package best
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        "License :: OSI Approved :: MIT License",   # Again, pick a license
        "Programming Language :: Python :: 3.6",    # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=['numpy',
                      'pandas',
     ],
    include_package_data=True,
    #  entry_points={
    #     "console_scripts": [
    #         "topsis=topsis.topsis:main",
    #     ]
    # },
)
