# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICategoryManagement

class TestShopCategoryManagement(EasyShopTestCase):
    """
    """
    def testGetCategories(self):
        """
        """        
        cm = ICategoryManagement(self.shop)
        ids = [c.id for c in cm.getCategories()]

        self.failUnless("category_1"   in ids)
        self.failUnless("category_2"   in ids)        
        self.failUnless("category_11"  in ids)
        self.failUnless("category_111" in ids)
        
    def testGetTopLevelCategories(self):
        """
        """
        cm = ICategoryManagement(self.shop)
        ids = [c.id for c in cm.getTopLevelCategories()]
        
        self.assertEqual(ids, ["category_1", "category_2", "category_3"])
        
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShopCategoryManagement))
    return suite