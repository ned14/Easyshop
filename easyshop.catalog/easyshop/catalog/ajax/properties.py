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
        renderer = getMultiAdapter((self.context, self.request, self), IViewletManager, name="easyshop.product-manager")
        renderer = renderer.__of__(self.context)
        
        renderer.update()
        return renderer.render()        
