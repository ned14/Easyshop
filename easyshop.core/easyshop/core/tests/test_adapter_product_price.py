# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IPrices

class TestProductPriceCalculation_1(EasyShopTestCase):
    """Customer has same tax rate as default
    """
    def testGetPriceForCustomer(self):
        """Customer has same tax rate as default
        """
        p = IPrices(self.shop.products.product_1)
        self.assertEqual("%.2f" % p.getPriceForCustomer(), "22.00")

    def testGetPriceNet(self):
        """
        """
        p = IPrices(self.shop.products.product_1)
        self.assertEqual("%.2f" % p.getPriceNet(), "18.49")

    def testGetPriceGross(self):
        """
        """
        p = IPrices(self.shop.products.product_1)
        self.assertEqual(p.getPriceGross(), 22.0)

class TestProductPriceCalculation_2(EasyShopTestCase):
    """Customer has other tax rate than default
    """
    def afterSetUp(self):
        """
        """
        super(TestProductPriceCalculation_2, self).afterSetUp()
        self.shop.taxes.invokeFactory("CustomerTax", id="customer", rate=10.0)
        
    def testGetPriceForCustomer(self):
        """
        """
        p = IPrices(self.shop.products.product_1)
        self.assertEqual("%.2f" % p.getPriceForCustomer(), "20.34")
        
    def testGetPriceNet(self):
        """
        """
        p = IPrices(self.shop.products.product_1)
        self.assertEqual("%.2f" % p.getPriceNet(), "18.49")

    def testGetPriceGross(self):
        """
        """
        p = IPrices(self.shop.products.product_1)
        self.assertEqual(p.getPriceGross(), 22.0)
        
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductPriceCalculation_1))
    suite.addTest(makeSuite(TestProductPriceCalculation_2))    
    return suite
                                               