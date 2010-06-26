# zope imports
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IInformationManagement

class IInformationPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    """
    """
    implements(IInformationPortlet)

    def __init__(self):
        """
        """

    @property
    def title(self):
        """
        """
        return _(u"EasyShop: Information")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('information.pt')
    
    def update(self):
        """
        """
        self.information = self._information()

    @memoize    
    def _information(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        im = IInformationManagement(shop)
        
        pvm = IProductVariantsManagement(self.context)
        
        if pvm.hasVariants() == False:
            information = im.getInformationPagesFor(self.context)
        else:
            product_variant = pvm.getSelectedVariant()

            # First, we try to get information for the selected product variant
            information = im.getInformationPagesFor(product_variant)

            # If nothing is found, we try to get information for parent product 
            # variants object.
            if information is None:
                information = im.getInformationPagesFor(self.context)
            
        return information
        
    @property
    def available(self):
        """
        """
        return len(self._information()) > 0
        
class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()