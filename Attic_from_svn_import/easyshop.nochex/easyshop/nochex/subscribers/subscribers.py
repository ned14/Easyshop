# zope imports
from zope.component import adapter
from easyshop.shop.events import IShopCreatedEvent

# CMFCore imports
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException

# easyshop imports
from easyshop.core.interfaces import IShop

@adapter(IShop, IShopCreatedEvent)
def createContainers(shop, event):
    """
    """
    if getattr(shop, "paymentmethods", None) is None:
        shop.manage_addProduct["easyshop.shop"].addPaymentMethodsContainer(
            id="paymentmethods",
            title="Payment Methods")
    
    # Create
    shop.paymentmethods.manage_addProduct["easyshop.shop"].addNochexPaymentMethod(
        id="nochex", 
        title="Nochex")

    # Publish
    wftool = getToolByName(shop, "portal_workflow")
    try:
        wftool.doActionFor(shop.paymentmethods.nochex, "publish")
    except WorkflowException:    
        pass

    # Reindex
    shop.paymentmethods.nochex.reindexObject()
