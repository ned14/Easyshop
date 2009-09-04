from zope.interface import Interface
from easyshop.core.interfaces import IGenericPaymentMethod, IAsynchronPaymentMethod

class ImPAY24PaymentMethod(IGenericPaymentMethod, IAsynchronPaymentMethod):
    """
    """
    
class ImPAY24ProductLayer(Interface):
    """A layer specific for easyshop.mpay24
    We will use this to register browser pages that should only be used
    when easyshop.mpay24 is installed in the site.
    """