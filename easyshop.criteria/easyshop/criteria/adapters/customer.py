# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import ICustomerCriteria

class CustomerCriteriaValidity:
    """Adapter which provides IValidity for customer criteria content objects.
    """    
    implements(IValidity)
    adapts(ICustomerCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Returns True if the current customer is in selected customers of the 
        criterion
        """
        # TODO: This could lead to problems if a manager adds products for a 
        # customer
        mtool = getToolByName(self.context, "portal_membership")
        current_customer = mtool.getAuthenticatedMember().getId()

        if current_customer in self.context.getCustomers():
            return True

        return False

