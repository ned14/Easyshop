# zope imports
from zope.interface import implements
  
# easyshop imports
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IValidity

class Validity(object):
    """An adapter which provides IValidity for several classes. See 
    configure.zcml for more information.
    """
    implements(IValidity)
     
    def __init__(self, context):
        """
        """
        self.context = context

    def isValid(self, product=None):
        """Returns true if all contained criteria are true.
        """
        # To be true all criteria must be true (AND)
        for criteria in self.context.objectValues():
            # First try "isValid" on the criterion. This maybe makes it easier
            # to write own 3rd party criteria without the need to write an 
            # adapter.
            try:
                if criteria.isValid(product) == False:
                    return False
            except AttributeError:
                # Then take the adapter. This makes it OTOH easier to overwrite the 
                # default behaviour of the default criterias
                if IValidity(criteria).isValid(product) == False:
                    return False
                                            
        return True


class PayPalValidity(Validity):
    """An adapter which provides IValidity for PayPal payment method.
    """
    implements(IValidity)
     
    def __init__(self, context):
        """
        """
        self.context = context

    def isValid(self, product=None):
        """Returns False if the PayPal id is not filled in.
        """
        shop = IShopManagement(self.context).getShop()
        if shop.getPayPalId() == "":
            return False

        return super(PayPalValidity, self).isValid(product)