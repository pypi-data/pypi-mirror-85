import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dataset-utils",
    version="0.0.3",
    author="Kapil Yedidi",
    author_email="kapily.code@gmail.com",
    description="A few helper utilities to the dataset pip package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kapily/dataset-utils",
    packages=setuptools.find_packages(),
    install_requires=[
        'dataset>=1.3.2,<2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
