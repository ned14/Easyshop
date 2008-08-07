# zope imports
from zope.interface import implements
from zope.component import adapts

# Archetypes imports
from Products.Archetypes.utils import shasattr

# easyshop imports
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import ICart

class CartItemManagement:
    """Adapter which provides IItemManagement for cart content objects.
    """
    implements(IItemManagement)
    adapts(ICart)

    def __init__(self, context):
        """
        """
        self.context = context           
        
    def addItem(self, product, properties, quantity=1):
        """Add given product to the cart. Returns True if the product was 
        already within the cart.
           
        Properties have to be a tuple of dicts with: 
                
                    {"column1" : name, "column2" : value}
        """
        product_is_already_in_cart = False        
        cart_items = self.getItems()
        for cart_item in cart_items:
            if (product == cart_item.getProduct()) and \
               (properties == cart_item.getProperties()):
                    product_is_already_in_cart = True
                    break

        if product_is_already_in_cart:
            cart_item.setAmount(cart_item.getAmount() + quantity)
            
            # to set modification date etc.    
            cart_item.reindexObject()
        else:
            new_id = len(cart_items)

            while shasattr(self.context, str(new_id)):
                new_id += 1

            new_id = str(new_id)

            self.context.manage_addProduct["easyshop.core"].addCartItem(id = new_id)
            cart_item = getattr(self.context, new_id)
            cart_item.setAmount(quantity)
            cart_item.setProperties(properties)
            cart_item.setProduct(product)

        return (product_is_already_in_cart, cart_item.getId())

    def addItemsFromCart(self, cart):
        """
        """
        for cart_item in IItemManagement(cart).getItems():
            self.addItem(cart_item.getProduct(), cart_item.getProperties(), cart_item.getAmount())

    def deleteItem(self, id):
        """
        """
        try:
            self.context._delObject(id)
        except AttributeError:
            return False

        return True

    def deleteItemByOrd(self, ord):
        """
        """
        try:
            toDeleteItem = self.context.objectValues()[ord]
        except IndexError:
            return False

        toDeleteId = toDeleteItem.getId()

        try:
            self.context._delObject(toDeleteId)
        except AttributeError:
            return False

        return True

    def getItem(self, id):
        """
        """        
        try:
            return self.context[id]
        except KeyError:
            return None
            
    def getItems(self):
        """
        """
        # If an item has no product (product has been deleted in the meanwhile, 
        # it isn't considered at all.
        items = []
        for item in self.context.objectValues("CartItem"):
            if item.getProduct() is not None:
                items.append(item)
        
        return items    

    def hasItems(self):
        """
        """    
        if len(self.getItems()) == 0:
            return False
        return True
        
