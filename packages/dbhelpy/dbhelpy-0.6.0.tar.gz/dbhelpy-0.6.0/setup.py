import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dbhelpy",
    version="0.6.0",
    author="Angel Davila",
    author_email="adavila0703@gmail.com",
    description="dbhelpy is an easy to use Python library that allows you to interact with your sqlite database using "
                "dbhelpy methods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adavila0703/dbhelpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)