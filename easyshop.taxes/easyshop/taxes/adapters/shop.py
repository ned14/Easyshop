# Zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import ITaxes
from easyshop.core.interfaces import ITaxManagement
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IShopManagement

class TaxManagement:
    """An adapter, which provides methods to manage tax objects for shop 
    context objects
    """
    implements(ITaxManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
    
    def getCustomerTaxes(self):
        """
        """
        return self.context.taxes.objectValues("CustomerTax")
        
        # Todo: Optimize        
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = "/".join(self.context.taxes.getPhysicalPath()),
            portal_type="CustomerTax",
            sort_on = "getObjPositionInParent",
        )

        # Todo
        return [brain.getObject() for brain in brains]

    def getDefaultTaxes(self):
        """
        """
        return self.context.taxes.objectValues("DefaultTax")
        shop = IShopManagement(self.context).getShop()
        
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = "/".join(self.context.taxes.getPhysicalPath()),
            portal_type="DefaultTax",
            sort_on = "getObjPositionInParent",
        )

        # Todo
        return [brain.getObject() for brain in brains]
                    
    def getTax(self, id):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            portal_type = ("DefaultTax", "CustomerTax"),
            path = "/".join(self.context.taxes.getPhysicalPath()),
            id = id,
        )

        try:
            return brains[0].getObject()
        except IndexError:
            return None