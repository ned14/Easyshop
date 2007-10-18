# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import IValidity

class TestValidityAdapters(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        self.folder.manage_addProduct["EasyShop"].addDirectDebit("cpm")
        self.folder.manage_addProduct["EasyShop"].addSimplePaymentMethod("spm")
        self.folder.manage_addProduct["EasyShop"].addPaymentValidator("pmv")
        self.folder.manage_addProduct["EasyShop"].addPaymentPrice("pp")
                        
        self.folder.manage_addProduct["EasyShop"].addCustomerTax("ct")
        self.folder.manage_addProduct["EasyShop"].addDefaultTax("dt")

        self.folder.manage_addProduct["EasyShop"].addShippingPrice("sp")
        # self.folder.manage_addProduct["EasyShop"].addShippingMethod("sm")
                                
    def testAdapters(self):
        """
        """
        adapter = IValidity(self.folder.cpm)
        self.assertEqual(str(adapter.__class__), "<class 'Products.EasyShop.adapters.generic.validity.CustomerPaymentValidityManagement'>")

        adapter = IValidity(self.folder.spm)
        self.assertEqual(str(adapter.__class__), "<class 'Products.EasyShop.adapters.generic.validity.ValidityManagement'>")

        adapter = IValidity(self.folder.pmv)
        self.assertEqual(str(adapter.__class__), "<class 'Products.EasyShop.adapters.generic.validity.ValidityManagement'>")

        adapter = IValidity(self.folder.pp)
        self.assertEqual(str(adapter.__class__), "<class 'Products.EasyShop.adapters.generic.validity.ValidityManagement'>")

        adapter = IValidity(self.folder.ct)
        self.assertEqual(str(adapter.__class__), "<class 'Products.EasyShop.adapters.generic.validity.ValidityManagement'>")

        adapter = IValidity(self.folder.dt)
        self.assertEqual(str(adapter.__class__), "<class 'Products.EasyShop.adapters.generic.validity.ValidityManagement'>")
        
        adapter = IValidity(self.folder.sp)
        self.assertEqual(str(adapter.__class__), "<class 'Products.EasyShop.adapters.generic.validity.ValidityManagement'>")
        
        # adapter = IValidity(self.folder.sm)
        # self.assertEqual(str(adapter.__class__), "<class 'Products.EasyShop.adapters.generic.validity.ValidityManagement'>")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestValidityAdapters))
    return suite
                                               