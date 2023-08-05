import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="srenamer",
    version="0.1.0",
    description="This is a simple file renamer for TV shows and anime.",
    author="Maxim Makovskiy",
    author_email="makovskiyms@gmail.com",
    url="https://github.com/evorition/srenamer",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["srenamer"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["requests"],
    entry_points={"console_scripts": ["srenamer=srenamer.__main__:main"]},
    python_requires=">=3.6",
)
