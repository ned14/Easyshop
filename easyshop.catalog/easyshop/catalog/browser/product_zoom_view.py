# Five imports
from Products.Five.browser import BrowserView

# easyshop imports 
from easyshop.core.interfaces import IImageManagement

class ProductZoomView(BrowserView):
    """
    """
    def getCurrentImage(self):
        """
        """
        ord = self.request.get("ord", 0)
        try:
            ord = int(ord)
        except ValueError:
            ord = 0
                
        try:
            return self.getImageUrls()[ord]
        except IndexError:
            return self.getImageUrls()[0]

    def getImageUrls(self):
        """
        """
        pm = IImageManagement(self.context)

        result = []
        for image in pm.getImages():
            result.append({
                "small" : "%s/image_thumb"  % image.absolute_url(),
                "large" : "%s/image_large" % image.absolute_url(),
            })
                        
        return result