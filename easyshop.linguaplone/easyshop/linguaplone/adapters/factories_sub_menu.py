# zope imports
from zope.interface import implements

# plone.app.contentmenu imports
from plone.app.contentmenu.menu import FactoriesSubMenuItem
from plone.app.contentmenu.interfaces import IFactoriesSubMenuItem

# CMFCore imports
from Products.CMFCore.utils import getToolByName

class EasyShopFactoriesSubMenuItem(FactoriesSubMenuItem):
    """
    """
    implements(IFactoriesSubMenuItem)
    
    def available(self):
        """Show add menu only when the current language is the default language.
        """
        ltool = getToolByName(self.context, "portal_languages")
        default_language  = ltool.getDefaultLanguage()            
        preferred_lanuage = ltool.getPreferredLanguage()
        
        if default_language != preferred_lanuage:
            return False
        else:
            return super(EasyShopFactoriesSubMenuItem, self).available()