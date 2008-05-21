# zope imports
from zope.interface import Interface

# plone imports
from plone.app.portlets.interfaces import IColumn

# easyshop.imports
from easyshop.core.interfaces import IFormatable

class IShop(IFormatable):
    """Marker interface to mark shop content objects.
    """
    
class IShopInformation(Interface):
    """Methods which provide information of an shop.
    """
    def getTermsAndConditions():
        """Returns terms and conditions as file and text.
        """
        
class IShopManagement(Interface):
    """
    """
    def getShop():
        """Returns the parent shop
        """

class ICountryVocabulary(Interface):
    """
    """
    
class IEasyShopTop(IColumn):
    """A portlet for EasyShop
    """
    
class IEasyShopBottom(IColumn):
    """A portlet for EasyShop
    """