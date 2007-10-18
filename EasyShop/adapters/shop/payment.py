# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.content.product.EasyShopProduct import EasyShopProduct
from Products.EasyShop.interfaces import ICustomerManagement
from Products.EasyShop.interfaces import IPaymentManagement
from Products.EasyShop.interfaces import IPaymentMethodContent
from Products.EasyShop.interfaces import IPaymentPrices
from Products.EasyShop.interfaces import IPaymentPriceContent
from Products.EasyShop.interfaces import IShopContent
from Products.EasyShop.interfaces import IShopPaymentMethod
from Products.EasyShop.interfaces import ITaxes
from Products.EasyShop.interfaces import IValidity

class PaymentManagement:
    """An adapter which provides IPaymentManagement for shop content objects.
    """
    implements(IPaymentManagement)
    adapts(IShopContent)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def deletePaymentMethod(self, id):
        """
        """
        try:
            self.context.paymentmethods.manage_delObjects(id)
        except AttributeError:
            return False

        return True

    def getPaymentMethod(self, id):
        """Returns payment method by given id.
        """
        try:
            return self.context.paymentmethods[id]
        except KeyError:
            return None
            
    def getPaymentMethods(self, interface=None, check_validity=False):
        """Returns the payment methods on shop level. 
        """
        # Todo: This can be optimized with Plone 3.0 because there will be an
        # interface index (IIRC).

        result = []
        for object in self.context.paymentmethods.objectValues():

            if interface and interface.providedBy(object) == False:
                continue

            if check_validity and\
               IValidity(object).isValid(object) == False:
                continue                    
                
            result.append(object)
        
        return result
        
    def getSelectedPaymentMethod(self, check_validity=False):
        """Returns the selected payment method of the current customer on shop
        level.
        """
        # First try to get the selected payment method from user level
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()

        # Then from shop level:
        try:
            method = getattr(
                self.context.paymentmethods, 
                customer.getSelectedPaymentMethod())
        except AttributeError:
            # return default, which is prepayment (because for that no
            # information is needed.) Todo: Make this editable
            return getattr(self.context.paymentmethods, "prepayment")
        
        if check_validity == False:
            return method
            
        if IValidity(method).isValid() == True:
            return method
            
        return getattr(self.context.paymentmethods, "prepayment")
        
class PaymentPrices:
    """
    """
    implements(IPaymentPrices)
    adapts(IShopContent)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def getPaymentPrices(self):
        """
        """
        prices = self.context.paymentprices.objectValues("EasyShopPaymentPrice")
        
        result = []
        for price in prices:
            if IPaymentPriceContent.providedBy(price) == False:
                continue
                
            result.append(price)    
        
        return result
        
    def getPriceGross(self):
        """Returns the first valid price.
        """
        for price in self.getPaymentPrices():
            if IValidity(price).isValid() == True:
                return price.getPriceGross()

        return 0

    # Todo: Optimize. The next methods are the same as for shipping tax
    # calculations
    
    def getPriceForCustomer(self):
        """
        """
        return self.getPriceNet() + self.getTaxForCustomer()
        
    def getPriceNet(self):
        """
        """
        return self.getPriceGross() - self.getTax()

    def getTax(self):
        """
        """
        temp_payment_product = self.createTemporaryPaymentProduct()
        taxes = ITaxes(temp_payment_product)        
        tax = taxes.getTax()
        return tax

    def getTaxForCustomer(self):
        """
        """
        temp_payment_product = self.createTemporaryPaymentProduct()
        taxes = ITaxes(temp_payment_product)        
        tax = taxes.getTaxForCustomer()

        return tax

    def getTaxRate(self):
        """
        """
        temp_payment_product = self.createTemporaryPaymentProduct()
        taxes = ITaxes(temp_payment_product)
        tax = taxes.getTaxRate()
        
        return tax

    def getTaxRateForCustomer(self):
        """
        """
        temp_payment_product = self.createTemporaryPaymentProduct()
        taxes = ITaxes(temp_payment_product)
        tax = taxes.getTaxRate()

        return tax

    def createTemporaryPaymentProduct(self):
        """
        """
        temp_payment_product = EasyShopProduct("payment")
        temp_payment_product.setPriceGross(self.getPriceGross())
        temp_payment_product.context = self.context
        
        return temp_payment_product
