import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS_Ansh_Gupta_101803121", # Replace with your own username
    version="0.0.4",
    description = 'Implementation of TOPSIS',
    author="Ansh Gupta",
    author_email="agupta2_be18@thapar.edu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PROFESSORRQ/TOPSIS_AnshGupta",
    packages=["TOPSIS_AnshGupta_101803121"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data = True,
    python_requires='>=3.0',
    keywords='topsis pandas rank',
    install_requires=['pandas'],
)
