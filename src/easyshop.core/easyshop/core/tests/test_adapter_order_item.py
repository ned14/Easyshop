# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import ICartManagement

class TestOrderItemManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestOrderItemManagement, self).afterSetUp()                        
        self.login("newmember")
                
        self.shop.orders.invokeFactory("Order", "order")
        self.order = self.shop.orders.order

    def testAddItem(self):
        """
        """
        im = IItemManagement(self.order)
        self.assertRaises(Exception, im.addItem, "dummy_product")
        
    def testDeleteItemByOrd(self):
        """
        """
        im = IItemManagement(self.order)
        self.assertRaises(Exception, im.deleteItemByOrd, 0)
        
    def testDeleteItem(self):
        """
        """
        im = IItemManagement(self.order)
        self.assertRaises(Exception, im.deleteItem, "dummy_id")
        
    def testGetItems(self):
        """
        """
        self.order.invokeFactory("OrderItem", "item_1")
        self.order.invokeFactory("OrderItem", "item_2")        
                        
        im = IItemManagement(self.order)
        item_ids = [item.getId() for item in im.getItems()]

        self.assertEqual(item_ids, ["item_1", "item_2"])
    
    def testAddItemsFromCart(self):
        """
        """
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view.addToCart()

        view = getMultiAdapter((self.shop.products.product_2, self.shop.products.product_2.REQUEST), name="addToCart")
        view.addToCart()

        cm = ICartManagement(self.shop)
        cart = cm.getCart()
        
        im = IItemManagement(self.order)
        im.addItemsFromCart(cart)

        product_ids = [item.getProduct().getId() for item in im.getItems()]

        self.assertEqual(product_ids, ["product_1", "product_2"])
                
    def testAddItemFromCartItem(self):
        """
        """
        cm = ICartManagement(self.shop)
        cart = cm.createCart()

        properties = (
            {"id" : "color"   , "selected_option" : "Red" },    # -10.0
            {"id" : "material", "selected_option" : "Wood"},    # 0.0
            {"id" : "quality" , "selected_option" : "High"},    # 1500.0
        )

        cim = IItemManagement(cart)
        cim.addItem(self.product_1, properties=properties, quantity=3)
                
        cart_item = IItemManagement(cart).getItems()[0]
        
        oim = IItemManagement(self.order)        
        oim._addItemFromCartItem("0", cart_item)
        
        order_item = oim.getItems()[0]
        
        self.assertEqual(order_item.getProductQuantity(), 3)
        self.assertEqual("%.2f" % order_item.getProductPriceGross(), "22.00")
        self.assertEqual("%.2f" % order_item.getProductPriceNet(), "18.49")
        self.assertEqual("%.2f" % order_item.getProductTax(), "3.51")
        self.assertEqual("%.2f" % order_item.getPriceGross(), "4536.00")
        self.assertEqual("%.2f" % order_item.getPriceNet(), "3811.76")
        self.assertEqual(order_item.getTaxRate(), 19.0)
        self.assertEqual("%.2f" % order_item.getTax(), "724.24")
        self.assertEqual(order_item.getProduct(), self.product_1)
        
        properties = order_item.getProperties()
            
        self.assertEqual(properties[0]["title"], "Color")
        self.assertEqual(properties[0]["selected_option"], "Red")
        self.assertEqual(properties[0]["price"], "-10.0")

        self.assertEqual(properties[1]["title"], "Material")
        self.assertEqual(properties[1]["selected_option"], "Wood")
        self.assertEqual(properties[1]["price"], "0.0")

        self.assertEqual(properties[2]["title"], "Quality")
        self.assertEqual(properties[2]["selected_option"], "High")
        self.assertEqual(properties[2]["price"], "1500.0")
        
                
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestOrderItemManagement))
    return suite
                                               