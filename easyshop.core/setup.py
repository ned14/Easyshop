import os
from setuptools import setup, find_packages

version = '0.1a1'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

setup(name='easyshop.core',
      version=version,
      description="An out-of-the-box online shop for Plone.",
      long_description=README,
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
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
          # -*- Extra requirements: -*-
          "easyshop.carts",
          "easyshop.catalog",
          "easyshop.checkout",
          "easyshop.criteria",
          "easyshop.customers",
          "easyshop.discounts",
          "easyshop.groups",
          "easyshop.information",
          "easyshop.kss",
          "easyshop.login",
          "easyshop.management",
          "easyshop.order",
          "easyshop.payment",
          "easyshop.shipping",
          "easyshop.shop",
          "easyshop.stocks",
          "easyshop.taxes",
          "zc.authorizedotnet",
          "Products.DataGridField"          
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )