# Zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import ITaxManagement
from easyshop.taxes.adapters.tax_management \
    import TaxManagement as BaseTaxManagement

# easymall imports
from easymall.mall.interfaces import IMall

class MallTaxManagement(BaseTaxManagement):
    """An adapter, which provides methods to manage tax objects for mall context
    objects.
    """
    implements(ITaxManagement)
    adapts(IMall)

class ShopTaxManagement(BaseTaxManagement):
    """An adapter, which provides methods to manage tax objects for shop context
    objects.
    """
    implements(ITaxManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        
        mall = self.context.aq_inner.aq_parent
        self.taxes = mall.taxes