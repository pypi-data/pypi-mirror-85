import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    #Here is the module name.
    name="TOPSIS-Vedant-101803329",
 
    #version of the module
    version="1",
 
    #Name of Author
    author="Vedant Gupta",
 
    #your Email address
    author_email="vgupta2_be18@thapar.edu",
 
    #Small Description about module
    description="Topsis Calculator",
 
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
