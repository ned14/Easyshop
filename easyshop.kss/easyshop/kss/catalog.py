# python imports
import re

# kss imports
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction

# CMFCore imports
from Products.CMFCore.utils import getToolByName

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
            if letter == "0-9":
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
        
        html = ""
        for product in products:
            html += """<div>"""
            html += """<a href="." class="product-details kssattr-uid-%s">[Details]</a> """ % product.UID
            html += """<a href="%s">%s</a>""" % (product.getURL(), product.Title)
            html += """</div>"""
            
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

        pd  = "<h1>%s</h1>" % product.Title()
        pd += "<div>%s</div>" % product.getShortTitle()        
        pd += "<div>%s</div>" % product.getArticle_id()       
        pd += "<img src='%s/image_mini'/>" % product.absolute_url()
        pd += "<div>%s</div>" % product.getText()
        pd += "<div>%s</div>" % product.getShortText()
        pd += "<div>%s</div>" % product.getPriceGross()

        kss_core  = self.getCommandSet("core")
        kss_core.replaceInnerHTML('#product-details-box', pd)