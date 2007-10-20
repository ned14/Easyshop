# zope imports
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent

# EasyShop imports
from Products.EasyShop.interfaces import IShop

@adapter(IShop, IObjectInitializedEvent)
def createContainers(shop, event):
    """
    """
    shop.manage_addProduct["EasyShop"].addPaymentMethodsContainer(
        id="paymentmethods", 
        title="Payment Methods")
        
    shop.manage_addProduct["EasyShop"].addPaymentPricesContainer(
        id="paymentprices", 
        title="Payment Prices")
        
    shop.paymentmethods.manage_addProduct["EasyShop"].addPayPal(
        id="paypal", 
        title="PayPal")
        
    shop.paymentmethods.manage_addProduct["EasyShop"].addPaymentValidator(
        id="direct-debit", 
        title="Direct Debit")
        
    shop.paymentmethods.manage_addProduct["EasyShop"].addSimplePaymentMethod(
        id="prepayment", 
        title="Prepayment")   
        
    shop.paymentmethods.manage_addProduct["EasyShop"].addSimplePaymentMethod(
        id="cash-on-delivery",
        title="Cash on Delivery")
        
    shop.paymentmethods.reindexObject()
    shop.paymentprices.reindexObject()
