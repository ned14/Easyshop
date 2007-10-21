# kss imports
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.config import MESSAGES
from Products.EasyShop.interfaces import IFormatterInfos
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import IItemManagement
from Products.EasyShop.interfaces import IShopManagement

class EasyShopKSSView(PloneKSSView):
    """
    """
    @kssaction    
    def addProduct(self, form):
        """
        """
        shop = IShopManagement(self.context).getShop()
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
        already_exist = IItemManagement(cart).addItem(
            self.context, 
            tuple(properties), 
            quantity)

        kss_core  = self.getCommandSet("core")
        kss_zope  = self.getCommandSet("zope")
        kss_plone = self.getCommandSet("plone")

        if already_exist == True:
            kss_plone.issuePortalMessage(MESSAGES["CART_INCREASED_AMOUNT"])
        else:
            kss_plone.issuePortalMessage(MESSAGES["CART_ADDED_PRODUCT"])
            
        # refresh cart
        selector = kss_core.getHtmlIdSelector("portlet-cart")
        kss_zope.refreshViewlet(selector,
                                manager="easyshop.cart-viewlet-manager",
                                name="easyshop.cart-viewlet")
                                
        # refresh product
        selector = kss_core.getHtmlIdSelector("myproduct")
        kss_zope.refreshViewlet(selector,
                                manager="easyshop.easyshop-manager",
                                name="easyshop.product")
        
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
                                manager="iqpp.easyshop.easyshop-manager",
                                name="iqpp.easyshop.categories")
         
        kss_plone.refreshPortlet(portlethash)