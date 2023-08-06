
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS-Brijeshwar-101803170",
    version="1.0.0",
    author="Brijeshwar Singh",
    author_email="brijeshwar11singh@gmail.com",
    description="A package that makes it easy to implement TOPSIS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 
