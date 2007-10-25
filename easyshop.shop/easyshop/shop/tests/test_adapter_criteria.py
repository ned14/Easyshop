# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.shop.tests import utils
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IValidity

class TestValidity(EasyShopTestCase):
    """
    """
    def testCategory(self):
        """
        """
        # Criteria has one catogory, products have this too
        self.folder.manage_addProduct["easyshop.shop"].addCategoryCriteria("c")
        self.folder.c.setCategories(("category_11",))
        v = IValidity(self.folder.c)
        
        self.assertEqual(v.isValid(self.product_1), True)
        self.assertEqual(v.isValid(self.product_2), True)

        # Criteria has one catogory, products haven't this         
        self.folder.c.setCategories(("category_2",))
        v = IValidity(self.folder.c)
        self.assertEqual(v.isValid(self.product_1), False)
        self.assertEqual(v.isValid(self.product_2), False)

        # Criteria has two catogories; products have just one of these
        self.folder.c.setCategories(("category_11", "category_1"))
        v = IValidity(self.folder.c)
        self.assertEqual(v.isValid(self.product_1), True)
        self.assertEqual(v.isValid(self.product_2), True)

    def testCountry(self):
        """
        """
        self.shop.manage_addProduct["easyshop.shop"].addCountryCriteria("c")
        self.shop.c.setCountries(("USA",))
        v = IValidity(self.shop.c)
        
        self.login("newmember")

        cm = ICustomerManagement(self.shop)
        customer = cm.getAuthenticatedCustomer()        
        customer.invokeFactory("Address", "address_1")

        customer.address_1.setCountry("USA")
        self.assertEqual(v.isValid(), True)

        customer.address_1.setCountry("Germany")
        self.assertEqual(v.isValid(), False)
        
    def testCustomer(self):
        """
        """
        # customer criteria needs context
        self.folder.manage_addProduct["easyshop.shop"].addCustomerCriteria("c")
        v = IValidity(self.folder.c)        

        self.assertEqual(v.isValid(), False)

        self.folder.c.setCustomers(("newmember",))
        self.assertEqual(v.isValid(), False)            
        
        self.login("newmember")
        self.assertEqual(v.isValid(), True)        
                
        self.folder.c.setCustomers(("newmember", "anothermember"))        
        self.assertEqual(v.isValid(), True)    
        
    def testDate(self):
        """
        """
        self.folder.manage_addProduct["easyshop.shop"].addDateCriteria("c")
        v = IValidity(self.folder.c)
        
        self.folder.c.setStart(DateTime()-2)
        self.folder.c.setEnd(DateTime()-1)            
        self.assertEqual(v.isValid(), False)

        self.folder.c.setStart(DateTime()-2)
        self.folder.c.setEnd(DateTime()+1)            
        self.assertEqual(v.isValid(), True)

        self.folder.c.setStart(DateTime()+1)
        self.folder.c.setEnd(DateTime()+2)            
        self.assertEqual(v.isValid(), False)
        
    def testGroup(self):
        """
        """
        self.folder.manage_addProduct["easyshop.shop"].addGroupCriteria("c")
        v = IValidity(self.folder.c)

        self.assertEqual(v.isValid(self.product_1), False)
        self.assertEqual(v.isValid(self.product_2), False)
                
        self.folder.c.setGroups(("group_1"),)
        self.assertEqual(v.isValid(self.product_1), True)
        self.assertEqual(v.isValid(self.product_2), True)
        
        self.folder.c.setGroups(("group_2"),)        
        self.assertEqual(v.isValid(self.product_1), True)
        self.assertEqual(v.isValid(self.product_2), False)
        
        self.folder.c.setGroups(("group_1", "group_2"),)        
        self.assertEqual(v.isValid(self.product_1), True)
        self.assertEqual(v.isValid(self.product_2), True)

    def testPaymentMethod(self):
        """
        """
        self.shop.manage_addProduct["easyshop.shop"].addPaymentMethodCriteria("c")
        v = IValidity(self.shop.c)
        
        self.login("newmember")

        cm = ICustomerManagement(self.shop)
        customer = cm.getAuthenticatedCustomer()

        customer.setSelectedPaymentMethod("cash-on-delivery")
        self.assertEqual(v.isValid(), False)

        customer.setSelectedPaymentMethod("prepayment")
        self.assertEqual(v.isValid(), False)

        self.shop.c.setPaymentMethods(["directdebit"])
        self.assertEqual(v.isValid(), False)        

        self.shop.c.setPaymentMethods(["prepayment"])
        self.assertEqual(v.isValid(), True)

        self.shop.c.setPaymentMethods(["prepayment", "directdebit"])
        self.assertEqual(v.isValid(), True)
                
    def testPrice(self):
        """
        """
        self.shop.manage_addProduct["easyshop.shop"].addPriceCriteria("c")
        v = IValidity(self.shop.c)
        
        self.login("newmember")        

        self.assertEqual(v.isValid(), False)
        
        view = getMultiAdapter((
            self.shop.products.product_1, 
            self.shop.products.product_1.REQUEST), name="addToCart")
            
        view.addToCart()
        self.assertEqual(v.isValid(), True)

        self.shop.c.setPrice(21.00)
        self.assertEqual(v.isValid(), True)
        
        self.shop.c.setPrice(22.00)
        self.assertEqual(v.isValid(), False)

        view = getMultiAdapter((
            self.shop.products.product_2, 
            self.shop.products.product_2.REQUEST), name="addToCart")
            
        view.addToCart()

        self.shop.c.setPrice(40.00)
        self.assertEqual(v.isValid(), True)

        self.shop.c.setPrice(41.00)
        self.assertEqual(v.isValid(), False)

    def testProduct(self):
        """
        """
        self.shop.manage_addProduct["easyshop.shop"].addProductCriteria("c")
        v = IValidity(self.shop.c)

        self.assertEqual(v.isValid(self.product_1), False)
        
        self.shop.c.setProducts(("product_1",))
        self.assertEqual(v.isValid(self.product_1), True)
        self.assertEqual(v.isValid(self.product_2), False)

        self.shop.c.setProducts(("product_1", "product_2"))
        self.assertEqual(v.isValid(self.product_1), True)
        self.assertEqual(v.isValid(self.product_2), True)

    def testWeight(self):
        """
        """
        self.shop.manage_addProduct["easyshop.shop"].addWeightCriteria("c")
        v = IValidity(self.shop.c)

        self.assertEqual(v.isValid(), False)
        
        view = getMultiAdapter((
            self.shop.products.product_1, 
            self.shop.products.product_1.REQUEST), name="addToCart")

        view.addToCart()

        view = getMultiAdapter((
            self.shop.products.product_2, 
            self.shop.products.product_2.REQUEST), name="addToCart")

        view.addToCart()
        
        self.assertEqual(v.isValid(), True)

        self.shop.c.setWeight(29.0)
        self.assertEqual(v.isValid(), True)

        self.shop.c.setWeight(30.0)
        self.assertEqual(v.isValid(), False)
        
                
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestValidity))    
    
    return suite
                                               