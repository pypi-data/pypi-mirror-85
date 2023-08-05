from distutils import util

from setuptools import find_packages, setup

main_ns = {}
ver_path = util.convert_path("chia_tools/version.py")

with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="chia-tools",
    version=main_ns["__version__"],
    packages=["chia_tools"],
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "tqdm~=4.51",
        "tables~=3.6.1",
        "pandas~=1.0.4",
        "pyqt5~=5.15.0",
        "matplotlib~=3.2.1",
        "chia~=2.0rc20",
    ],
    # metadata to display on PyPI
    author="Clemens-Alexander Brust",
    author_email="clemens-alexander.brust@uni-jena.de",
    description="Extra tools for the CHIA framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    url="https://github.com/cabrust/chia-tools",
)
