# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.interfaces import ICustomerManagement
from Products.EasyShop.interfaces import IPaymentManagement
from Products.EasyShop.interfaces import IAddressManagement
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import IItemManagement
from Products.EasyShop.interfaces import IPrices
from Products.EasyShop.interfaces import ITaxes

class TestInitialize(EasyShopTestCase):
    """
    """
    def testContainers(self):
        """
        """
        containers = [
            "carts",
            "categories",
            "products",
            "customers",
            "groups",
            "information",
            "orders",
            "paymentmethods",
            "paymentprices",
            "shippingmethods",
            "shippingprices",
            "taxes"
        ]
        
        object_ids = self.shop.objectIds()
        for container in containers:
            self.failUnless(container in objectIds)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInitialize))
    return suite
                                               