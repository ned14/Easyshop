from Testing.ZopeTestCase import FunctionalDocFileSuite
from Globals import package_home
from base import EasyShopFunctionalTestCase
from unittest import TestSuite
from os.path import join, split
from os import walk
from re import compile
from sys import argv

if '-t' in argv:
    pattern = compile('.*\.(txt|rst)$')
else:
    pattern = compile('(^test.*|/test[^/]*)\.(txt|rst)$')

# we collect all matching doctests in docs/
tests = []
docs = join(package_home(globals()), '../docs/')

for path, dirs, files in walk(docs, topdown=False):
    for name in files:
        relative = join(path, name)[len(docs):]
        if not '.svn' in split(path) and pattern.search(relative):
            tests.append(relative)

def test_suite():
    suite = TestSuite()
    for test in tests:
        suite.addTest(FunctionalDocFileSuite(test,
            package="easyshop.shop.docs",
            test_class=EasyShopFunctionalTestCase))
    return suite

