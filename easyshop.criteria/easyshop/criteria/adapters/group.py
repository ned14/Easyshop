# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IGroupCriteria
from easyshop.core.interfaces import IGroupManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IShopManagement

class GroupCriteriaValidity:
    """Adapter which provides IValidity for group criteria content
    objects.
    """    
    implements(IValidity)
    adapts(IGroupCriteria)

    def __init__(self, context):
        """
        """        
        self.context = context
        
    def isValid(self, product=None):
        """Returns true, if given products are at least in one of the selected 
           groups
        """
        # First, we collect all products which have to be checked.
        
        # If no product is given we are on cart level. That means take all
        # products of the cart.
        products = []
        if product is None:
            
            cm = ICartManagement(IShopManagement(self.context).getShop())
            cart = cm.getCart()
            
            im = IItemManagement(cart)
            
            for item in im.getItems():
                products.append(item.getProduct())
                
        # If a product is given (for calculation tax) we are on product level
        # and have to check only this one.
        else:
            products.append(product)

        # Now we go through all products.
        for product in products:
            # XXX Need this here, because the shipping product is a temporary product
            # and has no context and could not get reference_catalog.
            pm = IGroupManagement(product)                    
            try:
                product_groups = [g.getId() for g in pm.getGroups()]
            except AttributeError:
                product_groups = []    
            
            # Each product has to be at least in one of the selected groups of
            # the criterion
            found = False
            for product_group in product_groups:
                if product_group in self.context.getGroups():
                    found = True
                    continue

            if found == False:
                return False
                        
        return True

