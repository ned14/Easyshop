# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IPropertyManagement

class TestProductPropertyManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestProductPropertyManagement, self).afterSetUp()
        self.shop.taxes.invokeFactory("CustomerTax", id="customer", rate=10.0)
                
    def testGetPriceForCustomer_1(self):
        """Test a property which is in group and product.
        """
        pm = IPropertyManagement(self.shop.products.product_1)

        price = pm.getPriceForCustomer("color", "Red")
        self.assertEqual("%.2f" % price, "-9.24")

        price = pm.getPriceForCustomer("color", "Blue")
        self.assertEqual(price, 0.0) 

        price = pm.getPriceForCustomer("color", "Green")
        self.assertEqual("%.2f" % price, "13.87") 
                
    def testGetPriceForCustomer_2(self):
        """Test a property which is just in group.
        """
        pm = IPropertyManagement(self.shop.products.product_1)

        price = pm.getPriceForCustomer("size", "Small")
        self.assertEqual("%.2f" % price, "-10.17")

        price = pm.getPriceForCustomer("size", "Medium")
        self.assertEqual("%.2f" % price, "0.92") 

        price = pm.getPriceForCustomer("size", "Large")
        self.assertEqual("%.2f" % price, "20.34") 
                
    def testGetPriceGross_1(self):
        """Test a property which is in group and product.
        """
        pm = IPropertyManagement(self.shop.products.product_1)

        price = pm.getPriceGross("color", "Red")
        self.assertEqual(price, -10.0) 

        price = pm.getPriceGross("color", "Blue")
        self.assertEqual(price, 0.0) 

        price = pm.getPriceGross("color", "Green")
        self.assertEqual(price, 15.0) 

    def testGetPriceGross_2(self):
        """Test a properties which is just in groups
        """
        pm = IPropertyManagement(self.shop.products.product_1)

        price = pm.getPriceGross("size", "Small")
        self.assertEqual(price, -11.0) 

        price = pm.getPriceGross("size", "Medium")
        self.assertEqual(price, 1.0) 

        price = pm.getPriceGross("size", "Large")
        self.assertEqual(price, 22.0) 
                
    def testGetPriceNet_1(self):
        """Test a property which is in group and product
        """
        pm = IPropertyManagement(self.shop.products.product_1)

        # Note that color prices are taken from product not from group
        price = pm.getPriceNet("color", "Red")
        self.assertEqual("%.2f" % price, "-8.40")

        price = pm.getPriceNet("color", "Blue")
        self.assertEqual(price, 0.0) 

        price = pm.getPriceNet("color", "Green")
        self.assertEqual("%.2f" % price, "12.61") 

    def testGetPriceNet_2(self):
        """Test a properties which is just in groups
        """
        pm = IPropertyManagement(self.shop.products.product_1)

        price = pm.getPriceNet("size", "Small")
        self.assertEqual("%.2f" % price, "-9.24")

        price = pm.getPriceNet("size", "Medium")
        self.assertEqual("%.2f" % price, "0.84") 

        price = pm.getPriceNet("size", "Large")
        self.assertEqual("%.2f" % price, "18.49") 
                
    def testGetProperties(self):
        """Get properties from product.
        
        Note:
            product 1 is in group 1
            group 1 has color property too
            but products properties are choosen

        Note that properties are taken from group and product
        """
        
        pm = IPropertyManagement(self.shop.products.product_1)
        ids = [p.getId() for p in pm.getProperties()]
        
        self.assertEqual(ids, ["color", "material", "quality", "size"])

    def testGetProperty(self):
        """
        """
        pm = IPropertyManagement(self.shop.products.product_1)

        p = pm.getProperty("color")        
        self.assertEqual(p.aq_inner.aq_parent.portal_type, "Product")

        p = pm.getProperty("size")        
        self.assertEqual(p.aq_inner.aq_parent.portal_type, "ProductGroup")
                
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductPropertyManagement))
    return suite
                                               