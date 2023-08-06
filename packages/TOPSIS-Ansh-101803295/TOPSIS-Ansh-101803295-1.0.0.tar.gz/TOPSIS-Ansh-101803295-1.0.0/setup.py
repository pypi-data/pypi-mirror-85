
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS-Ansh-101803295",
    version="1.0.0",
    author="Ansh Garg",
    author_email="anshgarg7@gmail.com",
    description="The Technique for Order of Preference by Similarity to the Ideal Solution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pandas','numpy==1.19.3'],
    url="https://github.com/anshgarg7/TOPSIS-Ansh-101803295",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
