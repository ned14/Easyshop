# -*- coding: utf-8 -*-
"""
This module contains the tool of easyshop.coupon
"""
import os
from setuptools import setup, find_packages
from xml.dom.minidom import parse


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


def readversion():
    mdfile = os.path.join(os.path.dirname(__file__), 'easyshop', 'coupon',
                          'profiles', 'default', 'metadata.xml')
    metadata = parse(mdfile)
    assert metadata.documentElement.tagName == "metadata"
    return metadata.getElementsByTagName("version")[0].childNodes[0].data

long_description = (
    read('docs','README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('docs','HISTORY.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('docs','CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n')

tests_require=['zope.testing']

setup(name='easyshop.coupon',
      version=readversion(),
      description="",
      long_description=long_description,
      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='petschki',
      author_email='pedrotschki@gmail.com',
      url='http://svn.plone.org/svn/plone/plone.example',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['easyshop', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'collective.monkeypatcher',
        'plone.app.z3cform',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'easyshop.coupon.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list

      [egg_info.writers]
      paster_plugins.txt = setuptools.command.egg_info:write_arg
      """,
      paster_plugins = ["ZopeSkel"],
      )
