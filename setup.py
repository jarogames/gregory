import os
from setuptools import setup
import subprocess
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

### read :  to read README.md for description -  copy paste
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


### package_files: to attach all irellevent files in directory: eg.in.NuPhyPy
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths
extra_files = package_files('mymod/') # i did this with NuPhy


#############   if you want to version git and setup be the same #########
# git tag -a v$(python setup.py --version) -m '   '


### OR - CopyPaste from http://blogs.nopcode.org/brainstorm/2013/05/20/pragmatic-python-versioning-via-setuptools-and-git-tags/
### store version in (annotated) GIT:  git tag -a v0.0.3
version_py = os.path.join(os.path.dirname(__file__), 'version.py')
try:
    version_git = subprocess.check_output(["git", "describe"]).decode("utf8").rstrip()
    print("D... version=", version_git)
except:
    with open(version_py, 'r') as fh:
        version_git = open(version_py).read().strip().split('=')[-1].replace('"','')
version_msg="# Do not edit this file, pipeline versioning is governed by git tags"
with open(version_py, 'w') as fh:
    fh.write(version_msg + str(os.linesep) + "__version__=" + version_git)

################################
#
# MAIN PART
#
#################################

setup(
    name = "gregory",
    version="{ver}".format(ver=version_git),  # this comes from http://blogs.nopcode.org/brainstorm/2013/05/20/pragmatic-python-versioning-via-setuptools-and-git-tags/
    #version = "0.0.2b",
    zip_safe= False,
    author = "jaromir mrazek",
    author_email = "jaromrax@gmail.com",
    description = ("Gregory will be a system of services in userspace"
                  ),
    license = "GPLv2",
    keywords = "python",
    url = "",
    #package_dir = {'': 'mymod'},
    py_modules=['mymod'],
    packages=['gregory.mymod','gregory','gregory.gps','gregory.pi','gregory.pi'],
    scripts=['bin/gps.py','bin/keypress.py','bin/pureborg.py','bin/pigory.py'],
    package_data={'':extra_files},  # this I did with NuPhyPy ... [ok]
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
)
