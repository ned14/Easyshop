# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.interfaces import IPaymentInformationManagement

class TestPaymentInformationManagement(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestPaymentInformationManagement, self).afterSetUp()

        self.shop.customers.invokeFactory("Customer", "customer")
        self.customer = self.shop.customers.customer
        self.customer.at_post_create_script()
        
        self.customer.invokeFactory("BankAccount", id="bank-account")
        
    def testDeletePaymentInformations(self):
        """
        """            
        pm = IPaymentInformationManagement(self.customer)
        
        ids = [p.getId() for p in pm.getPaymentInformations()]
        self.assertEqual(["bank-account"], ids)

        # Shop level payment methods shouldn't be deletable here.
        result = pm.deletePaymentInformation("paypal")
        self.assertEqual(result, False)

        result = pm.deletePaymentInformation("prepayment")
        self.assertEqual(result, False)
        
        # still all there?
        ids = [p.getId() for p in pm.getPaymentInformations()]
        self.assertEqual(["bank-account"], ids)

        result = pm.deletePaymentInformation("bank-account")        
        self.assertEqual(result, True)
                
        ids = [p.getId() for p in pm.getPaymentInformations()]
        self.assertEqual([], ids)

    def testGetPaymentInformations(self):
        """Get all payment methods (without parameter)
        """
        pm = IPaymentInformationManagement(self.customer)

        ids = [p.getId() for p in pm.getPaymentInformations()]
        self.assertEqual(["bank-account"], ids)
                        
    def testGetSelectedPaymentMethod(self):
        """
        """
        pm = IPaymentInformationManagement(self.customer)
        result = pm.getSelectedPaymentMethod().getId()
        self.assertEqual(result, "prepayment")

    def testGetSelectedPaymentInformation(self):
        """
        """
        pm = IPaymentInformationManagement(self.customer)
        result = pm.getSelectedPaymentInformation()
        self.failUnless(result is None)
                

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPaymentInformationManagement))

    return suite