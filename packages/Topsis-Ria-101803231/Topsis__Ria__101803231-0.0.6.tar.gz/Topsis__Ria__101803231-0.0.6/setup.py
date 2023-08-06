import setuptools
with open("README.md", "r") as fh:
    long = fh.read()
setuptools.setup(
    name="Topsis__Ria__101803231",
    packages = ['Topsis_package'],
    version="0.0.6",
    author="Ria",
    author_email="rria_be18@thapar.edu",
    description="it is package which tells you best value based on the data by using some mathematical calculations",
    long_description=long,
    long_description_content_type="text/markdown",
    url="https://github.com/Ria017/Topsis_package",
    install_requires=['pandas','numpy==1.19.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)