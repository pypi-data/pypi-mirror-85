import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="comapsmarthome-lambda-decorators",
    version="1.1.1",
    author="Aurélien Sylvan",
    author_email="aurelien.sylvan@comap.eu",
    description="Helpful decorators for aws lambda handler functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
