# zope imports
from zope.component import getMultiAdapter

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.interfaces import IOrderManagement

class TestOrderManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestOrderManagement, self).afterSetUp()

    def testAddOrder(self):
        """
        """
        self.login("newmember")
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view.addToCart()

        view = getMultiAdapter((self.shop.products.product_2, self.shop.products.product_2.REQUEST), name="addToCart")
        view.addToCart()
        
        new_order = IOrderManagement(self.shop).addOrder()
        
        self.assertEqual(new_order.getShippingPriceGross(), 10.0)
        self.assertEqual("%.2f" % new_order.getShippingPriceNet(), "8.40")
        self.assertEqual("%.2f" % new_order.getShippingTax(), "1.60")
        self.assertEqual(new_order.getShippingTaxRate(), 19.0)

        self.assertEqual(new_order.getPaymentPriceGross(), 100.0)
        self.assertEqual("%.2f" % new_order.getPaymentPriceNet(), "84.03")
        self.assertEqual("%.2f" % new_order.getPaymentTax(), "15.97")
        self.assertEqual(new_order.getPaymentTaxRate(), 19.0)

        # items should be overtaken (more concise tests for item managment are
        # in a seperated file)
        self.failUnless(len(new_order.objectIds("OrderItem")) == 2)
        
        # customer should be copied
        self.assertEqual(new_order.getCustomer().getId(), "newmember")
        
        # The cart should still be there, because we need it until the payment 
        # has been successfully processed. See order_preview.py/handle_buy_action
        # for more.
        self.failUnless(self.shop.carts.get("newmember"))
                        
    def testGetOrders(self):
        """
        """
        om = IOrderManagement(self.shop)
                
        o = self.shop.orders
        o.invokeFactory("Order", "o1")
        
        o.invokeFactory("Order", "o5")        
        o.invokeFactory("Order", "o3")
        o.invokeFactory("Order", "o4")
        o.invokeFactory("Order", "o2")        
        o.reindexObject()
        
        ids = [o.getId() for o in om.getOrders(sorting="id", sort_order="descending")]
        self.assertEqual(ids, ["o5", "o4", "o3", "o2", "o1"])

        ids = [o.getId() for o in om.getOrders(sorting="id", sort_order="ascending")]
        self.assertEqual(ids, ["o1", "o2", "o3", "o4", "o5"])

        ids = [o.getId() for o in om.getOrders("created", sorting="getObjPositionInParent")]
        self.assertEqual(ids, ["o2", "o4", "o3", "o5", "o1"])
                        
    def testGetOrdersForAuthenticatedCustomer(self):
        """
        """
        self.login("newmember")
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view.addToCart()

        view = getMultiAdapter((self.shop.products.product_2, self.shop.products.product_2.REQUEST), name="addToCart")
        view.addToCart()
            
        om = IOrderManagement(self.shop)            
        new_order = om.addOrder()

        order = om.getOrdersForAuthenticatedCustomer()[0]
        self.assertEqual(order, new_order)
        
    def testGetOrderByUID(self):
        """
        """
        self.login("newmember")
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view.addToCart()

        view = getMultiAdapter((self.shop.products.product_2, self.shop.products.product_2.REQUEST), name="addToCart")
        view.addToCart()
            
        om = IOrderManagement(self.shop)            
        new_order = om.addOrder()
        
        order = om.getOrderByUID(new_order.UID())
        self.assertEqual(order, new_order)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestOrderManagement))
    return suite