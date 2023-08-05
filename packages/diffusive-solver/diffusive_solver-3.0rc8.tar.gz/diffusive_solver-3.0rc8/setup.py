import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "diffusive_solver",
    version = "3.0rc8",
    author = "Iacopo Torre",
    author_email = "iacopo.torre@icfo.eu",
    description = "Package for solving systems of coupled diffusion equations",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitlab.com/itorre/diffusive_solver",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research"
    ],
    python_requires = '>=3.6',
    install_requires = ['numpy','matplotlib','meshio'],

)