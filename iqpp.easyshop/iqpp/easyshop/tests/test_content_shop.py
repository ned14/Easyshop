# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from iqpp.easyshop.interfaces import ICustomerManagement
from iqpp.easyshop.interfaces import IPaymentMethodManagement
from iqpp.easyshop.interfaces import IAddressManagement
from iqpp.easyshop.interfaces import ICartManagement
from iqpp.easyshop.interfaces import IItemManagement
from iqpp.easyshop.interfaces import IPrices
from iqpp.easyshop.interfaces import ITaxes

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
                                               