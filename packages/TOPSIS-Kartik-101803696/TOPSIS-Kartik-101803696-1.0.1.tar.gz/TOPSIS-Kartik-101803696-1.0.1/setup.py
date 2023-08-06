
from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="TOPSIS-Kartik-101803696",
    version="1.0.1",
    description="A Python package to get best out of various features using TOPSIS.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Kartik-Bhardwaj192/topsis",
    author="Kartik Bhardwaj",
    author_email="kbhardwaj_be18@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["Topsis_Kartik_101803696"],
    include_package_data = True,
    install_requires=["sys","os","pandas","numpy","scipy"],
    
    
)
