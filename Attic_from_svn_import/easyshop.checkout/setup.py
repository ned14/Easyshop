import os
from setuptools import setup, find_packages

version = "0.1a1"

def read(*pathnames):
    return open(os.path.join(os.path.dirname(__file__), *pathnames)).read()

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
setup(name='easyshop.checkout',
      version=version,
      description="Checkout process for EasyShop",
      long_description='\n'.join([
        read("README.txt"),
        read("docs", "HISTORY.txt"),
      ]),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone e-commerce online-shop',
      author='Kai Diefenbach',
      author_email='kai.diefenbach@iqpp.de',
      url='http://iqpp.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['easyshop'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'easyshop.core',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
