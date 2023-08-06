from setuptools import setup, find_namespace_packages

setup(
    name="fileargs",
    version="0.1",
    author="AlessioM",
    author_email="none@example.com",
    url="",
    packages=find_namespace_packages(include=['fileargs.*']),
    package_dir={'':'src'},
    install_requires=[
        "click>=7.1.2",
        "Jinja2>=2.11.2",
        "PyYAML>=5.3.1", 
        "configparser>=5.0.1"       
    ],
    extras_require={},
    setup_requires=[],
    python_requires='>=3.7',
    test_suite='tests',
    tests_require=[],
    zip_safe=False,
    include_package_data=True,
    entry_points='''
        [console_scripts]
        fileargs=fileargs.command_line:main        
    '''    
)
