# CMFCore imports
from Products.CMFCore.utils import getToolByName

def installDependencies(portal):
    """
    """
    qit = getToolByName(portal, "portal_quickinstaller")

    products_to_install = ["ATBackRef",
                           "DataGridField"]
                           
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
                                         "EasyShopCustomer",
                                         "checkout",
                                         "redirect_to",
                                         "python: '%s/easyshoporder_preview' % object.getShop().absolute_url()")
    
    for klass in ("EasyShopAddress", "EasyShopDirectDebit"):    
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
                                         "EasyShopAddress",
                                         "",
                                         "traverse_to",
                                         "string:easyshop_goto")


    portal_form_controller.addFormAction("validate_integrity",
                                         "success",
                                         "EasyShopCustomer",
                                         "",
                                         "redirect_to",
                                         "python: '%s?fieldset=%s' % (object.REQUEST.URL, object.REQUEST.form.get('fieldset'))")
                                         
def installRelations(portal):
    """
    """
    from five.intid.site import FiveIntIdsInstall, addUtility, add_intids    
    add_intids(portal)
    
    from plone.app.relations.utils import add_relations
    add_relations(portal)
    
def importVarious(context):
    """Import various settings.
    """
    portal = context.getSite()

    setupFormController(portal)
    installDependencies(portal)
    installRelations(portal)
