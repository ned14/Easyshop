# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import ITaxes

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
            "discounts",
            "groups",
            "information",
            "orders",
            "paymentmethods",
            "paymentprices",
            "shippingmethods",
            "shippingprices",
            "stock-information",
            "taxes"
        ]

        object_ids = self.shop.objectIds()
        for container in containers:
            self.failUnless(container in object_ids)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInitialize))
    return suite
                                               