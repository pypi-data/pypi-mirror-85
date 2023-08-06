import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mfem", # Replace with your own username
    version="0.0.2",
    author="MFEM developement team",
    author_email="shiraiwa@princeton.edu",
    description="MFEM and python wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mfem",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
