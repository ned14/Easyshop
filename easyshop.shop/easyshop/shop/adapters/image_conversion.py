# zope imports
from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IImageConversion

class ImageConversion:
    """Dummy adapter to convert image before saving. 
    
    3rd-party developers can provide their own adapter to convert/add images
    before they are saved. See a example in DemmelhuberShop.
    """
    implements(IImageConversion)
    adapts(Interface)

    def __init__(self, context):
        self.context = context
    
    def convertImage(self, data):
        """
        """
        return data