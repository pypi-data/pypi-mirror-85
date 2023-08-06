import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="textencryptor", 
    version="0.0.1",
    author="Andrew Mummery",
    author_email="andrew.mummery.software@gmail.com",
    description="A small package which encrypts plain text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewmummery/TextEncryptor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)