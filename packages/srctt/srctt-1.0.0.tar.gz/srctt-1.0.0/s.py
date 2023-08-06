from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="srctt",
    version="1.0.0",
    description="A Python package to get the the topsis score and rank",
    long_description=readme(),
    long_description_content_type="text/markdown",
    
    author="Shruti Agrawal",
    #author_email="ni97@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["srctt"],
    include_package_data=True,
    install_requires=["requests","pandas","numpy"],
    entry_points={
        "console_scripts": [
            "Trail=srctt.topsis:main",
        ]
    },
)