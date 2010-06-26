# zope imports
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewletManager

# Five imports
from Products.Five.browser import BrowserView

class AccessoriesView(BrowserView):
    """
    """ 
    def moveDown(self):
        """
        """
        uid = self.request.form.get("item")
        accessories = list(self.context.getAccessories())
        
        found = False
        i=0
        for accessory in accessories:
           if accessory.startswith(uid):
               found = True
               break
           i+=1
        
        if found:
            try:
                temp = accessories[i+1]
                accessories[i+1] = accessories[i]
                accessories[i] = temp
            except IndexError:
                pass
        
        self.context.setAccessories(accessories)        
        return self.refreshViewletManager()
        
    def moveUp(self):
        """
        """
        uid = self.request.form.get("item")
        accessories = list(self.context.getAccessories())
        
        found = False
        i=0
        for accessory in accessories:
           if accessory.startswith(uid):
               found = True
               break
           i+=1
        
        if found:
            try:
                temp = accessories[i]
                accessories[i] = accessories[i-1]
                accessories[i-1] = temp
            except IndexError:
                pass
        
        self.context.setAccessories(accessories)
        return self.refreshViewletManager()
        
    def refreshViewletManager(self):
        renderer = getMultiAdapter((self.context, self.request, self), IViewletManager, name="easyshop.manage-accessories-manager")
        renderer = renderer.__of__(self.context)
        
        renderer.update()
        return renderer.render()
        