# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import IAddress
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import IPaymentManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import ICustomer
from easyshop.core.interfaces import IShopManagement

class CustomerCompleteness:
    """
    """
    implements(ICompleteness)
    adapts(ICustomer)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def isComplete(self):
        """Checks weather the customer is complete to checkout.
        
           Customer completeness means the customer is ready to check out:
             1. Invoice address is complete
             2. Shipping address is complete
             3. Selected payment method is complete
             4. There a items in the cart            
        """        
        # Get shop
        shop = IShopManagement(self.context).getShop()
        
        # Get shipping and invoice address
        adressman = IAddressManagement(self.context)
        
        s_addr = adressman.getShippingAddress()
        if s_addr is None: return False
        
        i_addr = adressman.getInvoiceAddress()
        if i_addr is None: return False

        # Get payment method
        payman = IPaymentManagement(self.context)
        paymeth = payman.getSelectedPaymentMethod()

        # Get cart of the customer
        cart = ICartManagement(shop).getCart()

        # If there is no cart, the customer hasn't selected a product, hence
        # he is not complete
        if cart is None:
            return False
            
        im = IItemManagement(cart)
        
        # Check all for completeness
        # if at least one is False customer is not complete, too.        
        for toCheck in s_addr, i_addr, paymeth:
            if ICompleteness(toCheck).isComplete() == False:
                return False
        
        # check items in cart
        if im.hasItems() == False:
            return False

        return True
        
class AddressCompleteness:
    """Provides ICompleteness for address content objects
    """
    implements(ICompleteness)
    adapts(IAddress)
    
    def __init__(self, context):
        """
        """
        self.context = context                  

    def isComplete(self):
        """Checks weather the address is complete
        """        
        if len(self.context.getAddress1()) == 0:
            return False
        elif len(self.context.getZipCode()) == 0:
            return False
        elif len(self.context.getCity()) == 0:
            return False
        elif len(self.context.getCountry()) == 0:
            return False

        return True        