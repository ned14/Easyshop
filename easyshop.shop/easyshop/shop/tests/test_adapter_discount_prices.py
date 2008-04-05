# zope imports
from zope.component import getMultiAdapter

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IPrices

class TestDiscountPrices(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestDiscountPrices, self).afterSetUp()
                
    def testPrices1(self):
        """
        """
        self.shop.discounts.invokeFactory("Discount", id="d1", title="D1", value="1.0", base="product", type="absolute")
        discount = self.shop.discounts.d1
        
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view()
        view()
        
        cart = ICartManagement(self.shop).getCart()
        item = IItemManagement(cart).getItems()[0]
        
        prices = getMultiAdapter((discount, item), IPrices)
        price_net = "%.2f" % prices.getPriceNet()
        
        self.assertEqual(prices.getPriceGross(), 2.0)
        self.assertEqual(prices.getPriceForCustomer(), 2.0)
        self.assertEqual(price_net, "1.68")

    def testPrices2(self):
        """
        """
        self.shop.discounts.invokeFactory("Discount", id="d1", title="D1", value="1.0", base="product", type="percentage")
        discount = self.shop.discounts.d1
        
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view()
        view()
        
        cart = ICartManagement(self.shop).getCart()
        item = IItemManagement(cart).getItems()[0]
        
        prices = getMultiAdapter((discount, item), IPrices)
        price_net = "%.2f" % prices.getPriceNet()
        price_gross = "%.2f" % prices.getPriceGross()
        price_for_customer = "%.2f" % prices.getPriceForCustomer()
        
        self.assertEqual(price_gross, "0.44")
        self.assertEqual(price_for_customer, "0.44")
        self.assertEqual(price_net, "0.37")

    def testPrices3(self):
        """
        """
        self.shop.discounts.invokeFactory("Discount", id="d1", title="D1", value="1.0", base="cart_item", type="percentage")
        discount = self.shop.discounts.d1
        
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view()
        view()
        
        cart = ICartManagement(self.shop).getCart()
        item = IItemManagement(cart).getItems()[0]
            
        prices = getMultiAdapter((discount, item), IPrices)
        price_net = "%.2f" % prices.getPriceNet()
        price_gross = "%.2f" % prices.getPriceGross()
        price_for_customer = "%.2f" % prices.getPriceForCustomer()
        
        self.assertEqual(price_gross, "0.44")
        self.assertEqual(price_for_customer, "0.44")
        self.assertEqual(price_net, "0.37")

    def testPrices4(self):
        """
        """
        self.shop.discounts.invokeFactory("Discount", id="d1", title="D1", value="1.0", base="cart_item", type="absolute")
        discount = self.shop.discounts.d1
        
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view()
        view()
        
        cart = ICartManagement(self.shop).getCart()
        item = IItemManagement(cart).getItems()[0]
        
        prices = getMultiAdapter((discount, item), IPrices)
        price_net = "%.2f" % prices.getPriceNet()
        
        self.assertEqual(prices.getPriceGross(), 1)
        self.assertEqual(prices.getPriceForCustomer(), 1)
        self.assertEqual(price_net, "0.84")
                        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestDiscountPrices))
    return suite