from zope.interface import implements
from zope.component import adapts
from easyshop.core.interfaces import ICompleteness
from easyshop.mpay24.interfaces import ImPAY24PaymentMethod

class mPAY24PaymentMethodCompleteness:
    """
    """
    implements(ICompleteness)
    adapts(ImPAY24PaymentMethod)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def isComplete(self):
        """Returns true if the credit card informations are complete.
        """        
        return True