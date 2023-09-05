from setuptools import find_packages, setup

setup(
    name="Nagios API",
    version="0.0.1",
    description="Python bindings for Nagios' JSON API.",
    author="Willem Hunt",
    author_email="whunt1@uvm.edu",
    packages=find_packages(),
    requires=["requests", "pandas"],
)
