from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="easyglue",
    version="0.0.2",
    author="Albert Quiroga",
    author_email="albertquirogabertolin@gmail.com",
    description="Glue DynamicFrame syntax closer to DataFrames",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.0"
)
