import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lib-handler-romakot", # Replace with your own username
    version="0.0.1",
    author="romakot",
    author_email="dota234con@mail.ru",
    description="Handler for me",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/romakot321/gamedev",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)