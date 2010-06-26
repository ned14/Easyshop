from setuptools import setup, find_packages

version = '0.1'

setup(name='easymall.mall',
      version=version,
      description="",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Zope, Plone, e-commerce, shop, online-shop, e-shop',
      author='Kai Diefenbach',
      author_email='kai.diefenbach@iqpp.de',
      url='http://iqpp.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['easymall'],
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
