# zope imports
from zope.component import adapter
from easyshop.shop.events import IShopCreatedEvent

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IShop

@adapter(IShop, IShopCreatedEvent)
def createContainers(shop, event):
    """
    """
    shop.manage_addProduct["easyshop.shop"].addPaymentMethodsContainer(
        id="paymentmethods", 
        title="Payment Methods")
        
    shop.manage_addProduct["easyshop.shop"].addPaymentPricesContainer(
        id="paymentprices", 
        title="Payment Prices")

    shop.paymentmethods.manage_addProduct["easyshop.shop"].addGenericPaymentMethod(
        id="cash-on-delivery",
        title="Cash on Delivery")
                
    shop.paymentmethods.manage_addProduct["easyshop.shop"].addCreditCardPaymentMethod(
        id="credit-card", 
        title="Credit Card")
                
    shop.paymentmethods.manage_addProduct["easyshop.shop"].addDirectDebitPaymentMethod(
        id="direct-debit", 
        title="Direct Debit")

    shop.paymentmethods.manage_addProduct["easyshop.shop"].addPayPalPaymentMethod(
        id="paypal", 
        title="PayPal")

    shop.paymentmethods.manage_addProduct["easyshop.shop"].addGenericPaymentMethod(
        id="prepayment", 
        title="Prepayment")   

    # Publish all payment methods by default
    wftool = getToolByName(shop, "portal_workflow")
    for payment_method in shop.paymentmethods.objectValues():
        wftool.doActionFor(payment_method, "publish")
        
    shop.paymentmethods.reindexObject()
    shop.paymentprices.reindexObject()
