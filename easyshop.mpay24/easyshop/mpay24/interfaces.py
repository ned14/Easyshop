from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from easyshop.core.interfaces import IGenericPaymentMethod, \
    IAsynchronPaymentMethod

class ImPAY24PaymentMethod(IGenericPaymentMethod, IAsynchronPaymentMethod):
    """
    """

class ImPAY24ProductLayer(IDefaultBrowserLayer):
    """A layer specific for easyshop.mpay24
    We will use this to register browser pages that should only be used
    when easyshop.mpay24 is installed in the site.
    """