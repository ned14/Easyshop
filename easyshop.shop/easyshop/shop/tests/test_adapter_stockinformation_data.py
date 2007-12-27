# easyshop imports 
from base import EasyShopTestCase
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IStockManagement

class TestStockInformationData(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestStockInformationData, self).afterSetUp()
        container = self.shop["stock-information"]
        container.invokeFactory("StockInformation", id="s1")

        sm = IStockManagement(self.shop)
        self.si = sm.getStockInformationFor(self.shop.products.product_1)
    
    def testAsDict1(self):
        """
        """
        self.si.setDeliveryTimeMin("1")
        self.si.setDeliveryTimeMax("2")
        self.si.setDeliveryTimeUnit("Days")
        
        data = IData(self.si).asDict()        
        self.assertEqual(data["time_period"], "1-2")
        self.assertEqual(data["time_unit"], "Days")
        
    def testAsDict2(self):
        """
        """        
        self.si.setDeliveryTimeMin("2")
        self.si.setDeliveryTimeMax("2")
        self.si.setDeliveryTimeUnit("Days")
        
        data = IData(self.si).asDict()        
        self.assertEqual(data["time_period"], "2")
        self.assertEqual(data["time_unit"], "Days")
        
    def testAsDict3(self):
        """
        """        
        self.si.setDeliveryTimeMin("1")
        self.si.setDeliveryTimeMax("1")
        self.si.setDeliveryTimeUnit("Days")
        
        data = IData(self.si).asDict()
        self.assertEqual(data["time_period"], "1")
        self.assertEqual(data["time_unit"], "Day")
        
    def testAsDict4(self):
        """
        """        
        self.si.setDeliveryTimeMin("1")
        self.si.setDeliveryTimeMax("1")
        self.si.setDeliveryTimeUnit("Weeks")
        
        data = IData(self.si).asDict()
        self.assertEqual(data["time_period"], "1")
        self.assertEqual(data["time_unit"], "Week")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestStockInformationData))
    return suite