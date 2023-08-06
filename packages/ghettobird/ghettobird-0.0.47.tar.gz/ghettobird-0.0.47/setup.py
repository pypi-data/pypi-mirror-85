import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ghettobird",
    version="0.0.47",
    author="miles-moran",
    author_email="miles-moran@hotmail.com",
    description="Framework/tool for web scraping.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miles-moran/ghetto-bird",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)