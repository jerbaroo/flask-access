from setuptools import find_packages, setup

with open("README.md", "r") as f:
    README = f.read()

setup(
    name="flask-access",
    version="0.1.1",
    description="A Flask extension which limits access to views.",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["example"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
        "Intended Audience :: Developers",
    ],
    install_requires=[],
    python_requires=">=3",
)
