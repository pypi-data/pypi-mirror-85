import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cheap-local-websites-booking",
    version="0.0.1",
    author="John",
    author_email="john@cheaplocalwebsites.com",
    description="A Web App to collects and store lead contact info",
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
