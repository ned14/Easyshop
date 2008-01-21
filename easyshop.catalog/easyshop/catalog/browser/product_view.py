# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import IProductVariantsManagement

class ProductView(BrowserView):
    """
    """ 
    def __call__(self):
        """
        """
        pvm = IProductVariantsManagement(self.context)
        if pvm.hasVariants() == True and \
           self.request.get("variant_selected", None) is not None:
        
            selected_variant = pvm.getSelectedVariant()
        
            if selected_variant is None:
                putils = getToolByName(self.context, "plone_utils")
                putils.addPortalMessage(MESSAGES["VARIANT_DONT_EXIST"])

        return super(ProductView, self).__call__()