# zope imports
from zope.interface import Interface
from zope.interface import Attribute

class ICartItem(Interface):
    """A cart item holds a selected product and its amount an properties.
    """
    amount     = Attribute("The selected amount of the product")
    product    = Attribute("The selected product.")
    properties = Attribute("The selected attributes of the product")