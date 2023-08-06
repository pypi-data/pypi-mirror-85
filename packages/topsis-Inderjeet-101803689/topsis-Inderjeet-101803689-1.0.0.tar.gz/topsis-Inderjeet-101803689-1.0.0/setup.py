import setuptools
with open("README.md", "r") as f:
    long = f.read()
setuptools.setup(
    name="topsis-Inderjeet-101803689",
    packages = ['topsis_package'],
    version="1.0.0",
    author="Inderjeet Singh",
    author_email="inder052000@gmail.com",
    description="It is package which is used to find best among the value using mathematical model(topsis)",
    long_description=long,
    long_description_content_type="text/markdown",
    url="https://github.com/inder052000/topsis_package",
    install_requires=['pandas','numpy==1.19.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)