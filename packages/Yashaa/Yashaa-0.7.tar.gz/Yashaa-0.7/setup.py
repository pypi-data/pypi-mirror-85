from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="Yashaa",
    version="0.7",
    description="Topsis technique in a python package",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Yash Singh Pathania",
    author_email="newtoneinstienfarady@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["example-pkg-Yashaa"],
    include_package_data=True,
    install_requires=[
                      'numpy',
                      'pandas'
     ],
     entry_points={
        "console_scripts": [
            "topsis=manpreet.topsis:main",
        ]
     },
)
