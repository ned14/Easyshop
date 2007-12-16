# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICategoryCriteria
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IValidity

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
        categories = []
        cm = ICategoryManagement(product)

        for product_category in cm.getTopLevelCategories():
            object = product_category
            while IShop.providedBy(objects) == False:
                object = object.aq_inner.aq_parent
                if ICategory.providedBy()
        
        product_categories_ids = \
            [c.getId() for c in ]
        criteria_categories_ids = self.context.getCategories()

        import pdb; pdb.set_trace()
        for criteria_category in criteria_categories:
            if criteria_category in product_categories:
                return True
        return False
        
