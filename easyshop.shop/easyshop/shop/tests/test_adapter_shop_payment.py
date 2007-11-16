# easyshop imports 
from base import EasyShopTestCase
from easyshop.shop.tests import utils
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IPaymentManagement
from easyshop.core.interfaces import IPaymentPrices
from easyshop.core.interfaces import IPayPal

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
                
    def testDeletePaymentMethod(self):
        """
        """            
        pm = IPaymentManagement(self.shop)

        ids = [p.getId() for p in pm.getPaymentMethods()]
        self.assertEqual(["paypal", "direct-debit", "prepayment", "cash-on-delivery"], ids)

        result = pm.deletePaymentMethod("paypal")
        self.assertEqual(result, True)

        ids = [p.getId() for p in pm.getPaymentMethods()]
        self.assertEqual(["direct-debit", "prepayment", "cash-on-delivery"], ids)

        result = pm.deletePaymentMethod("prepayment")
        self.assertEqual(result, True)
        
        ids = [p.getId() for p in pm.getPaymentMethods()]
        self.assertEqual(["direct-debit", "cash-on-delivery"], ids)

        # delete payment validor
        result = pm.deletePaymentMethod("direct-debit")
        self.assertEqual(result, True)
        
        ids = [p.getId() for p in pm.getPaymentMethods()]
        self.assertEqual(["cash-on-delivery"], ids)

        result = pm.deletePaymentMethod("paypal")
        self.assertEqual(result, False)

        result = pm.deletePaymentMethod("prepayment")
        self.assertEqual(result, False)

    def testGetPaymentMethods_1(self):
        """Get all payment methods (without parameter)
        """
        pm = IPaymentManagement(self.shop)

        ids = [p.getId() for p in pm.getPaymentMethods()]
        self.assertEqual(["paypal", "direct-debit", "prepayment", "cash-on-delivery"], ids)

    def testGetPaymentMethods_2(self):
        """Get paypal (with parameter=paypal)
        """
        pm = IPaymentManagement(self.shop)

        ids = [p.getId() for p in pm.getPaymentMethods(interface=IPayPal)]
        self.assertEqual(["paypal"], ids)

    def testGetSelectedPaymentMethod_1(self):
        """Customer has selected prepayment
        """
        pm = IPaymentManagement(self.shop)
        result = pm.getSelectedPaymentMethod().getId()
        self.assertEqual(result, "prepayment")

    def testGetSelectedPaymentMethod_2(self):
        """Customer has selected paypal
        """
        cm = ICustomerManagement(self.shop)
        customer = cm.getAuthenticatedCustomer()        
        customer.selected_payment_method = "paypal"
        
        pm = IPaymentManagement(self.shop)
        result = pm.getSelectedPaymentMethod().getId()
        self.assertEqual(result, "paypal")

    def testGetSelectedPaymentMethod_3(self):
        """Customer has selected a non existing. Returns default, which is 
        prepayment atm.
        """
        self.customer.selected_payment_method = "dummy"
        pm = IPaymentManagement(self.shop)
        result = pm.getSelectedPaymentMethod().getId()
        self.assertEqual(result, "prepayment")

class TestPaymentPrices(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestPaymentPrices, self).afterSetUp()

        self.shop.customers.invokeFactory("Customer", "customer")
        self.customer = self.shop.customers.customer
        self.customer.at_post_create_script()
        
    def testGetPaymentPrices(self):
        """
        """            
        pp = IPaymentPrices(self.shop)
        ids = [pp.getId() for pp in pp.getPaymentPrices()]
        self.assertEqual(ids, ["default"])

    def testGetPriceGross(self):
        """
        """
        pp = IPaymentPrices(self.shop)
        price_gross = pp.getPriceGross()
        
        self.assertEqual(price_gross, 100.0)

    def testGetPriceForCustomer(self):
        """
        """
        pp = IPaymentPrices(self.shop)
        price_gross = pp.getPriceGross()
        
        self.assertEqual(price_gross, 100.0)

    def testGetPriceNet(self):
        """
        """
        pp = IPaymentPrices(self.shop)
        price_net = pp.getPriceNet()
        
        self.assertEqual("%.2f" % price_net, "84.03")

    def testGetTax(self):
        """
        """
        pp = IPaymentPrices(self.shop)
        tax = pp.getTax()

        self.assertEqual("%.2f" % tax, "15.97")
                
    def testGetTaxForCustomer(self):
        """
        """
        pp = IPaymentPrices(self.shop)
        tax = pp.getTaxForCustomer()

        self.assertEqual("%.2f" % tax, "15.97")

    def testGetTaxRate(self):
        """
        """
        pp = IPaymentPrices(self.shop)
        tax = pp.getTaxRate()

        self.assertEqual(tax, 19.0)
        
    def testGetTaxRateForCustomer(self):
        """
        """
        pp = IPaymentPrices(self.shop)
        tax = pp.getTaxRateForCustomer()

        self.assertEqual(tax, 19.0)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPaymentManagement))
    suite.addTest(makeSuite(TestPaymentPrices))
    return suite
