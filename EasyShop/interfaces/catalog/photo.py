# Zope imports
from zope.interface import Interface

class IProductPhoto(Interface):
    """Marker interface for a product photo content objects.
    """                                       
    
class IImageConversion(Interface):
    """Provides methods to convert an image. 
    """
    def convertImage(image):
        """Convert given image.
        """
        
class IPhotoManagement(Interface):
    """Provides methods to manage photo content objects.
    """    
    def getMainPhoto():
        """Return the main photo.
        """    

    def getPhotos():
        """Returns all photos.
        """
        
    def hasPhotos():
        """Returns True if at least one photo exists.
        """        