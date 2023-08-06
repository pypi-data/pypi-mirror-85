import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="TOPSIS-Karan-101853003",
    version="1.0.0",
    description="Topsis score calculator",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/KARANQUERNMADAVIDE/TOPSIS-Karan-101853003",
    author="Karan Madan",
    author_email="kmadan_be18@thapar.edu",
    license="MIT",
    classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers', 
          'Topic :: Software Development :: Build Tools',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["tk1"],
    include_package_data=True,
    install_requires=["pandas"],
    keywords = ['topsis', 'thapar', 'rank', 'topsis score'], 
    
)