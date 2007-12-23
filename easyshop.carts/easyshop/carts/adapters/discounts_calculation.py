# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICart
from easyshop.core.interfaces import ICartItem
from easyshop.core.interfaces import IDiscountsCalculation
from easyshop.core.interfaces import IDiscountsManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import ITaxes

class CartDiscountsCalculation:
    """An adapter which provides IDiscountsCalculation for cart content objects.
    """
    implements(IDiscountsCalculation)
    adapts(ICart)

    def __init__(self, context):
        """
        """
        self.context = context
    
    def getDiscounts(self):
        """Returns calculated discounts.
        """
        return self.getDiscountsInformation()["discounts"]
        
    def getDiscount(self):
        """Returns total calculated discount.
        """
        return self.getDiscountsInformation()["total"]

    def getDiscountsInformation(self):
        """
        """
        result = []
        total_value = 0.0

        # NOTE: The "real" calculation of the discount takes place in 
        # CartItemDiscountsCalculation (see below).
        for cart_item in IItemManagement(self.context).getItems():
            discounts = IDiscountsCalculation(cart_item).getDiscountsInformation()
            total_value += discounts["total"]
            result.extend(discounts["discounts"])
            
        return {
            "total"     : total_value,
            "discounts" : result,
        }
        

class CartItemDiscountsCalculation:
    """An adapter which provides IDiscountsCalculation for cart item content
    objects.
    """
    implements(IDiscountsCalculation)
    adapts(ICartItem)

    def __init__(self, context):
        """
        """
        self.context = context
        self.taxes   = ITaxes(self.context.getProduct())
        self.shop    = IShopManagement(self.context).getShop()
        
    def getDiscounts(self):
        """Returns calculated discounts.
        """
        return self.getDiscountsInformation()["discounts"]
        
    def getDiscountForCustomer(self):
        """Returns total calculated discount.
        """
        import pdb; pdb.set_trace()
        tax_rate_for_customer = self.taxes.getTaxRateForCustomer()
        discount_net = self.getDiscountNet()
    
        return discount_net * ((tax_rate_for_customer+100)/100)

    def getDiscountGross(self):
        """Returns total calculated discount.
        """
        tax_rate = self.taxes.getTaxRate()
        
        discount = self.getDiscountsInformation()["total"]
        if self.shop.getGrossPrices() == True:
            return discount
        else:            
            return discount + (discount * (tax_rate/100))

    def getDiscountNet(self):
        """Returns total calculated discount.
        """
        tax_rate = self.taxes.getTaxRate()
        discount = self.getDiscountsInformation()["total"]
        
        if self.shop.getGrossPrices() == True:
            return discount - (tax_rate/(tax_rate+100)) * discount
        else:
            return discount            

    def getDiscountsInformation(self):
        """
        """
        discounts = []
        total_value = 0.0
        
        for discount in IDiscountsManagement(self.context).getDiscounts():
                
            if discount.getType() == "absolute":
                if discount.getBase() == "product":
                    value = self.context.getAmount() * discount.getValue()
                    total_value += value
                    discounts.append({
                        "value" : value,
                        "title" : discount.Title()
                    })
        
        return {
            "total"     : total_value,
            "discounts" : discounts,
        }
