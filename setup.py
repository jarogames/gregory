import os
from setuptools import setup
#
#   python3 setup.py install --user
#-------- results in:
#/home/ojr/.local/lib/python3.5/site-packages/gregory-0.0.1a0-py3.5.egg/mymod
# because  gps.py is copied to .local/bin/   u can run gps.py from wherever
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
#modules=[]    #  single files in root dir
#
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

#packages=['mymod']   #  directory with __init__.py
#py_modules=['mymod.mymod']
extra_files = package_files('mymod/') # i did this with nuphy
#
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
    #package_dir = {'': 'mymod'},
    #py_modules=['mymod.mymod'],
    packages=['mymod','gregory','gregory.gps'],
    scripts=['bin/gps.py'],
    package_data={'':extra_files},
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
)
