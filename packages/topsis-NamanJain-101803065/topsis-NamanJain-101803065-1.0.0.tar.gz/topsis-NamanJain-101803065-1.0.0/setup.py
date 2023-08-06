import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topsis-NamanJain-101803065",
    version="1.0.0",
    author="Naman Jain",
    author_email="namanjain24682468@gmail.com",
    description="Decision Making using topsis (Python Package)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/namanjain323232/topsis',
    download_url = 'https://github.com/namanjain323232/topsis/archive/1.0.0.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=[            
          'pandas',
          'numpy'
      ],
    classifiers=[
      'License :: OSI Approved :: MIT License', 
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.7'
    ],
)