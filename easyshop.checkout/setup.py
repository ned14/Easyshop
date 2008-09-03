import os
from setuptools import setup, find_packages

version = '0.1a1'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
setup(name='easyshop.checkout',
      version=version,
      description="Checkout process for EasyShop",
      long_description= README,      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Kai Diefenbach',
      author_email='kai.diefenbach@iqpp.de',
      url='http://svn.plone.org/svn/plone/plone.example',
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
