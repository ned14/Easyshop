# Zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# EasyShop imports
from Products.EasyShop.interfaces import IAddressManagement
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import ICurrencyManagement
from Products.EasyShop.interfaces import ICustomerManagement
from Products.EasyShop.interfaces import IItemManagement 
from Products.EasyShop.interfaces import IPropertyManagement
from Products.EasyShop.interfaces import IPrices
from Products.EasyShop.interfaces import IShippingManagement

class ICartFormView(Interface):
    """A view to show the cart of the current user.
    """
    def deleteItem():
        """Deletes a item for the cart.
        """
        
    def getCartItems():
        """Returns the items of the current cart.
        """
    
    def getCartPrice():
        """Returns the price of the current cart.
        """
        
    def getGoto():
        """Returns the url to which it should redirect after pushing the back 
        button.
        """

    def getShippingPrice():
        """Returns the shipping price for the current cart.
        """
        
    def refresh():
        """Refreshes the cart.
        """

    def showCheckOutButton():
        """Returns True if the checkout button is to be displayed.
        """

    def showShippingNote():        
        """Returns True if the shipping price can't calculated
        """
        
class CartFormView(BrowserView):
    """
    """
    implements(ICartFormView)

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
        shop = self.context.getShop()        
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
        shop = self.context.getShop()        
        cm   = ICartManagement(shop)

        cart = cm.getCart()
        if cart is None: 
            price = 0.0
        else:    
            price = IPrices(cart).getPriceForCustomer()
        
        cm = ICurrencyManagement(self.context)
        return cm.priceToString(price)

    def getShippingPrice(self):
        """
        """
        shop = self.context.getShop()
        sm = IShippingManagement(shop)
        shipping_price = sm.getPriceForCustomer()

        cm = ICurrencyManagement(shop)
        return cm.priceToString(shipping_price)
        
    def getGoto(self):
        """
        """
        return self.context.request.get("HTTP_REFERER")
                
    def refreshCart(self):
        """
        """
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
        
    def showShippingNote(self):
        """
        """
        # Todo Shipping price should return a message.
        cm = ICustomerManagement(self.context.getShop())
        customer = cm.getAuthenticatedCustomer()

        am = IAddressManagement(customer)
        address = am.getShippingAddress()
        
        if address.getCountry() != "Deutschland":
            return True
        else:
            return False        