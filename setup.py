import os
from setuptools import setup

#############
# JM now I blindly copy some setup.py
############ MANUALS 
#https://pythonhosted.org/an_example_pypi_project/setuptools.html
#https://pypi.python.org/pypi?%3Aaction=list_classifiers
################# install from git repo #############
# pip install git+git://github.com/username/testpyrepo@master
############# this included all files ##############
#http://stackoverflow.com/questions/27664504/how-to-add-package-data-recursively-in-python-setup-py
##

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
##########################################################
#packages=[]   #  directory with __init__.py
#modules=[]    #  single files in root dir
#
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('mymod/')

############   if you want to version git and setup be the same #########
# git tag -a v$(python setup.py --version) -m '   '

setup(
    name = "gregory",
    version = "0.0.1a",
    zip_safe= False,
    author = "jaromir mrazek",
    author_email = "jaromrax@gmail.com",
    description = ("Gregory will be a system of services in userspace"
                                   " ....."),
    license = "GPLv2",
    keywords = "python",
    url = "",
    packages=['mymod'],
    package_data={'':extra_files},
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
)
