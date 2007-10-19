# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import IGroupManagement

class TestProductGroupManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestProductGroupManagement, self).afterSetUp()
        self.shop.products.invokeFactory(
            "Product", 
            id="product_3", 
            priceGross=19.0)        
            
        self.product_3 = self.shop.products.product_3
        
    def testHasGroups(self):
        """
        """
        cm = IGroupManagement(self.shop.products.product_1)
        self.assertEqual(cm.hasGroups(), True)

        cm = IGroupManagement(self.shop.products.product_3)
        self.assertEqual(cm.hasGroups(), False)

    def testGetGroups_1(self):
        """
        """
        cm = IGroupManagement(self.shop.products.product_1)
        ids = [g.getId() for g in cm.getGroups()]
        self.assertEqual(ids, ["group_1", "group_2"])
        
    def testGetGroups_2(self):
        """
        """
        cm = IGroupManagement(self.shop.products.product_3)
        self.assertEqual(cm.getGroups(), [])

        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductGroupManagement))
    return suite
                                               