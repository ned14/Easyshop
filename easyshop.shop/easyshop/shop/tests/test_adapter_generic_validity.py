# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.shop.tests import utils
from easyshop.core.interfaces import IValidity

from easyshop.payment.content import DirectDebit
from easyshop.taxes.content import CustomerTax
from easyshop.taxes.content import DefaultTax
from easyshop.payment.content import PaymentPrice
from easyshop.payment.content import GenericPaymentMethod
from easyshop.shipping.content import ShippingPrice
from easyshop.shipping.content import ShippingMethod

class TestValidityAdapters(EasyShopTestCase):
    """
    """
    def testAdapters(self):
        """
        """
        adapter = IValidity(DirectDebit("dummy"))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.CustomerPaymentValidityManagement'>")

        adapter = IValidity(GenericPaymentMethod("dummy"))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.ValidityManagement'>")

        adapter = IValidity(PaymentPrice("dummy"))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.ValidityManagement'>")

        adapter = IValidity(CustomerTax("dummy"))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.ValidityManagement'>")

        adapter = IValidity(DefaultTax("dummy"))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.ValidityManagement'>")
        
        adapter = IValidity(ShippingPrice("dummy"))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.ValidityManagement'>")
        
        # adapter = IValidity(ShippingMethod("dummy"))
        # self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.ValidityManagement'>")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestValidityAdapters))
    return suite
                                               