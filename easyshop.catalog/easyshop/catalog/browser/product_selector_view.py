# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import ICurrencyManagement
from Products.EasyShop.interfaces import IFormatterInfos
from Products.EasyShop.interfaces import IPhotoManagement
from Products.EasyShop.interfaces import IPrices
from Products.EasyShop.interfaces import IPropertyManagement


class ProductSelectorView(BrowserView):
    """
    """
    def getFormatInfo(self):
        """
        """
        return IFormatterInfos(self.context).getFormatInfosAsDict()

    def getSelectors(self):
        """
        """
        fi = self.getFormatInfo()
        products_per_line = fi.get("products_per_line")
        
        mtool = getToolByName(self.context, "portal_membership")
            
        selectors = []
        # Todo: Optimize
        for selector in self.context.objectValues("ProductSelector"):

            # ignore thank you selection
            if selector.getId() == "thank-you":
                continue

            products_per_line = products_per_line

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
                "edit_url"         : "%s/base_edit" % selector.absolute_url(),
                "show_title"       : selector.getShowTitle(),
                "title"            : selector.Title(),
                "lines"            : lines,
                "products_per_line" : products_per_line,
                "td_width"         : "%s%%" % (100 / products_per_line),                
            })

        return selectors
        
    def showEditLink(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        if mtool.checkPermission("Manage portal", self.context):
            return True
        return False
        
