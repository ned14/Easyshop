# zope imports
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent

# easyshop imports
from easyshop.core.interfaces import IShop

@adapter(IShop, IObjectInitializedEvent)
def createContainers(shop, event):
    """
    """
    shop.manage_addProduct["easyshop.shop"].addPaymentMethodsContainer(
        id="paymentmethods", 
        title="Payment Methods")
        
    shop.manage_addProduct["easyshop.shop"].addPaymentPricesContainer(
        id="paymentprices", 
        title="Payment Prices")

    shop.paymentmethods.manage_addProduct["easyshop.shop"].addSimplePaymentMethod(
        id="cash-on-delivery",
        title="Cash on Delivery")
                
    shop.paymentmethods.manage_addProduct["easyshop.shop"].addPaymentValidator(
        id="credit-card", 
        title="Credit Card")
                
    shop.paymentmethods.manage_addProduct["easyshop.shop"].addPaymentValidator(
        id="direct-debit", 
        title="Direct Debit")

    shop.paymentmethods.manage_addProduct["easyshop.shop"].addPayPal(
        id="paypal", 
        title="PayPal")

    shop.paymentmethods.manage_addProduct["easyshop.shop"].addSimplePaymentMethod(
        id="prepayment", 
        title="Prepayment")   
        
    shop.paymentmethods.reindexObject()
    shop.paymentprices.reindexObject()
