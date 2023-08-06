import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aquariumlearning",  # Replace with your own username
    version="0.0.15",
    author="Quinn Johnson",
    author_email="quinn@aquarium-learn.com",
    description="Aquarium Learning Python Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.aquariumlearning.com",
    packages=setuptools.find_packages(
        include=["aquariumlearning", "aquariumlearning.*"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests==2.23.0",
        "pyarrow==0.17.1",
        "pandas==1.1.4",
        "numpy==1.19.4",
        "google-resumable-media==1.1.0",
    ],
)
