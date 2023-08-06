import setuptools
 
with open("readme.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    #Here is the module name.
    name="topsis_Vinay_101803108",
 
    #version of the module
    version="0.0.1",
 
    #Name of Author
    author="Vinay Singh",
 
    #your Email address
    author_email="singh.v357@gmail.com",
 
    #Small Description about module
    description="TOPSIS Package to rank different models",
 
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