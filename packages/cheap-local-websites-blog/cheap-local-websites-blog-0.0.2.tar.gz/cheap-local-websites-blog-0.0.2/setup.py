import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cheap-local-websites-blog",
    version="0.0.2",
    author="John",
    author_email="john@cheaplocalwebsites.com",
    description="A dynamic blog application including rss feed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.cheaplocalwebsites.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
