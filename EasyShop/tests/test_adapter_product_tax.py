# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import ITaxes

class TestProductTaxCalculation(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        utils.createTestEnvironment(self)
        self.shop.taxes.invokeFactory("EasyShopCustomerTax", id="customer", rate=10.0)
        
    def testGetTaxRate(self):
        """
        """
        t = ITaxes(self.product_1)
        self.assertEqual(t.getTaxRate(), 19.0)
        
    def testGetTaxRateForCustomer(self):
        """
        """
        t = ITaxes(self.product_1)
        self.assertEqual(t.getTaxRateForCustomer(), 10.0)

    def testGetTax(self):
        """
        """
        t = ITaxes(self.product_1)
        self.assertEqual("%.2f" % t.getTax(), "3.51")
        
    def testGetTaxForCustomer(self):
        """
        """
        t = ITaxes(self.product_1)
        self.assertEqual("%.2f" % t.getTaxForCustomer(), "1.85")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductTaxCalculation))
    return suite
                                               