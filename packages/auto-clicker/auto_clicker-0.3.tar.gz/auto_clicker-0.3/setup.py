import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auto_clicker", # Replace with your own username
    version="0.3",
    author="Finn Pfaff",
    author_email="pfaff_finn@yahoo.com",
    description="You can search for images on your screen and then click, hover or press them.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Warfare03/auto_clicker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
