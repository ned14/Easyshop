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

class TestValidityAdapters(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        self.folder.manage_addProduct["easyshop.shop"].addDirectDebit("cpm")
        self.folder.manage_addProduct["easyshop.shop"].addSimplePaymentMethod("spm")
        self.folder.manage_addProduct["easyshop.shop"].addPaymentValidator("pmv")
        self.folder.manage_addProduct["easyshop.shop"].addPaymentPrice("pp")
                        
        self.folder.manage_addProduct["easyshop.shop"].addCustomerTax("ct")
        self.folder.manage_addProduct["easyshop.shop"].addDefaultTax("dt")

        self.folder.manage_addProduct["easyshop.shop"].addShippingPrice("sp")
        # self.folder.manage_addProduct["easyshop.shop"].addShippingMethod("sm")
                                
    def testAdapters(self):
        """
        """
        adapter = IValidity(self.folder.cpm)
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.CustomerPaymentValidityManagement'>")

        adapter = IValidity(self.folder.spm)
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.ValidityManagement'>")

        adapter = IValidity(self.folder.pmv)
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.ValidityManagement'>")

        adapter = IValidity(self.folder.pp)
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.ValidityManagement'>")

        adapter = IValidity(self.folder.ct)
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.ValidityManagement'>")

        adapter = IValidity(self.folder.dt)
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.ValidityManagement'>")
        
        adapter = IValidity(self.folder.sp)
        self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.ValidityManagement'>")
        
        # adapter = IValidity(self.folder.sm)
        # self.assertEqual(str(adapter.__class__), "<class 'easyshop.shop.adapters.generic.validity.ValidityManagement'>")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestValidityAdapters))
    return suite
                                               