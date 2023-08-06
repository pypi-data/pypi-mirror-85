import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CassavaPy", # Replace with your own username
    version="0.0.10",
    author="Fábio Seixas",
    author_email="flscosta94@gmail.com",
    description="A package to write, run and get outputs from DSSAT-Manihot model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FabioSeixas/CassavaPy",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy>=1.18.0',
        'pandas>=0.25.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
