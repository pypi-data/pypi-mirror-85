import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="sbcommons",
    version="0.0.50",
    author="Olof Nilsson",
    author_email="olof.nilsson@snusbolaget.se",
    description="Packages shared between lambda functions and other systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Snusbolaget/lambdas",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
