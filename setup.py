from setuptools import find_packages, setup

with open("parambulator/README.md", "r") as f:
    long_description = f.read()

setup(
    name="parambulator",
    version="0.0.1",
    description="An id generator that generated various types and lengths ids",
    package_dir={"": "parambulator"},
    packages=find_packages(where="parambulator"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FrostyGecko/parambulator",
    author="FrostyGecko",
    author_email="imanfoster@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    install_requires=["bson < 2.0.0"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.12",
)

