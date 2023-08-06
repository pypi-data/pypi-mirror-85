import setuptools
 
# with open("README.md", "r") as fh:
#     long_description = fh.read()
 
setuptools.setup(
    #Here is the module name.
    name="TOPSISPANKAJ",
 
    #version of the module
    version="0.0.3",
 
    #Name of Author
    author="Pankaj Gupta",
 
    #your Email address
    author_email="pankaj140699@gmail.com",
 
    #Small Description about module
    description="Multiple Criteria Decision Making using Topsis",
 
    long_description="It will give a Topsis score",
 
    #Specifying that we are using markdown file for description
    # long_description_content_type="text/markdown",

    #Any link to reach this module, if you have any webpage or github profile
    # url="https://github.com/Pushkar-Singh-14/",
    packages=['TOPSISPANKAJ'],
    install_requires=['pandas']
    #classifiers like program is suitable for python3, just leave as it is.
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
)