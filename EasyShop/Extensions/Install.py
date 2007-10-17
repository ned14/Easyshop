from Products.CMFCore.utils import getToolByName

def install(portal):
    """External Method to install EasyShop.
    """
    # install profiles    
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-Products.EasyShop:default')
    setup_tool.runAllImportSteps()