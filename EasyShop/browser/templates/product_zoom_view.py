# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from Products.EasyShop.interfaces import IPhotoManagement

class IProductZoomView(Interface):    
    """
    """
    def getCurrentPhoto():
        """
        """
        
    def getPhotoUrls():
        """
        """
        
class ProductZoomView(BrowserView):
    """
    """
    implements(IProductZoomView)

    def getCurrentPhoto(self):
        """
        """
        ord = self.request.get("ord", 0)
        try:
            ord = int(ord)
        except ValueError:
            ord = 0
                
        try:
            return self.getPhotoUrls()[ord]
        except IndexError:
            return self.getPhotoUrls()[0]

    def getPhotoUrls(self):
        """
        """
        pm = IPhotoManagement(self.context)

        result = []
        for photo in pm.getPhotos():
            result.append({
                "small" : "%s/image_thumb"  % photo.absolute_url(),
                "large" : "%s/image_large" % photo.absolute_url(),
            })
                        
        return result