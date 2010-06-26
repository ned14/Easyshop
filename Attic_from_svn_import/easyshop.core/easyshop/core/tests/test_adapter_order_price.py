# Zope imports
from DateTime import DateTime

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IPrices

class TestOrderPriceCalculation(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestOrderPriceCalculation, self).afterSetUp()                        
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