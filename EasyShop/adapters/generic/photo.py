# zope imports
from zope.interface import implements

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import IPhotoManagement

class PhotoManagement:
    """Provides IPhotoManagement
    """
    implements(IPhotoManagement)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def getMainPhoto(self):
        """Returns the main photo. This is either the image field of the
        product or the first Photo object within the product.
        """ 
        # Returns the object(s), which contains the image field (not the image
        # field itself), to be able to get image_shop_large. etc.
        image = self.context.getField("image").get(self.context)
        if len(image) != 0:
            return self.context
        else:
            try:
                return self.context.objectValues("Photo")[0]
            except IndexError:
                return None
                
    def getPhotos(self):
        """Returns all photos.
        """
        result = []
        image = self.context.getField("image").get(self.context)
        if len(image) != 0:
            result.append(self.context)
        
        result.extend(self.context.objectValues("Photo"))
        return result
        
    def hasPhotos(self):
        """Returns True if at least one photo exists.
        """
        return len(self.getPhotos()) > 0