import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lazy-network-engineer-jaaacck",
    version="0.1a0",
    author="Jack Houlden",
    author_email="xjackh@gmail.com",
    description="Lots of scripts and APIs bundled together in one easy to use CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaaacck/lazy-network-engineer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.2',
)