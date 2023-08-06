import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    #Here is the module name.
    name="TOPSIS-Utkarsh-101803419",
 
    #version of the module
    version="1.0",
 
    #Name of Author
    author="Utkarsh Sharma",
 
    #your Email address
    author_email="usharma1_be18@thapar.edu",
 
    #Small Description about module
    description="Package for ranking multiple components based on TOPSIS calculation",
 
    long_description=long_description,
 
    #Specifying that we are using markdown file for description
    long_description_content_type="text/markdown",
 
    #Any link to reach this module, if you have any webpage or github profile
    #url="https://github.com/Pushkar-Singh-14/",
    packages=setuptools.find_packages(),
 
    #classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
