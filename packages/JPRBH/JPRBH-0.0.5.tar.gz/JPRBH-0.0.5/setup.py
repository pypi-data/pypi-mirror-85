import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JPRBH",
    version="0.0.5",
    author="John Patrick Roach",
    author_email="contact@johnpatrickroach.com",
    description="JPR Bayesian Health Code Test Submission",
    url="https://github.com/johnpatrickroach/JPRBH",
    packages=setuptools.find_packages(

    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
