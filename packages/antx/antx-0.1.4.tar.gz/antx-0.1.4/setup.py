import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="antx",  # Replace with your own username
    version="0.1.4",
    author="Ngawang Thrinley, Tenzin, Tenzin Kaldan",
    author_email="esukhiadev@gmail.com",
    description="Transfer annotations from source text to destination using diff match patch.",
    py_modules=["antx"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache2",
    url="https://github.com/Esukhia/annotation_transfer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "diff-match-patch==20181111",
        "PyYAML==5.1.2",
        "regex==2020.5.7",
        "requests==2.24.0",
    ],
    python_requires=">=3.6",
    tests_require=["pytest"],
)
