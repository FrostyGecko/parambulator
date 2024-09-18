from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="parambulator",
    version="0.0.1",
    description="General purpose orbital mechanics library",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source" : "https://github.com/FrostyGecko/parambulator",
        },
    author="FrostyGecko",
    author_email="frostygecko1@gmail.com",
    license="MIT",
    classifiers=[
        "Development STatus :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12.4",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.10",
)

