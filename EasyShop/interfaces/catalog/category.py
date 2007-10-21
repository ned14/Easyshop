from zope.interface import Interface
        
class ICategory(Interface):
    """Marker interface to mark category content objects. 

    A Category groups arbitrary Products together.
    
    Categories are visible to Customer and mainly used to structure 
    Products. A user of a shop may browse through Products via Categories.
       
    Categories may have sub-categories. 
       
    A product can have more than one category.

    categories may assigned special taxes, shipping prices, discounts and 
    similiar.
    """
    
class ICategoryManagement(Interface):
    """Provides methods to manage category content objects.
    """
    def hasCategories():
        """Returns True, if context has categories.
        """

    def hasParentCategory():
        """Returns True, if there are upper categories.
        """

    def getCategories():
        """Returns all direct subcategories of context.
        """

    def getTotalCategories():
        """Returns all subcategories of context.
        """

    def getTopLevelCategories(self):
        """Returns the top level categories of context.
        """
        
class ICategoriesContainer(Interface):
    """A marker interface for categories containers.
    """
    
