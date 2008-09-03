# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.catalog.content.product import Product
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IPaymentPriceManagement
from easyshop.core.interfaces import IPaymentPrice
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import ITaxes
from easyshop.core.interfaces import IValidity

class PaymentPriceManagement(object):
    """Provides IPaymentPriceManagement for shop content objects.
    """
    implements(IPaymentPriceManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.paymentprices = self.context.paymentprices
        
    def getPaymentPrices(self):
        """
        """
        prices = self.paymentprices.objectValues("PaymentPrice")
        
        result = []
        for price in prices:
            if IPaymentPrice.providedBy(price) == False:
                continue
                
            result.append(price)    
        
        return result
        
    def getPriceGross(self):
        """Returns the first valid price.
        """
        for price in self.getPaymentPrices():
            if IValidity(price).isValid() == True:
                return price.getPrice()

        return 0

    def getPriceForCustomer(self):
        """
        """
        # If there a no items the payment price for cutomers is zero.
        cart_manager = ICartManagement(self.context)
        cart = cart_manager.getCart()        
        
        if cart is None:
            return 0
                    
        cart_item_manager = IItemManagement(cart)
        if cart_item_manager.hasItems() == False:
            return 0
                
        return self.getPriceNet() + self.getTaxForCustomer()
        
    def getPriceNet(self):
        """
        """
        return self.getPriceGross() - self.getTax()

    def getTax(self):
        """
        """
        temp_payment_product = self._createTemporaryPaymentProduct()
        taxes = ITaxes(temp_payment_product)        
        tax = taxes.getTax()
        return tax

    def getTaxForCustomer(self):
        """
        """
        temp_payment_product = self._createTemporaryPaymentProduct()
        taxes = ITaxes(temp_payment_product)        
        tax = taxes.getTaxForCustomer()

        return tax

    def getTaxRate(self):
        """
        """
        temp_payment_product = self._createTemporaryPaymentProduct()
        taxes = ITaxes(temp_payment_product)
        tax = taxes.getTaxRate()
        
        return tax

    def getTaxRateForCustomer(self):
        """
        """
        temp_payment_product = self._createTemporaryPaymentProduct()
        taxes = ITaxes(temp_payment_product)
        tax = taxes.getTaxRate()

        return tax

    def _createTemporaryPaymentProduct(self):
        """
        """
        temp_payment_product = Product("payment")
        temp_payment_product.setPrice(self.getPriceGross())
        temp_payment_product.context = self.context
        
        return temp_payment_product
