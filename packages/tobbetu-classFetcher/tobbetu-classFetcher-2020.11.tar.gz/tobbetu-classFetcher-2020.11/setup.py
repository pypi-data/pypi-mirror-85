import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tobbetu-classFetcher", # Replace with your own username
    version="2020.11",
    author="Ufuk Karaca",
    author_email="ufukqarca@gmail.com",
    description="A simple library to fetch class Zoom links from the TOBB ETU class portal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ufukkaraca/tobbetu-classFetcher",
    packages=setuptools.find_packages(),
    install_requires=['selenium',],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)