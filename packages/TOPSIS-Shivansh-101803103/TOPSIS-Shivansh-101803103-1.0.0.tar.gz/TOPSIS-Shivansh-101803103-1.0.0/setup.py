# import setuptools
 
# with open("README.md", "r") as fh:
#     long_description = fh.read()

# setuptools.setup(
#     #Here is the module name.
#     name="TOPSIS-SHIVANSH-101803103",
 
#     #version of the module
#     version="0.0.1",

#     #Name of Author
#     author="Shivansh Kumar",
 
#     #your Email address
#     author_email="skumar_be18@thapar.edu",
 
#     #Small Description about module
#     description="Python Package for TOPSIS",
 
#     long_description=long_description,
 
#     #Specifying that we are using markdown file for description
#     long_description_content_type="text/markdown",
 
#     packages=setuptools.find_packages(),
 
#     #classifiers like program is suitable for python3, just leave as it is.
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
# )
from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="TOPSIS-Shivansh-101803103",
    version="1.0.0",
    description="Python Package for TOPSIS",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Shivansh Kumar",
    author_email="skumar_be18@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["TOPSIS-SHIVANSH-101803103"],
    include_package_data=True,
    install_requires=["requests"],
    
)