import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-bolt",
    version="0.0.8",
    author="geb",
    author_email="853934146@qq.com",
    description="Fast text processing acceleration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikuh/pybolt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'': ['data/*.txt', 'bolt_nlp/count_ngrams']},
    install_requires=['numpy', 'pandas', 'pandarallel'],
    python_requires='>=3.6',
)
