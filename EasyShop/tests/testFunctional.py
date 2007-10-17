"""EasyShop functional doctests.  This module collects all *.txt files in the
tests directory and runs them. (stolen from Ploneboard, which has it stolen 
from Plone)
"""

import os, sys

import glob
import doctest
import unittest
from Globals import package_home
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

from Products.EasyShop.config import product_globals

# Load products
from Products.EasyShop.tests.base import EasyShopFunctionalTestCase

REQUIRE_TESTBROWSER = ['func_add_product.txt']

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def list_doctests():
    home = package_home(product_globals)
    return [filename for filename in
            glob.glob(os.path.sep.join([home, 'tests', '*.txt']))]

def list_nontestbrowser_tests():
    return [filename for filename in list_doctests()
            if os.path.basename(filename) not in REQUIRE_TESTBROWSER]

def test_suite():

    # BBB: We can obviously remove this when testbrowser is Plone
    #      mainstream, read: with Five 1.4.
    try:
        import Products.Five.testbrowser
    except ImportError:
        print >> sys.stderr, ("WARNING: testbrowser not found - you probably"
                              "need to add Five 1.4 to the Products folder. "
                              "testbrowser tests skipped")
        filenames = list_nontestbrowser_tests()
    else:
        filenames = list_doctests()

    return unittest.TestSuite(
        [Suite(os.path.basename(filename),
               optionflags=OPTIONFLAGS,
               package='Products.EasyShop.tests',
               test_class=EasyShopFunctionalTestCase)
         for filename in filenames]
        )