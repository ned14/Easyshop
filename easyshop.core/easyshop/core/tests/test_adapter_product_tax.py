# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ITaxes

class TestProductTaxCalculation(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestProductTaxCalculation, self).afterSetUp()
        self.shop.taxes.invokeFactory("CustomerTax", id="customer", rate=10.0)
        
    def testGetTaxRate(self):
        """
        """
        t = ITaxes(self.shop.products.product_1)
        self.assertEqual(t.getTaxRate(), 19.0)
        
    def testGetTaxRateForCustomer(self):
        """
        """
        t = ITaxes(self.shop.products.product_1)
        self.assertEqual(t.getTaxRateForCustomer(), 10.0)

    def testGetTax(self):
        """
        """
        t = ITaxes(self.shop.products.product_1)
        self.assertEqual("%.2f" % t.getTax(), "3.51")
        
    def testGetTaxForCustomer(self):
        """
        """
        t = ITaxes(self.shop.products.product_1)
        self.assertEqual("%.2f" % t.getTaxForCustomer(), "1.85")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductTaxCalculation))
    return suite
                                               