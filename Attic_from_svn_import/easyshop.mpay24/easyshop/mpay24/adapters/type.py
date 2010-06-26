from zope.interface import implements
from zope.component import adapts
from easyshop.core.interfaces import IType
from easyshop.mpay24.interfaces import ImPAY24PaymentMethod

class mPAY24PaymentType:
    """Provides IType for simple payment content objects.
    """
    implements(IType)
    adapts(ImPAY24PaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def getType(self):
        """Returns type.
        """
        return "mpay24-payment"
        