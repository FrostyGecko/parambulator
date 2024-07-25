from setuptools import find_packages, setup

with open("parambulator/README.md", "r") as f:
    long_description = f.read()

setup(
    name="parambulator",
    version="0.0.1",
    description="General purpose orbital mechanics library",
    package_dir={"": "parambulator"},
    packages=find_packages(where="parambulator"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source" : "https://github.com/FrostyGecko/parambulator",
        },
    author="FrostyGecko",
    author_email="imanfoster@gmail.com",
    license="MIT",
    classifiers=[
        "Development STatus :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=["bson < 2.0.0","numpy <= 1.26.4"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.12",
)

