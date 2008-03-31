# zope imports
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.config import _
from easyshop.core.config import TEXTS, TITLES, IMAGE_SIZES
from easyshop.core.interfaces import IFormats
from easyshop.core.interfaces import IFormatable
from easyshop.core.interfaces import IProductSelector
from easyshop.core.interfaces import IShop

class IFormatterPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    """
    """
    implements(IFormatterPortlet)

    def __init__(self):
        """
        """

    @property
    def title(self):
        """
        """
        return _(u"EasyShop: Formatter")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('formatter.pt')

    @property
    def available(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        if not mtool.checkPermission("Manage portal", self.context):
            return False
             
        if IFormatable.providedBy(self.context) == False:
            return False

        return True        

    @memoize
    def getFormatInfo(self):
        """
        """
        fi = IFormats(self.context)
        return fi.getFormats(effective=False)

    def getTitles(self):
        """
        """
        fi = self.getFormatInfo()
        selected_title = fi["title"]
        
        result = []
        for title in TITLES:        
            result.append({
                "id" : title[0],
                "title" : title[1],
                "selected" : selected_title == title[0],
            })
    
        return result

    def getTexts(self):
        """
        """
        fi = self.getFormatInfo()
        selected_text = fi["text"]
        
        result = []
        for text in TEXTS:        
            result.append({
                "id" : text[0],
                "title" : text[1],
                "selected" : selected_text == text[0],
            })
    
        return result
        
    def getImageSizes(self):
        """
        """
        fi = self.getFormatInfo()
        selected_size = fi["image_size"]
        
        sizes = IMAGE_SIZES.keys()
        sizes.sort(lambda a, b: cmp(IMAGE_SIZES[a][0], IMAGE_SIZES[b][0]))

        result = []
        for size in sizes:
            result.append({
                "title" : size,
                "selected" : selected_size == size,
            })
            
        return result

    @memoize
    def showEnabledField(self):
        """Returns True when the enabled field should be displayed.
        """
        if IShop.providedBy(self.context) == True:
            return False
        else:
            return True

    @memoize  
    def showLinesPerPage(self):
        """Returns True when the lines per page field should be displayed.
        """
        # If "product-selector-view" is selected, we decide thru the amount of 
        # selected products and product per lines how much products per page 
        # are supposed to be displayed, hence we hide the input field.
        if IProductSelector.providedBy(self.context) == True:
            return False
                        
        else:
            return True
            
class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()

class FormatterView(BrowserView):
    """
    """
    def saveFormatter(self):
        """
        """
        fi = IFormats(self.context)
        f = fi.setFormats(self.request)
                
        referer = self.request.get("HTTP_REFERER", "")
        if referer.find("thank-you") != -1:
            url = referer
        else:
            url = self.context.absolute_url()
                            
        self.request.response.redirect(url)