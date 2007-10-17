# Zope imports
from DateTime import DateTime

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import IPrices

class TestOrderPriceCalculation(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        utils.createTestEnvironment(self)
        self.login("newmember")                
        utils.createTestOrder(self)
        
    def testGetPriceNet(self):
        """
        """
        p = IPrices(self.order)
        self.assertEqual("%.2f" % p.getPriceNet(), "126.89")
        
    def testGetPriceGross(self):
        """
        """
        p = IPrices(self.order)
        self.assertEqual("%.2f" % p.getPriceGross(), "151.00")

    def testGetPriceForCustomer(self):
        """
        """
        p = IPrices(self.order)
        self.assertEqual("%.2f" % p.getPriceForCustomer(), "151.00")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestOrderPriceCalculation))
    return suite
                                               