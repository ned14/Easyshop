# easyshop imports 
from base import EasyShopTestCase
from easyshop.shop.tests import utils
from easyshop.core.interfaces import IPaymentManagement

class TestPaymentManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestPaymentManagement, self).afterSetUp()

        self.shop.customers.invokeFactory("Customer", "customer")
        self.customer = self.shop.customers.customer
        self.customer.at_post_create_script()
        
        self.customer.invokeFactory("DirectDebit", id="directdebit")
        
    def testDeletePaymentMethod(self):
        """
        """            
        pm = IPaymentManagement(self.customer)

        ids = [p.getId() for p in pm.getPaymentMethods()]
        self.assertEqual(["directdebit"], ids)

        # Shop level payment methods shouldn't be deletable here.
        result = pm.deletePaymentMethod("paypal")
        self.assertEqual(result, False)

        result = pm.deletePaymentMethod("prepayment")
        self.assertEqual(result, False)
        
        # still all there?
        ids = [p.getId() for p in pm.getPaymentMethods()]
        self.assertEqual(["directdebit"], ids)

        result = pm.deletePaymentMethod("directdebit")        
        self.assertEqual(result, True)
                
        ids = [p.getId() for p in pm.getPaymentMethods()]
        self.assertEqual([], ids)

    def testGetPaymentMethods_1(self):
        """Get all payment methods (without parameter)
        """
        pm = IPaymentManagement(self.customer)

        ids = [p.getId() for p in pm.getPaymentMethods()]
        self.assertEqual(["directdebit"], ids)
                        
    def testGetSelectedPaymentMethod(self):
        """
        """
        pm = IPaymentManagement(self.customer)
        result = pm.getSelectedPaymentMethod().getId()
        self.assertEqual(result, "prepayment")
                

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPaymentManagement))

    return suite