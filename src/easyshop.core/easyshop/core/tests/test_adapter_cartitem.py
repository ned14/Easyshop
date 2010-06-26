# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import ITaxes

class TestCartItems(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestCartItems, self).afterSetUp()
        
        self.login("newmember")
        cm = ICartManagement(self.shop)
        cart = cm.createCart()
        
        im = IItemManagement(cart)
        im.addItem(self.product_1, properties=(), quantity=2)
        im.addItem(self.product_2, properties=(), quantity=3)
        
        self.item1, self.item2 = im.getItems()
            
    def testGetPriceForCustomer(self):
        """
        """
        p = IPrices(self.item1)
        self.assertEqual("%.2f" % p.getPriceForCustomer(), "44.00")

        p = IPrices(self.item2)
        self.assertEqual(p.getPriceForCustomer(), 57.0)
                
    def testGetPriceGross(self):
        """
        """
        p = IPrices(self.item1)
        self.assertEqual(p.getPriceGross(), 44.0)

        p = IPrices(self.item2)
        self.assertEqual(p.getPriceGross(), 57.0)

    def testGetPriceNet(self):
        """
        """
        p = IPrices(self.item1)
        price_net = "%.2f" % p.getPriceNet()
        self.assertEqual(price_net, "36.97")

        p = IPrices(self.item2)
        price_net = "%.2f" % p.getPriceNet()
        self.assertEqual(price_net, "47.90")

    def testGetTax(self):
        """
        """
        t = ITaxes(self.item1)
        tax = "%.2f" % t.getTax()
        self.assertEqual(tax, "7.03")

        t = ITaxes(self.item2)
        tax = "%.2f" % t.getTax()
        self.assertEqual(tax, "9.10")
        
    def testGetTaxForCustomer(self):
        """
        """
        t = ITaxes(self.item1)
        tax = "%.2f" % t.getTaxForCustomer()
        self.assertEqual(tax, "7.03")

        t = ITaxes(self.item2)
        tax = "%.2f" % t.getTaxForCustomer()
        self.assertEqual(tax, "9.10")
        
    def testGetTaxRate(self):
        """
        """
        t = ITaxes(self.item1)
        self.assertEqual(t.getTaxRate(), 19.00)

        t = ITaxes(self.item2)
        self.assertEqual(t.getTaxRate(), 19.00)
        
    def testGetTaxRateForCustomer(self):
        """
        """
        t = ITaxes(self.item1)
        self.assertEqual(t.getTaxRate(), 19.00)

        t = ITaxes(self.item2)
        self.assertEqual(t.getTaxRate(), 19.00)

class TestCartItemProperties(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestCartItemProperties, self).afterSetUp()
        self.login("newmember")
        cm = ICartManagement(self.shop)
        cart = cm.createCart()
        
        im = IItemManagement(cart)

        properties = (
            {"id" : "color"   , "selected_option" : "Red" },    # -10.0
            {"id" : "material", "selected_option" : "Wood"},    # 0.0
            {"id" : "quality" , "selected_option" : "High"},    # 1500.0
        )

        im.addItem(self.product_1, properties=properties, quantity=3)
        self.item1 = im.getItems()[0]
            
    def testGetPriceForCustomer(self):
        """
        """
        pp = IPrices(self.item1)
        self.assertEqual(pp.getPriceForCustomer(), 4536.0)
        
    def testGetPriceGross(self):
        """
        """
        pp = IPrices(self.item1)
        self.assertEqual(pp.getPriceGross(), 4536.0)
        
    def testGetPriceNet(self):
        """
        """
        pp = IPrices(self.item1)
        price_net = "%.2f" % pp.getPriceNet()
        self.assertEqual(price_net, "3811.76")

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCartItems))
    suite.addTest(makeSuite(TestCartItemProperties))
    
    return suite
                                               