# kss imports
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import force_unicode, kssaction

# CMFPlone imports
from Products.CMFPlone.utils import safe_unicode

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# kss imports
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import force_unicode, kssaction

# EasyShop imports
from Products.EasyShop.interfaces import IFormatterInfos
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import IItemManagement

class EasyShopKSSView(PloneKSSView):
    """
    """
    @kssaction
    def addProduct(self, form):
        """
        """
        shop = self.context.getShop()
        cm = ICartManagement(shop)
        
        cart = cm.getCart()
        if cart is None:
            cart = cm.createCart()
                
        properties = []
        
        # for property_id, selected_option in self.request.form.items():
        #     if property_id.startswith("property") == False:
        #         continue
        #         
        #     if selected_option == "please_select":
        #         continue
        #             
        #     properties.append(
        #         {"id" : property_id[9:], 
        #          "selected_option" : selected_option 
        #         }
        #     )

        # get quantity
        quantity = int(form.get("quantity", 1))

        # returns true if the product was already within the cart
        result = IItemManagement(cart).addItem(self.context, tuple(properties), quantity)

        kss_plone = self.getCommandSet("plone")
        kss_core = self.getCommandSet("core")
        kss_zope = self.getCommandSet("zope")
            
        kss_plone.refreshPortlet("706c6f6e652e7269676874636f6c756d6e0a636f6e746578740a2f706f7274616c2f73686f700a41737369676e6d656e74")

        self.getCommandSet('plone').issuePortalMessage("Added product to card.")
    
        selector = kss_core.getHtmlIdSelector("products-view")
        kss_zope.refreshViewlet(selector,
                                manager="iqpp.easyshop.main",
                                name="iqpp.easyshop.product")

    @kssaction
    def saveFormatter(self, form, portlethash):
        """
        """
        fi = IFormatterInfos(self.context)
        f = fi.getFormatter()
        
        products_per_line = form.get("products_per_line", 0)
        lines_per_page    = form.get("lines_per_page", 0)
        image_size        = form.get("image_size", "mini")
        text              = form.get("text", "")
        product_height    = form.get("product_height", 0)
        
        products_per_line = int(products_per_line)
        lines_per_page    = int(lines_per_page)
        product_height    = int(product_height)
                
        f.setProductsPerLine(products_per_line)
        f.setLinesPerPage(lines_per_page)
        f.setImageSize(image_size)
        f.setProductHeight(product_height)        
        f.setText(text)
        
        kss_core  = self.getCommandSet("core")
        kss_zope  = self.getCommandSet("zope")
        kss_plone = self.getCommandSet("plone")

        selector = kss_core.getHtmlIdSelector("mycategories")
        kss_zope.refreshViewlet(selector,
                                manager="iqpp.easyshop.products-manager",
                                name="iqpp.easyshop.products")
         
        kss_plone.refreshPortlet(portlethash)