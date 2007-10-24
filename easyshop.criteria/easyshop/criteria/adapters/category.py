# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICategoryCriteria
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IValidity

class CategoryCriteriaValidity:
    """Adapter which provides IValidity for category criteria content
    objects.
    """
    implements(IValidity)
    adapts(ICategoryCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Checks whether a product has a selected categories.
        """
        category_manager = ICategoryManagement(product)
        product_categories = [c.getId() for c in category_manager.getCategories()]
        criteria_categories = self.context.getCategories()

        for criteria_category in criteria_categories:
            if criteria_category in product_categories:
                return True
        return False