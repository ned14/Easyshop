# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.interfaces import IValidity

from easyshop.payment.content import BankAccount
from easyshop.taxes.content import CustomerTax
from easyshop.taxes.content import DefaultTax
from easyshop.payment.content import PaymentPrice
from easyshop.payment.content import GenericPaymentMethod
from easyshop.shipping.content import ShippingPrice

class TestValidityAdapters(EasyShopTestCase):
    """
    """
    def testAdapters(self):
        """
        """
        adapter = IValidity(BankAccount("dummy"))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.validity.Validity'>")

        adapter = IValidity(GenericPaymentMethod("dummy"))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.validity.Validity'>")

        adapter = IValidity(PaymentPrice("dummy"))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.validity.Validity'>")

        adapter = IValidity(CustomerTax("dummy"))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.validity.Validity'>")

        adapter = IValidity(DefaultTax("dummy"))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.validity.Validity'>")
        
        adapter = IValidity(ShippingPrice("dummy"))
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.validity.Validity'>")
        
        # adapter = IValidity(ShippingMethod("dummy"))
        # self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.validity.Validity'>")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestValidityAdapters))
    return suite