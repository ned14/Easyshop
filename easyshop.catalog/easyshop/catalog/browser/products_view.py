# Python imports
import re

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser import BrowserView

class ProductsView(BrowserView):
    """
    """
    def getLetters(self):
        """
        """
        return  ("All", "0-9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", 
                 "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W",
                 "X", "Y", "Z")

    def getProduct(self):
        """
        """
        uid = self.request.get("uid", "")
        if uid == "":
            return None

        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            UID = uid
        )
        
        try:
            brain = brains[0]
        except IndexError:
            return None
        
        product = brain.getObject()

        return {
            "id"          : product.getId(),
            "article_id"  : product.getArticle_id(),
            "description" : product.Description(),
            "title"       : product.Title(),
            "short_title" : product.getShortTitle(),
            "url"         : product.absolute_url(),
            "text"        : product.getText(),
            "short_text"  : product.getShortText(),
            "price"       : product.getPriceGross(),
        }
        
    def getProducts(self):
        """Returns products as a list of brains.
        """
        catalog = getToolByName(self.context, "portal_catalog")
                
        searchable_text = self.request.get("searchable_text", "")
        if searchable_text != "":
            brains = catalog.searchResults(
                path = "/".join(self.context.getPhysicalPath()),
                portal_type = "Product",
                SearchableText = searchable_text,
                sort_on = "sortable_title",
            )
        
            return brains
        
        letter = self.request.get("letter", "")
        if letter == "":
            return []
        
        result = []
        if letter == "All":
            result = catalog.searchResults(
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
                    result.append(brain)
        else:
            brains = catalog.searchResults(
                path = "/".join(self.context.getPhysicalPath()),
                portal_type = "Product",
                Title = "%s*" % letter,
                sort_on = "sortable_title",
            )
            
            for brain in brains:
                if brain.Title.upper().startswith(letter):
                    result.append(brain)
        
        lines = []
        line = []
        for i, product in enumerate(result):
            line.append(product)
            if (i+1) % 8 == 0:
                lines.append(line)
                line = []
        
        if len(line) > 0:
            lines.append(line)        

        return lines