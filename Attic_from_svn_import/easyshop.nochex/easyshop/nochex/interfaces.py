from easyshop.core.interfaces import IAsynchronPaymentMethod
from easyshop.core.interfaces import IPaymentMethod
from easyshop.core.interfaces import ISelectablePaymentMethod

class INochexPaymentMethod(IPaymentMethod, ISelectablePaymentMethod, IAsynchronPaymentMethod):
    """Marker interface for payment via Nochex (http://www.nochex.com).
    """