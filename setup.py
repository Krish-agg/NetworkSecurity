'''
The setup.py file is an essential part of packaging and distributing Python projects. 
It is used by setuptools (or distutils in older Python versions) to define the configuration of your project,
 such as its metadata, dependencies, and more
'''
from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """
    This function reads a requirements file and returns a list of required packages.
    
    """
    try:
        with open(file_path) as file:
            requirements = file.readlines()
            requirements = [req.strip() for req in requirements]
            requirements = [req for req in requirements if req and not req.startswith('#') and req != '-e .']
        return requirements
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")    


setup(
    name='NetowrkSecurity-ML',
    version='0.0.1',
    authoe='Krish Aggarwal',
    author_email='akrish620@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    description='A project for Network Security using Machine Learning',
)
       