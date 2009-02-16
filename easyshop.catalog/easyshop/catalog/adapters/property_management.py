# Zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IGroupManagement
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IProductVariant
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import ITaxes


class ProductPropertyManagement(object):
    """Provides IPropertyManagement for product content objects.
    """
    implements(IPropertyManagement)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def getOptionsForProperty(self, property_id):
        """
        """
        property = self.getProperty(property_id)
        return property.getOptions()
        
    def getPriceForCustomer(self, property_id, option_id):
        """
        """
        # Get the tax rate for the product to which the property belongs.
        # Note: That means, the tax rate for the product's properties is the
        # same as for the product.
        tax_rate_for_customer = ITaxes(self.context).getTaxRateForCustomer()
        
        price_net = self.getPriceNet(property_id, option_id)
        price_for_customer =  price_net * ((tax_rate_for_customer + 100) / 100)

        return price_for_customer
        
    def getPriceGross(self, property_id, option_id):
        """
        """
        shop     = IShopManagement(self.context).getShop()
        tax_rate = ITaxes(self.context).getTaxRate()
        price    = self._calcPrice(property_id, option_id)

        # The price entered is considered as gross price, so we simply
        # return it.
        if shop.getGrossPrices() == True:
            return price

        # The price entered is considered as net price. So we have to calculate 
        # the gross price first.
        else:
            return price * ((tax_rate + 100) / 100)
        
    def getPriceNet(self, property_id, option_id):
        """
        """
        # Get the tax rate for the product to which the property belongs.
        # Note: That means, the tax rate for the product's properties is the
        # same as for the product.
        shop     = IShopManagement(self.context).getShop()
        tax_rate = ITaxes(self.context).getTaxRate()
        price    = self._calcPrice(property_id, option_id)


        # The price entered is considered as gross price. So we have to 
        # calculate the net price first.
        
        if shop.getGrossPrices() == True:
            return price * (100 / (tax_rate + 100))
            
        # The price entered is considered as net price, so we simply
        # return it.            
        else:
            return price

    def getProperties(self):
        """Returns all unique Properties for a Product, wheras properties from 
        the Product have higher precedence than Properties from a Group.
        """
        # NOTE: We can't use dictionaries here to unify properties, because we 
        # need the properties in the order of positions within the product.
        
        property_ids = []
        properties = []
        
        # Get all Properties from Groups        
        for group in IGroupManagement(self.context).getGroups():
            for property in group.objectValues("ProductProperty"):
                property_ids.append(property.getId())
                properties.append(property)
        
        # Overwrite with Properties from Product
        for property in self.context.objectValues("ProductProperty"):
            if property.getId() in property_ids:
                index = property_ids.index(property.getId())
                properties[index] = property
            else:
                properties.append(property)
            
        return properties
                        
    def getProperty(self, id):
        """
        """
        return self._getPropertiesAsDict().get(id)

    def getTitlesByIds(self, property_id, option_id):
        """
        """
        # Get all properties as dict
        result = self._getPropertiesAsDict()
        
        if result.has_key(property_id) == False:
            return {
                "property" : property_id, 
                "option" : option_id,
            }

        property = result[property_id]
        for option in property.getOptions():
            if option["id"] == option_id:
                return {
                    "property" : property.Title(), 
                    "option" : option["name"],
                }
        
        return None

    def _getPropertiesAsDict(self):
        """Returns all unique Properties for a Product, wheras properties from 
        the Product have higher precedence than Properties from a Group.
        """
        groups = IGroupManagement(self.context).getGroups()

        # Get all Properties from Groups
        result = {}
        for group in groups:
            for property in group.objectValues("ProductProperty"):
                result[property.getId()] = property
        
        # Overwrite with Properties from Product
        for property in self.context.objectValues("ProductProperty"):
            result[property.getId()] = property
        
        return result

    def _calcPrice(self, property_id, option_id):
        """
        """
        found = False
        for property in self.getProperties():
            if property.getId() == property_id:
                found = True
                break

        if found == False:
            return 0.0
                    
        found = False
        for option in property.getOptions():
            if option["id"] == option_id:
                found = True
                break
                
        if found == False:
            return 0.0
                    
        try:
            price = float(option["price"])
        except ValueError:
            price = 0.0

        return price


def getTitlesByIds(product, property_id, option_id):
    # TODO: This may not be the cleanest way. Rethink it. YAGNI?
    """A simple wrapper to get the variants options (global options) of a 
    variant. In this way the adapter still works for local properties (price 
    changing) of a variant, which may later used additional to the global ones.
    """
    
    if IProductVariant.providedBy(product) == True:
        product = product.aq_inner.aq_parent

    pm = IPropertyManagement(product)
    return pm.getTitlesByIds(property_id, option_id)
    
def getOptionsForProperty(product, property_id):
    """Returns all options for a given property id.
    """
    if IProductVariant.providedBy(product) == True:
        product = product.aq_inner.aq_parent

    pm = IPropertyManagement(product)
    return pm.getOptionsForProperty(property_id)