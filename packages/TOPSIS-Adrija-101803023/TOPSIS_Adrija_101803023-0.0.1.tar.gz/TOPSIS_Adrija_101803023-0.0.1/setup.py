import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'TOPSIS_Adrija_101803023',
    version="0.0.1",
    author="Adrija Akriti",
    author_email="adrija.akriti@gmail.com",
    description="package that helps to calculate the topsis score",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)