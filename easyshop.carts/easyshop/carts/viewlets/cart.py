# zope imports
from zope.component import getMultiAdapter
from zope.component import getUtility

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# CMFPlone imports
from Products.CMFPlone.utils import safe_unicode

# plone imports
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IDiscountsCalculation
from easyshop.core.interfaces import IItemManagement 
from easyshop.core.interfaces import INumberConverter
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IPaymentPriceManagement
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProductVariant
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IShippingMethodManagement
from easyshop.core.interfaces import IShippingPriceManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import ITaxes

class CheckoutCartViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('cart.pt')
        
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
    
    @memoize
    def getCartItems(self):
        """
        """    
        shop = IShopManagement(self.context).getShop()        
        cart = self._getCart()

        # If there isn't a cart yet
        if cart is None:
            return []
            
        cm = ICurrencyManagement(self.context)
        
        total_amount = 0
        result = []
        for cart_item in IItemManagement(cart).getItems():
            
            product = cart_item.getProduct()

            product_price = IPrices(cart_item).getPriceForCustomer() / cart_item.getAmount()
            product_price = cm.priceToString(product_price)
            
            price = IPrices(cart_item).getPriceForCustomer()

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
            
            # Product title
            data = IData(product).asDict()
            title = data["title"]
            
            # Amount
            amount = cart_item.getAmount()
            
            result.append({
                "id"            : cart_item.getId(),
                "product_title" : title,
                "product_url"   : product.absolute_url(),
                "product_price" : product_price,
                "price"         : cm.priceToString(price),
                "amount"        : amount,
                "properties"    : self._getProperties(cart_item),
                "total_price"   : cm.priceToString(total_price),
                "discount"      : discount,
            })
            
            total_amount += amount
            
        return {
            "cart_items" : result,
            "total_amount" : total_amount
        }

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
        
        if selected_payment_method is None: 
            return {
                "display" : False
            }
        else:    
            return {
                "price"   : price,
                "title"   : selected_payment_method.Title(),
                "display" : len(self.getCartItems()) > 0,
            }

    def _getProperties(self, cart_item):
        """
        """
        product = cart_item.getProduct()
        if IProductVariant.providedBy(product):
            return self._getPropertiesForVariants(cart_item)
        else:
            return self._getPropertiesForConfiguration(cart_item)
    
    # TODO: Try to factory this out to use this just on one place. See
    # catalog/vievlets/product.py
    def _getPropertiesForConfiguration(self, cart_item):
        """
        """        
        u = getUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)

        # Store all selected options for lookup below
        selected_options = {}
        
        for property in cart_item.getProperties():
            selected_options[property["id"]] = property["selected_option"]

        product = cart_item.getProduct()
        pm = IPropertyManagement(product)
        
        result = []
        for property in pm.getProperties():
            
            # Only properties with at least one option are displayed.
            if len(property.getOptions()) == 0:
                continue
            
            options = []
            for option in property.getOptions():

                # generate value string
                option_id    = option["id"]
                option_name  = option["name"]
                option_price = option["price"]

                if option_price != "0.0":
                    option_price = u.stringToFloat(option_price)
                    option_price = cm.priceToString(option_price, "long", "after")
                    content = "%s %s" % (option_name, option_price)
                else:
                    content = option_name
                        
                # is option selected?
                selected_option = selected_options.get(property.getId(), "")
                selected = option_id == selected_option
                
                options.append({
                    "id"       : option_id,
                    "title"    : content,
                    "selected" : selected,
                })
                
            result.append({
                "id"      : "property_" + property.getId(),
                "title"   : property.Title(),
                "options" : options,
            })

        return result

    def _getPropertiesForVariants(self, cart_item):
        """
        """        
        u = getUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)

        variant = cart_item.getProduct()
        product = variant.aq_inner.aq_parent

        selected_options = {}
        for property in variant.getForProperties():
            name, value = property.split(":")
            selected_options[name] = value
            
        pm = IPropertyManagement(product)
        
        result = []
        for property in pm.getProperties():
            
            # Only properties with at least one option are displayed.
            if len(property.getOptions()) == 0:
                continue
            
            options = []
            for option in property.getOptions():

                # generate value string
                option_id = option["id"]
                option_name = option["name"]
                content = option_name
                        
                # is option selected?
                selected_option = selected_options.get(property.getId(), "")
                selected = option_id == selected_option
                
                options.append({
                    "id"       : option_id,
                    "title"    : content,
                    "selected" : selected,
                })
                
            result.append({
                "id"      : "property_" + property.getId(),
                "title"   : property.Title(),
                "options" : options,
            })

        return result

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
        
        if method is None:
            return {
                "display"     : False,
            }        
        else:
            return {
                "price"       : price,
                "title"       : method.Title(),
                "description" : method.Description(),
                "display"     : len(self.getCartItems()) > 0
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

        return cm.priceToString(tax, suffix=None)
        
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
        if cart is None:
            url = "%s/cart" % self.context.absolute_url()
            self.context.request.response.redirect(url)
            return

        # Collect cart item properties for lookup
        selected_properties = {}
        for key, value in self.context.request.items():
            if key.startswith("property_"):
                property_id, cart_item_id = key.split(":")
                property_id = property_id[9:]

                if selected_properties.has_key(cart_item_id) == False:
                    selected_properties[cart_item_id] = []

                selected_properties[cart_item_id].append({
                    "id" : property_id,
                    "selected_option" : value})
        
        im = IItemManagement(cart)

        i = 1
        for cart_item in im.getItems():
            ci = "cart_item_%s" % i
            amount = self.context.REQUEST.get(ci)
                        
            try:
                amount = int(amount)
            except ValueError:
                continue
            
            if amount < 0:
                continue
                    
            if amount == 0:
                im.deleteItemByOrd(i-1)
            else:    
                cart_item.setAmount(amount)
            i += 1

            # Set properties
            product = cart_item.getProduct()
            if IProductVariant.providedBy(product):
                product = product.aq_inner.aq_parent
                pvm = IProductVariantsManagement(product)
                
                # We need the properties also as dict to get the selected 
                # variant. Feels somewhat dirty. TODO: Try to unify the data 
                # model for properties.
                properties = {}
                for property in selected_properties[cart_item.getId()]:
                    properties[property["id"]] = property["selected_option"]                    
                    
                variant = pvm.getSelectedVariant(properties)
                cart_item.setProduct(variant)
                
                # TODO: At the moment we have to set the properties of the cart
                # item too. This is used in checkout-order-preview. Think about 
                # to get rid of this because the properties are already available 
                # in the variant.
                cart_item.setProperties(selected_properties[cart_item.getId()])
                
            else:
                if selected_properties.has_key(cart_item.getId()):
                    cart_item.setProperties(selected_properties[cart_item.getId()])
            
        # next template
        if self.context.REQUEST.get("goto", "") == "order-preview":
            url = "%s/checkout-order-preview" % self.context.absolute_url()
        else:
            url = "%s/cart" % self.context.absolute_url()

        self.context.request.response.redirect(url)

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