# kss imports
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction

# CMFCore imports
from Products.CMFCore.utils import getToolByName

class CatalogKSSView(PloneKSSView):
    """
    """
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