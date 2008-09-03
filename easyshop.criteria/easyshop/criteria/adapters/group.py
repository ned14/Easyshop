# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from iqpp.easyshop.interfaces import ICartManagement
from iqpp.easyshop.interfaces import IGroupCriteria
from iqpp.easyshop.interfaces import IGroupManagement
from iqpp.easyshop.interfaces import IItemManagement
from iqpp.easyshop.interfaces import IValidity
from iqpp.easyshop.interfaces import IShopManagement

class GroupCriteriaValidity:
    """Adapter which provides IValidity for group criteria content objects.
    """    
    implements(IValidity)
    adapts(IGroupCriteria)

    def __init__(self, context):
        """
        """        
        self.context = context
        
    def isValid(self, product):
        """Returns True if given product is at least in one of the selected
        groups of the criterion.
        """
        pm = IGroupManagement(product)
        product_groups = [group.getId() for group in pm.getGroups()]
        criteria_groups = self.context.getGroups()

        for criteria_group in criteria_groups:
            if criteria_group in product_groups:
                return True
        return False
