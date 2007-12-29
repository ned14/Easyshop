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

class TestCartItemManagement(EasyShopTestCase):
    """
    """
    def testHasItemsAsAdmin(self):
        """
        """
        cm = ICartManagement(self.shop)
        cart = cm.createCart()
        
        # This caused an error as shasattr was not yet used within
        # CartManagement.getCart(). It returned an ATFolder.
        im = IItemManagement(cart)

    def testHasItems(self):
        """
        """
        self.logout()

        cm = ICartManagement(self.shop)
        cart = cm.createCart()
        
        im = IItemManagement(cart)

        self.assertEqual(im.hasItems(), False)
        im.addItem(self.product_1, properties=[])                
        self.assertEqual(im.hasItems(), True)

    def testAddItemsAndGetItems(self):
        """
        """
        self.logout()

        cm = ICartManagement(self.shop)
        cart = cm.createCart()
        
        im = IItemManagement(cart)
        
        im.addItem(self.product_1, properties=())
        self.assertEqual(len(im.getItems()), 1)

        im.addItem(self.product_1, properties=())
        self.assertEqual(len(im.getItems()), 1)

        im.addItem(self.product_1, properties=(), quantity=2)
        self.assertEqual(len(im.getItems()), 1)

        im.addItem(self.product_2, properties=(), quantity=3)
        self.assertEqual(len(im.getItems()), 2)

        i1, i2 = im.getItems()        

        i1.getId() == "0"
        i1.getProduct() == self.product_1
        i1.getAmount() == 4
        
        i1.getId() == "1"
        i1.getProduct() == self.product_2
        i1.getAmount() == 2

    def testDeleteItemByOrd(self):
        """
        """
        self.logout()

        cm = ICartManagement(self.shop)
        cart = cm.createCart()
        
        im = IItemManagement(cart)
        
        im.addItem(self.product_1, properties=())
        self.assertEqual(len(im.getItems()), 1)

        im.addItem(self.product_2, properties=(), quantity=3)
        self.assertEqual(len(im.getItems()), 2)

        # Try to delete non existing ord
        result = im.deleteItemByOrd(3)
        self.assertEqual(result, False)

        # Still 2 items in there
        self.assertEqual(len(im.getItems()), 2)
        
        # delete first item
        result = im.deleteItemByOrd(0)
        self.assertEqual(result, True)        
        self.assertEqual(len(im.getItems()), 1)

        # Once again, but now it should be another
        result = im.deleteItemByOrd(0)
        self.assertEqual(result, True)        
        self.assertEqual(len(im.getItems()), 0)

    def testDeleteItem(self):
        """
        """
        self.logout()

        cm = ICartManagement(self.shop)
        cart = cm.createCart()
        
        im = IItemManagement(cart)
        
        im.addItem(self.product_1, properties=())
        self.assertEqual(len(im.getItems()), 1)

        im.addItem(self.product_2, properties=(), quantity=3)
        self.assertEqual(len(im.getItems()), 2)
        
        # Try to delete non existing id
        result = im.deleteItem("3")
        self.assertEqual(result, False)

        # Still 2 items in there
        self.assertEqual(len(im.getItems()), 2)

        # delete first item
        result = im.deleteItem("0")
        self.assertEqual(result, True)        
        self.assertEqual(len(im.getItems()), 1)

        # delete second item
        result = im.deleteItem("1")
        self.assertEqual(result, True)        
        self.assertEqual(len(im.getItems()), 0)

    def testAddItemsFromCart(self):        
        """
        """
        cm = ICartManagement(self.shop)
        cart1 = cm.createCart()
        
        im1 = IItemManagement(cart1)
        
        im1.addItem(self.product_1, properties=())
        im1.addItem(self.product_2, properties=(), quantity=3)
        
        self.login("newmember")
        cart2 = cm.createCart()

        im2 = IItemManagement(cart2)
        im2.addItemsFromCart(cart1)
        
        self.assertEqual(len(im2.getItems()), 2)

class TestCartPrices(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestCartPrices, self).afterSetUp()
        cm = ICartManagement(self.shop)
        self.cart = cm.createCart()
        
        im = IItemManagement(self.cart)
        im.addItem(self.product_1, properties=(), quantity=2)
        im.addItem(self.product_2, properties=(), quantity=3)
        
    def testGetPriceForCustomer(self):
        """
        """
        p = IPrices(self.cart)
        self.assertEqual(p.getPriceForCustomer(), 211.00)
        
    def testGetPriceGross(self):
        """
        """
        p = IPrices(self.cart)
        self.assertEqual(p.getPriceGross(), 211.00)
    
    def testGetPriceNet(self):
        """
        """
        p = IPrices(self.cart)
        price_net = "%.2f" % p.getPriceNet()
        self.assertEqual(price_net, "177.31")

class TestCartTaxes(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestCartTaxes, self).afterSetUp()
        cm = ICartManagement(self.shop)
        self.cart = cm.createCart()
        
        im = IItemManagement(self.cart)
        im.addItem(self.product_1, properties=(), quantity=2)
        im.addItem(self.product_2, properties=(), quantity=3)

    def testGetTaxRate(self):
        """
        """
        t = ITaxes(self.cart)
        self.assertRaises(ValueError, t.getTaxRate)
        
    def testGetTaxRateForCustomer(self):
        """
        """
        t = ITaxes(self.cart)
        self.assertRaises(ValueError, t.getTaxRateForCustomer)

    def testGetTax(self):
        """
        """
        t = ITaxes(self.cart)
        tax = "%.2f" % t.getTax()
        self.assertEqual(tax, "33.69")

    def testGetTaxForCustomer(self):
        """
        """
        t = ITaxes(self.cart)
        tax = "%.2f" % t.getTaxForCustomer()
        self.assertEqual(tax, "33.69")
    
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCartItemManagement))
    suite.addTest(makeSuite(TestCartPrices))
    suite.addTest(makeSuite(TestCartTaxes))            
    return suite
                                               