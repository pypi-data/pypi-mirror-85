import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airtable-cacher",
    version="1.2.3",
    author="thuxley",
    author_email="thomas.huxley90@gmail.com",
    description="Utility for caching api responses from the airtable-python-wrapper based on airtable-caching by "
                "rmountjoy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bawpcwpn/AirtableCacher",
    install_requires=["airtable-python-wrapper"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
