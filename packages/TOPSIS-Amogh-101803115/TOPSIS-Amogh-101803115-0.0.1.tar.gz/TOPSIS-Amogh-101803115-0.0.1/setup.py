from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="TOPSIS-Amogh-101803115",
    version="0.0.1",
    py_modules = ["topsis"],
    description="Python Package for TOPSIS",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Amogh Mittal",
    author_email="amoghmittal16@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["TOPSIS-Amogh-101803115"],
    include_package_data=True,
    install_requires=["requests"],
    
)

