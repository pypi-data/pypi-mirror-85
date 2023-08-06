from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="TOPSIS-PARNEET-101803281",
    packages=["TOPSIS-PARNEET-101803281"],
    version="0.1",
    description="TOPSIS IMPLEMENTAION python package ",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/parneetpp/Topsis-implementstion",
    download_url="https://github.com/parneetpp/Topsis-implementstion/archive/v_01.tar.gz",
    author="Parneet Singh",
    author_email="psingh3_be18@thapar.edu",
    license="MIT",
    keywords = ['IMPLEMENTATION','TOPSIS','PYTHON'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    install_requires=[
                      'numpy',
                      'pandas'
    
        ],

)
