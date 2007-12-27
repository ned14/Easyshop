# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.interfaces import IDiscountsManagement

class TestDiscountsManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestDiscountsManagement, self).afterSetUp()
                
    def testGetDiscounts1(self):
        """There are no discounts.
        """        
        dm = IDiscountsManagement(self.shop)
        self.assertEqual(dm.getDiscounts(), [])

    def testGetDiscounts2(self):
        """
        """
        self.shop.discounts.invokeFactory("Discount", id="d1", title="D1", value="1.0")
        self.shop.discounts.invokeFactory("Discount", id="d2", title="D2", value="2.0", base="cart_item", type="percentage")
        
        dm = IDiscountsManagement(self.shop)

        # Discount 1
        discount = dm.getDiscounts()[0]        
        self.assertEqual(discount.getId(), "d1")
        self.assertEqual(discount.Title(), "D1")
        self.assertEqual(discount.getValue(), 1.0)
        # defaults
        self.assertEqual(discount.getBase(), "product")
        self.assertEqual(discount.getType(), "absolute")

        # Discount 2
        discount = dm.getDiscounts()[1]
        self.assertEqual(discount.getId(), "d2")
        self.assertEqual(discount.Title(), "D2")
        self.assertEqual(discount.getValue(), 2.0)
        self.assertEqual(discount.getBase(), "cart_item")
        self.assertEqual(discount.getType(), "percentage")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestDiscountsManagement))
    return suite