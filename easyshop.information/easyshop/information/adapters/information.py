# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.interface import Interface

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import ICurrencyManagement
from Products.EasyShop.interfaces import IShop

class ShopInformation:
    """Provices currency related methods.
    """
    implements(IShopInformation)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.shop = context.getShop()

    def getInformationPage(self):
        """Returns terms and conditions as file and text.
        """        
        try:
            toc = self.context.information.objectValues("InformationPage")[0]
            toc_url  = toc_url.absolute_url()
            toc_text = toc_url.getText()                
        except IndexError:
            toc_url = None
            toc_url = None
        
        return {
            "shop_owner" : self.context.getShopOwner()
            "toc_url"    : toc_url,
            "toc_text"   : toc_text,
        }
        