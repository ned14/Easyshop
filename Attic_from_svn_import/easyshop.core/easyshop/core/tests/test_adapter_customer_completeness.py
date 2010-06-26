# zope imports
from zope.component import getMultiAdapter

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICompleteness

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
        id = am.addAddress({
            "firstname" : u"John",
            "lastname" : u"Doe",
            "address_1" : u"Doe Str. 1",            
            "zip_code" : u"4711",
            "city" : u"Doe City",
            "country" : u"Germany"
        })
        
        self.customer.selected_invoice_address= id        
        self.customer.selected_shipping_address = id
        self.assertEqual(c.isComplete(), False)
        
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view.addToCart()
        
        self.assertEqual(c.isComplete(), True)
                
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCustomerCompleteness))    

    return suite