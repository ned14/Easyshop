# zope imports
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IStockManagement

class IStockInformationPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    """
    """
    implements(IStockInformationPortlet)

    def __init__(self):
        """
        """

    @property
    def title(self):
        """
        """
        return _(u"EasyShop: Stock Information")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('stock_information.pt')

    @property
    def stock_information(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        sm = IStockManagement(shop)
        
        pvm = IProductVariantsManagement(self.context)
        
        if pvm.hasVariants() == False:
            stock_information = sm.getStockInformationFor(self.context)
        else:
            product_variant = pvm.getSelectedVariant()

            # First, we try to get information for the selected product variant
            stock_information = sm.getStockInformationFor(product_variant)

            # If nothing is found, we try to get information for parent product 
            # variants object.
            if stock_information is None:
                stock_information = sm.getStockInformationFor(self.context)
            
        if stock_information is None:
            return None
            
        return IData(stock_information).asDict()
        
    @property
    def available(self):
        """
        """
        return IProduct.providedBy(self.context)
        
class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()