# zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop imports
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import IGroupCriteriaContent
from Products.EasyShop.interfaces import IGroupManagement
from Products.EasyShop.interfaces import IItemManagement
from Products.EasyShop.interfaces import IValidity

class GroupCriteriaValidity:
    """Adapter which provides IValidity for group criteria content
    objects.
    """    
    implements(IValidity)
    adapts(IGroupCriteriaContent)

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
            
            cm = ICartManagement(self.context.getShop())
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

