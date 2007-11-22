# Five imports
from Products.Five.browser import BrowserView

# CMFPlone imports
from Products.CMFPlone.utils import safe_unicode

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IItemManagement 
from easyshop.core.interfaces import IPaymentManagement
from easyshop.core.interfaces import IPaymentPrices
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShippingManagement
from easyshop.core.interfaces import IShopManagement

class CartFormView(BrowserView):
    """
    """
    def deleteItem(self):
        """
        """        
        toDeleteItem = self.context.REQUEST.get("toDeleteItem")

        cart = ICartManagement(self.context).getCart()        
        IItemManagement(cart).deleteItem(toDeleteItem)

        url = "%s/cart" % self.context.absolute_url()

        # keep goto
        goto = self.request.get("goto", "")
        if goto != "": url += "?goto=%s" % goto
                    
        self.context.request.response.redirect(url)
        
    def getCartItems(self):
        """
        """    
        shop = IShopManagement(self.context).getShop()        
        cm   = ICartManagement(shop)

        cart = cm.getCart()

        # If there isn't a cart yet
        if cart is None:
            return []
            
        cm = ICurrencyManagement(self.context)
        
        result = []
        for cart_item in IItemManagement(cart).getItems():
            
            product = cart_item.getProduct()

            product_price = IPrices(cart_item).getPriceForCustomer() / cart_item.getAmount()
            product_price = cm.priceToString(product_price)
            
            price = IPrices(cart_item).getPriceForCustomer()
            price = cm.priceToString(price)

            properties = []
            pm = IPropertyManagement(product)

            for selected_property in cart_item.getProperties():
                property_price = pm.getPriceForCustomer(
                    selected_property["id"], 
                    selected_property["selected_option"]) 

                # This could happen if a property is deleted and there are 
                # still product with this selected property in the cart.
                # Todo: Think about, whether theses properties are not to 
                # display. See also checkout_order_preview
                try:    
                    property_title = pm.getProperty(
                        selected_property["id"]).Title()
                except AttributeError:
                    property_title = selected_property["id"]
                    
                properties.append({
                    "id" : selected_property["id"],
                    "selected_option" : selected_property["selected_option"],
                    "title" : property_title,
                    "price" : cm.priceToString(property_price)
                })
                
            result.append({
                "id"            : cart_item.getId(),
                "product_title" : product.Title(),
                "product_price" : product_price,
                "properties"    : properties,
                "price"         : price,
                "amount"        : cart_item.getAmount(),
            })
        
        return result

    def getCartPrice(self):
        """Returns the price of the current cart.
        """        
        shop = IShopManagement(self.context).getShop()        
        cm   = ICartManagement(shop)

        cart = cm.getCart()
        if cart is None: 
            price = 0.0
        else:    
            price = IPrices(cart).getPriceForCustomer()
        
        cm = ICurrencyManagement(self.context)
        return cm.priceToString(price)

    def getCountries(self):
        """Returns available countries.
        """
        result = []                
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        shop = IShopManagement(self.context).getShop()
        for country in shop.getCountries():
            result.append({
                "title" : country,
                "selected" : safe_unicode(country) == customer.selected_country                
            })
        
        return result    

    def getPaymentMethodTypes(self):
        """Returns all *types* of payment methods of the current customer.
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        pm = IPaymentManagement(self.context)
                
        result = []        
        for payment_method in pm.getPaymentMethods():
            
            id = payment_method.getId()
            selected = (id == customer.selected_payment_method_type)
            
            result.append({            
                "id"       : payment_method.getId(),
                "title"    : payment_method.Title(),
                "selected" : selected,
            })

        return result
                
    def getPaymentPrice(self):
        """
        """
        pp = IPaymentPrices(self.context)
        payment_price = pp.getPriceForCustomer()

        cm = ICurrencyManagement(self.context)
        return cm.priceToString(payment_price)

    def getShippingMethods(self):
        """
        """
        # TODO: Factor this out? Same is used within checkout/browser/shipping.py
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        selected_shipping_id = customer.selected_shipping_method
        
        sm = IShippingManagement(self.context)
        
        shipping_methods = []
        for shipping in sm.getShippingMethods():

            if selected_shipping_id == safe_unicode(shipping.getId()):
                checked = True
            elif selected_shipping_id == u"" and shipping.getId() == "default":
                checked = True
            else:
                checked = False
                            
            shipping_methods.append({
                "id" : shipping.getId(),
                "title" : shipping.Title,
                "description" : shipping.Description,
                "checked" : checked,
            })
            
        return shipping_methods        
        
    def getShippingPrice(self):
        """
        """
        sm = IShippingManagement(self.context)
        shipping_price = sm.getPriceForCustomer()

        cm = ICurrencyManagement(self.context)
        return cm.priceToString(shipping_price)
        
    def getGoto(self):
        """
        """
        return self.context.request.get("HTTP_REFERER")
                
    def refreshCart(self):
        """
        """            
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()        
        
        # Set selected country global and within current selected invoice 
        # address. Why? If a customer delete all addresses the current selected 
        # country is still saved global and can be used to calculate the 
        # shipping price.        
        selected_country = safe_unicode(self.request.get("selected_country"))
        customer.selected_country = selected_country
        invoice_address = IAddressManagement(customer).getInvoiceAddress()
        if invoice_address is not None:
            invoice_address.country = selected_country

        # Set selected shipping method
        customer.selected_shipping_method = \
            safe_unicode(self.request.get("selected_shipping_method"))

        # Set selected payment method type
        customer.selected_payment_method_type = \
            safe_unicode(self.request.get("selected_payment_method_type"))
            
        cart = ICartManagement(self.context).getCart()
        item_manager = IItemManagement(cart)

        i = 1
        for cart_item in item_manager.getItems():
            ci = "cart_item_%s" % i
            amount = self.context.REQUEST.get(ci)
            
            try:
                amount = int(amount)
            except ValueError:
                continue
            
            if amount < 0:
                continue
                    
            if amount == 0:
                item_manager.deleteItemByOrd(i-1)
            else:    
                cart_item.setAmount(amount)
            i += 1

        # next template
        if self.context.REQUEST.get("goto", "") == "order-preview":
            url = "%s/check-out-order-preview-form" % self.context.absolute_url()
        else:
            url = "%s/cart" % self.context.absolute_url()

        return  self.context.request.response.redirect(url)        

    def showCheckOutButton(self):
        """
        """
        cart = ICartManagement(self.context).getCart()
        
        if IItemManagement(cart).hasItems():
            return True

        return False