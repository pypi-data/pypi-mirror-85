from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="fileargs",        
    version="0.2",
    author="AlessioM",
    author_email="none@example.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/AlessioM/fileargs",
    packages=find_packages(),    
    install_requires=[        
        "Jinja2>=2.11.2",
        "PyYAML>=5.3.1", 
        "configparser>=5.0.1"       
    ],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],    
    entry_points='''
        [console_scripts]
        fileargs=fileargs.command_line:main        
    '''    
)
