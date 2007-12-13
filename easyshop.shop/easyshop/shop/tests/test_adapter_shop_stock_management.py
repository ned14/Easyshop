# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.shop.tests import utils
from easyshop.core.interfaces import IStockManagement

class TestShopStockManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestShopStockManagement, self).afterSetUp()
                
    def testRemoveCart(self):
        """
        """
                
    def testGetStockInformation(self):
        """
        """
        container = self.shop["stock_information"]
        
    def testGetValidStockInformationFor(self):
        """
        """
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShopStockManagement))
    return suite                                               