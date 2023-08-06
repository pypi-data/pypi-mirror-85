from setuptools import setup, find_packages

def readme():
    with open('C:\\Users\\PARAS\\Desktop\\New Folder\\TOPSIS-Paras-101983048\\Readme.txt') as f:
        README = f.read()
    return README

setup(
    name= "TOPSIS-Paras-101983048", 
    version="1.0.1", 
    long_description=readme(),
    packages=["topsis_create"],
    include_package_data=True,
    install_requires=["pandas" , "numpy"]
)