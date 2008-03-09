# python imports
import cgi
import re

# kss imports
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction

# CMFPlone imports
from Products.CMFPlone.utils import safe_unicode

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop.kss imports
from snippets import *

# easyshop.core imports
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import ICurrencyManagement

class CatalogKSSView(PloneKSSView):
    """
    """
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
                object_provides = "easyshop.core.interfaces.catalog.IProduct",
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
            kss_core.replaceHTML("#search-products-form", safe_unicode(form))
            
        else:
            if letter == "All":
                products = catalog.searchResults(
                    path = "/".join(self.context.getPhysicalPath()),
                    object_provides = "easyshop.core.interfaces.catalog.IProduct",
                    sort_on = "sortable_title",
                )
                        
            elif letter == "0-9":
                brains = catalog.searchResults(
                    path = "/".join(self.context.getPhysicalPath()),
                    object_provides = "easyshop.core.interfaces.catalog.IProduct",
                    sort_on = "sortable_title",
                )
                    
                for brain in brains:
                    if re.match("\d", brain.Title):
                        products.append(brain)
            else:
                brains = catalog.searchResults(
                    path = "/".join(self.context.getPhysicalPath()),
                    object_provides = "easyshop.core.interfaces.catalog.IProduct",
                    Title = "%s*" % letter,
                    sort_on = "sortable_title",
                )
            
                for brain in brains:
                    if brain.Title.upper().startswith(letter):
                        products.append(brain)
        
        html = """<table class="products-list"><tr>"""
        
        for i, product in enumerate(products):
            html += "<td>"
            html += """<img class="product-details kssattr-uid-%s" alt="info" src="info_icon.gif" />""" % product.UID
            html += """<div><a href="%s">%s</a></div>""" % (product.getURL(), cgi.escape(product.Title))
            html += """</td><td class="image">"""
            html += """<img src="%s/image_tile" /> """  % product.getURL()
            html += """</td>"""
            if (i+1) % 3 == 0:
                html += "</tr><tr>"
        
        if len(products) == 0:
            html += "<td>%s</td>" % cgi.escape(MESSAGES["NO_PRODUCTS_FOUND"])
            
        html += "</tr></table>"

        html = safe_unicode(html)
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

        cm    = ICurrencyManagement(self.context)
        price = cm.priceToString(product.getPrice())

        info = {
            "title"       : product.Title(),
            "short_title" : product.getShortTitle(),
            "short_text"  : product.getText(),
            "url"         : product.absolute_url(),
            "article_id"  : product.getArticleId(),
            "price"       : price,
        }
        
        pd = PRODUCT_DETAILS % info

        # Related products
        related_products = product.getRelatedProducts()
        if len(related_products) > 0:
            pd += RELATED_PRODUCTS_HEADER
            for related_product in related_products:
                pd += RELATED_PRODUCTS_BODY % {
                    "title"      : cgi.escape(related_product.Title()),
                    "article_id" : related_product.getArticleId(),
                    "url"        : related_product.absolute_url()
                }            
            pd += RELATED_PRODUCTS_FOOTER
        
        # Categories
        categories = product.getCategories()
        if len(categories) > 0: 
            pd += CATEGORIES_HEADER
            for category in categories:
                pd += CATEGORIES_BODY % {
                    "title"      : cgi.escape(category.Title()),
                    "url"        : category.absolute_url()
                }            
            pd += CATEGORIES_FOOTER

        # Groups
        groups = product.getGroups()
        if len(groups) > 0: 
            pd += GROUPS_HEADER
            for group in groups:
                pd += GROUPS_BODY % {
                    "title"      : cgi.escape(group.Title()),
                    "url"        : group.absolute_url()
                }            
            pd += GROUPS_FOOTER
        
        kss_core  = self.getCommandSet("core")
        
        pd = safe_unicode(pd)
        kss_core.replaceInnerHTML('#product-details-box', pd)