# zope imports
from zope.component import getMultiAdapter

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import IAddressManagement
from Products.EasyShop.interfaces import ICompleteness

class TestCustomerCompleteness(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestCustomerCompleteness, self).afterSetUp()

        self.shop.customers.invokeFactory("Customer", "customer")
        self.customer = self.shop.customers.customer
        self.customer.at_post_create_script()
        
    def testIsComplete(self):
        """
        """        
        c = ICompleteness(self.shop.customers.customer)
        self.assertEqual(c.isComplete(), False)
        
        am = IAddressManagement(self.customer)
        id = am.addAddress(
            "Doe Str. 1",
            "App. 1",
            "4711",
            "Doe City",
            "Germany"
        )
        
        self.customer.setInvoiceAddressAsString(id)        
        self.customer.setShippingAddressAsString(id)
        self.assertEqual(c.isComplete(), False)
        
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view.addToCart()
        
        self.assertEqual(c.isComplete(), True)
                
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCustomerCompleteness))    

    return suite