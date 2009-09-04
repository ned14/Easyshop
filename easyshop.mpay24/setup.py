import os
from setuptools import setup, find_packages
from xml.dom.minidom import parse

def readversion():
    mdfile = os.path.join(os.path.dirname(__file__), 'easyshop', 'mpay24', 'profiles', 'default', 'metadata.xml')
    metadata = parse(mdfile)
    assert metadata.documentElement.tagName == "metadata"
    return metadata.getElementsByTagName("version")[0].childNodes[0].data

def read(*pathnames):
    return open(os.path.join(os.path.dirname(__file__), *pathnames)).read()

setup(name='easyshop.mpay24',
      version=readversion().strip(),
      description="",
      long_description='\n'.join([
        read("docs", "README.txt"),
        read("docs", "HISTORY.txt"),
      ]),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['easyshop'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
