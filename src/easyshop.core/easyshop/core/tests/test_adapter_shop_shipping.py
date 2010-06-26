# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IShippingPriceManagement

class TestShopShippingManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestShopShippingManagement, self).afterSetUp()
        self.shop.taxes.invokeFactory("CustomerTax", id="customer", rate=10.0)
        self.sm = IShippingPriceManagement(self.shop)
        
    def testGetShippingPrice(self):
        """
        """
        price = self.sm.getShippingPrice("default")
        self.assertEqual(price.getPrice(), 10.0)
                
    def testGetShippingPrices(self):
        """
        """
        self.shop.shippingprices.invokeFactory("ShippingPrice", "s1")
        self.shop.shippingprices.invokeFactory("ShippingPrice", "s2")
        self.shop.shippingprices.invokeFactory("ShippingPrice", "s3")
        self.shop.shippingprices.invokeFactory("ShippingPrice", "s4")
        
        ids = [p.getId() for p in self.sm.getShippingPrices()]
        self.assertEqual(ids, ["default", "s1", "s2", "s3", "s4"])
                
    def testGetPriceGross(self):
        """
        """
        self.assertEqual(self.sm.getPriceGross(), 10.0)
                
    def testGetTaxRate(self):
        """
        """
        self.assertEqual(self.sm.getTaxRate(), 19.0)
        
    def testGetTaxRateForCustomer(self):
        """
        """
        self.assertEqual(self.sm.getTaxRateForCustomer(), 10.0)
        
    def testGetTax(self):
        """
        """
        self.assertEqual("%.2f" % self.sm.getTax(), "1.60")
                
    def testGetTaxForCustomer_1(self):
        """
        """
        self.assertEqual(self.sm.getTaxForCustomer(), 0)

    def testGetTaxForCustomer_2(self):
        """
        """
        self.login("newmember")
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view.addToCart()
        
        self.assertEqual("%.2f" % self.sm.getTaxForCustomer(), "0.84")

    def testGetPriceNet(self):
        """
        """
        self.assertEqual("%.2f" % self.sm.getPriceNet(), "8.40")
        
    def testGetPriceForCustomer_1(self):
        """
        """
        self.assertEqual(self.sm.getPriceForCustomer(), 0.0)

    def testGetPriceForCustomer_2(self):
        """
        """
        self.login("newmember")
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view.addToCart()
        
        self.assertEqual("%.2f" % self.sm.getPriceForCustomer(), "9.24")
        
    def testCreateTemporaryShippingProduct(self):
        """
        """
        product = self.sm._createTemporaryShippingProduct()
        self.assertEqual(product.getPrice(), 10.0)
        self.assertEqual(product.getId(), "shipping")
                
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShopShippingManagement))
    return suite