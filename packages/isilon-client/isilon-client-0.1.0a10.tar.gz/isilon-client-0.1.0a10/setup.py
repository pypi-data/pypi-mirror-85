from isilon import __version__

from collections import OrderedDict

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="isilon-client",
    version=f"{__version__}",
    author="alexandre menezes",
    author_email="alexandre.fmenezes@gmail.com",
    description="async rest client for isilon object storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    url="https://github.com/amenezes/isilon-client",
    packages=setuptools.find_packages(include=["isilon", "isilon.*"]),
    python_requires=">=3.6.0",
    project_urls=OrderedDict(
        (
            ("Documentation", "https://isilon-client.amenezes.net"),
            ("Code", "https://github.com/amenezes/isilon-client"),
            ("Issue tracker", "https://github.com/amenezes/isilon-client/issues"),
        )
    ),
    install_requires=["aiohttp>=3.5.2", "attrs>=19.1.0"],
    tests_require=[
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
        "flake8",
        "flake8-blind-except",
        "flake8-polyfill",
        "isort",
        "black",
        "mypy",
        "aiohttp"
    ],
    extras_require={
        "docs": ["portray"],
        "cli": ["cleo"],
        "all": ["portray", "cleo"],
    },
    setup_requires=["setuptools>=38.6.0"],    
    classifiers=[        
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries"
    ],
)
