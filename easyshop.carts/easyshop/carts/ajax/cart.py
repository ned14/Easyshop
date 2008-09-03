# zope imports
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewletManager

# CMFPlone imports
from Products.CMFPlone.utils import safe_unicode

# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IItemManagement 
from easyshop.core.interfaces import IProductVariant
from easyshop.core.interfaces import IProductVariantsManagement

class AjaxView(BrowserView):
    """
    """ 
    def deleteItem(self):
        """
        """        
        toDeleteItem = self.context.REQUEST.get("toDeleteItem")

        cart = ICartManagement(self.context).getCart()
        IItemManagement(cart).deleteItem(toDeleteItem)
        
        return self._render()
        
    def refreshCart(self):
        """
        """
        self._refreshCart()
        return self._render()

    def _render(self):
        """
        """
        renderer = getMultiAdapter((self.context, self.request, self), IViewletManager, name="easyshop.carts.cart-manager")
        renderer = renderer.__of__(self.context)
                
        renderer.update()        
        return renderer.render()
                
    def _refreshCart(self):
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
            
        cart = ICartManagement(self.context).getCart()
        if cart is None:
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
        
        total_items = 0
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