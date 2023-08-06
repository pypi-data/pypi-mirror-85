import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AnubhavJain", # Replace with your own username
    version="1.0.0",
    author="Anubhav Jain",
    author_email="anubhav.jain1201@gmail.com",
    description="TOPSIS_Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Anubhavjain1201",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)