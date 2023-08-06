import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="valorant",
    version="0.1.2",
    author="IreTheKID",
    author_email="author@example.com",
    description="An unofficial synchronous client package for interacting with Riot Games' Valorant API endpoints.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IreTheKID/valorant.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)