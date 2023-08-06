import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="osmeterium", 
    version="0.0.3",
    author="MapColonies",
    author_email="mapcolonies@gmail.com",
    description="A wrapper for subprocess popen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MapColonies/osmeterium",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)
