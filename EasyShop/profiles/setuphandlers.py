# CMFCore imports
from Products.CMFCore.utils import getToolByName

def installDependencies(portal):
    """
    """
    qit = getToolByName(portal, "portal_quickinstaller")

    products_to_install = ["ATBackRef",
                           "DataGridField",
                           
                           "easyshop.carts",
                           "easyshop.criteria",
                           "easyshop.taxes",
                           ]
                           
    ids = [ x['id'] for x in qit.listInstallableProducts(skipInstalled=1) ]
    for product in products_to_install:
        if product in ids:
            qit.installProduct(product)
    
def setupFormController(portal):
    """
    """
    portal_form_controller = getToolByName(portal, "portal_form_controller")
    portal_form_controller.addFormAction("validate_integrity",
                                         "success",
                                         "Customer",
                                         "checkout",
                                         "redirect_to",
                                         "python: '%s/easyshoporder_preview' % object.getShop().absolute_url()")
    
    for klass in ("Address", "DirectDebit"):    
        portal_form_controller.addFormAction("validate_integrity",
                                             "success",
                                             klass,
                                             "",
                                             "traverse_to",
                                             "string:easyshop_goto")

        portal_form_controller.addFormAction("base_edit",
                                             "success",
                                             klass,
                                             "cancel",
                                             "traverse_to",
                                             "string:easyshop_goto")

    portal_form_controller.addFormAction("validate_integrity",
                                         "success",
                                         "Address",
                                         "",
                                         "traverse_to",
                                         "string:easyshop_goto")


    portal_form_controller.addFormAction("validate_integrity",
                                         "success",
                                         "Customer",
                                         "",
                                         "redirect_to",
                                         "python: '%s?fieldset=%s' % (object.REQUEST.URL, object.REQUEST.form.get('fieldset'))")
                                         
def importVarious(context):
    """Import various settings.
    """
    portal = context.getSite()

    setupFormController(portal)
    installDependencies(portal)

