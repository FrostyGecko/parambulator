from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="parambulator",
    version="0.0.1",
    description="General purpose orbital mechanics library",
    package_dir={"": "src/parambulator"},
    packages=find_packages(where="src/parambulator"),
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
    install_requires=["numpy >= 2.0.4"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.12",
)

