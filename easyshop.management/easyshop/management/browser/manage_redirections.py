# zope imports
from zope.component import getUtility

# Five imports
from Products.Five.browser import BrowserView

# redirector imports
from plone.app.redirector.interfaces import IRedirectionStorage

class ManageRedirectionsView(BrowserView):
    """
    """
    def getRedirections(self):
        """
        """
        storage = getUtility(IRedirectionStorage)
        
        result = []
        for old_path, new_path in storage._paths.items():
            result.append({
                "old_path" : old_path,
                "new_path" : new_path
            })
            
        return result
        
    def removePath(self):
        """
        """
        path = self.request.get("path", "")
        
        if path != "" and storage.hasPath(path):
            storage = getUtility(IRedirectionStorage)
            storage.remove(path)
        
        url = self.context.absolute_url() + "/manage-redirections"
        self.request.response.redirect(url)