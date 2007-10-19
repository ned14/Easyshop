# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import IValidity
from Products.EasyShop.interfaces import ICustomerCriteria

class CustomerCriteriaValidity:
    """Adapter which provides IValidity for customer criteria content
    objects.
    """    
    implements(IValidity)
    adapts(ICustomerCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Returns true, if the current customer is in selected customers.
        """
        # Todo: this could be lead to problems if a manager adds products for
        # a customer
        mtool = getToolByName(self.context, "portal_membership")
        current_customer = mtool.getAuthenticatedMember().getId()

        if current_customer in self.context.getCustomers():
            return True

        return False

