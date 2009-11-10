# Zope imports
from zLOG import LOG, INFO
from DateTime import DateTime

# CMFCore imports
from Products.CMFCore.utils import getToolByName

class ManageSessions:
    """
    """
    def deleteCarts(self):
        """Delete expired Sessions
        """
        now = DateTime()
        
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            object_provides="easyshop.core.interfaces.shop.IShop"
        )

        for brain in brains:
            shop = brain.getObject()
            to_delete = []
            for cart in shop.carts.objectValues():
                
                # delete only expired carts
                if now - cart.modified() < 10:
                    continue
                
                # delete only anonymous carts
                if cart.getId().isdigit() == False:
                    continue
                         
                to_delete.append(cart.getId())
            
            shop.carts.manage_delObjects(to_delete)
            LOG("Delete Carts", INFO, "%s expired carts deleted for %s" % (len(to_delete), shop.Title()))


    def deleteCustomers(self):
        """
        """
        now = DateTime()
        
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            object_provides="easyshop.core.interfaces.shop.IShop"
        )

        for brain in brains:
            shop = brain.getObject()
            to_delete = []
            for customer in shop.customers.objectValues():
                
                # delete only expired carts
                if now - customer.modified() < 10:
                    continue
                
                # delete only anonymous carts
                if customer.getId().isdigit() == False:
                    continue
                         
                to_delete.append(cart.getId())
            
            shop.customers.manage_delObjects(to_delete)
            LOG("Delete Customers", INFO, "%s expired customers deleted for %s" % (len(to_delete), shop.Title()))
        