import setuptools
 
with open("readme.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    #Here is the module name.
    name="topsis_simran_101803100",
 
    #version of the module
    version="1.0.2",
 
    #Name of Author
    author="Simran Jot Kaur",
 
    #your Email address
    author_email="simranjotkaur82@gmail.com",
 
    #Small Description about module
    description="Compare different models using performance score",
 
    long_description=long_description,
 
    #Specifying that we are using markdown file for description
    long_description_content_type="text/markdown",
 
    #Any link to reach this module, if you have any webpage or github profile
    packages=setuptools.find_packages(),
 
    #classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)