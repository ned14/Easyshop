# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from iqpp.easyshop.interfaces import ICategoryCriteria
from iqpp.easyshop.interfaces import ICategoryManagement
from iqpp.easyshop.interfaces import IValidity

class CategoryCriteriaValidity:
    """Adapter which provides IValidity for category criteria content objects.
    """
    implements(IValidity)
    adapts(ICategoryCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product):
        """Returns True if the given product has at least one of the selected 
        categories of the criterion.
        """
        cm = ICategoryManagement(product)
        product_categories = ["/".join(c.getPhysicalPath()) for c in cm.getTopLevelCategories()]
        criteria_categories = self.context.getCategories()

        for criteria_category in criteria_categories:
            if criteria_category in product_categories:
                return True
        return False