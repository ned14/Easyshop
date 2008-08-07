# Zope imports
from zope.interface import implements
from zope.component import adapts
from zope.component import getMultiAdapter

# easyshop imports
from easyshop.catalog.adapters.property_management import getTitlesByIds
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IDiscountsCalculation
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IOrder
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import ITaxes
from easyshop.core.interfaces import IShopManagement

class OrderItemManagement:
    """Provides IItemManagement for order content objects.
    """
    implements(IItemManagement)
    adapts(IOrder)

    def __init__(self, context):
        """
        """
        self.context = context

    def addItem(self, product, amount=1):
        """Adds a item
        """
        raise Exception

    def addItemsFromCart(self, cart):
        """Adds all items from a given cart to the order
        """
        shop = IShopManagement(self.context).getShop()        

        if cart is None:
            cartmanager = ICartManagement(shop)
            cart = cartmanager.getCart()

        # edit cart items
        id = 0
        for cart_item in IItemManagement(cart).getItems():
            id += 1
            self._addItemFromCartItem(id, cart_item)

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
        return self.context.objectValues("OrderItem")
        
    def hasItems(self):
        """
        """    
        if len(self.getItems()) == 0:
            return False
        return True
        
    def _addItemFromCartItem(self, id, cart_item):
        """Sets the item by given cart item.
        """        
        self.context.manage_addProduct["easyshop.core"].addOrderItem(id=str(id))
        new_item = getattr(self.context, str(id))

        # set product quantity        
        new_item.setProductQuantity(cart_item.getAmount())
                
        # Set product prices & taxes
        product_taxes  = ITaxes(cart_item.getProduct())
        product_prices = IPrices(cart_item.getProduct())
        item_prices = IPrices(cart_item)
        item_taxes  = ITaxes(cart_item)
        
        new_item.setTaxRate(product_taxes.getTaxRateForCustomer())
        new_item.setProductTax(product_taxes.getTaxForCustomer())
        
        new_item.setProductPriceGross(product_prices.getPriceForCustomer())
        new_item.setProductPriceNet(product_prices.getPriceNet())

        # Set item prices & taxes
        new_item.setTax(item_taxes.getTaxForCustomer())
        new_item.setPriceGross(item_prices.getPriceForCustomer())
        new_item.setPriceNet(item_prices.getPriceNet())

        # Discount
        discount = IDiscountsCalculation(cart_item).getDiscount()
        if discount is not None:
            new_item.setDiscountDescription(discount.Title())

            dp = getMultiAdapter((discount, cart_item))
            new_item.setDiscountGross(dp.getPriceForCustomer())
            new_item.setDiscountNet(dp.getPriceNet())
        
        # Set product
        product = cart_item.getProduct()
        new_item.setProduct(product)

        # Set product name and id
        data = IData(product).asDict()
        new_item.setProductTitle(data["title"])
        new_item.setArticleId(data["article_id"])

        # Set properties
        properties = []
        pm = IPropertyManagement(product)
        for selected_property in cart_item.getProperties():

            # Get the price
            property_price = pm.getPriceForCustomer(
                selected_property["id"], 
                selected_property["selected_option"])

            # By default we save the titles of the properties and selected 
            # options In this way they are kept if the title of a property or 
            # option will be changed after the product has been bought.
            titles = getTitlesByIds(
                product,
                selected_property["id"], 
                selected_property["selected_option"])

            # If we don't find the property or option we ignore the property. 
            # This can only happen if the property has been deleted after a 
            # product has been added to the cart. In this case we don't want the 
            # property at all (I think).
            if titles is None:
                continue
                                    
            properties.append({
                "title" : titles["property"],
                "selected_option" : titles["option"],
                "price" : str(property_price),
            })
                            
        new_item.setProperties(properties)
