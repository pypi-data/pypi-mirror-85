
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS_Sheramir_101803549",
    version="1.0.1",
    author="Sheramir",
    author_email="sheramir51@gmail.com",
    description="This package is for TOPSIS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pandas','numpy==1.19.3'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
