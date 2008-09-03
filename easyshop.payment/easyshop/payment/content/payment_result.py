# zope imports
from zope.interface import implements

# iqpp.easyshop
from iqpp.easyshop.interfaces import IPaymentResult

class PaymentResult(object):
    """A payment result is returned by all payment processors.
    """
    implements(IPaymentResult)
    
    def __init__(self, code, message=u""):
        """
        """
        self.code = code
        self.message = message