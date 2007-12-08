# CMFCore imports
from Products.CMFCore.utils import getToolByName

def installDependencies(portal):
    """
    """
    qit = getToolByName(portal, "portal_quickinstaller")

    products_to_install = ["ATBackRef",
                           "DataGridField",                           
                           ]
                           
    ids = [ x['id'] for x in qit.listInstallableProducts(skipInstalled=1) ]
    for product in products_to_install:
        if product in ids:
            qit.installProduct(product)
    
def importVarious(context):
    """Import various settings.
    """
    portal = context.getSite()
    installDependencies(portal)

