# plone imports
from plone.app.layout.viewlets.common import ViewletBase

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# plone imports
from plone.memoize.instance import memoize

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IFormats
from easyshop.core.interfaces import IPhotoManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IPropertyManagement

class ProductSelectorViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('product_selector.pt')

    def getFormatInfo(self):
        """
        """
        return IFormats(self.context).getFormats()

    def getImages(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = {"query" : "/".join(self.context.getPhysicalPath()),
                    "depth" : 1},
            portal_type = "ESImage",
            sort_on = "getObjPositionInParent",
        )
        
        return brains
                
    def getSelectors(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        catalog = getToolByName(self.context, "portal_catalog")
                    
        selectors = []
        brains = catalog.searchResults(
            path = "/".join(self.context.getPhysicalPath()),
            portal_type = "ProductSelector",
            sort_on = "getObjPositionInParent",
        )
        
        for selector in brains:

            # ignore thank you selection
            if selector.getId == "thank-you":
                continue

            selector = selector.getObject()
            
            fi = IFormats(selector).getFormats()
            products_per_line = fi.get("products_per_line")

            lines = []            
            products = []
            for index, product in enumerate(selector.getRefs()):

                if mtool.checkPermission("View", product) is None:
                    continue

                cm    = ICurrencyManagement(self.context)
                price = IPrices(product).getPriceForCustomer()
                price = cm.priceToString(price)
                
                # photo
                photo = IPhotoManagement(product).getMainPhoto()
                if photo is not None:
                    image = "%s/image_%s" % (photo.absolute_url(), fi.get("image_size"))

                # properties view
                property_manager = IPropertyManagement(product)
                if len(property_manager.getProperties()) > 0:
                    showSelectPropertiesView = True
                else:    
                    showSelectPropertiesView = False

                t = fi.get("text")
                if t == "description":
                    text = product.getDescription()
                elif t == "short_text":
                    text = product.getShortText()
                elif t == "text":
                    text = product.getText()
                else:
                    text = ""
                
                if (index + 1) % products_per_line == 0 and products_per_line > 1:
                    klass = "last"
                else:
                    klass = "notlast"
                                        
                products.append({
                    "title"                    : product.Title(),
                    "short_title"              : product.getShortTitle() or product.Title(),                    
                    "url"                      : product.absolute_url(),
                    "price"                    : price,
                    "image"                    : image,
                    "text"                     : text,
                    "showSelectPropertiesView" : showSelectPropertiesView,
                    "class"                    : klass,
                })
    
                if (index+1) % products_per_line == 0:
                    lines.append(products)
                    products = []

            # the rest
            lines.append(products)

            selectors.append({
                "edit_url"          : "%s/base_edit" % selector.absolute_url(),
                "show_title"        : selector.getShowTitle(),
                "title"             : selector.Title(),
                "lines"             : lines,
                "products_per_line" : products_per_line,
                "product_height"    : fi.get("product_height"),
                "td_width"          : "%s%%" % (100 / products_per_line),
            })

        return selectors

    @memoize
    def showEditLink(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        if mtool.checkPermission("Manage portal", self.context):
            return True
        return False