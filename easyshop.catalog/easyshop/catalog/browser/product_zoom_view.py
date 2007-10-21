# Five imports
from Products.Five.browser import BrowserView

# EasyShop imports 
from Products.EasyShop.interfaces import IPhotoManagement

class ProductZoomView(BrowserView):
    """
    """
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