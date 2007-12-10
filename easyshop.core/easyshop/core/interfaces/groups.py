# zope imports
from zope.interface import Interface
from zope.interface import Attribute

class IProductGroup(Interface):
    """A group combines arbitrary products.
    o Groups may then assigned special taxes, shipping prices, discounts and 
      similiar.
    o As a specialty groups may have assigned properties. All products, which 
      are within a group inherit properties of this group.
    o Groups are in contrary to categories not visible to customers.
    """    

    products = Attribute("Products which belongs to this group.")
    
    
class IGroupManagement(Interface):
    """Provides methods to manage groups.
    """
    def addGroup(group):
        """Adds given group.
        """

    def deleteGroup(id):
        """Deletes group with given id.
        """
        
    def getGroup(group_id):
        """Returns a group by given id.
        """
        
    def getGroups():
        """Returns all Groups
        """

    def hasGroups():
        """Returns True, if there is at least on Group.
        """
                        
class IGroupsContainer(Interface):
    """A container to hold groups.
    """      