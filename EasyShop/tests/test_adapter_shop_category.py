# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import ICategoryManagement

class TestShopCategoryManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        utils.createTestEnvironment(self)

    def testHasCategories(self):
        """
        """
        cm = ICategoryManagement(self.shop)
        self.assertEqual(cm.hasCategories(), True)
        
        ids = self.shop.categories.objectIds()
        self.shop.categories.manage_delObjects(ids)
        self.assertEqual(cm.hasCategories(), False) 
               
    def testHasParentCategory(self):
        """
        """
        cm = ICategoryManagement(self.shop)
        self.assertEqual(cm.hasParentCategory(), False)
        
    def testGetCategories(self):
        """
        """        
        cm = ICategoryManagement(self.shop)
        ids = [c.getId() for c in cm.getCategories()]
            
        self.failUnless("category_1"   in ids)
        self.failUnless("category_2"   in ids)        
        self.failUnless("category_11"  in ids)
        self.failUnless("category_111" in ids)
        
    def testGetTopLevelCategories(self):
        """
        """ 
        cm = ICategoryManagement(self.shop)
        ids = [c.getId for c in cm.getTopLevelCategories()]
        
        self.assertEqual(ids, ["category_1", "category_2"])
        
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShopCategoryManagement))
    return suite