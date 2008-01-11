# zope imports
from zope.component import getMultiAdapter

# Five imports
from Products.Five.browser import BrowserView

# CMFPlone imports
from Products.CMFPlone.utils import safe_unicode

# plone imports
from plone.memoize.instance import memoize

# ATCT imports
from Products.ATContentTypes.config import HAS_LINGUA_PLONE

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IDiscountsCalculation
from easyshop.core.interfaces import IItemManagement 
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IPaymentPriceManagement
from easyshop.core.interfaces import IPhotoManagement
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShippingMethodManagement
from easyshop.core.interfaces import IShippingPriceManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import ITaxes

class CartFormView(BrowserView):
    """
    """
    def deleteItem(self):
        """
        """        
        toDeleteItem = self.context.REQUEST.get("toDeleteItem")

        cart = self._getCart()
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
        cart = self._getCart()

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

            # Properties
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

            # Discount
            total_price = 0
            discount = IDiscountsCalculation(cart_item).getDiscount()
            if discount is not None:
                discount_price = getMultiAdapter((discount, cart_item)).getPriceForCustomer()

                discount = {
                    "title" : discount.Title(),
                    "value" : cm.priceToString(discount_price, prefix="-"),
                }

                total_price = price - discount_price
                
            # Photo
            photo = IPhotoManagement(product).getMainPhoto()

            # After we have taken properties and stuff from canonical we change
            # to translation to get translated title and url. 
            if HAS_LINGUA_PLONE:
                product = product.getTranslation()
                
            result.append({
                "id"            : cart_item.getId(),
                "product_title" : product.Title(),
                "product_url"   : product.absolute_url(),
                "product_price" : product_price,
                "price"         : cm.priceToString(price),
                "amount"        : cart_item.getAmount(),
                "properties"    : properties,
                "total_price"   : cm.priceToString(total_price),
                "discount"      : discount,
                "photo_url"     : "%s/image_tile" % photo.absolute_url(),
            })
        
        return result

    def getCartPrice(self):
        """Returns the price of the current cart.
        """        
        cart = self._getCart()
        
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

    def getDiscounts(self):
        """
        """
        return []
                
        cm = ICurrencyManagement(self.context)
        
        cart = self._getCart()        

        if cart is None: 
            return []
        
        discounts = []
        for cart_item in IItemManagement(cart).getItems():
            discount = IDiscountsCalculation(cart_item).getDiscount()

            if discount is not None:
                value = getMultiAdapter((discount, cart_item)).getPriceForCustomer()
                discounts.append({
                    "title" : discount.Title(),
                    "value" : cm.priceToString(value, prefix="-"),
                })
        
        return discounts
                
    def getPaymentMethodTypes(self):
        """Returns all *types* of payment methods of the current customer.
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        pm = IPaymentMethodManagement(self.context)
                
        result = []        
        for payment_method in pm.getPaymentMethods(check_validity=True):
            
            id = payment_method.getId()
            selected = (id == customer.selected_payment_method)
            
            
            result.append({            
                "id"       : payment_method.getId(),
                "title"    : payment_method.Title(),
                "selected" : selected,
            })

        return result
                
    def getPaymentInfo(self):
        """
        """
        pp = IPaymentPriceManagement(self.context)
        price = pp.getPriceForCustomer()

        cm = ICurrencyManagement(self.context)
        price =  cm.priceToString(price)

        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        pim = IPaymentInformationManagement(customer)
        selected_payment_method = pim.getSelectedPaymentMethod()
        
        return {
            "price"       : price,
            "title"       : selected_payment_method.Title(),
        }

    def getShippingMethods(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        selected_shipping_id = customer.selected_shipping_method
        
        sm = IShippingMethodManagement(self.context)
        
        shipping_methods = []
        for shipping in sm.getShippingMethods(check_validity=True):

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

    def getShippingInfo(self):
        """
        """
        sm = IShippingPriceManagement(self.context)
        shipping_price = sm.getPriceForCustomer()

        cm = ICurrencyManagement(self.context)
        price = cm.priceToString(shipping_price)
        method = IShippingMethodManagement(self.context).getSelectedShippingMethod()
                
        return {
            "price"       : price,
            "title"       : method.Title(),
            "description" : method.Description()
        }

    def getTaxForCustomer(self):
        """
        """
        cm   = ICurrencyManagement(self.context)                
        cart = self._getCart()
        
        if cart is None:
            tax = 0.0
        else:
            tax  = ITaxes(cart).getTaxForCustomer()

        return cm.priceToString(tax)
        
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
        customer.selected_payment_method = \
            safe_unicode(self.request.get("selected_payment_method"))
            
        cart = self._getCart()
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
            url = "%s/checkout-order-preview" % self.context.absolute_url()
        else:
            url = "%s/cart" % self.context.absolute_url()

        return  self.context.request.response.redirect(url)        

    def showCheckOutButton(self):
        """
        """
        cart = self._getCart()
        if IItemManagement(cart).hasItems():
            return True

        return False

    @memoize
    def _getCart(self):
        """Returns the cart.
        """
        return ICartManagement(self.context).getCart()