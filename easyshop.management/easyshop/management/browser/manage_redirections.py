# zope imports
from zope.component import getUtility

# CMFPlone imports
from Products.CMFPlone import Batch

# Five imports
from Products.Five.browser import BrowserView

# redirector imports
from plone.app.redirector.interfaces import IRedirectionStorage

class ManageRedirectionsView(BrowserView):
    """
    """
    def getRedirections(self):
        """Returns all stored redirections.
        """
        storage = getUtility(IRedirectionStorage)

        result = []
        for old_path, new_path in storage._paths.items():
            result.append({
                "old_path" : old_path,
                "new_path" : new_path
            })

        # Get start page
        b_start = self.request.get('b_start', 0);
        amount = self.request.get("amount", 20)
            
        # Calculate Batch
        return Batch(result, int(amount), int(b_start), orphan=0);

    def addRedirection(self):
        """
        """
        import pdb; pdb.set_trace()
        old_path = self.request.get("old_path", "")
        new_path = self.request.get("new_path", "")
        
        if old_path != "" and new_path != "":
            storage = getUtility(IRedirectionStorage)
            storage.add(old_path, new_path)
            
        self._redirect()
        
    def removeRedirection(self):
        """Removes given path
        """
        path = self.request.get("path", "")

        if path != "" and storage.has_path(path):
            storage = getUtility(IRedirectionStorage)
            storage.remove(path)
        
        self._redirect()
        
    def removeRedirections(self):
        """
        """
        paths = self.request.get("paths", [])
        if not isinstance(paths, (list, tuple)):
            paths = (paths,)

        storage = getUtility(IRedirectionStorage)
                        
        for path in paths:
            if path != "" and storage.has_path(path):
                storage.remove(path)
        
        self._redirect()

    def _redirect(self):
        """
        """
        b_start  = self.request.get('b_start', 0);
            
        url = self.context.absolute_url() + "/manage-redirections?b_start:int=" + str(b_start)
        self.request.response.redirect(url)