import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.readlines()

setuptools.setup(
    name="davebot",
    version="1.0.0",
    author="Eunika Wu",
    author_email="eunika@pdxcodeguild.com",
    description="A screenplay bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DED8IRD/D.A.V.E",
    packages=[
        'DAVE',
        'DAVE.nlp',
        'DAVE.scraper',
    ],    
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requries=requirements,
)