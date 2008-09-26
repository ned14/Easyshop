from webdav.Lockable import ResourceLockedError
from OFS.CopySupport import CopyError
# Zope imports
from zLOG import LOG, INFO

# zope imports
from zope.component import getMultiAdapter
from zope.component import queryUtility

# plone imports
from plone.i18n.normalizer.interfaces import IURLNormalizer
from plone.i18n.normalizer.interfaces import IIDNormalizer

from Products.CMFPlone.utils import safe_unicode

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser import BrowserView

class CleanUpView(BrowserView):
    """
    """
    def cleanupIds(self):
        """
        """
        putils = getToolByName(self.context, "plone_utils")
        catalog = getToolByName(self.context, "portal_catalog")        
        
        for brain in catalog(portal_type="Product"):
            product = brain.getObject()
            new_id = product.generateNewId()
            
            if new_id != product.getId():
                try:
                    putils._renameObject(product, new_id)
                except ResourceLockedError:
                    view = getMultiAdapter((product, self.request), name="plone_lock_operations")
                    view.force_unlock()
                    putils._renameObject(product, new_id) 
                except CopyError:
                    LOG("Cleanup Ids:", INFO, "ID exists: %s / Try to rename product %s"  % (new_id, product.getId()))