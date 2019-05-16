import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DAVE_bot_DED8IRD",
    version="1.0.1",
    author="Eunika Wu",
    author_email="eunika@pdxcodeguild.com",
    description="A screenplay bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DED8IRD/D.A.V.E",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)