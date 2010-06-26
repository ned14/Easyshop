# easyshop imports
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import ICategoriesContainer

class IMallProduct(IProduct):
    """A mall product is a replacement for the default product. It has 
    additional to the default product mall categories.
    """

class IMallCategory(ICategory):
    """A mall category exists additionally to the default category.
    """

class IMallCategoriesContainer(ICategoriesContainer):
    """Additionally to CategoriesContainer to hold MallCategories.
    """
    
