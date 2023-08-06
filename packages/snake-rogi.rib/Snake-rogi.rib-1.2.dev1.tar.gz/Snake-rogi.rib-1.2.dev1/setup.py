import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Snake-rogi.rib", # Replace with your own username
    version="1.2.dev1",
    author="Igor Ribeiro de Souza",
    author_email="igor.r.souza@hotmail.com",
    description="The famous game snake, built with python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/igor-rib-souza/Snake",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
