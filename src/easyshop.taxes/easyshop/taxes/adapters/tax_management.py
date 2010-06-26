# Zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import ITaxManagement

class TaxManagement:
    """An adapter, which provides methods to manage tax objects for shop context
    objects.
    """
    implements(ITaxManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.taxes = self.context.taxes
    
    def getCustomerTaxes(self):
        """
        """
        return self.taxes.objectValues("CustomerTax")

    def getDefaultTaxes(self):
        """
        """
        return self.taxes.objectValues("DefaultTax")
                    
    def getTax(self, id):
        """
        """
        try:
            return self.taxes[id]
        except KeyError:
            return None