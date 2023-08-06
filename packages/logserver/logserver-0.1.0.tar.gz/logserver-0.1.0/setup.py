from setuptools import setup

# https://setuptools.readthedocs.io/en/latest/
setup(
    name="logserver",
    version="0.1.0",
    description="A simple socket-based log server based on the Python logging cookbook.",
    long_description=open("README.md", "rt").read(),
    url="https://github.com/luismsgomes/logserver",
    author="Luís Gomes",
    author_email="luismsgomes@gmail.com",
    license="GPLv3",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="logging util",
    install_requires=[],
    package_dir={"": "."},
    py_modules=["logserver"],
)
