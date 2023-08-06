import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cheap-local-websites-services",
    version="0.0.1",
    author="John",
    author_email="john@cheaplocalwebsites.com",
    description="This small application creates a page for a dynamic list of services populated from the admin model.",
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
