# zope imports
from zope.interface import Interface

class IGroupContent(Interface):
    """Marker interface to mark group content objects.
    
    A group groups arbitrary Products together.
    
    Groups may then assigned special taxes, shipping prices, discounts
    and similiar.
       
    As a specialty groups may be assigned properties. All products, which 
    are within a group inherit properties of this group.
       
    Groups are contrary to categories not visible to customers.
    """
    
class IGroupManagement(Interface):
    """Provides methods to manage groups content objects.
    """

    def hasGroups():
        """Returns True, if there is at least on Group.
        """
    def getGroups():
        """Returns all Groups
        """