import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="connect_umls", # Replace with your own username
    version="0.0.1",
    author="Grace Turner",
    author_email="gracekatherineturner@gmail.com",
    description="Make connecting to the UMLS rest APIs easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/gracekatherineturner/umls_connect",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
