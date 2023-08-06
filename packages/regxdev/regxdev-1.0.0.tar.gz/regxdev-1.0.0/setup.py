import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="regxdev",
    version="1.0.0",
    author="Sanjay kumar J",
    author_email='sanjaykumarj222@gmail.com',
    description="This package is made especially for developers or web scrapers for saving time while scraping the information.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mr-elliot/Regx-Dev/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords='re, phone-scrape, finding',
    # install_requires=[
    #       're >= 2.2.0',
    #   ],
    project_urls={ 
        'Bug Reports': 'https://github.com/mr-elliot/Regx-Dev/issues',
        'Source': 'https://github.com/mr-elliot/Regx-Dev/',
    },
)
