# zope imports
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewletManager

# Five imports
from Products.Five.browser import BrowserView

class PropertiesView(BrowserView):
    """
    """ 
    def selectProperties(self):
        """
        """
        # We just have to update the viewlet, everything else is made within the 
        # viewlet (e.g. calculate price by current selected properties, etc.)
        renderer = getMultiAdapter((self.context, self.request, self), IViewletManager, name="easyshop.product-manager")
        renderer = renderer.__of__(self.context)
        
        renderer.update()
        return renderer.render()        
