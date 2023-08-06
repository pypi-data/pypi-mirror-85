import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    #Here is the module name.
    name="neji",
 
    #version of the module
    version="0.0.1.0",
 
    #Name of Author
    author="Viraj Neji",
 
    #your Email address
    author_email="unanneji@gmail.com",
 
    #Small Description about module
    description="Cloud Storage and GUI Framework",

    # Required installments
    install_requires=[
        'requests',
        'whichcraft'
    ],
    
    packages=['neji'],

    long_description=long_description,
 
    #Specifying that we are using markdown file for description
    long_description_content_type="text/markdown",
 
     
    #classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)