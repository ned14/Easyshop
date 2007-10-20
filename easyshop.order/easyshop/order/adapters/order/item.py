# Zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop imports
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import IItemManagement
from Products.EasyShop.interfaces import IOrder
from Products.EasyShop.interfaces import IPrices
from Products.EasyShop.interfaces import IPropertyManagement
from Products.EasyShop.interfaces import ITaxes

class OrderItemManager:
    """Provides IItemManagement for order content objects.
    """
    implements(IItemManagement)
    adapts(IOrder)

    def __init__(self, context):
        self.context = context

    def addItem(self, product, amount=1):
        """Adds a item
        """
        raise Exception

    def deleteItemByOrd(self, ord):
        """Deletes the item by passed ord
        """
        raise Exception
        
    def deleteItem(self, id):
        """deletes the Item by passed id
        """
        raise Exception
        
    def getItems(self):
        """Returns all items of an order
        """
        # XXX: Optimize
        return self.context.objectValues("OrderItem")

    def addItemsFromCart(self, cart):
        """Adds all items from a given cart to the order
        """
        shop = self.context.getShop()        

        if cart is None:
            cartmanager = ICartManagement(shop)
            cart = cartmanager.getCart()

        # edit cart items
        id = 0
        for cart_item in IItemManagement(cart).getItems():
            id += 1
            self.addItemFromCartItem(str(id), cart_item)


    def addItemFromCartItem(self, id, cart_item):
        """Sets the item by given CartItem

        """
        shop = self.context.getShop()                
        taxes = ITaxes(shop)
                
        self.context.manage_addProduct["EasyShop"].addOrderItem(id=id)
        new_item = getattr(self.context, id)
        
        # Todo: use the adapters here
        # set product prices & taxes
        new_item.setProductQuantity(cart_item.getAmount())
        new_item.setTaxRate(taxes.getTaxRate(cart_item.getProduct()))
        new_item.setProductTax(taxes.getTax(cart_item.getProduct()))
        new_item.setProductPriceGross(cart_item.getProduct().getPriceGross())
        new_item.setProductPriceNet(new_item.getProductPriceGross() - new_item.getProductTax())

        # set item prices & taxes
        new_item.setTax(ITaxes(cart_item).getTaxForCustomer())
        new_item.setPriceGross(IPrices(cart_item).getPriceForCustomer())        
        new_item.setPriceNet(IPrices(cart_item).getPriceNet())
        
        # set product
        new_item.setProduct(cart_item.getProduct())

        # set properties
        properties = []
        pm = IPropertyManagement(cart_item.getProduct())
        for selected_property in cart_item.getProperties():

            property_price = pm.getPriceForCustomer(
                selected_property["id"], 
                selected_property["selected_option"])

            # This could happen if a property is deleted and there are 
            # still product with this selected property in the cart.
            # Todo: Think about, whether theses properties are not to 
            # display. See also checkout_order_preview
            try:    
                property_title = pm.getProperty(
                    selected_property["id"]).Title()
            except AttributeError:
                property_title = selected_property["id"]
                
            properties.append({
                "title" : property_title,            
                "selected_option" : selected_property["selected_option"],
                "price" : str(property_price)
            })
                            
        new_item.setProperties(properties)