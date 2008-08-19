# python imports
import re

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
        old_path = self.request.get("old_path", "")
        new_path = self.request.get("new_path", "")
        
        if old_path != "" and new_path != "":
            storage = getUtility(IRedirectionStorage)
            storage.add(old_path, new_path)
            
        self._redirect()

    def cleanupRedirections(self):
        """
        """
        storage = getUtility(IRedirectionStorage)
        
        to_delete_paths = []
        for key, value in storage._paths.items():
            if key == value:
                to_delete_paths.append(key)

        for path in to_delete_paths:
            storage.remove(path)
            
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
        
        # selected paths                
        for path in paths:
            if path != "" and storage.has_path(path):
                storage.remove(path)

        regex = self.request.get("regex", "")
        if regex != "":
            # entered path
            to_delete_paths = []
            for path in storage._paths.keys():
                if re.search(regex, path):
                    to_delete_paths.append(path)

            for path in to_delete_paths:
                storage.remove(path)
            
        self._redirect()

    def _redirect(self):
        """
        """
        amount  = self.request.get('amount', "");
        b_start = self.request.get('b_start', "");
        
        if amount == "":
            amount = 0
            
        if b_start == "":
            b_start = 0
            
        url = self.context.absolute_url() + "/manage-redirections?b_start:int=" + str(b_start) + "&amount=" + amount
        self.request.response.redirect(url)