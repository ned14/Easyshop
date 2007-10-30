# Python imports
import re

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# plone imports
from plone.memoize.instance import memoize

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IShopManagement

class CustomersContainerView(BrowserView):
    """
    """
    def getCart(self):
        """
        """
        customer = self._getCustomer()
        if customer is None:
            return None
            
        shop = IShopManagement(self.context).getShop()
        cart = ICartManagement(shop).getCartById(customer.getId())
        
        if cart is None:
            return None
        else:
            return {
                "url" : cart.absolute_url()
            }
        
    def getCustomer(self):
        """
        """
        customer = self._getCustomer()
        if customer is None:
            return None
            
        return {
            "name" : self._getCustomerName(customer.getId()),
            "url"  : customer.absolute_url(),
        }
                
    def getCustomers(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
                
        searchable_text = self.request.get("searchable_text", "")
        if searchable_text != "":
            result = catalog.searchResults(
                path = "/".join(self.context.getPhysicalPath()),
                portal_type = "Customer",
                SearchableText = searchable_text,
                sort_on = "sortable_title",
            )
        
            return result
        
        letter = self.request.get("letter", "")
        if letter == "":
            return []
        
        result = []
        if letter == "All":
            result = catalog.searchResults(
                path = "/".join(self.context.getPhysicalPath()),
                portal_type = "Customer",
                sort_on = "sortable_title",
            )
            
        elif letter == "0-9":
            brains = catalog.searchResults(
                path = "/".join(self.context.getPhysicalPath()),
                portal_type = "Customer",
                sort_on = "sortable_title",
            )
                    
            for brain in brains:
                if re.match("\d", brain.Title):
                    result.append(brain)
        else:
            brains = catalog.searchResults(
                path = "/".join(self.context.getPhysicalPath()),
                portal_type = "Customer",
                Title = "%s*" % letter,
                sort_on = "sortable_title",
            )
            
            for brain in brains:
                if brain.Title.upper().startswith(letter):
                    result.append(brain)

        temp = []
        for customer in result:

            temp.append({
                "name" : self._getCustomerName(customer.getId),
                "uid"  : customer.UID,
                "url"  : customer.getURL(),
            })
        
        return temp
        
    def getLetters(self):
        """
        """
        return  ("All", "0-9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", 
                 "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W",
                 "X", "Y", "Z")

    def getOrders(self):
        """
        """
        ttool = getToolByName(self.context, 'translation_service')
        wftool = getToolByName(self.context, "portal_workflow")

        customer = self._getCustomer()
        if customer is  None:
            return []
            
        shop = IShopManagement(self.context).getShop()
        om = IOrderManagement(shop)
        
        orders = []                
        for order in om.getOrdersForCustomer(customer.getId()):
            
            # get fullname
            fullname = "There is no customer."
            customer = order.getCustomer()
            if customer is not None:
                am = IAddressManagement(customer)
                address = am.getInvoiceAddress()
                if address is not None:
                    fullname = address.getName(reverse=True)
                                
            # created
            created = ttool.ulocalized_time(order.created(), long_format=True)
            
            orders.append({
                "id"            : order.getId(),
                "url"           : order.absolute_url(),
                "created"       : created,
                "customer_name" : fullname,
                "review_state"  : wftool.getInfoFor(order, "review_state")
            })
            
        return orders   
        
    @memoize
    def _getCustomer(self):
        """
        """
        uid = self.request.get("uid")
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            UID = uid
        )
        
        try:
            return brains[0].getObject()
        except:
            return None
                    
    def _getCustomerName(self, customer_id):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")            
        member = mtool.getMemberById(customer_id)
        if member and member.getProperty('firstname') and member.getProperty('lastname'):
            name = member.getProperty('firstname') + " " + \
                   member.getProperty('lastname')
        else:
            name = customer_id
            
        return name