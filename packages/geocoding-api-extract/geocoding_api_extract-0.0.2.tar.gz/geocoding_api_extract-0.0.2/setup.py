import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geocoding_api_extract",
    version="0.0.2",
    author="Anders Bergman",
    author_email="",
    description="Geocoding api extract to dataframe script.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndoKalrisian/geocoding_api_extract",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pandas','numpy','configparser'],
    license="MIT License"
)
