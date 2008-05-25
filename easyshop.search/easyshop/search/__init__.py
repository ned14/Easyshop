# DirectoryView
from Products.CMFCore import DirectoryView

def initialize(context):
    """Initializer called when used as a Zope 2 product.
    """
    import easyshop.search.content
    
    # Register skin directory
    DirectoryView.registerDirectory('skins', globals())


