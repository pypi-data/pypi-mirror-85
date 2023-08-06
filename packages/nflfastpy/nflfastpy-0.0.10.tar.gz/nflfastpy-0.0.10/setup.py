import setuptools
from nflfastpy import __version__


setuptools.setup(
    name="nflfastpy",
    version=__version__,
    author="Ben Dominguez",
    author_email="bendominguez011@gmail.com",
    description="A Python package for loading NFL play by play data, schedule data, roster data, and team logo data from nflfastR",
    long_description="A Python package for loading NFL play by play data from nflfastR",
    url="https://github.com/fantasydatapros/nflfast_py",
    license="MIT",
    install_requires=['pandas', 'requests', 'matplotlib', 'pyreadr'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)