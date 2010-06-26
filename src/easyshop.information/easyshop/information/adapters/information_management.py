# zope imports
from zope.component import adapts
from zope.interface import implements

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IInformationManagement
from easyshop.core.interfaces import IValidity

class InformationManagement:
    """Adapter which provides InformationManagement for shop content objects.
    """
    implements(IInformationManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.information = context["information"]

    def getInformationPage(self, id):
        """
        """
        try:
            return self.information[id]
        except KeyError:
            return None
        
    def getInformationPages(self):
        """
        """
        return self.information.objectValues()
        
    def getInformationPagesFor(self, product):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        
        result = []
        for information in self.information.objectValues():
            if IValidity(information).isValid(product) == False:
                continue
                
            if IValidity(information).isValid(product) == False:
                continue

            if mtool.checkPermission("View", information) != True:
                continue
                
            result.append({
                "title" : information.Title(),
                "id"    : information.getId(),
            })

        return result