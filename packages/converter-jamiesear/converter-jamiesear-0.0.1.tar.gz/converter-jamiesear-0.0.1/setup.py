import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='converter-jamiesear',
    version='0.0.1',
    author="Jamie Sear",
    description="Unit converter using metres and centermetres",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JamieSear/unit_converter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free For Home Use",
        "Operating System :: OS Independent",
    ],
    # python_requires='>=3.6',
)