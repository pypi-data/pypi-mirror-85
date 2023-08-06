import setuptools
with open("README.md", "r") as fh:
    long = fh.read()
setuptools.setup(
    name="Topsis_RiaSoam-101803258",
    packages = ['topsis_pckg'],
    version="0.0.6",
    author="Ria Soam",
    author_email="rsoam_be18@thapar.edu",
    description="it is package which tells you best value based on the data by applying accurate mathematics functions",
    long_description=long,
    long_description_content_type="text/markdown",
    url="https://github.com/ria-2511/topsis_pckg",
    install_requires=['pandas','numpy==1.19.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)