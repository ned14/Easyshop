# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.shop.tests import utils
from easyshop.core.interfaces import ITaxes
from easyshop.core.interfaces import ITax
from easyshop.core.interfaces import ITaxManagement

class TestShopTaxManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestShopTaxManagement, self).afterSetUp()
        self.shop.taxes.invokeFactory("DefaultTax", "d1")
        self.shop.taxes.invokeFactory("DefaultTax", "d2")
        self.shop.taxes.invokeFactory("DefaultTax", "d3")
        self.shop.taxes.invokeFactory("DefaultTax", "d4")

        self.shop.taxes.invokeFactory("CustomerTax", "c1", rate=10)
        self.shop.taxes.invokeFactory("CustomerTax", "c2")
        self.shop.taxes.invokeFactory("CustomerTax", "c3")
        self.shop.taxes.invokeFactory("CustomerTax", "c4")
                
    def testGetCustomerTaxes(self):
        """
        """        
        tm = ITaxManagement(self.shop)
        ids = [t.getId() for t in tm.getCustomerTaxes()]
        
        self.assertEqual(ids, ["c1", "c2", "c3", "c4"])

    def testGetDefaultTaxes(self):
        """
        """
        tm = ITaxManagement(self.shop)
        ids = [t.getId() for t in tm.getDefaultTaxes()]
        
        self.assertEqual(ids, ["default", "d1", "d2", "d3", "d4"])
                    
    def getTax(self, id):
        """
        """
        tm = ITaxManagement(self.shop)
        tax = tm.getTax("c2")
        
        self.assertEqual(tax.getId(), "c2")
        self.failUnless(ITax.providedBy(tax))
        
class TestShopTaxes(EasyShopTestCase):
    """
    """
    def testGetTax(self):
        """
        """
        tm = ITaxes(self.shop)
        tax = tm.getTax(self.product_1)
        self.assertEqual("%.2f" % tax, "3.51")

    def testGetTaxForCustomer_1(self):
        """Without tax rate for customer
        """
        tm = ITaxes(self.shop)
        tax = tm.getTaxForCustomer(self.product_1)
        self.assertEqual("%.2f" % tax, "3.51")

    def testGetTaxForCustomer_2(self):
        """With tax rate for customer
        """
        self.shop.taxes.invokeFactory("CustomerTax", id="customer", rate=10.0)        
        tm = ITaxes(self.shop)
        tax = tm.getTaxForCustomer(self.product_1)
        self.assertEqual("%.2f" % tax, "1.85")

    def testGetTaxRate(self):
        """
        """
        tm = ITaxes(self.shop)
        rate = tm.getTaxRate(self.product_1)
        self.assertEqual(rate, 19.0)

    def testGetTaxRateForCustomer_1(self):
        """Without tax rate for customer
        """
        tm = ITaxes(self.shop)
        rate = tm.getTaxRateForCustomer(self.product_1)
        self.assertEqual(rate, 19.0)

    def testGetTaxRateForCustomer_2(self):
        """With tax rate for customer
        """
        self.shop.taxes.invokeFactory("CustomerTax", id="customer", rate=10.0)
        tm = ITaxes(self.shop)
        rate = tm.getTaxRateForCustomer(self.product_1)
        self.assertEqual(rate, 10.0)
                
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShopTaxManagement))
    suite.addTest(makeSuite(TestShopTaxes))    
    return suite
                                               