# -*- coding: utf-8 -*-

# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICurrencyManagement

class TestCurrencyManagementEUR(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestCurrencyManagementEUR, self).afterSetUp()
        self.cm = ICurrencyManagement(self.shop)
        
    def testGetLongName(self):
        """
        """
        self.assertEqual(self.cm.getLongName(), "Euro")
        
    def testGetShortName(self):
        """
        """
        self.assertEqual(self.cm.getShortName(), "EUR")
        
    def testGetSymbol(self):
        """
        """
        self.assertEqual(self.cm.getSymbol(), "€")
                
    def testPriceToString(self):
        """
        """
        price = 42.0
        
        string = self.cm.priceToString(price)
        self.assertEqual(string, "€ 42,00")
        
        string = self.cm.priceToString(price, "short")
        self.assertEqual(string, "EUR 42,00")
        
        string = self.cm.priceToString(price, "long")
        self.assertEqual(string, "Euro 42,00")

        string = self.cm.priceToString(price, "long", "after")
        self.assertEqual(string, "42,00 Euro")

class TestCurrencyManagementUSD(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestCurrencyManagementUSD, self).afterSetUp()
        self.shop.setCurrency("usd")
        
        self.cm = ICurrencyManagement(self.shop)
        
    def testGetLongName(self):
        """
        """
        self.assertEqual(self.cm.getLongName(), "US-Dollar")
        
    def testGetShortName(self):
        """
        """
        self.assertEqual(self.cm.getShortName(), "USD")
        
    def testGetSymbol(self):
        """
        """
        self.assertEqual(self.cm.getSymbol(), "$")
                
    def testPriceToString(self):
        """
        """
        price = 42.0
        
        string = self.cm.priceToString(price)
        self.assertEqual(string, "$ 42,00")
        
        string = self.cm.priceToString(price, "short")
        self.assertEqual(string, "USD 42,00")
        
        string = self.cm.priceToString(price, "long")
        self.assertEqual(string, "US-Dollar 42,00")

        string = self.cm.priceToString(price, "long", "after")
        self.assertEqual(string, "42,00 US-Dollar")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCurrencyManagementEUR))
    suite.addTest(makeSuite(TestCurrencyManagementUSD))    
    
    return suite
                                               