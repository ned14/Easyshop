# CMFCore imports
from Products.CMFCore.utils import getToolByName

# TODO: Move this to a local utility
def getObjectByUID(context, uid):
    """
    """
    catalog = getToolByName(context, "portal_catalog")
    brains = catalog.searchResults(
        uid = uid
    )
    
    try:
        return brains[0]
    except IndexError:
        return None