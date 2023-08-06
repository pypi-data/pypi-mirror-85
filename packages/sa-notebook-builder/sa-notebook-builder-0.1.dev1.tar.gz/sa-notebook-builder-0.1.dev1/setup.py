import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sa-notebook-builder",
    version="0.1.dev1",
    author="András Kohlmann",
    author_email="metuoku@outlook.com",
    description="Building jupyter notebooks from code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andraskohlmann/sa-notebook-builder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
