# zope imports
from zope.component import getMultiAdapter
from zope import event

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.event import ObjectInitializedEvent

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IPrices

class TestSession:
    """
    """
    def __init__(self, sid):
        """
        """
        self.sid = sid
        
    def getId(self):
        """
        """
        return self.sid
        
class TestCart(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        self.setRoles(['Manager'])
        utils.createMember(self.portal, "newmember")
                
        self.folder.invokeFactory("EasyShop", 
                                  id="myshop", 
                                  title="MyShop", 
                                  description="My test shop")

        event.notify(ObjectInitializedEvent(self.folder.myshop))
        self.shop = self.folder.myshop
        self.shop.at_post_create_script()        
                        
        self.shop.products.invokeFactory("Product", id="product_1", price=22.0)
        self.product_1 = self.shop.products.product_1
        
        self.shop.products.invokeFactory("Product", id="product_2", price=19.0)
        self.product_2 = self.shop.products.product_2
        
        self.sid = self.portal.REQUEST.SESSION = TestSession("123")
                
    def testAddProductAsMember(self):
        """
        """
        self.login("newmember")

        view = getMultiAdapter((self.shop.products.product_2, self.shop.products.product_2.REQUEST), name="addToCart")
        view.addToCart()

        cart = ICartManagement(self.shop).getCart()        
        items = IItemManagement(cart).getItems()
        self.assertEqual(len(items), 1)
        
        view.addToCart()        

        items = IItemManagement(cart).getItems()
        self.assertEqual(len(items), 1)
        
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view.addToCart()

        items = IItemManagement(cart).getItems()
        self.assertEqual(len(items), 2)

    def testAddProductAsAnonymous(self):
        """
        """
        self.logout()

        view = getMultiAdapter((self.shop.products.product_2, self.shop.products.product_2.REQUEST), name="addToCart")
        view.addToCart()

        cart = ICartManagement(self.shop).getCart()

        items = IItemManagement(cart).getItems()
        self.assertEqual(len(items), 1)
        
        view.addToCart()        
    
        items = IItemManagement(cart).getItems()
        self.assertEqual(len(items), 1)
        
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view.addToCart()
        
        items = IItemManagement(cart).getItems()
        self.assertEqual(len(items), 2)
    
    def testAddProductAsAnonymousAndMember(self):
        """Proves that a member will overtake the cart items, which he has added,
        as anonymous user.
        """
        self.logout()
        
        view = getMultiAdapter((self.shop.products.product_2, self.shop.products.product_2.REQUEST), name="addToCart")
        view.addToCart()

        cart = ICartManagement(self.shop).getCart()        
        items = IItemManagement(cart).getItems()
        self.assertEqual(len(items), 1)
        
        view.addToCart()        
    
        items = IItemManagement(cart).getItems()
        self.assertEqual(len(items), 1)
        
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view.addToCart()
        
        items = IItemManagement(cart).getItems()
        self.assertEqual(len(items), 2)
        
        self.login("newmember")

        cart = ICartManagement(self.shop).getCart()
        items = IItemManagement(cart).getItems()
        self.assertEqual(len(items), 2)
        self.assertEqual(cart.getId(), "newmember")
        
    def testDeleteItem(self):
        """
        """
        self.login("newmember")
    
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view.addToCart()

        cart = ICartManagement(self.shop).getCart()
        im = IItemManagement(cart)            
        im.deleteItem("0")
    
        self.failIf(hasattr(cart, "0"))
        self.assertEqual(im.deleteItem("0"), False)
                
    def testDeleteItemByOrd(self):
        """
        """
        self.login("newmember")
    
        view = getMultiAdapter((self.shop.products.product_1, self.shop.products.product_1.REQUEST), name="addToCart")
        view.addToCart()

        cart = ICartManagement(self.shop).getCart()    
        im = IItemManagement(cart)            
        im.deleteItemByOrd(0)
    
        self.failIf(hasattr(cart, "0"))
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCart))
    
    return suite
                                               