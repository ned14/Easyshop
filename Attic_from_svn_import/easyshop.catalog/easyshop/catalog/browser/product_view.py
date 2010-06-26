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
        # Set last seen products
        title = self.context.Title()
        short_title = title[:10] + "..."

        url = self.context.absolute_url()
            
        last_products = self.request.SESSION.get("last_products", [])
        if len(last_products) > 5:
            last_products = last_products[0:-1]

        urls = [p["url"] for p in last_products]

        if self.context.absolute_url() not in urls:
            last_products.insert(
                0, {
                    "title" : title,
                    "short_title" : short_title,
                    "url" : url
                    }
            )

        self.request.SESSION.set("last_products", last_products)

        pvm = IProductVariantsManagement(self.context)
        if pvm.hasVariants() == True and \
           self.request.get("variant_selected", None) is not None:

            selected_variant = pvm.getSelectedVariant()

            if selected_variant is None:
                putils = getToolByName(self.context, "plone_utils")
                putils.addPortalMessage(MESSAGES["VARIANT_DONT_EXIST"])

        return super(ProductView, self).__call__()