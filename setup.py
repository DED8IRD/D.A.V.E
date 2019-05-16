import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="DAVE_bot_DED8IRD",
    version="1.0.1",
    author="Eunika Wu",
    author_email="eunika@pdxcodeguild.com",
    description="A screenplay bot",
    long_description=__doc__,
    long_description_content_type="text/markdown",
    url="https://github.com/DED8IRD/D.A.V.E",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
    # install_requires=[
    #     'beautifulsoup4==4.7.1',
    #     'certifi==2018.11.29',
    #     'chardet==3.0.4',
    #     'Click==7.0',
    #     'Flask==1.0.2',
    #     'fpdf==1.7.2',
    #     'idna==2.8',
    #     'itsdangerous==1.1.0',
    #     'Jinja2==2.10.1',
    #     'markovify==0.7.1',
    #     'MarkupSafe==1.1.0',
    #     'pytz==2018.9',
    #     'requests==2.21.0',
    #     'soupsieve==1.8',
    #     'Unidecode==1.0.23',
    #     'urllib3==1.24.1',
    #     'Werkzeug==0.14.1',
    # ]