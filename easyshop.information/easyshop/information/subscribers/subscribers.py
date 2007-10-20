# zope imports
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent

# EasyShop imports
from Products.EasyShop.interfaces import IShop

@adapter(IShop, IObjectInitializedEvent)
def createInformation(shop, event):
    """
    """
    shop.manage_addProduct["EasyShop"].addInformationContainer(
        id="information", 
        title="Information")
        
    shop.information.manage_addProduct["EasyShop"].addInformationPage(
        id="terms-and-conditions",
        title="Terms And Conditions")
        
    shop.information.reindexObject()
