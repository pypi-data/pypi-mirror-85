import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-crtsh",
    version="0.0.3",
    author="Plant Daddy",
    author_email="CqP5TZ77NYBf5uQt@protonmail.com",
    description="A simple package to do basic queries of crt.sh",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PlantDaddy/py-crtsh",
    license="BSD",
    install_requires=['scrapy', 'requests'],
    packages=setuptools.find_packages(),
    project_urls={'Tracker': 'https://github.com/PlantDaddy/py-crtsh'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)