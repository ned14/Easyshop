# python imports
import re

# kss imports
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop.kss imports
from snippets import *

# easyshop.core imports
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IShopManagement

class CatalogKSSView(PloneKSSView):
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
    def showProducts(self, letter=None, form={}):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        kss_core  = self.getCommandSet("core")
                
        searchable_text = form.get("searchable_text", "")

        products = []        
        if searchable_text != "":
            products = catalog.searchResults(
                path = "/".join(self.context.getPhysicalPath()),
                portal_type = "Product",
                SearchableText = searchable_text,
                sort_on = "sortable_title",
            )

            # Workaround for browser message: "you have already sent this form"
            form = """
                <form id="search-products-form"
                      action="."
                      method="post"
                      style="display:inline">
                    <input type="text"
                           name="searchable_text"
                           value="%s" />
                    <input id="search-products"
                           type="submit"
                           value="OK" />
                </form>""" % searchable_text
            kss_core.replaceHTML("#search-products-form", form)
            
        else:
            if letter == "All":
                products = catalog.searchResults(
                    path = "/".join(self.context.getPhysicalPath()),
                    portal_type = "Product",
                    sort_on = "sortable_title",
                )
            
            
            elif letter == "0-9":
                brains = catalog.searchResults(
                    path = "/".join(self.context.getPhysicalPath()),
                    portal_type = "Product",
                    sort_on = "sortable_title",
                )
                    
                for brain in brains:
                    if re.match("\d", brain.Title):
                        products.append(brain)
            else:
                brains = catalog.searchResults(
                    path = "/".join(self.context.getPhysicalPath()),
                    portal_type = "Product",
                    Title = "%s*" % letter,
                    sort_on = "sortable_title",
                )
            
                for brain in brains:
                    if brain.Title.upper().startswith(letter):
                        products.append(brain)
        
        html = "<table><tr>"
        
        for i, product in enumerate(products):
            html += "<td>"            
            # html += """<a href="." class="product-details kssattr-uid-%s">[Details]</a> """ % product.UID            
            html += """<img class="product-details kssattr-uid-%s" alt="info" src="info_icon.gif" />""" % product.UID
            html += """<div><a href="%s">%s</a></div>""" % (product.getURL(), product.Title)
            html += """<img src="%s/image_tile" /> """  % product.getURL()
            html += """</td>"""
            if (i+1) % 5 == 0:
                html += "</tr><tr>"
                
        html += "</tr></table>"
        
        kss_core.replaceInnerHTML('#products', html)    
        kss_core.replaceInnerHTML('#product-details-box', "")
                        
    @kssaction    
    def showProductDetails(self, uid):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            UID = uid
        )
        
        try:
            product = brains[0].getObject()
        except IndexError:
            return

        info = {
            "title"       : product.Title(),
            "short_title" : product.getShortTitle(),
            "short_text"  : product.getShortText(),
            "url"         : product.absolute_url(),
            "article_id"  : product.getArticle_id(),
            "price"       : product.getPriceGross(),            
        }
        
        pd = PRODUCT_DETAILS % info

        # Related products
        related_products = product.getRelatedProducts()
        if len(related_products) > 0:
            pd += RELATED_PRODUCTS_HEADER
            for related_product in related_products:
                pd += RELATED_PRODUCTS_BODY % {
                    "title"      : related_product.Title(),
                    "article_id" : related_product.getArticle_id(),
                    "url"        : related_product.absolute_url()
                }            
            pd += RELATED_PRODUCTS_FOOTER
        
        # Categories
        categories = product.getEasyshopcategories()
        if len(categories) > 0: 
            pd += CATEGORIES_HEADER
            for category in categories:
                pd += CATEGORIES_BODY % {
                    "title"      : category.Title(),
                    "url"        : category.absolute_url()
                }            
            pd += CATEGORIES_FOOTER

        # Groups
        groups = product.getEasyshopgroups()
        if len(groups) > 0: 
            pd += GROUPS_HEADER
            for group in groups:
                pd += GROUPS_BODY % {
                    "title"      : group.Title(),
                    "url"        : group.absolute_url()
                }            
            pd += GROUPS_FOOTER
        
        kss_core  = self.getCommandSet("core")
        kss_core.replaceInnerHTML('#product-details-box', pd)