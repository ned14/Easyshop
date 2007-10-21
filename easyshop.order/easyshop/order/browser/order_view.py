# Zope imports
from AccessControl import Unauthorized

# zope imports
from zope.component import queryUtility

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IAddressManagement
from Products.EasyShop.interfaces import ICurrencyManagement
from Products.EasyShop.interfaces import IItemManagement
from Products.EasyShop.interfaces import INumberConverter
from Products.EasyShop.interfaces import IPaymentManagement
from Products.EasyShop.interfaces import IPrices
from Products.EasyShop.interfaces import IType

class OrderView(BrowserView):
    """
    """
    def disable_border(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        if mtool.checkPermission('Manage portal', self.context):
            return False
        return True
        
    def getCreationDate(self):
        """
        """
        date = self.context.created()        
        
        tool = getToolByName(self.context, 'translation_service')
        return tool.ulocalized_time(date, long_format=True)
                
    def getCustomerFullname(self):
        """
        """
        # Todo: Create an adapter Address Management for IOrder         
        customer = self.context.getCustomer()
        am = IAddressManagement(customer)
        address = am.getInvoiceAddress()
        
        return address.getName()

    def getEmail(self):
        """
        """                
        customer = self.context.getCustomer()
        
        mtool = getToolByName(self.context, "portal_membership")

        try:
            member = mtool.getMemberById(customer.getId())
        except Unauthorized:
            return None
        else:
            if member is not None:
                return member.getProperty("email")
            
        return None
                
    def getItems(self):
        """
        """    
        nc = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)
        
        items = []
        item_manager = IItemManagement(self.context)
        for item in item_manager.getItems():

            product_price_net = cm.priceToString(item.getProductPriceNet())
            price_net = cm.priceToString(item.getPriceNet())
            tax_rate = nc.floatToTaxString(item.getTaxRate())
            tax = cm.priceToString(item.getTax())
            price_gross = cm.priceToString(item.getPriceGross())

            temp = {
                "product_title"     : item.getProduct().Title(),
                "product_quantity"  : item.getProductQuantity(),
                "product_price_net" : product_price_net,
                "price_net"         : price_net,
                "tax_rate"          : tax_rate,
                "tax"               : tax,
                "price_gross"       : price_gross,
                "properties"        : item.getProperties(),
            }
            items.append(temp)

        return items

    def getPaymentValues(self):
        """
        """
        nc = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)

        price_net = cm.priceToString(self.context.getPaymentPriceNet())
        price_gross = cm.priceToString(self.context.getPaymentPriceGross())
        tax_rate = nc.floatToTaxString(self.context.getPaymentTaxRate())
        tax = cm.priceToString(self.context.getPaymentTax())
        
        return {
            "display" : self.context.getPaymentPriceGross() != 0,
            "price_net" : price_net,
            "price_gross" : price_gross,
            "tax_rate" : tax_rate,
            "tax" : tax, 
            "title" : "Cash on Delivery"
        }
        
    def getPaymentMethod(self):
        """
        """
        customer = self.context.getCustomer()
        pm = IPaymentManagement(customer)                
        return pm.getSelectedPaymentMethod()
        
    def getPaymentMethodType(self):
        """
        """
        pm = self.getPaymentMethod()
        return IType(pm).getType()
        
    def getPriceForCustomer(self):
        """
        """
        p = IPrices(self.context)        
        price = p.getPriceForCustomer()

        cm = ICurrencyManagement(self.context)
        return cm.priceToString(price)
        
    def getInvoiceAddress(self):
        """
        """
        # Todo: Create an adapter Address Management for IOrder 
        customer = self.context.getCustomer()
        am = IAddressManagement(customer)
        address = am.getInvoiceAddress()
        
        return {
            "name" : address.getName(),
            "company_name" : address.getCompanyName(),
            "address1" : address.getAddress1(),
            "address2" : address.getAddress2(),
            "zipcode" : address.getZipCode(),
            "city": address.getCity(),
            "country" : address.getCountry(),
            "phone" : address.getPhone()            
        }
        
    def getShippingAddress(self):
        """
        """
        # Todo: Create an adapter Address Management for IOrder         
        customer = self.context.getCustomer()
        am = IAddressManagement(customer)
        address = am.getShippingAddress()
        
        return {
            "name" : address.getName(),
            "company_name" : address.getCompanyName(),
            "address1" : address.getAddress1(),
            "address2" : address.getAddress2(),
            "zipcode" : address.getZipCode(),
            "city": address.getCity(),
            "country" : address.getCountry(),
            "phone" : address.getPhone(),
        }

    def getShipping(self):
        """
        """
        nc = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)

        price_net = cm.priceToString(self.context.getShippingPriceNet())
        price_gross = cm.priceToString(self.context.getShippingPriceGross())
        tax_rate = nc.floatToTaxString(self.context.getShippingTaxRate())
        tax = cm.priceToString(self.context.getShippingTax())
        
        return {
            "price_net" : price_net,
            "price_gross" : price_gross,
            "tax_rate" : tax_rate,
            "tax" : tax,    
        }
    
    def getState(self):
        """
        """
        wftool = getToolByName(self.context, "portal_workflow")
        return wftool.getInfoFor(self.context, "review_state")

    def isRedoPaymentAllowed(self):
        """
        """
        pm = IPaymentManagement(self.context)
        m = pm.getSelectedPaymentMethod()
        
        if IType(m).getType() not in REDO_PAYMENT_PAYMENT_METHODS:
            return False

        wftool = getToolByName(self.context, "portal_workflow")
        state = wftool.getInfoFor(self.context, "review_state")
        
        if state not in REDO_PAYMENT_STATES:
            return False

        return True
        
    def redoPayment(self):
        """
        """
        # ATM only PayPal is allowed, so I haven't to differ and no redirect
        # is needed as the paypal process redirects to paypal.com
        if self.isRedoPaymentAllowed():
            pm = IPaymentManagement(self.context)
            pm.processSelectedPaymentMethod()
