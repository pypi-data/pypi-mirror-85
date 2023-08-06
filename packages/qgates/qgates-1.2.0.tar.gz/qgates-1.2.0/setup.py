import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qgates",
    version="1.2.0",
    author="Austin Poor",
    author_email="austinpoor@gmail.com",
    description="Helper library for quantum matrix math",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a-poor/QGates",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
