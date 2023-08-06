
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS-Rohan-101803151",
    version="1.0.1",
    author="",
    author_email="",
    description="A package that makes it easy to create Pypi packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/duttrohan0302/TOPSIS-Rohan-101803151',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/duttrohan0302/TOPSIS-Rohan-101803151/archive/v_01.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=[
          'numpy',
          'pandas',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 
