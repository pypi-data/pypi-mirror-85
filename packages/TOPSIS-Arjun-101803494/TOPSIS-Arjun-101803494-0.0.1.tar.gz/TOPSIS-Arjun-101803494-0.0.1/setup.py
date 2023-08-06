from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="TOPSIS-Arjun-101803494",
    version="0.0.1",
    py_modules = ["topsis"],
    description="Python Package for TOPSIS",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Arjun Shoor",
    author_email="aarjun_be18@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["TOPSIS-Arjun-101803494"],
    include_package_data=True,
    install_requires=["requests"],
    
)

